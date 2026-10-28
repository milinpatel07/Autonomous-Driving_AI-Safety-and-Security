# Contributing

Thank you for helping to improve this course. Corrections are as valuable as new material: in safety
engineering, a wrong table is worse than a missing one.

## Ways to contribute

- **Report an error or outdated fact**: open a [content issue](https://github.com/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/issues/new/choose) with the file, cell and a verifiable source.
- **Report a notebook that does not run**: open a bug issue with the failing cell and environment.
- **Suggest a topic**: see [ROADMAP.md](ROADMAP.md) for planned topics, then open a topic request.
- **Submit a pull request**: fork, create a branch from `main`, and follow the rules below.

## Repository layout

```
NN_Module_Name/            eight modules, each with a README.md and notebooks NN_topic.ipynb
templates/                 HARA, SOTIF and TARA templates
avsafety/                  tested Python toolkit (normative tables and formulas)
site/                      website pages and interactive browser tools (site/tools/)
scripts/                   check_course.py (linter), execute_notebooks.py
tests/                     pytest suite, including browser-tool parity checks
```

## Notebook conventions

1. **Header**: title, module and position, an *Open in Colab* badge pointing at the file's path on `main`, a
   small table (level, time, prerequisites, standards), author line and learning objectives.
2. **Runs everywhere**: top to bottom on CPU in a few minutes, without dataset downloads (use synthetic data or
   scikit-learn built-ins; wrap optional downloads with an offline fallback). Seed all random generators.
3. **Correct and sourced**: standards are cited with their edition (e.g. ISO 21448:2022). Time-sensitive
   statements say "(as of Month YYYY)" and link a primary source. Invented numbers are labelled
   *Illustrative data*.
4. **Consistent**: normative tables must give the same results as `avsafety` (the tests check the toolkit).
5. **Ends with** key takeaways, self-assessment questions (answers in a collapsible block), references and
   navigation links.
6. British English, calm academic tone.

## Before opening a pull request

```bash
pip install -e ".[test]" -r requirements.txt
pytest -q
python scripts/check_course.py
python scripts/execute_notebooks.py path/to/changed.ipynb
```

To refresh the stored outputs of a notebook you changed, run
`python scripts/execute_notebooks.py --write path/to/changed.ipynb`.

## Code of conduct

Be respectful, constructive and professional. Focus on the content and ideas, not the person.

## Licence

By contributing, you agree that your contributions are licensed under the [MIT Licence](LICENSE).
