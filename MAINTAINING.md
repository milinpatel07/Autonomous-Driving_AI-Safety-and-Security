# Maintaining the course

The course cites standards and regulations that change, and downloads data from servers it does not
control. Three automated checks catch most of the decay; this page says what to do when they fire. In addition,
the website workflow (`site.yml`) refreshes the field-safety statistics page from the NHTSA, California DMV and Waymo
files on the 17th of each month and redeploys the site; nothing is committed.

| Check | When | What it does | When it fails |
|---|---|---|---|
| **CI** (`ci.yml`) | every push and pull request | unit tests, course linter, README and reference checks, safety-case integrity and per-module evidence diff, benchmark leaderboard, classroom template, German edition sync, every notebook (warm cache) | the pull request is red |
| **Source watch** (`watch-sources.yml`) | 3rd of each month, or by hand | compares a fingerprint of each watched source (ISO stage codes, EU consolidated versions, UNECE amendment lists, dataset checksums and CSV headers) with `references/fingerprints.json` | one open issue labelled `source-watch` |
| **Canary** (`canary.yml`) | 10th of each month, or by hand | runs every notebook with an empty data cache against the live sources and the newest dependency versions, and checks all external links | one open issue labelled `course-rot` |

Unreachable sources and links (timeouts, sites that refuse automated clients) appear only in the job
summary. They do not open issues.

## Monthly routine

1. After the 3rd and the 10th, look at the open `source-watch` and `course-rot` issues. No issue means
   nothing changed and nothing broke.
2. Skim the job summaries of both runs for sources and links that were unreachable two months in a row;
   check those by hand and either fix the URL or add the host to `BOT_BLOCKING` in `scripts/check_links.py`.
3. Run `python scripts/check_references.py` locally and clear any new warnings.

## Handling a watch issue

The issue lists each changed source, what its fingerprint said before and now, and the files that cite it.

1. Find out what changed:
   - **ISO stage code** (e.g. a successor moved from DIS 40.20 to FDIS 50.00 or was published 60.60):
     a new edition is coming or out. Record the stage in the document's `edition`. When the new edition
     is published, check every entry of that document against the new table of contents.
   - **EU act** (new amending act or consolidated version): open the amending act on EUR-Lex and check
     the cited articles and annexes; update dates and wording in the notebooks.
   - **UNECE list** (new supplement, series or revision): check whether the cited paragraphs moved — the
     R157 01 series, for example, swapped paragraphs 5.5.1 and 5.5.2.
   - **Dataset** (new checksum, header or row count): run the notebooks that cite it with a cold cache:
     `AVSAFETY_CACHE=$(mktemp -d) python scripts/execute_notebooks.py <notebooks>`.
2. Update `references/normative.yaml` and the notebooks (next section).
3. Accept the new fingerprints: download the `fingerprints-<run id>` artifact of the run and replace
   `references/fingerprints.json` with its `fingerprints.new.json`, or run
   `python scripts/watch_sources.py --update` locally. Commit, and close the issue with a short note of
   what changed.

## Handling a canary issue

The issue names the failing modules (with the last lines of the log) and the broken links. The
`versions.txt` artifact lists the package versions that were used.

- **A dependency broke a notebook:** fix the code, or set an upper bound in `requirements.txt` with a comment
  saying why, and open a follow-up issue to remove it.
- **A data source moved or changed format:** fix the loader in `avsafety/data.py` and its unit test.
- **A link is broken:** replace it with the new address or an archived copy (web.archive.org) and keep
  the access date in the reference.

The canary comments on the open issue when a later run passes; close it once the fix is merged.

## Updating a reference

Every clause, paragraph, table, annex or article that the course cites has an entry in
`references/normative.yaml`: what the course states, the source and how it was verified
(`official-text`, `official-summary`, `secondary` or `unverified`, with the date checked).

```bash
python scripts/check_references.py                  # warnings for unregistered citations and unverified entries
python scripts/check_references.py --strict         # what CI runs: unregistered citations fail
python scripts/check_references.py --update-used-in --index   # refresh used_in and site/references.md
```

- **New citation:** add an entry (copy a neighbour), cite the edition the notebook follows, and verify it
  against the primary text where it is public (UNECE PDFs, EUR-Lex, gesetze-im-internet.de) or against the
  official table of contents for paywalled standards. If you cannot verify it, say `unverified` and word the
  notebook cautiously.
- **Facts that must agree across notebooks** (a limit cited with a paragraph number) get a `fact` pattern;
  the checker fails if any notebook cites that fact with another paragraph. Paragraph numbers of earlier
  editions go into `superseded_locators`.
- `used_in` is computed: never edit it by hand.

## Releases and versions

The course uses semantic versions, independent of the `avsafety` package version in `pyproject.toml`:

- **major** — notebooks or modules renumbered, renamed or removed (links into the course break);
- **minor** — new notebooks, pages, tools or toolkit functions;
- **patch** — corrections, updated facts and references, dependency fixes.

To release:

1. Move the entries under *Unreleased* in `CHANGELOG.md` to a new heading `## [X.Y.Z] — YYYY-MM-DD`.
2. Set `version` and `date-released` in `CITATION.cff` (and the toolkit version in `pyproject.toml` if the
   toolkit changed). Run the full check: `pytest -q`, `python scripts/check_course.py`,
   `python scripts/check_references.py --strict`.
3. Commit, tag `vX.Y.Z` and publish a GitHub release whose notes are the changelog section.

**Zenodo DOI (one-time set-up by the repository owner).** Sign in at <https://zenodo.org> with the GitHub
account that owns the repository, open *Account → GitHub*, and switch the repository on. From then on
every published GitHub release is archived on Zenodo and receives its own DOI; the *concept DOI* shown on
the Zenodo record always resolves to the latest version. Zenodo reads the title, authors and licence from
`CITATION.cff`. After the first archived release, add the concept DOI to `CITATION.cff` (`doi:`) and as a
badge in `README.md`.

## Adding a notebook

1. Name it `NN_topic.ipynb` in its module folder and follow the header, *In industry*, takeaways,
   self-assessment, references and navigation format of the neighbouring notebooks (see `CONTRIBUTING.md`).
   Update "Notebook N of M" and the navigation links of the other notebooks in the module.
2. Use the `avsafety.data` loaders for real data and state the dataset licence; label synthetic numbers
   *Illustrative data*.
3. Register every clause or paragraph it cites in `references/normative.yaml`.
4. Add it to the table of contents in `myst.yml`, regenerate the module README
   (`python scripts/build_readmes.py`) and store outputs:
   `python scripts/execute_notebooks.py --write <notebook>`.
5. Before the pull request: `pytest -q`, `python scripts/check_course.py`,
   `python scripts/check_references.py --strict`; add a line under *Unreleased* in `CHANGELOG.md`.
