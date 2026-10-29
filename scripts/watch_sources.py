#!/usr/bin/env python3
"""Detect new editions, amendments and data releases of the sources the course relies on.

For every document in references/normative.yaml that has a ``watch`` list, fetch the source, reduce it to a
normalised fingerprint and compare it with references/fingerprints.json:

  iso-open-data   ISO Open Data deliverables metadata: stage code of the edition and of its successors
  eu-cellar       EU Publications Office SPARQL endpoint: amending acts and consolidated versions of a CELEX
  regex-page      the sorted set of matches of a pattern in a web page (e.g. the list of amendment PDFs)
  headers         ETag / Last-Modified / Content-Length of a file (for large or noisy downloads)
  csv-header      the header row of a CSV file (a renamed column breaks the notebooks)
  json-fields     selected fields of a JSON API response (e.g. Zenodo checksums)

A source that cannot be fetched after three attempts is reported as unreachable and never counts as a change.
The affected notebooks of a changed source come from the citation index of check_references.py.

Usage
  python scripts/watch_sources.py --report report.md --issue issue.md   # check (exit 0)
  python scripts/watch_sources.py --update                              # accept current fingerprints
  python scripts/watch_sources.py --fixtures tests/fixtures/watch       # offline, recorded responses
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[1]
FINGERPRINTS = ROOT / "references" / "fingerprints.json"
REPO = "milinpatel07/Autonomous-Driving_AI-Safety-and-Security"
USER_AGENT = f"course-source-watch/1.0 (+https://github.com/{REPO})"
ISO_OPEN_DATA = ("https://isopublicstorageprod.blob.core.windows.net/opendata/_latest/"
                 "iso_deliverables_metadata/json/iso_deliverables_metadata.jsonl")
SPARQL = "https://publications.europa.eu/webapi/rdf/sparql"
ISSUE_MARKER = "<!-- source-watch -->"


@dataclass
class Response:
    status: int
    headers: Dict[str, str]
    body: bytes


class Unreachable(Exception):
    """The source could not be fetched (network error, timeout, HTTP error after retries)."""


# --------------------------------------------------------------------------------------------
# Fetching
# --------------------------------------------------------------------------------------------
class HttpFetcher:
    """Polite HTTP client: a fixed user agent, at least ``delay`` seconds between requests to the same
    host, and ``retries`` attempts with exponential back-off."""

    def __init__(self, delay: float = 2.0, retries: int = 3, timeout: float = 60.0,
                 sleep: Callable[[float], None] = time.sleep):
        self.delay, self.retries, self.timeout, self.sleep = delay, retries, timeout, sleep
        self._last: Dict[str, float] = {}

    def __call__(self, url: str, method: str = "GET", headers: Optional[Dict[str, str]] = None) -> Response:
        host = urllib.parse.urlsplit(url).netloc
        error: Exception = Unreachable(url)
        for attempt in range(self.retries):
            wait = self._last.get(host, 0) + self.delay - time.monotonic()
            if wait > 0:
                self.sleep(wait)
            req = urllib.request.Request(url, method=method, headers={"User-Agent": USER_AGENT, **(headers or {})})
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as r:
                    body = r.read() if method != "HEAD" else b""
                    resp = Response(r.status, {k.lower(): v for k, v in r.headers.items()}, body)
                self._last[host] = time.monotonic()
                return resp
            except urllib.error.HTTPError as e:
                self._last[host] = time.monotonic()
                error = e
                if e.code in (400, 401, 403, 404, 410):   # retrying does not help
                    break
            except Exception as e:                        # timeouts, resets, DNS
                self._last[host] = time.monotonic()
                error = e
            self.sleep(2 ** attempt)
        raise Unreachable(f"{url}: {error}")


class FixtureFetcher:
    """Replays recorded responses: ``index.json`` maps "METHOD URL" to {status, headers, body}
    where body is a file name in the same directory (missing key -> unreachable)."""

    def __init__(self, directory: Path):
        self.dir = Path(directory)
        self.index = json.loads((self.dir / "index.json").read_text(encoding="utf-8"))

    def __call__(self, url: str, method: str = "GET", headers: Optional[Dict[str, str]] = None) -> Response:
        rec = self.index.get(f"{method} {url}") or (self.index.get(f"GET {url}") if method == "HEAD" else None)
        if rec is None or rec.get("status", 200) >= 400:
            raise Unreachable(f"{url}: no recorded response")
        body = (self.dir / rec["body"]).read_bytes() if rec.get("body") else b""
        return Response(rec.get("status", 200), {k.lower(): v for k, v in rec.get("headers", {}).items()}, body)


# --------------------------------------------------------------------------------------------
# Fingerprint methods: each returns (summary lines, canonical payload)
# --------------------------------------------------------------------------------------------
def _digest(payload) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()[:16]


class Watcher:
    def __init__(self, fetch: Callable[..., Response]):
        self.fetch = fetch
        self._iso: Optional[Dict[str, dict]] = None

    # ISO Open Data ----------------------------------------------------------------------
    def iso_rows(self) -> Dict[str, dict]:
        if self._iso is None:
            body = self.fetch(ISO_OPEN_DATA).body.decode("utf-8")
            rows = {}
            for line in body.splitlines():
                if not line.strip():
                    continue
                d = json.loads(line)
                rows[str(d["id"])] = {"reference": d.get("reference"), "stage": d.get("currentStage"),
                                      "replacedBy": [str(x) for x in (d.get("replacedBy") or [])]}
            self._iso = rows
        return self._iso

    def iso_open_data(self, spec: dict) -> Tuple[List[str], object]:
        rows = self.iso_rows()
        by_ref = {r["reference"]: r for r in rows.values()}
        row = by_ref.get(spec["reference"])
        if row is None:
            raise Unreachable(f"{spec['reference']} not found in ISO Open Data")
        succ = sorted((rows[i]["reference"], rows[i]["stage"]) for i in row["replacedBy"] if i in rows)
        payload = {"stage": row["stage"], "successors": succ}
        lines = [f"{spec['reference']}: stage {row['stage']}"] + [f"successor {r}: stage {s}" for r, s in succ]
        return lines, payload

    # EU Publications Office ---------------------------------------------------------------
    def eu_cellar(self, spec: dict) -> Tuple[List[str], object]:
        celex = spec["celex"]
        data = json.loads(self.fetch(cellar_url(celex)).body.decode("utf-8"))
        own = "0" + celex[1:]                     # consolidated versions of this act: 0YYYYRNNNN-date
        values = sorted({v for v in (b["c"]["value"] for b in data["results"]["bindings"])
                         if v.startswith(own) or v.startswith("3")})
        amending = [v for v in values if v.startswith("3")]
        consolidated = [v.split("-")[-1] for v in values if v.startswith(own)]
        return [f"{celex}: amending acts {', '.join(amending) or 'none'}; consolidated versions "
                f"{', '.join(consolidated) or 'none'}"], values

    # Generic web --------------------------------------------------------------------------
    def regex_page(self, spec: dict) -> Tuple[List[str], object]:
        text = self.fetch(spec["url"]).body.decode("utf-8", errors="replace")
        found = set()
        for m in re.finditer(spec["pattern"], text):
            val = m.group(1) if m.groups() else m.group(0)
            found.add(re.sub(r"\s+", " ", val).strip())
        values = sorted(found)
        if not values:
            raise Unreachable(f"{spec['url']}: pattern not found (page layout changed?)")
        return [f"{len(values)} matches; last: {values[-1][:100]}"], values

    def headers(self, spec: dict) -> Tuple[List[str], object]:
        h = self.fetch(spec["url"], method="HEAD").headers
        payload = {k: h[k] for k in ("etag", "last-modified", "content-length") if k in h}
        if not payload:
            raise Unreachable(f"{spec['url']}: no ETag, Last-Modified or Content-Length")
        return [", ".join(f"{k}: {v}" for k, v in payload.items())], payload

    def csv_header(self, spec: dict) -> Tuple[List[str], object]:
        body = self.fetch(spec["url"], headers={"Range": "bytes=0-16383"}).body.decode("utf-8-sig", errors="replace")
        first = body.splitlines()[0] if body else ""
        cols = [c.strip().strip('"') for c in first.split(",")]
        return [f"{len(cols)} columns: {', '.join(cols[:6])}{' ...' if len(cols) > 6 else ''}"], cols

    def json_fields(self, spec: dict) -> Tuple[List[str], object]:
        data = json.loads(self.fetch(spec["url"]).body.decode("utf-8"))
        payload = {f: pick(data, f) for f in spec["fields"]}
        lines = [f"{f}: {_short(v)}" for f, v in payload.items()]
        return lines, payload

    def run(self, spec: dict) -> Tuple[List[str], object]:
        return getattr(self, spec["method"].replace("-", "_"))(spec)


def cellar_url(celex: str) -> str:
    """SPARQL query for the acts that amend a CELEX document and for its consolidated versions."""
    query = ("PREFIX cdm: <http://publications.europa.eu/ontology/cdm#> SELECT DISTINCT ?c WHERE { "
             f'?t cdm:resource_legal_id_celex "{celex}"^^<http://www.w3.org/2001/XMLSchema#string> . '
             "{ ?a cdm:resource_legal_amends_resource_legal ?t } UNION "
             "{ ?a cdm:act_consolidated_consolidates_resource_legal ?t } "
             "?a cdm:resource_legal_id_celex ?c }")
    return SPARQL + "?" + urllib.parse.urlencode({"query": query, "format": "application/sparql-results+json"})


def pick(data, path: str):
    """'a.b' -> data['a']['b']; 'files[].checksum' -> [f['checksum'] for f in data['files']]."""
    cur = [data]
    for part in path.split("."):
        nxt = []
        for c in cur:
            if part.endswith("[]"):
                nxt.extend((c or {}).get(part[:-2], []) or [])
            else:
                nxt.append((c or {}).get(part) if isinstance(c, dict) else None)
        cur = nxt
    return cur if "[]" in path else (cur[0] if cur else None)


def _short(v) -> str:
    s = json.dumps(v, ensure_ascii=False)
    return s if len(s) <= 90 else s[:87] + "..."


# --------------------------------------------------------------------------------------------
# Comparison and reports
# --------------------------------------------------------------------------------------------
@dataclass
class Result:
    key: str
    doc: str
    title: str
    status: str                      # unchanged | changed | new | unreachable
    summary: List[str] = field(default_factory=list)
    previous: List[str] = field(default_factory=list)
    fingerprint: Optional[str] = None
    error: str = ""
    affected: List[str] = field(default_factory=list)


def watch_key(doc: str, spec: dict) -> str:
    target = spec.get("url") or spec.get("celex") or spec.get("reference")
    return f"{doc} {spec['method']} {target}"


def check_sources(documents: dict, baseline: dict, watcher: Watcher,
                  affected: Optional[Dict[str, List[str]]] = None) -> List[Result]:
    results = []
    for doc, d in documents.items():
        for spec in d.get("watch") or []:
            key = watch_key(doc, spec)
            r = Result(key, doc, d.get("title", doc), "unreachable", affected=(affected or {}).get(doc, []))
            try:
                r.summary, payload = watcher.run(spec)
                r.fingerprint = _digest(payload)
            except Unreachable as e:
                r.error = str(e)
                results.append(r)
                continue
            old = baseline.get(key)
            if old is None:
                r.status = "new"
            elif old.get("fingerprint") == r.fingerprint:
                r.status = "unchanged"
            else:
                r.status, r.previous = "changed", old.get("summary", [])
            results.append(r)
    return results


def affected_notebooks() -> Dict[str, List[str]]:
    """Document key -> files that cite it (any clause or the document as a whole)."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import check_references as C

    reg = C.load_registry()
    rep = C.check(reg, C.extract_all())
    out: Dict[str, set] = {}
    entry_doc = {e["id"]: e["doc"] for e in reg["entries"]}
    for k, paths in rep.used_in.items():
        doc = k[4:] if k.startswith("doc:") else entry_doc.get(k)
        if doc:
            out.setdefault(doc, set()).update(paths)
    return {k: sorted(v) for k, v in out.items()}


