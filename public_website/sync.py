#!/usr/bin/env python3
"""Copy the static Circa site into public_website/ for GitHub Pages."""

from __future__ import annotations

import json
from datetime import date
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

WSL_HEDGE = (
    "file://wsl.localhost/Ubuntu-22.04/home/johnbuts/mobile_app/sports_circa/"
    "pick_selection/week1/index.html"
)
HEDGE_REL = "pick_selection/week1/index.html"

PAGES = [
    "index.html",
    "week1.html",
    "week2.html",
    "week3.html",
    "week4.html",
    "week5.html",
    "models.html",
    "entries.html",
    "view.html",
    "404.html",
    "pick_selection/week1/index.html",
    "all_picks_2026/index.html",
]

ASSETS = [
    "assets/circa.css",
    "assets/hub.css",
    "assets/circa-nav.js",
    "assets/circa-view.js",
    "assets/our-book.js",
    "assets/week2-crowd.js",
    "assets/week3-crowd.js",
    "assets/week5-crowd.js",
    "assets/week2-chip.js",
]

BUNDLE_FILES = [
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
    "Weekly_models/MODELS.md",
    "Weekly_models/Week3/NOTES.md",
    "Weekly_models/Week5/NOTES.md",
    "Weekly_models/Week5/out/week5_book.md",
    "Weekly_models/Week5/out/week5_shares.csv",
    "Weekly_models/Week2_v2/actual_odds.md",
]

EXTRA = [
    "pick_selection/week1/fanduel_odds.json",
]

WIPE = (
    "assets",
    "pick_selection",
    "all_picks_2026",
    "Power_Rankings",
    "model_crafting",
    "Weekly_models",
)


# Files that live only on the author's machine (e.g. model_crafting/) and are not in
# this checkout: reuse the copy already published here instead of failing.
FALLBACK: dict[str, bytes] = {}


def cache_fallbacks(rels: list[str]) -> None:
    for rel in rels:
        if not (ROOT / rel).is_file() and (HERE / rel).is_file():
            FALLBACK[rel] = (HERE / rel).read_bytes()


def bundle_list() -> list[str]:
    files = list(BUNDLE_FILES)
    for folder in (
        ROOT / "Power_Rankings/9-9-2026/sources",
        ROOT / "Power_Rankings/9-15-2026/sources",
    ):
        files.extend(sorted(p.relative_to(ROOT).as_posix() for p in folder.glob("*.csv")))
    return files


def portable(text: str) -> str:
    return text.replace(WSL_HEDGE, HEDGE_REL)


def copy_file(rel: str) -> None:
    src = ROOT / rel
    dst = HERE / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not src.is_file():
        if rel not in FALLBACK:
            raise SystemExit(f"missing {rel}")
        dst.write_bytes(FALLBACK[rel])
        return
    if src.suffix.lower() in {".md", ".html"}:
        dst.write_text(portable(src.read_text(encoding="utf-8", errors="replace")), encoding="utf-8")
    else:
        shutil.copy2(src, dst)


def wipe_generated() -> None:
    logs = {}
    for name in WIPE:
        path = HERE / name
        if path.is_dir():
            logs.update({log: log.read_bytes() for log in path.rglob("CHANGES.md")})
            shutil.rmtree(path)
    for log, body in logs.items():
        log.parent.mkdir(parents=True, exist_ok=True)
        log.write_bytes(body)


def write_bundle(files: list[str]) -> None:
    bundle: dict[str, str] = {}
    missing: list[str] = []
    for rel in files:
        path = ROOT / rel
        if path.is_file():
            bundle[rel] = portable(path.read_text(encoding="utf-8", errors="replace"))
        elif rel in FALLBACK:
            bundle[rel] = FALLBACK[rel].decode("utf-8", errors="replace")
        else:
            missing.append(rel)
    if missing:
        raise SystemExit("missing: " + ", ".join(missing))
    out = HERE / "assets" / "files-bundle.js"
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = "window.CIRCA_FILES = " + json.dumps(bundle, ensure_ascii=False) + ";\n"
    out.write_text(payload, encoding="utf-8")
    root_out = ROOT / "assets" / "files-bundle.js"
    root_out.parent.mkdir(parents=True, exist_ok=True)
    root_out.write_text(payload, encoding="utf-8")
    print(f"wrote {out.relative_to(HERE)} ({len(bundle)} files, {out.stat().st_size} bytes)")


def note_dir(path: Path) -> None:
    log = path / "CHANGES.md"
    if log.exists():
        return
    log.write_text(
        "# Changes\n\n"
        f"- {date.today().isoformat()} — Synced from repo root for the GitHub Pages snapshot.\n",
        encoding="utf-8",
    )


def main() -> None:
    files = bundle_list()
    cache_fallbacks(PAGES + ASSETS + EXTRA + files)
    wipe_generated()
    for rel in PAGES + ASSETS + EXTRA + files:
        copy_file(rel)
        note_dir((HERE / rel).parent)
    write_bundle(files)
    (HERE / ".nojekyll").write_text("", encoding="utf-8")
    print(f"synced {HERE}")


if __name__ == "__main__":
    main()
