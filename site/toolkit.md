---
title: The avsafety toolkit
---

`avsafety` collects the normative tables and formulas used throughout the course in one small, tested Python
package. The notebooks stay self-contained for Colab, but every table they define gives the same results as the
toolkit, and the browser tools are checked against it in CI.

```bash
pip install "git+https://github.com/milinpatel07/Autonomous-Driving_AI-Safety-and-Security.git"
```

```python
from avsafety import iso26262, iso21434, sotif, validation, uq, coverage

iso26262.determine_asil("S3", "E4", "C2")           # 'C'
iso26262.decomposition_options("D")                 # [('C(D)', 'A(D)'), ('B(D)', 'B(D)'), ('D(D)', 'QM(D)')]
iso21434.risk_value("Severe", "Medium")             # 4
iso21434.determine_cal("Major", "Network")          # 4
iso21434.cvss31_base_score("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H")  # 9.8
sotif.rss_safe_longitudinal_distance(25.0, 20.0)     # metres
validation.miles_to_demonstrate(1.09e-8, 0.95)       # ≈ 2.75e8 miles (Kalra & Paddock, 2016)
```

| Module | Contents | Source |
|---|---|---|
| `iso26262` | ASIL table, decomposition, SPFM / LFM / PMHF | ISO 26262-3/-5/-9:2018 |
| `iso21434` | attack potential, feasibility, risk value, CAL, CVSS v3.1 | ISO/SAE 21434:2021 Annexes E, G, H; FIRST CVSS v3.1 |
| `sotif` | TTC, THW, DRAC, RSS safe distance | Shalev-Shwartz et al. 2017 |
| `validation` | zero-failure miles, Poisson confidence bounds | Kalra & Paddock 2016 |
| `uq` | ECE, Brier, NLL, temperature scaling, split conformal | Guo et al. 2017; Angelopoulos & Bates 2021 |
| `coverage` | n-wise scenario / ODD coverage | ISO 34502:2022, ISO 34503:2023 |

:::{note}
ISO/SAE 21434 Annexes E, G and H are informative; organisations may define their own rating schemes. The toolkit
implements the examples given in the standard and is a teaching aid, not a substitute for the standards.
:::
