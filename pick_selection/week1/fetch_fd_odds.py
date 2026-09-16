"""Fetch FanDuel NFL moneylines into fanduel_odds.json next to this script.

Reads ODDS_API_KEY from the environment, then week1/.env (gitignored).

  uv run python fetch_fd_odds.py
"""
from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "fanduel_odds.json"
ENV_PATH = HERE / ".env"


def load_dotenv(path: Path) -> None:
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key, val = key.strip(), val.strip().strip("'").strip('"')
        if key and key not in os.environ:
            os.environ[key] = val


load_dotenv(ENV_PATH)
KEY = os.environ.get("ODDS_API_KEY", "").strip()
if not KEY:
    raise SystemExit(f"Set ODDS_API_KEY or put it in {ENV_PATH}")

URL = (
    "https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds"
    "?regions=us&markets=h2h&oddsFormat=american&bookmakers=fanduel"
    f"&apiKey={KEY}"
)

req = urllib.request.Request(URL)
with urllib.request.urlopen(req) as resp:
    events = json.loads(resp.read().decode())
    remaining = resp.headers.get("x-requests-remaining")

OUT.write_text(json.dumps({"events": events, "remaining": remaining}), encoding="utf-8")
print(f"wrote {OUT} ({len(events)} events, remaining={remaining})")
