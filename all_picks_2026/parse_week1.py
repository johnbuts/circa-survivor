"""Parse Circa Survivor weekly selection PDFs into entry rows.

Ghostscript `txtwrite` dumps the 3-column board as text. Each cell is
`OWNER-N` plus `##. TEAM PK`. Long names sometimes collide with the pick
(`THEABSOLUTEGOVERNORS-122. CHARGERS PK` = entry 1 on 22. CHARGERS).
The pair regex splits on the last `-(1–10)` before the team number.
"""

from __future__ import annotations

import csv
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PDF = ROOT / "raw__pdf" / "Circa-Survivor-2026-Week-1-Selections.pdf"
PARSED = ROOT / "parsed"

PAIR_RE = re.compile(
    r"(.+?)-(10|[1-9])\s*(\d{1,2})\.\s+([A-Z0-9][A-Z0-9 ]+?)\s+PK"
)
SKIP_LINES = {"Circa Survivor 2026", "Week 1 Selections", "09/12/26"}

# Official Circa Survivor last-standing / pot-splitters (handles).
# 2020–2025 match PoolGenius survived_to_end and Circa/RJ payout lists.
OFFICIAL_WINNERS: dict[int, list[str]] = {
    2020: [
        "* THE NUT SQUIRRELS",
        "7- Out",
        "Artie Blanco",
        "BALD RAZORS",
        "BOBBYT",
        "BOYCOTT 8 PCT",
        "CLARKGRIZWOLD",
        "COLTS45",
        "DaliBones",
        "EX-FINANCE",
        "Golfing in Hell",
        "JakestroJans",
        "Joncon16",
        "LoveMyBaxter",
        "MK INVEST",
        "Mucked Nuts.",
        "PICKSWCLARS24",
        "PLAYIN N STAYIN",
        "PRESENCE",
        "Pauline Park",
        "Practice Squad QB",
        "ROBERTRUTTER",
        "Rip Wheeler",
        "SHAMWOW.",
        "Slick Rick11",
        "Staying Alive",
        "Sting",
        "THAWK",
        "TIM'S SUNSCREEN",
        "Texas Bound.",
        "WHAT IS FOOTBALL?",
        "WHERE'S LUNCH",
        "pointsonthepackage",
    ],
    2021: [
        "CHRIS PIPER",
        "MYCOOL",
        "On Top 247",
        "RETURN OF SURVIVOR",
        "SYRACUSE HAWKEYES",
    ],
    2022: ["BROWNA", "JED"],
    2023: ["CIRCUS MASTER", "IndianaJet", "JAX JAGS", "LAJONESER"],
    2024: [
        "C3 Picks",
        "DREAM STAKES",
        "MEATBALL BROTHERS",
        "PUMBAPACK9",
        "TY1823",
        "VODKA JOHNNY",
        "WHATEVERYALLWANT",
        "Whiskey Business",
    ],
    2025: [
        "DYLAN W",
        "GaryA",
        "JUICY KEWCHI",
        "KICK YOUR KNEES UP",
        "REAL BRO",
    ],
}

VARIANTS: dict[str, list[str]] = {
    "7- Out": ["7-OUT", "7 OUT"],
    "C3 Picks": ["C3 PICKS"],
    "CIRCUS MASTER": ["Circus Master"],
    "DREAM STAKES": ["Dream Stakes"],
    "IndianaJet": ["INDIANAJET", "Indiana Jet"],
    "JAX JAGS": ["Jax Jags"],
    "JED": ["Jed"],
    "LAJONESER": ["LA JONESER", "LAJoneser", "Lajoneser"],
    "MEATBALL BROTHERS": ["Meatball Brothers"],
    "Mucked Nuts.": ["Mucked Nuts", "MUCKED NUTS"],
    "On Top 247": ["ON TOP 247"],
    "PLAYIN N STAYIN": ["PLAYIN N STAYING"],
    "PUMBAPACK9": ["PUMBAPACK 9"],
    "SHAMWOW.": ["SHAMWOW"],
    "Texas Bound.": ["Texas Bound"],
    "WHAT IS FOOTBALL?": ["WHAT IS FOOTBALL"],
    "Whiskey Business": ["WHISKEY BUSINESS"],
    "BROWNA": ["Browna"],
    "DYLAN W": ["Dylan W"],
    "GaryA": ["GARYA"],
    "JUICY KEWCHI": ["Juicy Kewchi"],
    "REAL BRO": ["Real Bro"],
    "KICK YOUR KNEES UP": ["Kick Your Knees Up"],
}


