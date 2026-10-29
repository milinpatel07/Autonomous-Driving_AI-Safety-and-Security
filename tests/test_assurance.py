"""Offline tests for avsafety.assurance (continuous assurance / safety case as code)."""
import json
import datetime as dt
from pathlib import Path

import pytest

from avsafety import assurance as A

ROOT = Path(__file__).resolve().parents[1]


# --------------------------------------------------------------------------- helpers
def make_repo(tmp_path, code="x = 1"):
    (tmp_path / "pyproject.toml").write_text('[project]\nname = "avsafety"\n')
    nb = {"cells": [{"cell_type": "markdown", "source": "# T"}, {"cell_type": "code", "source": code, "outputs": []}],
          "metadata": {}, "nbformat": 4, "nbformat_minor": 5}
    (tmp_path / "nb.ipynb").write_text(json.dumps(nb))
    return tmp_path


def write_nb_code(repo, code):
    nb = json.loads((repo / "nb.ipynb").read_text())
    nb["cells"][1]["source"] = code
    (repo / "nb.ipynb").write_text(json.dumps(nb))


def rec(eid, repo=None, **values):
    return A.record_evidence(eid, notebook="nb.ipynb", dataset="test", licence="n/a",
                             evidence_dir=(repo / "ev") if repo else None, write=repo is not None, **values)


def small_case(repo=None):
    nodes = [
        A.Node("G1", "Goal", "Top claim for {SG-01.asil}", supported_by=["S1"], in_context_of=["C1"]),
        A.Node("C1", "Context", "Scope"),
        A.Node("S1", "Strategy", "Argue over parts", supported_by=["G2", "G3"]),
        A.Node("G2", "Goal", "Part A", supported_by=["Sn2"], in_context_of=["A2"]),
        A.Node("A2", "Assumption", "Independence"),
        A.Node("Sn2", "Solution", "Test A", evidence="ev-a", criterion="recall_lower_95 >= 0.90"),
        A.Node("G3", "Goal", "Part B", supported_by=["Sn3"]),
        A.Node("Sn3", "Solution", "Test B", evidence="ev-b", criterion="high <= threshold", refute="low > threshold"),
    ]
    hara = {"hazardous_events": {"HE-1": {"S": "S3", "E": "E4", "C": "C3", "goal": "SG-01"},
                                 "HE-2": {"S": "S3", "E": "E2", "C": "C2", "goal": "SG-02"}},
            "safety_goals": {"SG-01": {"ftti_ms": 300}, "SG-02": {"ftti_ms": 500}}}
    return A.AssuranceCase(nodes, name="t", hara=hara, tara={"threats": {"TS-1": {"impact": "Severe", "attack_vector": "Physical"}}},
                           root=repo, evidence_dir=(repo / "ev") if repo else None)


def evidence(a=0.95, high=0.08, low=0.03, thr=0.10):
    return {"ev-a": dict(rec("ev-a", recall_lower_95=a)), "ev-b": dict(rec("ev-b", high=high, low=low, threshold=thr))}


# --------------------------------------------------------------------------- criteria
@pytest.mark.parametrize("crit,values,expected", [
    ("exists", {"x": 1}, True),
    ("x >= 0.9", {"x": 0.95}, True),
    ("x >= 0.9", {"x": 0.85}, False),
    ("x < y", {"x": 1, "y": 2}, True),
    ("ok", {"ok": True}, True),
    ("not ok", {"ok": True}, False),
    ("x == \"D\"", {"x": "D"}, True),
    ("x != null", {"x": None}, False),
    ("x != null", {"x": 40}, True),
    ("d in [[\"B(D)\", \"B(D)\"]]", {"d": ["B(D)", "B(D)"]}, True),
    ("a >= 1 and b <= 2", {"a": 1, "b": 3}, False),
    ("x not in [1, 2]", {"x": 3}, True),
])
def test_criteria(crit, values, expected):
    assert A.evaluate_criterion(crit, values)[0] is expected


def test_criterion_missing_metric_and_reference():
    assert A.evaluate_criterion("y >= 1", {"x": 1})[0] is None
    assert A.evaluate_criterion("x >= nowhere", {"x": 1})[0] is None
    assert A.evaluate_criterion("x == SG-01.asil", {"x": "D"}, {"SG-01.asil": "D"})[0] is True


@pytest.mark.parametrize("bad", ["", "x >=", "not x >= 1", ">= 3"])
def test_criterion_parse_errors(bad):
    with pytest.raises(A.CriterionError):
        A.parse_criterion(bad)


# --------------------------------------------------------------------------- normative values
def test_derived_values_come_from_iso_tables():
    d = small_case().derived()
    assert d["SG-01.asil"] == "D" and d["SG-02.asil"] == "A"
    assert d["SG-01.pmhf_target_per_h"] == 1e-8
    assert ["B(D)", "B(D)"] in d["SG-01.decompositions"]
    assert d["TS-1.cal"] == 2  # Severe + Physical (ISO/SAE 21434 Annex E, as in avsafety.iso21434)
    assert small_case().text("G1") == "Top claim for D"


