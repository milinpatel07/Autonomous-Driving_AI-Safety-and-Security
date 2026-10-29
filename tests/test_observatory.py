"""Offline tests for scripts/observatory.py on tiny fixtures that follow the real file schemas."""
import importlib.util
import json
import sys
from pathlib import Path

import pytest

pd = pytest.importorskip("pandas")
pytest.importorskip("matplotlib")
pytest.importorskip("scipy")

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("observatory", ROOT / "scripts" / "observatory.py")
O = importlib.util.module_from_spec(_spec)
sys.modules["observatory"] = O          # dataclasses resolve annotations through sys.modules
_spec.loader.exec_module(O)

# Columns read from the NHTSA SGO CSVs (names as in the archive and current files).
SGO_COLUMNS = ["Report ID", "Report Version", "Reporting Entity", "Report Type", "Report Submission Date",
               "Same Incident ID", "Incident Date", "State", "Crash With", "Roadway Type",
               "Highest Injury Severity Alleged", "SV Pre-Crash Movement", "Source - Telematics",
               "Narrative - CBI?", "Narrative"]


def sgo_frame(rows):
    return pd.DataFrame(rows, columns=SGO_COLUMNS)


ADS_ARCHIVE = [  # archive vocabulary ('Minor', 'No Injuries Reported')
    ["30270-1", 1, "Waymo LLC", "Monthly", "AUG-2023", "inc-a", "JUL-2023", "CA", "SUV", "Street",
     "No Injuries Reported", "Stopped", "Y", " ", "text"],
    ["30270-1", 2, "Waymo LLC", "Update", "SEP-2023", "inc-a", "JUL-2023", "CA", "SUV", "Street",
     "Minor", "Stopped", "Y", " ", "text"],
    ["777-1", 1, "Transdev Alternative Services", "1-Day", "AUG-2023", "inc-a", "JUL-2023", "CA", "SUV",
     "Street", "No Injuries Reported", "Stopped", " ", "Y",
     "[REDACTED, MAY CONTAIN CONFIDENTIAL BUSINESS INFORMATION]"],
    ["30270-2", 1, "Waymo LLC", "1-Day", "NOV-2024", "inc-b", "OCT-2024", "AZ", "Non-Motorist: Cyclist",
     "Intersection", "Moderate", "Making Right Turn", "Y", " ", "text"],
]
ADS_CURRENT = [  # current vocabulary ('Minor W/O Hospitalization')
    ["30270-9", 1, "Waymo LLC", "Monthly", "AUG-2025", "inc-c", "JUL-2025", "CA", "Passenger Car", "Street",
     "Property Damage. No Injured Reported", "Proceeding Straight", "Y", " ", "text"],
    ["40000-1", 1, "Zoox, Inc.", "5-Day", "SEP-2025", "inc-d", "SEP-2025", "NV", "Heavy Truck", "Intersection",
     "Minor W/ Hospitalization", "Making Left Turn", "Y", " ", "text"],
]
ADAS_ARCHIVE = [
    ["13781-1", 1, "Tesla, Inc.", "1-Day", "MAR-2024", "inc-x", "MAR-2024", "", "Unknown", "Unknown",
     "Unknown", "Unknown", "Y", "Y", "[REDACTED, MAY CONTAIN CONFIDENTIAL BUSINESS INFORMATION]"],
    ["13781-2", 1, "Tesla, Inc.", "5-Day", "MAY-2025", "inc-y", "MAY-2025", "", "Pole / Tree",
     "Highway / Freeway", "Fatality", "Lane / Road Departure", "Y", " ", "text"],
    ["13781-3", 1, "Tesla, Inc.", "No New or Updated Incident Reports", "JUN-2025", "", "", "", "", "", "",
     "", " ", " ", ""],
]
ADAS_CURRENT = [
    ["13781-2", 2, "Tesla, Inc.", "Update", "JUL-2025", "inc-y", "MAY-2025", "TX", "Pole / Tree",
     "Highway / Freeway", "Fatality", "Lane / Road Departure", "Y", " ", "text"],
    ["502-5", 1, "General Motors, LLC", "5-Day", "AUG-2025", "inc-z", "AUG-2025", "MI", "SUV",
     "Highway / Freeway", "Serious W/ Hospitalization", "Changing Lanes", "Y", " ", "text"],
]


