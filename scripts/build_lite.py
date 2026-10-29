#!/usr/bin/env python3
"""Build the in-browser edition of the course (JupyterLite + Pyodide, no account, no server).

    pip install -r lite/requirements-lite.txt
    python scripts/build_lite.py                          # build into _build/lite
    python scripts/build_lite.py --list-only              # eligibility report only (no build)
    python scripts/build_lite.py --list-only --sync-page site/run-in-browser.md
    python scripts/build_lite.py --list-only --check-page site/run-in-browser.md

Which notebooks go into the browser build is decided by static analysis of every code cell:

* every imported package must exist in the Pyodide distribution that the pinned
  jupyterlite-pyodide-kernel uses (PyTorch, for instance, does not);
* every ``avsafety.data`` loader a notebook calls is traced (through ``avsafety/data.py``) to the
  hosts it downloads from; a host is usable only if it allows cross-origin requests (``CORS``
  below). A blocked loader inside ``try: ... except D.DataUnavailable`` whose handler does not
  re-raise is tolerated: that section is skipped in the browser;
* no shell commands, unsupported magics or direct network calls;
* notebooks listed in ``lite/exclude.json`` failed when executed in Pyodide and stay on Colab.

The repository notebooks are never modified. The build works on copies: outputs are stripped,
the kernel is set to Pyodide, the standard ``%pip install "avsafety[data] @ git+https://..."``
line becomes ``%pip install "avsafety[data]"`` (served from a wheel built here), notebooks that
download from CORS-enabled hosts get a short prelude that routes urllib through the browser,
remote badge images become plain links, and links to notebooks that are not in the browser build
point to GitHub. A notebook that imports avsafety without the standard install line fails the build.

The Pyodide runtime and the packages the selected notebooks need are self-hosted inside the
output (``static/pyodide``) and the PyPI fallback is disabled, so a loaded page needs no
third-party server: no CDN, no PyPI, no GitHub.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tarfile
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LITE_SRC = ROOT / "lite"
REPO_URL = "https://github.com/milinpatel07/Autonomous-Driving_AI-Safety-and-Security"
BLOB_URL = REPO_URL + "/blob/main/"
#: the deployed site; the book theme routes relative links through its client-side router, so
#: links from the course pages into the browser build are absolute (as for site/tools)
SITE_URL = "https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/"

#: the standard install line of the course notebooks (CONVENTIONS: first code cell)
INSTALL_LINE = re.compile(
    r'^(?P<indent>[ \t]*)%pip install -q "(?P<req>avsafety(?:\[[a-z_,]+\])?) @ git\+'
    + re.escape(REPO_URL) + r'\.git"[ \t]*$')
#: replacement: the same requirement, served from the wheel built into the site
LITE_INSTALL = '%pip install -q "{req}"'
#: other magics that work unchanged in the Pyodide kernel
SIMPLE_PIP = re.compile(r"^%pip install(?: -q)?((?: [A-Za-z0-9_.\-]+)+)\s*$")
HARMLESS_MAGICS = re.compile(r"^%(matplotlib inline|config .*)$")

#: cross-origin (CORS) behaviour of the download hosts, checked with curl from an Origin header
#: (GET, and an OPTIONS pre-flight with "Access-Control-Request-Headers: range") on 29 Oct 2026.
CORS = {
    "s3.eu-central-1.amazonaws.com": (False, "the KITTI bucket sends no Access-Control-Allow-Origin "
                                             "header and refuses the pre-flight for range requests"),
    "static.nhtsa.gov": (False, "the NHTSA file server sends no Access-Control-Allow-Origin header"),
    "data.transportation.gov": (True, "Access-Control-Allow-Origin: *"),
    "api.nhtsa.gov": (True, "Access-Control-Allow-Origin echoes the requesting origin"),
    "storage.googleapis.com": (True, "Access-Control-Allow-Origin: *"),
}
DATASETS = {"s3.eu-central-1.amazonaws.com": "KITTI", "static.nhtsa.gov": "NHTSA crash-report"}
#: optional dependencies that pandas imports only when a method is used (method -> packages)
IMPLICIT = {"style": {"jinja2"}, "to_latex": {"jinja2"}, "to_markdown": {"tabulate"},
            "read_excel": {"openpyxl"}, "to_excel": {"openpyxl"}, "read_parquet": {"pyarrow"}}
#: modules that open network connections directly (bypassing avsafety.data)
DIRECT_NET = {"urllib.request", "requests", "http.client", "socket", "httpx", "aiohttp", "ftplib"}
#: standard-library modules that Pyodide does not provide or cannot use
NO_STDLIB = {"tkinter", "turtle", "turtledemo", "curses", "dbm", "venv", "ensurepip", "idlelib",
             "readline", "subprocess", "multiprocessing", "msvcrt", "winreg", "winsound"}
#: Pyodide packages the kernel itself loads (micropip, IPython, jedi) and avsafety[data] needs
KERNEL_PACKAGES = {"micropip", "packaging", "ipython", "jedi", "numpy", "scipy", "pandas", "pillow"}
#: added for notebooks that download from CORS-enabled hosts (routes urllib through the browser)
ONLINE_PACKAGES = {"pyodide-http"}
ONLINE_PRELUDE = '''# Browser edition: downloads go through the browser; a refused request raises URLError
import urllib.error, urllib.request, pyodide_http
pyodide_http.patch_all()
def _urlopen(*args, _open=urllib.request.urlopen, **kwargs):
    try:
        return _open(*args, **kwargs)
    except urllib.error.URLError:
        raise
    except Exception as exc:
        raise urllib.error.URLError(exc) from None
urllib.request.urlopen = _urlopen

'''
#: files left out of the self-hosted runtime (command-line launchers, type stubs)
PYODIDE_CORE_SKIP = {"python", "python.bat", "python.exe", "python_cli_entry.mjs",
                     "pyodide.d.ts", "ffi.d.ts"}


class BuildError(RuntimeError):
    pass


def _norm(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def _extras() -> dict:
    import tomllib
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    return {extra: {_norm(re.split(r"[ <>=!~;\[]", dep, maxsplit=1)[0]) for dep in deps}
            for extra, deps in project.get("optional-dependencies", {}).items()}


EXTRAS = _extras()


# --------------------------------------------------------------------------- notebook analysis
@dataclass
class Report:
    path: str
    title: str
    module: str
    imports: set = field(default_factory=set)
    packages: set = field(default_factory=set)
    blockers: list = field(default_factory=list)
    notes: list = field(default_factory=list)
    online_hosts: set = field(default_factory=set)
    skipped_hosts: set = field(default_factory=set)
    implicit: dict = field(default_factory=dict)          # package -> pandas method needing it
    uses_avsafety: bool = False
    install_lines: int = 0
    nb: dict = field(default_factory=dict, repr=False)   # the notebook as analysed

    @property
    def eligible(self) -> bool:
        return not self.blockers

    @property
    def tier(self) -> str:
        if not self.eligible:
            return "colab"
        return "online" if self.online_hosts else "offline"


def _hosts_in(node) -> set:
    out = set()
    for n in ast.walk(node):
        if isinstance(n, ast.Constant) and isinstance(n.value, str) and re.match(r"https?://", n.value):
            out.add(urllib.parse.urlparse(n.value).hostname)
    return out


def data_loaders(path: Path = ROOT / "avsafety" / "data.py") -> dict:
    """Map each network-using name in avsafety.data to the hosts it downloads from."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    consts, defs = {}, {}
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for t in targets:
                if isinstance(t, ast.Name):
                    consts[t.id] = _hosts_in(node.value)
        elif isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            defs[node.name] = node
    refs, net, hosts = {}, {}, {}
    for name, node in defs.items():
        refs[name] = {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}
        net[name] = any(isinstance(n, ast.Attribute) and n.attr == "urlopen" for n in ast.walk(node))
        hosts[name] = _hosts_in(node) | set().union(*(consts.get(r, set()) for r in refs[name]))
    changed = True
    while changed:
        changed = False
        for name in defs:
            for r in refs[name] & defs.keys():
                if r == name:
                    continue
                if net[r] and not net[name]:
                    net[name] = changed = True
                if net[r] and not hosts[r] <= hosts[name]:
                    hosts[name] |= hosts[r]
                    changed = True
    return {name: hosts[name] for name in defs if net[name]}


