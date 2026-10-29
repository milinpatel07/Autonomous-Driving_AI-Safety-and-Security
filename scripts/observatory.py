"""Field-safety observatory: fetch public field data, compute summaries, render a MyST page.

Sources (all public; see the page for licences, access dates and caveats):

* NHTSA Standing General Order 2021-01 incident reports, ADS and Level 2 ADAS
  (current files under the third amended order and the 2021-2025 archive).
* California DMV annual autonomous-vehicle mileage and disengagement reports.
* Waymo Safety Impact Data Hub: rider-only miles (CSV1) and the rider-only crash list
  with SGO report IDs (CSV2), used only to form rates with exact Poisson intervals.

Outputs (deterministic for given inputs):

* ``site/observatory.md``                 the page (MyST markdown)
* ``site/observatory/*.svg``              figures
* ``site/observatory/data/*.csv``         summary tables (downloadable)
* ``site/observatory/data/snapshot.json`` counts, release dates, file hashes

Usage::

    python scripts/observatory.py            # fetch (conditional requests), compute, render
    python scripts/observatory.py --offline  # use the local cache only

The cache lives in ``$AVSAFETY_CACHE/observatory`` (default ``~/.cache/avsafety/observatory``).
Exit status: 0 page rendered; 3 the NHTSA data are unavailable (page left unchanged except
for a notice at the top).
"""
from __future__ import annotations

import argparse
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
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

USER_AGENT = ("avsafety-observatory/1.0 (open course on automated-driving safety; "
              "+https://github.com/milinpatel07/Autonomous-Driving_AI-Safety-and-Security)")

NHTSA_BASE = "https://static.nhtsa.gov/odi/ffdd/sgo-2021-01/"
NHTSA_PAGE = "https://www.nhtsa.gov/laws-regulations/standing-general-order-crash-reporting"
SGO_FILES = {  # key: (url, kind, regime file)
    "sgo_ads_current": (NHTSA_BASE + "SGO-2021-01_Incident_Reports_ADS.csv", "ADS", "current"),
    "sgo_adas_current": (NHTSA_BASE + "SGO-2021-01_Incident_Reports_ADAS.csv", "ADAS", "current"),
    "sgo_ads_archive": (NHTSA_BASE + "Archive-2021-2025/SGO-2021-01_Incident_Reports_ADS.csv", "ADS", "archive"),
    "sgo_adas_archive": (NHTSA_BASE + "Archive-2021-2025/SGO-2021-01_Incident_Reports_ADAS.csv", "ADAS", "archive"),
}
SGO_DICTIONARY = NHTSA_BASE + "SGO-2021-01_Data_Element_Definitions.pdf"
SGO_DICTIONARY_ARCHIVE = NHTSA_BASE + "Archive-2021-2025/SGO-2021-01_Data_Element_Definitions.pdf"
SGO_ICR = "https://omb.report/icr/202605-2127-005/doc/169129500.pdf"

DMV_FILE = "https://www.dmv.ca.gov/portal/file/{year}-autonomous-mileage-reports-csv/"
DMV_NEWS_2025 = ("https://www.dmv.ca.gov/portal/news-and-media/autonomous-vehicle-permit-holders-in-california-"
                 "logged-more-than-9-million-test-miles-between-december-1-2024-and-november-30-2025/")
DMV_NEW_REGS = ("https://www.dmv.ca.gov/portal/news-and-media/new-autonomous-vehicle-regulations-strengthen-"
                "oversight-and-enforcement-authorize-trucks-and-transit/")
DMV_CONDITIONS = "https://www.dmv.ca.gov/portal/conditions-of-use/"
DMV_COLLISIONS = "https://tims.berkeley.edu/tools/avsafety.php"
DMV_FIRST_YEAR = 2020

WAYMO_PAGE = "https://waymo.com/safety/impact/"
WAYMO_BUCKET = "https://storage.googleapis.com/waymo-uploads/files/documents/safety/safety-impact-data/"
WAYMO_PINNED = {  # used only when the hub page cannot be read
    "csv1": "CSV1 - RO Miles per Location 202009-202606-2022benchmark.csv",
    "csv2": "CSV2 - Crashes with SGO ID and Group Membership 202009-202606-2022benchmark.csv",
}
# Counties with their own RO-mile figure in CSV1, grouped into the service areas used on the page.
WAYMO_AREAS = {"Maricopa": "Phoenix", "San Francisco": "SF Bay Area", "San Mateo": "SF Bay Area",
               "Santa Clara": "SF Bay Area", "Los Angeles": "Los Angeles", "Travis": "Austin",
               "Fulton": "Atlanta", "DeKalb": "Atlanta"}
WAYMO_OUTCOMES = {"police-reported crash": "Is Police-Reported",
                  "any-injury-reported crash": "Is Any-Injury-Reported",
                  "air-bag deployment (any vehicle)": "Is Any Vehicle Airbag Deployment",
                  "suspected serious injury or worse": "Is Suspected Serious Injury+"}

# Reporting-rule changes marked on every time axis (verified: SGO data dictionaries; OMB ICR 2127-0754).
RULE_CHANGES = [("2021-07-01", "SGO reporting starts (order of 29 Jun 2021)"),
                ("2023-05-15", "2nd amended order in force"),
                ("2025-06-16", "3rd amended order in force")]
REGIMES = [("original / 1st amended order", "2021-07", "2023-04"),
           ("2nd amended order", "2023-05", "2025-05"),
           ("3rd amended order", "2025-06", "2100-12")]
PLOT_START = "2021-07"

SEVERITY_ORDER = ["no injury reported", "minor", "moderate", "serious", "fatal", "unknown"]
PARTNER_ORDER = ["passenger vehicle", "heavy truck or bus", "motorcycle", "pedestrian, cyclist or other VRU",
                 "fixed object", "other", "unknown"]
ROAD_ORDER = ["street", "intersection", "highway or freeway", "parking area", "rural road", "other", "unknown"]
MOVEMENT_ORDER = ["stopped or parked", "proceeding straight", "turning", "lane change, merge or entering",
                  "lane or road departure", "backing or parking", "other", "unknown"]
DIMENSIONS = {"partner": ("Crash partner", PARTNER_ORDER),
              "road": ("Roadway type", ROAD_ORDER),
              "severity": ("Highest injury severity alleged", SEVERITY_ORDER),
              "movement": ("Subject-vehicle pre-crash movement", MOVEMENT_ORDER)}

# Okabe-Ito hues in an order validated for colour-vision deficiency; grey for other/unknown.
CATEGORICAL = ["#0072B2", "#E69F00", "#009E73", "#D55E00", "#56B4E9", "#CC79A7"]
OTHER_GREY, UNKNOWN_GREY = "#8C8C8C", "#C8C8C8"
SEVERITY_COLOURS = ["#FBC793", "#FDAE6B", "#F16913", "#C24A07", "#6A2504", UNKNOWN_GREY]
KIND_LABEL = {"ADS": "ADS", "ADAS": "Level 2 ADAS"}
CBI = "[REDACTED, MAY CONTAIN CONFIDENTIAL BUSINESS INFORMATION]"


# =========================================================================== fetching
@dataclass
class Fetched:
    """A source file in the local cache and how it was obtained in this run."""
    key: str
    url: str
    path: Path | None
    status: str                      # fresh | not-modified | cached-offline | cached-unreachable | missing
    meta: dict = field(default_factory=dict)
    error: str = ""

    @property
    def ok(self) -> bool:
        return self.path is not None and self.path.exists()


