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

SEP9_RANK = {'Los Angeles Rams': 1, 'Seattle Seahawks': 2, 'Buffalo Bills': 3, 'Baltimore Ravens': 4, 'Denver Broncos': 5, 'Philadelphia Eagles': 6, 'New England Patriots': 7, 'Houston Texans': 8, 'Los Angeles Chargers': 9, 'Dallas Cowboys': 10, 'Kansas City Chiefs': 11, 'Jacksonville Jaguars': 12, 'Green Bay Packers': 13, 'San Francisco 49ers': 14, 'Cincinnati Bengals': 15, 'Chicago Bears': 16, 'Detroit Lions': 17, 'Minnesota Vikings': 18, 'Tampa Bay Buccaneers': 19, 'Indianapolis Colts': 20, 'Pittsburgh Steelers': 21, 'New York Giants': 22, 'Carolina Panthers': 23, 'New Orleans Saints': 24, 'Washington Commanders': 25, 'Atlanta Falcons': 26, 'Tennessee Titans': 27, 'Las Vegas Raiders': 28, 'New York Jets': 29, 'Arizona Cardinals': 30, 'Cleveland Browns': 31, 'Miami Dolphins': 32}



# Rank 1-32. Optional sb_odds is American Super Bowl price quoted on that page.
SOURCES: list[dict] = [{'date': '2026-09-15', 'id': 'espn_fpi', 'label': 'ESPN_FPI', 'note': 'Live 2026 FPI table fetched Sep 15 (lastUpdated 2026-09-15T06:00Z). SEA 27th is the model after a low-scoring Lock start, not a writer list.', 'outlet': 'ESPN FPI', 'url': 'https://www.espn.com/nfl/fpi', 'teams': ['San Francisco 49ers', 'Buffalo Bills', 'Baltimore Ravens', 'Kansas City Chiefs', 'Jacksonville Jaguars', 'Los Angeles Rams', 'Chicago Bears', 'Houston Texans', 'Dallas Cowboys', 'Cincinnati Bengals', 'Detroit Lions', 'New England Patriots', 'Philadelphia Eagles', 'Green Bay Packers', 'Los Angeles Chargers', 'New York Giants', 'Tampa Bay Buccaneers', 'Minnesota Vikings', 'Washington Commanders', 'Denver Broncos', 'Pittsburgh Steelers', 'New Orleans Saints', 'Indianapolis Colts', 'Atlanta Falcons', 'Carolina Panthers', 'Arizona Cardinals', 'Seattle Seahawks', 'New York Jets', 'Las Vegas Raiders', 'Tennessee Titans', 'Cleveland Browns', 'Miami Dolphins']}, {'date': '2026-09-15', 'id': 'espn_panel', 'label': 'ESPN_panel', 'note': 'Week 2 power panel; TSN syndication of the ESPN 1-32', 'outlet': 'ESPN power panel', 'url': 'https://www.espn.com/nfl/story/_/id/49881711/power-rankings-week-2-all-teams-top-newcomers-debuts', 'teams': ['Buffalo Bills', 'Seattle Seahawks', 'Baltimore Ravens', 'Los Angeles Rams', 'San Francisco 49ers', 'Philadelphia Eagles', 'Chicago Bears', 'Kansas City Chiefs', 'Denver Broncos', 'New England Patriots', 'Houston Texans', 'Detroit Lions', 'Jacksonville Jaguars', 'Green Bay Packers', 'Cincinnati Bengals', 'Dallas Cowboys', 'Minnesota Vikings', 'New York Giants', 'Los Angeles Chargers', 'Tampa Bay Buccaneers', 'Pittsburgh Steelers', 'Indianapolis Colts', 'Washington Commanders', 'Arizona Cardinals', 'New Orleans Saints', 'Carolina Panthers', 'New York Jets', 'Las Vegas Raiders', 'Atlanta Falcons', 'Tennessee Titans', 'Miami Dolphins', 'Cleveland Browns']}, {'date': '2026-09-15', 'id': 'cbs_prisco', 'label': 'CBS_Prisco', 'note': 'Week 2 Prisco table after MNF', 'outlet': 'CBS Sports (Pete Prisco)', 'url': 'https://www.cbssports.com/nfl/news/priscos-nfl-week-2-power-rankings/', 'teams': ['Seattle Seahawks', 'Jacksonville Jaguars', 'Buffalo Bills', 'San Francisco 49ers', 'Los Angeles Rams', 'Baltimore Ravens', 'Philadelphia Eagles', 'Cincinnati Bengals', 'Chicago Bears', 'Kansas City Chiefs', 'Denver Broncos', 'Houston Texans', 'Minnesota Vikings', 'Green Bay Packers', 'Detroit Lions', 'New York Giants', 'Dallas Cowboys', 'Tampa Bay Buccaneers', 'New England Patriots', 'Pittsburgh Steelers', 'Los Angeles Chargers', 'Indianapolis Colts', 'New Orleans Saints', 'Arizona Cardinals', 'Carolina Panthers', 'Washington Commanders', 'New York Jets', 'Las Vegas Raiders', 'Atlanta Falcons', 'Tennessee Titans', 'Cleveland Browns', 'Miami Dolphins']}, {'date': '2026-09-15', 'id': 'fox_vacchiano', 'label': 'FOX_Vacchiano', 'note': 'Week 2 after MNF; Super Bowl odds quoted on page but not mixed into the rank average', 'outlet': 'FOX Sports (Ralph Vacchiano)', 'url': 'https://www.foxsports.com/stories/nfl/2026-nfl-power-rankings-week-2-which-teams-suffered-worst-opening-losses', 'teams': ['Baltimore Ravens', 'Chicago Bears', 'Seattle Seahawks', 'Buffalo Bills', 'Los Angeles Rams', 'Cincinnati Bengals', 'San Francisco 49ers', 'Denver Broncos', 'Philadelphia Eagles', 'New England Patriots', 'Jacksonville Jaguars', 'Kansas City Chiefs', 'Detroit Lions', 'Houston Texans', 'Minnesota Vikings', 'Pittsburgh Steelers', 'New York Giants', 'Green Bay Packers', 'New Orleans Saints', 'Los Angeles Chargers', 'Indianapolis Colts', 'Dallas Cowboys', 'Carolina Panthers', 'Tampa Bay Buccaneers', 'Arizona Cardinals', 'Washington Commanders', 'New York Jets', 'Atlanta Falcons', 'Las Vegas Raiders', 'Tennessee Titans', 'Cleveland Browns', 'Miami Dolphins']}, {'date': '2026-09-15', 'id': 'pft_florio', 'label': 'PFT_Florio', 'note': 'PFT Week 2 1-32 after MNF', 'outlet': 'Pro Football Talk (Mike Florio)', 'url': 'https://www.nbcsports.com/nfl/profootballtalk/rumor-mill/news/pfts-week-2-2026-nfl-power-rankings', 'teams': ['Seattle Seahawks', 'Buffalo Bills', 'Chicago Bears', 'Houston Texans', 'Jacksonville Jaguars', 'Baltimore Ravens', 'Cincinnati Bengals', 'Kansas City Chiefs', 'Philadelphia Eagles', 'San Francisco 49ers', 'Los Angeles Rams', 'Denver Broncos', 'New England Patriots', 'Detroit Lions', 'Minnesota Vikings', 'New York Giants', 'Pittsburgh Steelers', 'Arizona Cardinals', 'Los Angeles Chargers', 'Green Bay Packers', 'New Orleans Saints', 'Dallas Cowboys', 'Carolina Panthers', 'Tampa Bay Buccaneers', 'Indianapolis Colts', 'New York Jets', 'Las Vegas Raiders', 'Washington Commanders', 'Atlanta Falcons', 'Tennessee Titans', 'Miami Dolphins', 'Cleveland Browns']}, {'date': '2026-09-15', 'id': 'sporting_news', 'label': 'Sporting_News', 'note': 'Week 2 in-season 1-32', 'outlet': 'Sporting News (Vinnie Iyer)', 'url': 'https://www.sportingnews.com/us/nfl/news/nfl-power-rankings-bills-49ers-steelers-rams-chargers-week-2/c66ef9551cbc48cdb0a11d75', 'teams': ['Buffalo Bills', 'Chicago Bears', 'Baltimore Ravens', 'Seattle Seahawks', 'San Francisco 49ers', 'Philadelphia Eagles', 'Kansas City Chiefs', 'Jacksonville Jaguars', 'New England Patriots', 'Los Angeles Rams', 'Cincinnati Bengals', 'Detroit Lions', 'Pittsburgh Steelers', 'Denver Broncos', 'Minnesota Vikings', 'Houston Texans', 'New York Giants', 'Dallas Cowboys', 'Green Bay Packers', 'Arizona Cardinals', 'Las Vegas Raiders', 'New York Jets', 'Los Angeles Chargers', 'Washington Commanders', 'New Orleans Saints', 'Tampa Bay Buccaneers', 'Indianapolis Colts', 'Carolina Panthers', 'Tennessee Titans', 'Miami Dolphins', 'Atlanta Falcons', 'Cleveland Browns']}]

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
        sep9 = SEP9_RANK[row["Team"]]
        row["JuneRank"] = june
        row["Sep1Rank"] = sep1
        row["Sep9Rank"] = sep9
        row["RankDelta"] = sep9 - i

    source_path = HERE / "source_ranks.csv"
    with source_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Team", "Abbr"] + source_names)
        writer.writeheader()
        for row in sorted(team_rows, key=lambda r: r["Team"]):
            writer.writerow({k: row[k] for k in ["Team", "Abbr"] + source_names})

    consensus_path = HERE / "consensus_power_rankings.csv"
    fields = ["Rank", "Team", "Abbr", "Avg", "Best", "Worst", "Std", "JuneRank", "Sep1Rank", "Sep9Rank", "RankDelta"]
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
