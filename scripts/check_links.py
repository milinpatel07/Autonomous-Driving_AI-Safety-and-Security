#!/usr/bin/env python3
"""Check the external links in the notebooks, the site pages, the templates and the README.

Each distinct URL is requested once (HEAD, then GET when HEAD is refused), sequentially, with at least
``--delay`` seconds between two requests to the same host and one retry on timeouts and 5xx answers.

Outcomes
  ok           2xx/3xx
  blocked      401/403/429 or a refused connection from a host on the allowlist of sites that turn away
               automated clients (ISO, UNECE, EUR-Lex, NHTSA, publishers); not counted as broken
  unreachable  timeout or network error after the retry; reported, not counted as broken
  broken       404/410, or any other 4xx, or a DNS failure

Usage
  python scripts/check_links.py                       # all links, Markdown report on stdout
  python scripts/check_links.py --report links.md     # also write the report (exit 1 if broken)
  python scripts/check_links.py --list                # only list the URLs that would be checked
"""
from __future__ import annotations

import argparse
import json
import re
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Iterable, Iterator, List, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[1]
USER_AGENT = "course-link-check/1.0 (+https://github.com/milinpatel07/Autonomous-Driving_AI-Safety-and-Security)"

# Hosts that answer automated requests with 401/403/429 although the page exists.
BOT_BLOCKING = (
    "iso.org", "unece.org", "eur-lex.europa.eu", "nhtsa.gov", "sae.org", "ieeexplore.ieee.org", "dl.acm.org",
    "sciencedirect.com", "link.springer.com", "onlinelibrary.wiley.com", "researchgate.net", "linkedin.com",
    "tandfonline.com", "journals.sagepub.com", "webstore.iec.ch", "webstore.ansi.org", "ul.com",
    "shopulstandards.com", "standards.globalspec.com", "x.com", "twitter.com", "medium.com", "reuters.com",
    "bloomberg.com", "ft.com", "wsj.com", "nytimes.com", "cnbc.com", "insideevs.com", "sec.gov", "rand.org",
    "tuvsud.com", "crowell.com", "group.mercedes-benz.com", "omb.report",
)
# Links that are templates, local services or git remotes (pip install git+...), never fetched.
SKIP = re.compile(r"^https?://(?:localhost|127\.0\.0\.1|0\.0\.0\.0|example\.(?:org|com))|[{}<>]|\$\{|\.git$")

URL = re.compile(r"https?://[^\s<>\"'`\\()\[\]]+(?:\([^\s()]*\)[^\s<>\"'`\\()\[\]]*)*")
TRAILING = ".,;:!?*_'\""


@dataclass
class Link:
    url: str
    where: List[str]


@dataclass
class Outcome:
    url: str
    status: str            # ok | blocked | unreachable | broken
    code: Optional[int]
    detail: str = ""


# --------------------------------------------------------------------------------------------
# Extraction
# --------------------------------------------------------------------------------------------
def clean(url: str) -> str:
    url = url.rstrip(TRAILING)
    # a closing parenthesis belongs to the URL only if it opens one (Wikipedia style)
    while url.endswith(")") and url.count("(") < url.count(")"):
        url = url[:-1].rstrip(TRAILING)
    return url


def extract_urls(text: str) -> List[str]:
    out = []
    for m in URL.finditer(text):
        u = clean(m.group(0))
        if u and not SKIP.search(u):
            out.append(u)
    return out


def iter_sources(root: Path = ROOT) -> Iterator[Tuple[str, str]]:
    for nb in sorted(root.glob("[0-9][0-9]_*/*.ipynb")):
        cells = json.loads(nb.read_text(encoding="utf-8")).get("cells", [])
        for i, c in enumerate(cells):
            src = c.get("source", "")
            src = "".join(src) if isinstance(src, list) else src
            yield f"{nb.relative_to(root).as_posix()} cell {i}", src
    for md in [root / "README.md", *sorted(root.glob("site/*.md")), *sorted(root.glob("templates/*.md")),
               *sorted(root.glob("[0-9][0-9]_*/README.md"))]:
        if md.exists():
            yield md.relative_to(root).as_posix(), md.read_text(encoding="utf-8")


def collect(sources: Iterable[Tuple[str, str]]) -> List[Link]:
    where: Dict[str, List[str]] = defaultdict(list)
    for name, text in sources:
        for u in extract_urls(text):
            if name not in where[u]:
                where[u].append(name)
    return [Link(u, w) for u, w in sorted(where.items())]


# --------------------------------------------------------------------------------------------
# Checking
# --------------------------------------------------------------------------------------------
def host_of(url: str) -> str:
    return urllib.parse.urlsplit(url).hostname or ""


