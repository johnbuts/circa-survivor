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

# Rank 1-32. Optional sb_odds is American Super Bowl price quoted on that page.
SOURCES: list[dict] = [
    {
        "id": "espn_panel",
        "label": "ESPN_panel",
        "outlet": "ESPN power panel",
        "date": "2026-09-01",
        "url": "https://www.espn.com/nfl/story/_/id/49754534/2026-nfl-power-rankings-preseason-milestones",
        "note": "Final cuts / Week 1 panel",
        "teams": [
            "Los Angeles Rams",
            "Seattle Seahawks",
            "Buffalo Bills",
            "Denver Broncos",
            "Philadelphia Eagles",
            "New England Patriots",
            "Green Bay Packers",
            "Baltimore Ravens",
            "San Francisco 49ers",
            "Houston Texans",
            "Detroit Lions",
            "Chicago Bears",
            "Kansas City Chiefs",
            "Los Angeles Chargers",
            "Dallas Cowboys",
            "Cincinnati Bengals",
            "Jacksonville Jaguars",
            "Tampa Bay Buccaneers",
            "Indianapolis Colts",
            "Washington Commanders",
            "Pittsburgh Steelers",
            "Minnesota Vikings",
            "Carolina Panthers",
            "New York Giants",
            "New Orleans Saints",
            "Atlanta Falcons",
            "Las Vegas Raiders",
            "Tennessee Titans",
            "New York Jets",
            "Arizona Cardinals",
            "Cleveland Browns",
            "Miami Dolphins",
        ],
    },
    {
        "id": "sportsnaut",
        "label": "Sportsnaut",
        "outlet": "Sportsnaut",
        "date": "2026-08-31",
        "url": "https://sportsnaut.com/nfl/2026-nfl-power-rankings-after-preseason",
        "note": "Post-preseason (preseason wrapped Saturday Aug 29)",
        "teams": [
            "Los Angeles Rams",
            "Seattle Seahawks",
            "Houston Texans",
            "Baltimore Ravens",
            "Philadelphia Eagles",
            "Buffalo Bills",
            "Denver Broncos",
            "New England Patriots",
            "Detroit Lions",
            "Green Bay Packers",
            "Los Angeles Chargers",
            "Dallas Cowboys",
            "San Francisco 49ers",
            "Jacksonville Jaguars",
            "Cincinnati Bengals",
            "Chicago Bears",
            "Kansas City Chiefs",
            "Tampa Bay Buccaneers",
            "Minnesota Vikings",
            "Pittsburgh Steelers",
            "New Orleans Saints",
            "New York Giants",
            "Indianapolis Colts",
            "Carolina Panthers",
            "Las Vegas Raiders",
            "Washington Commanders",
            "Tennessee Titans",
            "Atlanta Falcons",
            "Arizona Cardinals",
            "New York Jets",
            "Miami Dolphins",
            "Cleveland Browns",
        ],
    },
    {
        "id": "nfl_spin_zone",
        "label": "NFL_Spin_Zone",
        "outlet": "NFL Spin Zone",
        "date": "2026-09-01",
        "url": "https://nflspinzone.com/nfl-power-rankings-updated-league-rankings-after-roster-cuts-01m1cszfw3z0",
        "note": "After roster cuts",
        "teams": [
            "Los Angeles Rams",
            "Seattle Seahawks",
            "Denver Broncos",
            "Buffalo Bills",
            "Houston Texans",
            "New England Patriots",
            "Chicago Bears",
            "Green Bay Packers",
            "Philadelphia Eagles",
            "Detroit Lions",
            "Baltimore Ravens",
            "Jacksonville Jaguars",
            "Los Angeles Chargers",
            "San Francisco 49ers",
            "Dallas Cowboys",
            "Indianapolis Colts",
            "Kansas City Chiefs",
            "Cincinnati Bengals",
            "Tampa Bay Buccaneers",
            "Pittsburgh Steelers",
            "New York Giants",
            "Carolina Panthers",
            "New Orleans Saints",
            "Minnesota Vikings",
            "Washington Commanders",
            "Atlanta Falcons",
            "New York Jets",
            "Tennessee Titans",
            "Las Vegas Raiders",
            "Arizona Cardinals",
            "Miami Dolphins",
            "Cleveland Browns",
        ],
    },
    {
        "id": "si_betting",
        "label": "SI_betting",
        "outlet": "SI Betting",
        "date": "2026-08-31",
        "url": "https://www.si.com/betting/nfl-power-rankings-based-on-super-bowl-odds-following-preseason-examining-top-contenders-to-win-in-2026",
        "note": "Writer order informed by Super Bowl odds; odds stored on this file",
        "teams": [
            "Los Angeles Rams",
            "Seattle Seahawks",
            "Baltimore Ravens",
            "Philadelphia Eagles",
            "New England Patriots",
            "Buffalo Bills",
            "Denver Broncos",
            "Kansas City Chiefs",
            "Detroit Lions",
            "Green Bay Packers",
            "Chicago Bears",
            "San Francisco 49ers",
            "Jacksonville Jaguars",
            "Houston Texans",
            "Dallas Cowboys",
            "Los Angeles Chargers",
            "Cincinnati Bengals",
            "Tampa Bay Buccaneers",
            "Minnesota Vikings",
            "Indianapolis Colts",
            "Pittsburgh Steelers",
            "Carolina Panthers",
            "Washington Commanders",
            "New Orleans Saints",
            "New York Giants",
            "Atlanta Falcons",
            "Tennessee Titans",
            "New York Jets",
            "Las Vegas Raiders",
            "Cleveland Browns",
            "Miami Dolphins",
            "Arizona Cardinals",
        ],
        "sb_odds": [
            500, 1200, 1000, 1700, 1800, 1000, 2000, 1600, 1900, 2000,
            2400, 1900, 3000, 1800, 2500, 1700, 1800, 5500, 5000, 6000,
            5000, 9000, 6000, 9000, 7000, 13000, 13000, 20000, 15000, 20000,
            35000, 50000,
        ],
    },
    {
        "id": "espn_fpi",
        "label": "ESPN_FPI",
        "outlet": "ESPN FPI",
        "date": "2026-09-01",
        "url": "https://www.espn.com/nfl/fpi",
        "note": "Live 2026 FPI table fetched Sep 1 (0-0-0)",
        "teams": [
            "Los Angeles Rams",
            "Buffalo Bills",
            "Seattle Seahawks",
            "Baltimore Ravens",
            "San Francisco 49ers",
            "Los Angeles Chargers",
            "Green Bay Packers",
            "Detroit Lions",
            "Kansas City Chiefs",
            "Philadelphia Eagles",
            "Dallas Cowboys",
            "Cincinnati Bengals",
            "Houston Texans",
            "New England Patriots",
            "Denver Broncos",
            "Jacksonville Jaguars",
            "Chicago Bears",
            "Tampa Bay Buccaneers",
            "Indianapolis Colts",
            "Minnesota Vikings",
            "Pittsburgh Steelers",
            "Washington Commanders",
            "New York Giants",
            "Atlanta Falcons",
            "New Orleans Saints",
            "Carolina Panthers",
            "Tennessee Titans",
            "Las Vegas Raiders",
            "New York Jets",
            "Cleveland Browns",
            "Arizona Cardinals",
            "Miami Dolphins",
        ],
    },
    {
        "id": "sporting_news",
        "label": "Sporting_News",
        "outlet": "Sporting News (Vinnie Iyer)",
        "date": "2026-08-17",
        "url": "https://www.sportingnews.com/us/nfl/news/nfl-preseason-power-rankings-bills-bears-rams-seahawks-patriots/2cb00c83ca025c07de32c837",
        "note": "Preseason edition; latest SN 1-32",
        "teams": [
            "Los Angeles Rams",
            "Buffalo Bills",
            "Chicago Bears",
            "Seattle Seahawks",
            "Kansas City Chiefs",
            "Baltimore Ravens",
            "Philadelphia Eagles",
            "San Francisco 49ers",
            "New England Patriots",
            "Los Angeles Chargers",
            "Denver Broncos",
            "Jacksonville Jaguars",
            "Houston Texans",
            "Cincinnati Bengals",
            "Green Bay Packers",
            "Detroit Lions",
            "Dallas Cowboys",
            "Pittsburgh Steelers",
            "New York Giants",
            "Washington Commanders",
            "Minnesota Vikings",
            "New Orleans Saints",
            "Tampa Bay Buccaneers",
            "Indianapolis Colts",
            "Las Vegas Raiders",
            "Tennessee Titans",
            "Carolina Panthers",
            "Arizona Cardinals",
            "New York Jets",
            "Atlanta Falcons",
            "Miami Dolphins",
            "Cleveland Browns",
        ],
    },
    {
        "id": "sharp_football",
        "label": "Sharp_Football",
        "outlet": "Sharp Football Analysis",
        "date": "2026-08-24",
        "url": "https://www.sharpfootballanalysis.com/analysis/nfl-power-rankings/",
        "note": "Aug 24 update; Super Bowl odds stored on this file",
        "teams": [
            "Los Angeles Rams",
            "Buffalo Bills",
            "Seattle Seahawks",
            "Green Bay Packers",
            "Los Angeles Chargers",
            "Denver Broncos",
            "Houston Texans",
            "Baltimore Ravens",
            "Philadelphia Eagles",
            "New England Patriots",
            "Cincinnati Bengals",
            "San Francisco 49ers",
            "Kansas City Chiefs",
            "Detroit Lions",
            "Jacksonville Jaguars",
            "Dallas Cowboys",
            "Chicago Bears",
            "Tampa Bay Buccaneers",
            "Minnesota Vikings",
            "Pittsburgh Steelers",
            "Indianapolis Colts",
            "Carolina Panthers",
            "Washington Commanders",
            "New York Giants",
            "New Orleans Saints",
            "Tennessee Titans",
            "New York Jets",
            "Atlanta Falcons",
            "Las Vegas Raiders",
            "Arizona Cardinals",
            "Cleveland Browns",
            "Miami Dolphins",
        ],
        "sb_odds": [
            550, 1000, 1100, 1800, 1700, 2000, 1800, 1000, 1600, 1600,
            2000, 1900, 1600, 1900, 3000, 2500, 2400, 5000, 5000, 5000,
            6000, 9000, 6000, 7000, 9000, 13000, 20000, 13000, 15000, 50000,
            20000, 35000,
        ],
    },
    {
        "id": "fansided",
        "label": "FanSided",
        "outlet": "FanSided",
        "date": "2026-08-22",
        "url": "https://fansided.com/nfl/nfl-power-rankings-after-two-weeks-of-the-preseason-injuries-and-more",
        "note": "After two weeks of preseason",
        "teams": [
            "Los Angeles Rams",
            "Seattle Seahawks",
            "Denver Broncos",
            "Chicago Bears",
            "Kansas City Chiefs",
            "Philadelphia Eagles",
            "Buffalo Bills",
            "Baltimore Ravens",
            "Los Angeles Chargers",
            "Dallas Cowboys",
            "Cincinnati Bengals",
            "Jacksonville Jaguars",
            "Houston Texans",
            "Green Bay Packers",
            "New England Patriots",
            "Carolina Panthers",
            "Minnesota Vikings",
            "Detroit Lions",
            "San Francisco 49ers",
            "Tampa Bay Buccaneers",
            "New Orleans Saints",
            "Pittsburgh Steelers",
            "Washington Commanders",
            "Indianapolis Colts",
            "New York Giants",
            "Las Vegas Raiders",
            "Miami Dolphins",
            "New York Jets",
            "Atlanta Falcons",
            "Cleveland Browns",
            "Arizona Cardinals",
            "Tennessee Titans",
        ],
    },
    {
        "id": "usa_today",
        "label": "USA_Today",
        "outlet": "USA Today (Nate Davis)",
        "date": "2026-08-06",
        "url": "https://www.usatoday.com/story/sports/nfl/columnist/nate-davis/2026/08/06/nfl-power-rankings-preseason-super-bowl/91193311007/",
        "note": "Entering preseason",
        "teams": [
            "Los Angeles Rams",
            "Seattle Seahawks",
            "Denver Broncos",
            "Buffalo Bills",
            "Chicago Bears",
            "Houston Texans",
            "San Francisco 49ers",
            "Cincinnati Bengals",
            "Dallas Cowboys",
            "Detroit Lions",
            "New England Patriots",
            "Kansas City Chiefs",
            "Baltimore Ravens",
            "Green Bay Packers",
            "Jacksonville Jaguars",
            "Los Angeles Chargers",
            "Minnesota Vikings",
            "Washington Commanders",
            "Philadelphia Eagles",
            "New Orleans Saints",
            "Pittsburgh Steelers",
            "Tampa Bay Buccaneers",
            "New York Giants",
            "Carolina Panthers",
            "Atlanta Falcons",
            "Tennessee Titans",
            "Cleveland Browns",
            "Las Vegas Raiders",
            "Indianapolis Colts",
            "New York Jets",
            "Arizona Cardinals",
            "Miami Dolphins",
        ],
    },
    {
        "id": "athletic",
        "label": "Athletic",
        "outlet": "The Athletic (Josh Kendall)",
        "date": "2026-08-08",
        "url": "https://www.nytimes.com/athletic/7464171/2026/07/28/nfl-power-rankings-training-camp-rams-seahawks/",
        "note": "Published Jul 28, updated Aug 8",
        "teams": [
            "Los Angeles Rams",
            "Denver Broncos",
            "Buffalo Bills",
            "New England Patriots",
            "Seattle Seahawks",
            "Houston Texans",
            "San Francisco 49ers",
            "Los Angeles Chargers",
            "Philadelphia Eagles",
            "Detroit Lions",
            "Jacksonville Jaguars",
            "Chicago Bears",
            "Dallas Cowboys",
            "Cincinnati Bengals",
            "Green Bay Packers",
            "Baltimore Ravens",
            "Pittsburgh Steelers",
            "Kansas City Chiefs",
            "Tampa Bay Buccaneers",
            "Minnesota Vikings",
            "Indianapolis Colts",
            "Carolina Panthers",
            "Washington Commanders",
            "Atlanta Falcons",
            "New Orleans Saints",
            "Las Vegas Raiders",
            "Cleveland Browns",
            "New York Giants",
            "Tennessee Titans",
            "Arizona Cardinals",
            "New York Jets",
            "Miami Dolphins",
        ],
    },
    {
        "id": "pfn_camp",
        "label": "PFN_camp",
        "outlet": "Pro Football Network (Jacob Infante)",
        "date": "2026-07-29",
        "url": "https://www.profootballnetwork.com/2026-nfl-power-rankings-training-camp/",
        "note": "Training camp; latest PFN 1-32",
        "teams": [
            "Los Angeles Rams",
            "Seattle Seahawks",
            "Buffalo Bills",
            "San Francisco 49ers",
            "Baltimore Ravens",
            "Denver Broncos",
            "Chicago Bears",
            "New England Patriots",
            "Green Bay Packers",
            "Detroit Lions",
            "Houston Texans",
            "Philadelphia Eagles",
            "Cincinnati Bengals",
            "Jacksonville Jaguars",
            "Kansas City Chiefs",
            "Dallas Cowboys",
            "Tampa Bay Buccaneers",
            "Washington Commanders",
            "Los Angeles Chargers",
            "Pittsburgh Steelers",
            "Indianapolis Colts",
            "Minnesota Vikings",
            "Atlanta Falcons",
            "New Orleans Saints",
            "New York Giants",
            "Carolina Panthers",
            "Tennessee Titans",
            "Las Vegas Raiders",
            "Cleveland Browns",
            "Miami Dolphins",
            "New York Jets",
            "Arizona Cardinals",
        ],
    },
    {
        "id": "yahoo_schwab",
        "label": "Yahoo_Schwab",
        "outlet": "Yahoo Sports (Frank Schwab)",
        "date": "2026-08-05",
        "url": "https://sports.yahoo.com/nfl/article/nfl-2026-offseason-power-rankings-countdown-defending-champion-seahawks-arent-no-1-131500536.html",
        "note": "Independent camp countdown; not the Sportsnaut reprint",
        "teams": [
            "Los Angeles Rams",
            "Seattle Seahawks",
            "Buffalo Bills",
            "Denver Broncos",
            "New England Patriots",
            "Detroit Lions",
            "Baltimore Ravens",
            "Dallas Cowboys",
            "Philadelphia Eagles",
            "Houston Texans",
            "Chicago Bears",
            "Kansas City Chiefs",
            "San Francisco 49ers",
            "Los Angeles Chargers",
            "Green Bay Packers",
            "Jacksonville Jaguars",
            "Cincinnati Bengals",
            "Washington Commanders",
            "Minnesota Vikings",
            "Pittsburgh Steelers",
            "Indianapolis Colts",
            "Tampa Bay Buccaneers",
            "Carolina Panthers",
            "New Orleans Saints",
            "New York Giants",
            "Atlanta Falcons",
            "Las Vegas Raiders",
            "Tennessee Titans",
            "Cleveland Browns",
            "Arizona Cardinals",
            "New York Jets",
            "Miami Dolphins",
        ],
    },
    {
        "id": "br_camp",
        "label": "BR_camp",
        "outlet": "Bleacher Report (training camp)",
        "date": "2026-07-10",
        "url": "https://bleacherreport.com/articles/25452865-2026-nfl-power-rankings-where-does-every-team-stack-entering-training-camp",
        "note": "Worst-to-first slideshow. Rank 32 Dolphins and 29 Jets are unnumbered sections on the page between numbered neighbors; not interpolated missing teams.",
        "teams": [
            "Los Angeles Rams",
            "Seattle Seahawks",
            "Denver Broncos",
            "Buffalo Bills",
            "Houston Texans",
            "New England Patriots",
            "Philadelphia Eagles",
            "Jacksonville Jaguars",
            "San Francisco 49ers",
            "Chicago Bears",
            "Los Angeles Chargers",
            "Detroit Lions",
            "Baltimore Ravens",
            "Green Bay Packers",
            "Cincinnati Bengals",
            "Tampa Bay Buccaneers",
            "Kansas City Chiefs",
            "Dallas Cowboys",
            "Pittsburgh Steelers",
            "Carolina Panthers",
            "Minnesota Vikings",
            "Indianapolis Colts",
            "New Orleans Saints",
            "Washington Commanders",
            "Las Vegas Raiders",
            "Atlanta Falcons",
            "New York Giants",
            "Tennessee Titans",
            "New York Jets",
            "Cleveland Browns",
            "Arizona Cardinals",
            "Miami Dolphins",
        ],
    },
    {
        "id": "otl_sports",
        "label": "OTL_Sports",
        "outlet": "OTL Sports",
        "date": "2026-08-17",
        "url": "https://otlsports.com/nfl-power-rankings-updated-preseason-week-1/",
        "note": "Updated preseason Week 1",
        "teams": [
            "Los Angeles Rams",
            "Denver Broncos",
            "Houston Texans",
            "Seattle Seahawks",
            "Detroit Lions",
            "Baltimore Ravens",
            "Buffalo Bills",
            "Chicago Bears",
            "San Francisco 49ers",
            "Philadelphia Eagles",
            "New England Patriots",
            "Green Bay Packers",
            "Cincinnati Bengals",
            "Los Angeles Chargers",
            "Jacksonville Jaguars",
            "Tampa Bay Buccaneers",
            "Dallas Cowboys",
            "Indianapolis Colts",
            "Kansas City Chiefs",
            "Minnesota Vikings",
            "Pittsburgh Steelers",
            "Washington Commanders",
            "Carolina Panthers",
            "Atlanta Falcons",
            "New Orleans Saints",
            "New York Jets",
            "Cleveland Browns",
            "Tennessee Titans",
            "Las Vegas Raiders",
            "New York Giants",
            "Arizona Cardinals",
            "Miami Dolphins",
        ],
    },
    {
        "id": "nfl_com",
        "label": "NFL_com",
        "outlet": "NFL.com (Nick Shook)",
        "date": "2026-08-11",
        "url": "https://www.nfl.com/news/nfl-power-rankings-rams-enter-preseason-on-top-seahawks-at-no-3-patriots-outside-top-10",
        "note": "Enter-preseason full 1-32; latest NFL.com list",
        "teams": [
            "Los Angeles Rams",
            "Denver Broncos",
            "Seattle Seahawks",
            "Philadelphia Eagles",
            "Buffalo Bills",
            "Baltimore Ravens",
            "Jacksonville Jaguars",
            "Cincinnati Bengals",
            "Houston Texans",
            "Chicago Bears",
            "Dallas Cowboys",
            "New England Patriots",
            "Green Bay Packers",
            "Detroit Lions",
            "Kansas City Chiefs",
            "San Francisco 49ers",
            "Los Angeles Chargers",
            "Minnesota Vikings",
            "Indianapolis Colts",
            "Pittsburgh Steelers",
            "New Orleans Saints",
            "Tampa Bay Buccaneers",
            "Carolina Panthers",
            "Tennessee Titans",
            "Atlanta Falcons",
            "Arizona Cardinals",
            "New York Giants",
            "Cleveland Browns",
            "Washington Commanders",
            "New York Jets",
            "Las Vegas Raiders",
            "Miami Dolphins",
        ],
    },
]


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
        row["JuneRank"] = june
        row["RankDelta"] = june - i

    source_path = HERE / "source_ranks.csv"
    with source_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Team", "Abbr"] + source_names)
        writer.writeheader()
        for row in sorted(team_rows, key=lambda r: r["Team"]):
            writer.writerow({k: row[k] for k in ["Team", "Abbr"] + source_names})

    consensus_path = HERE / "consensus_power_rankings.csv"
    fields = ["Rank", "Team", "Abbr", "Avg", "Best", "Worst", "Std", "JuneRank", "RankDelta"]
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
