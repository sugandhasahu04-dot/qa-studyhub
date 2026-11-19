import os
import sys
import hmac
import random
import hashlib
from datetime import timedelta
from functools import wraps

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import markdown as md  # noqa: E402
from flask import (Flask, render_template, request, redirect, url_for,  # noqa: E402
                   session, jsonify, abort, flash)

import db  # noqa: E402
import srs  # noqa: E402
from content import TOPICS, BY_SLUG, LEVELS, CARDS  # noqa: E402

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")
APP_PASSWORD = os.environ.get("APP_PASSWORD", "")

RESOURCE_KINDS = {"pdf": "📕 PDF / Book", "youtube": "▶️ YouTube", "link": "🔗 Website"}
QUIZ_TYPES = {"theory": "Theory", "practical": "Practical"}

_lesson_cache = {}


def lesson_html(topic):
    if topic["slug"] not in _lesson_cache:
        _lesson_cache[topic["slug"]] = md.markdown(topic["lesson"], extensions=["fenced_code", "tables"])
    return _lesson_cache[topic["slug"]]


def get_topic(slug):
    t = BY_SLUG.get(slug)
    if not t:
        abort(404)
    return t


def mark_active():
    db.execute("INSERT INTO activity (day) VALUES (?) ON CONFLICT (day) DO NOTHING", (srs.today_str(),))


def add_card(key, topic, front, back, source):
    return db.execute(
        "INSERT INTO cards (key, topic, front, back, source, due) VALUES (?, ?, ?, ?, ?, ?) "
        "ON CONFLICT (key) DO NOTHING", (key, topic, front, back, source, srs.today_str()))


def seed_cards(slug):
    added = 0
    for i, (front, back) in enumerate(CARDS.get(slug, [])):
        added += add_card(f"builtin:{slug}:{i}", slug, front, back, "builtin") or 0
    return added


def split_lesson(markdown_text):
    """Split a lesson into chunks at each '## ' heading (Oakley: learn in small chunks)."""
    chunks, cur = [], []
    for line in markdown_text.strip().split("\n"):
        if line.startswith("## ") and cur:
            chunks.append("\n".join(cur))
            cur = []
        cur.append(line)
    if cur:
        chunks.append("\n".join(cur))
    out = []
    for c in chunks:
        first = c.split("\n", 1)[0]
        title = first[3:].strip() if first.startswith("## ") else "Introduction"
        body = c.split("\n", 1)[1] if first.startswith("## ") and "\n" in c else c
        out.append({"title": title, "html": md.markdown(body.replace("\n---\n", "\n"), extensions=["fenced_code", "tables"])})
    return out


# ---------- auth (optional: set APP_PASSWORD to lock the site) ----------
@app.before_request
def require_login():
    if not APP_PASSWORD:
        return
    if request.endpoint in ("login", "static") or session.get("ok"):
        return
    if request.path.startswith("/api/"):
        return jsonify(error="login required"), 401
    return redirect(url_for("login", next=request.path))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if APP_PASSWORD and hmac.compare_digest(request.form.get("password", ""), APP_PASSWORD):
            session["ok"] = True
            session.permanent = True
            nxt = request.args.get("next", "/")
            return redirect(nxt if nxt.startswith("/") and not nxt.startswith("//") else "/")
        error = "Wrong password"
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login") if APP_PASSWORD else "/")


@app.context_processor
def inject_globals():
    return {"TOPICS": TOPICS, "LEVELS": LEVELS, "QUIZ_TYPES": QUIZ_TYPES, "BY_SLUG": BY_SLUG,
            "TEMP_DB": bool(os.environ.get("VERCEL")) and not db.IS_PG,
            "RESOURCE_KINDS": RESOURCE_KINDS, "LOCKED": bool(APP_PASSWORD)}