def pooled():
    parts = [O.harmonise_sgo(sgo_frame(ADS_ARCHIVE), "ADS", "archive"),
             O.harmonise_sgo(sgo_frame(ADS_CURRENT), "ADS", "current"),
             O.harmonise_sgo(sgo_frame(ADAS_ARCHIVE), "ADAS", "archive"),
             O.harmonise_sgo(sgo_frame(ADAS_CURRENT), "ADAS", "current")]
    return pd.concat(parts, ignore_index=True)


# --------------------------------------------------------------------------- category maps
@pytest.mark.parametrize("raw, group", [
    ("Minor", "minor"), ("Minor W/O Hospitalization", "minor"), ("Serious W/ Hospitalization", "serious"),
    ("Fatality", "fatal"), ("No Injuries Reported", "no injury reported"),
    ("Property Damage. No Injured Reported", "no injury reported"), ("Unknown", "unknown"), (None, "unknown")])
def test_severity_vocabularies_merge(raw, group):
    assert O.severity_group(raw) == group


def test_other_category_maps():
    assert O.partner_group("Non-Motorist: Scooter - Skateboard") == "pedestrian, cyclist or other VRU"
    assert O.partner_group("SUV") == "passenger vehicle" and O.partner_group("Bus") == "heavy truck or bus"
    assert O.partner_group(float("nan")) == "unknown" and O.partner_group("Animal") == "other"
    assert O.road_group("Parking Garage") == "parking area" and O.road_group("Traffic Circle") == "other"
    assert O.movement_group("Parked") == "stopped or parked" and O.movement_group("Making U-Turn") == "turning"
    assert O.movement_group("Parking Maneuver") == "backing or parking"
    assert O.short_entity("Waymo LLC") == "Waymo" and O.short_entity("Zoox, Inc.") == "Zoox"


def test_regime_boundaries():
    assert O.regime_of(pd.Period("2023-04", "M")) == "original / 1st amended order"
    assert O.regime_of(pd.Period("2023-05", "M")) == "2nd amended order"
    assert O.regime_of(pd.Period("2025-06", "M")) == "3rd amended order"
    assert O.regime_of(pd.Period("2020-01", "M")) == "before SGO reporting"


# --------------------------------------------------------------------------- versions and incidents
def test_nil_reports_dropped_and_latest_version_kept():
    raw = pooled()
    assert "13781-3" not in set(raw["report_id"])                    # "No New or Updated Incident Reports"
    rep = O.latest_versions(raw)
    assert rep["report_id"].is_unique
    r1 = rep.set_index("report_id").loc["30270-1"]
    assert r1["version"] == 2 and r1["severity"] == "minor"
    r2 = rep.set_index("report_id").loc["13781-2"]
    assert r2["version"] == 2 and r2["source"] == "current" and r2["state"] == "TX"


def test_current_file_wins_a_version_tie():
    a = O.harmonise_sgo(sgo_frame([ADAS_CURRENT[1]]), "ADAS", "archive").assign(state="OLD")
    c = O.harmonise_sgo(sgo_frame([ADAS_CURRENT[1]]), "ADAS", "current")
    rep = O.latest_versions(pd.concat([c, a], ignore_index=True))
    assert len(rep) == 1 and rep["source"].iloc[0] == "current"


