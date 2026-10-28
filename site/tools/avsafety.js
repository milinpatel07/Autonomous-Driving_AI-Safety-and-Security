/*
 * avsafety.js — browser port of the tested Python package `avsafety`.
 * Every function mirrors avsafety/*.py; tests/test_js_parity.py runs this file
 * under Node and checks it against the Python implementation.
 * MIT Licence · Milin Patel
 */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory();
  else root.AVSafety = factory();
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  // ---------------------------------------------------------------- ISO 26262
  const ASIL_TABLE = {
    S1: { E1: ["QM", "QM", "QM"], E2: ["QM", "QM", "QM"], E3: ["QM", "QM", "A"], E4: ["QM", "A", "B"] },
    S2: { E1: ["QM", "QM", "QM"], E2: ["QM", "QM", "A"], E3: ["QM", "A", "B"], E4: ["A", "B", "C"] },
    S3: { E1: ["QM", "QM", "A"], E2: ["QM", "A", "B"], E3: ["A", "B", "C"], E4: ["B", "C", "D"] },
  };
  const VALID = { S: ["S0", "S1", "S2", "S3"], E: ["E0", "E1", "E2", "E3", "E4"], C: ["C0", "C1", "C2", "C3"] };

  function determineAsil(s, e, c) {
    [s, e, c] = [s, e, c].map((x) => String(x).trim().toUpperCase());
    for (const [v, k] of [[s, "S"], [e, "E"], [c, "C"]]) {
      if (!VALID[k].includes(v)) throw new Error(`invalid ${k} class: ${v}`);
    }
    if (s === "S0" || e === "E0" || c === "C0") return "QM";
    return ASIL_TABLE[s][e][Number(c[1]) - 1];
  }

  const DECOMPOSITIONS = { D: [["C", "A"], ["B", "B"], ["D", "QM"]], C: [["B", "A"], ["C", "QM"]], B: [["A", "A"], ["B", "QM"]], A: [["A", "QM"]] };
  function decompositionOptions(asil) {
    if (!DECOMPOSITIONS[asil]) throw new Error(`ASIL ${asil} cannot be decomposed`);
    return DECOMPOSITIONS[asil].map(([a, b]) => [`${a}(${asil})`, `${b}(${asil})`]);
  }

  // -------------------------------------------------------------- ISO/SAE 21434
  const ELAPSED_TIME = { "<=1 day": 0, "<=1 week": 1, "<=1 month": 4, "<=6 months": 17, ">6 months": 19 };
  const EXPERTISE = { layman: 0, proficient: 3, expert: 6, "multiple experts": 8 };
  const KNOWLEDGE = { public: 0, restricted: 3, confidential: 7, "strictly confidential": 11 };
  const WINDOW = { unlimited: 0, easy: 1, moderate: 4, difficult: 10 };
  const EQUIPMENT = { standard: 0, specialized: 4, bespoke: 7, "multiple bespoke": 9 };

  function attackPotential(t, ex, k, w, eq) {
    const vals = [ELAPSED_TIME[t], EXPERTISE[ex], KNOWLEDGE[k], WINDOW[w], EQUIPMENT[eq]];
    if (vals.some((v) => v === undefined)) throw new Error("unknown factor value");
    return vals.reduce((a, b) => a + b, 0);
  }
  function feasibilityFromPotential(p) {
    if (p < 0) throw new Error("attack potential must be non-negative");
    if (p <= 13) return "High";
    if (p <= 19) return "Medium";
    if (p <= 24) return "Low";
    return "Very Low";
  }
  const FEASIBILITY_FROM_VECTOR = { Network: "High", Adjacent: "Medium", Local: "Low", Physical: "Very Low" };
  const RISK_MATRIX = {
    Severe: { "Very Low": 2, Low: 3, Medium: 4, High: 5 },
    Major: { "Very Low": 1, Low: 2, Medium: 3, High: 4 },
    Moderate: { "Very Low": 1, Low: 2, Medium: 2, High: 3 },
    Negligible: { "Very Low": 1, Low: 1, Medium: 1, High: 1 },
  };
  function riskValue(impact, feas) {
    const v = (RISK_MATRIX[impact] || {})[feas];
    if (v === undefined) throw new Error("invalid impact/feasibility");
    return v;
  }
  const CAL_TABLE = {
    Severe: { Physical: 2, Local: 3, Adjacent: 4, Network: 4 },
    Major: { Physical: 1, Local: 2, Adjacent: 3, Network: 4 },
    Moderate: { Physical: 1, Local: 1, Adjacent: 2, Network: 3 },
  };
  function determineCal(impact, vector) {
    if (impact === "Negligible") return null;
    const v = (CAL_TABLE[impact] || {})[vector];
    if (v === undefined) throw new Error("invalid impact/attack vector");
    return v;
  }

  // CVSS v3.1
  const AV = { N: 0.85, A: 0.62, L: 0.55, P: 0.2 }, AC = { L: 0.77, H: 0.44 };
  const PR_U = { N: 0.85, L: 0.62, H: 0.27 }, PR_C = { N: 0.85, L: 0.68, H: 0.5 };
  const UI = { N: 0.85, R: 0.62 }, CIA = { H: 0.56, L: 0.22, N: 0 };
  function roundup(x) {
    const i = Math.round(x * 100000);
    return i % 10000 === 0 ? i / 100000 : (Math.floor(i / 10000) + 1) / 10;
  }
  function cvss31Exploitability(av, ac, pr, ui, scope = "U") {
    return 8.22 * AV[av] * AC[ac] * (scope === "C" ? PR_C : PR_U)[pr] * UI[ui];
  }
  function cvss31BaseScore(vector) {
    const p = {};
    vector.split("/").filter((s) => !s.startsWith("CVSS")).forEach((s) => { const [k, v] = s.split(":"); p[k] = v; });
    const iss = 1 - (1 - CIA[p.C]) * (1 - CIA[p.I]) * (1 - CIA[p.A]);
    const impact = p.S === "U" ? 6.42 * iss : 7.52 * (iss - 0.029) - 3.25 * Math.pow(iss - 0.02, 15);
    const expl = cvss31Exploitability(p.AV, p.AC, p.PR, p.UI, p.S);
    if (impact <= 0) return 0;
    return p.S === "U" ? roundup(Math.min(impact + expl, 10)) : roundup(Math.min(1.08 * (impact + expl), 10));
  }
  function feasibilityFromCvssExploitability(e) {
    if (e >= 2.96) return "High";
    if (e >= 2.0) return "Medium";
    if (e >= 1.06) return "Low";
    return "Very Low";
  }

  // ---------------------------------------------------------- SOTIF / RSS
  function timeToCollision(gap, vf, vl) {
    const closing = vf - vl;
    if (gap <= 0) return 0;
    return closing > 0 ? gap / closing : Infinity;
  }
  function timeHeadway(gap, vf) { return vf > 0 ? gap / vf : Infinity; }
  function drac(gap, vf, vl) {
    const closing = vf - vl;
    if (closing <= 0) return 0;
    if (gap <= 0) return Infinity;
    return (closing * closing) / (2 * gap);
  }
  function rssSafeLongitudinalDistance(vr, vf, rho = 0.5, aMax = 2.0, bMin = 4.0, bMax = 8.0) {
    if (Math.min(rho, aMax, bMin, bMax) < 0 || bMin === 0 || bMax === 0) throw new Error("parameters must be positive");
    const vAfter = vr + rho * aMax;
    const d = vr * rho + 0.5 * aMax * rho * rho + (vAfter * vAfter) / (2 * bMin) - (vf * vf) / (2 * bMax);
    return Math.max(d, 0);
  }
  function stoppingDistance(v, reaction, decel) { return v * reaction + (v * v) / (2 * decel); }

  // ------------------------------------------------------------ validation
  // Regularised lower incomplete gamma and chi-square quantile (enough for k = 2(n+1)).
  function gammaln(x) {
    const c = [76.18009172947146, -86.50532032941677, 24.01409824083091, -1.231739572450155, 0.1208650973866179e-2, -0.5395239384953e-5];
    let y = x, tmp = x + 5.5, ser = 1.000000000190015;
    tmp -= (x + 0.5) * Math.log(tmp);
    for (let j = 0; j < 6; j++) ser += c[j] / ++y;
    return -tmp + Math.log((2.5066282746310005 * ser) / x);
  }
  function gammaP(a, x) {
    if (x <= 0) return 0;
    if (x < a + 1) {
      let sum = 1 / a, del = sum, ap = a;
      for (let n = 0; n < 500; n++) { ap += 1; del *= x / ap; sum += del; if (Math.abs(del) < Math.abs(sum) * 1e-15) break; }
      return sum * Math.exp(-x + a * Math.log(x) - gammaln(a));
    }
    let b = x + 1 - a, c = 1 / 1e-300, d = 1 / b, h = d;
    for (let i = 1; i < 500; i++) {
      const an = -i * (i - a); b += 2;
      d = an * d + b; if (Math.abs(d) < 1e-300) d = 1e-300;
      c = b + an / c; if (Math.abs(c) < 1e-300) c = 1e-300;
      d = 1 / d; const del = d * c; h *= del; if (Math.abs(del - 1) < 1e-15) break;
    }
    return 1 - Math.exp(-x + a * Math.log(x) - gammaln(a)) * h;
  }
  function chi2ppf(p, k) {
    let lo = 0, hi = Math.max(10, k * 10);
    while (gammaP(k / 2, hi / 2) < p) hi *= 2;
    for (let i = 0; i < 200; i++) { const mid = (lo + hi) / 2; if (gammaP(k / 2, mid / 2) < p) lo = mid; else hi = mid; }
    return (lo + hi) / 2;
  }
  function milesToDemonstrate(rate, confidence = 0.95, failures = 0) {
    if (!(confidence > 0 && confidence < 1) || rate <= 0 || failures < 0) throw new Error("invalid arguments");
    return chi2ppf(confidence, 2 * (failures + 1)) / (2 * rate);
  }
  function fleetYears(miles, vehicles = 100, perVehicleYear = 24 * 365 * 25) { return miles / (vehicles * perVehicleYear); }

  return {
    ASIL_TABLE, determineAsil, decompositionOptions,
    ELAPSED_TIME, EXPERTISE, KNOWLEDGE, WINDOW, EQUIPMENT, attackPotential, feasibilityFromPotential,
    FEASIBILITY_FROM_VECTOR, RISK_MATRIX, riskValue, CAL_TABLE, determineCal,
    cvss31Exploitability, cvss31BaseScore, feasibilityFromCvssExploitability,
    timeToCollision, timeHeadway, drac, rssSafeLongitudinalDistance, stoppingDistance,
    chi2ppf, milesToDemonstrate, fleetYears,
  };
});