# ---------- pages ----------
@app.route("/")
def home():
    today = srs.today_str()
    attempts = db.query(
        "SELECT topic, quiz_type, level, MAX(score * 100 / total) AS best, COUNT(*) AS tries "
        "FROM quiz_attempts WHERE total > 0 GROUP BY topic, quiz_type, level")
    best = {}
    for a in attempts:
        best[(a["topic"], a["quiz_type"], a["level"])] = int(a["best"])
    done = {r["topic"] for r in db.query("SELECT topic FROM lesson_progress")}
    note_counts = {r["topic"]: r["n"] for r in db.query("SELECT topic, COUNT(*) AS n FROM notes GROUP BY topic")}
    recent_notes = db.query("SELECT id, topic, title, updated_at FROM notes ORDER BY updated_at DESC LIMIT 5")
    due_total = db.query("SELECT COUNT(*) AS n FROM cards WHERE due <= ?", (today,), one=True)["n"]
    mem = {}
    for r in db.query("SELECT topic, interval_days FROM cards"):
        m = mem.setdefault(r["topic"], {"new": 0, "growing": 0, "strong": 0, "total": 0})
        m[srs.strength(r["interval_days"])] += 1
        m["total"] += 1
    days = {r["day"] for r in db.query("SELECT day FROM activity")}
    reviewed_today = db.query("SELECT COUNT(*) AS n FROM reviews WHERE day = ?", (today,), one=True)["n"]
    next_topic = next((t for t in TOPICS if t["slug"] not in done), None)
    return render_template("home.html", best=best, done=done, note_counts=note_counts,
                           recent_notes=recent_notes, due_total=due_total, mem=mem,
                           streak=srs.streak(days), studied_today=today in days,
                           reviewed_today=reviewed_today, next_topic=next_topic,
                           week=[(srs.today() - timedelta(days=i)).isoformat() in days
                                 for i in range(6, -1, -1)])


@app.route("/topic/<slug>")
def topic_page(slug):
    t = get_topic(slug)
    user_res = db.query("SELECT * FROM resources WHERE topic = ? ORDER BY id", (slug,))
    notes = db.query("SELECT id, title, updated_at FROM notes WHERE topic = ? ORDER BY updated_at DESC", (slug,))
    done = db.query("SELECT topic FROM lesson_progress WHERE topic = ?", (slug,), one=True) is not None
    counts = {qt: {lv: len(t[qt].get(lv, [])) for lv in LEVELS} for qt in QUIZ_TYPES}
    n_cards = db.query("SELECT COUNT(*) AS n FROM cards WHERE topic = ?", (slug,), one=True)["n"]
    return render_template("topic.html", t=t, lesson=lesson_html(t), user_res=user_res,
                           notes=notes, done=done, counts=counts, n_cards=n_cards)


@app.post("/topic/<slug>/complete")
def toggle_complete(slug):
    get_topic(slug)
    if db.query("SELECT topic FROM lesson_progress WHERE topic = ?", (slug,), one=True):
        db.execute("DELETE FROM lesson_progress WHERE topic = ?", (slug,))
    else:
        db.execute("INSERT INTO lesson_progress (topic) VALUES (?)", (slug,))
        n = seed_cards(slug)
        mark_active()
        if n:
            flash(f"✅ {n} flashcards for this topic were added to your daily review.")
    return redirect(url_for("topic_page", slug=slug))


@app.post("/resources")
def add_resource():
    slug = request.form.get("topic", "")
    get_topic(slug)
    title = request.form.get("title", "").strip()
    url = request.form.get("url", "").strip()
    kind = request.form.get("kind", "link")
    if kind not in RESOURCE_KINDS:
        kind = "link"
    if title and url.startswith(("http://", "https://")):
        db.execute("INSERT INTO resources (topic, kind, title, url) VALUES (?, ?, ?, ?)", (slug, kind, title, url))
    else:
        flash("Add a title and a link starting with http:// or https://")
    return redirect(url_for("topic_page", slug=slug) + "#resources")


@app.post("/resources/<int:rid>/delete")
def delete_resource(rid):
    r = db.query("SELECT topic FROM resources WHERE id = ?", (rid,), one=True)
    db.execute("DELETE FROM resources WHERE id = ?", (rid,))
    return redirect(url_for("topic_page", slug=r["topic"]) + "#resources" if r else "/")


@app.route("/quiz/<slug>/<qtype>/<level>")
def quiz(slug, qtype, level):
    t = get_topic(slug)
    if qtype not in QUIZ_TYPES or level not in LEVELS:
        abort(404)
    questions = t[qtype].get(level, [])
    history = db.query(
        "SELECT score, total, created_at FROM quiz_attempts WHERE topic = ? AND quiz_type = ? AND level = ? "
        "ORDER BY id DESC LIMIT 5", (slug, qtype, level))
    return render_template("quiz.html", t=t, qtype=qtype, level=level,
                           questions=questions, n=len(questions), history=history)