def test_aeb_case_derived_values_match_hara():
    pytest.importorskip("yaml")
    case = A.load_case(ROOT / "safety_case" / "aeb_pedestrian.yaml")
    d = case.derived()
    assert (d["SG-01.asil"], d["SG-01.ftti_ms"], d["SG-02.asil"], d["SG-02.ftti_ms"]) == ("D", 300, "B", 500)
    assert [d[f"TS-0{i}.cal"] for i in range(1, 5)] == [4, 4, 2, 2]


# --------------------------------------------------------------------------- propagation
def test_all_supported_and_assumed():
    ev = small_case().evaluate(evidence(), check_hashes=False)
    assert ev["Sn2"].status == "supported" and ev["Sn3"].status == "supported"
    assert ev["A2"].status == "assumed"
    assert ev["G2"].status == "assumed"            # P3: unverified assumption in context
    assert ev["G3"].status == "supported"
    assert ev["G1"].status == "assumed"
    assert ev["C1"].status == "context"
    assert ev["G1"].confidence == "2|3"            # two checks passed, one assumption not eliminated


def test_challenged_child_challenges_all_ancestors():
    ev = small_case().evaluate(evidence(a=0.80), check_hashes=False)
    assert ev["Sn2"].status == "challenged"
    assert [ev[n].status for n in ("G2", "S1", "G1")] == ["challenged"] * 3
    assert ev["G3"].status == "supported"
    assert "Sn2" in ev["G2"].reason


def test_refute_gives_inconclusive_then_challenged():
    ev = small_case().evaluate(evidence(high=0.12, low=0.03), check_hashes=False)
    assert ev["Sn3"].status == "inconclusive" and ev["G1"].status == "inconclusive"
    ev = small_case().evaluate(evidence(high=0.20, low=0.11), check_hashes=False)
    assert ev["Sn3"].status == "challenged" and ev["G1"].status == "challenged"


def test_worst_status_order():
    assert A.worst(["supported", "stale", "inconclusive"]) == "stale"
    assert A.worst(["missing", "challenged", "stale"]) == "challenged"
    assert A.worst([]) == "supported"
    assert A.STATUSES[0] == "supported" and A.STATUSES[-1] == "challenged"


def test_missing_evidence_and_undeveloped():
    case = small_case()
    case.nodes["G3"].supported_by = []
    case.nodes["G3"].undeveloped = True
    ev = case.evaluate({"ev-a": dict(rec("ev-a", other=1))}, check_hashes=False)
    assert ev["Sn2"].status == "missing"                       # metric not in evidence
    assert ev["G3"].status == "undeveloped"
    assert ev["G1"].status == "missing"                        # missing is worse than undeveloped


def test_checked_assumption_can_be_challenged():
    case = small_case()
    case.nodes["A2"].evidence, case.nodes["A2"].criterion = "ev-a", "recall_lower_95 >= 0.99"
    ev = case.evaluate(evidence(a=0.95), check_hashes=False)
    assert ev["Sn2"].status == "supported" and ev["A2"].status == "challenged"
    assert ev["G2"].status == "challenged"                     # undercutting defeater


def test_age_rule_makes_evidence_stale():
    case = small_case()
    case.nodes["Sn3"].max_age_days = 30
    e = evidence()
    e["ev-b"]["data_until"] = "2026-01-31"
    assert case.evaluate(e, as_of=dt.date(2026, 2, 20), check_hashes=False)["Sn3"].status == "supported"
    assert case.evaluate(e, as_of=dt.date(2026, 6, 1), check_hashes=False)["Sn3"].status == "stale"


# --------------------------------------------------------------------------- staleness and recording
def test_record_evidence_writes_in_repo_and_hash_staleness(tmp_path, monkeypatch):
    repo = make_repo(tmp_path)
    monkeypatch.chdir(repo)
    monkeypatch.delenv("AVSAFETY_EVIDENCE_DIR", raising=False)
    r = A.record_evidence("ev-a", notebook="nb.ipynb", dataset="d", licence="l", recall_lower_95=0.95)
    assert (repo / "safety_case" / "evidence" / "ev-a.json").is_file()
    assert r["producer"]["code_hash"] == A.notebook_code_hash(repo / "nb.ipynb")
    assert A.validate_evidence(json.loads((repo / "safety_case" / "evidence" / "ev-a.json").read_text())) == []
    rec("ev-a", repo, recall_lower_95=0.95)
    rec("ev-b", repo, high=0.05, low=0.01, threshold=0.1)
    case = small_case(repo)
    assert case.evaluate()["Sn2"].status == "supported"
    assert not [i for i in case.check() if i.level == "error"]
    write_nb_code(repo, "x = 2  # detector update")
    ev = case.evaluate()
    assert ev["Sn2"].status == "stale" and ev["G1"].status == "stale"
    assert any("stale" in i.message for i in case.check() if i.level == "error")
    assert case.evaluate(check_hashes=False)["Sn2"].status == "supported"


