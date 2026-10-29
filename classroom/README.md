# Autograded assignment template

A minimal, working starter repository for graded exercises with this course. Students answer eight questions
on HARA, FMEDA, TARA, RSS and SOTIF validation in `answers.py`; pytest checks each answer with
`avsafety.exercises`, which computes the reference value from the course toolkit, so there is no answer key to
maintain or leak. The repository CI grades `reference_answers.py` and the empty template on every change, so the
template cannot break silently.

| File | Purpose |
|---|---|
| `assignment/` | Contents of the starter repository students receive |
| `assignment/problem.py` | The questions and their parameters: **change these each term** |
| `assignment/answers.py` | Answer variables, all `None` at the start |
| `assignment/test_answers.py` | One pytest test (one point) per question |
| `assignment/.github/workflows/check.yml` | Runs the checks on every push, so students get feedback |
| `classroom50-tests.json` | Autograder definition for Classroom 50 |
| `reference_answers.py` | Correct answers computed from `problem.py`; for CI only, not for students |

## Running an assignment

GitHub Classroom was retired on 28 August 2026 ([GitHub changelog](https://github.blog/changelog/2026-08-27-github-classroom-deprecated); [closing-down notice](https://github.com/orgs/community/discussions/205975)).
Two routes fit this template (as of October 2026):

1. **Classroom 50** ([foundation50/classroom50](https://github.com/foundation50/classroom50)), the open-source
   successor named in GitHub's notice. It needs a GitHub organisation on the Team or Enterprise plan (Team is
   free for verified teachers through GitHub Education). Copy `assignment/` into a template repository, create the
   assignment with it as starter code, and load `classroom50-tests.json` as the autograder (`gh teacher assignment
   test set --tests …`; see the Classroom 50 wiki page *Autograding Basics*). Points are split across the pytest
   cases, so each question is worth one point; scores export as CSV.
2. **Any GitHub organisation without a classroom tool**: make `assignment/` a template repository and give each
   student a private copy. `check.yml` gives feedback on every push. Because students can edit any file in their
   copy, grade by running the original `problem.py` and `test_answers.py` against each student's `answers.py`
   (set `AVSAFETY_ANSWERS` to its path), at the last commit before the deadline.

Pin the toolkit in `assignment/requirements.txt` to the release you tested (replace `@main` by the tag), so that a
later toolkit change cannot alter grades during a term. Before releasing a new problem set, run from the
repository root:

```bash
AVSAFETY_ANSWERS=classroom/reference_answers.py python -m pytest -q classroom/assignment   # all pass
python -m pytest -q classroom/assignment                                                   # all fail
```

Students can compute every answer with the toolkit; that is intended practice, not a loophole. Weight these
checks as formative (see [teaching guide](../site/teaching.md)) and assess judgement in the HARA/TARA project.