def report_markdown(results: Sequence[Result]) -> str:
    counts = {s: sum(r.status == s for r in results) for s in ("changed", "new", "unchanged", "unreachable")}
    lines = [f"### Source watch ({dt.date.today().isoformat()})", "",
             f"{counts['changed']} changed, {counts['new']} without a baseline, {counts['unchanged']} unchanged, "
             f"{counts['unreachable']} unreachable.", "",
             "| Source | Status | Detail |", "|---|---|---|"]
    order = {"changed": 0, "new": 1, "unreachable": 2, "unchanged": 3}
    for r in sorted(results, key=lambda r: (order[r.status], r.key)):
        detail = r.error if r.status == "unreachable" else "; ".join(r.summary)
        lines.append(f"| {r.key} | {r.status} | {detail.replace('|', '/')[:200]} |")
    return "\n".join(lines) + "\n"


def issue_markdown(results: Sequence[Result]) -> str:
    changed = [r for r in results if r.status == "changed"]
    lines = [ISSUE_MARKER,
             f"The monthly source watch found **{len(changed)}** changed source(s) on {dt.date.today().isoformat()}. "
             "Check each change against the registry (`references/normative.yaml`) and the notebooks that cite it, "
             "then accept the new fingerprints (see MAINTAINING.md, *Handling a watch issue*).", ""]
    for r in changed:
        lines += [f"### {r.title}", f"`{r.key}`", "",
                  "- before: " + ("; ".join(r.previous) or "—"),
                  "- now: " + "; ".join(r.summary)]
        if r.affected:
            lines.append("- cited in: " + ", ".join(f"`{p}`" for p in r.affected))
        lines.append("")
    unreachable = [r for r in results if r.status == "unreachable"]
    if unreachable:
        lines.append(f"{len(unreachable)} source(s) were unreachable and are listed in the workflow summary only.")
    return "\n".join(lines) + "\n"


