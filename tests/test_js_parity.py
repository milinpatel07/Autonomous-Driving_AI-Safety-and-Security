"""The browser calculators (site/tools/avsafety.js) must agree with the Python toolkit."""
import itertools
import json
import shutil
import subprocess
from pathlib import Path

import pytest

from avsafety import iso21434, iso26262, sotif, validation

JS = Path(__file__).resolve().parents[1] / "site" / "tools" / "avsafety.js"
pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")


def js(expr: str):
    code = f"const A = require({json.dumps(str(JS))}); console.log(JSON.stringify({expr}));"
    out = subprocess.run(["node", "-"], input=code, capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def test_asil_full_table():
    combos = list(itertools.product(["S0", "S1", "S2", "S3"], ["E0", "E1", "E2", "E3", "E4"], ["C0", "C1", "C2", "C3"]))
    got = js("[" + ",".join(f"A.determineAsil('{s}','{e}','{c}')" for s, e, c in combos) + "]")
    assert got == [iso26262.determine_asil(s, e, c) for s, e, c in combos]


def test_decomposition():
    for a in "ABCD":
        assert [tuple(x) for x in js(f"A.decompositionOptions('{a}')")] == iso26262.decomposition_options(a)


def test_21434_tables():
    for p in range(0, 58):
        assert js(f"A.feasibilityFromPotential({p})") == iso21434.feasibility_from_potential(p)
    for imp in iso21434.IMPACT_LEVELS:
        for f in iso21434.FEASIBILITY_LEVELS:
            assert js(f"A.riskValue('{imp}','{f}')") == iso21434.risk_value(imp, f)
        for v in iso21434.FEASIBILITY_FROM_VECTOR:
            assert js(f"A.determineCal('{imp}','{v}')") == iso21434.determine_cal(imp, v)


def test_cvss_all_vectors():
    vectors = [f"CVSS:3.1/AV:{av}/AC:{ac}/PR:{pr}/UI:{ui}/S:{s}/C:{c}/I:{i}/A:{a}"
               for av, ac, pr, ui, s, c, i, a in itertools.product("NALP", "LH", "NLH", "NR", "UC", "HLN", "HLN", "HLN")]
    got = js("[" + ",".join(f"A.cvss31BaseScore('{v}')" for v in vectors) + "]")
    assert got == [iso21434.cvss31_base_score(v) for v in vectors]


def test_rss_and_metrics():
    cases = [(0, 0), (25, 25), (30, 20), (13.9, 0), (36, 30)]
    got = js("[" + ",".join(f"A.rssSafeLongitudinalDistance({a},{b},0.7,3,5,9)" for a, b in cases) + "]")
    want = [sotif.rss_safe_longitudinal_distance(a, b, 0.7, 3, 5, 9) for a, b in cases]
    assert got == pytest.approx(want, rel=1e-12)
    assert js("A.drac(25,15,5)") == pytest.approx(sotif.drac(25, 15, 5))


@pytest.mark.parametrize("rate,conf,k", [(1.09e-8, 0.95, 0), (1.09e-8, 0.99, 0), (2e-7, 0.95, 3), (1e-6, 0.9, 10)])
def test_validation_miles(rate, conf, k):
    assert js(f"A.milesToDemonstrate({rate},{conf},{k})") == pytest.approx(validation.miles_to_demonstrate(rate, conf, k), rel=1e-6)
