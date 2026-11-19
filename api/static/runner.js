// Runs Python (Pyodide) and SQL (sql.js) entirely in the browser.
// Nothing is executed on the server, so it's safe and free on Vercel.
const PYODIDE_URL = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/";
const SQLJS_URL = "https://cdn.jsdelivr.net/npm/sql.js@1.8.0/dist/";

function loadScript(src) {
  return new Promise((resolve, reject) => {
    const s = document.createElement("script");
    s.src = src; s.onload = resolve; s.onerror = () => reject(new Error("Could not load " + src + " (check your internet)"));
    document.head.appendChild(s);
  });
}

let _py = null;
async function getPython() {
  if (!_py) {
    _py = (async () => {
      await loadScript(PYODIDE_URL + "pyodide.js");
      return await loadPyodide({ indexURL: PYODIDE_URL });
    })();
  }
  return _py;
}

// Returns {ok, out, err}
async function runPython(code) {
  const py = await getPython();
  const lines = [];
  py.setStdout({ batched: s => lines.push(s) });
  py.setStderr({ batched: s => lines.push(s) });
  const globals = py.globals.get("dict")();
  try {
    await py.runPythonAsync(code, { globals });
    return { ok: true, out: lines.join("\n") };
  } catch (e) {
    let msg = String(e.message || e);
    // keep the useful end of the traceback
    const parts = msg.trim().split("\n");
    const i = parts.findIndex(l => l.includes('File "<exec>"'));
    msg = (i >= 0 ? parts.slice(i) : parts.slice(-3)).join("\n");
    return { ok: false, out: lines.join("\n"), err: msg };
  } finally {
    globals.destroy();
  }
}

let _SQL = null, _sampleSQL = null;
async function getSQL() {
  if (!_SQL) {
    _SQL = (async () => {
      await loadScript(SQLJS_URL + "sql-wasm.js");
      const SQL = await initSqlJs({ locateFile: f => SQLJS_URL + f });
      const res = await fetch("/static/sample_db.sql");
      _sampleSQL = await res.text();
      return SQL;
    })();
  }
  return _SQL;
}

// Fresh practice database each call (so your changes don't stick between runs)
async function freshDB() {
  const SQL = await getSQL();
  const db = new SQL.Database();
  db.run(_sampleSQL);
  return db;
}

// Returns {ok, results:[{columns, values}], err}
async function runSQL(query, db) {
  db = db || await freshDB();
  try {
    return { ok: true, results: db.exec(query) };
  } catch (e) {
    return { ok: false, results: [], err: String(e.message || e) };
  }
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

function resultsToHtml(results) {
  if (!results.length) return '<span class="muted">Query ran. No rows returned.</span>';
  return results.map(r => {
    const head = "<tr>" + r.columns.map(c => "<th>" + escapeHtml(c) + "</th>").join("") + "</tr>";
    const body = r.values.map(row => "<tr>" + row.map(v => "<td>" + (v === null ? "<i>NULL</i>" : escapeHtml(v)) + "</td>").join("") + "</tr>").join("");
    return "<table>" + head + body + "</table><div>" + r.values.length + " row(s)</div>";
  }).join("<br>");
}

// Let Tab insert spaces in code editors
function enableTabs(textarea) {
  textarea.addEventListener("keydown", e => {
    if (e.key === "Tab") {
      e.preventDefault();
      const s = textarea.selectionStart, end = textarea.selectionEnd;
      textarea.value = textarea.value.slice(0, s) + "    " + textarea.value.slice(end);
      textarea.selectionStart = textarea.selectionEnd = s + 4;
    }
  });
}