def test_hash_ignores_outputs_and_markdown(tmp_path):
    repo = make_repo(tmp_path)
    h = A.notebook_code_hash(repo / "nb.ipynb")
    nb = json.loads((repo / "nb.ipynb").read_text())
    nb["cells"][0]["source"] = "# Changed title"
    nb["cells"][1]["outputs"] = [{"output_type": "stream", "name": "stdout", "text": "1"}]
    (repo / "nb.ipynb").write_text(json.dumps(nb))
    assert A.notebook_code_hash(repo / "nb.ipynb") == h


def test_record_evidence_outside_repo_never_writes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("AVSAFETY_EVIDENCE_DIR", raising=False)
    r = A.record_evidence("colab-run", notebook="nb.ipynb", dataset="d", value=1)
    assert r["values"] == {"value": 1} and r["producer"]["code_hash"] is None
    assert not list(tmp_path.rglob("*.json"))
    assert "not written" in repr(r)


def test_record_evidence_converts_numpy_and_env_dir(tmp_path, monkeypatch):
    np = pytest.importorskip("numpy")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("AVSAFETY_EVIDENCE_DIR", str(tmp_path / "out"))
    r = A.record_evidence("np-test", notebook="nb.ipynb", dataset="d", a=np.float64(0.1234567891), b=np.int64(3),
                          c=np.bool_(True), d=np.array([1, 2]), e=float("nan"), f=("B(D)", "B(D)"))
    assert r["values"] == {"a": 0.123457, "b": 3, "c": True, "d": [1, 2], "e": None, "f": ["B(D)", "B(D)"]}
    assert json.loads((tmp_path / "out" / "np-test.json").read_text())["values"]["c"] is True


# --------------------------------------------------------------------------- integrity and serialisation
def test_check_finds_structural_errors():
    case = small_case()
    case.nodes["S1"].supported_by.append("Sn2")                   # Strategy -> Solution not permitted
    case.nodes["G3"].in_context_of.append("Sn3")                  # InContextOf to a solution
    case.nodes["Sn3"].criterion = "high <="                        # does not parse
    case.nodes["G1"].text += " {SG-09.asil}"                      # unknown placeholder
    msgs = " | ".join(str(i) for i in case.check(evidence()))
    for part in ("Strategy --SupportedBy--> Solution", "InContextOf--> Solution", "cannot parse", "SG-09.asil"):
        assert part in msgs


def test_check_reports_missing_evidence_and_unused_files():
    e = evidence()
    e["orphan"] = dict(rec("orphan", x=1))
    del e["ev-b"]
    issues = small_case().check(e)
    assert any(i.level == "error" and "ev-b.json does not exist" in i.message for i in issues)
    assert any(i.level == "warning" and i.node == "orphan" for i in issues)


def test_yaml_round_trip(tmp_path):
    pytest.importorskip("yaml")
    case = small_case()
    A.save_case(case, tmp_path / "c.yaml")
    back = A.load_case(tmp_path / "c.yaml", evidence_dir=tmp_path)
    assert back.to_dict() == case.to_dict()
    e = evidence(a=0.8)
    assert {k: v.status for k, v in back.evaluate(e, check_hashes=False).results.items()} == \
           {k: v.status for k, v in case.evaluate(e, check_hashes=False).results.items()}


def test_unknown_node_field_is_rejected():
    with pytest.raises(ValueError):
        A.AssuranceCase.from_dict({"nodes": [{"id": "G1", "type": "Goal", "text": "t", "evidense": "x"}]})


def test_diff_names_flipped_claims_and_changed_values():
    old = small_case().evaluate(evidence(a=0.95), check_hashes=False)
    new = small_case().evaluate(evidence(a=0.80), check_hashes=False)
    flips = {f["node"]: f for f in A.diff(old, new)}
    assert set(flips) == {"Sn2", "G2", "S1", "G1"}
    assert flips["Sn2"]["changes"] == ["recall_lower_95: 0.95 -> 0.8"]
    assert A.diff(old, old) == []


# --------------------------------------------------------------------------- rendering
def test_renderers_smoke():
    ev = small_case().evaluate(evidence(a=0.8, high=0.12), check_hashes=False)
    md = ev.to_markdown()
    assert "| Sn2 | Solution |" in md and "**challenged**" in md and "**inconclusive**" in md
    mm = ev.to_mermaid()
    assert mm.startswith("flowchart TD") and ":::challenged" in mm and "-.->" in mm
    svg = ev.to_svg(title="t")
    assert svg.startswith("<svg") and svg.rstrip().endswith("</svg>") and "CHALLENGED" in svg and "INCONCLUSIVE" in svg
    import xml.dom.minidom
    xml.dom.minidom.parseString(svg)                               # well-formed XML
    assert "<circle" in small_case().evaluate(evidence(), check_hashes=False).to_svg(root="G2")


def test_committed_aeb_case_is_consistent():
    pytest.importorskip("yaml")
    case = A.load_case(ROOT / "safety_case" / "aeb_pedestrian.yaml")
    errors = [i for i in case.check() if i.level == "error" and "stale" not in i.message]
    assert errors == []
    ev = case.evaluate(check_hashes=False)
    assert ev.top.status == "challenged"                          # intentionally "do not release"
    assert ev["G2.1"].status in ("supported", "assumed") and ev["G3.1"].status == "challenged"
