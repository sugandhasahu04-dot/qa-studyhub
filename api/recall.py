"""Score a free-text recall answer against the key points of a lesson part.

Simple and transparent: each key point has a few ways of saying it. A point counts
if any of them appears in what you wrote. Small typos and word endings are allowed
(design ≈ designing, requirment ≈ requirement).
"""
import re
from difflib import SequenceMatcher

WORD = re.compile(r"[a-z0-9_]+")


def _norm(text):
    return (text or "").lower().replace("’", "'")


def _word_hit(w, tokens):
    for t in tokens:
        if t == w:
            return True
        if len(w) >= 4 and len(t) >= 4 and (t.startswith(w) or w.startswith(t)):
            return True
        if len(w) >= 5 and len(t) >= 4 and SequenceMatcher(None, w, t).ratio() >= 0.84:
            return True
    return False


def _alt_hit(alt, raw, tokens):
    alt = alt.lower()
    # Symbols (==, *, {{, user[, 200 …) or padded phrases: plain text search
    if re.search(r"[^a-z0-9 \-]", alt) or alt != alt.strip():
        return alt in raw
    words = [w for w in re.split(r"[\s\-]+", alt) if w]
    if not words:
        return False
    if len(words) > 1 and alt in raw:
        return True
    return all(_word_hit(w, tokens) for w in words)


def score(text, points):
    """points: [(label, "alt|alt")]. Returns dict with percent, hits, misses."""
    raw = _norm(text)
    tokens = WORD.findall(raw)
    hits, misses = [], []
    for label, alts in points:
        ok = any(_alt_hit(a, raw, tokens) for a in alts.split("|") if a.strip() or a)
        (hits if ok else misses).append(label)
    total = len(points)
    pct = round(100 * len(hits) / total) if total else 0
    return {"percent": pct, "hits": hits, "misses": misses, "total": total}