def test_incidents_dedup_and_representative_is_most_severe():
    inc = O.to_incidents(O.latest_versions(pooled()))
    a = inc[inc["incident_id"].eq("inc-a")]
    assert len(a) == 1
    assert a["n_reports"].iloc[0] == 2 and a["n_entities"].iloc[0] == 2
    assert a["severity"].iloc[0] == "minor" and a["report_id"].iloc[0] == "30270-1"
    assert len(inc[inc["kind"].eq("ADS")]) == 4 and len(inc[inc["kind"].eq("ADAS")]) == 3
    assert bool(inc.set_index("incident_id").loc["inc-x", "narrative_cbi"])


def test_monthly_counts_zero_filled_and_regime():
    rep = O.latest_versions(pooled())
    m = O.monthly_counts(rep, O.to_incidents(rep))
    ads = m[m["kind"].eq("ADS")].set_index("incident_month")
    assert ads.index[0] == "2021-07" and ads.loc["2021-07", "crashes"] == 0
    assert ads.loc["2023-07", "reports"] == 2 and ads.loc["2023-07", "crashes"] == 1
    assert ads.loc["2025-07", "regime"] == "3rd amended order"


def test_monthly_by_category_and_concentration():
    inc = O.to_incidents(O.latest_versions(pooled()))
    t = O.monthly_by(inc, "partner")
    assert set(t.columns) == {"kind", "incident_month", "dimension", "category", "crashes"}
    assert t["crashes"].sum() == len(inc[inc["incident_month"] >= pd.Period("2021-07", "M")])
    c = O.concentration(inc)
    row = c[(c["kind"].eq("ADS")) & (c["incident_year"].eq(2025))].iloc[0]
    assert row["entities"] == 2 and row["largest_share_pct"] == 50.0 and row["hhi"] == 5000


def test_entity_table_is_alphabetical_and_pools_small_entities():
    inc = O.to_incidents(O.latest_versions(pooled()))
    t = O.entity_table(inc, min_crashes=2)
    ads = t[t["kind"].eq("ADS")]["entity"].tolist()
    assert ads[0] == "Waymo" and ads[-1].startswith("1 other entities")
    assert t["total"].sum() == len(inc)


def test_data_quality_shares():
    q = O.data_quality(O.to_incidents(O.latest_versions(pooled())))
    row = q[(q["kind"].eq("ADAS")) & (q["regime"].eq("2nd amended order"))].iloc[0]
    assert row["crashes"] == 2 and row["partner_unknown_pct"] == 50.0 and row["narrative_redacted_pct"] == 50.0


def test_diff_new_updated_and_new_incident():
    rep = O.latest_versions(pooled())
    current = O.report_index(rep)
    previous = current[current["report_id"].ne("40000-1")].copy()
    previous.loc[previous["report_id"].eq("13781-2"), "version"] = 1
    d = O.diff_reports(previous, current).set_index("report_id")
    assert bool(d.loc["40000-1", "new_report"]) and bool(d.loc["40000-1", "new_incident"])
    assert bool(d.loc["13781-2", "updated_report"]) and not bool(d.loc["13781-2", "new_report"])
    assert not d.loc["30270-9", ["new_report", "updated_report"]].any()


# --------------------------------------------------------------------------- rates
def test_garwood_matches_known_values():
    lo, hi = O.garwood(0, 1.0)
    assert lo == 0 and hi == pytest.approx(3.6889, abs=1e-4)
    lo, hi = O.garwood(10, 2.0)
    assert lo == pytest.approx(4.7954 / 2, abs=1e-3) and hi == pytest.approx(18.3904 / 2, abs=1e-3)


