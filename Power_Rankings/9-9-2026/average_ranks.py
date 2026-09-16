#!/usr/bin/env python3
"""Average in-window 1-32 lists into consensus_power_rankings.csv.

Also writes one CSV per source under sources/ so every list is auditable.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCES_DIR = HERE / "sources"

ABBR = {
    "Arizona Cardinals": "ARI",
    "Atlanta Falcons": "ATL",
    "Baltimore Ravens": "BAL",
    "Buffalo Bills": "BUF",
    "Carolina Panthers": "CAR",
    "Chicago Bears": "CHI",
    "Cincinnati Bengals": "CIN",
    "Cleveland Browns": "CLE",
    "Dallas Cowboys": "DAL",
    "Denver Broncos": "DEN",
    "Detroit Lions": "DET",
    "Green Bay Packers": "GB",
    "Houston Texans": "HOU",
    "Indianapolis Colts": "IND",
    "Jacksonville Jaguars": "JAX",
    "Kansas City Chiefs": "KC",
    "Las Vegas Raiders": "LV",
    "Los Angeles Chargers": "LAC",
    "Los Angeles Rams": "LAR",
    "Miami Dolphins": "MIA",
    "Minnesota Vikings": "MIN",
    "New England Patriots": "NE",
    "New Orleans Saints": "NO",
    "New York Giants": "NYG",
    "New York Jets": "NYJ",
    "Philadelphia Eagles": "PHI",
    "Pittsburgh Steelers": "PIT",
    "San Francisco 49ers": "SF",
    "Seattle Seahawks": "SEA",
    "Tampa Bay Buccaneers": "TB",
    "Tennessee Titans": "TEN",
    "Washington Commanders": "WAS",
}

# June 2026 17-list consensus rank (the pasted report).
JUNE_RANK = {
    "Los Angeles Rams": 1,
    "Seattle Seahawks": 2,
    "Buffalo Bills": 3,
    "Denver Broncos": 4,
    "Baltimore Ravens": 5,
    "New England Patriots": 6,
    "San Francisco 49ers": 7,
    "Philadelphia Eagles": 8,
    "Houston Texans": 9,
    "Chicago Bears": 10,
    "Green Bay Packers": 11,
    "Kansas City Chiefs": 12,
    "Detroit Lions": 13,
    "Los Angeles Chargers": 14,
    "Jacksonville Jaguars": 15,
    "Cincinnati Bengals": 16,
    "Dallas Cowboys": 17,
    "Tampa Bay Buccaneers": 18,
    "Pittsburgh Steelers": 19,
    "Carolina Panthers": 20,
    "Minnesota Vikings": 21,
    "Indianapolis Colts": 22,
    "Washington Commanders": 23,
    "New York Giants": 24,
    "New Orleans Saints": 25,
    "Atlanta Falcons": 26,
    "Tennessee Titans": 27,
    "Las Vegas Raiders": 28,
    "Cleveland Browns": 29,
    "New York Jets": 30,
    "Arizona Cardinals": 31,
    "Miami Dolphins": 32,
}

SEP1_RANK = {
    "Los Angeles Rams": 1,
    "Seattle Seahawks": 2,
    "Buffalo Bills": 3,
    "Denver Broncos": 4,
    "Baltimore Ravens": 5,
    "Philadelphia Eagles": 6,
    "Houston Texans": 7,
    "New England Patriots": 8,
    "Chicago Bears": 9,
    "San Francisco 49ers": 10,
    "Detroit Lions": 11,
    "Green Bay Packers": 12,
    "Los Angeles Chargers": 13,
    "Kansas City Chiefs": 14,
    "Jacksonville Jaguars": 15,
    "Cincinnati Bengals": 16,
    "Dallas Cowboys": 17,
    "Tampa Bay Buccaneers": 18,
    "Minnesota Vikings": 19,
    "Pittsburgh Steelers": 20,
    "Indianapolis Colts": 21,
    "Washington Commanders": 22,
    "Carolina Panthers": 23,
    "New Orleans Saints": 24,
    "New York Giants": 25,
    "Atlanta Falcons": 26,
    "Tennessee Titans": 27,
    "Las Vegas Raiders": 28,
    "New York Jets": 29,
    "Cleveland Browns": 30,
    "Arizona Cardinals": 31,
    "Miami Dolphins": 32,
}


# Rank 1-32. Optional sb_odds is American Super Bowl price quoted on that page.
SOURCES: list[dict] = [{'date': '2026-09-09',
  'id': 'espn_fpi',
  'label': 'ESPN_FPI',
  'note': 'Live 2026 FPI table fetched Sep 9 (0-0-0)',
  'outlet': 'ESPN FPI',
  'teams': ['Los Angeles Rams',
            'Buffalo Bills',
            'Seattle Seahawks',
            'Baltimore Ravens',
            'San Francisco 49ers',
            'Los Angeles Chargers',
            'Green Bay Packers',
            'Detroit Lions',
            'Kansas City Chiefs',
            'Philadelphia Eagles',
            'Dallas Cowboys',
            'Cincinnati Bengals',
            'Houston Texans',
            'New England Patriots',
            'Denver Broncos',
            'Jacksonville Jaguars',
            'Chicago Bears',
            'Tampa Bay Buccaneers',
            'Indianapolis Colts',
            'Minnesota Vikings',
            'Pittsburgh Steelers',
            'Washington Commanders',
            'New York Giants',
            'Atlanta Falcons',
            'New Orleans Saints',
            'Carolina Panthers',
            'Tennessee Titans',
            'Las Vegas Raiders',
            'New York Jets',
            'Cleveland Browns',
            'Arizona Cardinals',
            'Miami Dolphins'],
  'url': 'https://www.espn.com/nfl/fpi'},
 {'date': '2026-09-08',
  'id': 'nfl_com',
  'label': 'NFL_com',
  'note': 'Week 1 regular-season edition',
  'outlet': 'NFL.com (Nick Shook)',
  'teams': ['Los Angeles Rams',
            'Denver Broncos',
            'Seattle Seahawks',
            'Buffalo Bills',
            'Philadelphia Eagles',
            'Baltimore Ravens',
            'Cincinnati Bengals',
            'Dallas Cowboys',
            'Jacksonville Jaguars',
            'Houston Texans',
            'Chicago Bears',
            'Green Bay Packers',
            'New England Patriots',
            'Kansas City Chiefs',
            'Detroit Lions',
            'Los Angeles Chargers',
            'San Francisco 49ers',
            'Tampa Bay Buccaneers',
            'Minnesota Vikings',
            'Indianapolis Colts',
            'Pittsburgh Steelers',
            'New Orleans Saints',
            'Carolina Panthers',
            'Tennessee Titans',
            'Arizona Cardinals',
            'New York Giants',
            'Atlanta Falcons',
            'New York Jets',
            'Las Vegas Raiders',
            'Cleveland Browns',
            'Washington Commanders',
            'Miami Dolphins'],
  'url': 'https://www.nfl.com/news/nfl-power-rankings-week-1-2026-nfl-season'},
 {'date': '2026-09-08',
  'id': 'thescore',
  'label': 'theScore',
  'note': 'Week 1 entering regular season',
  'outlet': 'theScore',
  'teams': ['Los Angeles Rams',
            'Seattle Seahawks',
            'New England Patriots',
            'Buffalo Bills',
            'Chicago Bears',
            'Denver Broncos',
            'Philadelphia Eagles',
            'Baltimore Ravens',
            'Kansas City Chiefs',
            'Jacksonville Jaguars',
            'San Francisco 49ers',
            'Houston Texans',
            'Dallas Cowboys',
            'Los Angeles Chargers',
            'Minnesota Vikings',
            'Cincinnati Bengals',
            'Detroit Lions',
            'Green Bay Packers',
            'New York Giants',
            'Pittsburgh Steelers',
            'Indianapolis Colts',
            'New Orleans Saints',
            'Washington Commanders',
            'Tampa Bay Buccaneers',
            'Carolina Panthers',
            'Tennessee Titans',
            'Las Vegas Raiders',
            'Atlanta Falcons',
            'New York Jets',
            'Cleveland Browns',
            'Arizona Cardinals',
            'Miami Dolphins'],
  'url': 'https://www.thescore.com/nfl/news/3572167/nfl-power-rankings-week-1-where-does-your-team-stand'},
 {'date': '2026-09-08',
  'id': 'pff',
  'label': 'PFF',
  'note': 'PFF holistic power rankings model',
  'outlet': 'Pro Football Focus',
  'teams': ['Los Angeles Rams',
            'Seattle Seahawks',
            'Buffalo Bills',
            'Baltimore Ravens',
            'Los Angeles Chargers',
            'Houston Texans',
            'Philadelphia Eagles',
            'New England Patriots',
            'Denver Broncos',
            'Detroit Lions',
            'San Francisco 49ers',
            'Kansas City Chiefs',
            'Green Bay Packers',
            'Jacksonville Jaguars',
            'Chicago Bears',
            'Dallas Cowboys',
            'Minnesota Vikings',
            'Cincinnati Bengals',
            'Pittsburgh Steelers',
            'Tampa Bay Buccaneers',
            'Indianapolis Colts',
            'Washington Commanders',
            'New York Giants',
            'Atlanta Falcons',
            'Carolina Panthers',
            'New Orleans Saints',
            'Tennessee Titans',
            'Las Vegas Raiders',
            'Cleveland Browns',
            'New York Jets',
            'Arizona Cardinals',
            'Miami Dolphins'],
  'url': 'https://www.pff.com/news/2026-nfl-week-1-power-rankings-rams-seahawks-begin-season-on-top'},
 {'date': '2026-09-08',
  'id': 'cbs_prisco',
  'label': 'CBS_Prisco',
  'note': 'Week 1 Prisco table',
  'outlet': 'CBS Sports (Pete Prisco)',
  'teams': ['Seattle Seahawks',
            'Los Angeles Rams',
            'Jacksonville Jaguars',
            'Buffalo Bills',
            'Dallas Cowboys',
            'Denver Broncos',
            'Green Bay Packers',
            'Cincinnati Bengals',
            'Baltimore Ravens',
            'San Francisco 49ers',
            'Houston Texans',
            'Kansas City Chiefs',
            'Philadelphia Eagles',
            'Tampa Bay Buccaneers',
            'Chicago Bears',
            'New England Patriots',
            'Los Angeles Chargers',
            'Minnesota Vikings',
            'Detroit Lions',
            'Pittsburgh Steelers',
            'Indianapolis Colts',
            'New York Giants',
            'Carolina Panthers',
            'New Orleans Saints',
            'Atlanta Falcons',
            'Washington Commanders',
            'New York Jets',
            'Tennessee Titans',
            'Las Vegas Raiders',
            'Arizona Cardinals',
            'Cleveland Browns',
            'Miami Dolphins'],
  'url': 'https://www.cbssports.com/nfl/news/priscos-nfl-week-1-power-rankings-jaguars-cowboys-deserve-attention-rams-super-team-too-good-to-be-true/'},
 {'date': '2026-09-03',
  'id': 'sharp_football',
  'label': 'Sharp_Football',
  'note': 'Updated weekly table entering Week 1',
  'outlet': 'Sharp Football Analysis',
  'teams': ['Los Angeles Rams',
            'Buffalo Bills',
            'Seattle Seahawks',
            'Green Bay Packers',
            'Los Angeles Chargers',
            'Denver Broncos',
            'Houston Texans',
            'Baltimore Ravens',
            'Philadelphia Eagles',
            'New England Patriots',
            'Cincinnati Bengals',
            'Dallas Cowboys',
            'San Francisco 49ers',
            'Kansas City Chiefs',
            'Detroit Lions',
            'Jacksonville Jaguars',
            'Chicago Bears',
            'Tampa Bay Buccaneers',
            'Minnesota Vikings',
            'Pittsburgh Steelers',
            'Indianapolis Colts',
            'Carolina Panthers',
            'Washington Commanders',
            'New York Giants',
            'New York Jets',
            'New Orleans Saints',
            'Tennessee Titans',
            'Atlanta Falcons',
            'Las Vegas Raiders',
            'Arizona Cardinals',
            'Cleveland Browns',
            'Miami Dolphins'],
  'url': 'https://www.sharpfootballanalysis.com/analysis/nfl-power-rankings/'},
 {'date': '2026-09-07',
  'id': 'si_betting',
  'label': 'SI_betting',
  'note': 'Writer order informed by Super Bowl odds; odds stored on this file',
  'outlet': 'SI Betting',
  'sb_odds': [500,
              1200,
              1000,
              1700,
              1000,
              1800,
              2000,
              1600,
              1900,
              2400,
              1900,
              1800,
              2000,
              3000,
              2500,
              1700,
              1800,
              5500,
              5000,
              6000,
              5000,
              9000,
              6000,
              9000,
              7000,
              13000,
              13000,
              20000,
              15000,
              20000,
              35000,
              50000],
  'teams': ['Los Angeles Rams',
            'Seattle Seahawks',
            'Baltimore Ravens',
            'Philadelphia Eagles',
            'Buffalo Bills',
            'New England Patriots',
            'Denver Broncos',
            'Kansas City Chiefs',
            'Detroit Lions',
            'Chicago Bears',
            'San Francisco 49ers',
            'Houston Texans',
            'Green Bay Packers',
            'Jacksonville Jaguars',
            'Dallas Cowboys',
            'Los Angeles Chargers',
            'Cincinnati Bengals',
            'Tampa Bay Buccaneers',
            'Minnesota Vikings',
            'Indianapolis Colts',
            'Pittsburgh Steelers',
            'Carolina Panthers',
            'Washington Commanders',
            'New Orleans Saints',
            'New York Giants',
            'Atlanta Falcons',
            'Tennessee Titans',
            'New York Jets',
            'Las Vegas Raiders',
            'Cleveland Browns',
            'Miami Dolphins',
            'Arizona Cardinals'],
  'url': 'https://www.si.com/betting/nfl-power-rankings-based-on-super-bowl-odds-ahead-of-week-1-rams-enter-season-as-favorite-17-teams-inside-30-1'},
 {'date': '2026-09-07',
  'id': 'yahoo_schwab',
  'label': 'Yahoo_Schwab',
  'note': 'Week 1 edition; independent Schwab list',
  'outlet': 'Yahoo Sports (Frank Schwab)',
  'teams': ['Los Angeles Rams',
            'Seattle Seahawks',
            'Buffalo Bills',
            'Denver Broncos',
            'New England Patriots',
            'Baltimore Ravens',
            'Dallas Cowboys',
            'Philadelphia Eagles',
            'Detroit Lions',
            'Houston Texans',
            'Chicago Bears',
            'Kansas City Chiefs',
            'Los Angeles Chargers',
            'Jacksonville Jaguars',
            'Cincinnati Bengals',
            'San Francisco 49ers',
            'Green Bay Packers',
            'Minnesota Vikings',
            'Indianapolis Colts',
            'Pittsburgh Steelers',
            'Tampa Bay Buccaneers',
            'Washington Commanders',
            'New Orleans Saints',
            'New York Giants',
            'Carolina Panthers',
            'Las Vegas Raiders',
            'Tennessee Titans',
            'Atlanta Falcons',
            'New York Jets',
            'Cleveland Browns',
            'Arizona Cardinals',
            'Miami Dolphins'],
  'url': 'https://sports.yahoo.com/article/nfl-power-rankings-are-the-bills-and-josh-allen-the-biggest-threat-to-the-rams-reign-071327328.html'},
 {'date': '2026-09-08',
  'id': 'fox_vacchiano',
  'label': 'FOX_Vacchiano',
  'note': 'Week 1 entering regular season',
  'outlet': 'FOX Sports (Ralph Vacchiano)',
  'teams': ['Los Angeles Rams',
            'Denver Broncos',
            'Baltimore Ravens',
            'Seattle Seahawks',
            'New England Patriots',
            'Chicago Bears',
            'Buffalo Bills',
            'Cincinnati Bengals',
            'Philadelphia Eagles',
            'San Francisco 49ers',
            'Houston Texans',
            'Jacksonville Jaguars',
            'Detroit Lions',
            'Los Angeles Chargers',
            'Kansas City Chiefs',
            'Green Bay Packers',
            'Dallas Cowboys',
            'Minnesota Vikings',
            'Indianapolis Colts',
            'Pittsburgh Steelers',
            'Carolina Panthers',
            'Tampa Bay Buccaneers',
            'New York Giants',
            'Atlanta Falcons',
            'New Orleans Saints',
            'Washington Commanders',
            'Tennessee Titans',
            'New York Jets',
            'Las Vegas Raiders',
            'Cleveland Browns',
            'Arizona Cardinals',
            'Miami Dolphins'],
  'url': 'https://www.foxsports.com/stories/nfl/2026-nfl-power-rankings-where-every-team-stands-heading-season'},
 {'date': '2026-09-07',
  'id': 'the_ringer',
  'label': 'The_Ringer',
  'note': 'Preseason/Week 1 entering regular season',
  'outlet': 'The Ringer (Diante Lee)',
  'teams': ['Los Angeles Rams',
            'Seattle Seahawks',
            'Denver Broncos',
            'Houston Texans',
            'Buffalo Bills',
            'New England Patriots',
            'Baltimore Ravens',
            'Philadelphia Eagles',
            'Los Angeles Chargers',
            'Cincinnati Bengals',
            'Jacksonville Jaguars',
            'Green Bay Packers',
            'Kansas City Chiefs',
            'Dallas Cowboys',
            'San Francisco 49ers',
            'Detroit Lions',
            'Chicago Bears',
            'Tampa Bay Buccaneers',
            'Pittsburgh Steelers',
            'Indianapolis Colts',
            'Minnesota Vikings',
            'Carolina Panthers',
            'New Orleans Saints',
            'New York Giants',
            'Atlanta Falcons',
            'Las Vegas Raiders',
            'Arizona Cardinals',
            'Tennessee Titans',
            'Washington Commanders',
            'New York Jets',
            'Cleveland Browns',
            'Miami Dolphins'],
  'url': 'https://www.theringer.com/2026/09/07/nfl/nfl-power-rankings-2026-preseason-rams-seahawks-broncos'}]



def ranks_from_order(order: list[str], src_id: str) -> dict[str, int]:
    if len(order) != 32:
        raise SystemExit(f"{src_id}: list length {len(order)} != 32")
    if len(set(order)) != 32:
        raise SystemExit(f"{src_id}: duplicate or missing team")
    missing = set(ABBR) - set(order)
    extra = set(order) - set(ABBR)
    if missing or extra:
        raise SystemExit(f"{src_id}: name mismatch missing={missing} extra={extra}")
    return {team: i + 1 for i, team in enumerate(order)}


def stdev(values: list[float]) -> float:
    n = len(values)
    mean = sum(values) / n
    var = sum((x - mean) ** 2 for x in values) / n
    return math.sqrt(var)


def write_source_files() -> None:
    SOURCES_DIR.mkdir(exist_ok=True)
    manifest_path = SOURCES_DIR / "manifest.csv"
    with manifest_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id", "label", "outlet", "date", "url", "has_sb_odds", "note"],
        )
        writer.writeheader()
        for src in SOURCES:
            writer.writerow(
                {
                    "id": src["id"],
                    "label": src["label"],
                    "outlet": src["outlet"],
                    "date": src["date"],
                    "url": src["url"],
                    "has_sb_odds": "yes" if src.get("sb_odds") else "no",
                    "note": src["note"],
                }
            )

    for src in SOURCES:
        path = SOURCES_DIR / f"{src['id']}.csv"
        fieldnames = ["Rank", "Team", "Abbr"]
        if src.get("sb_odds"):
            fieldnames.append("SB_odds")
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            odds = src.get("sb_odds")
            if odds and len(odds) != 32:
                raise SystemExit(f"{src['id']}: sb_odds length {len(odds)} != 32")
            for i, team in enumerate(src["teams"]):
                row = {"Rank": i + 1, "Team": team, "Abbr": ABBR[team]}
                if odds:
                    row["SB_odds"] = odds[i]
                writer.writerow(row)


def main() -> None:
    source_ranks = {
        src["label"]: ranks_from_order(src["teams"], src["id"]) for src in SOURCES
    }
    source_names = [src["label"] for src in SOURCES]
    write_source_files()

    team_rows: list[dict] = []
    for team in ABBR:
        ranks = [source_ranks[src][team] for src in source_names]
        avg = sum(ranks) / len(ranks)
        team_rows.append(
            {
                "Team": team,
                "Abbr": ABBR[team],
                "Avg": avg,
                "Best": min(ranks),
                "Worst": max(ranks),
                "Std": stdev(ranks),
                **{src: source_ranks[src][team] for src in source_names},
            }
        )

    team_rows.sort(key=lambda r: (r["Avg"], r["Best"], r["Team"]))
    for i, row in enumerate(team_rows, start=1):
        row["Rank"] = i
        june = JUNE_RANK[row["Team"]]
        sep1 = SEP1_RANK[row["Team"]]
        row["JuneRank"] = june
        row["Sep1Rank"] = sep1
        row["RankDelta"] = sep1 - i

    source_path = HERE / "source_ranks.csv"
    with source_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Team", "Abbr"] + source_names)
        writer.writeheader()
        for row in sorted(team_rows, key=lambda r: r["Team"]):
            writer.writerow({k: row[k] for k in ["Team", "Abbr"] + source_names})

    consensus_path = HERE / "consensus_power_rankings.csv"
    fields = ["Rank", "Team", "Abbr", "Avg", "Best", "Worst", "Std", "JuneRank", "Sep1Rank", "RankDelta"]
    with consensus_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in team_rows:
            out = {k: row[k] for k in fields}
            out["Avg"] = f"{row['Avg']:.2f}"
            out["Std"] = f"{row['Std']:.2f}"
            writer.writerow(out)

    odds_sources = [src for src in SOURCES if src.get("sb_odds")]
    odds_path = HERE / "source_sb_odds.csv"
    with odds_path.open("w", newline="", encoding="utf-8") as f:
        fieldnames = ["Team", "Abbr"] + [src["label"] for src in odds_sources]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for team in sorted(ABBR):
            row = {"Team": team, "Abbr": ABBR[team]}
            for src in odds_sources:
                idx = src["teams"].index(team)
                row[src["label"]] = src["sb_odds"][idx]
            writer.writerow(row)

    print(f"sources: {len(source_names)}")
    print(f"wrote {SOURCES_DIR / 'manifest.csv'}")
    print(f"wrote {len(SOURCES)} files in {SOURCES_DIR}")
    print(f"wrote {source_path}")
    print(f"wrote {odds_path}")
    print(f"wrote {consensus_path}")
    for row in team_rows[:5]:
        print(f"  {row['Rank']:2d} {row['Abbr']:3s} avg={row['Avg']:.2f} delta={row['RankDelta']:+d}")


if __name__ == "__main__":
    main()