def on_allowlist(url: str) -> bool:
    h = host_of(url)
    return any(h == d or h.endswith("." + d) for d in BOT_BLOCKING)


def classify(url: str, code: Optional[int], error: Optional[BaseException] = None,
             final: Optional[str] = None) -> Outcome:
    """Turn an HTTP status (or a network error) into an outcome. ``final`` is the URL after redirects: a DOI
    or short link that redirects to a publisher which then refuses the client has still resolved."""
    final = final or url
    if code is not None:
        if code < 400:
            return Outcome(url, "ok", code)
        if code in (401, 403, 429) and (on_allowlist(final) or host_of(final) != host_of(url)):
            return Outcome(url, "blocked", code, f"{host_of(final)} blocks automated clients")
        if code == 429 or code >= 500:
            return Outcome(url, "unreachable", code, "server busy or failing")
        return Outcome(url, "broken", code)
    reason = getattr(error, "reason", error)
    if isinstance(reason, socket.gaierror):
        return Outcome(url, "broken", None, "host not found")
    if on_allowlist(url):
        return Outcome(url, "blocked", None, f"connection refused by allowlisted host ({reason})")
    return Outcome(url, "unreachable", None, str(reason)[:120])


def http_status(url: str, method: str, timeout: float) -> Tuple[int, str]:
    """(status code, URL after redirects)."""
    req = urllib.request.Request(url, method=method, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, e.geturl() or url


class Checker:
    def __init__(self, delay: float = 1.0, timeout: float = 20.0,
                 status: Callable[[str, str, float], Tuple[int, str]] = http_status,
                 sleep: Callable[[float], None] = time.sleep, clock: Callable[[], float] = time.monotonic):
        self.delay, self.timeout, self.status, self.sleep, self.clock = delay, timeout, status, sleep, clock
        self._last: Dict[str, float] = {}

    def _polite(self, url: str) -> None:
        h = host_of(url)
        wait = self._last.get(h, -1e9) + self.delay - self.clock()
        if wait > 0:
            self.sleep(wait)
        self._last[h] = self.clock()

    def check(self, url: str) -> Outcome:
        error: Optional[BaseException] = None
        for attempt in range(2):
            try:
                self._polite(url)
                code, final = self.status(url, "HEAD", self.timeout)
                if code in (403, 404, 405, 501) or code >= 500:     # some servers mishandle HEAD
                    self._polite(url)
                    code, final = self.status(url, "GET", self.timeout)
                out = classify(url, code, final=final)
                if out.status != "unreachable" or attempt == 1:
                    return out
            except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError, OSError) as e:
                error = e
                if isinstance(getattr(e, "reason", None), socket.gaierror):
                    break
            self.sleep(2.0)
        return classify(url, None, error)


def report(links: Sequence[Link], outcomes: Sequence[Outcome]) -> str:
    by = {o.url: o for o in outcomes}
    counts = defaultdict(int)
    for o in outcomes:
        counts[o.status] += 1
    lines = [f"### External links: {len(outcomes)} checked — {counts['broken']} broken, "
             f"{counts['unreachable']} unreachable, {counts['blocked']} blocked by the host, {counts['ok']} ok", ""]
    bad = [l for l in links if by[l.url].status in ("broken", "unreachable")]
    if bad:
        lines += ["| Status | URL | Where |", "|---|---|---|"]
        for l in sorted(bad, key=lambda l: (by[l.url].status, l.url)):
            o = by[l.url]
            code = f" {o.code}" if o.code else ""
            lines.append(f"| {o.status}{code} {o.detail} | {l.url} | {', '.join(l.where[:3])}"
                         f"{' …' if len(l.where) > 3 else ''} |")
    return "\n".join(lines) + "\n"


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--report", type=Path, help="write the Markdown report here")
    ap.add_argument("--delay", type=float, default=1.0, help="seconds between requests to the same host")
    ap.add_argument("--timeout", type=float, default=20.0)
    ap.add_argument("--list", action="store_true", help="list the URLs and exit")
    args = ap.parse_args(argv)

    links = collect(iter_sources())
    if args.list:
        for l in links:
            print(l.url)
        print(f"{len(links)} distinct external links")
        return 0
    checker = Checker(delay=args.delay, timeout=args.timeout)
    outcomes = [checker.check(l.url) for l in links]
    text = report(links, outcomes)
    print(text)
    if args.report:
        args.report.write_text(text, encoding="utf-8")
    return 1 if any(o.status == "broken" for o in outcomes) else 0


if __name__ == "__main__":
    sys.exit(main())