def avsafety_packages(lock: dict) -> set:
    """Pyodide packages that avsafety itself imports (optional imports included when available)."""
    lock_imports, stdlib, out = lock_import_map(lock), set(sys.stdlib_module_names), set()
    for py in (ROOT / "avsafety").glob("*.py"):
        for node in ast.walk(ast.parse(py.read_text(encoding="utf-8"))):
            names = ([a.name for a in node.names] if isinstance(node, ast.Import) else
                     [node.module] if isinstance(node, ast.ImportFrom) and node.level == 0 and node.module
                     else [])
            for top in {n.split(".")[0] for n in names} - stdlib - {"avsafety"}:
                if top in lock_imports:
                    out.add(lock_imports[top])
    return out


def lock_import_map(lock: dict) -> dict:
    out = {}
    for name, pkg in lock["packages"].items():
        for imp in pkg.get("imports", []):
            out.setdefault(imp, name)
    return out


def _mask_magics(src: str, report: Report, pip_packages: set) -> str:
    """Replace IPython magics with ``pass`` so the cell parses; record anything unsupported."""
    lines = src.splitlines()
    if lines and lines[0].startswith("%%"):
        report.blockers.append(f"uses the cell magic `{lines[0].split()[0]}`")
        return ""
    out = []
    for line in lines:
        stripped = line.strip()
        indent = line[: len(line) - len(line.lstrip())]
        if stripped.startswith(("!", "%")):
            if INSTALL_LINE.match(line):
                report.install_lines += 1
                req = INSTALL_LINE.match(line).group("req")
                extras = req[req.index("[") + 1:-1].split(",") if "[" in req else []
                for dep in sorted(set().union(*(EXTRAS.get(e, {f"unknown extra {e}"}) for e in extras))):
                    if dep in pip_packages:
                        report.packages.add(dep)
                    else:
                        report.blockers.append(f"installs avsafety[{','.join(extras)}], which needs {dep}")
            elif SIMPLE_PIP.match(stripped):
                names = SIMPLE_PIP.match(stripped).group(1).split()
                missing = [n for n in names if n.lower() not in pip_packages]
                if missing:
                    report.blockers.append(f"installs {', '.join(missing)} (not available in Pyodide)")
            elif not HARMLESS_MAGICS.match(stripped):
                report.blockers.append(f"runs `{stripped[:60]}` (shell commands and this magic "
                                       "do not work in the browser)")
            out.append(indent + "pass")
        else:
            out.append(line)
    return "\n".join(out)


