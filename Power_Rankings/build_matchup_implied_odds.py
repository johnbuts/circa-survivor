#!/usr/bin/env python3
"""Build team-by-week implied win % CSV from The Odds API (DraftKings) + NFL schedule."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
OUT_DIR = SCRIPT_DIR / "9-15-2026"
INPUT_FILE = OUT_DIR / "odds_api_dk.json"
SCHEDULE_FILE = SCRIPT_DIR.parent / "nfl_schedule_2026.tsv"
OUTPUT_FILE = OUT_DIR / "team_weekly_implied_odds.csv"
GAMES_FILE = OUT_DIR / "game_implied_odds.csv"

WEEK_COLUMNS = [
    "Week 1",
    "Week 2",
    "Week 3",
    "Week 4",
    "Week 5",
    "Week 6",
    "Week 7",
    "Week 8",
    "Week 9",
    "Week 10",
    "Week 11",
    "Thanksgiving",
    "Week 12",
    "Week 13",
    "Week 14",
    "Week 15",
    "Christmas",
    "Week 16",
    "Week 17",
    "Week 18",
]

ABBR_TO_FULL: dict[str, str] = {
    "ARI": "Arizona Cardinals",
    "ATL": "Atlanta Falcons",
    "BAL": "Baltimore Ravens",
    "BUF": "Buffalo Bills",
    "CAR": "Carolina Panthers",
    "CHI": "Chicago Bears",
    "CIN": "Cincinnati Bengals",
    "CLE": "Cleveland Browns",
    "DAL": "Dallas Cowboys",
    "DEN": "Denver Broncos",
    "DET": "Detroit Lions",
    "GB": "Green Bay Packers",
    "HOU": "Houston Texans",
    "IND": "Indianapolis Colts",
    "JAX": "Jacksonville Jaguars",
    "KC": "Kansas City Chiefs",
    "LV": "Las Vegas Raiders",
    "LAC": "Los Angeles Chargers",
    "LAR": "Los Angeles Rams",
    "MIA": "Miami Dolphins",
    "MIN": "Minnesota Vikings",
    "NE": "New England Patriots",
    "NO": "New Orleans Saints",
    "NYG": "New York Giants",
    "NYJ": "New York Jets",
    "PHI": "Philadelphia Eagles",
    "PIT": "Pittsburgh Steelers",
    "SF": "San Francisco 49ers",
    "SEA": "Seattle Seahawks",
    "TB": "Tampa Bay Buccaneers",
    "TEN": "Tennessee Titans",
    "WAS": "Washington Commanders",
}

ODDS_API_TO_FULL: dict[str, str] = {
    name: name for name in ABBR_TO_FULL.values()
}


def american_to_implied_prob(odds: int) -> float:
    if odds > 0:
        return 100.0 / (odds + 100.0)
    return (-odds) / ((-odds) + 100.0)


def spread_to_implied_prob(spread: float) -> float:
    return 0.5 * (1.0 + math.erf((-spread) / (13.5 * math.sqrt(2.0))))


def implied_prob(ml: int | None, spread: float | None) -> float | None:
    if ml is not None:
        return american_to_implied_prob(ml)
    if spread is not None:
        return spread_to_implied_prob(spread)
    return None


def parse_odds_api(path: Path) -> list[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    events = payload["events"] if isinstance(payload, dict) and "events" in payload else payload
    games: list[dict] = []

    for event in events:
        away = ODDS_API_TO_FULL.get(event["away_team"], event["away_team"])
        home = ODDS_API_TO_FULL.get(event["home_team"], event["home_team"])
        bookmaker = next(
            (bk for bk in event.get("bookmakers", []) if bk.get("key") == "draftkings"),
            None,
        )
        if bookmaker is None:
            continue

        markets = {market["key"]: market for market in bookmaker.get("markets", [])}
        h2h = markets.get("h2h")
        spreads = markets.get("spreads")

        away_ml: int | None = None
        home_ml: int | None = None
        if h2h:
            for outcome in h2h["outcomes"]:
                if outcome["name"] == event["away_team"]:
                    away_ml = int(outcome["price"])
                elif outcome["name"] == event["home_team"]:
                    home_ml = int(outcome["price"])

        away_spread: float | None = None
        home_spread: float | None = None
        if spreads:
            for outcome in spreads["outcomes"]:
                if outcome["name"] == event["away_team"]:
                    away_spread = float(outcome["point"])
                elif outcome["name"] == event["home_team"]:
                    home_spread = float(outcome["point"])

        games.append(
            {
                "away": away,
                "home": home,
                "away_spread": away_spread,
                "home_spread": home_spread,
                "away_ml": away_ml,
                "home_ml": home_ml,
            }
        )

    return games


def team_win_prob(game: dict, team: str) -> float | None:
    if game["away"] == team:
        return implied_prob(game["away_ml"], game["away_spread"])
    if game["home"] == team:
        return implied_prob(game["home_ml"], game["home_spread"])
    return None


def build_game_index(games: list[dict]) -> dict[tuple[str, str], dict]:
    index: dict[tuple[str, str], dict] = {}
    for game in games:
        index[(game["away"], game["home"])] = game
    return index


def load_schedule(path: Path) -> dict[str, dict[str, str]]:
    schedule: dict[str, dict[str, str]] = {}
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        if reader.fieldnames is None:
            raise ValueError(f"No header in {path}")
        for row in reader:
            team = row["Team"].strip()
            schedule[team] = {col: (row.get(col) or "").strip() for col in WEEK_COLUMNS}
    return schedule


def parse_matchup_cell(cell: str, team: str) -> tuple[str, str] | None:
    cell = cell.strip()
    if not cell or cell.upper() == "BYE":
        return None
    if cell.startswith("@"):
        opponent = ABBR_TO_FULL[cell[1:]]
        return team, opponent
    opponent = ABBR_TO_FULL[cell]
    return opponent, team


def write_weekly_csv(
    schedule: dict[str, dict[str, str]],
    game_index: dict[tuple[str, str], dict],
    path: Path,
) -> tuple[int, int, list[str]]:
    missing: list[str] = []
    filled = 0
    total_slots = 0

    team_order = list(schedule.keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Team"] + WEEK_COLUMNS)
        for team in team_order:
            row: list[str] = [team]
            for week in WEEK_COLUMNS:
                cell = schedule[team][week]
                matchup = parse_matchup_cell(cell, team)
                if matchup is None:
                    row.append("")
                    continue
                total_slots += 1
                game = game_index.get(matchup)
                if game is None:
                    missing.append(f"{team} | {week} | {cell} | missing game {matchup}")
                    row.append("")
                    continue
                prob = team_win_prob(game, team)
                if prob is None:
                    missing.append(f"{team} | {week} | {cell} | no odds for {matchup}")
                    row.append("")
                    continue
                row.append(f"{prob * 100:.2f}")
                filled += 1
            writer.writerow(row)

    return filled, total_slots, missing


def write_games_csv(games: list[dict], path: Path) -> None:
    fieldnames = [
        "away",
        "home",
        "away_spread",
        "home_spread",
        "away_ml",
        "home_ml",
        "away_implied_pct",
        "home_implied_pct",
        "implied_sum_pct",
        "away_from",
        "home_from",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for game in games:
            away_from = "ml" if game["away_ml"] is not None else ("spread" if game["away_spread"] is not None else "")
            home_from = "ml" if game["home_ml"] is not None else ("spread" if game["home_spread"] is not None else "")
            away_p = implied_prob(game["away_ml"], game["away_spread"])
            home_p = implied_prob(game["home_ml"], game["home_spread"])
            writer.writerow(
                {
                    "away": game["away"],
                    "home": game["home"],
                    "away_spread": "" if game["away_spread"] is None else game["away_spread"],
                    "home_spread": "" if game["home_spread"] is None else game["home_spread"],
                    "away_ml": "" if game["away_ml"] is None else game["away_ml"],
                    "home_ml": "" if game["home_ml"] is None else game["home_ml"],
                    "away_implied_pct": "" if away_p is None else f"{away_p * 100:.2f}",
                    "home_implied_pct": "" if home_p is None else f"{home_p * 100:.2f}",
                    "implied_sum_pct": ""
                    if away_p is None or home_p is None
                    else f"{(away_p + home_p) * 100:.2f}",
                    "away_from": away_from,
                    "home_from": home_from,
                }
            )


def spot_check(games: list[dict]) -> None:
    index = build_game_index(games)

    def show(label: str, away: str, home: str) -> None:
        game = index.get((away, home)) or index.get((home, away))
        if game is None:
            print(f"{label}: MISSING")
            return
        away_p = team_win_prob(game, away)
        home_p = team_win_prob(game, home)
        print(
            f"{label}: {away} {game['away_ml']} ({away_p * 100:.2f}%) @ "
            f"{home} {game['home_ml']} ({home_p * 100:.2f}%)"
        )

    show("MIA@SF big fav", "Miami Dolphins", "San Francisco 49ers")
    show("CAR@ATL juice", "Carolina Panthers", "Atlanta Falcons")
    show("CIN@HOU", "Cincinnati Bengals", "Houston Texans")


def main() -> None:
    games = parse_odds_api(INPUT_FILE)
    if not games:
        raise SystemExit(f"No games parsed from {INPUT_FILE}")

    schedule = load_schedule(SCHEDULE_FILE)
    game_index = build_game_index(games)
    filled, total_slots, missing = write_weekly_csv(schedule, game_index, OUTPUT_FILE)
    write_games_csv(games, GAMES_FILE)

    print(f"Parsed {len(games)} games from {INPUT_FILE.name}")
    print(f"Schedule teams: {len(schedule)}")
    print(f"Filled week cells: {filled} / {total_slots}")
    print(f"Wrote {OUTPUT_FILE}")
    print(f"Wrote {GAMES_FILE}")
    spot_check(games)
    if missing:
        print(f"Missing lookups: {len(missing)}")
        for item in missing[:15]:
            print(f"  - {item}")
        if len(missing) > 15:
            print(f"  ... and {len(missing) - 15} more")


if __name__ == "__main__":
    main()
