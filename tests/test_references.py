"""Offline tests for scripts/check_references.py (citation extraction and registry checks)."""
import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("check_references", ROOT / "scripts" / "check_references.py")
C = importlib.util.module_from_spec(spec)
sys.modules["check_references"] = C
spec.loader.exec_module(C)


def cites(text, code=False, path="01_X/01_a.ipynb"):
    return [(c.doc, c.locator) for c in C.extract(C.Unit(path, "cell 1", text, code)) if c.locator]


def entry(eid, doc, locator, **kw):
    e = {"id": eid, "doc": doc, "locator": locator, "states": "s", "source": "https://example.org",
         "verification": {"method": kw.pop("method", "official-text"), "checked": "2026-10-29"}, "used_in": []}
    e.update(kw)
    return e


def registry(*entries):
    doc = {"short": "UN R157", "title": "t", "edition": "e", "url": "https://example.org",
           "verification": {"method": "official-text", "checked": "2026-10-29"}}
    docs = {k: dict(doc, short=k) for k in ("UNR157", "ISO26262-9", "ISO21448", "ISO21434", "EU2024/1689")}
    return C.prepare_registry({"documents": docs, "entries": list(entries)})


@pytest.mark.parametrize("raw, norm", [
    ("§ 5.5.1.", "5.5.1"), ("clause 6", "6"), ("Art. 6 (1)", "Art. 6(1)"), ("Articles 102–109", "Art. 102-109"),
    ("6.4.1(c)", "6.4.1(c)"), ("5.4.4.1.", "5.4.4.1"),
])
def test_normalise(raw, norm):
    assert C.normalise(raw) == norm


def test_expand_range():
    assert C.expand_range("6.1–6.4") == ["6.1", "6.2", "6.3", "6.4"]
    assert C.expand_range("Annex E–H") == ["Annex E", "Annex F", "Annex G", "Annex H"]
    assert C.expand_range("1d–1l") == ["1d–1l"]                 # statute ranges stay as written
    assert C.expand_range("Art. 102–109") == ["Art. 102–109"]


def test_regulation_paragraphs_and_carry_through_a_cell():
    text = ("UN R157 fixes the sequence:\n\n1. **Escalation** at the latest 4 s (§6.4.1(c), §5.4.3.2).\n"
            "2. **MRM** at the earliest 10 s (§5.4.4.1); it ends in standstill (§5.5).")
    assert cites(text) == [("UNR157", "6.4.1(c)"), ("UNR157", "5.4.3.2"), ("UNR157", "5.4.4.1"), ("UNR157", "5.5")]


def test_bare_paragraph_after_document_and_annex_paragraph():
    assert cites('premature MRM (R157 5.4.4.1: earliest 10 s)', code=True) == [("UNR157", "5.4.4.1")]
    assert ("UNR157", "Annex 4 3.4.4") in cites("For UN R157 they are inspected under Annex 4 (§3.4.4).")


def test_iso_parts_clauses_and_lists():
    assert cites("ASIL decomposition (ISO 26262-9:2018, clause 5) and DFA (clause 7).") == [
        ("ISO26262-9", "5"), ("ISO26262-9", "7")]
    assert cites("ISO 26262 requires safety analyses at system level (Part 9, clause 8).") == [("ISO26262-9", "8")]
    assert cites("ISO/SAE 21434:2021 (cl. 9, 15; Annexes E–H)") == [
        ("ISO21434", "9"), ("ISO21434", "15"), ("ISO21434", "Annex E"), ("ISO21434", "Annex F"),
        ("ISO21434", "Annex G"), ("ISO21434", "Annex H")]


def test_articles_attach_to_the_act_named_later_in_the_sentence():
    assert cites("Under Art. 2(2), only a limited set of provisions of the AI Act applies.") == [
        ("EU2024/1689", "Art. 2(2)")]


def test_no_false_documents():
    assert cites("The KITTI metric AP|R40 is used; see §4 and §4.5 of this notebook.") == []
    assert cites("Table 1 of the systematic review (Schneier, 1999).") == []


def test_unregistered_and_fact_consistency():
    reg = registry(
        entry("mrm-standstill", "UNR157", "5.5.1"),
        entry("mrm-decel", "UNR157", "5.5.2", fact=r"\b4(?:\.0)?\s?m/s(?:²|\^2|2\b)", superseded_locators=["5.5.1"]),
    )
    units = [C.Unit("07_X/01_a.ipynb", "cell 1", "The MRM aims at ≤ 4.0 m/s² (R157 §5.5.2)."),
             C.Unit("07_X/03_b.ipynb", "cell 2", "UN R157: aiming at not more than 4.0 m/s² (§5.5.1)."),
             C.Unit("07_X/03_b.ipynb", "cell 3", "UN R157 §9.9.9 is not registered.")]
    rep = C.check(reg, C.extract_all(units))
    assert [(c.doc, c.locator) for c in rep.unregistered] == [("UNR157", "9.9.9")]
    assert len(rep.errors) == 1 and "mrm-decel" in rep.errors[0] and "5.5.1 in 07_X/03_b.ipynb" in rep.errors[0]
    assert "earlier edition" in rep.errors[0]
    assert rep.used_in["mrm-decel"] == ["07_X/01_a.ipynb"]


def test_fact_ignores_citations_across_a_semicolon():
    reg = registry(entry("mrm-10s", "UNR157", "5.4.4.1", fact=r"\b10\s?s\b"), entry("crit", "UNR157", "6.1.3.1"))
    units = [C.Unit("03_X/05_a.ipynb", "cell 1", 'checks ("two availability criteria (R157 6.1.3.1); MRM after 10 s")',
                    is_code=True)]
    assert C.check(reg, C.extract_all(units)).errors == []


def test_registry_resolution_prefers_a_registered_document():
    reg = registry(entry("sotif-ops", "ISO21448", "13"))
    text = ("The catalogue of the SOTIF analysis (ISO 21448 clauses 6–7) and the data specification (ISO/PAS 8800); "
            "field-reported cases (clause 13) are added.")
    rep = C.check(reg, C.extract_all([C.Unit("02_X/02_a.ipynb", "cell 1", text)]))
    assert rep.used_in.get("sotif-ops") == ["02_X/02_a.ipynb"]


def test_unverified_entries_are_reported():
    rep = C.check(registry(entry("t9", "ISO26262-9", "Table 9", method="unverified")), [])
    assert rep.unverified and rep.unverified[0].startswith("t9")


def test_validate_registry_flags_bad_entries():
    reg = registry(entry("a", "UNR157", "1"), entry("a", "NOPE", "2", method="maybe"))
    problems = C.validate_registry(reg)
    assert any("duplicate" in p for p in problems) and any("unknown document" in p for p in problems)
    assert any("verification.method" in p for p in problems)


def test_course_registry_is_well_formed():
    pytest.importorskip("yaml")
    reg = C.load_registry()
    assert C.validate_registry(reg) == []
    for e in reg["entries"]:
        assert e["source"].startswith("http"), e["id"]


def test_index_page_lists_entries(tmp_path):
    reg = registry(entry("mrm-decel", "UNR157", "5.5.2"))
    rep = C.check(reg, C.extract_all([C.Unit("07_X/01_a.ipynb", "cell 1", "UN R157 §5.5.2 applies.")]))
    text = C.write_index(reg, rep, tmp_path / "references.md")
    assert "| 5.5.2 |" in text and "[07-01](../07_X/01_a.ipynb)" in text
