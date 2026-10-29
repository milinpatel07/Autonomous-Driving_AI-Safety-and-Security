#!/usr/bin/env python3
"""Check the course's normative citations against references/normative.yaml.

The registry lists every clause, paragraph, table, annex or article of a standard or regulation that
the course relies on, with what the course states, where it was verified and how. This script

  * extracts citations such as "R157 §5.5.2", "ISO 26262-3:2018, clause 6", "ISO 21448 clause 7",
    "Part 9", "Table 4", "Annex 4 §3.4.4" or "Art. 6(1)" from notebooks (markdown and code),
    templates, site pages and the toolkit's docstrings, and maps them to registry entries;
  * warns about citations that are not in the registry (``--strict`` turns these into errors);
  * reports registry entries that are marked ``unverified``;
  * fails when the same fact (an entry with a ``fact`` pattern) is cited with a paragraph or clause
    number that differs from the registered one, e.g. the R157 MRM deceleration limit cited as
    §5.5.1 in one notebook and §5.5.2 in another;
  * writes the citation index (``--index``) and refreshes the computed ``used_in`` lists
    (``--update-used-in``).

It is offline and takes about a second.

Usage
  python scripts/check_references.py                 # report; exit 1 on errors
  python scripts/check_references.py --strict        # unregistered citations are errors too
  python scripts/check_references.py --index         # also write site/references.md
  python scripts/check_references.py --update-used-in
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[1]
FACT_WINDOW = 120   # characters between a fact (e.g. "4.0 m/s²") and the paragraph cited for it
REGISTRY = ROOT / "references" / "normative.yaml"
INDEX_PAGE = ROOT / "site" / "references.md"

# --------------------------------------------------------------------------------------------
# Document mentions. Each pattern yields a document key; registry documents are keyed the same way.
# --------------------------------------------------------------------------------------------
DOC_PATTERNS: List[Tuple[re.Pattern, object]] = [
    # ISO / ISO-SAE / ISO-PAS / ISO-TS / ISO-IEC-TR documents, with optional part and year.
    (re.compile(r"\bISO(?:/(?:SAE|PAS|TS|TR|IEC))*(?:\s(?:TS|PAS|TR))?\s?(\d{4,5})(?:-(\d{1,2}))?(?::(\d{4}))?(?!\d)"),
     lambda m: f"ISO{m.group(1)}" + (f"-{m.group(2)}" if m.group(2) else "")),
    (re.compile(r"\bUL\s?4600\b"), "UL4600"),
    (re.compile(r"\bSAE\s?J(\d{4})\b"), lambda m: f"SAEJ{m.group(1)}"),
    (re.compile(r"\bIEC\s?(\d{5})(?:-(\d{1,2}))?\b"), lambda m: f"IEC{m.group(1)}" + (f"-{m.group(2)}" if m.group(2) else "")),
    # UN Regulations: "UN R157", "R157", "UN Regulation No. 157", "Regulation No 155".
    (re.compile(r"(?<![\w/|])(?:UN(?:ECE)?[\s-]?)?R\s?(\d{2,3})(?![\w])"), lambda m: f"UNR{m.group(1)}"),
    (re.compile(r"\bRegulation No\.?\s?(\d{2,3})\b"), lambda m: f"UNR{m.group(1)}"),
    # EU acts: "(EU) 2022/1426", "Reg. (EU) 2024/1689", "EU 2022/1426", bare "2019/2144".
    (re.compile(r"(?<![\w/.])(20[12]\d)/(\d{3,4})(?![\w/])"), lambda m: f"EU{m.group(1)}/{m.group(2)}"),
    (re.compile(r"\bAI Act\b"), "EU2024/1689"),
    (re.compile(r"\bCyber Resilience Act\b"), "EU2024/2847"),
    (re.compile(r"\bGeneral Safety Regulation\b"), "EU2019/2144"),
    (re.compile(r"\b(?:SGO|Standing General Order)\b"), "NHTSA-SGO"),
    (re.compile(r"\bStVG\b|Straßenverkehrsgesetz"), "DE-StVG"),
    (re.compile(r"\bStVO\b|Straßenverkehrs-Ordnung"), "DE-StVO"),
    (re.compile(r"\bAFGBV\b"), "DE-AFGBV"),
    # datasets the notebooks download (watched by watch_sources.py)
    (re.compile(r"\bKITTI\b|\bkitti_(?:object|tracking)"), "KITTI"),
    (re.compile(r"\bNGSIM\b|\bngsim\("), "NGSIM"),
    (re.compile(r"\bROAD\b(?= (?:dataset|CAN|data))|\broad_metadata\(|\bcan_ids\("), "ROAD"),
    (re.compile(r"\bVeReMi\b|\bveremi\("), "VEREMI"),
    (re.compile(r"\bnhtsa_sgo\("), "NHTSA-SGO"),
]

NUM = r"\d+[a-z]?(?:\.\d+)*"
SUB = r"(?:\s?\((?:[a-z]|[ivx]+|\d+)\))*"
RANGE = rf"(?:\s?[–-]\s?§?{NUM})?"
LIST_ITEM = re.compile(rf"(?:,\s?|\s(?:and|or)\s)(?!§)({NUM}{SUB}{RANGE})(?![\w%])")

LOCATOR_PATTERNS: Dict[str, re.Pattern] = {
    "sect": re.compile(rf"§§?\s?({NUM}\.?{SUB}{RANGE})"),
    "para": re.compile(rf"\b(?:[Pp]aragraphs?|[Pp]aras?\.?)\s({NUM}\.?{SUB}{RANGE})"),
    "clause": re.compile(rf"\b(?:[Cc]lauses?|cl\.)\s?({NUM}{SUB}{RANGE})"),
    "table": re.compile(r"\bTables?\s([A-Z]?\d+(?:\.\d+)?|[A-H]\b)"),
    "annex": re.compile(r"\bAnnex(?:es)?\s((?:[IVX]{1,4}|[A-Z]|\d{1,2})(?:\s?[–-]\s?(?:[IVX]{1,4}|[A-Z]))?)\b"
                        r"(?:,?\s(Part|Section)\s([A-Z0-9]+))?"),
    "part": re.compile(r"\bPart\s(\d{1,2})\b"),
    "article": re.compile(r"\b(?:Articles?|Arts?\.?)\s?(\d{1,3}[a-z]?(?:\(\d+\))?(?:\([a-z]\))?(?:\s?[–-]\s?\d{1,3})?)"),
    "chapter": re.compile(r"\bChapter\s([IVX]+)(?:,?\sSection\s(\d+))?"),
}
URL = re.compile(r"https?://\S+|\]\([^)]*\)")
HARD_BREAK = re.compile(r"\n\s*\n|\n(?=\s*(?:[-*+]|\d+\.|\|)\s)|\|")
SENT_BREAK = re.compile(r"(?<=[.!?])\s+(?=[A-Z*_(\[])")


@dataclass
class Citation:
    path: str
    unit: str          # "cell 12", "line 40" ...
    doc: str
    locator: Optional[str]
    kind: str
    pos: int
    text: str          # the sentence, for messages
    sentence: Tuple[int, int] = (0, 0)
    alts: List[str] = field(default_factory=list)   # other documents the locator could belong to
    raw: str = ""                                    # the sentence as written (same offsets as `sentence`)


@dataclass
class Unit:
    path: str
    name: str
    text: str
    is_code: bool = False


@dataclass
class Report:
    citations: List[Citation] = field(default_factory=list)
    unregistered: List[Citation] = field(default_factory=list)
    ambiguous: List[Citation] = field(default_factory=list)
    unverified: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    used_in: Dict[str, List[str]] = field(default_factory=dict)
    registry_problems: List[str] = field(default_factory=list)


# --------------------------------------------------------------------------------------------
# Registry
# --------------------------------------------------------------------------------------------
def load_registry(path: Path = REGISTRY) -> dict:
    import yaml  # lazy: only this script needs PyYAML

    return prepare_registry(yaml.safe_load(path.read_text(encoding="utf-8")))


def prepare_registry(data: dict) -> dict:
    """Pre-compute normalised locators and compiled patterns of a parsed registry."""
    docs = data.get("documents", {})
    entries = data.get("entries", [])
    for e in entries:
        e["_locators"] = {normalise(e["locator"])} | {normalise(x) for x in e.get("also", [])}
        e["_superseded"] = {normalise(x) for x in e.get("superseded_locators", [])}
        e["_fact_ok"] = e["_locators"] | {normalise(x) for x in e.get("fact_locators", [])}
        e["_fact"] = re.compile(e["fact"], re.I) if e.get("fact") else None
        e["_context"] = re.compile(e["context"], re.I) if e.get("context") else None
    data["documents"], data["entries"] = docs, entries
    return data


def validate_registry(reg: dict) -> List[str]:
    problems = []
    seen = set()
    methods = {"official-text", "official-summary", "secondary", "unverified"}
    for e in reg["entries"]:
        eid = e.get("id", "?")
        if eid in seen:
            problems.append(f"duplicate entry id {eid}")
        seen.add(eid)
        for k in ("id", "doc", "locator", "states", "source", "verification"):
            if k not in e:
                problems.append(f"{eid}: missing field '{k}'")
        if e.get("doc") not in reg["documents"]:
            problems.append(f"{eid}: unknown document '{e.get('doc')}'")
        v = e.get("verification") or {}
        if v.get("method") not in methods:
            problems.append(f"{eid}: verification.method must be one of {sorted(methods)}")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(v.get("checked", ""))):
            problems.append(f"{eid}: verification.checked must be an ISO date")
    for key, d in reg["documents"].items():
        v = d.get("verification") or {}
        if v.get("method") not in methods:
            problems.append(f"document {key}: verification.method must be one of {sorted(methods)}")
        for k in ("short", "title", "edition", "url"):
            if k not in d:
                problems.append(f"document {key}: missing field '{k}'")
    return problems


def normalise(loc: Optional[str]) -> Optional[str]:
    """Canonical form of a locator: '§ 5.5.1.' -> '5.5.1', 'clause 6' -> '6', 'Art. 6 (1)' -> 'Art. 6(1)'."""
    if loc is None:
        return None
    s = str(loc).strip().replace("–", "-")
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"^(?:§§?|paragraphs?|paras?\.?|clauses?|cl\.)\s?", "", s, flags=re.I)
    s = re.sub(r"\s?-\s?§?", "-", s)
    s = re.sub(r"\s?\(", "(", s)
    s = re.sub(r"(?<=\d)\.(?=$|\(|-)", "", s)              # trailing dots of UNECE numbering
    s = re.sub(r"^(?:Articles?|Arts?\.?)\s?", "Art. ", s)
    return s


def base_locator(loc: str) -> str:
    """'6.4.1(c)' -> '6.4.1', 'Art. 6(1)(c)' -> 'Art. 6(1)'."""
    if loc.startswith("Art. "):
        return re.sub(r"(\(\d+\))\([a-z]\)$", r"\1", loc)
    return re.sub(r"(\((?:[a-z]|[ivx]+|\d+)\))+$", "", loc)


# --------------------------------------------------------------------------------------------
# Sources
# --------------------------------------------------------------------------------------------
def iter_units(root: Path = ROOT) -> Iterator[Unit]:
    for nb in sorted(root.glob("[0-9][0-9]_*/*.ipynb")):
        rel = nb.relative_to(root).as_posix()
        cells = json.loads(nb.read_text(encoding="utf-8")).get("cells", [])
        for i, c in enumerate(cells):
            src = c.get("source", "")
            src = "".join(src) if isinstance(src, list) else src
            yield Unit(rel, f"cell {i}", src, c.get("cell_type") == "code")
    for md in sorted(root.glob("templates/*.md")) + sorted(root.glob("site/*.md")):
        if md == INDEX_PAGE:
            continue
        yield Unit(md.relative_to(root).as_posix(), "file", md.read_text(encoding="utf-8"))
    for py in sorted(root.glob("avsafety/*.py")):
        yield Unit(py.relative_to(root).as_posix(), "file", py.read_text(encoding="utf-8"), True)


def blank(text: str, pattern: re.Pattern) -> str:
    return pattern.sub(lambda m: " " * len(m.group(0)), text)


def spans(text: str, breaker: re.Pattern) -> List[Tuple[int, int]]:
    out, start = [], 0
    for m in breaker.finditer(text):
        out.append((start, m.start()))
        start = m.end()
    out.append((start, len(text)))
    return out


def find_span(pos: int, sp: Sequence[Tuple[int, int]]) -> int:
    for i, (a, b) in enumerate(sp):
        if a <= pos <= b:
            return i
    return len(sp) - 1


# --------------------------------------------------------------------------------------------
# Extraction
# --------------------------------------------------------------------------------------------
def doc_mentions(text: str) -> List[Tuple[int, int, str]]:
    found = []
    for pat, key in DOC_PATTERNS:
        for m in pat.finditer(text):
            k = key(m) if callable(key) else key
            found.append((m.start(), m.end(), k))
    found.sort()
    # drop mentions contained in a longer one (e.g. "2024/1689" inside "Regulation No")
    out: List[Tuple[int, int, str]] = []
    for s, e, k in found:
        if out and s < out[-1][1]:
            continue
        out.append((s, e, k))
    return out


def locator_matches(text: str) -> List[Tuple[int, int, str, str]]:
    found = []
    for kind, pat in LOCATOR_PATTERNS.items():
        for m in pat.finditer(text):
            if kind == "annex":
                loc = f"Annex {m.group(1)}" + (f" {m.group(2)} {m.group(3)}" if m.group(2) else "")
                tail = re.match(r"\s?,?\s?\(?(?:§|paragraph\s|para\.\s)\s?(\d+(?:\.\d+)+)", text[m.end():m.end() + 30])
                end = m.end()
                if tail:
                    loc += f" {tail.group(1)}"
                    end += tail.end()
                found.append((m.start(), end, kind, loc))
                continue
            if kind == "table":
                found.append((m.start(), m.end(), kind, f"Table {m.group(1)}"))
                continue
            if kind == "part":
                found.append((m.start(), m.end(), kind, m.group(1)))
                continue
            if kind == "chapter":
                loc = f"Chapter {m.group(1)}" + (f" Section {m.group(2)}" if m.group(2) else "")
                found.append((m.start(), m.end(), kind, loc))
                continue
            if kind == "article":
                found.append((m.start(), m.end(), kind, "Art. " + m.group(1)))
                continue
            found.append((m.start(), m.end(), kind, m.group(1)))
            # comma lists: "paragraphs 5.1.8, 5.4, 5.5, 6.1-6.4"; "clauses 9, 10 and 11"
            if kind in ("sect", "para", "clause"):
                pos = m.end()
                while True:
                    lm = LIST_ITEM.match(text, pos)
                    if not lm:
                        break
                    found.append((lm.start(1), lm.end(1), kind, lm.group(1)))
                    pos = lm.end()
    found.sort()
    # an annex match swallows a "§..." it carries; drop the duplicate sect match
    out = []
    for f in found:
        if out and f[0] < out[-1][1] and out[-1][2] == "annex":
            continue
        out.append(f)
    return out


BARE_AFTER_DOC = re.compile(r"\s?,?\s?(\d+\.\d+(?:\.\d+)*(?:\([a-z]\))?)(?![\d.]*\s?(?:%|s\b|m\b|km|m/s))")

# Which locator kinds a document accepts, by the way its key is formed.
STYLE_KINDS = {
    "un": {"sect", "para", "annex", "bare", "table"},       # UN Regulations: numbered paragraphs, Annex 4
    "eu": {"article", "annex", "chapter", "para"},           # EU acts: Art. 6(1), Annex I, Chapter III
    "de": {"sect"},                                          # German statutes: § 1d
    "std": {"clause", "table", "annex", "part"},             # ISO / IEC / SAE / UL: clause 6, Table 4, Annex B
    "none": set(),
}
ANNEX_FORM = {"un": re.compile(r"Annex \d"), "eu": re.compile(r"Annex [IVX]+\b"),
              "std": re.compile(r"Annex [A-Z]\b")}
CARRY_UNIT = {"un": {"sect", "para", "annex"}, "eu": {"article", "chapter", "annex"}, "de": {"sect"}}
CARRY_PARA = {"std": {"clause", "annex", "table", "part"}}


def style(doc: str) -> str:
    if doc.startswith("UNR"):
        return "un"
    if doc.startswith("EU"):
        return "eu"
    if doc.startswith("DE-"):
        return "de"
    if doc.startswith("NHTSA"):
        return "none"
    return "std"


def accepts(doc: str, kind: str, loc: Optional[str]) -> bool:
    st = style(doc)
    if kind not in STYLE_KINDS[st]:
        return False
    if kind == "annex" and loc and st in ANNEX_FORM:
        return bool(ANNEX_FORM[st].match(loc))
    return True


def extract(unit: Unit, prior: Sequence[str] = ()) -> List[Citation]:
    """Citations in one cell or file. Each locator is attached to the document that the sentence names
    (before it, else after it); failing that, a regulation paragraph carries the last regulation named in the
    unit, and a standard's clause carries the last standard named in the same paragraph. ``prior`` lists the
    documents named in earlier cells of the same file; they are the last candidates for regulation paragraphs."""
    text = blank(unit.text, URL)
    hard = spans(text, re.compile(r"\n")) if unit.is_code else spans(text, HARD_BREAK)
    sent = []
    for a, b in hard:
        for sa, sb in spans(text[a:b], SENT_BREAK):
            sent.append((a + sa, a + sb))
    mentions = doc_mentions(text)
    locs = locator_matches(text)
    events = [(s, e, "doc", k, None) for s, e, k in mentions] + [(s, e, "loc", kind, loc) for s, e, kind, loc in locs]
    events.sort(key=lambda x: (x[0], 0 if x[2] == "doc" else 1))
    out: List[Citation] = []
    seen_docs: List[Tuple[str, int]] = []            # (document, position) of every mention so far

    def sentence_of(pos: int) -> Tuple[int, int]:
        return sent[find_span(pos, sent)]

    def make(doc, loc, kind, pos, alts=()):
        s = sentence_of(pos)
        c = Citation(unit.path, unit.name, doc, normalise(loc) if loc else None, kind, pos,
                     re.sub(r"\s+", " ", unit.text[s[0]:s[1]]).strip()[:240], s)
        c.alts = [a for a in dict.fromkeys(alts) if a != doc]
        c.raw = unit.text[s[0]:s[1]]
        out.append(c)

    for i, (s, e, typ, k, loc) in enumerate(events):
        if typ == "doc":
            seen_docs.append((k, s))
            make(k, None, "doc", s)
            bm = BARE_AFTER_DOC.match(text, e)
            if bm and style(k) == "un":
                make(k, bm.group(1), "bare", bm.start(1))
            continue
        kind, sen, para = k, sentence_of(s), find_span(s, hard)
        before = [d for d, p in reversed(seen_docs) if sentence_of(p) == sen]
        after = []
        for s2, _, typ2, k2, _ in events[i + 1:]:
            if s2 > sen[1]:
                break
            if typ2 == "doc":
                after.append(k2)
        carried = [(p, d) for d, p in seen_docs
                   if kind in CARRY_UNIT.get(style(d), ())
                   or (kind in CARRY_PARA.get(style(d), ()) and find_span(p, hard) == para)]
        carried = [d for _, d in sorted(carried, reverse=True)]
        carried += [d for d in reversed(prior) if kind in CARRY_UNIT.get(style(d), ())]
        cands = [d for d in before + after + carried if accepts(d, kind, normalise(loc))]
        if not cands:
            continue
        target = cands[0]
        if kind == "part":
            if target.startswith("ISO26262"):
                newdoc = f"ISO26262-{loc}"
                seen_docs.append((newdoc, s))
                make(newdoc, None, "doc", s)
            continue
        for one in expand_range(loc):
            make(target, one, kind, s, cands[1:])
    return out


def expand_range(loc: str) -> List[str]:
    """'6.1-6.4' -> 6.1 ... 6.4; 'clauses 5-14' -> 5 ... 14; 'Annexes E-H' -> E ... H.
    Article ranges ('Arts 102-109'), statute ranges ('1d-1l') and long ranges are kept as written."""
    n = normalise(loc)
    m = re.fullmatch(r"((?:\d+\.)*)(\d+)-(?:\1)?(\d+)", n or "")
    if m:
        a, b = int(m.group(2)), int(m.group(3))
        if 0 < b - a <= 15:
            return [f"{m.group(1)}{i}" for i in range(a, b + 1)]
    m = re.fullmatch(r"Annex ([A-Z])-([A-Z])", n or "")
    if m and ord(m.group(2)) - ord(m.group(1)) <= 10:
        return [f"Annex {chr(c)}" for c in range(ord(m.group(1)), ord(m.group(2)) + 1)]
    return [loc]


def extract_all(units: Optional[Iterable[Unit]] = None) -> List[Citation]:
    cites: List[Citation] = []
    seen: Dict[str, List[str]] = defaultdict(list)       # documents named so far in each file
    for u in units if units is not None else iter_units():
        found = extract(u, seen[u.path])
        cites.extend(found)
        for c in found:
            if c.kind == "doc" and c.doc not in seen[u.path][-3:]:
                seen[u.path].append(c.doc)
    return cites


# --------------------------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------------------------
def match_entry(c: Citation, by_doc: Dict[str, list], docs: dict) -> Optional[dict]:
    """Registry entry for a citation: the named document first, then the other documents the sentence names,
    then the act an amending act amends (a locator cited with an amending regulation usually belongs to the
    consolidated act)."""
    if c.locator is None:
        return None
    order = [c.doc] + list(c.alts)
    for d in list(order):
        order += docs.get(d, {}).get("amends", [])
    for doc in dict.fromkeys(order):
        for cand in (c.locator, base_locator(c.locator)):
            for e in by_doc.get(doc, []):
                if cand in e["_locators"] and (e["_context"] is None or e["_context"].search(c.text)):
                    return e
    return None


def fact_locator(m: re.Match, same: List[Citation], sen: Tuple[int, int]) -> Optional[Citation]:
    """The citation that gives the paragraph for a fact: the first one after it (within FACT_WINDOW),
    else the nearest one before it, provided no ';' or sentence end separates them."""
    raw = same[0].raw
    after = [x for x in same if 0 <= x.pos - sen[0] - m.start() <= FACT_WINDOW]
    if after:
        return min(after, key=lambda x: x.pos)
    before = [x for x in same if 0 < m.start() - (x.pos - sen[0]) <= FACT_WINDOW]
    for x in sorted(before, key=lambda x: -x.pos):
        gap = raw[x.pos - sen[0]:m.start()]
        return None if re.search(r";|\.\s", gap) else x
    return None


def compatible(cited: str, canonical: set) -> bool:
    """A citation agrees with the registry if it names the same paragraph, a sub-item of it, or a parent."""
    b = base_locator(cited)
    for c in canonical:
        if b == c or c.startswith(b + ".") or b.startswith(c + "."):
            return True
    return False


def check(reg: dict, cites: List[Citation]) -> Report:
    rep = Report(citations=cites)
    rep.registry_problems = validate_registry(reg)
    docs, entries = reg["documents"], reg["entries"]
    by_doc: Dict[str, list] = defaultdict(list)
    for e in entries:
        by_doc[e["doc"]].append(e)
    used: Dict[str, set] = defaultdict(set)

    for c in cites:
        if c.locator is None:
            if c.doc in docs:
                used[f"doc:{c.doc}"].add(c.path)
            continue
        e = match_entry(c, by_doc, docs)
        if e is None and c.doc == "ISO26262" and c.kind in ("clause", "table", "annex"):
            rep.ambiguous.append(c)
            continue
        if e is None:
            if c.doc in docs and docs[c.doc].get("locators") == "none":
                continue
            rep.unregistered.append(c)
            continue
        used[e["id"]].add(c.path)
        c.doc = e["doc"]                                  # resolved document

    # facts: the same fact must carry the registered paragraph everywhere. For every occurrence of a fact
    # pattern, the nearest citation of the same document in that sentence (within FACT_WINDOW characters)
    # is taken as the paragraph the course gives for the fact.
    by_sentence: Dict[Tuple[str, str, Tuple[int, int]], List[Citation]] = defaultdict(list)
    for c in cites:
        if c.locator and c.kind != "doc":
            by_sentence[(c.path, c.unit, c.sentence)].append(c)
    for e in entries:
        fact = e.get("_fact")
        if fact is None:
            continue
        variants: Dict[str, set] = defaultdict(set)
        for (path, _, sen), cs in by_sentence.items():
            same = [x for x in cs if x.doc == e["doc"]]
            if not same:
                continue
            for m in fact.finditer(same[0].raw):
                near = fact_locator(m, same, sen)
                if near is not None:
                    variants[near.locator].add(path)
        bad = {loc: paths for loc, paths in variants.items() if not compatible(loc, e["_fact_ok"])}
        if bad:
            detail = "; ".join(f"{loc} in {', '.join(sorted(p))}" for loc, p in sorted(bad.items()))
            good = "; ".join(f"{loc} in {', '.join(sorted(p))}" for loc, p in sorted(variants.items())
                             if loc not in bad)
            note = " (the paragraph number of an earlier edition)" if any(
                base_locator(x) in e["_superseded"] for x in bad) else ""
            rep.errors.append(f"inconsistent citation of fact '{e['id']}' ({docs[e['doc']]['short']} "
                              f"{e['locator']}: {e['states']}): cited as {detail}{note}"
                              + (f"; cited correctly in {good}" if good else ""))

    for e in entries:
        if e["verification"]["method"] == "unverified":
            rep.unverified.append(f"{e['id']} ({docs[e['doc']]['short']} {e['locator']}): "
                                  f"{e['verification'].get('note', '')}".strip())
    for key, d in docs.items():
        if d["verification"]["method"] == "unverified":
            rep.unverified.append(f"document {key} ({d['short']}): {d['verification'].get('note', '')}")
    rep.used_in = {k: sorted(v) for k, v in used.items()}
    rep.errors = rep.registry_problems + rep.errors
    return rep


# --------------------------------------------------------------------------------------------
# Outputs
# --------------------------------------------------------------------------------------------
def page_name(path: str) -> str:
    p = Path(path)
    m = re.match(r"(\d\d)_", p.parent.name)
    n = re.match(r"(\d\d)_", p.name)
    if m and n and p.suffix == ".ipynb":
        return f"{m.group(1)}-{n.group(1)}"
    return path


def link(path: str) -> str:
    """Markdown link from site/references.md to a citing file (toolkit sources are named, not linked)."""
    if path.endswith(".py"):
        return f"`{path}`"
    target = path[len("site/"):] if path.startswith("site/") else f"../{path}"
    return f"[{page_name(path)}]({target})"


def write_index(reg: dict, rep: Report, out: Path = INDEX_PAGE) -> str:
    docs, entries = reg["documents"], reg["entries"]
    lines = [
        "---", "title: Normative references", "---", "",
        "The course cites clauses, paragraphs and articles of standards and regulations. Each citation is listed",
        "in [`references/normative.yaml`](https://github.com/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/"
        "blob/main/references/normative.yaml) with what the course states, the edition and the source it was "
        "checked against. "
        "`scripts/check_references.py` keeps this page in step with the notebooks; do not edit it by hand.", "",
        "Verification: **official text** = checked against the published text; **official summary** = against",
        "an official table of contents, summary or data dictionary (the full text is paywalled or unavailable);",
        "**secondary** = against a reputable secondary source; **unverified** = not yet checked.", "",
    ]
    by_doc: Dict[str, list] = defaultdict(list)
    for e in entries:
        by_doc[e["doc"]].append(e)
    label = {"official-text": "official text", "official-summary": "official summary",
             "secondary": "secondary", "unverified": "**unverified**"}
    for key, d in docs.items():
        users = rep.used_in.get(f"doc:{key}", [])
        if not by_doc.get(key) and not users:
            continue
        lines += [f"## {d['title']}", "",
                  f"{d['edition']}. Source: <{d['url']}> ({label[d['verification']['method']]}, "
                  f"checked {d['verification']['checked']}).", ""]
        if users:
            lines += ["Cited in: " + ", ".join(link(u) for u in users) + ".", ""]
        rows = sorted(by_doc.get(key, []), key=lambda e: _sort_key(e["locator"]))
        if rows:
            lines += ["| Locator | The course states | Verification | Cited in |", "|---|---|---|---|"]
            for e in rows:
                where = ", ".join(link(u) for u in rep.used_in.get(e["id"], [])) or "—"
                states = e["states"].replace("|", "\\|").replace("\n", " ")
                lines.append(f"| {e['locator']} | {states} | {label[e['verification']['method']]} | {where} |")
            lines.append("")
    text = "\n".join(lines).rstrip() + "\n"
    out.write_text(text, encoding="utf-8")
    return text


def _sort_key(loc: str):
    parts = re.findall(r"\d+|[A-Za-z]+", str(loc))
    return [(0, int(p)) if p.isdigit() else (1, p) for p in parts]


def update_used_in(rep: Report, path: Path = REGISTRY) -> bool:
    """Rewrite the computed ``used_in:`` line of every entry. Returns True if the file changed."""
    text = path.read_text(encoding="utf-8")
    out, current = [], None
    for line in text.split("\n"):
        m = re.match(r"\s*- id:\s*(\S+)", line)
        if m:
            current = m.group(1)
        m2 = re.match(r"(\s*)used_in:", line)
        if m2 and current:
            users = [page_name(p) for p in rep.used_in.get(current, [])]
            line = f"{m2.group(1)}used_in: [{', '.join(users)}]"
        out.append(line)
    new = "\n".join(out)
    if new != text:
        path.write_text(new, encoding="utf-8")
        return True
    return False


def stale_used_in(reg: dict, rep: Report) -> List[str]:
    stale = []
    for e in reg["entries"]:
        want = [page_name(p) for p in rep.used_in.get(e["id"], [])]
        if list(e.get("used_in") or []) != want:
            stale.append(e["id"])
    return stale


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--strict", action="store_true", help="unregistered citations and stale used_in are errors")
    ap.add_argument("--index", action="store_true", help=f"write {INDEX_PAGE.relative_to(ROOT)}")
    ap.add_argument("--update-used-in", action="store_true", help="refresh the computed used_in lists")
    ap.add_argument("--list", action="store_true", help="print every extracted citation")
    ap.add_argument("--json", type=Path, help="write the citation index as JSON (used by watch_sources.py)")
    args = ap.parse_args(argv)

    reg = load_registry()
    rep = check(reg, extract_all())

    if args.list:
        for c in rep.citations:
            if c.locator:
                print(f"{c.path} {c.unit}: {c.doc} {c.locator} [{c.kind}]")
    if args.update_used_in and update_used_in(rep):
        print("updated used_in in", REGISTRY.relative_to(ROOT))
        reg = load_registry()
    if args.index:
        write_index(reg, rep)
        print("wrote", INDEX_PAGE.relative_to(ROOT))
    if args.json:
        args.json.write_text(json.dumps(rep.used_in, indent=1, sort_keys=True), encoding="utf-8")

    n_loc = sum(1 for c in rep.citations if c.locator)
    print(f"{len(reg['entries'])} registry entries, {len(reg['documents'])} documents; "
          f"{n_loc} clause-level citations in {len({c.path for c in rep.citations})} files.")
    for c in rep.unregistered:
        print(f"{'ERROR' if args.strict else 'WARNING'} unregistered citation: {c.path} {c.unit}: "
              f"{c.doc} {c.locator} — \"{c.text[:120]}\"")
    for c in rep.ambiguous:
        print(f"NOTE ambiguous (ISO 26262 part not named): {c.path} {c.unit}: {c.locator}")
    for u in rep.unverified:
        print("WARNING unverified registry entry:", u)
    stale = stale_used_in(reg, rep)
    if stale:
        print(f"{'ERROR' if args.strict else 'WARNING'} used_in out of date for {len(stale)} entries "
              f"(run with --update-used-in): {', '.join(stale[:8])}{' ...' if len(stale) > 8 else ''}")
    for e in rep.errors:
        print("ERROR", e)
    failed = bool(rep.errors) or (args.strict and (rep.unregistered or stale))
    print("FAILED" if failed else "OK")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
