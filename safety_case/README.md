# Safety case as code

The pedestrian AEB assurance case of the course, kept true by CI. Method and walkthrough:
[08-06 Continuous assurance](../08_Standards_Regulation_and_Safety_Case/06_continuous_assurance.ipynb);
current status: [site/safety-case.md](../site/safety-case.md).

| File | Role |
|---|---|
| `aeb_pedestrian.yaml` | GSN argument (goals, strategies, solutions, context, assumptions, justifications), the HARA and TARA entries it is scoped by, and an **acceptance criterion** per solution |
| `evidence/<id>.json` | Evidence records written by the notebooks that compute them (`avsafety.assurance.record_evidence`), with the producing notebook's code hash, timestamp, dataset and licence |

ASIL, PMHF target, permitted decompositions and CAL are computed from the HARA/TARA entries with
`avsafety.iso26262` and `avsafety.iso21434`; use them in texts and criteria as `{SG-01.asil}` or `SG-01.ftti_ms`.

## Commands

```bash
pip install -e ".[assurance]"                         # pyyaml
python scripts/safety_case.py --check                 # integrity: structure, files, schema, freshness (exit 1 on errors)
python scripts/safety_case.py --report                # update site/safety-case.md and site/safety-case.svg
python scripts/safety_case.py --diff OLD_EVIDENCE_DIR  # exit 1 if a claim's status differs from OLD_EVIDENCE_DIR
```

Claim statuses are reported, not enforced: the AEB case honestly evaluates to *do not release*.

## Adding a claim

1. In the producing notebook, add or extend its last code cell:
   `record_evidence("my-id", notebook="<repo-relative path>", dataset=..., licence=..., n=..., metric=value)`.
   Record values the notebook already computes; do not recompute them differently.
2. Execute the notebook (`python scripts/execute_notebooks.py --write <notebook>`); this writes `evidence/my-id.json`.
3. In `aeb_pedestrian.yaml`, add a goal and a solution with `evidence: my-id` and a criterion such as
   `metric_lower_95 >= 0.90` (operators `>= <= > < == != in`, `not in`, joined by `and`; operands are JSON literals,
   other metrics of the record, or derived values). Optional: `refute:` (failed criterion is *inconclusive* unless the
   refutation holds) and `max_age_days:` (age limit, from `data_until` or the recording date).
4. Run `--check` and `--report`, and commit the notebook, the evidence and the page together.

Changing a criterion is changing a safety requirement: review it on its own, with its rationale, never in the same
pull request as the evidence it turns green.