def test_waymo_rates_match_numerator_and_denominator():
    csv1 = pd.DataFrame({"County Name": ["Maricopa", "San Francisco", "All Locations (mileage blended)"],
                         "Waymo RO Miles (Millions)": [10.0, 5.0, 15.0]})
    flags = {c: [False] * 4 for c in O.WAYMO_OUTCOMES.values()}
    flags["Is Any-Injury-Reported"] = [True, True, False, True]
    csv2 = pd.DataFrame({"SGO Report ID": ["1", "2", "3", "4"],
                         "County": ["Maricopa", "San Francisco", "Maricopa", "Miami-Dade"], **flags})
    rates, excluded = O.waymo_rates(csv1, csv2)
    assert excluded == 1
    allr = rates[(rates["area"].str.startswith("all")) & rates["outcome"].eq("any-injury-reported crash")].iloc[0]
    assert allr["crashes"] == 2 and allr["ro_miles_million"] == 15.0
    assert allr["rate_per_million_miles"] == pytest.approx(2 / 15, abs=1e-4)
    assert allr["ci95_low"] < allr["rate_per_million_miles"] < allr["ci95_high"]


# --------------------------------------------------------------------------- California DMV
DMV_CSV = (
    "Manufacturer,Permit Number,VIN NUMBER,Annual Total of Disengagements,DEC 2023,JAN 2024,FEB 2024,"
    "ANNUAL TOTAL,,\n"
    "Waymo LLC,AVT003,VIN1,2,\"1,000.50\",500,0,\"1,500.50\",,\n"
    "WAYMO LLC,AVT003,VIN2,1,830 .04,0,0,830.04,,\n"
    "Weride Corp,AVT050,VIN3,0,100,100,\xa0100,999,,\n"        # annual total disagrees: monthly sum used
    ",,,,,,,,,\n"
)


def test_parse_dmv_mileage_and_rates(tmp_path):
    f = tmp_path / "dmv.csv"
    f.write_bytes(DMV_CSV.encode("cp1252"))
    v = O.parse_dmv_mileage(f, 2024)
    assert len(v) == 3 and set(v["manufacturer"]) == {"Waymo", "WeRide"}
    assert v.loc[v["vin"].eq("VIN3"), "miles"].iloc[0] == 300
    assert v["mileage_check"].tolist() == ["annual total", "annual total", "monthly sum"]
    r = O.disengagement_rates(v).set_index("manufacturer")
    assert r.loc["Waymo", "disengagements"] == 3 and r.loc["Waymo", "miles"] == 2331
    assert r.loc["Waymo", "per_1000_miles"] == pytest.approx(1000 * 3 / 2330.54, abs=1e-3)


def test_to_number_and_names():
    assert O.to_number("1,049.54") == pytest.approx(1049.54)
    assert O.to_number("830 .04") == pytest.approx(830.04)
    assert O.to_number("") == 0 and O.to_number(None) == 0
    assert O.canonical_manufacturer("NISSAN NORTH AMERICA, INC DBA ALLIANCE INNOVATION LAB") == "Nissan"
    assert O.canonical_manufacturer("Woven by Toyota, U.S., Inc.") == "Woven by Toyota"


