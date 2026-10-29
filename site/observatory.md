---
title: Field-safety statistics
short_title: Field-safety statistics
description: Monthly view of NHTSA Standing General Order crash reports for ADS and Level 2 ADAS, California testing disengagements and published exposure, with the caveats needed to read them.
---

<!-- refresh-notice -->
<!-- /refresh-notice -->

**NHTSA data release of 15 October 2026** (reports received through Sep 2026) · page refreshed from sources accessed on 29 October 2026 · rebuilt automatically every month.

What is happening on public roads with automated driving systems (ADS) and Level 2 driver assistance, as far as public records show it. The page is regenerated from the official files by [`scripts/observatory.py`](https://github.com/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/scripts/observatory.py); every number below is computed, and every table can be downloaded. For the method behind it, see [07-05 · Field safety monitoring](../07_Runtime_Assurance_and_Operations/05_field_safety_monitoring.ipynb).

:::{important} How to read this
- **Reports are not crashes, and crashes are not rates.** A crash can produce several reports (several entities, several versions); here each report is counted once in its latest version and each crash once per `Same Incident ID`. Without exposure (miles, hours, where and when) no count says which system is safer.
- **The reporting rules changed.** The thresholds differ between ADS and Level 2 ADAS and changed with the amended orders of May 2023 and June 2025 (dashed lines in every chart). Breaks at those dates are rule changes, not safety changes.
- **Reports are allegations, not findings.** They are filed on notice, “regardless of whether the manufacturer has verified those facts”; fault is not part of the crash definition.
- **Who reports reflects fleet size and data access.** Large fleets file more reports; Level 2 manufacturers with connected vehicles learn of more crashes. NHTSA: “Access to crash data may affect crash reporting.”
- **Recent months are provisional.** Monthly reports arrive up to a month after notice and updates later still (grey bands).
- **Exposure is public for almost no one.** Rates are computed only where an operator publishes matched exposure (one operator, below), and they are not comparable across operators or with an unmatched human baseline.
:::

## What changed in this release

Reports first submitted in Sep 2026 (no earlier snapshot was available for a diff): **74 ADS** and **144 Level 2 ADAS** reports.


New reports alleging a fatal or serious injury or involving a vulnerable road user (4):

| system | reporting entity | incident month | state | roadway | crash partner | highest severity alleged |
| --- | --- | --- | --- | --- | --- | --- |
| Level 2 ADAS | Tesla | Aug 2026 | NY | unknown | unknown | serious |
| Level 2 ADAS | Tesla | Aug 2026 | TX | intersection | pedestrian, cyclist or other VRU | no injury reported |
| Level 2 ADAS | Tesla | Sep 2026 | CT | unknown | unknown | serious |
| ADS | Motional | Sep 2026 | NV | intersection | pedestrian, cyclist or other VRU | minor |


All new reports: {download}`sgo_new_reports.csv <observatory/data/sgo_new_reports.csv>`.

## Reports and crashes per month

:::{figure} observatory/sgo_monthly.svg
:alt: Monthly SGO crashes and reports for ADS and Level 2 ADAS with reporting-rule changes marked
:width: 100%
Crashes (unique `Same Incident ID`) and reports per incident month, July 2021 to Sep 2026. Dashed lines: amended orders in force. Grey band: provisional months.
:::

Since July 2021 the files hold **3,059 ADS crashes** (3,449 reports) and **5,019 Level 2 ADAS crashes** (5,039 reports); 365 ADS and 13 ADAS crashes were reported more than once. Under the third amended order, complete months from Jul 2025 to Jul 2026 saw 61–145 ADS crashes per month (median 112) and 82–264 Level 2 ADAS crashes (median 130). These are counts: the fleets and their mileage changed over the same period.

**Reporting rules on the time axis** (as of October 2026; sources: NHTSA SGO data dictionaries and the OMB supporting statement for control no. 2127-0754):

| date | change | what must be reported |
| --- | --- | --- |
| 29 Jun 2021 | Standing General Order 2021-01 issued; first amended in August 2021 | 1-day reports (with 10-day updates) for the most severe crashes; other ADS crashes monthly; Level 2 ADAS: severe crashes only |
| 15 May 2023 | Second amended order in force (issued 5 Apr 2023) | 1-day reports for fatality, hospital transport or VRU; 5-day reports for air bag or tow-away (ADS and Level 2); other ADS crashes with any property damage monthly; new 5-day report type |
| 16 Jun 2025 | Third amended order in force (issued 24 Apr 2025) | 5-day reports for fatality, hospital transport, VRU strike or air-bag deployment, for ADS also tow-away; other ADS crashes monthly only if damage is expected to exceed USD 1,000, only the ADS vehicle was involved, or the ADS vehicle struck another vehicle or object; Level 2 tow-away-only crashes no longer reportable; no nil reports; duplicate reporting by several entities reduced |

The current files cover reports received from 16 June 2025; earlier reports come from NHTSA's archive files. 22 Level 2 ADAS crashes with incident dates before July 2021 (reported late) and 1 crash without an incident month are not plotted.

## What the crashes look like

Quarterly crash counts by category (one representative report per crash: the one alleging the highest severity). Shares within a system type are more informative than levels; comparisons *between* ADS and Level 2 ADAS are distorted by their different thresholds — the Level 2 file holds only severe crashes, the ADS file almost all.

:::{figure} observatory/sgo_partner.svg
:alt: Crash partner of SGO crashes per quarter, ADS and Level 2 ADAS
:width: 100%
Crash partner, crashes per quarter. Monthly values: {download}`sgo_monthly_by_category.csv <observatory/data/sgo_monthly_by_category.csv>`.
:::

:::{figure} observatory/sgo_road.svg
:alt: Roadway type of SGO crashes per quarter, ADS and Level 2 ADAS
:width: 100%
Roadway type, crashes per quarter. Monthly values: {download}`sgo_monthly_by_category.csv <observatory/data/sgo_monthly_by_category.csv>`.
:::

:::{figure} observatory/sgo_severity.svg
:alt: Highest injury severity alleged of SGO crashes per quarter, ADS and Level 2 ADAS
:width: 100%
Highest injury severity alleged, crashes per quarter. Monthly values: {download}`sgo_monthly_by_category.csv <observatory/data/sgo_monthly_by_category.csv>`.
:::

:::{figure} observatory/sgo_movement.svg
:alt: Pre-crash movement of the subject vehicle of SGO crashes per quarter, ADS and Level 2 ADAS
:width: 100%
Pre-crash movement of the subject vehicle, crashes per quarter. Monthly values: {download}`sgo_monthly_by_category.csv <observatory/data/sgo_monthly_by_category.csv>`.
:::

Under the third amended order, the ADS vehicle was stopped or parked in 50 % of ADS crashes, and 89 % happened on streets or at intersections; 37 % of Level 2 ADAS crashes were on highways or freeways and 38 % have an unknown roadway type. A struck, stopped vehicle says nothing about fault on its own, and an unknown field is not a random gap: it is concentrated in some reporters.

## Who reports

Concentration by reporting entity, per incident year. The share of the largest entity mostly reflects fleet size and data access, not safety; without exposure it supports no ranking. HHI is the Herfindahl–Hirschman index of reporting shares (10,000 = a single entity).

| system | year | crashes | entities | largest reporter | its share [%] | top 3 share [%] | HHI |
| --- | ---: | ---: | ---: | --- | ---: | ---: | ---: |
| Level 2 ADAS | 2021 | 226 | 13 | Tesla | 67.7 | 93.8 | 5078 |
| Level 2 ADAS | 2022 | 545 | 19 | Tesla | 83.1 | 92.8 | 6980 |
| Level 2 ADAS | 2023 | 616 | 16 | Tesla | 89.8 | 92.7 | 8069 |
| Level 2 ADAS | 2024 | 827 | 19 | Tesla | 86.5 | 91.9 | 7496 |
| Level 2 ADAS | 2025 | 1195 | 17 | Tesla | 87.2 | 94.1 | 7639 |
| Level 2 ADAS | 2026 | 1610 | 20 | Tesla | 91.7 | 96.8 | 8432 |
| ADS | 2021 | 68 | 12 | Waymo | 48.5 | 75.0 | 2837 |
| ADS | 2022 | 164 | 21 | Waymo | 47.0 | 76.8 | 2752 |
| ADS | 2023 | 287 | 21 | Waymo | 42.9 | 87.1 | 3400 |
| ADS | 2024 | 539 | 17 | Waymo | 85.7 | 92.2 | 7378 |
| ADS | 2025 | 1023 | 17 | Waymo | 87.8 | 94.4 | 7738 |
| ADS | 2026 | 978 | 16 | Waymo | 80.6 | 92.7 | 6576 |

Per-entity counts by regime, listed alphabetically: {download}`sgo_entities.csv <observatory/data/sgo_entities.csv>`. Of the reporting entities, only one (Waymo) publishes exposure that is machine-readable and linked to its SGO report IDs (as of October 2026); that is used in the next section.

## Data quality

Missing and redacted information per crash. Narratives are redacted where the reporting entity claims confidential business information (CBI). Unknown fields are concentrated in the Level 2 ADAS file: the manufacturer typically learns of the crash from vehicle telematics but, unlike an ADS operator with its own fleet data, often not its circumstances. For ADS the share of crashes reported more than once falls under the third amended order, which reduced duplicate reporting; for Level 2 ADAS it was low throughout.

| system | regime | crashes | partner unknown [%] | roadway unknown [%] | severity unknown [%] | movement unknown [%] | narrative redacted [%] | notice via telematics [%] | reported > once [%] |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Level 2 ADAS | original / 1st amended order | 965 | 28.8 | 13.8 | 82.2 | 16.6 | 84.7 | 76.8 | 0.4 |
| Level 2 ADAS | 2nd amended order | 1682 | 39.1 | 28.2 | 81.9 | 36.7 | 91.1 | 71.7 | 0.1 |
| Level 2 ADAS | 3rd amended order | 2372 | 52.6 | 38.0 | 91.2 | 52.8 | 91.7 | 90.6 | 0.3 |
| ADS | original / 1st amended order | 297 | 0.3 | 0.3 | 3.4 | 0.7 | 28.3 | 64.6 | 60.6 |
| ADS | 2nd amended order | 1200 | 0.0 | 0.1 | 1.5 | 0.1 | 8.5 | 88.6 | 15.3 |
| ADS | 3rd amended order | 1562 | 0.0 | 0.1 | 1.6 | 0.1 | 0.6 | 88.5 | 0.1 |

## Rates where exposure is public

Waymo publishes cumulative **rider-only (RO)** miles per county and the list of RO crashes with their SGO report IDs on its Safety Impact Data Hub (files `CSV1 - RO Miles per Location 202009-202606-2022benchmark.csv` and `CSV2 - Crashes with SGO ID and Group Membership 202009-202606-2022benchmark.csv`). Numerator and denominator are filtered by the same rule: RO operation, the counties with published miles, Sep 2020 to Jun 2026, 271.3 million RO miles. 41 RO crashes in counties without a published mileage figure are excluded. Of 2,221 Waymo ADS reports in the SGO files with incident months up to Jun 2026, 1,969 are in the RO crash list — the rest include supervised testing and areas outside RO service, which is why all SGO reports must not be divided by RO miles.

:::{figure} observatory/waymo_ro_rates.svg
:alt: Waymo rider-only crash rates per million miles with 95 percent exact Poisson intervals
:width: 100%
Waymo rider-only crash rates, all areas with published miles, with exact (Garwood) 95 % intervals.
:::

| outcome | crashes | per million RO miles | 95 % CI low | 95 % CI high |
| --- | ---: | ---: | ---: | ---: |
| police-reported crash | 396 | 1.4595 | 1.3193 | 1.6106 |
| any-injury-reported crash | 184 | 0.6781 | 0.5837 | 0.7835 |
| air-bag deployment (any vehicle) | 82 | 0.3022 | 0.2404 | 0.3751 |
| suspected serious injury or worse | 3 | 0.0111 | 0.0023 | 0.0323 |


Per-area values: {download}`waymo_ro_rates.csv <observatory/data/waymo_ro_rates.csv>`. **Comparison caveats.** These rates describe one operator's driverless ride-hailing service in specific cities, roads and times (its ODD). They are not comparable with other operators' SGO counts (no matched exposure), with Level 2 ADAS (different reporting threshold, human driver responsible), or with a human baseline unless that baseline is matched by area, road type, outcome definition and under-reporting. Waymo's own matched human benchmarks and their methodology are on the [Data Hub](https://waymo.com/safety/impact/); they are linked, not reproduced, here. An "any crash" rate is not shown: since June 2025 the ADS reporting threshold depends on damage and crash type, which Waymo's release notes describe as making that outcome impossible to compare with human benchmarks. Intervals capture random error only; at hundreds of millions of miles the systematic choices (which crashes count, which baseline) dominate.

## California testing: disengagements per 1,000 miles

California requires holders of a testing permit to report each year (1 December to 30 November) the autonomous miles driven and every disengagement — the safety driver taking control because of a technology failure or a safety concern. Shown: drivered testing, reporting years 2019/20 to 2023/24; manufacturers with at least 10,000 autonomous miles in the latest year, all years in which they reached that mileage.

:::{figure} observatory/ca_disengagements.svg
:alt: Disengagements per 1,000 autonomous miles by manufacturer and reporting year, California DMV
:width: 100%
Disengagements per 1,000 autonomous test miles (log scale); label: miles in 2023/24.
:::

| year | autonomous miles (all permit holders) | disengagements | pooled per 1,000 miles |
| --- | ---: | ---: | ---: |
| Dec 2019 – Nov 2020 | 1,955,199 | 3,695 | 1.89 |
| Dec 2020 – Nov 2021 | 4,091,108 | 2,676 | 0.654 |
| Dec 2021 – Nov 2022 | 5,099,141 | 8,216 | 1.611 |
| Dec 2022 – Nov 2023 | 5,748,298 | 6,562 | 1.142 |
| Dec 2023 – Nov 2024 | 3,912,658 | 1,773 | 0.453 |


All manufacturers and years: {download}`ca_disengagements.csv <observatory/data/ca_disengagements.csv>` (13 vehicle rows whose annual total disagreed with the monthly cells were summed from the months).

**Caveats.** The DMV states that the reports “are not designed for comparative analysis across companies”. Each company decides what counts as a disengagement and tests where and how it chooses (routes, difficulty, driver instructions), so a low rate can mean easy miles or a narrow definition. Driverless testing is reported separately and deployment operations not at all, so a company's main service can be absent. Disengagements cluster in time and place, so a Poisson interval would understate the uncertainty; none is shown. 
The report for December 2024 to November 2025 (announced on 20 February 2026, [news release](https://www.dmv.ca.gov/portal/news-and-media/autonomous-vehicle-permit-holders-in-california-logged-more-than-9-million-test-miles-between-december-1-2024-and-november-30-2025/)) was not available as a CSV file at the usual address when this page was built; it is added automatically once published there. 
New California regulations adopted on 28 April 2026 replace disengagement reporting with other metrics (system failures, immobilisations, hard-braking events, miles, SGO-aligned crash reports; [DMV](https://www.dmv.ca.gov/portal/news-and-media/new-autonomous-vehicle-regulations-strengthen-oversight-and-enforcement-authorize-trucks-and-transit/)), so this series will end.

California's collision reports (form OL 316) are published as individual PDF forms, now through UC Berkeley's [TIMS AV collision tool](https://tims.berkeley.edu/tools/avsafety.php); they are not used here because no machine-readable export with stable terms was found, and they overlap with the SGO reports.

## Why there is no human baseline here

A human baseline must match the numerator: the same outcome definition, area, road types, vehicle types and reporting completeness. FARS is a census of fatal crashes only, too few to compare with the outcomes above; CRSS is a national sample of police-reported crashes without the county- and road-level exposure that robotaxi or Level 2 operating domains require. Building matched baselines correctly (police-report under-reporting, vehicle miles by county and road type) is a research project in its own right — see Scanlon et al. (2024) and Kusano et al. (2024, 2025), whose benchmarks Waymo publishes on its Data Hub. A quick national average would mislead, so none is shown.

## Downloads

- {download}`sgo_monthly_by_system.csv <observatory/data/sgo_monthly_by_system.csv>` — reports and crashes per incident month and system type, with regime
- {download}`sgo_monthly_by_category.csv <observatory/data/sgo_monthly_by_category.csv>` — crashes per month by crash partner, roadway, severity and movement
- {download}`sgo_concentration.csv <observatory/data/sgo_concentration.csv>` — concentration by reporting entity per year
- {download}`sgo_entities.csv <observatory/data/sgo_entities.csv>` — crashes per reporting entity and regime (alphabetical)
- {download}`sgo_data_quality.csv <observatory/data/sgo_data_quality.csv>` — unknown and redacted fields per system type and regime
- {download}`sgo_new_reports.csv <observatory/data/sgo_new_reports.csv>` — reports new in this release
- {download}`sgo_report_index.csv <observatory/data/sgo_report_index.csv>` — report IDs and versions of this release (basis of the next diff)
- {download}`ca_disengagements.csv <observatory/data/ca_disengagements.csv>` — California miles and disengagements per manufacturer and year
- {download}`waymo_ro_rates.csv <observatory/data/waymo_ro_rates.csv>` — Waymo rider-only rates with exact Poisson intervals
- {download}`snapshot.json <observatory/data/snapshot.json>` — release dates, access dates, file hashes and headline counts

## Sources and method

- **NHTSA, Standing General Order 2021-01 incident reports**, ADS and Level 2 ADAS CSV files, current (release of 15 October 2026) and archive 2021–2025 (release of 26 March 2026). <https://static.nhtsa.gov/odi/ffdd/sgo-2021-01/> · overview: <https://www.nhtsa.gov/laws-regulations/standing-general-order-crash-reporting>. Public US government data. Accessed 29 October 2026 — checked in this refresh, unchanged.
- NHTSA, *Standing General Order 2021-01 Data Dictionary* (current: <https://static.nhtsa.gov/odi/ffdd/sgo-2021-01/SGO-2021-01_Data_Element_Definitions.pdf>; archive, with the change log of the earlier orders: <https://static.nhtsa.gov/odi/ffdd/sgo-2021-01/Archive-2021-2025/SGO-2021-01_Data_Element_Definitions.pdf>). Source of the caveats quoted above.
- NHTSA, *Information Collection Request Supporting Statement, Part A: Incident Reporting for ADS and Level 2 ADAS*, OMB control no. 2127-0754 (2026), <https://omb.report/icr/202605-2127-005/doc/169129500.pdf>. Source of the reporting criteria of the third amended order.
- **California DMV, Autonomous Vehicle Mileage Reports** (drivered testing), reporting years 2020 to 2024, e.g. <https://www.dmv.ca.gov/portal/file/2024-autonomous-mileage-reports-csv/>. Information on the DMV website is public domain unless otherwise indicated (<https://www.dmv.ca.gov/portal/conditions-of-use/>). Accessed 29 October 2026 — checked in this refresh, unchanged.
- **Waymo, Safety Impact Data Hub**, <https://waymo.com/safety/impact/>, CSV1 (RO miles per location) and CSV2 (crashes with SGO ID). Waymo provides the files “to help researchers reproduce the results or conduct their own research” (release notes); the files are not redistributed here, only derived counts and rates. Accessed 29 October 2026 — checked in this refresh, unchanged.
- Kusano, K. D., et al. (2024). Comparison of Waymo rider-only crash data to human benchmarks at 7.1 million miles. *Traffic Injury Prevention*, 25(sup1). <https://doi.org/10.1080/15389588.2024.2380786>
- Kusano, K. D., et al. (2025). Comparison of Waymo rider-only crash rates by crash type to human benchmarks at 56.7 million miles. *Traffic Injury Prevention*, 26(sup1). <https://doi.org/10.1080/15389588.2025.2499887>
- Scanlon, J. M., et al. (2024). Benchmarks for retrospective automated driving system crash rate analysis using police-reported crash data. *Traffic Injury Prevention*, 25(sup1). <https://doi.org/10.1080/15389588.2024.2380522>

**Method.** Reports from the archive and current files are pooled; each `Report ID` keeps its latest version (the current file wins a tie). Crashes are unique `Same Incident ID`s within a system type; the representative report is the one alleging the highest severity. Categories merge the archive and current vocabularies (e.g. “Minor” and “Minor W/O Hospitalization” → minor). The regime of a crash is assigned by incident month, so May 2023 and June 2025 straddle two regimes. Months from Aug 2026 are provisional. The diff compares report IDs and versions with the stored index of the previous release. Rate intervals are exact (Garwood) Poisson intervals from `avsafety.validation.poisson_rate_interval`. File hashes are in `snapshot.json`.