class Fetcher:
    """Cached, polite HTTP fetcher: conditional requests, retries with back-off, one request per second."""

    def __init__(self, cache: Path, offline: bool = False, retries: int = 3, timeout: float = 120.0):
        self.cache, self.offline, self.retries, self.timeout = cache, offline, retries, timeout
        self._last_request = 0.0

    def _meta_path(self, path: Path) -> Path:
        return path.with_name(path.name + ".meta.json")

    def _read_meta(self, path: Path) -> dict:
        mp = self._meta_path(path)
        return json.loads(mp.read_text()) if mp.exists() else {}

    def _request(self, url: str, headers: dict):
        wait = 1.0 - (time.monotonic() - self._last_request)
        if wait > 0:
            time.sleep(wait)
        self._last_request = time.monotonic()
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, **headers})
        return urllib.request.urlopen(req, timeout=self.timeout)

    def get(self, key: str, url: str, relpath: str, expect: str | None = None) -> Fetched:
        """Return the cached file for ``url``, refreshing it unless offline.

        ``expect`` is a substring the Content-Type must contain (e.g. 'csv'); a mismatch
        (such as an HTML 'not found' page served with status 200) counts as missing.
        """
        path = self.cache / relpath
        meta = self._read_meta(path) if path.exists() else {}
        if self.offline:
            return Fetched(key, url, path if path.exists() else None,
                           "cached-offline" if path.exists() else "missing", meta)
        headers = {}
        if path.exists() and meta.get("etag"):
            headers["If-None-Match"] = meta["etag"]
        if path.exists() and meta.get("last_modified"):
            headers["If-Modified-Since"] = meta["last_modified"]
        error = ""
        for attempt in range(self.retries):
            try:
                with self._request(url, headers) as resp:
                    ctype = resp.headers.get("Content-Type", "")
                    if expect and expect not in ctype.lower():
                        error = f"unexpected content type {ctype!r}"
                        break
                    data = resp.read()
                    new_meta = {"url": url, "fetched": time.strftime("%Y-%m-%d", time.gmtime()),
                                "last_modified": resp.headers.get("Last-Modified", ""),
                                "etag": resp.headers.get("ETag", ""),
                                "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
                    path.parent.mkdir(parents=True, exist_ok=True)
                    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
                    tmp.write_bytes(data)
                    os.replace(tmp, path)
                    self._meta_path(path).write_text(json.dumps(new_meta, indent=1, sort_keys=True))
                    return Fetched(key, url, path, "fresh", new_meta)
            except urllib.error.HTTPError as exc:
                if exc.code == 304:
                    meta["checked"] = time.strftime("%Y-%m-%d", time.gmtime())
                    self._meta_path(path).write_text(json.dumps(meta, indent=1, sort_keys=True))
                    return Fetched(key, url, path, "not-modified", meta)
                error = f"HTTP {exc.code}"
                if exc.code in (403, 404, 410):
                    break
            except (urllib.error.URLError, OSError) as exc:
                error = str(getattr(exc, "reason", exc))
            time.sleep(2 ** (attempt + 1))
        return Fetched(key, url, path if path.exists() else None,
                       "cached-unreachable" if path.exists() else "missing", meta, error)

    def get_text(self, url: str) -> str | None:
        """Small uncached text page (used only to discover current file names)."""
        if self.offline:
            return None
        try:
            with self._request(url, {}) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except (urllib.error.URLError, OSError):
            return None


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def release_date(fetched: Fetched) -> str:
    """Publication date of a source file (HTTP Last-Modified, else the date it was fetched)."""
    lm = fetched.meta.get("last_modified")
    if lm:
        return parsedate_to_datetime(lm).strftime("%Y-%m-%d")
    if fetched.meta.get("fetched"):
        return fetched.meta["fetched"]
    if fetched.path is not None and fetched.path.exists():  # no metadata: file modification date
        return time.strftime("%Y-%m-%d", time.gmtime(fetched.path.stat().st_mtime))
    return ""


def access_date(fetched: Fetched) -> str:
    return fetched.meta.get("checked") or fetched.meta.get("fetched") or release_date(fetched)


# =========================================================================== SGO cleaning
def parse_month(series):
    """'MAY-2025' -> Period('2025-05'); unparseable -> NaT."""
    import pandas as pd
    return pd.to_datetime(series.astype("string").str.strip().str.title(), format="%b-%Y",
                          errors="coerce").dt.to_period("M")


def severity_group(value) -> str:
    """Map both the archive ('Minor') and current ('Minor W/ Hospitalization') vocabularies."""
    s = str(value).lower() if isinstance(value, str) else ""
    for key, group in (("fatal", "fatal"), ("serious", "serious"), ("moderate", "moderate"),
                       ("minor", "minor"), ("no injur", "no injury reported")):
        if key in s:
            return group
    return "unknown"


def partner_group(value) -> str:
    s = value if isinstance(value, str) else ""
    if s.startswith("Non-Motorist"):
        return "pedestrian, cyclist or other VRU"
    return {"Passenger Car": "passenger vehicle", "SUV": "passenger vehicle", "Pickup Truck": "passenger vehicle",
            "Van": "passenger vehicle", "Heavy Truck": "heavy truck or bus", "Bus": "heavy truck or bus",
            "Motorcycle": "motorcycle", "Other Fixed Object": "fixed object", "Pole / Tree": "fixed object",
            "Unknown": "unknown", "": "unknown"}.get(s, "other")


def road_group(value) -> str:
    s = value if isinstance(value, str) else ""
    return {"Street": "street", "Intersection": "intersection", "Highway / Freeway": "highway or freeway",
            "Parking Lot": "parking area", "Parking Garage": "parking area", "Rural Road": "rural road",
            "Unknown": "unknown", "": "unknown"}.get(s, "other")


def movement_group(value) -> str:
    s = value if isinstance(value, str) else ""
    groups = {"stopped or parked": ("Stopped", "Parked"),
              "proceeding straight": ("Proceeding Straight",),
              "turning": ("Making Left Turn", "Making Right Turn", "Making U-Turn"),
              "lane change, merge or entering": ("Changing Lanes", "Merging", "Passing", "Entering Traffic",
                                                 "Crossing into Opposing Lane", "Traveling Wrong Way"),
              "lane or road departure": ("Lane / Road Departure",),
              "backing or parking": ("Backing", "Parking Maneuver"),
              "unknown": ("Unknown", "")}
    for group, values in groups.items():
        if s in values:
            return group
    return "other"


def short_entity(name) -> str:
    """'Waymo LLC' -> 'Waymo'; 'Mercedes-Benz USA, LLC' -> 'Mercedes-Benz'."""
    s = re.sub(r"\(.*?\)", "", str(name))
    s = re.sub(r",?\s*\b(Inc\.?|Incorporated|LLC|Corp\.?|CORP|Corporation|Operations|America|USA|US|Company|"
               r"of North America|Motor|Technologies|Group of)\b\.?", "", s)
    return re.sub(r"\s+", " ", s).strip(" ,.&") or str(name)


def regime_of(month) -> str:
    """Reporting regime by incident month (boundary months straddle two regimes)."""
    m = str(month)
    for name, start, end in REGIMES:
        if start <= m <= end:
            return name
    return "before SGO reporting"


def harmonise_sgo(df, kind: str, source: str):
    """Reduce one SGO CSV (archive or current schema) to the columns the observatory uses."""
    import pandas as pd
    out = pd.DataFrame({
        "kind": kind, "source": source,
        "report_id": df["Report ID"].astype(str).str.strip(),
        "version": pd.to_numeric(df["Report Version"], errors="coerce").fillna(1).astype(int),
        "report_type": df["Report Type"].astype("string"),
        "entity": df["Reporting Entity"].map(short_entity),
        "incident_id": df["Same Incident ID"].astype("string").str.strip(),
        "incident_month": parse_month(df["Incident Date"]),
        "submitted_month": parse_month(df["Report Submission Date"]),
        "state": df["State"].astype("string") if "State" in df else pd.Series(pd.NA, index=df.index, dtype="string"),
        "partner": df["Crash With"].map(partner_group),
        "road": df["Roadway Type"].map(road_group),
        "severity": df["Highest Injury Severity Alleged"].map(severity_group),
        "movement": df["SV Pre-Crash Movement"].map(movement_group),
        "narrative_cbi": df["Narrative - CBI?"].astype("string").str.strip().eq("Y")
        | df["Narrative"].astype("string").eq(CBI),
        "telematics": df["Source - Telematics"].astype("string").str.strip().eq("Y")
        if "Source - Telematics" in df else False,
    })
    out["vru"] = out["partner"].eq("pedestrian, cyclist or other VRU")
    out["sev_rank"] = out["severity"].map({s: i for i, s in enumerate(SEVERITY_ORDER[:-1])}).fillna(-1).astype(int)
    out = out[~out["report_type"].eq("No New or Updated Incident Reports")]
    return out.reset_index(drop=True)


def latest_versions(reports):
    """Keep the latest version of each report; on a tie the current file wins over the archive."""
    order = reports.assign(_src=reports["source"].eq("current").astype(int))
    order = order.sort_values(["report_id", "version", "_src"], kind="mergesort")
    return order.groupby(["kind", "report_id"], sort=False).tail(1).drop(columns="_src").reset_index(drop=True)


def to_incidents(reports):
    """One row per crash (``Same Incident ID`` within a system type).

    The representative report is the one alleging the highest severity; ties go to the
    lowest report ID, so the result does not depend on file order. ``n_reports`` and
    ``n_entities`` record how many reports and reporting entities the crash produced.
    """
    r = reports.dropna(subset=["incident_id"]).copy()
    r = r.sort_values(["kind", "incident_id", "sev_rank", "report_id"], ascending=[True, True, False, True],
                      kind="mergesort")
    g = r.groupby(["kind", "incident_id"], sort=False)
    inc = g.head(1).copy()
    inc["n_reports"] = g["report_id"].transform("nunique").loc[inc.index]
    inc["n_entities"] = g["entity"].transform("nunique").loc[inc.index]
    inc["first_submitted"] = g["submitted_month"].transform("min").loc[inc.index]
    return inc.reset_index(drop=True)


def monthly_counts(reports, incidents, start: str = PLOT_START):
    """Reports (latest versions) and crashes per incident month and system type."""
    import pandas as pd
    rows = []
    for kind in ("ADS", "ADAS"):
        rep = reports[reports["kind"].eq(kind)]["incident_month"].value_counts()
        inc = incidents[incidents["kind"].eq(kind)]["incident_month"].value_counts()
        end = max(rep.index.max(), inc.index.max())
        for month in pd.period_range(start, end, freq="M"):
            rows.append({"kind": kind, "incident_month": str(month), "reports": int(rep.get(month, 0)),
                         "crashes": int(inc.get(month, 0)), "regime": regime_of(month)})
    return pd.DataFrame(rows)


def monthly_by(incidents, dim: str, start: str = PLOT_START):
    """Long table: crashes per (system type, incident month, category of ``dim``)."""
    import pandas as pd
    order = DIMENSIONS[dim][1]
    d = incidents[incidents["incident_month"] >= pd.Period(start, "M")]
    tab = d.groupby(["kind", "incident_month", dim]).size().rename("crashes").reset_index()
    tab[dim] = pd.Categorical(tab[dim], order, ordered=True)
    tab = tab.sort_values(["kind", "incident_month", dim]).rename(columns={dim: "category"})
    tab["incident_month"] = tab["incident_month"].astype(str)
    tab.insert(2, "dimension", dim)
    return tab.reset_index(drop=True)


def concentration(incidents):
    """Per system type and incident year: entities, share of the largest entity, top-3 share, HHI."""
    import pandas as pd
    rows = []
    d = incidents.dropna(subset=["incident_month"])
    for (kind, year), grp in d.groupby([d["kind"], d["incident_month"].dt.year]):
        share = grp["entity"].value_counts(normalize=True)
        rows.append({"kind": kind, "incident_year": int(year), "crashes": len(grp), "entities": len(share),
                     "largest_entity": share.index[0], "largest_share_pct": round(100 * share.iloc[0], 1),
                     "top3_share_pct": round(100 * share.iloc[:3].sum(), 1),
                     "hhi": int(round(10000 * (share ** 2).sum()))})
    return pd.DataFrame(rows).sort_values(["kind", "incident_year"]).reset_index(drop=True)


def entity_table(incidents, min_crashes: int = 10):
    """Crashes per reporting entity and regime, alphabetical (not a ranking); small entities pooled."""
    import pandas as pd
    d = incidents.assign(regime=incidents["incident_month"].map(regime_of))
    tab = d.groupby(["kind", "entity", "regime"]).size().unstack(fill_value=0)
    tab = tab.reindex(columns=[r[0] for r in REGIMES], fill_value=0)
    tab["total"] = tab.sum(axis=1)
    out = []
    for kind, grp in tab.groupby(level=0):
        grp = grp.droplevel(0)
        big, small = grp[grp["total"] >= min_crashes], grp[grp["total"] < min_crashes]
        big = big.sort_index(key=lambda s: s.str.lower())
        if len(small):
            big.loc[f"{len(small)} other entities (< {min_crashes} crashes each)"] = small.sum()
        out.append(big.reset_index().rename(columns={"index": "entity"}).assign(kind=kind))
    res = pd.concat(out, ignore_index=True)
    return res[["kind", "entity"] + [r[0] for r in REGIMES] + ["total"]]


def data_quality(incidents):
    """Share of crashes with unknown fields or a redacted narrative, by system type and regime."""
    import pandas as pd
    rows = []
    d = incidents.assign(regime=incidents["incident_month"].map(regime_of))
    for (kind, regime), g in d.groupby(["kind", "regime"]):
        if regime == "before SGO reporting":
            continue
        rows.append({"kind": kind, "regime": regime, "crashes": len(g),
                     "partner_unknown_pct": round(100 * g["partner"].eq("unknown").mean(), 1),
                     "road_unknown_pct": round(100 * g["road"].eq("unknown").mean(), 1),
                     "severity_unknown_pct": round(100 * g["severity"].eq("unknown").mean(), 1),
                     "movement_unknown_pct": round(100 * g["movement"].eq("unknown").mean(), 1),
                     "narrative_redacted_pct": round(100 * g["narrative_cbi"].mean(), 1),
                     "notice_via_telematics_pct": round(100 * g["telematics"].mean(), 1),
                     "multi_report_crashes_pct": round(100 * (g["n_reports"] > 1).mean(), 1)})
    order = {r[0]: i for i, r in enumerate(REGIMES)}
    out = pd.DataFrame(rows)
    return out.sort_values(["kind", "regime"], key=lambda s: s.map(order) if s.name == "regime" else s) \
              .reset_index(drop=True)


def report_index(reports):
    """Compact index of the current-file reports, used to diff releases."""
    r = reports[reports["source"].eq("current")]
    idx = r[["kind", "report_id", "version", "incident_id"]].sort_values(["kind", "report_id"])
    return idx.reset_index(drop=True)


def diff_reports(previous, current):
    """New reports, updated reports and new crashes in ``current`` relative to ``previous``."""
    prev_v = dict(zip(zip(previous["kind"], previous["report_id"]), previous["version"]))
    prev_inc = set(zip(previous["kind"], previous["incident_id"].astype(str)))
    keys = list(zip(current["kind"], current["report_id"]))
    is_new = [k not in prev_v for k in keys]
    is_upd = [(k in prev_v) and (v > prev_v[k]) for k, v in zip(keys, current["version"])]
    new_inc = [(k, str(i)) not in prev_inc for k, i in zip(current["kind"], current["incident_id"])]
    cur = current.assign(new_report=is_new, updated_report=is_upd, new_incident=new_inc)
    return cur


# =========================================================================== exposure-based rates
def garwood(events: int, exposure: float, confidence: float = 0.95) -> tuple[float, float]:
    """Exact (Garwood) Poisson interval for events/exposure (delegates to avsafety.validation)."""
    from avsafety.validation import poisson_rate_interval
    return poisson_rate_interval(int(events), float(exposure), confidence)


def waymo_rates(csv1, csv2):
    """Rider-only crash rates per million miles with 95 % Garwood intervals.

    Numerator and denominator use the same counties (those with their own mileage in CSV1)
    and the same period (CSV1 and CSV2 of one release). Crashes in other counties are excluded.
    """
    import pandas as pd
    miles = csv1.set_index("County Name")["Waymo RO Miles (Millions)"].astype(float)
    miles = miles[miles.index.isin(WAYMO_AREAS)]
    crashes = csv2[csv2["County"].isin(miles.index)].assign(area=lambda d: d["County"].map(WAYMO_AREAS))
    area_miles = miles.groupby(miles.index.map(WAYMO_AREAS)).sum()
    rows = []
    for area in ["all areas with published miles"] + sorted(area_miles.index):
        sub = crashes if area.startswith("all") else crashes[crashes["area"].eq(area)]
        exp = float(area_miles.sum() if area.startswith("all") else area_miles[area])
        for outcome, col in WAYMO_OUTCOMES.items():
            k = int(sub[col].astype(str).str.lower().eq("true").sum())
            lo, hi = garwood(k, exp)
            rows.append({"area": area, "outcome": outcome, "crashes": k, "ro_miles_million": round(exp, 3),
                         "rate_per_million_miles": round(k / exp, 4), "ci95_low": round(lo, 4),
                         "ci95_high": round(hi, 4)})
    excluded = int((~csv2["County"].isin(miles.index)).sum())
    return pd.DataFrame(rows), excluded


# =========================================================================== California DMV
DMV_CANONICAL = [("aimotive", "aiMotive"), ("apollo", "Apollo (Baidu)"), ("apple", "Apple"), ("argo", "Argo AI"),
                 ("aurora", "Aurora"), ("autox", "AutoX"), ("bmw", "BMW"), ("bosch", "Bosch"), ("cruise", "Cruise"),
                 ("deeproute", "DeepRoute.ai"), ("didi", "DiDi"), ("easymile", "EasyMile"), ("gatik", "Gatik"),
                 ("ghost", "Ghost Autonomy"), ("imagry", "Imagry"), ("intel", "Intel"), ("lyft", "Lyft"),
                 ("mercedes", "Mercedes-Benz"), ("motional", "Motional"), ("nissan", "Nissan"),
                 ("nullmax", "Nullmax"), ("nuro", "Nuro"), ("nvidia", "NVIDIA"), ("pony", "Pony.ai"),
                 ("qcraft", "QCraft"), ("qualcomm", "Qualcomm"), ("toyota research", "Toyota Research Institute"),
                 ("woven", "Woven by Toyota"), ("valeo", "Valeo"), ("vueron", "Vueron"), ("waymo", "Waymo"),
                 ("weride", "WeRide"), ("zoox", "Zoox"), ("udelv", "Udelv"), ("ridecell", "Ridecell"),
                 ("telenav", "Telenav"), ("sf motors", "SF Motors")]


def canonical_manufacturer(name) -> str:
    """Unify the spelling variants of the DMV files ('WAYMO LLC', 'Waymo LLC', 'Weride Corp')."""
    s = str(name).strip().lower()
    for key, canon in DMV_CANONICAL:
        if key in s:
            return canon
    return short_entity(str(name).strip())


def to_number(value) -> float:
    """Parse DMV number cells such as '1,049.54', '830 .04' or ' 12 '; blanks -> 0."""
    s = re.sub(r"[^0-9.\-]", "", str(value)) if value is not None else ""
    try:
        return float(s) if s not in ("", ".", "-") else 0.0
    except ValueError:
        return 0.0


def parse_dmv_mileage(path_or_buffer, report_year: int):
    """One DMV annual mileage file (drivered testing) -> rows per vehicle with miles and disengagements.

    The reporting year runs from 1 December of the previous year to 30 November.
    Annual miles = the 'ANNUAL TOTAL' cell when it agrees with the monthly cells within 1 %,
    otherwise the sum of the monthly cells (``mileage_check`` records which).
    """
    import pandas as pd
    df = pd.read_csv(path_or_buffer, dtype=str, encoding="cp1252", keep_default_na=False)
    df.columns = [str(c).strip() for c in df.columns]
    df = df.loc[:, ~df.columns.str.startswith("Unnamed")]
    month_cols = [c for c in df.columns if re.fullmatch(r"[A-Z]{3,4} \d{4}", c.upper())]
    df = df[df["Manufacturer"].str.strip().ne("")]
    month_sum = df[month_cols].apply(lambda col: col.map(to_number)).sum(axis=1)
    annual = df["ANNUAL TOTAL"].map(to_number) if "ANNUAL TOTAL" in df else month_sum
    agree = (annual - month_sum).abs() <= 0.01 * month_sum.clip(lower=1)
    return pd.DataFrame({"report_year": report_year,
                         "manufacturer": df["Manufacturer"].map(canonical_manufacturer),
                         "vin": df["VIN NUMBER"].str.strip(),
                         "disengagements": df["Annual Total of Disengagements"].map(to_number).astype(int),
                         "miles": annual.where(agree, month_sum).round(2),
                         "mileage_check": agree.map({True: "annual total", False: "monthly sum"})})


def disengagement_rates(vehicles, min_miles: float = 0.0):
    """Disengagements per 1,000 autonomous miles by manufacturer and reporting year."""
    g = vehicles.groupby(["report_year", "manufacturer"]).agg(
        vehicles=("vin", "nunique"), miles=("miles", "sum"), disengagements=("disengagements", "sum")).reset_index()
    g = g[g["miles"] > max(min_miles, 0)].copy()
    g["per_1000_miles"] = (1000 * g["disengagements"] / g["miles"]).round(3)
    g["miles"] = g["miles"].round(0).astype(int)
    return g.sort_values(["report_year", "manufacturer"],
                         key=lambda s: s.str.lower() if s.name == "manufacturer" else s).reset_index(drop=True)


# =========================================================================== figures
def _plt():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"svg.hashsalt": "avsafety-observatory", "svg.fonttype": "none",
                         "font.family": "DejaVu Sans", "font.size": 8.5, "axes.titlesize": 9.5,
                         "axes.labelsize": 8.5, "axes.spines.top": False, "axes.spines.right": False,
                         "axes.grid": True, "grid.alpha": 0.25, "grid.linewidth": 0.6,
                         "axes.edgecolor": "#555555", "xtick.color": "#333333", "ytick.color": "#333333",
                         "figure.facecolor": "white", "axes.facecolor": "white", "legend.frameon": False})
    return plt


