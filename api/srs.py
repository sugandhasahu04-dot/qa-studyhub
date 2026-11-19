"""Spaced repetition (SM-2 algorithm, Wozniak 1987) + study-day helpers.

Grades from the review buttons:
  Again = 1 (forgot)   Hard = 3   Good = 4   Easy = 5
"""
import os
from datetime import datetime, timedelta, timezone

# Days are counted in your local time (default India, UTC+5:30)
TZ = timezone(timedelta(minutes=int(os.environ.get("TZ_OFFSET_MINUTES", "330"))))

GRADES = {"again": 1, "hard": 3, "good": 4, "easy": 5}


def today():
    return datetime.now(TZ).date()


def today_str():
    return today().isoformat()


def schedule(ease, interval, reps, grade):
    """Return (ease, interval_days, reps, lapsed) after one review."""
    lapsed = False
    if grade < 3:
        # Forgot: start the card again. It comes back today (in this session) and then tomorrow.
        reps, interval, lapsed = 0, 0, True
    else:
        reps += 1
        if reps == 1:
            interval = 3 if grade == 5 else 1
        elif reps == 2:
            interval = 3 if grade == 3 else 6
        else:
            factor = 1.2 if grade == 3 else ease * (1.3 if grade == 5 else 1.0)
            interval = max(interval + 1, round(interval * factor))
    ease = ease + (0.1 - (5 - grade) * (0.08 + (5 - grade) * 0.02))
    ease = max(1.3, round(ease, 2))
    return ease, interval, reps, lapsed


def due_date(interval):
    return (today() + timedelta(days=interval)).isoformat()


def preview_intervals(ease, interval, reps):
    """What each button would do – shown under the buttons, like Anki."""
    out = {}
    for name, g in GRADES.items():
        _, iv, _, _ = schedule(ease, interval, reps, g)
        out[name] = "now" if iv == 0 else ("1 day" if iv == 1 else (f"{iv} days" if iv < 31 else f"{round(iv / 30)} mo"))
    return out


def streak(days):
    """days: set of 'YYYY-MM-DD' strings with any study activity."""
    d = today()
    if d.isoformat() not in days:
        d -= timedelta(days=1)  # streak still alive if you studied yesterday
    n = 0
    while d.isoformat() in days:
        n += 1
        d -= timedelta(days=1)
    return n


def strength(interval):
    """Rough memory strength label for a card."""
    if interval >= 21:
        return "strong"
    if interval >= 6:
        return "growing"
    return "new"
