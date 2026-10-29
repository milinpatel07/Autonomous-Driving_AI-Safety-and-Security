"""Offline tests for the notebook selection and transformation of scripts/build_lite.py."""
import importlib.util
import json
import sys
from pathlib import Path

import pytest

pytest.importorskip("tomllib")  # the build script needs Python >= 3.11

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("build_lite", ROOT / "scripts" / "build_lite.py")
B = importlib.util.module_from_spec(spec)
sys.modules["build_lite"] = B          # dataclasses look the module up while it is executed
spec.loader.exec_module(B)

INSTALL = ('try:\n    import avsafety\nexcept ImportError:\n'
           f'    %pip install -q "avsafety[data] @ git+{B.REPO_URL}.git"\n'
           '    import avsafety\nfrom avsafety import data as D\n')
LOCK = {"_version": "test", "info": {"python": "3.14"}, "packages": {
    name: {"imports": [imp], "depends": deps, "file_name": f"{name}.whl"}
    for name, imp, deps in [("numpy", "numpy", []), ("pandas", "pandas", ["numpy"]),
                            ("pillow", "PIL", []), ("jinja2", "jinja2", [])]}}


def notebook(tmp_path, *cells, name="nb.ipynb"):
    nb = {"cells": [{"cell_type": "markdown", "metadata": {}, "source": "# Title"}]
          + [{"cell_type": "code", "metadata": {}, "execution_count": 3, "outputs": [{"output_type": "stream"}],
              "source": c} for c in cells],
          "metadata": {"kernelspec": {"name": "python3"}}, "nbformat": 4, "nbformat_minor": 5}
    path = tmp_path / name
    path.write_text(json.dumps(nb))
    return path


def report(path):
    return B.analyse(path, LOCK, B.data_loaders(), {})


def test_offline_notebook_is_rewritten(tmp_path):
    rep = report(notebook(tmp_path, INSTALL + "import pandas as pd\nD.attribution('KITTI')"))
    assert rep.tier == "offline" and rep.packages == {"pandas", "pillow"}
    nb = B.transform(tmp_path / "nb.ipynb", rep, set())
    code = nb["cells"][1]
    assert '%pip install -q "avsafety[data]"' in code["source"] and "git+" not in code["source"]
    assert code["outputs"] == [] and code["execution_count"] is None
    assert nb["metadata"]["kernelspec"]["name"] == "python"


def test_blocked_sources_and_packages(tmp_path):
    rep = report(notebook(tmp_path, INSTALL + "import torch\nf = D.kitti_object(0)"))
    assert not rep.eligible
    assert any("PyTorch" in b for b in rep.blockers)
    assert any("s3.eu-central-1.amazonaws.com" in b for b in rep.blockers)


def test_guarded_blocked_loader_is_skipped_but_reraise_is_not(tmp_path):
    ok = report(notebook(tmp_path, INSTALL + "try:\n    D.nhtsa_sgo()\nexcept D.DataUnavailable:\n    pass"))
    assert ok.eligible and ok.skipped_hosts == {"static.nhtsa.gov"}
    bad = report(notebook(tmp_path, INSTALL + "try:\n    D.nhtsa_sgo()\nexcept D.DataUnavailable:\n"
                                              "    raise SystemExit('needed')", name="b.ipynb"))
    assert not bad.eligible


def test_cors_enabled_source_is_online(tmp_path):
    rep = report(notebook(tmp_path, INSTALL + "df = D.ngsim('us-101')"))
    assert rep.tier == "online" and rep.online_hosts == {"data.transportation.gov"}
    assert B.transform(tmp_path / "nb.ipynb", rep, set())["cells"][1]["source"].startswith(B.ONLINE_PRELUDE)


def test_pandas_styler_preloads_jinja2(tmp_path):
    rep = report(notebook(tmp_path, "import pandas as pd\npd.DataFrame().style"))
    assert rep.eligible and "jinja2" in rep.packages
    assert B.transform(tmp_path / "nb.ipynb", rep, set())["cells"][1]["source"].startswith("import jinja2")


def test_avsafety_without_install_line_fails_loudly(tmp_path):
    with pytest.raises(B.BuildError):
        report(notebook(tmp_path, "from avsafety import sotif"))
    optional = notebook(tmp_path, "try:\n    from avsafety import sotif\nexcept ImportError:\n    pass",
                        name="o.ipynb")
    assert report(optional).eligible


def test_shell_commands_are_not_eligible(tmp_path):
    assert not report(notebook(tmp_path, "!ls")).eligible
