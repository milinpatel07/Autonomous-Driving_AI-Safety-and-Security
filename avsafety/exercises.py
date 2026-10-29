"""Auto-checked exercises: formative feedback computed from the toolkit itself.

Every checker compares a learner's answer with the value that the tested toolkit
functions give for the same problem (:mod:`avsafety.iso26262`, :mod:`avsafety.iso21434`,
:mod:`avsafety.sotif`, :mod:`avsafety.validation`), so there is no separate answer key
to maintain. A checker never raises because of a learner's answer: it returns a
:class:`CheckResult` whose text says whether the answer is correct and, if not, gives a
hint and points to the notebook section that explains the step. Invalid *problem*
parameters (e.g. an exposure class ``"E5"``) still raise ``ValueError``, because they are
the instructor's error, not the learner's.

Usage in a notebook (the cell runs before the learner has answered)::

    from avsafety import exercises as ex
    my_asil = None                      # your answer, e.g. "B"
    ex.check_asil(my_asil, "S3", "E2", "C2")

Usage in a grading test::

    assert ex.check_asil(answers.ASIL_HE01, "S3", "E2", "C2").correct
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from itertools import combinations
from typing import Any, Iterable, Mapping

from . import iso21434, iso26262, sotif, validation

__all__ = [
    "CheckResult", "check_asil", "check_asil_decomposition", "check_hardware_metrics",
    "check_hw_targets", "check_basic_event_probability", "check_minimal_cut_sets",
    "minimal_cut_sets", "check_attack_feasibility", "check_risk_value", "check_cal",
    "check_rss_distance", "check_criticality_metrics", "check_validation_target",
    "check_sotif_area", "check_triggering_condition_table",
]

_MARK = {"correct": "✓", "incorrect": "✗", "invalid": "✗", "missing": "○"}


@dataclass(frozen=True)
class CheckResult:
    """Outcome of one check.

    ``status`` is ``"correct"``, ``"incorrect"``, ``"invalid"`` (the answer could not be
    read, e.g. a misspelt class) or ``"missing"`` (no answer yet). ``hint`` and ``see``
    are empty for a correct answer. The object is truthy only when the answer is correct,
    and it displays as a one-line message in a notebook.
    """

    exercise: str
    status: str
    message: str
    hint: str = ""
    see: str = ""

    @property
    def correct(self) -> bool:
        return self.status == "correct"

    def __bool__(self) -> bool:
        return self.correct

    def __str__(self) -> str:
        text = f"{_MARK.get(self.status, '?')} {self.exercise}: {self.message}"
        if self.hint:
            text += f"\n  Hint: {self.hint}"
        if self.see:
            text += f"\n  See: {self.see}"
        return text

    __repr__ = __str__


# ---------------------------------------------------------------- helpers
def _is_missing(answer: Any) -> bool:
    return answer is None or answer is Ellipsis or (isinstance(answer, str) and not answer.strip())


def _missing(exercise: str) -> CheckResult:
    return CheckResult(exercise, "missing", "no answer yet. Fill in your answer and run the check again.")


def _ok(exercise: str, message: str = "correct.") -> CheckResult:
    return CheckResult(exercise, "correct", message)


def _close(a: float, b: float, rel: float, abs_: float = 0.0) -> bool:
    if math.isinf(a) or math.isinf(b):
        return math.isinf(a) and math.isinf(b) and (a > 0) == (b > 0)
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_)


def _number(x: Any):
    """Read a number (int/float/numeric string, 'inf'); None if impossible."""
    if isinstance(x, bool):
        return None
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def _asil_label(x: Any):
    s = str(x).strip().upper().replace("ASIL", "").replace(" ", "")
    return s if s in iso26262.ASIL_ORDER else None


def _cmp_word(answer_rank: int, expected_rank: int, unit: str) -> str:
    return f"Your {unit} is {'higher' if answer_rank > expected_rank else 'lower'} than the table gives."


# ---------------------------------------------------------------- ISO 26262
def check_asil(answer: Any, severity: str, exposure: str, controllability: str, *,
               exercise: str = "ASIL", see: str = "03-02 HARA, section 7 (ASIL determination)") -> CheckResult:
    """Check an ASIL ("QM", "A".."D", "ASIL B" accepted) against ISO 26262-3:2018 Table 4."""
    expected = iso26262.determine_asil(severity, exposure, controllability)  # raises for invalid problems
    if _is_missing(answer):
        return _missing(exercise)
    got = _asil_label(answer)
    if got is None:
        return CheckResult(exercise, "invalid", f"cannot read {answer!r} as an ASIL.",
                           "Write one of 'QM', 'A', 'B', 'C' or 'D'.", see)
    if got == expected:
        return _ok(exercise, f"correct, {severity}/{exposure}/{controllability} gives "
                             f"{'QM' if expected == 'QM' else 'ASIL ' + expected}.")
    classes = (str(severity).upper(), str(exposure).upper(), str(controllability).upper())
    if any(c.endswith("0") for c in classes):
        hint = "One of the classes is S0, E0 or C0. What does a class of 0 mean for the ASIL?"
    else:
        hint = (_cmp_word(iso26262.asil_rank(got), iso26262.asil_rank(expected), "ASIL")
                + f" Read ISO 26262-3 Table 4 again: block {classes[0]}, row {classes[1]}, column {classes[2]}.")
    return CheckResult(exercise, "incorrect", f"{got} is not the ASIL for this hazardous event.", hint, see)


def _split_decomposed(label: Any):
    """'B(D)' -> ('B', 'D'); 'B' -> ('B', None); None if unreadable."""
    s = str(label).strip().upper().replace("ASIL", "").replace(" ", "")
    if "(" in s:
        if not s.endswith(")"):
            return None
        own, parent = s[:-1].split("(", 1)
    else:
        own, parent = s, None
    if own not in iso26262.ASIL_ORDER or (parent is not None and parent not in iso26262.ASIL_ORDER):
        return None
    return own, parent


def check_asil_decomposition(answer: Any, asil: str, *, exercise: str = "ASIL decomposition",
                             see: str = "03-02 HARA, section 10; 03-04 Fault tree analysis, section 8") -> CheckResult:
    """Check a pair such as ``("B(D)", "B(D)")`` against ISO 26262-9:2018 clause 5.

    Any permitted decomposition is accepted (order does not matter). The ISO notation
    with the original ASIL in brackets is required.
    """
    options = iso26262.decomposition_options(asil)  # raises for QM
    if _is_missing(answer):
        return _missing(exercise)
    try:
        answer = tuple(answer) if not isinstance(answer, str) else answer
    except TypeError:
        answer = str(answer)
    if isinstance(answer, str) or len(answer) != 2:
        return CheckResult(exercise, "invalid", "give exactly two requirements, e.g. ('X(D)', 'Y(D)').",
                           "A decomposition splits one requirement into two redundant ones.", see)
    parts = [_split_decomposed(a) for a in answer]
    if None in parts:
        return CheckResult(exercise, "invalid", f"cannot read {tuple(answer)!r}.",
                           "Write each part as an ASIL with the original ASIL in brackets, e.g. 'A(C)'.", see)
    pair = sorted((p[0] for p in parts), key=iso26262.asil_rank)
    permitted = [sorted((a.split("(")[0], b.split("(")[0]), key=iso26262.asil_rank) for a, b in options]
    if pair not in permitted:
        total = sum(iso26262.asil_rank(p) for p in pair)
        if total < iso26262.asil_rank(asil):
            hint = "The two parts together are weaker than the original ASIL allows."
        else:
            hint = "Check the list of permitted schemes in ISO 26262-9 clause 5.4 for this ASIL."
        return CheckResult(exercise, "incorrect", f"{pair[0]} + {pair[1]} is not a permitted decomposition of "
                                                  f"ASIL {asil}.", hint, see)
    if any(p[1] != asil for p in parts):
        return CheckResult(exercise, "incorrect", "the split is right, but the notation is incomplete.",
                           f"Write the original ASIL in brackets after each part, e.g. '{pair[1]}({asil})'. "
                           "It records which targets (e.g. hardware metrics) still apply.", see)
    return _ok(exercise, f"correct, {answer[0]} + {answer[1]} is a permitted decomposition of ASIL {asil}. "
                         "It still needs independence shown by a dependent failure analysis.")


def _fmeda_rows(entries: Iterable[Any]) -> list[dict]:
    """Accept avsafety-style mappings or objects with FMEDA attributes (as in notebook 03-03)."""
    rows = []
    for e in entries:
        if isinstance(e, Mapping):
            rows.append(dict(e))
        else:
            rows.append({"rate": e.rate, "safe": getattr(e, "safe_fault", False),
                         "spf": getattr(e, "single_point", False), "dc": getattr(e, "dc_rf", 0.0),
                         "dc_latent": getattr(e, "dc_latent", 0.0)})
    return rows


def check_hardware_metrics(answer: Any, entries: Iterable[Any], *, abs_tol: float = 5e-4, rel_tol_fit: float = 0.01,
                           exercise: str = "Hardware metrics",
                           see: str = "03-03 FMEA and FMEDA, section 8") -> CheckResult:
    """Check SPFM / LFM (fractions, 0..1) and PMHF_FIT against :func:`avsafety.iso26262.hardware_metrics`.

    ``answer`` is a mapping with any of the keys ``"SPFM"``, ``"LFM"``, ``"PMHF_FIT"``;
    only the keys given are checked. ``entries`` are FMEDA rows (see the toolkit function).
    """
    rows = _fmeda_rows(entries)
    ref = iso26262.hardware_metrics(rows)
    if _is_missing(answer) or (isinstance(answer, Mapping) and all(_is_missing(v) for v in answer.values())):
        return _missing(exercise)
    if not isinstance(answer, Mapping):
        return CheckResult(exercise, "invalid", "give a dict such as {'SPFM': 0.98, 'LFM': 0.9, 'PMHF_FIT': 3.2}.",
                           see=see)
    wrong, hints, checked = [], [], []
    for key, val in answer.items():
        if key not in ("SPFM", "LFM", "PMHF_FIT") or _is_missing(val):
            continue
        num = _number(val)
        if num is None:
            return CheckResult(exercise, "invalid", f"{key} = {val!r} is not a number.", see=see)
        checked.append(key)
        if key in ("SPFM", "LFM") and num > 1.0:
            wrong.append(key)
            hints.append(f"Give {key} as a fraction between 0 and 1 (e.g. 0.97, not 97).")
            continue
        exp = ref[key]
        ok = _close(num, exp, rel_tol_fit) if key == "PMHF_FIT" else abs(num - exp) <= abs_tol
        if ok:
            continue
        wrong.append(key)
        total = sum(float(r["rate"]) for r in rows)
        spf = sum(float(r["rate"]) for r in rows if r.get("spf") and not r.get("safe"))
        if key == "SPFM":
            if abs(num - (1 - spf / total)) <= abs_tol:
                hints.append("Your SPFM counts single-point faults only; residual faults "
                             "(the part a safety mechanism misses, rate x (1 - DC)) also count.")
            else:
                hints.append("SPFM = 1 - (single-point + residual) / total rate; safe faults stay in the total.")
        elif key == "LFM":
            if abs(num - ref["SPFM"]) <= abs_tol:
                hints.append("Your LFM equals the SPFM. The LFM measures latent faults of the safety mechanisms: "
                             "rate x DC_RF x (1 - DC_latent), over the total minus single-point and residual faults.")
            else:
                hints.append("LFM = 1 - latent multiple-point faults / (total - single-point - residual).")
        else:
            if _close(num, ref["PMHF_FIT"] * 1e-9, 0.01):
                hints.append("PMHF_FIT is asked in FIT (failures per 1e9 h), not per hour.")
            else:
                hints.append("The first-order PMHF here is the sum of single-point and residual fault rates (FIT).")
    if not checked:
        return _missing(exercise)
    if wrong:
        right = [k for k in checked if k not in wrong]
        msg = f"{', '.join(wrong)} not correct" + (f"; {', '.join(right)} correct." if right else ".")
        return CheckResult(exercise, "incorrect", msg, " ".join(hints), see)
    return _ok(exercise, f"correct ({', '.join(checked)}).")


def check_hw_targets(answer: Any, entries: Iterable[Any], asil: str, *, exercise: str = "Hardware targets",
                     see: str = "03-03 FMEA and FMEDA, section 8 (target values)") -> CheckResult:
    """Check whether the learner judged the ISO 26262-5 targets for ``asil`` correctly.

    ``answer`` is either one bool ("all targets met") or a mapping
    ``{"SPFM": bool, "LFM": bool, "PMHF": bool}``.
    """
    met = iso26262.meets_hw_targets(iso26262.hardware_metrics(_fmeda_rows(entries)), asil)
    if _is_missing(answer) or (isinstance(answer, Mapping) and all(_is_missing(v) for v in answer.values())):
        return _missing(exercise)
    if isinstance(answer, bool):
        if answer == all(met.values()):
            return _ok(exercise, f"correct, the ASIL {asil} targets are {'met' if answer else 'not all met'}.")
        return CheckResult(exercise, "incorrect", "your overall verdict is not right.",
                           f"Compare each metric with its ASIL {asil} target: SPFM and LFM must be at least the "
                           "target, the PMHF strictly below it.", see)
    if not isinstance(answer, Mapping):
        return CheckResult(exercise, "invalid", "give True/False or a dict {'SPFM': bool, 'LFM': bool, 'PMHF': bool}.",
                           see=see)
    wrong = [k for k, v in answer.items() if k in met and not _is_missing(v) and bool(v) != met[k]]
    if wrong:
        return CheckResult(exercise, "incorrect", f"verdict for {', '.join(wrong)} not right.",
                           f"Look up the ASIL {asil} target of each metric in ISO 26262-5 Tables 4-6 and compare.", see)
    return _ok(exercise, "correct.")


def check_basic_event_probability(answer: Any, lambda_fit: float, tau_h: float, *, rel_tol: float = 0.02,
                                  exercise: str = "Basic event probability",
                                  see: str = "03-04 Fault tree analysis, section 6") -> CheckResult:
    """Check q = 1 - exp(-lambda * tau) with lambda in FIT (1e-9 per hour) and tau in hours."""
    if lambda_fit < 0 or tau_h < 0:
        raise ValueError("lambda_fit and tau_h must be non-negative")
    expected = 1.0 - math.exp(-lambda_fit * 1e-9 * tau_h)
    if _is_missing(answer):
        return _missing(exercise)
    num = _number(answer)
    if num is None:
        return CheckResult(exercise, "invalid", f"{answer!r} is not a number.", see=see)
    if _close(num, expected, rel_tol, 1e-15):
        return _ok(exercise, f"correct, q = {expected:.2e}.")
    if _close(num, lambda_fit * tau_h, rel_tol) or (lambda_fit * tau_h > 0 and _close(num, 1 - math.exp(-lambda_fit * tau_h), rel_tol)):
        hint = "Check the units: 1 FIT is one failure per 10^9 hours."
    elif not 0 <= num <= 1:
        hint = "A probability lies between 0 and 1."
    else:
        hint = "Use q = 1 - exp(-lambda * tau): lambda per hour, tau the exposure time in hours."
    return CheckResult(exercise, "incorrect", f"{num:.3g} is not the probability of this basic event.", hint, see)


def minimal_cut_sets(gates: Mapping[str, tuple], top: str) -> list[frozenset]:
    """Minimal cut sets of a small fault tree (top-down expansion, then absorption).

    ``gates`` maps a gate name to ``("AND", [children])``, ``("OR", [children])`` or
    ``("KOFN", [children], k)``; every name that is not a gate is a basic event.
    """
    def expand(name: str) -> list[frozenset]:
        if name not in gates:
            return [frozenset([name])]
        kind, children, *rest = gates[name]
        kind = kind.upper()
        child_sets = [expand(c) for c in children]
        if kind == "OR":
            return [cs for sets in child_sets for cs in sets]
        if kind == "AND":
            groups = [child_sets]
        elif kind == "KOFN":
            k = int(rest[0])
            groups = [list(sub) for sub in combinations(child_sets, k)]
        else:
            raise ValueError(f"unknown gate type {kind!r}")
        out = []
        for group in groups:
            acc = [frozenset()]
            for sets in group:
                acc = [a | s for a in acc for s in sets]
            out.extend(acc)
        return out

    sets = set(expand(top))
    minimal = [s for s in sets if not any(o < s for o in sets)]
    return sorted(minimal, key=lambda s: (len(s), sorted(s)))


def check_minimal_cut_sets(answer: Any, gates: Mapping[str, tuple], top: str, *,
                           exercise: str = "Minimal cut sets",
                           see: str = "03-04 Fault tree analysis, sections 3 and 5") -> CheckResult:
    """Check a list of cut sets, e.g. ``[{"A"}, {"B", "C"}]`` (order does not matter)."""
    expected = set(minimal_cut_sets(gates, top))
    if _is_missing(answer):
        return _missing(exercise)
    try:
        got = {frozenset([c]) if isinstance(c, str) else frozenset(c) for c in answer}
    except TypeError:
        return CheckResult(exercise, "invalid", "give a list of sets, e.g. [{'A'}, {'B', 'C'}].", see=see)
    if got == expected:
        return _ok(exercise, f"correct, {len(expected)} minimal cut set(s).")
    events = set().union(*expected)
    unknown = set().union(*got) - events if got else set()
    if unknown:
        return CheckResult(exercise, "invalid", f"unknown event(s): {', '.join(sorted(unknown))}.", see=see)
    not_minimal = [s for s in got if any(o < s for o in got)]
    hints = []
    if not_minimal:
        hints.append(f"{len(not_minimal)} of your sets contain another of your sets; absorption removes them.")
    missing = len(expected - got)
    wrong = len(got - expected) - len(not_minimal)
    if missing:
        hints.append(f"{missing} minimal cut set(s) are missing.")
    if wrong > 0:
        hints.append(f"{wrong} of your sets do not cause the top event on their own or are not minimal.")
    return CheckResult(exercise, "incorrect", "not the minimal cut sets of this tree.",
                       " ".join(hints) + " Expand AND gates into one row, OR gates into separate rows.", see)


# ---------------------------------------------------------------- ISO/SAE 21434
def check_attack_feasibility(answer: Any, elapsed_time: str, expertise: str, knowledge: str, window: str,
                             equipment: str, *, exercise: str = "Attack feasibility",
                             see: str = "05-02 TARA, sections 3 and 8") -> CheckResult:
    """Check an attack potential (int), a feasibility rating (str), or both.

    ``answer`` may be ``14``, ``"Medium"``, ``(14, "Medium")`` or
    ``{"potential": 14, "feasibility": "Medium"}``. Factor labels as in
    :mod:`avsafety.iso21434` (ISO/SAE 21434:2021 Annex G.2).
    """
    potential = iso21434.attack_potential(elapsed_time, expertise, knowledge, window, equipment)
    feasibility = iso21434.feasibility_from_potential(potential)
    if _is_missing(answer):
        return _missing(exercise)
    if isinstance(answer, Mapping):
        ans_p, ans_f = answer.get("potential"), answer.get("feasibility")
    elif isinstance(answer, (tuple, list)) and len(answer) == 2:
        ans_p, ans_f = answer
    elif isinstance(answer, str) and _number(answer) is None:
        ans_p, ans_f = None, answer
    else:
        ans_p, ans_f = answer, None
    if _is_missing(ans_p) and _is_missing(ans_f):
        return _missing(exercise)
    if not _is_missing(ans_p):
        p = _number(ans_p)
        if p is None:
            return CheckResult(exercise, "invalid", f"attack potential {ans_p!r} is not a number.", see=see)
        if int(p) != potential:
            return CheckResult(exercise, "incorrect", f"attack potential {int(p)} is not right.",
                               "Add the five factor values (elapsed time, expertise, knowledge of the item, "
                               "window of opportunity, equipment) from the Annex G.2 tables.", see)
    if not _is_missing(ans_f):
        f = str(ans_f).strip().title().replace("Very low", "Very Low")
        if f not in iso21434.FEASIBILITY_LEVELS:
            return CheckResult(exercise, "invalid", f"cannot read {ans_f!r} as a feasibility rating.",
                               "Use 'Very Low', 'Low', 'Medium' or 'High'.", see)
        if f != feasibility:
            hint = ("A higher attack potential means a harder attack, so a lower feasibility. "
                    "Map the potential to the four bands of Annex G.2.")
            return CheckResult(exercise, "incorrect", f"feasibility '{f}' is not right.", hint, see)
    return _ok(exercise, "correct.")


def check_risk_value(answer: Any, impact: str, feasibility: str, *, exercise: str = "Risk value",
                     see: str = "05-02 TARA, section 9") -> CheckResult:
    """Check a risk value (1-5) against the ISO/SAE 21434:2021 Annex H example matrix."""
    expected = iso21434.risk_value(impact, feasibility)
    if _is_missing(answer):
        return _missing(exercise)
    num = _number(answer)
    if num is None or num != int(num) or not 1 <= num <= 5:
        return CheckResult(exercise, "invalid", f"{answer!r} is not a risk value.", "Risk values are integers 1-5.", see)
    if int(num) == expected:
        return _ok(exercise, f"correct, {impact} impact with {feasibility} feasibility gives risk value {expected}.")
    return CheckResult(exercise, "incorrect", f"risk value {int(num)} is not right.",
                       _cmp_word(int(num), expected, "risk value")
                       + " Use the row of the impact and the column of the feasibility.", see)


def _cal_value(x: Any):
    if isinstance(x, str):
        s = x.strip().upper().replace("CAL", "").strip()
        if s in ("NONE", "NO", "-", "N/A", ""):
            return "none"
        x = s
    num = _number(x)
    return int(num) if num is not None and num == int(num) and 1 <= num <= 4 else None


def check_cal(answer: Any, impact: str, attack_vector: str, *, exercise: str = "CAL",
              see: str = "05-02 TARA, section 10; 05-01 ISO/SAE 21434 fundamentals, section 2") -> CheckResult:
    """Check a CAL (1-4, or ``"none"`` for negligible impact) against the Annex E example."""
    expected = iso21434.determine_cal(impact, attack_vector)
    if answer is None and expected is None:
        return _missing(exercise)  # None is the "not answered" marker; write "none" for no CAL
    if _is_missing(answer):
        return _missing(exercise)
    got = _cal_value(answer)
    if got is None:
        return CheckResult(exercise, "invalid", f"cannot read {answer!r} as a CAL.",
                           "Write 1, 2, 3, 4 (or 'CAL 3'), or 'none'.", see)
    exp = "none" if expected is None else expected
    if got == exp:
        return _ok(exercise, "correct" + ("." if exp == "none" else f", CAL {exp}."))
    if exp == "none":
        hint = "Look at the impact rating: which impact level receives no CAL?"
    elif got == "none":
        hint = "Only a negligible impact receives no CAL."
    else:
        hint = (_cmp_word(got, exp, "CAL") + " The Annex E example uses impact and *attack vector* "
                "(not the feasibility rating or the risk value).")
    return CheckResult(exercise, "incorrect", f"CAL {got} is not right.", hint, see)


# ---------------------------------------------------------------- SOTIF and validation
def check_rss_distance(answer: Any, v_rear: float, v_front: float, rho: float = 0.5, a_max_accel: float = 2.0,
                       b_min_brake: float = 4.0, b_max_brake: float = 8.0, *, rel_tol: float = 0.01,
                       abs_tol_m: float = 0.05, exercise: str = "RSS safe distance",
                       see: str = "04-05 Criticality metrics and RSS, section 4") -> CheckResult:
    """Check an RSS minimum safe longitudinal distance in metres (speeds in m/s, accelerations in m/s^2)."""
    f = sotif.rss_safe_longitudinal_distance
    expected = f(v_rear, v_front, rho, a_max_accel, b_min_brake, b_max_brake)
    if _is_missing(answer):
        return _missing(exercise)
    num = _number(answer)
    if num is None:
        return CheckResult(exercise, "invalid", f"{answer!r} is not a number (metres).", see=see)
    if _close(num, expected, rel_tol, abs_tol_m):
        return _ok(exercise, f"correct, d_min = {expected:.1f} m.")
    raw = (v_rear * rho + 0.5 * a_max_accel * rho ** 2 + (v_rear + rho * a_max_accel) ** 2 / (2 * b_min_brake)
           - v_front ** 2 / (2 * b_max_brake))
    candidates = [
        (f(v_rear * 3.6, v_front * 3.6, rho, a_max_accel, b_min_brake, b_max_brake),
         "Convert speeds from km/h to m/s (divide by 3.6) before using the formula."),
        (f(v_rear, v_front, rho, 0.0, b_min_brake, b_max_brake),
         "The rear car may still accelerate at a_max during the response time rho; include that term."),
        (f(v_rear, v_front, rho, a_max_accel, b_max_brake, b_min_brake),
         "b_min is the rear car's guaranteed braking, b_max the front car's maximum braking; check which is which."),
        (raw, "The distance cannot be negative: apply [x]+ = max(x, 0)."),
    ]
    hint = next((h for c, h in candidates if _close(num, c, rel_tol, abs_tol_m) and not _close(c, expected, rel_tol, abs_tol_m)),
                "Recompute the four terms: reaction distance, extra distance from accelerating during rho, "
                "rear braking distance from the speed after rho, minus the front braking distance.")
    return CheckResult(exercise, "incorrect", f"{num:.2f} m is not the RSS minimum safe distance.", hint, see)


def check_criticality_metrics(answer: Any, gap_m: float, v_follow: float, v_lead: float, *, rel_tol: float = 0.01,
                              exercise: str = "Criticality metrics",
                              see: str = "04-05 Criticality metrics and RSS, section 2") -> CheckResult:
    """Check any of ``{"TTC": s, "THW": s, "DRAC": m/s^2}`` (``math.inf`` or ``"inf"`` for infinite TTC)."""
    ref = {"TTC": sotif.time_to_collision(gap_m, v_follow, v_lead), "THW": sotif.time_headway(gap_m, v_follow),
           "DRAC": sotif.drac(gap_m, v_follow, v_lead)}
    tips = {"TTC": "TTC = gap / closing speed, and infinite when the follower is not faster than the leader.",
            "THW": "THW = gap / follower speed; it does not depend on the leader's speed.",
            "DRAC": "DRAC = closing speed^2 / (2 gap), and 0 when the vehicles are not closing."}
    if _is_missing(answer) or (isinstance(answer, Mapping) and all(_is_missing(v) for v in answer.values())):
        return _missing(exercise)
    if not isinstance(answer, Mapping):
        return CheckResult(exercise, "invalid", "give a dict such as {'TTC': 3.0, 'THW': 1.2, 'DRAC': 2.5}.", see=see)
    wrong, checked = [], []
    for key, val in answer.items():
        if key not in ref or _is_missing(val):
            continue
        num = _number(val)
        if num is None:
            return CheckResult(exercise, "invalid", f"{key} = {val!r} is not a number.", see=see)
        checked.append(key)
        if not _close(num, ref[key], rel_tol, 1e-9):
            wrong.append(key)
    if not checked:
        return _missing(exercise)
    if wrong:
        return CheckResult(exercise, "incorrect", f"{', '.join(wrong)} not correct.",
                           " ".join(tips[k] for k in wrong), see)
    return _ok(exercise, f"correct ({', '.join(checked)}).")


def check_validation_target(answer: Any, rate: float, confidence: float = 0.95, failures: int = 0, *,
                            rel_tol: float = 0.02, exercise: str = "Validation target",
                            see: str = "04-01 SOTIF fundamentals, section 6") -> CheckResult:
    """Check the exposure needed to show ``rate`` with ``confidence`` after ``failures`` events.

    Uses :func:`avsafety.validation.miles_to_demonstrate` (one-sided Poisson bound); the
    exposure unit is that of ``rate`` (hours, km, miles or encounters).
    """
    expected = validation.miles_to_demonstrate(rate, confidence, failures)
    if _is_missing(answer):
        return _missing(exercise)
    num = _number(answer)
    if num is None:
        return CheckResult(exercise, "invalid", f"{answer!r} is not a number.", see=see)
    if _close(num, expected, rel_tol):
        return _ok(exercise, f"correct, about {expected:.3g} units of exposure.")
    if _close(num, 1 / rate, rel_tol):
        hint = "1/rate is the expected exposure per event; the confidence level adds a factor (about 3 for 95 %)."
    elif _close(num, -math.log(confidence) / rate, rel_tol):
        hint = "Use -ln(1 - C), not -ln(C)."
    elif failures and _close(num, validation.miles_to_demonstrate(rate, confidence, 0), rel_tol):
        hint = "Events were observed: use the chi-square bound with 2(k + 1) degrees of freedom."
    else:
        hint = "n = chi2_C(2(k + 1)) / (2 lambda); for k = 0 this is -ln(1 - C) / lambda."
    return CheckResult(exercise, "incorrect", f"{num:.3g} is not the required exposure.", hint, see)


_AREA = {(True, False): 1, (True, True): 2, (False, True): 3, (False, False): 4}


def _area_number(x: Any):
    s = str(x).strip().lower().replace("area", "").strip()
    num = _number(s)
    return int(num) if num is not None and num == int(num) and 1 <= num <= 4 else None


def check_sotif_area(answer: Any, known: bool, hazardous: bool, *, exercise: str = "SOTIF area",
                     see: str = "04-01 SOTIF fundamentals, section 3") -> CheckResult:
    """Check the ISO 21448:2022 scenario area (1-4) for a known/unknown, hazardous/not hazardous scenario."""
    expected = _AREA[(bool(known), bool(hazardous))]
    if _is_missing(answer):
        return _missing(exercise)
    got = _area_number(answer)
    if got is None:
        return CheckResult(exercise, "invalid", f"cannot read {answer!r} as an area.", "Write 1-4 or 'Area 2'.", see)
    if got == expected:
        return _ok(exercise, f"correct, Area {expected}.")
    hint = ("Areas 1 and 2 are the known scenarios, Areas 3 and 4 the unknown ones."
            if (got <= 2) != bool(known) else "Within the known (or unknown) pair, which area is the hazardous one?")
    return CheckResult(exercise, "incorrect", f"Area {got} is not right.", hint, see)


def check_triggering_condition_table(answer: Any, rows: Iterable[Mapping], required_rate: float, *,
                                     exercise: str = "Triggering-condition table",
                                     see: str = "04-01 SOTIF fundamentals, sections 3, 4 and 7") -> CheckResult:
    """Check the area assigned to each *known* scenario of a triggering-condition register.

    ``rows`` are mappings with ``"id"`` and ``"performance"`` (e.g. a detection rate);
    a known scenario is in Area 1 if its performance meets ``required_rate`` (>=),
    otherwise in Area 2 (known hazardous). ``answer`` maps ids to areas
    (``{"SC-1": "Area 2", ...}`` or ``{"SC-1": 2, ...}``).
    """
    expected = {}
    for r in rows:
        expected[str(r["id"])] = 1 if float(r["performance"]) >= required_rate else 2
    if not expected:
        raise ValueError("rows must not be empty")
    if _is_missing(answer) or (isinstance(answer, Mapping) and all(_is_missing(v) for v in answer.values())):
        return _missing(exercise)
    if not isinstance(answer, Mapping):
        return CheckResult(exercise, "invalid", "give a dict {scenario id: area}.", see=see)
    unread = [k for k, v in answer.items() if not _is_missing(v) and _area_number(v) is None]
    if unread:
        return CheckResult(exercise, "invalid", f"cannot read the area of {', '.join(map(str, unread))}.",
                           "Write 1-4 or 'Area 2'.", see)
    got = {str(k): _area_number(v) for k, v in answer.items() if not _is_missing(v)}
    missing = [k for k in expected if k not in got]
    wrong = sorted(k for k in expected if k in got and got[k] != expected[k])
    if not wrong and not missing:
        return _ok(exercise, f"correct, all {len(expected)} scenarios placed.")
    hints = []
    if wrong:
        if any(got[k] in (3, 4) for k in wrong):
            hints.append("Every scenario in a register is known, so it can only be in Area 1 or Area 2.")
        hints.append(f"Compare each performance with the requirement {required_rate:g} (meeting it means >=).")
    msg = f"{len(expected) - len(wrong) - len(missing)} of {len(expected)} correct"
    if wrong:
        msg += f"; re-check {', '.join(wrong)}"
    if missing:
        msg += f"; not answered: {', '.join(missing)}"
    return CheckResult(exercise, "incorrect", msg + ".", " ".join(hints), see)
