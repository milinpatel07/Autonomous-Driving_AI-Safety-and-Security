"""Offline tests for scripts/check_translations.py (German edition under de/)."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("check_translations", ROOT / "scripts" / "check_translations.py")
ct = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ct)

REL = "03_Functional_Safety_ISO26262/02_hara.ipynb"
BADGE = ("[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]"
         "(https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/{path})")


def _nb(cells):
    return {"cells": [{"cell_type": t, "metadata": {}, "source": s, **({"outputs": [], "execution_count": None} if t == "code" else {})}
                      for t, s in cells], "metadata": {}, "nbformat": 4, "nbformat_minor": 5}


def _write(path: Path, cells):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_nb(cells)), encoding="utf-8")


def _pair(tmp_path: Path, de_code=("x = 1\n", "print(x)")):
    _write(tmp_path / REL, [
        ("markdown", "# HARA\n\n**Module 03 · Functional Safety** · Notebook 2 of 6\n\n" + BADGE.format(path=REL)),
        ("code", "x = 1\n"), ("markdown", "text"), ("code", "print(x)"),
        ("markdown", "## In industry\n## Key takeaways\n## Self-assessment\n<details></details>\n## References"),
    ])
    header = ("# G&R\n\n**Modul 03 · Funktionale Sicherheit** · Notebook 2 von 6 (Deutsche Ausgabe)\n\n"
              + BADGE.format(path="de/" + REL)
              + "\n\n| Niveau | Voraussetzungen | Normen |\n|---|---|---|\n\n"
              "**Autor:** Milin Patel · Hochschule Kempten · MIT-Lizenz\n\n## Lernziele\n")
    footer = ("## In der Industrie\n## Kernaussagen\n## Selbsttest\n<details></details>\n## Literatur\n\n"
              f"**Navigation:** [Englisches Original](../../{REL}) · [Übersicht](../README.md)")
    _write(tmp_path / "de" / REL, [("markdown", header), ("code", de_code[0]), ("markdown", "Text"),
                                    ("code", de_code[1]), ("markdown", footer)])
    (tmp_path / "de" / "README.md").write_text("# Deutsche Ausgabe\n", encoding="utf-8")


def test_repository_edition_is_consistent():
    errors, _, n = ct.check(ROOT)
    assert n >= 6
    assert errors == []


def test_clean_pair_passes(tmp_path):
    _pair(tmp_path)
    errors, warnings, n = ct.check(tmp_path)
    assert (errors, warnings, n) == ([], [], 1)


def test_code_drift_is_reported_with_cell(tmp_path, capsys):
    _pair(tmp_path, de_code=("x = 1\n", "print(x + 1)"))
    errors, _, _ = ct.check(tmp_path)
    assert len(errors) == 1 and "code cell #2" in errors[0] and "English cell 3, German cell 3" in errors[0]
    assert ct.main(["--root", str(tmp_path)]) == 1
    assert "code drift" in capsys.readouterr().out


def test_missing_original_and_markdown_count(tmp_path):
    _pair(tmp_path)
    nb = json.loads((tmp_path / "de" / REL).read_text(encoding="utf-8"))
    nb["cells"].insert(2, {"cell_type": "markdown", "metadata": {}, "source": "extra"})
    (tmp_path / "de" / REL).write_text(json.dumps(nb), encoding="utf-8")
    errors, warnings, _ = ct.check(tmp_path)
    assert errors == [] and any("markdown cells" in w for w in warnings)
    (tmp_path / REL).unlink()
    errors, _, _ = ct.check(tmp_path)
    assert errors and "not found" in errors[0]


@pytest.mark.parametrize("old, new, expected", [
    ("(Deutsche Ausgabe)", "", "Deutsche Ausgabe"),
    ("blob/main/de/", "blob/main/", "Colab badge"),
    ("| Niveau |", "| Level |", "table header"),
    ("## Selbsttest", "## Self-assessment", "Selbsttest"),
    ("](../README.md)", "](../../README.md)", "de/README.md"),
])
def test_format_violations(tmp_path, old, new, expected):
    _pair(tmp_path)
    p = tmp_path / "de" / REL
    p.write_text(p.read_text(encoding="utf-8").replace(old, new), encoding="utf-8")
    errors, _, _ = ct.check(tmp_path)
    assert any(expected in e for e in errors), errors
