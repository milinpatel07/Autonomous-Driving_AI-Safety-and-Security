#!/usr/bin/env node
// Headless smoke test of the in-browser edition built by scripts/build_lite.py.
//
//   node scripts/test_lite.mjs                       # the three representative notebooks
//   node scripts/test_lite.mjs --all                 # every notebook in the browser build
//   node scripts/test_lite.mjs --all --offline-only --jobs 3   # CI: no third-party hosts, 3 tabs
//   node scripts/test_lite.mjs --site _build/lite 05_Cybersecurity_ISO21434/02_tara.ipynb
//
// Serves the built site from a local static server, opens each notebook through the same URL the
// course pages link to (notebooks/index.html?path=...), runs all cells in the Pyodide kernel and
// fails on any error output or unexecuted cell. Offline notebooks must not contact any host other
// than the local server; notebooks that download data may reach only the hosts listed in
// lite-manifest.json. Needs Playwright with Chromium (npm install playwright && npx playwright install chromium).

import { createServer } from "node:http";
import { createReadStream, existsSync, readFileSync, statSync } from "node:fs";
import { createRequire } from "node:module";
import { dirname, extname, join, normalize, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const DEFAULT = [
  "03_Functional_Safety_ISO26262/02_hara.ipynb",
  "05_Cybersecurity_ISO21434/02_tara.ipynb",
  "04_SOTIF_ISO21448/05_criticality_metrics_and_rss.ipynb",
];
const TYPES = {
  ".html": "text/html", ".js": "text/javascript", ".mjs": "text/javascript", ".css": "text/css",
  ".json": "application/json", ".ipynb": "application/json", ".wasm": "application/wasm",
  ".svg": "image/svg+xml", ".png": "image/png", ".ico": "image/x-icon", ".woff2": "font/woff2",
  ".woff": "font/woff", ".ttf": "font/ttf", ".zip": "application/zip", ".whl": "application/zip",
  ".webmanifest": "application/manifest+json", ".txt": "text/plain",
};

function parseArgs(argv) {
  const opts = { site: join(ROOT, "_build", "lite"), timeout: 900, all: false, offline: false, jobs: 1, paths: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--site") opts.site = resolve(argv[++i]);
    else if (a === "--timeout") opts.timeout = Number(argv[++i]);
    else if (a === "--all") opts.all = true;
    else if (a === "--offline-only") opts.offline = true;
    else if (a === "--jobs") opts.jobs = Math.max(1, Number(argv[++i]));
    else opts.paths.push(a);
  }
  return opts;
}

function loadPlaywright() {
  const require = createRequire(import.meta.url);
  const bases = [ROOT, ...(process.env.NODE_PATH || "").split(":").filter(Boolean)];
  for (const base of bases) {
    try {
      return require(require.resolve("playwright", { paths: [base] }));
    } catch { /* try the next location */ }
  }
  throw new Error("Playwright not found: npm install playwright && npx playwright install chromium");
}

function serve(dir) {
  const server = createServer((req, res) => {
    const url = new URL(req.url, "http://localhost");
    let file = normalize(join(dir, decodeURIComponent(url.pathname)));
    if (!file.startsWith(dir)) { res.writeHead(403).end(); return; }
    if (existsSync(file) && statSync(file).isDirectory()) file = join(file, "index.html");
    if (!existsSync(file)) { res.writeHead(404).end(); return; }
    res.writeHead(200, {
      "Content-Type": TYPES[extname(file)] || "application/octet-stream",
      "Content-Length": statSync(file).size,
    });
    createReadStream(file).pipe(res);
  });
  return new Promise((ok) => server.listen(0, "127.0.0.1", () => ok(server)));
}

async function runNotebook(browser, base, entry) {
  const context = await browser.newContext();
  const page = await context.newPage();
  const allowed = new Set(entry.hosts);
  const expectedFail = new Set(entry.skipped_hosts || []);   // sections that skip themselves
  const blocked = new Set();
  const missing = new Set();
  await context.route("**/*", (route) => {
    const host = new URL(route.request().url()).hostname;
    if (host === "127.0.0.1" || allowed.has(host)) return route.continue();
    if (!expectedFail.has(host)) blocked.add(host);
    return route.abort();
  });
  let bytes = 0;
  page.on("response", (r) => {
    if (r.status() === 404 && r.url().startsWith(base)) missing.add(r.url().slice(base.length));
    bytes += Number(r.headers()["content-length"] || 0);
  });
  const t0 = Date.now();
  await page.goto(`${base}/${entry.url}`);
  await page.waitForFunction(() => {
    const w = window.jupyterapp?.shell?.currentWidget;
    return w?.sessionContext?.session?.kernel && w.content?.model?.cells?.length > 0;
  }, null, { timeout: 120_000 });
  const result = await page.evaluate(async () => {
    const app = window.jupyterapp;
    const panel = app.shell.currentWidget;
    await panel.context.ready;
    await panel.sessionContext.ready;
    await panel.sessionContext.session.kernel.info;          // Pyodide loaded, kernel started
    const tRun = performance.now();
    await app.commands.execute("notebook:run-all-cells");
    while (panel.sessionContext.session.kernel.status !== "idle") {
      await new Promise((r) => setTimeout(r, 250));
    }
    const runS = (performance.now() - tRun) / 1000;
    const errors = [];
    let unexecuted = 0;
    let code = 0;
    const cells = panel.content.model.cells;
    for (let i = 0; i < cells.length; i++) {
      const cell = cells.get(i);
      if (cell.type !== "code") continue;
      code++;
      if (cell.executionCount == null) unexecuted++;
      for (const out of cell.outputs.toJSON()) {
        if (out.output_type === "error") {
          errors.push({ cell: i, ename: out.ename, evalue: String(out.evalue).slice(0, 300) });
        }
      }
    }
    return { runS, errors, unexecuted, code };
  });
  result.totalS = (Date.now() - t0) / 1000;
  result.mb = bytes / 1e6;
  result.blocked = [...blocked];
  result.missing = [...missing];
  await context.close();
  return result;
}

async function main() {
  const opts = parseArgs(process.argv.slice(2));
  const manifestPath = join(opts.site, "lite-manifest.json");
  if (!existsSync(manifestPath)) throw new Error(`${manifestPath} not found: run scripts/build_lite.py first`);
  const manifest = JSON.parse(readFileSync(manifestPath, "utf8"));
  const inBuild = new Map(manifest.notebooks.filter((n) => n.browser).map((n) => [n.path, n]));
  let paths = opts.all ? [...inBuild.keys()] : (opts.paths.length ? opts.paths : DEFAULT);
  if (opts.offline) paths = paths.filter((p) => inBuild.get(p)?.tier !== "online");
  for (const p of paths) if (!inBuild.has(p)) throw new Error(`${p} is not in the browser build`);

  const { chromium } = loadPlaywright();
  const server = await serve(resolve(opts.site));
  const base = `http://127.0.0.1:${server.address().port}`;
  const browser = await chromium.launch();
  let failures = 0;
  const check = async (p) => {
    const entry = inBuild.get(p);
    let r;
    try {
      r = await Promise.race([
        runNotebook(browser, base, entry),
        new Promise((_, no) => setTimeout(() => no(new Error(`timeout after ${opts.timeout} s`)), opts.timeout * 1000)),
      ]);
    } catch (err) {
      failures++;
      console.log(`FAIL ${p}: ${err.message}`);
      return;
    }
    const problems = [];
    if (r.errors.length) problems.push(...r.errors.map((e) => `cell ${e.cell}: ${e.ename}: ${e.evalue}`));
    if (r.unexecuted) problems.push(`${r.unexecuted} of ${r.code} code cells did not run`);
    if (r.blocked.length) problems.push(`contacted hosts outside the build: ${r.blocked.join(", ")}`);
    if (r.missing.length) problems.push(`missing files: ${r.missing.join(", ")}`);
    const timing = `${r.code} cells, run ${r.runS.toFixed(1)} s, total ${r.totalS.toFixed(1)} s, `
      + `${r.mb.toFixed(0)} MB loaded`;
    if (problems.length) {
      failures++;
      console.log(`FAIL ${p} (${timing})\n  ${problems.join("\n  ")}`);
    } else {
      console.log(`ok   ${p} (${timing})`);
    }
  };
  const queue = [...paths];
  try {
    await Promise.all(Array.from({ length: Math.min(opts.jobs, queue.length) }, async () => {
      while (queue.length) await check(queue.shift());
    }));
  } finally {
    await browser.close();
    server.close();
  }
  console.log(`${paths.length - failures} of ${paths.length} notebooks ran without errors in Pyodide ${manifest.pyodide}`);
  process.exit(failures ? 1 : 0);
}

main().catch((err) => { console.error(err.message); process.exit(1); });