def _save(fig, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, format="svg", bbox_inches="tight", metadata={"Date": None, "Creator": None})
    import matplotlib.pyplot as plt
    plt.close(fig)


def _mark_rules(ax, provisional_start=None, end=None):
    """Dashed lines at the amended orders; grey band from ``provisional_start`` to ``end`` (timestamps)."""
    import pandas as pd
    for date, _ in RULE_CHANGES[1:]:
        ax.axvline(pd.Timestamp(date), color="#333333", lw=0.9, ls=(0, (4, 2)))
    if provisional_start is not None:
        ax.axvspan(provisional_start, end, color="#999999", alpha=0.18, lw=0)


def _rule_labels(ax, ymax):
    import pandas as pd
    for date, label in RULE_CHANGES[1:]:
        ax.text(pd.Timestamp(date) + pd.Timedelta(days=12), ymax, label.replace(" in force", ""),
                fontsize=7, va="top", ha="left", color="#333333")


def fig_monthly(monthly, provisional_from: str, path: Path):
    import pandas as pd
    plt = _plt()
    fig, axes = plt.subplots(2, 1, figsize=(7.2, 5.0), sharex=True)
    for ax, kind in zip(axes, ("ADS", "ADAS")):
        m = monthly[monthly["kind"].eq(kind)]
        x = pd.PeriodIndex(m["incident_month"], freq="M").to_timestamp()
        ax.bar(x, m["crashes"], width=24, color=CATEGORICAL[0], label="crashes (unique incidents)",
               edgecolor="white", linewidth=0.3)
        ax.plot(x, m["reports"], color=CATEGORICAL[1], lw=1.4, label="reports (latest version)")
        ax.set_ylabel("per incident month")
        ax.set_title(KIND_LABEL[kind], loc="left", fontweight="bold")
        ax.set_ylim(0, max(m["reports"].max(), m["crashes"].max()) * 1.22)
        ax.set_xlim(x.min() - pd.Timedelta(days=20), x.max() + pd.Timedelta(days=20))
        _mark_rules(ax, pd.Period(provisional_from, "M").to_timestamp() - pd.Timedelta(days=14),
                    x.max() + pd.Timedelta(days=20))
        _rule_labels(ax, ax.get_ylim()[1] * 0.99)
    axes[0].legend(loc="upper left", bbox_to_anchor=(0, 0.86), fontsize=7.5)
    axes[1].set_xlabel("incident month  (grey band: provisional, reports still arriving)")
    fig.tight_layout()
    _save(fig, path)


