"""Offline tests for scripts/check_links.py (no requests are sent)."""
import importlib.util
import socket
import sys
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("check_links", ROOT / "scripts" / "check_links.py")
L = importlib.util.module_from_spec(spec)
sys.modules["check_links"] = L
spec.loader.exec_module(L)


def test_extract_urls_from_markdown_and_code():
    text = ("See [ISO 21448](https://www.iso.org/standard/77490.html), and https://en.wikipedia.org/wiki/Foo_(bar). "
            "Also <https://arxiv.org/abs/2307.02261>; **https://doi.org/10.1000/x**.\n"
            'url = f"https://api.example.net/{campaign}"  # computed\n'
            'TEMPLATE = "http://localhost:8888/tree"')
    assert L.extract_urls(text) == [
        "https://www.iso.org/standard/77490.html", "https://en.wikipedia.org/wiki/Foo_(bar)",
        "https://arxiv.org/abs/2307.02261", "https://doi.org/10.1000/x"]


def test_collect_deduplicates_and_records_locations():
    links = L.collect([("a.md", "https://x.org/1 https://x.org/1"), ("b.md", "https://x.org/1 https://y.org")])
    assert [(l.url, l.where) for l in links] == [("https://x.org/1", ["a.md", "b.md"]), ("https://y.org", ["b.md"])]


def test_classify():
    assert L.classify("https://x.org", 200).status == "ok"
    assert L.classify("https://x.org", 404).status == "broken"
    assert L.classify("https://www.iso.org/standard/1.html", 403).status == "blocked"
    assert L.classify("https://x.org/p", 403).status == "broken"
    assert L.classify("https://doi.org/10.1/x", 403, final="https://www.sciencedirect.com/a").status == "blocked"
    assert L.classify("https://x.org", 503).status == "unreachable"
    dns = urllib.error.URLError(socket.gaierror(-2, "Name or service not known"))
    assert L.classify("https://no-such-host.invalid", None, dns).status == "broken"
    assert L.classify("https://x.org", None, urllib.error.URLError("timed out")).status == "unreachable"


class FakeClock:
    def __init__(self):
        self.t, self.sleeps = 0.0, []

    def __call__(self):
        return self.t

    def sleep(self, s):
        self.sleeps.append(round(s, 3))
        self.t += s


def test_rate_limit_per_host_and_head_fallback():
    clock, calls = FakeClock(), []

    def status(url, method, timeout):
        calls.append((method, url))
        return (405, url) if method == "HEAD" and "a.org" in url else (200, url)

    c = L.Checker(delay=1.5, status=status, sleep=clock.sleep, clock=clock)
    assert c.check("https://a.org/1").status == "ok"
    assert c.check("https://b.org/1").status == "ok"
    assert calls[:2] == [("HEAD", "https://a.org/1"), ("GET", "https://a.org/1")]
    assert clock.sleeps == [1.5]          # GET waited for the same host; b.org did not wait


def test_retry_once_then_unreachable():
    clock, n = FakeClock(), []

    def status(url, method, timeout):
        n.append(1)
        raise urllib.error.URLError("timed out")

    c = L.Checker(delay=0, status=status, sleep=clock.sleep, clock=clock)
    assert c.check("https://slow.org").status == "unreachable"
    assert len(n) == 2


def test_report_lists_only_problems():
    links = [L.Link("https://ok.org", ["a.md"]), L.Link("https://gone.org", ["b.ipynb cell 3"])]
    outcomes = [L.Outcome("https://ok.org", "ok", 200), L.Outcome("https://gone.org", "broken", 404)]
    text = L.report(links, outcomes)
    assert "1 broken" in text and "https://gone.org" in text and "https://ok.org" not in text.split("\n", 2)[2]