# --------------------------------------------------------------------------- end to end (offline)
def _write(path: Path, text: str, release: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    meta = {"fetched": "2026-10-29", "last_modified": release, "etag": "", "sha256": "", "bytes": len(text)}
    path.with_name(path.name + ".meta.json").write_text(json.dumps(meta))


def _cache(root: Path, ads_current, release="Thu, 15 Oct 2026 12:30:03 GMT"):
    obs = root / "observatory"
    _write(obs / "nhtsa/archive/SGO-2021-01_Incident_Reports_ADS.csv", sgo_frame(ADS_ARCHIVE).to_csv(index=False),
           "Thu, 26 Mar 2026 20:12:34 GMT")
    _write(obs / "nhtsa/archive/SGO-2021-01_Incident_Reports_ADAS.csv",
           sgo_frame(ADAS_ARCHIVE).to_csv(index=False), "Thu, 26 Mar 2026 20:12:33 GMT")
    _write(obs / "nhtsa/current/SGO-2021-01_Incident_Reports_ADS.csv", sgo_frame(ads_current).to_csv(index=False),
           release)
    _write(obs / "nhtsa/current/SGO-2021-01_Incident_Reports_ADAS.csv",
           sgo_frame(ADAS_CURRENT).to_csv(index=False), release)
    (obs / "cadmv").mkdir(parents=True, exist_ok=True)
    (obs / "cadmv/2024-autonomous-mileage-reports.csv").write_bytes(DMV_CSV.encode("cp1252"))
    flags = {c: ["True", "False"] for c in O.WAYMO_OUTCOMES.values()}
    _write(obs / "waymo" / O.WAYMO_PINNED["csv1"], "County Name,Waymo RO Miles (Millions)\nMaricopa,10.0\n",
           release)
    _write(obs / "waymo" / O.WAYMO_PINNED["csv2"],
           pd.DataFrame({"SGO Report ID": ["30270-2", "30270-9"], "Year Month": [202410, 202507],
                         "County": ["Maricopa", "Maricopa"], **flags}).to_csv(index=False), release)


def test_end_to_end_offline_render_and_diff(tmp_path):
    cache, site = tmp_path / "cache", tmp_path / "site"
    _cache(cache, ADS_CURRENT)
    assert O.main(["--offline", "--cache", str(cache), "--out", str(site), "--max-year", "2024"]) == 0
    page = (site / "observatory.md").read_text()
    for needle in ("How to read this", "Reports are not crashes", "third amended order", "Garwood",
                   "{download}`sgo_monthly_by_system.csv", "Dec 2023 – Nov 2024", "no earlier snapshot"):
        assert needle in page
    assert "generated by" not in page.lower()
    for name in ("sgo_monthly", "sgo_partner", "sgo_road", "sgo_severity", "sgo_movement",
                 "ca_disengagements", "waymo_ro_rates"):
        svg = (site / "observatory" / f"{name}.svg").read_text()
        assert svg.startswith("<?xml") and "<dc:date>" not in svg
    snap = json.loads((site / "observatory/data/snapshot.json").read_text())
    assert snap["nhtsa_release"] == "2026-10-15" and snap["counts"]["ADS"]["crashes"] == 4

    # determinism: same inputs -> identical outputs
    first = {p.name: p.read_bytes() for p in (site / "observatory").rglob("*") if p.is_file()}
    assert O.main(["--offline", "--cache", str(cache), "--out", str(site), "--max-year", "2024"]) == 0
    assert first == {p.name: p.read_bytes() for p in (site / "observatory").rglob("*") if p.is_file()}

    # next release: one new report and one update -> diff against the stored index
    nxt = ADS_CURRENT + [["40000-2", 1, "Zoox, Inc.", "5-Day", "OCT-2025", "inc-e", "OCT-2025", "NV",
                          "Non-Motorist: Pedestrian", "Street", "Fatality", "Proceeding Straight", "Y", " ", "t"]]
    nxt[0] = nxt[0][:1] + [2] + nxt[0][2:]
    _cache(cache, nxt, release="Sun, 15 Nov 2026 12:30:03 GMT")
    assert O.main(["--offline", "--cache", str(cache), "--out", str(site), "--max-year", "2024"]) == 0
    page = (site / "observatory.md").read_text()
    assert "since the release of 15 October 2026" in page and "**1 ADS**" in page
    assert "1 ADS and 0 Level 2 ADAS reports were updated" in page
    new = pd.read_csv(site / "observatory/data/sgo_new_reports.csv")
    assert new["report_id"].tolist() == ["40000-2"]


def test_missing_nhtsa_data_leaves_page_with_notice(tmp_path):
    site = tmp_path / "site"
    site.mkdir()
    (site / "observatory.md").write_text("x\n<!-- refresh-notice -->\n<!-- /refresh-notice -->\ny\n")
    assert O.main(["--offline", "--cache", str(tmp_path / "empty"), "--out", str(site)]) == 3
    text = (site / "observatory.md").read_text()
    assert "Refresh failed" in text and text.startswith("x\n") and text.endswith("y\n")