def fig_composition(table, dim: str, provisional_from: str, path: Path):
    """Quarterly stacked counts by category, ADS and Level 2 ADAS in two panels."""
    import pandas as pd
    plt = _plt()
    title, order = DIMENSIONS[dim]
    if dim == "severity":
        colours = dict(zip(order, SEVERITY_COLOURS))
    else:
        named = [c for c in order if c not in ("other", "unknown")]
        colours = dict(zip(named, CATEGORICAL))
        colours.update({"other": OTHER_GREY, "unknown": UNKNOWN_GREY})
    t = table.assign(quarter=pd.PeriodIndex(table["incident_month"], freq="M").asfreq("Q"))
    fig, axes = plt.subplots(2, 1, figsize=(7.2, 5.4), sharex=True)
    for ax, kind in zip(axes, ("ADS", "ADAS")):
        q = t[t["kind"].eq(kind)].pivot_table(index="quarter", columns="category", values="crashes",
                                               aggfunc="sum", fill_value=0, observed=False)
        q = q.reindex(columns=[c for c in order if c in q.columns])
        x = q.index.to_timestamp() + pd.Timedelta(days=45)
        bottom = None
        for cat in q.columns:
            ax.bar(x, q[cat], width=78, bottom=bottom, color=colours[cat], label=cat,
                   edgecolor="white", linewidth=0.6)
            bottom = q[cat] if bottom is None else bottom + q[cat]
        ax.set_title(KIND_LABEL[kind], loc="left", fontweight="bold")
        ax.set_ylabel("crashes per quarter")
        ax.set_ylim(0, q.sum(axis=1).max() * 1.2)
        ax.set_xlim(x.min() - pd.Timedelta(days=50), x.max() + pd.Timedelta(days=50))
        _mark_rules(ax, pd.Period(provisional_from, "M").asfreq("Q").to_timestamp(), x.max() + pd.Timedelta(days=45))
    handles, labels = axes[0].get_legend_handles_labels()
    h2, l2 = axes[1].get_legend_handles_labels()
    for h, l in zip(h2, l2):
        if l not in labels:
            handles.append(h), labels.append(l)
    rank = {c: i for i, c in enumerate(order)}
    pairs = sorted(zip(handles, labels), key=lambda p: rank[p[1]])
    fig.legend([p[0] for p in pairs], [p[1] for p in pairs], loc="lower center", ncol=min(4, len(pairs)),
               fontsize=7.5, title=title, title_fontsize=8, bbox_to_anchor=(0.5, -0.01))
    axes[1].set_xlabel("quarter of incident  (dashed: amended order in force; grey: provisional)")
    fig.tight_layout(rect=(0, 0.11 if len(pairs) > 4 else 0.07, 1, 1))
    _save(fig, path)


def fig_disengagements(rates, path: Path, min_miles: float = 10_000):
    import numpy as np
    plt = _plt()
    latest = rates["report_year"].max()
    keep = rates[(rates["report_year"].eq(latest)) & (rates["miles"] >= min_miles)]["manufacturer"]
    d = rates[rates["manufacturer"].isin(keep) & (rates["miles"] >= min_miles)]
    names = sorted(keep, key=str.lower)
    years = sorted(d["report_year"].unique())[-6:]
    d = d[d["report_year"].isin(years)]
    ramp = ["#C6DBEF", "#9ECAE1", "#6BAED6", "#3182BD", "#08519C", "#08306B"][-len(years):]
    fig, ax = plt.subplots(figsize=(7.2, 0.42 * len(names) + 1.4))
    for i, name in enumerate(names):
        r = d[d["manufacturer"].eq(name)].sort_values("report_year")
        vals = r["per_1000_miles"].clip(lower=0.005)
        ax.plot(vals, [i] * len(r), color="#BBBBBB", lw=1, zorder=1)
        for (_, row), v in zip(r.iterrows(), vals):
            ax.scatter(v, i, s=34 if row["report_year"] == latest else 22,
                       color=ramp[years.index(row["report_year"])], edgecolor="white", linewidth=0.8, zorder=2)
        last = r[r["report_year"].eq(latest)].iloc[0]
        ax.text(vals.max() * 1.25, i, f"{last['miles'] / 1000:,.0f}k mi", va="center", fontsize=7, color="#555555")
    ax.set_xscale("log")
    ax.set_yticks(np.arange(len(names)), names)
    ax.invert_yaxis()
    ax.set_xlabel("disengagements per 1,000 autonomous miles (log scale; zero shown at 0.005)")
    handles = [plt.Line2D([], [], marker="o", ls="", color=c, markersize=6, label=f"{y - 1}/{y % 100:02d}")
               for y, c in zip(years, ramp)]
    ax.legend(handles=handles, title="reporting year (Dec-Nov)", fontsize=7, title_fontsize=7.5,
              loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=len(years))
    ax.grid(axis="y", alpha=0)
    xmin, xmax = ax.get_xlim()
    ax.set_xlim(xmin, xmax * 4)
    fig.tight_layout()
    _save(fig, path)


def fig_waymo(rates, path: Path):
    import numpy as np
    plt = _plt()
    d = rates[rates["area"].eq("all areas with published miles")]
    fig, ax = plt.subplots(figsize=(7.2, 2.4))
    y = np.arange(len(d))
    ax.errorbar(d["rate_per_million_miles"], y,
                xerr=[d["rate_per_million_miles"] - d["ci95_low"], d["ci95_high"] - d["rate_per_million_miles"]],
                fmt="o", color=CATEGORICAL[0], ecolor="#333333", capsize=3, markersize=6, lw=1.2)
    for yi, (_, r) in zip(y, d.iterrows()):
        ax.text(r["ci95_high"] * 1.08 + 0.01, yi, f"{r['rate_per_million_miles']:.3f}  (n = {r['crashes']})",
                va="center", fontsize=7.5)
    ax.set_yticks(y, d["outcome"])
    ax.invert_yaxis()
    ax.set_xlim(0, d["ci95_high"].max() * 1.55)
    ax.set_xlabel("crashes per million rider-only miles (95 % exact Poisson interval)")
    ax.grid(axis="y", alpha=0)
    fig.tight_layout()
    _save(fig, path)


