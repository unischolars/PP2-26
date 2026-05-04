"""
persistence.py — Load and save settings and leaderboard data to JSON files.
All disk I/O for the game lives here so racer.py stays clean.
"""

import json
import os
from datetime import datetime

# ── File paths ────────────────────────────────────────────────────────────────
SETTINGS_FILE    = os.path.join(os.path.dirname(__file__), "settings.json")
LEADERBOARD_FILE = os.path.join(os.path.dirname(__file__), "leaderboard.json")

# ── Default settings applied when no settings.json exists ─────────────────────
DEFAULT_SETTINGS = {
    "sound":      True,          # sound effects on/off
    "car_color":  "red",         # player car color
    "difficulty": "normal",      # easy / normal / hard
}

# ── Settings helpers ──────────────────────────────────────────────────────────

def load_settings() -> dict:
    """Return settings dict, falling back to defaults on any error."""
    if not os.path.exists(SETTINGS_FILE):
        return dict(DEFAULT_SETTINGS)
    try:
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)
        # Fill in any keys added after the file was first written
        for key, val in DEFAULT_SETTINGS.items():
            data.setdefault(key, val)
        return data
    except (json.JSONDecodeError, IOError):
        return dict(DEFAULT_SETTINGS)


def save_settings(settings: dict) -> None:
    """Write settings dict to disk."""
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=2)
    except IOError as e:
        print(f"[persistence] Could not save settings: {e}")

# ── Leaderboard helpers ───────────────────────────────────────────────────────

def load_leaderboard() -> list:
    """Return top-10 leaderboard entries (list of dicts), sorted by score desc."""
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            data = json.load(f)
        # Sort descending by score, return top 10
        return sorted(data, key=lambda e: e.get("score", 0), reverse=True)[:10]
    except (json.JSONDecodeError, IOError):
        return []


def save_score(username: str, score: int, distance: float, coins: int) -> None:
    """Append a new score entry and keep only the top 10 on disk."""
    entries = load_leaderboard()

    new_entry = {
        "name":     username,
        "score":    score,
        "distance": round(distance),
        "coins":    coins,
        "date":     datetime.now().strftime("%Y-%m-%d"),
    }
    entries.append(new_entry)

    # Keep top 10 only
    entries = sorted(entries, key=lambda e: e["score"], reverse=True)[:10]

    try:
        with open(LEADERBOARD_FILE, "w") as f:
            json.dump(entries, f, indent=2)
    except IOError as e:
        print(f"[persistence] Could not save leaderboard: {e}")