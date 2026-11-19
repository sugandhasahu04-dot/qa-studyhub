// Animated / interactive diagrams (dual coding: words + pictures).
// In a lesson, write:  <div class="viz" data-viz="groupby"></div>
(function () {
  const esc = s => String(s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const sleep = ms => new Promise(r => setTimeout(r, ms));

  function shell(el, title, hint) {
    el.innerHTML = `<div class="viz-head"><strong>🎬 ${esc(title)}</strong>${hint ? `<span class="muted small">${esc(hint)}</span>` : ''}</div>
      <div class="viz-stage"></div><div class="viz-cap"></div><div class="viz-ctl row"></div>`;
    return { stage: el.querySelector('.viz-stage'), cap: el.querySelector('.viz-cap'), ctl: el.querySelector('.viz-ctl') };
  }
  function button(ctl, label, fn, primary) {
    const b = document.createElement('button');
    b.className = 'btn small' + (primary ? ' primary' : '');
    b.textContent = label; b.onclick = fn; ctl.appendChild(b); return b;
  }
  // Generic "stepper": steps = [{caption, render()}]
  function stepper(ctl, cap, steps, opts = {}) {
    let i = -1, playing = false;
    const back = button(ctl, '◀ Back', () => show(i - 1));
    const next = button(ctl, 'Next ▶', () => show(i + 1), true);
    const play = button(ctl, '▶ Play all', async () => {
      if (playing) return; playing = true; play.disabled = true;
      for (let k = 0; k < steps.length; k++) { show(k); await sleep(opts.delay || 1800); }
      playing = false; play.disabled = false;
    });
    function show(k) {
      if (k < 0 || k >= steps.length) return;
      i = k; steps[k].render(); cap.innerHTML = `<span class="pill">${k + 1}/${steps.length}</span> ${steps[k].caption}`;
      back.disabled = k === 0; next.disabled = k === steps.length - 1;
    }
    show(0);
    return show;
  }

  // ---------- 1. Cycle diagrams (SDLC, STLC, Scrum) ----------
  function cycle(el, title, items, center) {
    const { stage, cap, ctl } = shell(el, title, 'Tap a step');
    const n = items.length, W = 340, H = 300, cx = 170, cy = 150, R = 112;
    const pos = items.map((_, i) => { const a = -Math.PI / 2 + i * 2 * Math.PI / n; return [cx + R * Math.cos(a), cy + R * Math.sin(a)]; });
    let svg = `<svg viewBox="0 0 ${W} ${H}" class="viz-svg"><defs><marker id="ah-${title.length}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="v-arrowhead"/></marker></defs>`;
    svg += `<circle cx="${cx}" cy="${cy}" r="${R}" class="v-ring"/>`;
    svg += `<text x="${cx}" y="${cy - 4}" class="v-center" text-anchor="middle">${esc(center[0])}</text><text x="${cx}" y="${cy + 16}" class="v-center-sub" text-anchor="middle">${esc(center[1] || '')}</text>`;
    items.forEach((it, i) => {
      const [x, y] = pos[i];
      svg += `<g class="v-node" data-i="${i}" style="cursor:pointer"><circle cx="${x}" cy="${y}" r="27"/><text x="${x}" y="${y - 3}" text-anchor="middle" class="v-emoji">${it.icon}</text><text x="${x}" y="${y + 13}" text-anchor="middle" class="v-label">${esc(it.short)}</text></g>`;
    });
    svg += `<g class="v-dot"><circle r="7"/></g></svg>`;
    stage.innerHTML = svg;
    const nodes = stage.querySelectorAll('.v-node'), dot = stage.querySelector('.v-dot');
    function show(i) {
      nodes.forEach((g, j) => g.classList.toggle('active', j === i));
      const [x, y] = pos[i];
      dot.style.transform = `translate(${x + 20}px, ${y - 20}px)`;
      cap.innerHTML = `<strong>${i + 1}. ${esc(items[i].name)}</strong> – ${items[i].desc}`;
    }
    nodes.forEach(g => g.onclick = () => show(+g.dataset.i));
    let k = 0, timer = null;
    const playBtn = button(ctl, '▶ Play cycle', () => {
      if (timer) { clearInterval(timer); timer = null; playBtn.textContent = '▶ Play cycle'; return; }
      playBtn.textContent = '⏸ Pause';
      timer = setInterval(() => { k = (k + 1) % n; show(k); }, 1700);
    }, true);
    show(0);
  }

  const VIZ = {};

  VIZ.sdlc = el => cycle(el, 'SDLC – how software is built', [
    { icon: '📝', short: 'Require', name: 'Requirements', desc: 'Client says what they want: "Users log in with email + OTP".' },
    { icon: '📐', short: 'Design', name: 'Design', desc: 'Team plans screens, database tables and architecture.' },
    { icon: '👩‍💻', short: 'Code', name: 'Development', desc: 'Developers write the code for the login page.' },
    { icon: '🧪', short: 'Test', name: 'Testing ⭐ (you!)', desc: 'You test login with right/wrong OTP, log bugs, re-test fixes.' },
    { icon: '🚀', short: 'Deploy', name: 'Deployment', desc: 'Software goes live for real users.' },
    { icon: '🔧', short: 'Maintain', name: 'Maintenance', desc: 'Fix bugs, add features – and the cycle starts again.' },
  ], ['SDLC', 'repeats every release']);

  VIZ.stlc = el => cycle(el, 'STLC – the tester\'s own cycle', [
    { icon: '🔍', short: 'Analyse', name: 'Requirement analysis', desc: 'Read requirements, ask questions, find what can be tested.' },
    { icon: '🗺️', short: 'Plan', name: 'Test planning', desc: 'Decide scope, tools, people, timeline → Test Plan.' },
    { icon: '✍️', short: 'Design', name: 'Test case design', desc: 'Write test cases + test data (positive and negative).' },
    { icon: '🖥️', short: 'Setup', name: 'Environment setup', desc: 'Test server, logins and data ready.' },
    { icon: '▶️', short: 'Execute', name: 'Test execution', desc: 'Run tests, mark Pass/Fail, log bugs, re-test fixes.' },
    { icon: '📊', short: 'Close', name: 'Test closure', desc: 'Summary report: passed, failed, open bugs, lessons learned.' },
  ], ['STLC', 'inside the Testing phase']);

  VIZ.sprint = el => cycle(el, 'A Scrum sprint (usually 2 weeks)', [
    { icon: '📚', short: 'Backlog', name: 'Product Backlog', desc: 'Product Owner keeps the ordered list of everything to build.' },
    { icon: '🎯', short: 'Planning', name: 'Sprint Planning', desc: 'Team picks stories for this sprint. Testers estimate test effort and ask about acceptance criteria.' },
    { icon: '🗣️', short: 'Daily', name: 'Daily Stand-up (every day)', desc: '15 min: yesterday, today, blockers. Development and TESTING happen during the sprint.' },
    { icon: '🎬', short: 'Review', name: 'Sprint Review', desc: 'Team demos tested, working features to stakeholders.' },
    { icon: '🔁', short: 'Retro', name: 'Retrospective', desc: 'What went well? What to improve next sprint?' },
  ], ['Sprint', '2 weeks, repeat']);

  // ---------- 2. Bug life cycle ----------
  VIZ.buglife = el => {
    const { stage, cap, ctl } = shell(el, 'Bug life cycle', 'Choose a story');
    const N = { New: [55, 45], Assigned: [170, 45], Open: [285, 45], Fixed: [285, 155], Retest: [170, 155], Closed: [55, 155], Reopened: [170, 255] };
    const edges = [['New', 'Assigned'], ['Assigned', 'Open'], ['Open', 'Fixed'], ['Fixed', 'Retest'], ['Retest', 'Closed'], ['Retest', 'Reopened'], ['Reopened', 'Open']];
    let svg = `<svg viewBox="0 0 340 300" class="viz-svg"><defs><marker id="ahb" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="v-arrowhead"/></marker></defs>`;
    edges.forEach(([a, b]) => {
      let [x1, y1] = N[a], [x2, y2] = N[b];
      const dx = x2 - x1, dy = y2 - y1, d = Math.hypot(dx, dy), ux = dx / d, uy = dy / d;
      if (a === 'Reopened') svg += `<path d="M${x1 + 40},${y1} Q 330,250 ${x2 + 20},${y2 + 22}" class="v-edge" marker-end="url(#ahb)"/>`;
      else svg += `<line x1="${x1 + ux * 40}" y1="${y1 + uy * 22}" x2="${x2 - ux * 42}" y2="${y2 - uy * 24}" class="v-edge" marker-end="url(#ahb)"/>`;
    });
    Object.entries(N).forEach(([k, [x, y]]) => {
      svg += `<g class="v-node rect" data-k="${k}"><rect x="${x - 42}" y="${y - 18}" width="84" height="36" rx="10"/><text x="${x}" y="${y + 5}" text-anchor="middle" class="v-label big">${k}</text></g>`;
    });
    svg += `<g class="v-bug"><text font-size="22" text-anchor="middle">🐞</text></g></svg>`;
    stage.innerHTML = svg;
    const bug = stage.querySelector('.v-bug');
    const say = {
      New: 'Tester logs the bug: "Login fails with valid password".',
      Assigned: 'Lead assigns it to a developer.',
      Open: 'Developer starts working on it.',
      Fixed: 'Developer fixes the code and sends it back to QA.',
      Retest: 'Tester re-tests the fix on the new build.',
      Closed: '✅ Fix works – bug is Closed.',
      Reopened: '❌ Fix did not work – tester Reopens it, it goes back to the developer.',
    };
    function at(k) {
      const [x, y] = N[k];
      bug.style.transform = `translate(${x + 40}px, ${y - 20}px)`;
      stage.querySelectorAll('.v-node').forEach(g => g.classList.toggle('active', g.dataset.k === k));
      cap.innerHTML = `<strong>${k}</strong> – ${say[k]}`;
    }
    let running = false;
    async function run(path) {
      if (running) return; running = true;
      for (const k of path) { at(k); await sleep(1400); }
      running = false;
    }
    button(ctl, '▶ Fix works', () => run(['New', 'Assigned', 'Open', 'Fixed', 'Retest', 'Closed']), true);
    button(ctl, '▶ Fix fails first time', () => run(['New', 'Assigned', 'Open', 'Fixed', 'Retest', 'Reopened', 'Open', 'Fixed', 'Retest', 'Closed']));
    at('New');
  };

  // ---------- 3. GROUP BY / HAVING ----------
  VIZ.groupby = el => {
    const { stage, cap, ctl } = shell(el, 'How GROUP BY and HAVING work', 'Step through it');
    const rows = [[1, 'Login', 'Open'], [2, 'Signup', 'Closed'], [3, 'Cart', 'Open'], [4, 'Home', 'Open'], [5, 'Payment', 'Fixed'], [6, 'Login', 'Reopened'], [7, 'Search', 'Open'], [8, 'Profile', 'Closed']];
    const color = { Open: 'c1', Closed: 'c2', Fixed: 'c3', Reopened: 'c4' };
    const sqlLines = ['SELECT status, COUNT(*)', 'FROM bugs', 'GROUP BY status', 'HAVING COUNT(*) > 1;'];
    function sql(hl) { return `<pre class="viz-sql">${sqlLines.map((l, i) => `<span class="${hl.includes(i) ? 'hl' : ''}">${esc(l)}</span>`).join('\n')}</pre>`; }
    const groups = {};
    rows.forEach(r => (groups[r[2]] = groups[r[2]] || []).push(r));
    const table = (head, body) => `<table class="viz-table"><tr>${head.map(h => `<th>${h}</th>`).join('')}</tr>${body}</table>`;
    stepper(ctl, cap, [
      { caption: '<code>FROM bugs</code> – start with every row of the table.', render: () => {
        stage.innerHTML = sql([1]) + table(['id', 'module', 'status'], rows.map(r => `<tr class="pop"><td>${r[0]}</td><td>${r[1]}</td><td><span class="chip ${color[r[2]]}">${r[2]}</span></td></tr>`).join('')); } },
      { caption: '<code>GROUP BY status</code> – rows with the same status are put into one bucket.', render: () => {
        stage.innerHTML = sql([2]) + `<div class="buckets">${Object.entries(groups).map(([k, v]) => `<div class="bucket ${color[k]} pop"><div class="bucket-h">${k}</div>${v.map(r => `<div class="bucket-row">#${r[0]} ${r[1]}</div>`).join('')}</div>`).join('')}</div>`; } },
      { caption: '<code>COUNT(*)</code> – each bucket becomes ONE row with a count. That\'s why you get one result per group.', render: () => {
        stage.innerHTML = sql([0, 2]) + table(['status', 'COUNT(*)'], Object.entries(groups).map(([k, v]) => `<tr class="pop"><td><span class="chip ${color[k]}">${k}</span></td><td><strong>${v.length}</strong></td></tr>`).join('')); } },
      { caption: '<code>HAVING COUNT(*) > 1</code> – filters the GROUPS. Buckets with only 1 bug are removed. (WHERE could not do this – counts don\'t exist until after grouping.)', render: () => {
        stage.innerHTML = sql([3]) + table(['status', 'COUNT(*)'], Object.entries(groups).map(([k, v]) => `<tr class="${v.length > 1 ? 'keep' : 'gone'}"><td><span class="chip ${color[k]}">${k}</span></td><td><strong>${v.length}</strong> ${v.length > 1 ? '✅' : '❌'}</td></tr>`).join('')); } },
    ], { delay: 2600 });
  };

  // ---------- 4. JOINs ----------
  VIZ.joins = el => {
    const { stage, cap, ctl } = shell(el, 'INNER JOIN vs LEFT JOIN', 'Pick a join');
    const emp = [['Asha', 2], ['Ravi', 1], ['Priya', 3], ['Rahul', null]];
    const dep = { 1: 'QA', 2: 'Development', 3: 'HR', 4: 'Sales' };
    stage.innerHTML = `<svg viewBox="0 0 340 170" class="viz-svg venn">
        <defs><clipPath id="clipL"><circle cx="135" cy="85" r="70"/></clipPath></defs>
        <circle cx="135" cy="85" r="70" class="v-left"/>
        <circle cx="205" cy="85" r="70" class="v-right"/>
        <circle cx="205" cy="85" r="70" class="v-mid" clip-path="url(#clipL)"/>
        <text x="95" y="90" text-anchor="middle" class="v-label big">employees</text>
        <text x="250" y="90" text-anchor="middle" class="v-label big">departments</text>
        <text x="170" y="165" text-anchor="middle" class="v-label">overlap = matching department_id</text>
      </svg><div class="join-out"></div>`;
    const svg = stage.querySelector('svg'), out = stage.querySelector('.join-out');
    function show(kind) {
      svg.dataset.kind = kind;
      const rows = emp.filter(e => kind === 'left' || e[1] !== null).map(e => `<tr class="pop ${e[1] === null ? 'nullrow' : ''}"><td>${e[0]}</td><td>${e[1] === null ? '<i>NULL</i>' : dep[e[1]]}</td></tr>`).join('');
      out.innerHTML = `<pre class="viz-sql">SELECT e.name, d.name\nFROM employees e\n<span class="hl">${kind === 'left' ? 'LEFT' : 'INNER'} JOIN</span> departments d\n  ON e.department_id = d.id;</pre>
        <table class="viz-table"><tr><th>employee</th><th>department</th></tr>${rows}</table>`;
      cap.innerHTML = kind === 'left'
        ? '<strong>LEFT JOIN</strong> keeps <em>every</em> employee. Rahul has no department, so he appears with <strong>NULL</strong>. (Sales has no employees, so it never appears.)'
        : '<strong>INNER JOIN</strong> keeps only rows that match on both sides – Rahul (no department) disappears.';
      ctl.querySelectorAll('button').forEach(b => b.classList.toggle('primary', b.dataset.k === kind));
    }
    button(ctl, 'INNER JOIN', () => show('inner')).dataset.k = 'inner';
    button(ctl, 'LEFT JOIN', () => show('left')).dataset.k = 'left';
    show('inner');
  };

  // ---------- 5. Python for loop ----------
  VIZ.forloop = el => {
    const { stage, cap, ctl } = shell(el, 'Watch a for loop run', 'Step line by line');
    const code = ['for i in range(1, 4):', '    print(i * 10)', 'print("done")'];
    const trace = [
      [0, 1, [], 'range(1, 4) gives 1, 2, 3. First round: <code>i = 1</code>.'],
      [1, 1, ['10'], 'Indented line runs: prints 1 × 10.'],
      [0, 2, ['10'], 'Back to the top. Next value: <code>i = 2</code>.'],
      [1, 2, ['10', '20'], 'Prints 20.'],
      [0, 3, ['10', '20'], 'Next value: <code>i = 3</code>.'],
      [1, 3, ['10', '20', '30'], 'Prints 30.'],
      [2, 3, ['10', '20', '30', 'done'], 'No more values (4 is NOT included). Loop ends; the un-indented line runs once.'],
    ];
    stepper(ctl, cap, trace.map(([line, i, out, c]) => ({ caption: c, render: () => {
      stage.innerHTML = `<div class="loop-grid">
        <pre class="viz-code">${code.map((l, k) => `<span class="${k === line ? 'hl' : ''}">${esc(l)}</span>`).join('\n')}</pre>
        <div><div class="var-box">i = <strong class="pop">${i}</strong></div>
        <div class="out-box"><div class="muted small">Output</div>${out.map(o => `<div class="pop">${o}</div>`).join('')}</div></div></div>`; } })), { delay: 1500 });
  };

  // ---------- 6. HTTP request / response ----------
  VIZ.http = el => {
    const { stage, cap, ctl } = shell(el, 'API request → response', 'Pick a scenario');
    stage.innerHTML = `<div class="http-wrap"><div class="http-box">📱<div class="small">App / Postman</div></div>
      <div class="http-wire"><div class="packet"></div></div><div class="http-box">🖥️<div class="small">Server</div></div></div>
      <div class="http-detail"></div>`;
    const packet = stage.querySelector('.packet'), detail = stage.querySelector('.http-detail');
    const S = {
      'GET user': ['GET /api/users/2', '200 OK', '{ "id": 2, "name": "Janet" }', 'ok', 'Reading data that exists → <strong>200 OK</strong> with the data.'],
      'POST create': ['POST /api/users\n{ "name": "Ravi", "job": "QA" }', '201 Created', '{ "id": 77, "name": "Ravi" }', 'ok', 'Creating something → <strong>201 Created</strong>, usually returns the new id.'],
      'Wrong id': ['GET /api/users/9999', '404 Not Found', '{ "error": "user not found" }', 'bad', 'The thing doesn\'t exist → <strong>404</strong>. A 4xx means the <em>request</em> has a problem.'],
      'No token': ['GET /api/orders\n(no Authorization header)', '401 Unauthorized', '{ "error": "login required" }', 'bad', 'Not logged in / bad token → <strong>401</strong>.'],
      'Server bug': ['GET /api/report', '500 Internal Server Error', '{ "error": "NullPointerException" }', 'err', 'Server crashed → <strong>500</strong>. 5xx = the <em>server\'s</em> fault – log a bug!'],
    };
    let busy = false;
    async function send(name) {
      if (busy) return; busy = true;
      const [req, code, body, cls, c] = S[name];
      detail.innerHTML = `<div class="req"><span class="muted small">Request</span><pre>${esc(req)}</pre></div><div class="res" style="opacity:.25"><span class="muted small">Response</span><pre></pre></div>`;
      packet.className = 'packet go-right'; packet.textContent = req.split(' ')[0];
      await sleep(1100);
      packet.className = `packet at-right ${cls}`; packet.textContent = code.split(' ')[0];
      await sleep(250);
      packet.className = `packet go-left ${cls}`;
      await sleep(1100);
      const res = detail.querySelector('.res');
      res.style.opacity = 1; res.querySelector('pre').innerHTML = `<span class="code-${cls}">${esc(code)}</span>\n${esc(body)}`;
      cap.innerHTML = c; busy = false;
    }
    Object.keys(S).forEach((k, i) => button(ctl, k, () => send(k), i === 0));
    cap.textContent = 'Tap a scenario to send a request.';
  };

  // ---------- 7. Playwright test run ----------
  VIZ.playwright = el => {
    const { stage, cap, ctl } = shell(el, 'What a Playwright test does', 'Step through the test');
    const code = [
      'page.goto("https://shop.test/login")',
      'page.get_by_label("Email").fill("ravi@mail.com")',
      'page.get_by_label("Password").fill("Pass@123")',
      'page.get_by_role("button", name="Login").click()',
      'expect(page.get_by_text("Welcome, Ravi")).to_be_visible()',
    ];
    const st = (n) => ({
      url: n >= 0 ? 'shop.test/' + (n >= 3 ? 'dashboard' : 'login') : '',
      email: n >= 1 ? 'ravi@mail.com' : '', pwd: n >= 2 ? '••••••••' : '', clicked: n === 3, dash: n >= 3, pass: n >= 4,
    });
    const caps = ['<code>goto</code> opens the page – like typing the URL.', '<code>fill</code> types into the field found by its label.',
      'Same for password.', '<code>click</code> presses the button – Playwright waits for it to be ready first.',
      '<code>expect</code> checks the result and retries for up to 5 s. ✅ = test PASSED. If the text never appears → test FAILS.'];
    stepper(ctl, cap, code.map((_, n) => ({ caption: caps[n], render: () => {
      const s = st(n);
      stage.innerHTML = `<pre class="viz-code">${code.map((l, k) => `<span class="${k === n ? 'hl' : ''}">${esc(l)}</span>`).join('\n')}</pre>
        <div class="mock-browser"><div class="mb-bar">🔒 ${esc(s.url)}</div><div class="mb-body">
        ${s.dash ? `<div class="pop" style="font-size:18px">👋 Welcome, Ravi</div>${s.pass ? '<div class="pass pop">✅ assertion passed</div>' : ''}` :
        `<label class="small">Email</label><div class="mb-input ${n === 1 ? 'focus' : ''}">${s.email}</div>
         <label class="small">Password</label><div class="mb-input ${n === 2 ? 'focus' : ''}">${s.pwd}</div>
         <div class="mb-btn ${s.clicked ? 'pressed' : ''}">Login</div>`}</div></div>`; } })), { delay: 2000 });
  };

  // ---------- 8. Git areas ----------
  VIZ.git = el => {
    const { stage, cap, ctl } = shell(el, 'Where your file goes in Git', 'Press the commands in order');
    stage.innerHTML = `<div class="git-areas">
      <div class="git-area" data-a="0"><div class="ga-h">📁 Working folder</div><div class="ga-b"></div></div>
      <div class="git-area" data-a="1"><div class="ga-h">📦 Staging</div><div class="ga-b"></div></div>
      <div class="git-area" data-a="2"><div class="ga-h">💾 Local repo</div><div class="ga-b"></div></div>
      <div class="git-area" data-a="3"><div class="ga-h">☁️ GitHub</div><div class="ga-b"></div></div></div>
      <pre class="viz-sql git-log">$ </pre>`;
    const areas = stage.querySelectorAll('.ga-b'), log = stage.querySelector('.git-log');
    let state = -1, commits = 0;
    function put(i, html) { areas.forEach(a => a.querySelectorAll('.file').forEach(f => f.remove())); if (i >= 0) areas[i].insertAdjacentHTML('beforeend', html); }
    const acts = [
      ['✏️ edit file', 0, 'You changed <code>test_login.py</code>. Git sees it as <strong>modified</strong> – not saved in history yet.', '(you edit test_login.py)'],
      ['git add', 1, '<code>git add</code> puts the change in the <strong>staging</strong> box – "this goes in my next save".', 'git add test_login.py'],
      ['git commit', 2, '<code>git commit</code> saves a <strong>version</strong> in your local history with a message.', 'git commit -m "Add login tests"'],
      ['git push', 3, '<code>git push</code> uploads your commits to <strong>GitHub</strong> – now recruiters and teammates can see them.', 'git push'],
    ];
    const btns = acts.map(([label, to, c, cmd], i) => button(ctl, label, () => {
      if (i !== state + 1 && !(i === 0 && state === 3)) { cap.innerHTML = '⚠️ Try the commands in order: edit → add → commit → push.'; return; }
      state = i;
      if (i === 2) commits++;
      put(to, `<div class="file pop">${i >= 2 ? '🟢 commit #' + commits : '📄 test_login.py'}</div>`);
      if (i === 3) areas[2].insertAdjacentHTML('beforeend', `<div class="file">🟢 commit #${commits}</div>`);
      log.textContent = '$ ' + cmd;
      cap.innerHTML = c;
      btns.forEach((b, k) => b.classList.toggle('primary', k === (state + 1) % 4));
    }, i === 0));
    cap.innerHTML = 'Start by editing a file.';
  };

  // ---------- 9. Forgetting curve (method page) ----------
  VIZ.forgetting = el => {
    const { stage, cap, ctl } = shell(el, 'Why spaced reviews work', 'Compare the two lines');
    const W = 340, H = 200, x0 = 34, y0 = 170, xw = 290, yh = 140;
    const X = d => x0 + d / 30 * xw, Y = p => y0 - p / 100 * yh;
    let noRev = '', rev = '';
    for (let d = 0; d <= 30; d += 0.5) noRev += `${d ? 'L' : 'M'}${X(d)},${Y(100 * Math.exp(-d / 2.2))}`;
    const reviews = [1, 3, 7, 16, 30]; let start = 0, s = 2.2, path = '';
    reviews.forEach((r, k) => {
      for (let d = start; d <= r; d += 0.25) path += `${(d === start && k === 0) ? 'M' : 'L'}${X(d)},${Y(100 * Math.exp(-(d - start) / s))}`;
      path += `L${X(r)},${Y(100)}`; start = r; s *= 2.6;
    });
    rev = path;
    stage.innerHTML = `<svg viewBox="0 0 ${W} ${H + 20}" class="viz-svg">
      <line x1="${x0}" y1="${y0}" x2="${x0 + xw}" y2="${y0}" class="v-axis"/><line x1="${x0}" y1="${y0}" x2="${x0}" y2="${y0 - yh}" class="v-axis"/>
      <text x="${x0 - 6}" y="${Y(100) + 4}" text-anchor="end" class="v-label">100%</text><text x="${x0 - 6}" y="${y0}" text-anchor="end" class="v-label">0</text>
      <text x="${x0 + xw / 2}" y="${y0 + 22}" text-anchor="middle" class="v-label">days after learning →</text>
      ${reviews.map(r => `<text x="${X(r)}" y="${y0 + 11}" text-anchor="middle" class="v-label">${r}</text>`).join('')}
      <path d="${noRev}" class="curve-bad"/><path d="${rev}" class="curve-good"/></svg>`;
    const bad = stage.querySelector('.curve-bad'), good = stage.querySelector('.curve-good');
    [bad, good].forEach(p => { const L = p.getTotalLength(); p.style.strokeDasharray = L; p.style.strokeDashoffset = L; });
    function draw(p) { p.style.transition = 'none'; p.style.strokeDashoffset = p.getTotalLength(); p.getBoundingClientRect(); p.style.transition = 'stroke-dashoffset 2.5s ease'; p.style.strokeDashoffset = 0; }
    button(ctl, '▶ No review', () => { draw(bad); cap.innerHTML = '<span class="chip c4">red</span> Learn once, never review: most of it is gone within days.'; }, true);
    button(ctl, '▶ Spaced reviews', () => { draw(good); cap.innerHTML = '<span class="chip c3">green</span> Review on day 1, 3, 7, 16, 30: each review resets memory AND makes it fade more slowly.'; });
    cap.textContent = 'Press the buttons to draw each line. (Illustration of the forgetting curve.)';
  };

  window.initViz = function (root) {
    (root || document).querySelectorAll('.viz:not([data-ready])').forEach(el => {
      if (el.offsetParent === null && !el.closest('.step:not([hidden])')) return; // draw when visible
      const fn = VIZ[el.dataset.viz];
      if (!fn) return;
      el.dataset.ready = 1;
      try { fn(el); } catch (e) { el.innerHTML = '<p class="muted small">Diagram could not load.</p>'; console.error(e); }
    });
  };
  document.addEventListener('DOMContentLoaded', () => initViz(document));
})();