class _CallFinder(ast.NodeVisitor):
    """Find calls to avsafety.data loaders (noting whether a non-re-raising
    ``except DataUnavailable`` handler protects them) and avsafety imports that
    are not optional (outside ``try: ... except ImportError``)."""

    def __init__(self, loaders: dict):
        self.loaders = loaders
        self.modules = set()     # names bound to the avsafety.data module
        self.funcs = {}          # local name -> loader name
        self.guard = 0
        self.import_guard = 0
        self.needs_avsafety = False
        self.calls = []          # (loader, guarded)
        self.direct = set()      # direct network access

    def visit_Import(self, node):
        for a in node.names:
            if a.name.split(".")[0] == "avsafety" and not self.import_guard:
                self.needs_avsafety = True
            if a.name == "avsafety.data" and a.asname:
                self.modules.add(a.asname)
            if a.name in DIRECT_NET:
                self.direct.add(a.name)

    def visit_ImportFrom(self, node):
        mod = node.module or ""
        if mod.split(".")[0] == "avsafety" and not self.import_guard:
            self.needs_avsafety = True
        for a in node.names:
            if mod == "avsafety" and a.name == "data":
                self.modules.add(a.asname or "data")
            elif mod == "avsafety.data" and a.name in self.loaders:
                self.funcs[a.asname or a.name] = a.name
            if f"{mod}.{a.name}" in DIRECT_NET or mod in DIRECT_NET:
                self.direct.add(mod if mod in DIRECT_NET else f"{mod}.{a.name}")

    def visit_Try(self, node):
        def caught(h):
            return {n.id if isinstance(n, ast.Name) else getattr(n, "attr", "")
                    for n in ast.walk(h.type)} if h.type is not None else {"BaseException"}

        def reraises(h):
            return any(isinstance(n, ast.Raise) for n in ast.walk(h))
        protected = any("DataUnavailable" in caught(h) and not reraises(h) for h in node.handlers)
        optional = any(caught(h) & {"ImportError", "ModuleNotFoundError", "Exception", "BaseException"}
                       for h in node.handlers)
        self.guard += protected
        self.import_guard += optional
        for n in node.body:
            self.visit(n)
        self.guard -= protected
        self.import_guard -= optional
        for n in node.handlers + node.orelse + node.finalbody:
            self.visit(n)

    visit_TryStar = visit_Try

    def visit_Call(self, node):
        f = node.func
        loader = None
        if isinstance(f, ast.Attribute):
            base = f.value
            if isinstance(base, ast.Name) and base.id in self.modules:
                loader = f.attr
            elif (isinstance(base, ast.Attribute) and base.attr == "data"
                  and isinstance(base.value, ast.Name) and base.value.id == "avsafety"):
                loader = f.attr
            if f.attr == "urlopen":
                self.direct.add("urllib.request")
            if (f.attr.startswith("read_") and node.args and isinstance(node.args[0], ast.Constant)
                    and isinstance(node.args[0].value, str) and node.args[0].value.startswith("http")):
                self.direct.add(f"pandas.{f.attr} on a URL")
        elif isinstance(f, ast.Name) and f.id in self.funcs:
            loader = self.funcs[f.id]
        if loader in self.loaders:
            self.calls.append((loader, self.guard > 0))
        self.generic_visit(node)