@app.post("/api/attempts")
def save_attempt():
    data = request.get_json(silent=True) or {}
    slug, qtype, level = data.get("topic"), data.get("quiz_type"), data.get("level")
    try:
        score, total = int(data.get("score", 0)), int(data.get("total", 0))
    except (TypeError, ValueError):
        return jsonify(error="bad numbers"), 400
    mixed = slug == "mixed" and level == "mixed"
    if not mixed and (slug not in BY_SLUG or qtype not in QUIZ_TYPES or level not in LEVELS):
        return jsonify(error="bad data"), 400
    if total <= 0 or not 0 <= score <= total:
        return jsonify(error="bad data"), 400
    mark_active()
    db.execute("INSERT INTO quiz_attempts (topic, quiz_type, level, score, total) VALUES (?, ?, ?, ?, ?)",
               (slug, qtype if not mixed else "theory", level, score, total))
    return jsonify(ok=True)


@app.post("/api/cards/mistakes")
def save_mistakes():
    """Wrong quiz answers become flashcards, so mistakes come back until you know them."""
    items = (request.get_json(silent=True) or {}).get("items", [])[:30]
    added = 0
    for it in items:
        topic, front, back = it.get("topic"), str(it.get("front", ""))[:1000], str(it.get("back", ""))[:2000]
        if topic not in BY_SLUG or not front or not back:
            continue
        key = "mistake:" + hashlib.sha1(front.encode()).hexdigest()[:16]
        added += add_card(key, topic, front, back, "mistake") or 0
    return jsonify(ok=True, added=added)


# ---------- spaced repetition review ----------
@app.route("/review")
def review():
    topic = request.args.get("topic", "")
    sql, params = "SELECT * FROM cards WHERE due <= ?", [srs.today_str()]
    if topic in BY_SLUG:
        sql += " AND topic = ?"
        params.append(topic)
    cards = db.query(sql, tuple(params))
    random.shuffle(cards)  # interleaving: topics mixed together
    cards = cards[:60]
    for c in cards:
        c["preview"] = srs.preview_intervals(c["ease"], c["interval_days"], c["reps"])
        c["topic_title"] = BY_SLUG.get(c["topic"], {}).get("title", c["topic"])
        c.pop("created_at", None)
    total_cards = db.query("SELECT COUNT(*) AS n FROM cards", one=True)["n"]
    return render_template("review.html", cards=cards, topic=topic, total_cards=total_cards)


@app.post("/api/review")
def api_review():
    data = request.get_json(silent=True) or {}
    grade = srs.GRADES.get(data.get("grade"))
    card = db.query("SELECT * FROM cards WHERE id = ?", (int(data.get("card_id", 0)),), one=True)
    if not grade or not card:
        return jsonify(error="bad data"), 400
    ease, interval, reps, lapsed = srs.schedule(card["ease"], card["interval_days"], card["reps"], grade)
    db.execute("UPDATE cards SET ease = ?, interval_days = ?, reps = ?, lapses = lapses + ?, due = ? WHERE id = ?",
               (ease, interval, reps, 1 if lapsed else 0, srs.due_date(interval), card["id"]))
    db.execute("INSERT INTO reviews (card_id, grade, day) VALUES (?, ?, ?)", (card["id"], grade, srs.today_str()))
    mark_active()
    preview = srs.preview_intervals(ease, interval, reps)
    return jsonify(ok=True, again=interval == 0, interval=interval, preview=preview)


@app.route("/cards")
def cards_page():
    topic = request.args.get("topic", "")
    sql, params = "SELECT * FROM cards", ()
    if topic in BY_SLUG:
        sql, params = sql + " WHERE topic = ?", (topic,)
    rows = db.query(sql + " ORDER BY topic, id", params)
    for r in rows:
        r["strength"] = srs.strength(r["interval_days"])
    return render_template("cards.html", cards=rows, topic=topic)


@app.post("/cards/add")
def cards_add():
    topic = request.form.get("topic", "")
    front, back = request.form.get("front", "").strip(), request.form.get("back", "").strip()
    if topic in BY_SLUG and front and back:
        key = "mine:" + hashlib.sha1((front + srs.today_str() + str(random.random())).encode()).hexdigest()[:16]
        add_card(key, topic, front, back, "mine")
        flash("Card added – it will appear in today's review.")
    else:
        flash("Choose a topic and fill both sides of the card.")
    return redirect(url_for("cards_page", topic=topic))


@app.post("/cards/<int:cid>/delete")
def cards_delete(cid):
    db.execute("DELETE FROM cards WHERE id = ?", (cid,))
    return redirect(request.referrer or url_for("cards_page"))


# ---------- guided learning ----------
@app.route("/learn/<slug>")
def learn(slug):
    t = get_topic(slug)
    pool = t["theory"].get("easy", []) + t["theory"].get("medium", [])
    pretest = random.sample(pool, min(3, len(pool)))
    return render_template("learn.html", t=t, chunks=split_lesson(t["lesson"]), pretest=pretest,
                           n_cards=len(CARDS.get(slug, [])))


