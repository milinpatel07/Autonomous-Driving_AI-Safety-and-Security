"""Offline tests for scripts/watch_sources.py, replaying recorded responses from tests/fixtures/watch."""
import importlib.util
import sys
import urllib.error
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "tests" / "fixtures" / "watch"
spec = importlib.util.spec_from_file_location("watch_sources", ROOT / "scripts" / "watch_sources.py")
W = importlib.util.module_from_spec(spec)
sys.modules["watch_sources"] = W
spec.loader.exec_module(W)

KITTI = "https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_label_2.zip"
SGO = "https://static.nhtsa.gov/odi/ffdd/sgo-2021-01/SGO-2021-01_Incident_Reports_ADS.csv"
UNECE = "https://unece.org/transport/vehicle-regulations-wp29/standards/addenda-1958-agreement-regulations-141-160"
DOCS = {
    "ISO21448": {"title": "ISO 21448", "watch": [{"method": "iso-open-data", "reference": "ISO 21448:2022"}]},
    "EU2022/1426": {"title": "Reg. (EU) 2022/1426", "watch": [{"method": "eu-cellar", "celex": "32022R1426"}]},
    "UNR157": {"title": "UN R157", "watch": [
        {"method": "regex-page", "url": UNECE, "pattern": r'R157[^"<>]{0,40}\.pdf'},
        {"method": "regex-page", "url": "https://globalautoregs.com/rules/247/texts",
         "pattern": r">\s*((?:Revision \d+(?: \| Amendment \d+)?)|Amendment \d+)\s*<"}]},
    "KITTI": {"title": "KITTI", "watch": [{"method": "headers", "url": KITTI}]},
    "NHTSA-SGO": {"title": "SGO", "watch": [{"method": "csv-header", "url": SGO}]},
    "ROAD": {"title": "ROAD", "watch": [{"method": "json-fields", "url": "https://zenodo.org/api/records/10462796",
                                        "fields": ["revision", "files[].checksum"]}]},
}


@pytest.fixture
def watcher():
    return W.Watcher(W.FixtureFetcher(FIX))


def test_methods_on_recorded_responses(watcher):
    lines, payload = watcher.run(DOCS["ISO21448"]["watch"][0])
    assert payload == {"stage": 9092, "successors": [("ISO/WD 21448", 2060)]}
    assert "successor ISO/WD 21448: stage 2060" in lines
    lines, payload = watcher.run(DOCS["EU2022/1426"]["watch"][0])
    assert "32026R0481" in payload and any(v.startswith("02022R1426-2026") for v in payload)
    lines, payload = watcher.run(DOCS["UNR157"]["watch"][1])
    assert "Revision 1 | Amendment 2" in payload and len(payload) == 8
    lines, payload = watcher.run(DOCS["KITTI"]["watch"][0])
    assert set(payload) == {"etag", "last-modified", "content-length"}
    lines, payload = watcher.run(DOCS["NHTSA-SGO"]["watch"][0])
    assert payload[0] == "Report ID" and len(payload) > 50
    lines, payload = watcher.run(DOCS["ROAD"]["watch"][0])
    assert payload["files[].checksum"][0].startswith("md5:")


def test_changed_new_unchanged_and_unreachable(watcher):
    first = W.check_sources(DOCS, {}, watcher)
    assert {r.status for r in first} == {"new", "unreachable"}
    unreachable = [r for r in first if r.status == "unreachable"]
    assert [r.key for r in unreachable] == [W.watch_key("UNR157", DOCS["UNR157"]["watch"][0])]

    baseline = W.update_baseline({}, first)
    assert W.watch_key("UNR157", DOCS["UNR157"]["watch"][0]) not in baseline      # never stored
    kitti_key = W.watch_key("KITTI", DOCS["KITTI"]["watch"][0])
    baseline[kitti_key] = {"fingerprint": "0" * 16, "summary": ["etag: old"], "checked": "2026-09-01"}
    second = W.check_sources(DOCS, baseline, watcher, affected={"KITTI": ["01_Perception/03_lidar_point_clouds.ipynb"]})
    status = {r.key: r.status for r in second}
    assert status[kitti_key] == "changed"
    assert sum(s == "unchanged" for s in status.values()) == len(status) - 2

    issue = W.issue_markdown(second)
    assert issue.startswith(W.ISSUE_MARKER)
    assert "etag: old" in issue and "01_Perception/03_lidar_point_clouds.ipynb" in issue
    assert "1 source(s) were unreachable" in issue
    report = W.report_markdown(second)
    assert "1 changed" in report and "| unreachable |" in report


def test_page_without_pattern_counts_as_unreachable(tmp_path):
    (tmp_path / "p.html").write_text("<html>redesigned</html>")
    (tmp_path / "index.json").write_text('{"GET https://example.org/p": {"status": 200, "body": "p.html"}}')
    w = W.Watcher(W.FixtureFetcher(tmp_path))
    res = W.check_sources({"X": {"title": "X", "watch": [{"method": "regex-page", "url": "https://example.org/p",
                                                          "pattern": "R157"}]}}, {}, w)
    assert res[0].status == "unreachable" and "pattern not found" in res[0].error


def test_http_fetcher_retries_then_gives_up(monkeypatch):
    calls, sleeps = [], []

    def fail(req, timeout):
        calls.append(req.full_url)
        raise urllib.error.URLError("connection reset")

    monkeypatch.setattr(W.urllib.request, "urlopen", fail)
    f = W.HttpFetcher(delay=0, retries=3, sleep=sleeps.append)
    with pytest.raises(W.Unreachable):
        f("https://example.org/x")
    assert len(calls) == 3 and sleeps == [1, 2, 4]


def test_http_fetcher_does_not_retry_forbidden(monkeypatch):
    calls = []

    def forbidden(req, timeout):
        calls.append(1)
        raise urllib.error.HTTPError(req.full_url, 403, "Forbidden", {}, None)

    monkeypatch.setattr(W.urllib.request, "urlopen", forbidden)
    with pytest.raises(W.Unreachable):
        W.HttpFetcher(delay=0, sleep=lambda s: None)("https://example.org/y")
    assert calls == [1]


def test_pick():
    data = {"a": {"b": 3}, "files": [{"checksum": "x"}, {"checksum": "y"}]}
    assert W.pick(data, "a.b") == 3 and W.pick(data, "files[].checksum") == ["x", "y"]


def test_registry_watch_specs_are_valid():
    pytest.importorskip("yaml")
    sys.path.insert(0, str(ROOT / "scripts"))
    import check_references as C

    methods = {"iso-open-data", "eu-cellar", "regex-page", "headers", "csv-header", "json-fields"}
    docs = C.load_registry()["documents"]
    specs = [s for d in docs.values() for s in d.get("watch") or []]
    assert specs and all(s["method"] in methods for s in specs)
    keys = [W.watch_key(k, s) for k, d in docs.items() for s in d.get("watch") or []]
    assert len(keys) == len(set(keys))