def analyse(path: Path, lock: dict, loaders: dict, exclude: dict) -> Report:
    nb = json.loads(path.read_text(encoding="utf-8"))
    rel = path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else path.name
    first = "".join(nb["cells"][0]["source"]) if nb["cells"] else ""
    title = next((ln[2:].strip() for ln in first.splitlines() if ln.startswith("# ")), path.stem)
    rep = Report(path=rel, title=title, module=path.parent.name, nb=nb)
    lock_imports = lock_import_map(lock)
    pip_packages = {n.lower() for n in lock["packages"]}
    stdlib = set(sys.stdlib_module_names)
    finder = _CallFinder(loaders)
    for i, cell in enumerate(nb["cells"]):
        if cell["cell_type"] != "code":
            continue
        src = _mask_magics("".join(cell["source"]), rep, pip_packages)
        try:
            tree = ast.parse(src)
        except SyntaxError as exc:
            rep.blockers.append(f"code cell {i} does not parse ({exc.msg})")
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                rep.imports |= {a.name.split(".")[0] for a in node.names}
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                rep.imports.add(node.module.split(".")[0])
            elif isinstance(node, ast.Attribute) and node.attr in IMPLICIT:
                for dep in IMPLICIT[node.attr]:
                    if dep in pip_packages:
                        rep.packages.add(dep)
                        rep.implicit[dep] = node.attr
                    else:
                        rep.blockers.append(f"uses pandas .{node.attr}, which needs {dep} (not in Pyodide)")
            elif (isinstance(node, ast.Attribute) and node.attr == "system"
                  and isinstance(node.value, ast.Call) and getattr(node.value.func, "id", "") == "get_ipython"):
                rep.blockers.append("runs shell commands")
        finder.visit(tree)
    rep.uses_avsafety = finder.needs_avsafety
    for mod in sorted(rep.imports):
        if mod == "avsafety":
            continue
        elif mod in NO_STDLIB:
            rep.blockers.append(f"imports {mod} (not usable in the browser)")
        elif mod in stdlib or mod == "__future__":
            continue
        elif mod in lock_imports:
            rep.packages.add(lock_imports[mod])
        elif mod in ("torch", "torchvision"):
            if "needs PyTorch (no WebAssembly build)" not in rep.blockers:
                rep.blockers.append("needs PyTorch (no WebAssembly build)")
        else:
            rep.blockers.append(f"needs {mod} (not in Pyodide {lock['_version']})")
    for mod in sorted(finder.direct):
        rep.blockers.append(f"downloads directly with {mod}")
    seen = set()
    for loader, guarded in finder.calls:
        if (loader, guarded) in seen:
            continue
        seen.add((loader, guarded))
        hosts = loaders[loader]
        if not hosts:
            rep.blockers.append(f"calls avsafety.data.{loader} (download host unknown)")
        for host in sorted(hosts):
            ok, why = CORS.get(host, (None, "cross-origin access not checked"))
            if ok:
                rep.online_hosts.add(host)
            elif guarded:
                rep.skipped_hosts.add(host)
                rep.notes.append(f"the {loader}() section is skipped in the browser ({host}: {why})")
            else:
                rep.blockers.append(f"downloads from {host} via avsafety.data.{loader}() ({why})")
    if rel in exclude:
        rep.blockers.append(exclude[rel])
    if rep.uses_avsafety and rep.eligible and rep.install_lines == 0:
        raise BuildError(f"{rel} imports avsafety but has no standard install line "
                         f"(expected: {INSTALL_LINE.pattern}); fix the notebook or lite/exclude.json")
    return rep