@app.post("/api/learn/<slug>/finish")
def learn_finish(slug):
    t = get_topic(slug)
    data = request.get_json(silent=True) or {}
    explanation = str(data.get("explanation", "")).strip()
    recalls = data.get("recalls", [])
    if explanation or any(str(r).strip() for r in recalls):
        body = ""
        if explanation:
            body += "🧒 My simple explanation (Feynman):\n" + explanation + "\n\n"
        for r in recalls:
            if str(r.get("text", "")).strip():
                body += f"🧠 Recall – {r.get('title', '')}:\n{str(r['text']).strip()}\n\n"
        db.execute("INSERT INTO notes (topic, title, body) VALUES (?, ?, ?)",
                   (slug, f"{t['title']} – what I learned ({srs.today().strftime('%d %b')})", body.strip()))
    db.execute("INSERT INTO lesson_progress (topic) VALUES (?) ON CONFLICT (topic) DO NOTHING", (slug,))
    added = seed_cards(slug)
    mark_active()
    return jsonify(ok=True, cards_added=added)


@app.route("/mixed")
def mixed():
    """Interleaved practice: questions from different topics and levels, shuffled."""
    done = [r["topic"] for r in db.query("SELECT topic FROM lesson_progress")]
    topics = [BY_SLUG[s] for s in done if s in BY_SLUG] or TOPICS
    pool = []
    for t in topics:
        for qt in ("theory", "practical"):
            for lv in LEVELS:
                for q in t[qt].get(lv, []):
                    if q.get("type", "mcq") in ("mcq", "scenario"):
                        pool.append({**q, "topic": t["slug"], "tag": f"{t['icon']} {t['title']} · {lv}"})
    questions = random.sample(pool, min(10, len(pool)))
    fake_topic = {"slug": "mixed", "title": "Mixed practice", "icon": "🔀"}
    return render_template("quiz.html", t=fake_topic, qtype="mixed", level="mixed",
                           questions=questions, n=len(questions), history=[])


@app.route("/method")
def method():
    return render_template("method.html")


@app.route("/console")
def console():
    return render_template("console.html")


# ---------- notes ----------
@app.route("/notes")
def notes():
    topic = request.args.get("topic", "")
    q = request.args.get("q", "").strip()
    sql, params = "SELECT * FROM notes WHERE 1=1", []
    if topic:
        sql += " AND topic = ?"
        params.append(topic)
    if q:
        sql += " AND (LOWER(title) LIKE ? OR LOWER(body) LIKE ?)"
        params += [f"%{q.lower()}%"] * 2
    sql += " ORDER BY updated_at DESC"
    return render_template("notes.html", notes=db.query(sql, tuple(params)), topic=topic, q=q)


@app.route("/notes/new")
def new_note():
    note = {"id": None, "topic": request.args.get("topic", "general"),
            "title": request.args.get("title", ""), "body": request.args.get("body", "")}
    return render_template("note_edit.html", note=note)


@app.route("/notes/<int:nid>")
def view_note(nid):
    note = db.query("SELECT * FROM notes WHERE id = ?", (nid,), one=True) or abort(404)
    return render_template("note_view.html", note=note)


@app.route("/notes/<int:nid>/edit")
def edit_note(nid):
    note = db.query("SELECT * FROM notes WHERE id = ?", (nid,), one=True) or abort(404)
    return render_template("note_edit.html", note=note)


@app.post("/notes/save")
def save_note():
    nid = request.form.get("id")
    topic = request.form.get("topic", "general")
    if topic != "general" and topic not in BY_SLUG:
        topic = "general"
    title = request.form.get("title", "").strip() or "Untitled note"
    body = request.form.get("body", "")
    if nid:
        db.execute("UPDATE notes SET topic = ?, title = ?, body = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                   (topic, title, body, int(nid)))
        return redirect(url_for("view_note", nid=int(nid)))
    db.execute("INSERT INTO notes (topic, title, body) VALUES (?, ?, ?)", (topic, title, body))
    new = db.query("SELECT id FROM notes ORDER BY id DESC LIMIT 1", one=True)
    return redirect(url_for("view_note", nid=new["id"]))


@app.post("/notes/<int:nid>/delete")
def delete_note(nid):
    db.execute("DELETE FROM notes WHERE id = ?", (nid,))
    return redirect(url_for("notes"))


@app.errorhandler(404)
def not_found(e):
    return render_template("base.html", content_404=True), 404


if __name__ == "__main__":
    app.run(debug=True, port=5000)