# =========================================================================== markdown helpers
def _cell(v) -> str:
    import pandas as pd
    try:
        if pd.isna(v):
            return "—"
    except (TypeError, ValueError):
        pass
    return str(v).replace("|", "/")


def md_table(df, align: str | None = None) -> str:
    cols = list(df.columns)
    align = align or "l" + "r" * (len(cols) - 1)
    sep = ["---:" if a == "r" else "---" for a in align]
    lines = ["| " + " | ".join(map(str, cols)) + " |", "| " + " | ".join(sep) + " |"]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(_cell(v) for v in row) + " |")
    return "\n".join(lines)


def fmt_month(period) -> str:
    import pandas as pd
    if period is None or pd.isna(period):
        return "—"
    return pd.Period(str(period), "M").strftime("%b %Y")


def fmt_date(iso: str) -> str:
    import datetime as dt
    if not iso:
        return "unknown date"
    d = dt.date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%B %Y')}"


# =========================================================================== pipeline
def load_sgo(fetched: dict):
    import pandas as pd
    parts = []
    for key, (_, kind, source) in SGO_FILES.items():
        f = fetched[key]
        df = pd.read_csv(f.path, low_memory=False, encoding_errors="replace")
        parts.append(harmonise_sgo(df, kind, source))
    return pd.concat(parts, ignore_index=True)


def previous_index(cache: Path, data_dir: Path, current_release: str, explicit: Path | None):
    """Latest stored report index from a release before ``current_release`` (cache state, then committed)."""
    import pandas as pd
    if explicit and explicit.exists():
        return pd.read_csv(explicit, dtype={"report_id": str, "incident_id": str}), "the supplied index"
    candidates = []
    for p in (cache / "state").glob("sgo_index_*.csv"):
        candidates.append((p.stem.rsplit("_", 1)[-1], p))
    snap = data_dir / "snapshot.json"
    committed = data_dir / "sgo_report_index.csv"
    if snap.exists() and committed.exists():
        rel = json.loads(snap.read_text()).get("sources", {}).get("sgo_ads_current", {}).get("release", "")
        candidates.append((rel, committed))
    older = sorted((rel, p) for rel, p in candidates if rel and rel < current_release)
    if not older:
        return None, None
    rel, path = older[-1]
    return pd.read_csv(path, dtype={"report_id": str, "incident_id": str}), rel


def run(args) -> int:
    import pandas as pd

    cache = Path(args.cache or os.environ.get("AVSAFETY_CACHE", Path.home() / ".cache" / "avsafety")) / "observatory"
    out = Path(args.out)
    fig_dir, data_dir = out / "observatory", out / "observatory" / "data"
    page = out / "observatory.md"
    fetcher = Fetcher(cache, offline=args.offline)

    # ---- fetch
    fetched = {}
    for key, (url, _, source) in SGO_FILES.items():
        fetched[key] = fetcher.get(key, url, f"nhtsa/{source}/{Path(url).name}", expect="csv")
    if not all(fetched[k].ok for k in SGO_FILES):
        missing = ", ".join(f"{k} ({fetched[k].error or fetched[k].status})" for k in SGO_FILES if not fetched[k].ok)
        notice = (f"> **Refresh failed:** the NHTSA files could not be obtained ({missing}). "
                  "The figures and tables below are the last published snapshot.\n\n")
        if page.exists():
            text = re.sub(r"<!-- refresh-notice -->.*?<!-- /refresh-notice -->",
                          f"<!-- refresh-notice -->\n{notice}<!-- /refresh-notice -->", page.read_text(), flags=re.S)
            page.write_text(text)
        print(notice.strip(), file=sys.stderr)
        return 3

    release = release_date(fetched["sgo_ads_current"])
    max_year = args.max_year or int(release[:4])
    dmv = {}
    for year in range(DMV_FIRST_YEAR, max_year + 1):
        f = fetcher.get(f"dmv_{year}", DMV_FILE.format(year=year), f"cadmv/{year}-autonomous-mileage-reports.csv",
                        expect="csv")
        if f.ok:
            dmv[year] = f

    hub = fetcher.get_text(WAYMO_PAGE)
    names = dict(WAYMO_PINNED)
    if hub:
        for key, prefix in (("csv1", "CSV1"), ("csv2", "CSV2")):
            m = re.findall(rf"safety-impact-data/({prefix}%20-%20[^\"'<>]+?\.csv)", hub)
            if m:
                names[key] = urllib.parse.unquote(sorted(set(m))[-1])
    waymo = {}
    for key, name in names.items():
        f = fetcher.get(f"waymo_{key}", WAYMO_BUCKET + urllib.parse.quote(name), f"waymo/{name}", expect="")
        if not f.ok:  # fall back to the newest cached release
            cached = sorted((cache / "waymo").glob(f"{key.upper()} - *.csv"))
            if cached:
                f = Fetched(f.key, f.url, cached[-1], "cached-unreachable", fetcher._read_meta(cached[-1]), f.error)
        if f.ok:
            waymo[key] = f

    # ---- SGO
    raw = load_sgo(fetched)
    reports = latest_versions(raw)
    incidents = to_incidents(reports)
    last_sub = reports.loc[reports["source"].eq("current"), "submitted_month"].max()
    provisional_from = str(last_sub - 1)
    monthly = monthly_counts(reports, incidents)
    by_dim = {dim: monthly_by(incidents, dim) for dim in DIMENSIONS}
    conc = concentration(incidents[incidents["incident_month"] >= pd.Period(PLOT_START, "M")])
    ents = entity_table(incidents[incidents["incident_month"] >= pd.Period(PLOT_START, "M")])
    quality = data_quality(incidents)
    index = report_index(reports)

    prev, prev_release = previous_index(cache, data_dir, release, Path(args.previous) if args.previous else None)
    cur_idx = index.merge(reports[["kind", "report_id", "entity", "incident_month", "state", "road", "partner",
                                   "severity", "vru", "submitted_month"]], on=["kind", "report_id"], how="left")
    if prev is not None:
        diff = diff_reports(prev, cur_idx)
        new = diff[diff["new_report"]]
        diff_mode = (f"since the release of {fmt_date(prev_release)}" if prev_release[:1].isdigit()
                     else f"relative to {prev_release}")
    else:
        first = raw[raw["source"].eq("current")].groupby(["kind", "report_id"])["submitted_month"].min()
        recv = first[first.eq(last_sub)].index
        diff = cur_idx.assign(new_report=pd.MultiIndex.from_frame(cur_idx[["kind", "report_id"]]).isin(recv),
                              updated_report=False, new_incident=False)
        new = diff[diff["new_report"]]
        diff_mode = f"first submitted in {fmt_month(last_sub)} (no earlier snapshot was available for a diff)"

    # ---- write tables
    data_dir.mkdir(parents=True, exist_ok=True)
    monthly.to_csv(data_dir / "sgo_monthly_by_system.csv", index=False)
    pd.concat(by_dim.values(), ignore_index=True).to_csv(data_dir / "sgo_monthly_by_category.csv", index=False)
    conc.to_csv(data_dir / "sgo_concentration.csv", index=False)
    ents.to_csv(data_dir / "sgo_entities.csv", index=False)
    quality.to_csv(data_dir / "sgo_data_quality.csv", index=False)
    index.to_csv(data_dir / "sgo_report_index.csv", index=False)
    (cache / "state").mkdir(parents=True, exist_ok=True)
    index.to_csv(cache / "state" / f"sgo_index_{release}.csv", index=False)
    new_cols = ["kind", "report_id", "version", "entity", "incident_month", "state", "road", "partner", "severity"]
    new_out = new[new_cols].sort_values(["kind", "incident_month", "report_id"])
    new_out.to_csv(data_dir / "sgo_new_reports.csv", index=False)

    # ---- figures
    fig_monthly(monthly, provisional_from, fig_dir / "sgo_monthly.svg")
    for dim in DIMENSIONS:
        fig_composition(by_dim[dim], dim, provisional_from, fig_dir / f"sgo_{dim}.svg")

    # ---- DMV
    dmv_rates, dmv_checks, dmv_min_miles = None, 0, 0
    if dmv:
        veh = pd.concat([parse_dmv_mileage(f.path, y) for y, f in sorted(dmv.items())], ignore_index=True)
        dmv_checks = int(veh["mileage_check"].eq("monthly sum").sum())
        dmv_rates = disengagement_rates(veh)
        dmv_rates.to_csv(data_dir / "ca_disengagements.csv", index=False)
        latest_rates = dmv_rates[dmv_rates["report_year"].eq(dmv_rates["report_year"].max())]
        dmv_min_miles = 10_000 if (latest_rates["miles"] >= 10_000).any() else 0
        fig_disengagements(dmv_rates, fig_dir / "ca_disengagements.svg", dmv_min_miles)

    # ---- Waymo
    w_rates, w_excluded, w_match = None, 0, None
    if {"csv1", "csv2"} <= waymo.keys():
        csv1 = pd.read_csv(waymo["csv1"].path)
        csv2 = pd.read_csv(waymo["csv2"].path, dtype={"SGO Report ID": str})
        w_rates, w_excluded = waymo_rates(csv1, csv2)
        w_rates.to_csv(data_dir / "waymo_ro_rates.csv", index=False)
        fig_waymo(w_rates, fig_dir / "waymo_ro_rates.svg")
        end = pd.Period(str(int(csv2["Year Month"].max())), "M")
        wsgo = reports[reports["kind"].eq("ADS") & reports["entity"].str.startswith("Waymo")
                       & (reports["incident_month"] <= end)]
        w_match = {"sgo_reports": len(wsgo), "in_ro_list": int(wsgo["report_id"].isin(set(csv2["SGO Report ID"])).sum()),
                   "end": fmt_month(end), "first": fmt_month(str(int(csv2["Year Month"].min())))}

    # ---- snapshot
    sources = {}
    for key, f in list(fetched.items()) + [(f"dmv_{y}", f) for y, f in sorted(dmv.items())] + \
            [(f"waymo_{k}", f) for k, f in sorted(waymo.items())]:
        sources[key] = {"url": f.url, "status": f.status, "release": release_date(f), "accessed": access_date(f),
                        "sha256": file_sha256(f.path), "bytes": f.path.stat().st_size}
    ads = incidents[incidents["kind"].eq("ADS")]
    adas = incidents[incidents["kind"].eq("ADAS")]
    snapshot = {
        "nhtsa_release": release, "reports_received_through_month": str(last_sub),
        "provisional_from_month": provisional_from,
        "counts": {k: {"reports_latest_version": int(reports["kind"].eq(k).sum()),
                       "crashes": int(incidents["kind"].eq(k).sum()),
                       "crashes_third_amendment": int((incidents["kind"].eq(k)
                                                       & (incidents["incident_month"] >= pd.Period("2025-06", "M"))).sum())}
                   for k in ("ADS", "ADAS")},
        "new_reports": {k: int(new["kind"].eq(k).sum()) for k in ("ADS", "ADAS")},
        "updated_reports": {k: int((diff["updated_report"] & diff["kind"].eq(k)).sum()) for k in ("ADS", "ADAS")},
        "diff_basis": diff_mode,
        "dmv_years": sorted(dmv), "waymo_files": {k: f.path.name for k, f in sorted(waymo.items())},
        "sources": sources,
    }
    (data_dir / "snapshot.json").write_text(json.dumps(snapshot, indent=1, sort_keys=True) + "\n")

    # ---- page
    ctx = dict(release=release, last_sub=last_sub, provisional_from=provisional_from, monthly=monthly,
               incidents=incidents, reports=reports, raw=raw, conc=conc, ents=ents, quality=quality,
               new=new_out, diff=diff, diff_mode=diff_mode, prev=prev is not None, dmv=dmv, dmv_rates=dmv_rates,
               dmv_checks=dmv_checks, dmv_min_miles=dmv_min_miles, waymo=waymo, w_rates=w_rates, w_excluded=w_excluded, w_match=w_match,
               fetched=fetched, sources=sources, ads=ads, adas=adas, max_year=max_year)
    page.write_text(render_page(ctx))
    print(f"observatory: NHTSA release {release}; ADS {snapshot['counts']['ADS']['crashes']} crashes, "
          f"ADAS {snapshot['counts']['ADAS']['crashes']} crashes; DMV years {sorted(dmv)}; "
          f"Waymo files {len(waymo)}")
    return 0


