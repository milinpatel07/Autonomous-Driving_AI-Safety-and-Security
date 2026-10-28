import pytest

from avsafety import iso26262 as fs


@pytest.mark.parametrize("s,e,c,expected", [
    ("S3", "E4", "C3", "D"), ("S3", "E4", "C2", "C"), ("S3", "E3", "C3", "C"),
    ("S3", "E4", "C1", "B"), ("S2", "E4", "C3", "C"), ("S1", "E4", "C3", "B"),
    ("S1", "E1", "C3", "QM"), ("S3", "E1", "C3", "A"), ("S2", "E2", "C2", "QM"),
    ("S0", "E4", "C3", "QM"), ("S3", "E0", "C3", "QM"), ("S3", "E4", "C0", "QM"),
    ("s3", "e4", "c3", "D"),
])
def test_asil_table(s, e, c, expected):
    assert fs.determine_asil(s, e, c) == expected


def test_asil_table_shape_and_monotonicity():
    # Raising any of S, E, C never lowers the ASIL.
    for s in ("S1", "S2", "S3"):
        for e in ("E1", "E2", "E3", "E4"):
            ranks = [fs.asil_rank(a) for a in fs.ASIL_TABLE[s][e]]
            assert ranks == sorted(ranks)
    # The table's "sum rule": S+E+C = 10 -> D, 9 -> C, 8 -> B, 7 -> A, else QM
    for s in (1, 2, 3):
        for e in (1, 2, 3, 4):
            for c in (1, 2, 3):
                expected = {10: "D", 9: "C", 8: "B", 7: "A"}.get(s + e + c, "QM")
                assert fs.determine_asil(f"S{s}", f"E{e}", f"C{c}") == expected


@pytest.mark.parametrize("bad", [("S4", "E1", "C1"), ("S1", "E5", "C1"), ("S1", "E1", "X")])
def test_invalid_classes_raise(bad):
    with pytest.raises(ValueError):
        fs.determine_asil(*bad)


def test_decomposition():
    assert ("B(D)", "B(D)") in fs.decomposition_options("D")
    assert len(fs.decomposition_options("D")) == 3
    assert fs.decomposition_options("A") == [("A(A)", "QM(A)")]
    with pytest.raises(ValueError):
        fs.decomposition_options("QM")


def test_hardware_metrics():
    entries = [
        {"rate": 100, "safe": True},
        {"rate": 10, "spf": True},
        {"rate": 890, "dc": 0.99, "dc_latent": 0.9},
    ]
    m = fs.hardware_metrics(entries)
    assert m["SPFM"] == pytest.approx(1 - (10 + 8.9) / 1000)
    latent = 890 * 0.99 * 0.1
    assert m["LFM"] == pytest.approx(1 - latent / (1000 - 10 - 8.9))
    # LFM is not identical to SPFM (a bug found in the original FMEDA notebook)
    assert m["LFM"] != pytest.approx(m["SPFM"])
    assert all(fs.meets_hw_targets(m, "B").values())          # 98.1 % SPFM >= 90 %
    ok = fs.meets_hw_targets(m, "D")
    assert ok == {"SPFM": False, "LFM": True, "PMHF": False}  # 18.9 FIT >= 10 FIT
