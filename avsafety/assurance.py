"""Continuous assurance: a safety case as code.

A GSN-style argument (goals, strategies, solutions, context, assumptions,
justifications) is stored as YAML; each *solution* points to an evidence record
(JSON) that a notebook or a test pipeline writes with :func:`record_evidence`, and
carries an **acceptance criterion** that is fixed in the argument, not by the
producer of the evidence. :meth:`AssuranceCase.evaluate` recomputes the status of
every node from the evidence that exists *now*, so a claim turns *challenged* the
moment its evidence no longer meets the criterion, and *stale* the moment the
code that produced the evidence changes.

Node statuses, from best to worst (``STATUSES``)::

    supported     evidence current and meets its criterion
    assumed       supported, but relies on an assumption without its own evidence
    undeveloped   explicitly marked as still to be developed (open item)
    inconclusive  evidence current, but neither meets the criterion nor refutes it
    stale         evidence exists but its producer code changed, or it is too old
    missing       referenced evidence (or metric) does not exist
    challenged    evidence current and fails the criterion (a rebutting or
                  undermining defeater), or an assumption is contradicted
                  (an undercutting defeater)

Propagation rules (documented and unit-tested):

P1  Solution: missing -> stale -> criterion; with a ``refute`` condition, a
    failed criterion is *challenged* only if the refutation holds, otherwise
    *inconclusive* (e.g. a confidence interval that straddles a threshold).
P2  Assumption: *assumed* without a check; with a check (evidence + criterion)
    it is evaluated like a solution, and a failed check *challenges* it.
P3  Goal / Strategy: the worst status over its SupportedBy children and its
    InContextOf assumptions. Context and justification nodes do not propagate.
    All support is conjunctive (GSN has no "or"): a goal is *supported* only if
    every child is supported, and any challenged child challenges it.
P4  A goal or strategy marked ``undeveloped`` contributes *undeveloped*; a leaf
    goal that is neither supported nor marked undeveloped is reported as an
    integrity error and treated as *undeveloped*.

Confidence is reported in the Baconian style of eliminative argumentation
(Goodenough, Weinstock & Klein, ICSE 2013, doi:10.1109/ICSE.2013.6606668):
``eliminated|identified`` counts of the checks (solutions and assumption checks)
below a node. Treating counter-evidence and defeaters as first-class follows the
spirit of Assurance 2.0 (Bloomfield & Rushby, arXiv:2004.10474).

Normative values used in criteria and texts (ASIL, PMHF target, permitted ASIL
decompositions, CAL) are computed with :mod:`avsafety.iso26262` and
:mod:`avsafety.iso21434` from the HARA and TARA entries of the case file.

Optional dependency: ``pyyaml`` (only for :func:`load_case`).
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import html
import json
import math
import os
import re
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from . import iso21434, iso26262

SCHEMA = "avsafety.evidence/1"
STATUSES = ("supported", "assumed", "undeveloped", "inconclusive", "stale", "missing", "challenged")
SEVERITY = {s: i for i, s in enumerate(STATUSES)}
NODE_TYPES = ("Goal", "Strategy", "Solution", "Context", "Assumption", "Justification")
SUPPORTED_BY = {"Goal": {"Goal", "Strategy", "Solution"}, "Strategy": {"Goal"}}
IN_CONTEXT_OF = {"Goal": {"Context", "Assumption", "Justification"},
                 "Strategy": {"Context", "Assumption", "Justification"}}
RESERVED_FIELDS = ("title", "notebook", "dataset", "licence", "units", "n", "confidence", "notes", "values",
                   "evidence_dir", "write", "recorded_at", "data_until")

# Okabe-Ito based styles; status is also given as a word and a glyph, never by colour alone.
STYLE = {
    "supported":    {"stroke": "#0072B2", "fill": "#D4E6F3", "glyph": "\u2713", "dash": "", "width": 1.6},
    "assumed":      {"stroke": "#CC79A7", "fill": "#F5E0EC", "glyph": "A", "dash": "", "width": 1.6},
    "undeveloped":  {"stroke": "#777777", "fill": "#EEEEEE", "glyph": "\u25C7", "dash": "2,3", "width": 1.4},
    "inconclusive": {"stroke": "#8C7A00", "fill": "#FAF4B8", "glyph": "?", "dash": "6,3", "width": 1.8},
    "stale":        {"stroke": "#B87800", "fill": "#FBE6BC", "glyph": "\u21BB", "dash": "8,4", "width": 2.2},
    "missing":      {"stroke": "#000000", "fill": "#FFFFFF", "glyph": "\u2205", "dash": "1,3", "width": 2.0},
    "challenged":   {"stroke": "#D55E00", "fill": "#F7D2BC", "glyph": "\u2717", "dash": "", "width": 3.2},
    "context":      {"stroke": "#555555", "fill": "#FFFFFF", "glyph": "", "dash": "", "width": 1.0},
}


# --------------------------------------------------------------------------- utilities
def worst(statuses: Iterable[str]) -> str:
    """Worst status of an iterable (``supported`` if empty)."""
    out = "supported"
    for s in statuses:
        if SEVERITY[s] > SEVERITY[out]:
            out = s
    return out


def find_repo_root(start: Optional[os.PathLike] = None) -> Optional[Path]:
    """Walk up from ``start`` (default: cwd) to the directory whose pyproject.toml names avsafety."""
    p = Path(start or os.getcwd()).resolve()
    for d in (p, *p.parents):
        f = d / "pyproject.toml"
        try:
            if f.is_file() and re.search(r'^name\s*=\s*"avsafety"', f.read_text(encoding="utf-8"), re.M):
                return d
        except OSError:
            continue
    return None


def notebook_code_hash(path: os.PathLike) -> str:
    """Hash of a notebook's code cells (sources only; outputs and markdown are ignored).

    Returns ``"sha256:<16 hex>"``. Any change to any code cell changes the hash, which
    makes evidence recorded by the previous version *stale* (a conservative rule).
    """
    nb = json.loads(Path(path).read_text(encoding="utf-8"))
    parts = []
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "code":
            src = cell.get("source", "")
            src = "".join(src) if isinstance(src, list) else src
            parts.append("\n".join(line.rstrip() for line in src.replace("\r\n", "\n").strip().split("\n")))
    return "sha256:" + hashlib.sha256("\n\x1e\n".join(parts).encode("utf-8")).hexdigest()[:16]


def _jsonable(x: Any) -> Any:
    """Convert numpy scalars/arrays, tuples and floats to plain JSON values (6 significant digits)."""
    if hasattr(x, "tolist") and not isinstance(x, (str, bytes)):
        x = x.tolist()
    if hasattr(x, "item") and not isinstance(x, (list, dict, str)):
        x = x.item()
    if isinstance(x, bool) or x is None or isinstance(x, str):
        return x
    if isinstance(x, int):
        return int(x)
    if isinstance(x, float):
        if math.isnan(x) or math.isinf(x):
            return None
        return float(f"{x:.6g}")
    if isinstance(x, dict):
        return {str(k): _jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    return str(x)


def _now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


# --------------------------------------------------------------------------- evidence
class EvidenceRecord(dict):
    """An evidence record (a ``dict`` with a compact representation)."""

    def __repr__(self) -> str:
        vals = ", ".join(f"{k}={v}" for k, v in list(self.get("values", {}).items())[:6])
        where = self.get("_written_to")
        return f"Evidence {self.get('id')}: {vals}" + (f" -> {where}" if where else " (not written)")


def validate_evidence(rec: dict) -> List[str]:
    """Schema errors of an evidence record (empty list if valid)."""
    errs = []
    if rec.get("schema") != SCHEMA:
        errs.append(f"schema must be {SCHEMA!r}")
    if not isinstance(rec.get("id"), str) or not re.fullmatch(r"[a-z0-9][a-z0-9_.\-]*", rec.get("id") or ""):
        errs.append("id must be a lower-case slug")
    if not isinstance(rec.get("values"), dict) or not rec.get("values"):
        errs.append("values must be a non-empty mapping")
    prod = rec.get("producer")
    if not isinstance(prod, dict) or not isinstance(prod.get("notebook"), str):
        errs.append("producer.notebook (repository-relative path) is required")
    elif prod.get("code_hash") is not None and not str(prod["code_hash"]).startswith("sha256:"):
        errs.append("producer.code_hash must start with 'sha256:'")
    try:
        _dt.datetime.fromisoformat(str(rec.get("recorded_at", "")).replace("Z", "+00:00"))
    except ValueError:
        errs.append("recorded_at must be an ISO 8601 timestamp")
    if not rec.get("dataset"):
        errs.append("dataset (name and licence) is required; use 'none (analysis)' for pure analyses")
    return errs


def record_evidence(id: str, **fields: Any) -> EvidenceRecord:
    """Record an evidence item from a notebook; never fails because of the environment.

    Reserved keyword arguments: ``title``, ``notebook`` (repository-relative path of the
    producing notebook), ``dataset``, ``licence``, ``units`` (mapping metric -> unit),
    ``n``, ``confidence``, ``notes``, ``data_until`` (ISO date of the newest data),
    ``values`` (mapping), ``evidence_dir`` and ``write``. Every other keyword is a metric
    value. Inside the repository (located by walking up to the ``pyproject.toml`` that
    names avsafety) the record is written to ``safety_case/evidence/<id>.json``; the
    environment variable ``AVSAFETY_EVIDENCE_DIR`` or ``evidence_dir=`` override the
    location. Outside the repository (e.g. on Colab) nothing is written and the record
    is only returned. ``write=False`` never writes.
    """
    values = dict(fields.pop("values", {}) or {})
    meta = {k: fields.pop(k) for k in list(fields) if k in RESERVED_FIELDS}
    values.update(fields)
    root = find_repo_root()
    nb = meta.get("notebook")
    code_hash = None
    if nb and root is not None and (root / nb).is_file():
        try:
            code_hash = notebook_code_hash(root / nb)
        except (OSError, ValueError):
            code_hash = None
    try:
        from . import __version__ as version
    except ImportError:  # pragma: no cover
        version = None
    rec = EvidenceRecord({
        "schema": SCHEMA, "id": id, "title": meta.get("title", id),
        "values": _jsonable(values), "units": _jsonable(meta.get("units", {})),
        "n": _jsonable(meta.get("n")), "confidence": _jsonable(meta.get("confidence")),
        "producer": {"notebook": nb, "code_hash": code_hash, "avsafety_version": version},
        "recorded_at": meta.get("recorded_at") or _now(),
        "dataset": {"name": meta.get("dataset"), "licence": meta.get("licence")} if meta.get("dataset") else None,
    })
    if meta.get("data_until"):
        rec["data_until"] = str(meta["data_until"])
    if meta.get("notes"):
        rec["notes"] = meta["notes"]
    target = meta.get("evidence_dir") or os.environ.get("AVSAFETY_EVIDENCE_DIR")
    if target is None and root is not None:
        target = root / "safety_case" / "evidence"
        # Only the declared producer writes to the committed evidence: a translation or copy of
        # the notebook (run from another folder) returns the record without overwriting it.
        if nb and Path.cwd().resolve() != (root / nb).parent.resolve():
            target = None
    if meta.get("write", True) is not False and target is not None:
        try:
            path = Path(target) / f"{id}.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
            tmp.write_text(json.dumps(dict(rec), indent=2, sort_keys=False) + "\n", encoding="utf-8")
            os.replace(tmp, path)
            rel = path.relative_to(root) if root is not None and root in path.resolve().parents else path
            rec["_written_to"] = str(rel)
        except (OSError, ValueError):
            pass
    return rec


def load_evidence(directory: os.PathLike) -> Dict[str, dict]:
    """All ``*.json`` evidence records of a directory, keyed by id (invalid JSON is skipped)."""
    out = {}
    d = Path(directory)
    if not d.is_dir():
        return out
    for f in sorted(d.glob("*.json")):
        try:
            rec = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            rec = {"id": f.stem, "_invalid": True}
        rec["_file"] = f.name
        out[rec.get("id") or f.stem] = rec
    return out


# --------------------------------------------------------------------------- criteria
_CLAUSE = re.compile(r"^\s*(not\s+)?([A-Za-z_][\w.\-]*)\s*(?:(>=|<=|==|!=|>|<|not\s+in|in)\s*([^=<>\s].*?))?\s*$")
_OPS = {">=": lambda a, b: a >= b, "<=": lambda a, b: a <= b, ">": lambda a, b: a > b, "<": lambda a, b: a < b,
        "==": lambda a, b: a == b, "!=": lambda a, b: a != b, "in": lambda a, b: a in b,
        "not in": lambda a, b: a not in b}


class CriterionError(ValueError):
    """Raised for a criterion that cannot be parsed."""


def parse_criterion(text: str) -> List[Tuple[bool, str, Optional[str], Optional[str]]]:
    """Parse ``"exists"`` or clauses joined by ``and``: ``name OP operand``, ``name`` or ``not name``.

    OP is one of ``>= <= > < == != in``, ``not in``. An operand is a JSON literal
    (number, ``true``/``false``/``null``, ``"string"``, ``[list]``) or a reference: another
    metric of the same record, or a derived normative value such as ``SG-01.asil``.
    """
    if not isinstance(text, str) or not text.strip():
        raise CriterionError("empty criterion")
    if text.strip() == "exists":
        return []
    clauses = []
    for part in re.split(r"\s+and\s+", text.strip()):
        m = _CLAUSE.match(part)
        if not m:
            raise CriterionError(f"cannot parse clause {part!r} in {text!r}")
        neg, name, op, rhs = m.groups()
        if neg and op:
            raise CriterionError(f"'not' only applies to a boolean metric: {part!r}")
        clauses.append((bool(neg), name, re.sub(r"\s+", " ", op) if op else None, rhs))
    return clauses


def _operand(tok: str, values: dict, derived: dict):
    try:
        return json.loads(tok)
    except ValueError:
        pass
    low = tok.strip()
    if low in ("True", "False", "None"):
        return {"True": True, "False": False, "None": None}[low]
    if low in values:
        return values[low]
    if low in derived:
        return derived[low]
    raise KeyError(low)


def evaluate_criterion(text: str, values: dict, derived: Optional[dict] = None) -> Tuple[Optional[bool], str]:
    """Evaluate a criterion. Returns ``(result, explanation)``; result is ``None`` if a metric is missing."""
    derived = derived or {}
    clauses = parse_criterion(text)
    if not clauses:
        return True, "evidence exists"
    ok, notes = True, []
    for neg, name, op, rhs in clauses:
        if name not in values:
            return None, f"metric {name!r} not in evidence"
        lhs = values[name]
        if op is None:
            res = (not lhs) if neg else bool(lhs)
            notes.append(f"{'not ' if neg else ''}{name} = {lhs}")
        else:
            try:
                r = _operand(rhs, values, derived)
            except KeyError as exc:
                return None, f"reference {exc.args[0]!r} is neither a metric nor a derived value"
            try:
                res = bool(_OPS[op](lhs, r)) if lhs is not None else False
            except TypeError:
                res = False
            try:
                json.loads(rhs)
                ref = ""
            except ValueError:
                ref = f" ({rhs.strip()})"
            notes.append(f"{name} = {_fmt(lhs)} {op} {_fmt(r)}{ref}")
        ok = ok and res
    return ok, "; ".join(notes)


def _fmt(v: Any) -> str:
    if isinstance(v, float):
        return f"{v:.3g}" if abs(v) < 1e-3 or abs(v) >= 1e4 else f"{v:.3f}".rstrip("0").rstrip(".")
    if isinstance(v, list):
        return "[" + ", ".join(_fmt(x) for x in v) + "]"
    return json.dumps(v) if v is None or isinstance(v, bool) else str(v)


# --------------------------------------------------------------------------- argument model
@dataclass
class Node:
    """One GSN element. Solutions (and checked assumptions) reference evidence by id."""
    id: str
    type: str
    text: str
    supported_by: List[str] = field(default_factory=list)
    in_context_of: List[str] = field(default_factory=list)
    undeveloped: bool = False
    evidence: Optional[str] = None
    criterion: Optional[str] = None
    refute: Optional[str] = None
    max_age_days: Optional[int] = None
    notebook: Optional[str] = None
    notes: Optional[str] = None

    def to_dict(self) -> dict:
        d = {"id": self.id, "type": self.type, "text": self.text}
        for k in ("supported_by", "in_context_of"):
            if getattr(self, k):
                d[k] = list(getattr(self, k))
        for k in ("undeveloped", "evidence", "criterion", "refute", "max_age_days", "notebook", "notes"):
            v = getattr(self, k)
            if v not in (None, False):
                d[k] = v
        return d


@dataclass
class Result:
    """Evaluated status of one node."""
    status: str
    reason: str = ""
    eliminated: int = 0
    identified: int = 0
    observed: str = ""

    @property
    def confidence(self) -> str:
        return f"{self.eliminated}|{self.identified}"


@dataclass
class Issue:
    """An integrity finding of :meth:`AssuranceCase.check`."""
    level: str        # "error" or "warning"
    node: str
    message: str

    def __str__(self) -> str:
        return f"{self.level.upper():7s} {self.node}: {self.message}"


class AssuranceCase:
    """A GSN argument plus the normative data (HARA, TARA) it is scoped by."""

    def __init__(self, nodes: Iterable[Node], *, name: str = "case", title: str = "", hara: Optional[dict] = None,
                 tara: Optional[dict] = None, root: Optional[os.PathLike] = None,
                 evidence_dir: Optional[os.PathLike] = None):
        self.name, self.title = name, title or name
        self.nodes: Dict[str, Node] = {}
        for n in nodes:
            if n.id in self.nodes:
                raise ValueError(f"duplicate node id {n.id}")
            if n.type not in NODE_TYPES:
                raise ValueError(f"{n.id}: unknown GSN element type {n.type!r}")
            self.nodes[n.id] = n
        self.hara, self.tara = hara or {}, tara or {}
        self.root = Path(root) if root else None
        self.evidence_dir = Path(evidence_dir) if evidence_dir else None

    # ---- structure
    def parents(self, nid: str) -> List[str]:
        return [p for p, n in self.nodes.items() if nid in n.supported_by or nid in n.in_context_of]

    def roots(self) -> List[str]:
        return [n for n in self.nodes if not self.parents(n)]

    def derived(self) -> Dict[str, Any]:
        """Normative values computed from the HARA and TARA with avsafety (not typed by hand).

        Keys: ``HE-xx.asil``; ``SG-xx.asil``, ``.ftti_ms``, ``.pmhf_target_per_h``,
        ``.spfm_target``, ``.lfm_target``, ``.decompositions`` (lists of two ASIL strings);
        ``TS-xx.cal``.
        """
        d: Dict[str, Any] = {}
        events = (self.hara or {}).get("hazardous_events", {})
        for he, e in events.items():
            d[f"{he}.asil"] = iso26262.determine_asil(e["S"], e["E"], e["C"])
        for sg, g in (self.hara or {}).get("safety_goals", {}).items():
            covered = [d[f"{he}.asil"] for he, e in events.items() if e.get("goal") == sg]
            asil = max(covered, key=iso26262.asil_rank) if covered else "QM"
            d[f"{sg}.asil"] = asil
            if "ftti_ms" in g:
                d[f"{sg}.ftti_ms"] = g["ftti_ms"]
            if asil in iso26262.PMHF_TARGET_PER_HOUR:
                d[f"{sg}.pmhf_target_per_h"] = iso26262.PMHF_TARGET_PER_HOUR[asil]
                d[f"{sg}.spfm_target"] = iso26262.SPFM_TARGET[asil]
                d[f"{sg}.lfm_target"] = iso26262.LFM_TARGET[asil]
            d[f"{sg}.decompositions"] = ([list(x) for x in iso26262.decomposition_options(asil)]
                                         if asil in iso26262.DECOMPOSITIONS else [])
        for ts, t in (self.tara or {}).get("threats", {}).items():
            d[f"{ts}.cal"] = iso21434.determine_cal(t["impact"], t["attack_vector"])
        return d

    def text(self, nid: str, derived: Optional[dict] = None) -> str:
        """Node text with ``{SG-01.asil}``-style placeholders filled from :meth:`derived`."""
        derived = self.derived() if derived is None else derived
        return re.sub(r"\{([A-Za-z0-9_\-]+\.[a-z_]+)\}", lambda m: str(derived.get(m.group(1), m.group(0))),
                      self.nodes[nid].text)

    # ---- evaluation
    def evaluate(self, evidence: Optional[Dict[str, dict]] = None, *, as_of: Optional[_dt.date] = None,
                 check_hashes: bool = True) -> "Evaluation":
        """Evaluate every node (rules P1-P4 of the module docstring).

        ``evidence`` defaults to the case's evidence directory. Staleness by code hash
        requires the repository root (``root``); ``check_hashes=False`` skips it, which is
        what a comparison of two evidence sets needs. ``as_of`` (default today) is used for
        ``max_age_days``.
        """
        if evidence is None:
            evidence = load_evidence(self.evidence_dir) if self.evidence_dir else {}
        as_of = as_of or _dt.date.today()
        derived = self.derived()
        hashes: Dict[str, Optional[str]] = {}
        res: Dict[str, Result] = {}

        def current_hash(nb: str) -> Optional[str]:
            if nb not in hashes:
                p = (self.root / nb) if self.root else None
                hashes[nb] = notebook_code_hash(p) if p is not None and p.is_file() else None
            return hashes[nb]

        def check(n: Node) -> Result:
            rec = evidence.get(n.evidence) if n.evidence else None
            if rec is None or rec.get("_invalid"):
                return Result("missing", f"evidence {n.evidence!r} not found", 0, 1)
            if check_hashes and self.root is not None:
                nb = (rec.get("producer") or {}).get("notebook")
                rec_hash, now_hash = (rec.get("producer") or {}).get("code_hash"), current_hash(nb) if nb else None
                if rec_hash is None:
                    return Result("stale", "evidence has no producer code hash (recorded outside the repository)", 0, 1)
                if now_hash is None:
                    return Result("missing", f"producer notebook {nb!r} not found", 0, 1)
                if rec_hash != now_hash:
                    return Result("stale", f"producer {Path(nb).name} changed since the evidence was recorded "
                                           f"({rec_hash[7:15]} -> {now_hash[7:15]})", 0, 1)
            if n.max_age_days is not None:
                stamp = rec.get("data_until") or rec.get("recorded_at", "")[:10]
                try:
                    age = (as_of - _dt.date.fromisoformat(stamp[:10])).days
                except ValueError:
                    age = None
                if age is None or age > n.max_age_days:
                    return Result("stale", f"evidence dated {stamp[:10]} is older than {n.max_age_days} days on "
                                           f"{as_of.isoformat()}", 0, 1)
            values = rec.get("values", {})
            ok, why = evaluate_criterion(n.criterion or "exists", values, derived)
            if ok is None:
                return Result("missing", why, 0, 1)
            if ok:
                return Result("supported", why, 1, 1, why)
            if n.refute:
                refuted, why_r = evaluate_criterion(n.refute, values, derived)
                if not refuted:
                    return Result("inconclusive", f"criterion not met ({why}), refutation not met ({why_r})", 0, 1, why)
                why = f"{why}; refuted: {why_r}"
            return Result("challenged", f"criterion not met: {why}", 0, 1, why)

        visiting = set()

        def visit(nid: str) -> Result:
            if nid in res:
                return res[nid]
            if nid not in self.nodes:
                return Result("missing", f"unknown node {nid}")
            if nid in visiting:
                return Result("missing", "cycle in SupportedBy")
            visiting.add(nid)
            n = self.nodes[nid]
            if n.type in ("Context", "Justification"):
                r = Result("supported", "context")
            elif n.type == "Solution":
                r = check(n)
            elif n.type == "Assumption":
                r = check(n) if n.evidence else Result("assumed", "assumption without supporting evidence", 0, 1)
                if r.status == "supported":
                    r.reason = "assumption checked: " + r.reason
            else:
                kids = [visit(c) for c in n.supported_by]
                assumptions = [visit(c) for c in n.in_context_of
                               if c in self.nodes and self.nodes[c].type == "Assumption"]
                statuses = [k.status for k in kids] + [a.status for a in assumptions]
                if n.undeveloped or not n.supported_by:
                    statuses.append("undeveloped")
                st = worst(statuses)
                drivers = [c for c in n.supported_by + n.in_context_of
                           if c in res and res[c].status == st and self.nodes.get(c) is not None
                           and self.nodes[c].type not in ("Context", "Justification")]
                reason = ("marked undeveloped" if st == "undeveloped" and (n.undeveloped or not n.supported_by)
                          else (f"from {', '.join(drivers)}" if drivers and st != "supported" else
                                "all support supported"))
                r = Result(st, reason, sum(k.eliminated for k in kids + assumptions),
                           sum(k.identified for k in kids + assumptions))
            visiting.discard(nid)
            res[nid] = r
            return r

        for nid in self.nodes:
            visit(nid)
        # Context-type nodes: report 'context' rather than a support status.
        for nid, n in self.nodes.items():
            if n.type in ("Context", "Justification"):
                res[nid] = Result("context", "")
        return Evaluation(self, res, evidence, derived)

    # ---- integrity
    def check(self, evidence: Optional[Dict[str, dict]] = None) -> List[Issue]:
        """Integrity findings: GSN well-formedness, references, evidence schema and freshness.

        Claim statuses are *not* findings: a challenged claim is a valid, honest result.
        """
        if evidence is None:
            evidence = load_evidence(self.evidence_dir) if self.evidence_dir else {}
        out: List[Issue] = []
        add = lambda lvl, nid, msg: out.append(Issue(lvl, nid, msg))
        roots = self.roots()
        if len(roots) != 1 or self.nodes[roots[0]].type != "Goal":
            add("error", ",".join(roots) or "-", "the argument must have exactly one root, and it must be a goal")
        derived = self.derived()
        for nid, n in self.nodes.items():
            for c in n.supported_by:
                if c not in self.nodes:
                    add("error", nid, f"SupportedBy refers to unknown node {c}")
                elif self.nodes[c].type not in SUPPORTED_BY.get(n.type, set()):
                    add("error", nid, f"{n.type} --SupportedBy--> {self.nodes[c].type} {c} is not permitted in GSN")
            for c in n.in_context_of:
                if c not in self.nodes:
                    add("error", nid, f"InContextOf refers to unknown node {c}")
                elif self.nodes[c].type not in IN_CONTEXT_OF.get(n.type, set()):
                    add("error", nid, f"{n.type} --InContextOf--> {self.nodes[c].type} {c} is not permitted in GSN")
            if n.type in ("Goal", "Strategy") and not n.supported_by and not n.undeveloped:
                add("error", nid, f"{n.type.lower()} is neither supported nor marked undeveloped")
            if n.type == "Solution" and not n.evidence:
                add("error", nid, "solution without an evidence reference")
            for t in (n.criterion, n.refute):
                if t:
                    try:
                        parse_criterion(t)
                    except CriterionError as exc:
                        add("error", nid, str(exc))
            for ph in re.findall(r"\{([A-Za-z0-9_\-]+\.[a-z_]+)\}", n.text):
                if ph not in derived:
                    add("error", nid, f"placeholder {{{ph}}} is not a derived value")
            if n.notebook and self.root is not None and not (self.root / n.notebook).is_file():
                add("error", nid, f"notebook {n.notebook} does not exist")
            if n.evidence:
                rec = evidence.get(n.evidence)
                if rec is None:
                    add("error", nid, f"evidence file {n.evidence}.json does not exist")
                    continue
                if rec.get("_invalid"):
                    add("error", nid, f"evidence file {rec.get('_file')} is not valid JSON")
                    continue
                for e in validate_evidence(rec):
                    add("error", nid, f"evidence {n.evidence}: {e}")
                for t in (n.criterion, n.refute):
                    if not t:
                        continue
                    try:
                        ok, why = evaluate_criterion(t, rec.get("values", {}), derived)
                    except CriterionError:
                        continue
                    if ok is None:
                        add("error", nid, f"criterion cannot be evaluated: {why}")
                prod = rec.get("producer") or {}
                nb = prod.get("notebook")
                if self.root is not None and nb:
                    p = self.root / nb
                    if not p.is_file():
                        add("error", nid, f"producer notebook {nb} does not exist")
                    elif prod.get("code_hash") != notebook_code_hash(p):
                        add("error", nid, f"evidence {n.evidence} is stale: {nb} changed since it was recorded "
                                          f"(re-execute the notebook and commit the evidence)")
        # cycles
        state: Dict[str, int] = {}

        def dfs(u: str) -> bool:
            state[u] = 1
            for v in self.nodes[u].supported_by:
                if v in self.nodes and (state.get(v) == 1 or (state.get(v) is None and dfs(v))):
                    return True
            state[u] = 2
            return False
        for u in self.nodes:
            if state.get(u) is None and dfs(u):
                add("error", u, "SupportedBy graph contains a cycle")
                break
        used = {n.evidence for n in self.nodes.values() if n.evidence}
        for eid in sorted(set(evidence) - used):
            add("warning", eid, "evidence file is not referenced by any node")
        return out

    # ---- serialisation
    def to_dict(self) -> dict:
        d = {"name": self.name, "title": self.title}
        if self.hara:
            d["hara"] = self.hara
        if self.tara:
            d["tara"] = self.tara
        d["nodes"] = [n.to_dict() for n in self.nodes.values()]
        return d

    @classmethod
    def from_dict(cls, d: dict, *, root: Optional[os.PathLike] = None,
                  evidence_dir: Optional[os.PathLike] = None) -> "AssuranceCase":
        allowed = set(Node.__dataclass_fields__)
        nodes = []
        for raw in d.get("nodes", []):
            unknown = set(raw) - allowed
            if unknown:
                raise ValueError(f"node {raw.get('id')}: unknown field(s) {sorted(unknown)}")
            nodes.append(Node(**raw))
        return cls(nodes, name=d.get("name", "case"), title=d.get("title", ""), hara=d.get("hara"),
                   tara=d.get("tara"), root=root, evidence_dir=evidence_dir)


def load_case(path: os.PathLike, *, evidence_dir: Optional[os.PathLike] = None,
              root: Optional[os.PathLike] = None) -> AssuranceCase:
    """Load a case from YAML. Evidence defaults to ``<case dir>/evidence``; root to the repository root."""
    import yaml  # optional dependency: pip install "avsafety[assurance]"
    path = Path(path)
    d = yaml.safe_load(path.read_text(encoding="utf-8"))
    root = Path(root) if root else find_repo_root(path.parent)
    return AssuranceCase.from_dict(d, root=root, evidence_dir=evidence_dir or path.parent / d.get("evidence", "evidence"))


def save_case(case: AssuranceCase, path: os.PathLike) -> None:
    """Write a case to YAML (round-trips with :func:`load_case`)."""
    import yaml
    Path(path).write_text(yaml.safe_dump(case.to_dict(), sort_keys=False, allow_unicode=True, width=110),
                          encoding="utf-8")


# --------------------------------------------------------------------------- results and rendering
class Evaluation:
    """Statuses of all nodes, with renderers."""

    def __init__(self, case: AssuranceCase, results: Dict[str, Result], evidence: Dict[str, dict], derived: dict):
        self.case, self.results, self.evidence, self.derived = case, results, evidence, derived

    def __getitem__(self, nid: str) -> Result:
        return self.results[nid]

    @property
    def top(self) -> Result:
        return self.results[self.case.roots()[0]]

    def counts(self, types: Tuple[str, ...] = ("Goal",)) -> Dict[str, int]:
        c: Dict[str, int] = {}
        for nid, n in self.case.nodes.items():
            if n.type in types:
                c[self.results[nid].status] = c.get(self.results[nid].status, 0) + 1
        return {s: c[s] for s in STATUSES if s in c}

    def rows(self) -> List[dict]:
        """One row per node, in document order."""
        out = []
        for nid, n in self.case.nodes.items():
            r = self.results[nid]
            rec = self.evidence.get(n.evidence) if n.evidence else None
            prod = ((rec or {}).get("producer") or {}).get("notebook") or n.notebook
            out.append({"node": nid, "type": n.type, "text": self.case.text(nid, self.derived), "status": r.status,
                        "reason": r.reason, "criterion": n.criterion or "", "observed": r.observed,
                        "producer": prod, "recorded": ((rec or {}).get("recorded_at") or "")[:10],
                        "confidence": r.confidence if n.type in ("Goal", "Strategy") else ""})
        return out

    def to_markdown(self, link_base: str = "", types: Tuple[str, ...] = ("Goal", "Strategy", "Solution", "Assumption")) -> str:
        """Markdown table (status as glyph + word). ``link_base`` is prefixed to producer paths."""
        lines = ["| Node | Type | Claim / evidence | Status | Criterion → observed | Producer | Confidence |",
                 "|---|---|---|---|---|---|---|"]
        for r in self.rows():
            if r["type"] not in types:
                continue
            st = r["status"]
            word = f"{STYLE[st]['glyph']} **{st}**" if st not in ("supported", "context") else f"{STYLE[st]['glyph']} {st}"
            crit = f"`{r['criterion']}`" if r["criterion"] else ""
            if r["status"] not in ("supported",) and r["type"] in ("Solution", "Assumption"):
                crit += f" — {r['reason']}" if crit else r["reason"]
            elif r["observed"]:
                crit += f" → {r['observed']}"
            prod = f"[{Path(r['producer']).stem}]({link_base}{r['producer']})" if r["producer"] else ""
            cells = [r["node"], r["type"], r["text"], word, crit, prod, r["confidence"]]
            lines.append("| " + " | ".join(str(c).replace("|", "\\|").replace("\n", " ") for c in cells) + " |")
        return "\n".join(lines)

    def to_mermaid(self) -> str:
        """Mermaid flowchart: GSN shapes, status in the label and as a class (colour + dash pattern)."""
        def q(s: str) -> str:
            return s.replace('"', "'")
        lines = ["flowchart TD"]
        for nid, n in self.case.nodes.items():
            r = self.results[nid]
            txt = q(textwrap.shorten(self.case.text(nid, self.derived), 70, placeholder=" ..."))
            lab = f"{nid}: {txt}" + (f"<br/>[{r.status.upper()}]" if r.status != "context" else "")
            safe = re.sub(r"\W", "_", nid)
            shape = {"Goal": f'["{lab}"]', "Strategy": f'[/"{lab}"/]', "Solution": f'(("{lab}"))',
                     "Context": f'(["{lab}"])', "Assumption": f'(["A — {lab}"])',
                     "Justification": f'(["J — {lab}"])'}[n.type]
            lines.append(f"  {safe}{shape}:::{r.status}")
        for nid, n in self.case.nodes.items():
            for c in n.supported_by:
                lines.append(f"  {re.sub(chr(92) + 'W', '_', nid)} --> {re.sub(chr(92) + 'W', '_', c)}")
            for c in n.in_context_of:
                lines.append(f"  {re.sub(chr(92) + 'W', '_', nid)} -.-> {re.sub(chr(92) + 'W', '_', c)}")
        for s, st in STYLE.items():
            dash = f",stroke-dasharray:{st['dash'].replace(',', ' ')}" if st["dash"] else ""
            lines.append(f"  classDef {s} fill:{st['fill']},stroke:{st['stroke']},stroke-width:{st['width']}px{dash}")
        return "\n".join(lines)

    def to_svg(self, root: Optional[str] = None, max_depth: Optional[int] = None, legend: bool = True,
               title: Optional[str] = None) -> str:
        """Standalone SVG of the argument (GSN shapes, status by colour, dash pattern, glyph and word)."""
        return _render_svg(self, root, max_depth, legend, title)


def diff(old: Evaluation, new: Evaluation) -> List[dict]:
    """Nodes whose status differs between two evaluations, with the reason and the changed values."""
    out = []
    for nid in new.case.nodes:
        a, b = old.results.get(nid), new.results.get(nid)
        if a is None or b is None or a.status == b.status:
            continue
        n = new.case.nodes[nid]
        changes = []
        if n.evidence:
            va = (old.evidence.get(n.evidence) or {}).get("values", {})
            vb = (new.evidence.get(n.evidence) or {}).get("values", {})
            changes = [f"{k}: {_fmt(va.get(k))} -> {_fmt(vb.get(k))}" for k in sorted(set(va) | set(vb))
                       if va.get(k) != vb.get(k)]
        out.append({"node": nid, "type": n.type, "old": a.status, "new": b.status, "reason": b.reason,
                    "changes": changes})
    return out


# --------------------------------------------------------------------------- SVG renderer
_W, _H, _R, _CW, _GAP, _DY = 210, 96, 54, 170, 26, 150


def _size(t: str) -> Tuple[float, float]:
    if t == "Solution":
        return 2 * _R, 2 * _R
    if t in ("Context", "Assumption", "Justification"):
        return _CW, 80
    return _W, _H


def _render_svg(ev: Evaluation, root, max_depth, legend, title) -> str:
    case = ev.case
    root = root or case.roots()[0]
    placed: Dict[str, Tuple[float, float]] = {}
    seen = set()

    def kids(nid, depth):
        if max_depth is not None and depth >= max_depth:
            return []
        out = []
        for c in case.nodes[nid].supported_by:
            if c in case.nodes and c not in seen:
                seen.add(c)
                out.append(c)
        return out

    tree: Dict[str, List[str]] = {}

    def build(nid, depth):
        seen.add(nid)
        tree[nid] = kids(nid, depth)
        for c in tree[nid]:
            build(c, depth + 1)
    build(root, 0)

    def ctx(nid):
        return [c for c in case.nodes[nid].in_context_of if c in case.nodes]

    widths: Dict[str, float] = {}

    def width(nid):
        own = _size(case.nodes[nid].type)[0] + sum(_size(case.nodes[c].type)[0] + _GAP for c in ctx(nid))
        ch = sum(width(c) for c in tree[nid]) + _GAP * max(0, len(tree[nid]) - 1)
        widths[nid] = max(own, ch)
        return widths[nid]
    width(root)

    def place(nid, x0, depth):
        w = widths[nid]
        own = _size(case.nodes[nid].type)[0] + sum(_size(case.nodes[c].type)[0] + _GAP for c in ctx(nid))
        x = x0 + (w - own) / 2 + _size(case.nodes[nid].type)[0] / 2
        y = 40 + depth * _DY + _H / 2 + (34 if title else 0)
        placed[nid] = (x, y)
        cx = x + _size(case.nodes[nid].type)[0] / 2 + _GAP
        for c in ctx(nid):
            cw = _size(case.nodes[c].type)[0]
            placed.setdefault(c, (cx + cw / 2, y))
            cx += cw + _GAP
        ch_w = sum(widths[c] for c in tree[nid]) + _GAP * max(0, len(tree[nid]) - 1)
        cx0 = x0 + (w - ch_w) / 2
        for c in tree[nid]:
            place(c, cx0, depth + 1)
            cx0 += widths[c] + _GAP
    place(root, 20, 0)

    depth_max = max(y for _, y in placed.values())
    W = widths[root] + 40
    H = depth_max + _H / 2 + 50 + (110 if legend else 0)
    esc = html.escape
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}" '
           f'font-family="DejaVu Sans, Arial, sans-serif" role="img">',
           f'<title>{esc(title or case.title)}</title>',
           '<defs><marker id="sb" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="8" markerHeight="8" orient="auto">'
           '<path d="M0,0 L10,5 L0,10 z" fill="#222"/></marker>'
           '<marker id="ic" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="8" markerHeight="8" orient="auto">'
           '<path d="M0,0 L10,5 L0,10 z" fill="#fff" stroke="#222"/></marker></defs>',
           f'<rect width="{W:.0f}" height="{H:.0f}" fill="#ffffff"/>']
    if title:
        out.append(f'<text x="20" y="30" font-size="17" font-weight="bold" fill="#111">{esc(title)}</text>')
    # edges first
    for nid, (x, y) in placed.items():
        n = case.nodes[nid]
        if nid in tree:
            for c in tree[nid]:
                cx, cy = placed[c]
                h2 = _size(case.nodes[c].type)[1] / 2
                out.append(f'<line x1="{x:.0f}" y1="{y + _size(n.type)[1] / 2:.0f}" x2="{cx:.0f}" y2="{cy - h2:.0f}" '
                           'stroke="#222" stroke-width="1.2" marker-end="url(#sb)"/>')
        for c in n.in_context_of:
            if c in placed and nid in tree:
                cx, cy = placed[c]
                out.append(f'<line x1="{x + _size(n.type)[0] / 2:.0f}" y1="{y:.0f}" '
                           f'x2="{cx - _size(case.nodes[c].type)[0] / 2:.0f}" y2="{cy:.0f}" stroke="#222" '
                           'stroke-width="1.1" marker-end="url(#ic)"/>')
    for nid, (x, y) in placed.items():
        out.append(_svg_node(ev, nid, x, y, truncated=(nid in tree and not tree[nid] and bool(case.nodes[nid].supported_by))))
    if legend:
        ly = H - 95
        out.append(f'<text x="20" y="{ly:.0f}" font-size="12" font-weight="bold">Status (colour, outline pattern, '
                   'glyph and word)</text>')
        for i, s in enumerate(STATUSES):
            st = STYLE[s]
            lx = 20 + i * 150
            dash = f' stroke-dasharray="{st["dash"]}"' if st["dash"] else ""
            out.append(f'<rect x="{lx}" y="{ly + 12:.0f}" width="34" height="22" fill="{st["fill"]}" stroke="{st["stroke"]}" '
                       f'stroke-width="{st["width"]}"{dash}/><text x="{lx + 17}" y="{ly + 28:.0f}" font-size="13" '
                       f'text-anchor="middle">{esc(st["glyph"])}</text><text x="{lx + 40}" y="{ly + 28:.0f}" '
                       f'font-size="12">{s}</text>')
        out.append(f'<text x="20" y="{ly + 60:.0f}" font-size="11" fill="#333">Rectangle goal · parallelogram strategy · '
                   'circle solution (evidence) · rounded box context · ellipse A assumption / J justification · '
                   '◇ undeveloped · solid arrow SupportedBy · hollow arrow InContextOf · confidence n|m = checks '
                   'passed | checks identified</text>')
    out.append("</svg>")
    return "\n".join(out)


def _svg_node(ev: Evaluation, nid: str, x: float, y: float, truncated: bool = False) -> str:
    n, r = ev.case.nodes[nid], ev.results[nid]
    st = STYLE[r.status]
    w, h = _size(n.type)
    dash = f' stroke-dasharray="{st["dash"]}"' if st["dash"] else ""
    attrs = f'fill="{st["fill"]}" stroke="{st["stroke"]}" stroke-width="{st["width"]}"{dash}'
    esc = html.escape
    parts = [f'<g><title>{esc(nid)} [{r.status}] {esc(ev.case.text(nid, ev.derived))} {esc(r.reason)}</title>']
    if n.type == "Goal":
        parts.append(f'<rect x="{x - w / 2:.0f}" y="{y - h / 2:.0f}" width="{w}" height="{h}" {attrs}/>')
    elif n.type == "Strategy":
        s = 14
        pts = [(x - w / 2 + s, y - h / 2), (x + w / 2 + s, y - h / 2), (x + w / 2 - s, y + h / 2), (x - w / 2 - s, y + h / 2)]
        parts.append(f'<polygon points="{" ".join(f"{a:.0f},{b:.0f}" for a, b in pts)}" {attrs}/>')
    elif n.type == "Solution":
        parts.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{_R}" {attrs}/>')
    elif n.type == "Context":
        parts.append(f'<rect x="{x - w / 2:.0f}" y="{y - h / 2:.0f}" width="{w}" height="{h}" rx="18" {attrs}/>')
    else:
        parts.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{w / 2:.0f}" ry="{h / 2:.0f}" {attrs}/>')
        parts.append(f'<text x="{x + w / 2 - 6:.0f}" y="{y + h / 2:.0f}" font-size="13" font-weight="bold">'
                     f'{"A" if n.type == "Assumption" else "J"}</text>')
    if n.type == "Solution":
        rec = ev.evidence.get(n.evidence) if n.evidence else None
        lines = [nid, f"{st['glyph']} {r.status.upper()}"] + textwrap.wrap(n.evidence or "", 16)[:2]
        top = y - 8 * (len(lines) - 1)
        for i, line in enumerate(lines):
            parts.append(f'<text x="{x:.0f}" y="{top + i * 16 + 4:.0f}" font-size="{12 if i == 0 else 10}" '
                         f'text-anchor="middle"{" font-weight=" + chr(34) + "bold" + chr(34) if i < 2 else ""}>'
                         f'{esc(line)}</text>')
        del rec
    else:
        text = ev.case.text(nid, ev.derived)
        oval = n.type in ("Assumption", "Justification")
        wrap = {"Goal": 32, "Strategy": 30}.get(n.type, 22 if oval else 26)
        body = textwrap.wrap(text, wrap)
        maxl = 4 if n.type in ("Goal", "Strategy") else 3
        if len(body) > maxl:
            body = body[:maxl - 1] + [textwrap.shorten(" ".join(body[maxl - 1:]), wrap, placeholder=" …")]
        head = nid if r.status == "context" else f"{nid}   {st['glyph']} {r.status.upper()}"
        if n.type in ("Goal", "Strategy") and r.identified:
            head += f"   {r.confidence}"
        top = y - h / 2 + (20 if oval else 16)
        tx = x if oval else x - w / 2 + (22 if n.type == "Strategy" else 8)
        anchor = ' text-anchor="middle"' if oval else ""
        parts.append(f'<text x="{tx:.0f}" y="{top:.0f}" font-size="11.5" font-weight="bold"{anchor}>{esc(head)}</text>')
        for i, line in enumerate(body):
            parts.append(f'<text x="{tx:.0f}" y="{top + 15 + i * 14:.0f}" font-size="11"{anchor}>{esc(line)}</text>')
    if n.undeveloped:
        parts.append(f'<polygon points="{x:.0f},{y + h / 2:.0f} {x + 9:.0f},{y + h / 2 + 9:.0f} {x:.0f},{y + h / 2 + 18:.0f} '
                     f'{x - 9:.0f},{y + h / 2 + 9:.0f}" fill="#fff" stroke="#222"/>')
    if truncated:
        parts.append(f'<text x="{x:.0f}" y="{y + h / 2 + 16:.0f}" font-size="11" text-anchor="middle" fill="#333">'
                     '▼ continued</text>')
    parts.append("</g>")
    return "".join(parts)
