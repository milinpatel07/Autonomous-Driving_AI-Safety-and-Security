"""avsafety — small, tested reference implementations for AV safety & security.

The notebooks in this repository are self-contained for Google Colab; this package
holds the same normative tables and formulas in one tested place so that they can
be reused in projects and checked in CI.

Modules
-------
iso26262    ASIL determination, ASIL decomposition, hardware-metric targets
iso21434    attack potential, attack feasibility, risk value, CAL, CVSS v3.1 base score
sotif       criticality metrics (TTC, THW, DRAC), RSS longitudinal safe distance
validation  statistical validation (zero-failure miles, Poisson confidence bounds)
uq          calibration (ECE, Brier, NLL), temperature scaling, split conformal prediction
coverage    scenario / ODD coverage (n-wise combinatorial coverage)
data        real public datasets on demand: KITTI, NGSIM, NHTSA SGO crash reports,
            ROAD CAN intrusion logs, VeReMi Extension V2X messages
perturb     physically grounded perturbations: Koschmieder fog from LiDAR depth, low light, lens dirt, LiDAR fog
bench       SOTIF perception benchmark: versioned split, evaluation, report, release verdict (python -m avsafety.bench)
assurance   safety case as code: GSN argument, evidence records, status evaluation, staleness, rendering
exercises   auto-checked exercises with formative feedback (reference values computed by the modules above)
"""

__version__ = "1.2.0"

from . import assurance, bench, coverage, data, exercises, iso21434, iso26262, perturb, sotif, uq, validation  # noqa: F401