# --------------------------------------------------------------------------- transformation
_LINK = re.compile(r"(\]\()([^)\s#]+)(#[^)\s]*)?(\))")
#: remote images would make the browser contact third-party hosts; badges become plain links
_BADGE = re.compile(r"\[!\[([^\]]*)\]\(https?://[^)\s]+\)\]\(([^)\s]+)\)")
_REMOTE_IMG = re.compile(r"!\[([^\]]*)\]\((https?://[^)\s]+)\)")


def transform(path: Path, rep: Report, in_build: set) -> dict:
    """Return the browser copy of a notebook (the original file is not touched)."""
    nb = json.loads(json.dumps(rep.nb))
    here = path.parent

    def relink(m):
        target = m.group(2)
        if re.match(r"[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith("/"):
            return m.group(0)
        resolved = (here / urllib.parse.unquote(target)).resolve()
        try:
            rel = resolved.relative_to(ROOT).as_posix()
        except ValueError:
            return m.group(0)
        if rel in in_build:
            return m.group(0)
        return f"{m.group(1)}{BLOB_URL}{rel}{m.group(3) or ''}{m.group(4)}"

    rewrites = 0
    for cell in nb["cells"]:
        src = "".join(cell["source"])
        if cell["cell_type"] == "markdown":
            src = _BADGE.sub(lambda m: "" if m.group(2).startswith(SITE_URL + "lite/")   # badge to itself
                             else f"[{m.group(1)}]({m.group(2)})", src)
            src = _REMOTE_IMG.sub(r"[\1 (image)](\2)", src)
            src = _LINK.sub(relink, src)
        elif cell["cell_type"] == "code":
            lines = src.splitlines(keepends=True)
            found = 0
            for i, line in enumerate(lines):
                m = INSTALL_LINE.match(line.rstrip("\n"))
                if m:
                    lines[i] = (m.group("indent") + LITE_INSTALL.format(req=m.group("req"))
                                + ("\n" if line.endswith("\n") else ""))
                    found += 1
            src = "".join(lines)
            if found and rep.online_hosts and rewrites == 0:
                src = ONLINE_PRELUDE + src
            rewrites += found
            cell["outputs"] = []
            cell["execution_count"] = None
            cell.get("metadata", {}).pop("execution", None)
        cell["source"] = src
    if rewrites != rep.install_lines:
        raise BuildError(f"{rep.path}: rewrote {rewrites} install lines, expected {rep.install_lines}")
    if rep.uses_avsafety and not rewrites:
        raise BuildError(f"{rep.path}: imports avsafety but no install line was rewritten")
    if rep.implicit:
        first = next(c for c in nb["cells"] if c["cell_type"] == "code")
        first["source"] = "".join(
            f"import {dep}  # browser edition: pandas .{attr} needs {dep}, which Pyodide loads on import\n"
            for dep, attr in sorted(rep.implicit.items())) + first["source"]
    nb["metadata"]["kernelspec"] = {"name": "python", "display_name": "Python (Pyodide)", "language": "python"}
    nb["metadata"].pop("widgets", None)
    return nb


# --------------------------------------------------------------------------- downloads
def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(url: str, target: Path, sha256: str | None) -> Path:
    if target.exists() and (sha256 is None or _sha256(target) == sha256):
        return target
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(target.suffix + ".part")
    with urllib.request.urlopen(url, timeout=300) as resp, tmp.open("wb") as out:
        shutil.copyfileobj(resp, out)
    if sha256 and _sha256(tmp) != sha256:
        tmp.unlink()
        raise BuildError(f"checksum mismatch for {url}")
    tmp.replace(target)
    return target


def closure(lock: dict, seeds: set) -> set:
    pkgs = lock["packages"]
    out, pending = set(), list(seeds)
    while pending:
        name = _norm(pending.pop())
        if name in out:
            continue
        if name not in pkgs:
            raise BuildError(f"package {name} is not in pyodide-lock.json")
        out.add(name)
        pending.extend(pkgs[name].get("depends", []))
    return out


def stage_pyodide(dist: dict, lock: dict, packages: set, cache: Path, target: Path) -> int:
    """Self-host the Pyodide core plus only the packages the selected notebooks need."""
    ver = dist["pyodide_version"]
    core = fetch(dist["core_url"].format(version=ver), cache / f"pyodide-core-{ver}.tar.bz2",
                 dist["core_sha256"])
    target.mkdir(parents=True, exist_ok=True)
    with tarfile.open(core) as tar:
        for member in tar.getmembers():
            name = Path(member.name).name
            if member.isfile() and name not in PYODIDE_CORE_SKIP and name != "pyodide-lock.json":
                with tar.extractfile(member) as src, (target / name).open("wb") as dst:
                    shutil.copyfileobj(src, dst)
    cdn = dist["packages_url"].format(version=ver)
    size = 0
    for name in sorted(packages):
        pkg = lock["packages"][name]
        wheel = fetch(f"{cdn}/{pkg['file_name']}", cache / "packages" / pkg["file_name"], pkg["sha256"])
        shutil.copy2(wheel, target / pkg["file_name"])
        size += wheel.stat().st_size
    pruned = dict(lock)
    pruned.pop("_version", None)
    pruned["packages"] = {k: v for k, v in lock["packages"].items() if k in packages}
    (target / "pyodide-lock.json").write_text(json.dumps(pruned, separators=(",", ":")), encoding="utf-8")
    return size


def build_wheels(out: Path, extra: list) -> list:
    out.mkdir(parents=True, exist_ok=True)
    src = out.parent / "avsafety-src"           # build from a copy: setuptools writes build/ in-tree
    shutil.rmtree(src, ignore_errors=True)
    shutil.copytree(ROOT / "avsafety", src / "avsafety", ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copy2(ROOT / "pyproject.toml", src / "pyproject.toml")
    subprocess.run([sys.executable, "-m", "pip", "wheel", "--no-deps", "--no-build-isolation", "-q",
                    "-w", str(out), str(src)], check=True)
    if extra:
        subprocess.run([sys.executable, "-m", "pip", "download", "--no-deps", "--only-binary=:all:",
                        "-q", "-d", str(out), *extra], check=True)
    wheels = sorted(out.glob("*.whl"))
    if not any(w.name.startswith("avsafety-") for w in wheels):
        raise BuildError("the avsafety wheel was not built")
    bad = [w.name for w in wheels if not w.name.endswith("-py3-none-any.whl")]
    if bad:
        raise BuildError(f"browser wheels must be pure Python: {bad}")
    return wheels


# --------------------------------------------------------------------------- page listing
PAGE_START, PAGE_END = "<!-- lite-notebooks:start -->", "<!-- lite-notebooks:end -->"


def short_reason(r: Report) -> str:
    text = " ".join(r.blockers)
    reasons = ["needs PyTorch"] if "PyTorch" in text else []
    for host, name in DATASETS.items():
        if host in text:
            reasons.append(f"{name} data cannot be downloaded from a browser")
    if not reasons and "downloads directly" in text:
        reasons.append("downloads data directly, which the browser edition does not support")
    return "; ".join(reasons) or r.blockers[0]


def page_block(reports: list) -> str:
    rows = [PAGE_START, "", "| Notebook | Runs in the browser |", "|---|---|"]
    for r in reports:
        num = f"{r.module[:2]}-{Path(r.path).name[:2]}"
        if r.eligible:
            link = f"[Open in browser]({SITE_URL}lite/notebooks/index.html?path={urllib.parse.quote(r.path)})"
            extra = " · downloads NGSIM data" if r.online_hosts == {"data.transportation.gov"} else (
                f" · downloads data from {', '.join(sorted(r.online_hosts))}" if r.online_hosts else "")
            rows.append(f"| {num} {r.title} | {link}{extra} |")
        else:
            rows.append(f"| {num} {r.title} | No: {short_reason(r)} |")
    rows += ["", PAGE_END]
    return "\n".join(rows)


def sync_page(page: Path, reports: list, check: bool) -> bool:
    text = page.read_text(encoding="utf-8")
    if PAGE_START not in text or PAGE_END not in text:
        raise BuildError(f"{page} lacks the {PAGE_START} ... {PAGE_END} markers")
    head, rest = text.split(PAGE_START, 1)
    _, tail = rest.split(PAGE_END, 1)
    new = head + page_block(reports) + tail
    if check:
        return new == text
    page.write_text(new, encoding="utf-8")
    return True


# --------------------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--output-dir", type=Path, default=ROOT / "_build" / "lite")
    ap.add_argument("--work-dir", type=Path, default=ROOT / "_build" / "lite-src")
    ap.add_argument("--cache-dir", type=Path, default=Path.home() / ".cache" / "avsafety-lite")
    ap.add_argument("--list-only", action="store_true", help="report eligibility, do not build")
    ap.add_argument("--sync-page", type=Path, help="rewrite the notebook table in this page")
    ap.add_argument("--check-page", type=Path, help="fail if the notebook table in this page is stale")
    args = ap.parse_args()

    dist = json.loads((LITE_SRC / "pyodide.json").read_text(encoding="utf-8"))
    exclude = json.loads((LITE_SRC / "exclude.json").read_text(encoding="utf-8"))
    try:
        from jupyterlite_pyodide_kernel.constants import PYODIDE_VERSION
    except ImportError:
        PYODIDE_VERSION = None
        if not args.list_only:
            raise BuildError("install the pinned build tools: pip install -r lite/requirements-lite.txt")
    if PYODIDE_VERSION and PYODIDE_VERSION != dist["pyodide_version"]:
        raise BuildError(f"lite/pyodide.json pins Pyodide {dist['pyodide_version']} but the installed "
                         f"jupyterlite-pyodide-kernel uses {PYODIDE_VERSION}; update both together")
    ver = dist["pyodide_version"]
    lock_path = fetch(dist["lock_url"].format(version=ver), args.cache_dir / f"pyodide-lock-{ver}.json",
                      dist["lock_sha256"])
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    lock["_version"] = ver

    loaders = data_loaders()
    paths = sorted(ROOT.glob("[0-9][0-9]_*/[0-9][0-9]_*.ipynb"))
    stale = sorted(set(exclude) - {p.relative_to(ROOT).as_posix() for p in paths})
    if stale:
        raise BuildError(f"lite/exclude.json names notebooks that do not exist: {stale}")
    reports = [analyse(p, lock, loaders, exclude) for p in paths]
    chosen = [r for r in reports if r.eligible]

    width = max(len(r.path) for r in reports)
    for r in reports:
        why = "; ".join(r.blockers) if r.blockers else "; ".join(r.notes)
        print(f"{r.tier:8s} {r.path:{width}s}  {why}")
    print(f"\n{len(chosen)} of {len(reports)} notebooks run in the browser "
          f"({sum(r.tier == 'online' for r in chosen)} of them download data).")

    if args.sync_page:
        sync_page(args.sync_page, reports, check=False)
        print(f"updated {args.sync_page}")
    if args.check_page and not sync_page(args.check_page, reports, check=True):
        raise BuildError(f"{args.check_page} is out of date: run "
                         f"python scripts/build_lite.py --list-only --sync-page {args.check_page}")
    if args.list_only:
        return 0

    work, out = args.work_dir.resolve(), args.output_dir.resolve()
    shutil.rmtree(work, ignore_errors=True)
    shutil.rmtree(out, ignore_errors=True)
    (work / "files").mkdir(parents=True)
    in_build = {r.path for r in chosen}
    raw_size = lite_size = 0
    for r in chosen:
        src = ROOT / r.path
        dst = work / "files" / r.path
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(json.dumps(transform(src, r, in_build), indent=1, ensure_ascii=False) + "\n",
                       encoding="utf-8")
        raw_size += src.stat().st_size
        lite_size += dst.stat().st_size

    wheels = build_wheels(work / "wheels", dist.get("extra_wheels", []))
    packages = closure(lock, KERNEL_PACKAGES | avsafety_packages(lock) | set().union(*(r.packages for r in chosen))
                       | (ONLINE_PACKAGES if any(r.tier == "online" for r in chosen) else set()))
    pkg_bytes = stage_pyodide(dist, lock, packages, args.cache_dir, work / "static" / "pyodide")

    shutil.copy2(LITE_SRC / "jupyter-lite.json", work / "jupyter-lite.json")
    config = json.loads((LITE_SRC / "jupyter_lite_config.json").read_text(encoding="utf-8"))
    config.setdefault("PipliteAddon", {})["piplite_urls"] = [str(w) for w in wheels]
    (work / "jupyter_lite_config.json").write_text(json.dumps(config, indent=2), encoding="utf-8")

    subprocess.run([sys.executable, "-m", "jupyter", "lite", "build", "--lite-dir", str(work),
                    "--contents", str(work / "files"), "--output-dir", str(out)], check=True, cwd=work)

    settings = json.loads((out / "jupyter-lite.json").read_text(encoding="utf-8"))
    kernel = settings["jupyter-config-data"]["litePluginSettings"]["@jupyterlite/pyodide-kernel-extension:kernel"]
    if not (kernel.get("pyodideUrl", "").startswith("./static/pyodide/") and kernel.get("disablePyPIFallback")):
        raise BuildError(f"the build does not self-host Pyodide or still falls back to PyPI: {kernel}")
    for r in chosen:
        if not (out / "files" / r.path).exists():
            raise BuildError(f"{r.path} is missing from the build output")

    import jupyterlite_core
    manifest = {
        "jupyterlite_core": jupyterlite_core.__version__,
        "pyodide": ver,
        "python": lock["info"]["python"],
        "pyodide_packages": sorted(packages),
        "wheels": [w.name for w in wheels],
        "notebooks": [{"path": r.path, "title": r.title, "browser": r.eligible, "tier": r.tier,
                       "url": f"notebooks/index.html?path={urllib.parse.quote(r.path)}" if r.eligible else None,
                       "reasons": r.blockers, "notes": r.notes, "hosts": sorted(r.online_hosts),
                       "skipped_hosts": sorted(r.skipped_hosts)}
                      for r in reports],
    }
    (out / "lite-manifest.json").write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    total = sum(p.stat().st_size for p in out.rglob("*") if p.is_file())
    print(f"\nnotebooks: {raw_size / 1e6:.1f} MB with outputs -> {lite_size / 1e6:.1f} MB stripped; "
          f"{len(packages)} Pyodide packages ({pkg_bytes / 1e6:.1f} MB); site {total / 1e6:.0f} MB in {out}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (BuildError, subprocess.CalledProcessError) as exc:
        print(f"build_lite: error: {exc}", file=sys.stderr)
        sys.exit(1)
