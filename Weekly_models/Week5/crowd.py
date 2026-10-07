"""Week 5 Circa crowd stand-in, chip, and leverage. Standard library only.

Reads inputs.json, writes out/ and ../../assets/week5-crowd.js.

    python3 Weekly_models/Week5/crowd.py
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
OUT = HERE / "out"
ASSET = REPO / "assets" / "week5-crowd.js"

LAMBDA = 0.7
CROWD_FLOOR = 0.001
MIN_WIN = 0.60
PG_WEIGHT = 0.5

TEAMS = [
    "ARI", "ATL", "BAL", "BUF", "CAR", "CHI", "CIN", "CLE", "DAL", "DEN", "DET",
    "GB", "HOU", "IND", "JAC", "KC", "LAC", "LAR", "LV", "MIA", "MIN", "NE", "NO",
    "NYG", "NYJ", "PHI", "PIT", "SEA", "SF", "TB", "TEN", "WAS",
]


def implied_raw(ml: float) -> float:
    return -ml / (-ml + 100) if ml < 0 else 100 / (ml + 100)


def vig_free(games: list[dict]) -> dict[str, float]:
    out: dict[str, float] = {}
    for g in games:
        a, h = implied_raw(g["awayMl"]), implied_raw(g["homeMl"])
        out[g["away"]] = a / (a + h)
        out[g["home"]] = h / (a + h)
    return out


def normalize(d: dict[str, float]) -> dict[str, float]:
    s = sum(d.values())
    return {k: v / s for k, v in d.items()}


def public_base(cfg: dict, playing: set[str]) -> dict[str, float]:
    """Blend PoolGenius (top 5 only) with SurvivorGrid (full board).

    PoolGenius tail mass goes to the non-top-5 teams in SurvivorGrid's proportions.
    """
    sg_cfg = cfg["public"]["survivorgrid"]
    sg = {t: sg_cfg["pct"].get(t, sg_cfg["unlistedPct"]) for t in playing}
    sg = normalize(sg)
    pg_top = {t: v / 100 for t, v in cfg["public"]["poolgenius"]["pct"].items()}
    tail = max(0.0, 1.0 - sum(pg_top.values()))
    rest = normalize({t: sg[t] for t in playing if t not in pg_top})
    pg = {t: pg_top.get(t, tail * rest.get(t, 0.0)) for t in playing}
    return {t: PG_WEIGHT * pg[t] + (1 - PG_WEIGHT) * sg[t] for t in playing}


def circa_scaled(base: dict[str, float], avail: dict[str, float]) -> dict[str, float]:
    return normalize({t: base[t] * avail[t] for t in base})


def week4_backtest(cfg: dict) -> list[dict]:
    """Public Week 4 top 4 scaled by approximate Week 4 availability vs Circa actual.

    Week 4 availability is backed out of the Week 5 sheet: a live Week 5 ticket that has
    used T either used it in Week 4 (the Week 4 winners) or before. The before-share is
    applied to the 6,292 that entered Week 4.
    """
    n5 = cfg["availability"]["of"]
    w4 = cfg["circaWeek4"]
    actual_n = {**w4["won"], **w4["lost"]}
    pub = {t: v / 100 for t, v in cfg["publicWeek4"]["pct"].items()}
    other = 1.0 - sum(pub.values())
    avail4 = {}
    for t in pub:
        used_before = n5 - cfg["availability"]["n"][t] - w4["won"].get(t, 0)
        avail4[t] = 1.0 - used_before / n5
    scaled = {t: pub[t] * avail4[t] for t in pub}
    z = sum(scaled.values()) + other
    rows = []
    for t in pub:
        rows.append(
            {
                "team": t,
                "public": pub[t],
                "avail": avail4[t],
                "scaled": scaled[t] / z,
                "actual": actual_n.get(t, 0) / w4["picks"],
            }
        )
    return rows


def main() -> None:
    cfg = json.loads((HERE / "inputs.json").read_text(encoding="utf-8"))
    n_alive = cfg["field"]["enterWeek5"]
    pot = cfg["pot"]
    games = cfg["games"]
    implied = vig_free(games)
    playing = set(implied)
    bye = set(cfg["bye"])
    if playing & bye or len(playing) != 30 or playing | bye != set(TEAMS):
        raise SystemExit("FAIL slate does not cover 30 teams + 2 byes")
    if cfg["availability"]["of"] != n_alive:
        raise SystemExit("FAIL availability sheet is not the live field")

    avail = {t: cfg["availability"]["n"][t] / n_alive for t in TEAMS}
    base = public_base(cfg, playing)
    crowd = circa_scaled(base, avail)

    p_surv = sum(crowd[t] * implied[t] for t in playing)
    chip_now = pot / n_alive
    chip_exp = pot / (n_alive * p_surv)

    fav = {g["id"]: (g["home"] if implied[g["home"]] >= implied[g["away"]] else g["away"]) for g in games}
    fav_set = set(fav.values())
    hold = sum(crowd[t] for t in fav_set)

    order = sorted(playing, key=lambda t: crowd[t], reverse=True)

    def leverage(t: str) -> float:
        return math.log(implied[t]) - LAMBDA * math.log(max(crowd[t], CROWD_FLOOR))

    lev_rows = sorted(
        (t for t in playing if implied[t] >= MIN_WIN), key=leverage, reverse=True
    )

    opponent = {}
    for g in games:
        opponent[g["away"]], opponent[g["home"]] = g["home"], g["away"]

    what_if = []
    for t in order[:6]:
        if t not in fav_set:
            continue
        alive_share = hold - crowd[t] + crowd[opponent[t]]
        alive = n_alive * alive_share
        what_if.append({"team": t, "alive": alive, "chip": pot / alive})

    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "week5_shares.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["team", "circa_share", "public_base", "available", "implied_win_prob", "leverage"])
        for t in order:
            w.writerow(
                [t, f"{crowd[t]:.5f}", f"{base[t]:.5f}", f"{avail[t]:.4f}",
                 f"{implied[t]:.4f}", f"{leverage(t):.3f}"]
            )

    bt = week4_backtest(cfg)

    lines = [
        "# Week 5 crowd, chip, leverage",
        "",
        f"Generated by `crowd.py` from `inputs.json` (as of {cfg['asOf']}).",
        "",
        f"Live field **{n_alive:,}** / start {cfg['nStart']:,}, pot **${pot:,.0f}**. "
        f"Chip if paid now: **${chip_now:,.0f}**.",
        f"Crowd survives at implied rates: **{100 * p_surv:.1f}%** → expected chip **${chip_exp:,.0f}** "
        "(one week, not season EV).",
        f"If every favorite wins, {100 * hold:.1f}% of the field lives "
        f"({n_alive * hold:,.0f}) → chip ${pot / (n_alive * hold):,.0f}.",
        "",
        "Crowd = public base (½ PoolGenius 6 Oct top 5 + ½ SurvivorGrid 7 Oct) × "
        "Circa Week 5 team availability, renormalized.",
        "",
        "| team | Circa crowd % | public % | available % | win % | leverage |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for t in order[:14]:
        lines.append(
            f"| {t} | {100 * crowd[t]:.1f} | {100 * base[t]:.1f} | {100 * avail[t]:.1f} | "
            f"{100 * implied[t]:.1f} | {leverage(t):.3f} |"
        )
    lines += [
        "",
        f"## Leverage among ≥{100 * MIN_WIN:.0f}% favorites (λ={LAMBDA}, crowd floor {100 * CROWD_FLOOR:.1f}%)",
        "",
        "`log(win) − λ·log(crowd)`. Higher = survives at a good rate without riding the chalk. "
        "Check your own ticket's burns; availability is the field's, not ours.",
        "",
        "| team | win % | Circa crowd % | available % | leverage |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for t in lev_rows:
        lines.append(
            f"| {t} | {100 * implied[t]:.1f} | {100 * crowd[t]:.1f} | {100 * avail[t]:.1f} | {leverage(t):.3f} |"
        )
    lines += [
        "",
        "## One chalk loss (every other favorite wins)",
        "",
        "| loses | field alive | chip |",
        "| --- | ---: | ---: |",
    ]
    for r in what_if:
        lines.append(f"| {r['team']} | {r['alive']:,.0f} | ${r['chip']:,.0f} |")
    lines += [
        "",
        "## Backtest: Week 4 public × availability vs Circa PDF",
        "",
        "| team | public % | available % | scaled % | Circa actual % |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for r in bt:
        lines.append(
            f"| {r['team']} | {100 * r['public']:.1f} | {100 * r['avail']:.1f} | "
            f"{100 * r['scaled']:.1f} | {100 * r['actual']:.1f} |"
        )
    (OUT / "week5_book.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    def obj(d: dict[str, float]) -> str:
        return json.dumps({t: round(d.get(t, 0.0), 6) for t in TEAMS})

    chalk = [t for t in order if t in fav_set][:4]
    js_games = [
        {k: g[k] for k in ("id", "when", "away", "home", "line", "awayMl", "homeMl", "neutral") if k in g}
        for g in games
    ]
    js = "\n".join(
        [
            "// Generated by Weekly_models/Week5/crowd.py — edit inputs.json and rerun.",
            "(function () {",
            "  window.CIRCA_WEEK5 = {",
            f"    nStart: {cfg['nStart']},",
            f"    nAlive: {n_alive},",
            f"    pot: {pot},",
            '    saveKey: "circa-week5-chip-v1",',
            '    source: "Public (PoolGenius 6 Oct + SurvivorGrid 7 Oct) × Circa Week 5 availability. Not the Circa PDF.",',
            f"    bye: {json.dumps(sorted(bye))},",
            f"    chalk: {json.dumps(chalk)},",
            f"    share: {obj(crowd)},",
            f"    uncond: {obj(base)},",
            f"    available: {obj(avail)},",
            f"    implied: {obj(implied)},",
            f"    games: {json.dumps(js_games, ensure_ascii=False)}",
            "  };",
            "})();",
            "",
        ]
    )
    ASSET.write_text(js, encoding="utf-8")

    print(f"field {n_alive:,} chip now ${chip_now:,.0f} expected ${chip_exp:,.0f} p_surv {p_surv:.3f}")
    for t in order[:8]:
        print(f"  {t:4s} crowd {100 * crowd[t]:5.1f}  win {100 * implied[t]:5.1f}  avail {100 * avail[t]:5.1f}")
    print("leverage:", ", ".join(f"{t} {leverage(t):.2f}" for t in lev_rows))
    for r in bt:
        print(f"  W4 {r['team']} scaled {100 * r['scaled']:.1f} actual {100 * r['actual']:.1f}")


if __name__ == "__main__":
    main()
