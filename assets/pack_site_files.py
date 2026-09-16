#!/usr/bin/env python3
"""Pack linked markdown/csv into files-bundle.js so the site never downloads them."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / "files-bundle.js"

FILES = [
    "pick_selection/week1/ACTUAL_BOOK.md",
    "pick_selection/PROCESS.md",
    "pick_selection/week1/HEDGE_MONEY.md",
    "pick_selection/week1/hedge_econ_tables.md",
    "all_picks_2026/FINDINGS.md",
    "all_picks_2026/parsed/winner_matches.csv",
    "all_picks_2026/parsed/week1_pick_share.csv",
    "Power_Rankings/PROCESS.md",
    "Power_Rankings/9-9-2026/SOURCES.md",
    "Power_Rankings/9-9-2026/consensus_power_rankings.csv",
    "Power_Rankings/9-9-2026/source_ranks.csv",
    "Power_Rankings/9-9-2026/game_implied_odds.csv",
    "Power_Rankings/9-9-2026/team_weekly_implied_odds.csv",
    "Power_Rankings/9-15-2026/SOURCES.md",
    "Power_Rankings/9-15-2026/consensus_power_rankings.csv",
    "Power_Rankings/9-15-2026/source_ranks.csv",
    "Power_Rankings/9-15-2026/game_implied_odds.csv",
    "Power_Rankings/9-15-2026/team_weekly_implied_odds.csv",
    "model_crafting/data/2026/HOW_THE_MODEL_WORKS.md",
    "model_crafting/data/2026/pick_projections_2026.csv",
    "model_crafting/data/2026/raw/nfl_week2_spreads_2026.csv",
    "model_crafting/data/2026/raw/nfl_week1_spreads_2026.csv",
    "model_crafting/data/2026/raw/nfl_win_totals_2026.csv",
    "model_crafting/data/2026/portfolio_rationale.md",
    "model_crafting/data/2026/portfolio_10_entries.csv",
]

for folder in (
    ROOT / "Power_Rankings/9-9-2026/sources",
    ROOT / "Power_Rankings/9-15-2026/sources",
):
    FILES.extend(
        sorted(p.relative_to(ROOT).as_posix() for p in folder.glob("*.csv"))
    )

bundle: dict[str, str] = {}
missing: list[str] = []
for rel in FILES:
    path = ROOT / rel
    if not path.is_file():
        missing.append(rel)
        continue
    bundle[rel] = path.read_text(encoding="utf-8", errors="replace")

if missing:
    raise SystemExit("missing: " + ", ".join(missing))

OUT.write_text(
    "window.CIRCA_FILES = " + json.dumps(bundle, ensure_ascii=False) + ";\n",
    encoding="utf-8",
)
print(f"wrote {OUT.name} ({len(bundle)} files, {OUT.stat().st_size} bytes)")