# =========================================================================== page text
def _status_line(f: Fetched | dict) -> str:
    status = f["status"] if isinstance(f, dict) else f.status
    return {"fresh": "downloaded in this refresh", "not-modified": "checked in this refresh, unchanged",
            "cached-offline": "local copy (offline build)",
            "cached-unreachable": "**source unreachable in this refresh; local copy used**"}.get(status, status)


def render_page(c: dict) -> str:
    import pandas as pd
    P = pd.Period
    inc, rep = c["incidents"], c["reports"]
    third = inc["incident_month"] >= P("2025-06", "M")
    in_range = inc["incident_month"] >= P(PLOT_START, "M")
    n = {k: int((inc["kind"].eq(k) & in_range).sum()) for k in ("ADS", "ADAS")}
    nrep = {k: int((rep["kind"].eq(k) & (rep["incident_month"] >= P(PLOT_START, "M"))).sum()) for k in ("ADS", "ADAS")}
    early_adas = int((inc["kind"].eq("ADAS") & (inc["incident_month"] < P(PLOT_START, "M"))).sum())
    no_month = int(inc["incident_month"].isna().sum())
    multi = {k: int((inc["kind"].eq(k) & in_range & (inc["n_reports"] > 1)).sum()) for k in ("ADS", "ADAS")}
    m = c["monthly"]
    complete = m[(m["incident_month"] >= "2025-07") & (m["incident_month"] < c["provisional_from"])]
    rng = {k: (int(v.min()), int(v.max()), int(v.median())) if len(v) else None
           for k, v in ((k, complete[complete.kind.eq(k)]["crashes"]) for k in ("ADS", "ADAS"))}
    last_complete = fmt_month(P(c["provisional_from"], "M") - 1)
    acc = max((s["accessed"] for s in c["sources"].values()), default="")
    unreachable = [k for k, s in c["sources"].items() if s["status"] == "cached-unreachable"]

    L = []
    w = L.append
    w("---\ntitle: Field-safety statistics\nshort_title: Field-safety statistics\n"
      "description: Monthly view of NHTSA Standing General Order crash reports for ADS and Level 2 ADAS, "
      "California testing disengagements and published exposure, with the caveats needed to read them.\n---\n")
    w("<!-- refresh-notice -->")
    if unreachable:
        w(f"> **Partial refresh:** {', '.join(unreachable)} could not be reached; the local copy fetched earlier "
          "was used (see Sources for its date).\n")
    w("<!-- /refresh-notice -->\n")
    w(f"**NHTSA data release of {fmt_date(c['release'])}** (reports received through {fmt_month(c['last_sub'])}) · "
      f"page refreshed from sources accessed on {fmt_date(acc)} · rebuilt automatically every month.\n")
    w("What is happening on public roads with automated driving systems (ADS) and Level 2 driver assistance, as far "
      "as public records show it. The page is regenerated from the official files by "
      "[`scripts/observatory.py`](https://github.com/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/"
      "scripts/observatory.py); every number below is computed, and every table can be downloaded. For the method "
      "behind it, see [07-05 · Field safety monitoring](../07_Runtime_Assurance_and_Operations/"
      "05_field_safety_monitoring.ipynb).\n")

    w(":::{important} How to read this\n"
      "- **Reports are not crashes, and crashes are not rates.** A crash can produce several reports (several "
      "entities, several versions); here each report is counted once in its latest version and each crash once per "
      "`Same Incident ID`. Without exposure (miles, hours, where and when) no count says which system is safer.\n"
      "- **The reporting rules changed.** The thresholds differ between ADS and Level 2 ADAS and changed with the "
      "amended orders of May 2023 and June 2025 (dashed lines in every chart). Breaks at those dates are rule "
      "changes, not safety changes.\n"
      "- **Reports are allegations, not findings.** They are filed on notice, “regardless of whether the "
      "manufacturer has verified those facts”; fault is not part of the crash definition.\n"
      "- **Who reports reflects fleet size and data access.** Large fleets file more reports; Level 2 manufacturers "
      "with connected vehicles learn of more crashes. NHTSA: “Access to crash data may affect crash reporting.”\n"
      "- **Recent months are provisional.** Monthly reports arrive up to a month after notice and updates later "
      "still (grey bands).\n"
      "- **Exposure is public for almost no one.** Rates are computed only where an operator publishes matched "
      "exposure (one operator, below), and they are not comparable across operators or with an unmatched human "
      "baseline.\n:::\n")

    # ---- what changed
    w("## What changed in this release\n")
    nn = c["new"]
    dsum = c["diff"]
    para = (f"Reports {c['diff_mode']}: **{int(nn.kind.eq('ADS').sum())} ADS** and **{int(nn.kind.eq('ADAS').sum())} "
            f"Level 2 ADAS** reports")
    if c["prev"]:
        para += (f"; {int((dsum['updated_report'] & dsum.kind.eq('ADS')).sum())} ADS and "
                 f"{int((dsum['updated_report'] & dsum.kind.eq('ADAS')).sum())} Level 2 ADAS reports were updated "
                 f"to a new version; {int((dsum['new_incident'] & dsum['new_report']).sum())} new reports describe "
                 "crashes not reported before")
    para += "."
    if len(nn):
        old = nn[pd.PeriodIndex(nn["incident_month"].astype(str), freq="M") < c["last_sub"] - 2]
        if len(old):
            para += (f" {len(old)} of them describe crashes from {fmt_month(c['last_sub'] - 3)} or earlier: late "
                     "notice and late filing revise past months, which is why recent months are marked provisional.")
    w(para + "\n")
    if len(nn):
        sev = nn[nn["severity"].isin(["fatal", "serious"]) | nn["partner"].eq("pedestrian, cyclist or other VRU")]
        if len(sev):
            t = sev.assign(system=sev["kind"].map(KIND_LABEL), month=[fmt_month(x) for x in sev["incident_month"]],
                           state=sev["state"].fillna("—"))[["system", "entity", "month", "state", "road", "partner",
                                                             "severity"]]
            t = t.rename(columns={"entity": "reporting entity", "month": "incident month",
                                  "road": "roadway", "partner": "crash partner", "severity": "highest severity alleged"})
            w(f"\nNew reports alleging a fatal or serious injury or involving a vulnerable road user ({len(t)}):\n")
            w(md_table(t.head(40), "l" * 7))
            if len(t) > 40:
                w(f"\n… and {len(t) - 40} more in the download.")
        w(f"\n\nAll new reports: {{download}}`sgo_new_reports.csv <observatory/data/sgo_new_reports.csv>`.\n")
    else:
        w("\n")

    # ---- monthly
    w("## Reports and crashes per month\n")
    w(":::{figure} observatory/sgo_monthly.svg\n:alt: Monthly SGO crashes and reports for ADS and Level 2 ADAS with "
      "reporting-rule changes marked\n:width: 100%\n"
      f"Crashes (unique `Same Incident ID`) and reports per incident month, July 2021 to "
      f"{fmt_month(c['last_sub'])}. Dashed lines: amended orders in force. Grey band: provisional months.\n:::\n")
    w(f"Since July 2021 the files hold **{n['ADS']:,} ADS crashes** ({nrep['ADS']:,} reports) and "
      f"**{n['ADAS']:,} Level 2 ADAS crashes** ({nrep['ADAS']:,} reports); {multi['ADS']} ADS and {multi['ADAS']} "
      f"ADAS crashes were reported more than once."
      + (f" Under the third amended order, complete months from Jul 2025 to {last_complete} saw "
         f"{rng['ADS'][0]}–{rng['ADS'][1]} ADS crashes per month (median {rng['ADS'][2]}) and "
         f"{rng['ADAS'][0]}–{rng['ADAS'][1]} Level 2 ADAS crashes (median {rng['ADAS'][2]})."
         if rng["ADS"] and rng["ADAS"] else "")
      + " These are counts: the fleets and their mileage changed over the same period.\n")
    w("**Reporting rules on the time axis** (as of October 2026; sources: NHTSA SGO data dictionaries and the "
      "OMB supporting statement for control no. 2127-0754):\n")
    w(md_table(pd.DataFrame([
        ["29 Jun 2021", "Standing General Order 2021-01 issued; first amended in August 2021",
         "1-day reports (with 10-day updates) for the most severe crashes; other ADS crashes monthly; Level 2 ADAS: "
         "severe crashes only"],
        ["15 May 2023", "Second amended order in force (issued 5 Apr 2023)",
         "1-day reports for fatality, hospital transport or VRU; 5-day reports for air bag or tow-away "
         "(ADS and Level 2); other ADS crashes with any property damage monthly; new 5-day report type"],
        ["16 Jun 2025", "Third amended order in force (issued 24 Apr 2025)",
         "5-day reports for fatality, hospital transport, VRU strike or air-bag deployment, for ADS also tow-away; "
         "other ADS crashes monthly only if damage is expected to exceed USD 1,000, only the ADS vehicle was "
         "involved, or the ADS vehicle struck another vehicle or object; Level 2 tow-away-only crashes no longer "
         "reportable; no nil reports; duplicate reporting by several entities reduced"]],
        columns=["date", "change", "what must be reported"]), "lll"))
    w(f"\nThe current files cover reports received from 16 June 2025; earlier reports come from NHTSA's archive "
      f"files. {early_adas} Level 2 ADAS crashes with incident dates before July 2021 (reported late) and "
      f"{no_month} crash{'' if no_month == 1 else 'es'} without an incident month are not plotted.\n")

    # ---- composition
    w("## What the crashes look like\n")
    w("Quarterly crash counts by category (one representative report per crash: the one alleging the highest "
      "severity). Shares within a system type are more informative than levels; comparisons *between* ADS and "
      "Level 2 ADAS are distorted by their different thresholds — the Level 2 file holds only severe crashes, the "
      "ADS file almost all.\n")
    descr = {"partner": "Crash partner", "road": "Roadway type", "severity": "Highest injury severity alleged",
             "movement": "Pre-crash movement of the subject vehicle"}
    for dim, label in descr.items():
        w(f":::{{figure}} observatory/sgo_{dim}.svg\n:alt: {label} of SGO crashes per quarter, ADS and Level 2 ADAS\n"
          f":width: 100%\n{label}, crashes per quarter. Monthly values: "
          "{download}`sgo_monthly_by_category.csv <observatory/data/sgo_monthly_by_category.csv>`.\n:::\n")
    t3 = inc[third]
    def share(kind, col, val):
        d = t3[t3.kind.eq(kind)]
        return 100 * d[col].isin(val if isinstance(val, list) else [val]).mean()
    w(f"Under the third amended order, the ADS vehicle was stopped or parked in "
      f"{share('ADS', 'movement', 'stopped or parked'):.0f} % of ADS crashes, and "
      f"{share('ADS', 'road', ['street', 'intersection']):.0f} % happened on streets or at intersections; "
      f"{share('ADAS', 'road', 'highway or freeway'):.0f} % of Level 2 ADAS crashes were on highways or freeways and "
      f"{share('ADAS', 'road', 'unknown'):.0f} % have an unknown roadway type. A struck, stopped vehicle says nothing "
      "about fault on its own, and an unknown field is not a random gap: it is concentrated in some reporters.\n")

    # ---- entities
    w("## Who reports\n")
    conc = c["conc"]
    w("Concentration by reporting entity, per incident year. The share of the largest entity mostly reflects fleet "
      "size and data access, not safety; without exposure it supports no ranking. HHI is the "
      "Herfindahl–Hirschman index of reporting shares (10,000 = a single entity).\n")
    ct = conc.assign(system=conc["kind"].map(KIND_LABEL))[["system", "incident_year", "crashes", "entities",
                                                           "largest_entity", "largest_share_pct", "top3_share_pct",
                                                           "hhi"]]
    ct = ct.rename(columns={"incident_year": "year", "largest_entity": "largest reporter",
                            "largest_share_pct": "its share [%]", "top3_share_pct": "top 3 share [%]", "hhi": "HHI"})
    w(md_table(ct, "lrrrlrrr"))
    w(f"\nPer-entity counts by regime, listed alphabetically: "
      "{download}`sgo_entities.csv <observatory/data/sgo_entities.csv>`. Of the reporting entities, only one "
      "(Waymo) publishes exposure that is machine-readable and linked to its SGO report IDs (as of October 2026); "
      "that is used in the next section.\n")

    # ---- data quality
    w("## Data quality\n")
    q = c["quality"]
    qt = q.assign(system=q["kind"].map(KIND_LABEL))[["system", "regime", "crashes", "partner_unknown_pct",
                                                     "road_unknown_pct", "severity_unknown_pct",
                                                     "movement_unknown_pct", "narrative_redacted_pct",
                                                     "notice_via_telematics_pct", "multi_report_crashes_pct"]]
    qt.columns = ["system", "regime", "crashes", "partner unknown [%]", "roadway unknown [%]",
                  "severity unknown [%]", "movement unknown [%]", "narrative redacted [%]",
                  "notice via telematics [%]", "reported > once [%]"]
    w("Missing and redacted information per crash. Narratives are redacted where the reporting entity claims "
      "confidential business information (CBI). Unknown fields are concentrated in the Level 2 ADAS file: the "
      "manufacturer typically learns of the crash from vehicle telematics but, unlike an ADS operator with its own "
      "fleet data, often not its circumstances. For ADS the share of crashes reported more than "
      "once falls under the third amended order, which reduced duplicate reporting; for Level 2 ADAS it was low "
      "throughout.\n")
    w(md_table(qt, "llrrrrrrrr") + "\n")

    # ---- Waymo
    w("## Rates where exposure is public\n")
    wr = c["w_rates"]
    if wr is not None:
        wm = c["w_match"]
        allr = wr[wr["area"].str.startswith("all")]
        miles = allr["ro_miles_million"].iloc[0]
        w(f"Waymo publishes cumulative **rider-only (RO)** miles per county and the list of RO crashes with their SGO "
          f"report IDs on its Safety Impact Data Hub (files `{c['waymo']['csv1'].path.name}` and "
          f"`{c['waymo']['csv2'].path.name}`). Numerator and denominator are filtered by the same rule: RO operation, "
          f"the counties with published miles, {wm['first']} to {wm['end']}, {miles:.1f} million RO miles. "
          f"{c['w_excluded']} RO crashes in counties without a published mileage figure are excluded. "
          f"Of {wm['sgo_reports']:,} Waymo ADS reports in the SGO files with incident months up to {wm['end']}, "
          f"{wm['in_ro_list']:,} are in the RO crash list — the rest include supervised testing and areas outside "
          "RO service, which is why all SGO reports must not be divided by RO miles.\n")
        w(":::{figure} observatory/waymo_ro_rates.svg\n:alt: Waymo rider-only crash rates per million miles with "
          "95 percent exact Poisson intervals\n:width: 100%\n"
          "Waymo rider-only crash rates, all areas with published miles, with exact (Garwood) 95 % intervals.\n:::\n")
        tt = allr[["outcome", "crashes", "rate_per_million_miles", "ci95_low", "ci95_high"]].copy()
        tt.columns = ["outcome", "crashes", "per million RO miles", "95 % CI low", "95 % CI high"]
        w(md_table(tt, "lrrrr"))
        w("\n\nPer-area values: {download}`waymo_ro_rates.csv <observatory/data/waymo_ro_rates.csv>`. "
          "**Comparison caveats.** These rates describe one operator's driverless ride-hailing service in specific "
          "cities, roads and times (its ODD). They are not comparable with other operators' SGO counts (no matched "
          "exposure), with Level 2 ADAS (different reporting threshold, human driver responsible), or with a human "
          "baseline unless that baseline is matched by area, road type, outcome definition and under-reporting. "
          "Waymo's own matched human benchmarks and their methodology are on the "
          f"[Data Hub]({WAYMO_PAGE}); they are linked, not reproduced, here. An \"any crash\" rate is not shown: "
          "since June 2025 the ADS reporting threshold depends on damage and crash type, which Waymo's release "
          "notes describe as making that outcome impossible to compare with human benchmarks. Intervals capture "
          "random error only; at hundreds of millions of miles the systematic choices (which crashes count, which "
          "baseline) dominate.\n")
    else:
        w(f"The Waymo Safety Impact Data Hub files could not be obtained in this build; see [the Data Hub]"
          f"({WAYMO_PAGE}).\n")

    # ---- DMV
    w("## California testing: disengagements per 1,000 miles\n")
    dr = c["dmv_rates"]
    if dr is not None:
        years = sorted(c["dmv"])
        latest = years[-1]
        tot = dr.groupby("report_year")[["miles", "disengagements"]].sum()
        w(f"California requires holders of a testing permit to report each year (1 December to 30 November) the "
          f"autonomous miles driven and every disengagement — the safety driver taking control because of a "
          f"technology failure or a safety concern. Shown: drivered testing, reporting years "
          f"{years[0] - 1}/{years[0] % 100:02d} to {latest - 1}/{latest % 100:02d}; manufacturers with at least "
          f"{c['dmv_min_miles']:,} autonomous miles in the latest year, all years in which they reached that "
          f"mileage.\n")
        w(":::{figure} observatory/ca_disengagements.svg\n:alt: Disengagements per 1,000 autonomous miles by "
          "manufacturer and reporting year, California DMV\n:width: 100%\n"
          f"Disengagements per 1,000 autonomous test miles (log scale); label: miles in {latest - 1}/{latest % 100:02d}."
          "\n:::\n")
        tt = tot.reset_index().assign(
            year=lambda d: d["report_year"].map(lambda y: f"Dec {y - 1} – Nov {y}"),
            per_1000=lambda d: (1000 * d["disengagements"] / d["miles"]).round(3))
        tt["disengagements"] = tt["disengagements"].map("{:,}".format)
        tt = tt[["year", "miles", "disengagements", "per_1000"]].rename(
            columns={"miles": "autonomous miles (all permit holders)", "per_1000": "pooled per 1,000 miles"})
        tt["autonomous miles (all permit holders)"] = tt["autonomous miles (all permit holders)"].map("{:,.0f}".format)
        w(md_table(tt, "lrrr"))
        w(f"\n\nAll manufacturers and years: {{download}}`ca_disengagements.csv <observatory/data/ca_disengagements.csv>`"
          f" ({c['dmv_checks']} vehicle rows whose annual total disagreed with the monthly cells were summed from "
          "the months).\n")
        w("**Caveats.** The DMV states that the reports “are not designed for comparative analysis across companies”. "
          "Each company decides what counts as a disengagement and tests where and how it chooses (routes, "
          "difficulty, driver instructions), so a low rate can mean easy miles or a narrow definition. Driverless "
          "testing is reported separately and deployment operations not at all, so a company's main service can be "
          "absent. Disengagements cluster in time and place, so a Poisson interval would understate the uncertainty; "
          "none is shown. ")
        if latest + 1 < c["max_year"]:
            news = f" (announced on 20 February 2026, [news release]({DMV_NEWS_2025}))" if latest + 1 == 2025 else ""
            w(f"The report for December {latest} to November {latest + 1}{news} was not available as a CSV file at "
              f"the usual address when this page was built; it is added automatically once published there. ")
        w(f"New California regulations adopted on 28 April 2026 replace disengagement reporting with other metrics "
          f"(system failures, immobilisations, hard-braking events, miles, SGO-aligned crash reports; "
          f"[DMV]({DMV_NEW_REGS})), so this series will end.\n")
    else:
        w("The California DMV files could not be obtained in this build.\n")
    w(f"California's collision reports (form OL 316) are published as individual PDF forms, now through UC "
      f"Berkeley's [TIMS AV collision tool]({DMV_COLLISIONS}); they are not used here because no machine-readable "
      "export with stable terms was found, and they overlap with the SGO reports.\n")

    # ---- human baselines
    w("## Why there is no human baseline here\n")
    w("A human baseline must match the numerator: the same outcome definition, area, road types, vehicle types and "
      "reporting completeness. FARS is a census of fatal crashes only, too few to compare with the outcomes above; "
      "CRSS is a national sample of police-reported crashes without the county- and road-level exposure that "
      "robotaxi or Level 2 operating domains require. Building matched baselines correctly (police-report "
      "under-reporting, vehicle miles by county and road type) is a research project in its own right — see "
      "Scanlon et al. (2024) and Kusano et al. (2024, 2025), whose benchmarks Waymo publishes on its Data Hub. "
      "A quick national average would mislead, so none is shown.\n")

    # ---- downloads
    w("## Downloads\n")
    files = [("sgo_monthly_by_system.csv", "reports and crashes per incident month and system type, with regime"),
             ("sgo_monthly_by_category.csv", "crashes per month by crash partner, roadway, severity and movement"),
             ("sgo_concentration.csv", "concentration by reporting entity per year"),
             ("sgo_entities.csv", "crashes per reporting entity and regime (alphabetical)"),
             ("sgo_data_quality.csv", "unknown and redacted fields per system type and regime"),
             ("sgo_new_reports.csv", "reports new in this release"),
             ("sgo_report_index.csv", "report IDs and versions of this release (basis of the next diff)")]
    if dr is not None:
        files.append(("ca_disengagements.csv", "California miles and disengagements per manufacturer and year"))
    if wr is not None:
        files.append(("waymo_ro_rates.csv", "Waymo rider-only rates with exact Poisson intervals"))
    files.append(("snapshot.json", "release dates, access dates, file hashes and headline counts"))
    for name, d in files:
        w(f"- {{download}}`{name} <observatory/data/{name}>` — {d}")
    w("")

    # ---- sources
    s = c["sources"]
    w("## Sources and method\n")
    w(f"- **NHTSA, Standing General Order 2021-01 incident reports**, ADS and Level 2 ADAS CSV files, current "
      f"(release of {fmt_date(s['sgo_ads_current']['release'])}) and archive 2021–2025 (release of "
      f"{fmt_date(s['sgo_ads_archive']['release'])}). <{NHTSA_BASE}> · overview: <{NHTSA_PAGE}>. Public US "
      f"government data. Accessed {fmt_date(s['sgo_ads_current']['accessed'])} — "
      f"{_status_line(s['sgo_ads_current'])}.")
    w(f"- NHTSA, *Standing General Order 2021-01 Data Dictionary* (current: <{SGO_DICTIONARY}>; archive, with the "
      f"change log of the earlier orders: <{SGO_DICTIONARY_ARCHIVE}>). Source of the caveats quoted above.")
    w(f"- NHTSA, *Information Collection Request Supporting Statement, Part A: Incident Reporting for ADS and "
      f"Level 2 ADAS*, OMB control no. 2127-0754 (2026), <{SGO_ICR}>. Source of the reporting criteria of the "
      f"third amended order.")
    if c["dmv"]:
        y0, y1 = min(c["dmv"]), max(c["dmv"])
        dm = s[f"dmv_{y1}"]
        w(f"- **California DMV, Autonomous Vehicle Mileage Reports** (drivered testing), reporting years "
          f"{y0} to {y1}, e.g. <{DMV_FILE.format(year=y1)}>. Information on the DMV website is public domain "
          f"unless otherwise indicated (<{DMV_CONDITIONS}>). Accessed {fmt_date(dm['accessed'])} — "
          f"{_status_line(dm)}.")
    if c["waymo"]:
        wf = s.get("waymo_csv2", {})
        w(f"- **Waymo, Safety Impact Data Hub**, <{WAYMO_PAGE}>, CSV1 (RO miles per location) and CSV2 (crashes with "
          f"SGO ID). Waymo provides the files “to help researchers reproduce the results or conduct their own "
          f"research” (release notes); the files are not redistributed here, only derived counts and rates. "
          f"Accessed {fmt_date(wf.get('accessed', ''))} — {_status_line(wf) if wf else ''}.")
    w("- Kusano, K. D., et al. (2024). Comparison of Waymo rider-only crash data to human benchmarks at 7.1 million "
      "miles. *Traffic Injury Prevention*, 25(sup1). <https://doi.org/10.1080/15389588.2024.2380786>")
    w("- Kusano, K. D., et al. (2025). Comparison of Waymo rider-only crash rates by crash type to human benchmarks "
      "at 56.7 million miles. *Traffic Injury Prevention*, 26(sup1). <https://doi.org/10.1080/15389588.2025.2499887>")
    w("- Scanlon, J. M., et al. (2024). Benchmarks for retrospective automated driving system crash rate analysis "
      "using police-reported crash data. *Traffic Injury Prevention*, 25(sup1). "
      "<https://doi.org/10.1080/15389588.2024.2380522>\n")
    w("**Method.** Reports from the archive and current files are pooled; each `Report ID` keeps its latest version "
      "(the current file wins a tie). Crashes are unique `Same Incident ID`s within a system type; the "
      "representative report is the one alleging the highest severity. Categories merge the archive and current "
      "vocabularies (e.g. “Minor” and “Minor W/O Hospitalization” → minor). The regime of a crash is assigned by "
      "incident month, so May 2023 and June 2025 straddle two regimes. Months from "
      f"{fmt_month(c['provisional_from'])} are provisional. The diff compares report IDs and versions with the "
      "stored index of the previous release. Rate intervals are exact (Garwood) Poisson intervals from "
      "`avsafety.validation.poisson_rate_interval`. File hashes are in `snapshot.json`.\n")
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--offline", action="store_true", help="use cached files only")
    ap.add_argument("--cache", help="cache root (default: $AVSAFETY_CACHE or ~/.cache/avsafety)")
    ap.add_argument("--out", default=str(ROOT / "site"), help="site directory (default: site/)")
    ap.add_argument("--previous", help="report index of an earlier release to diff against")
    ap.add_argument("--max-year", type=int, default=None,
                    help="last DMV reporting year to look for (default: year of the NHTSA release)")
    return run(ap.parse_args(argv))


if __name__ == "__main__":
    sys.exit(main())