def update_baseline(baseline: dict, results: Sequence[Result]) -> dict:
    new = dict(baseline)
    today = dt.date.today().isoformat()
    for r in results:
        if r.status in ("changed", "new"):
            new[r.key] = {"fingerprint": r.fingerprint, "summary": r.summary, "checked": today}
        elif r.status == "unchanged":
            new[r.key] = dict(new[r.key], checked=today)
    return dict(sorted(new.items()))


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--fingerprints", type=Path, default=FINGERPRINTS)
    ap.add_argument("--fixtures", type=Path, help="replay recorded responses from this directory (offline)")
    ap.add_argument("--update", action="store_true", help="write the current fingerprints to --fingerprints")
    ap.add_argument("--write-new", type=Path, help="write the would-be updated fingerprints here")
    ap.add_argument("--report", type=Path, help="write a Markdown summary (for $GITHUB_STEP_SUMMARY)")
    ap.add_argument("--issue", type=Path, help="write the issue body if something changed")
    ap.add_argument("--github-output", type=Path, default=os.environ.get("GITHUB_OUTPUT") or None)
    ap.add_argument("--only", nargs="*", help="document keys to check")
    args = ap.parse_args(argv)

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import check_references as C

    documents = C.load_registry()["documents"]
    if args.only:
        documents = {k: v for k, v in documents.items() if k in args.only}
    baseline = json.loads(args.fingerprints.read_text(encoding="utf-8")) if args.fingerprints.exists() else {}
    fetch = FixtureFetcher(args.fixtures) if args.fixtures else HttpFetcher()
    results = check_sources(documents, baseline, Watcher(fetch), affected_notebooks())

    report = report_markdown(results)
    print(report)
    if args.report:
        args.report.write_text(report, encoding="utf-8")
    changed = [r for r in results if r.status == "changed"]
    if args.issue and changed:
        args.issue.write_text(issue_markdown(results), encoding="utf-8")
    new_baseline = update_baseline(baseline, results)
    if args.write_new:
        args.write_new.write_text(json.dumps(new_baseline, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.update:
        args.fingerprints.write_text(json.dumps(new_baseline, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print("updated", args.fingerprints)
    if args.github_output:
        with open(args.github_output, "a", encoding="utf-8") as fh:
            fh.write(f"changed={'true' if changed else 'false'}\n")
            fh.write(f"unreachable={sum(r.status == 'unreachable' for r in results)}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
