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
"""

__version__ = "1.0.0"

from . import coverage, iso21434, iso26262, sotif, uq, validation  # noqa: F401
