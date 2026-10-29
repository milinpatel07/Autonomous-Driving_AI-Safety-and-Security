# Contributing

Thank you for helping to improve this course. Corrections are as valuable as new material: in safety
engineering, a wrong table is worse than a missing one.

## Ways to contribute

- **Report an error or outdated fact**: open a [content issue](https://github.com/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/issues/new/choose) with the file, cell and a verifiable source.
- **Report a notebook that does not run**: open a bug issue with the failing cell and environment.
- **Suggest a topic**: see [ROADMAP.md](ROADMAP.md) for planned topics, then open a topic request.
- **Submit benchmark results**: run `python -m avsafety.bench` on your detector and open a pull request with the result file (see [benchmark/README.md](benchmark/README.md)).
- **Submit a pull request**: fork, create a branch from `main`, and follow the rules below.

## Repository layout

```
NN_Module_Name/            eight modules, each with a README.md and notebooks NN_topic.ipynb
templates/                 HARA, SOTIF and TARA templates
avsafety/                  tested Python toolkit (normative tables, formulas, data loaders, benchmark, safety case)
safety_case/               the pedestrian-AEB safety case as code and its committed evidence
benchmark/                 SOTIF benchmark specification, schema and results
references/                registry of the normative references the course cites
site/                      website pages, observatory and interactive browser tools (site/tools/)
lite/                      configuration of the in-browser edition (JupyterLite)
classroom/                 autograded assignment template (pytest + avsafety.exercises)
paper/                     Journal of Open Source Education paper (paper.md, paper.bib)
scripts/                   linter, notebook execution, README, safety case, leaderboard, references, observatory
tests/                     pytest suite, including browser-tool parity checks
```

## Notebook conventions

1. **Header**: title, module and position, an *Open in Colab* badge pointing at the file's path on `main`, a
   small table (level, prerequisites, standards), author line and learning objectives.
2. **Runs everywhere**: top to bottom on CPU. Use real public data through the `avsafety.data` loaders where the
   result depends on it (they download only what a notebook needs and cache it), and synthetic data, labelled
   *Illustrative data*, where it does not. Seed all random generators.
3. **Correct and sourced**: standards are cited with their edition (e.g. ISO 21448:2022). Time-sensitive
   statements say "(as of Month YYYY)" and link a primary source. Invented numbers are labelled
   *Illustrative data*. Every clause, paragraph or article you cite needs an entry in
   `references/normative.yaml` (see [MAINTAINING.md](MAINTAINING.md)).
4. **Consistent**: normative tables must give the same results as `avsafety` (the tests check the toolkit).
5. **Ends with** key takeaways, self-assessment questions (answers in a collapsible block), references and
   navigation links.
6. British English, calm academic tone.
7. **Auto-checked exercises** use `avsafety.exercises`: answer variables default to `None`, so the cell runs before
   the learner answers, and the checker computes the reference with the toolkit — never hard-code an answer key.
8. **Safety-case evidence**: notebooks that record evidence (`avsafety.assurance.record_evidence`) must be re-run
   after any code change and their `safety_case/evidence/*.json` committed; `python scripts/safety_case.py --check`
   reports stale evidence.

## Before opening a pull request

```bash
pip install -e ".[test,assurance]" -r requirements.txt
pytest -q
python scripts/check_course.py
python scripts/check_references.py --strict
python scripts/safety_case.py --check
python scripts/execute_notebooks.py path/to/changed.ipynb
```

To refresh the stored outputs of a notebook you changed, run
`python scripts/execute_notebooks.py --write path/to/changed.ipynb`. If the notebook is part of the in-browser
edition, also run `python scripts/build_lite.py --list-only --sync-page site/run-in-browser.md`.

## Code of conduct

Be respectful, constructive and professional. Focus on the content and ideas, not the person.

## Licence

By contributing, you agree that your contributions are licensed under the [MIT Licence](LICENSE).