def extract_text(pdf: Path) -> str:
    proc = subprocess.run(
        [
            "gs",
            "-sDEVICE=txtwrite",
            "-dNOPAUSE",
            "-dBATCH",
            "-dQUIET",
            "-sOutputFile=-",
            str(pdf),
        ],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return proc.stdout.decode("utf-8", errors="replace")


def parse_entries(text: str) -> list[dict]:
    entries: list[dict] = []
    for line in text.splitlines():
        if "ENTRY NAME" in line and "SELECTION" in line:
            continue
        if line.strip() in SKIP_LINES:
            continue
        raw = re.sub(r"\s+09/12/26\s*$", "", line).strip()
        if not raw:
            continue
        for m in PAIR_RE.finditer(raw):
            owner = m.group(1).strip()
            entry_num = int(m.group(2))
            entries.append(
                {
                    "owner": owner,
                    "entry_num": entry_num,
                    "entry_alias": f"{owner}-{entry_num}",
                    "team_num": int(m.group(3)),
                    "team": m.group(4).strip(),
                }
            )
    aliases = [e["entry_alias"] for e in entries]
    if len(aliases) != len(set(aliases)):
        raise SystemExit("duplicate entry aliases after parse")
    return entries


def compact(s: str) -> str:
    """Case/space/punct-insensitive key. 'On Top 247' == 'ONTOP247'."""
    return re.sub(r"[^A-Z0-9]", "", s.upper())


def match_winners(entries: list[dict]) -> list[dict]:
    by_key: dict[str, list[dict]] = defaultdict(list)
    for e in entries:
        by_key[compact(e["owner"])].append(e)

    rows: list[dict] = []
    for year, handles in OFFICIAL_WINNERS.items():
        for handle in handles:
            keys = [handle, *VARIANTS.get(handle, [])]
            hits: list[dict] = []
            seen: set[str] = set()
            matched_as = ""
            for key in keys:
                for e in by_key.get(compact(key), []):
                    if e["entry_alias"] not in seen:
                        seen.add(e["entry_alias"])
                        hits.append(e)
                        if not matched_as:
                            matched_as = e["owner"]
            if not hits:
                rows.append(
                    {
                        "year_won": year,
                        "handle": handle,
                        "in_2026": "NO",
                        "matched_owner": "",
                        "n_entries": 0,
                        "week1_teams": "",
                    }
                )
                continue
            team_counts = Counter(e["team"] for e in hits)
            week1 = ", ".join(
                f"{team} {n}" for team, n in team_counts.most_common()
            )
            rows.append(
                {
                    "year_won": year,
                    "handle": handle,
                    "in_2026": "YES",
                    "matched_owner": matched_as,
                    "n_entries": len(hits),
                    "week1_teams": week1,
                }
            )
    return rows


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    text = extract_text(PDF)
    entries = parse_entries(text)
    winners = match_winners(entries)
    n = len(entries)
    shares = Counter(e["team"] for e in entries)
    share_rows = [
        {
            "team": team,
            "n": count,
            "share": f"{count / n:.6f}",
            "share_pct": f"{100 * count / n:.2f}",
        }
        for team, count in shares.most_common()
    ]

    write_csv(
        PARSED / "week1_entries.csv",
        entries,
        ["owner", "entry_num", "entry_alias", "team_num", "team"],
    )
    write_csv(
        PARSED / "winner_matches.csv",
        winners,
        [
            "year_won",
            "handle",
            "in_2026",
            "matched_owner",
            "n_entries",
            "week1_teams",
        ],
    )
    write_csv(
        PARSED / "week1_pick_share.csv",
        share_rows,
        ["team", "n", "share", "share_pct"],
    )

    back = sum(1 for r in winners if r["in_2026"] == "YES")
    print(f"entries {n}")
    print(f"owners {len({e['owner'] for e in entries})}")
    print(f"official winning handles back {back}/{len(winners)}")
    print(f"wrote {PARSED}")


if __name__ == "__main__":
    main()
