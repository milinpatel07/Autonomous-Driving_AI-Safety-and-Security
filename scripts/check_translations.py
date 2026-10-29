#!/usr/bin/env python3
"""Check the German edition (de/) against the English course.

For every notebook under ``de/``:
  * the English original exists at the same relative path without ``de/``;
  * code cells are byte-identical to the original and in the same order
    (error, with the first differing cell reported);
  * the number of markdown cells matches (warning only);
  * the header follows the German format (title, "Modul NN · ... · Notebook N von M
    (Deutsche Ausgabe)", Colab badge on main pointing at the de/ path, table
    "| Niveau | Voraussetzungen | Normen |", author line, "## Lernziele");
    N and M are compared with the English header (warning only);
  * the footer has "## In der Industrie", "## Kernaussagen", "## Selbsttest" (answers in
    <details>), "## Literatur", and a navigation line that links the English original
    and the edition overview (de/README.md);
  * relative links in markdown cells resolve.

Usage:  python scripts/check_translations.py [--root PATH]   (exit code 1 on any error)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = "milinpatel07/Autonomous-Driving_AI-Safety-and-Security"
COLAB = re.compile(r"colab\.research\.google\.com/github/" + re.escape(REPO) + r"/blob/([^/]+)/([^)\s\"']+\.ipynb)")
MODULE_LINE_DE = re.compile(r"\*\*Modul (\d\d) · [^*]+\*\* · Notebook (\d+) von (\d+) \(Deutsche Ausgabe\)")
MODULE_LINE_EN = re.compile(r"\*\*Module (\d\d) · [^*]+\*\* · Notebook (\d+) of (\d+)")
TABLE_DE = "| Niveau | Voraussetzungen | Normen |"
AUTHOR_DE = "**Autor:** Milin Patel · Hochschule Kempten · MIT-Lizenz"
FOOTER_DE = ["## In der Industrie", "## Kernaussagen", "## Selbsttest", "## Literatur"]
LINK = re.compile(r"\]\(([^)\s]+)\)|href=\"([^\"]+)\"")


def _source(cell) -> str:
    src = cell.get("source", "")
    return "".join(src) if isinstance(src, list) else src


def _cells(path: Path):
    return json.loads(path.read_text(encoding="utf-8")).get("cells", [])


def _first_diff_line(a: str, b: str) -> str:
    la, lb = a.split("\n"), b.split("\n")
    for k, (x, y) in enumerate(zip(la, lb), 1):
        if x != y:
            return f"line {k}: English {x!r} vs German {y!r}"
    return f"line {min(len(la), len(lb)) + 1}: lengths differ ({len(la)} vs {len(lb)} lines)"


def check_notebook(de_path: Path, root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    rel_de = de_path.relative_to(root).as_posix()
    rel_en = de_path.relative_to(root / "de").as_posix()
    en_path = root / rel_en
    if not en_path.exists():
        return [f"{rel_de}: English original {rel_en} not found"], warnings
    de_cells, en_cells = _cells(de_path), _cells(en_path)

    # 1. code cells: identical and in the same order
    de_code = [(i, _source(c)) for i, c in enumerate(de_cells) if c.get("cell_type") == "code"]
    en_code = [(i, _source(c)) for i, c in enumerate(en_cells) if c.get("cell_type") == "code"]
    for k, ((ie, se), (id_, sd)) in enumerate(zip(en_code, de_code)):
        if se != sd:
            errors.append(f"{rel_de}: code drift in code cell #{k + 1} (English cell {ie}, German cell {id_}), "
                          + _first_diff_line(se, sd))
            break
    if len(de_code) != len(en_code):
        errors.append(f"{rel_de}: {len(de_code)} code cells, English original has {len(en_code)}")

    # 2. markdown cell count
    n_md_de = sum(c.get("cell_type") == "markdown" for c in de_cells)
    n_md_en = sum(c.get("cell_type") == "markdown" for c in en_cells)
    if n_md_de != n_md_en:
        warnings.append(f"{rel_de}: {n_md_de} markdown cells, English original has {n_md_en}")

    # 3. header
    if not de_cells or de_cells[0].get("cell_type") != "markdown":
        errors.append(f"{rel_de}: first cell must be the markdown header")
        return errors, warnings
    header = _source(de_cells[0])
    if not header.lstrip().startswith("# "):
        errors.append(f"{rel_de}: header must start with a '# ' title")
    m_de = MODULE_LINE_DE.search(header)
    if not m_de:
        errors.append(f"{rel_de}: header lacks '**Modul NN · <Titel>** · Notebook N von M (Deutsche Ausgabe)'")
    else:
        m_en = MODULE_LINE_EN.search(_source(en_cells[0])) if en_cells else None
        if m_en and m_en.groups() != m_de.groups():
            warnings.append(f"{rel_de}: header says Modul {m_de[1]}, Notebook {m_de[2]} von {m_de[3]}; "
                            f"English says Module {m_en[1]}, Notebook {m_en[2]} of {m_en[3]}")
    badge = COLAB.search(header)
    if not badge:
        errors.append(f"{rel_de}: header lacks an Open-in-Colab badge for {REPO}")
    elif badge.group(1) != "main" or badge.group(2) != rel_de:
        errors.append(f"{rel_de}: Colab badge points to {badge.group(1)}/{badge.group(2)}, expected main/{rel_de}")
    for needle, what in ((TABLE_DE, "table header"), (AUTHOR_DE, "author line"), ("## Lernziele", "'## Lernziele'")):
        if needle not in header:
            errors.append(f"{rel_de}: header lacks the German {what}: {needle}")

    # 4. footer sections, in order, in the markdown after the header
    body = "\n".join(_source(c) for c in de_cells[1:] if c.get("cell_type") == "markdown")
    pos = 0
    for heading in FOOTER_DE:
        m = re.search(r"^" + re.escape(heading) + r"\s*$", body[pos:], re.M)
        if not m:
            errors.append(f"{rel_de}: footer section '{heading}' missing or out of order")
            continue
        if heading == "## Selbsttest" and "<details>" not in body[pos + m.end():]:
            errors.append(f"{rel_de}: '## Selbsttest' needs answers in <details>")
        pos += m.end()
    nav = next((_source(c) for c in reversed(de_cells) if c.get("cell_type") == "markdown"
                and "**Navigation:**" in _source(c)), "")
    if not nav:
        errors.append(f"{rel_de}: no '**Navigation:**' line")
    else:
        depth = "../" * (len(Path(rel_de).parts) - 1)
        for target, what in ((depth + rel_en, "the English original"), ("../README.md", "de/README.md")):
            if f"]({target})" not in nav:
                errors.append(f"{rel_de}: navigation does not link {what} ({target})")

    # 5. relative links in markdown cells
    for i, cell in enumerate(de_cells):
        if cell.get("cell_type") != "markdown":
            continue
        for m in LINK.finditer(_source(cell)):
            target = (m.group(1) or m.group(2) or "").split("#")[0]
            if not target or re.match(r"^[a-z]+:", target) or target.startswith(("/", "{")):
                continue
            if not (de_path.parent / target).resolve().exists():
                errors.append(f"{rel_de} cell {i}: broken relative link -> {target}")
    return errors, warnings


def check(root: Path = ROOT) -> tuple[list[str], list[str], int]:
    errors: list[str] = []
    warnings: list[str] = []
    notebooks = sorted((root / "de").glob("*/*.ipynb")) if (root / "de").is_dir() else []
    for nb in notebooks:
        e, w = check_notebook(nb, root)
        errors += e
        warnings += w
    return errors, warnings, len(notebooks)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=ROOT, help="repository root (default: this repository)")
    args = ap.parse_args(argv)
    errors, warnings, n = check(args.root.resolve())
    print(f"Checked {n} German notebooks against their English originals.")
    for w in warnings:
        print("WARNING", w)
    for e in errors:
        print("ERROR", e)
    print("OK" if not errors else f"{len(errors)} problem(s) found")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
