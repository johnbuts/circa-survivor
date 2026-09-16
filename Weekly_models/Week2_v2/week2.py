"""Week 2 crowd + 8-live book. Writes only under Week2_v2/out."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from score_week1 import (
    DISPLAY_TO_ABBR,
    OUT,
    REPO,
    predict_week1,
)

WEEK1_ENTRIES = REPO / "all_picks_2026" / "parsed" / "week1_entries.csv"
LIVE_BOOK = {"JAC": 4, "PIT": 2, "LV": 2}
N_START = 25_017
N_ALIVE_W2 = 16_978
POT = 25_017_000.0
LAMBDA = 0.7

WEEK1_WON = {
    "ARI": True,
    "ATL": False,
    "BAL": True,
    "BUF": True,
    "CAR": False,
    "CHI": True,
    "CIN": True,
    "CLE": False,
    "DAL": False,
    "DEN": False,
    "DET": True,
    "GB": False,
    "HOU": False,
    "IND": False,
    "JAC": True,
    "KC": True,
    "LAC": False,
    "LAR": False,
    "LV": True,
    "MIA": True,
    "MIN": True,
    "NE": False,
    "NO": False,
    "NYG": True,
    "NYJ": True,
    "PHI": True,
    "PIT": True,
    "SEA": True,
    "SF": True,
    "TB": False,
    "TEN": False,
    "WAS": False,
}


def week_frame(gtw: pd.DataFrame, week_ord: int) -> pd.DataFrame:
    w = gtw[gtw["contest_week_ord"] == week_ord].sort_values("team").reset_index(drop=True)
    if len(w) != 32:
        raise ValueError(f"FAIL week {week_ord} rows {len(w)} != 32")
    return w


def load_live_field() -> pd.DataFrame:
    df = pd.read_csv(WEEK1_ENTRIES)
    df["abbr"] = df["team"].map(lambda x: DISPLAY_TO_ABBR[str(x).upper().strip()])
    df["won"] = df["abbr"].map(WEEK1_WON)
    if df["won"].isna().any():
        missing = sorted(df.loc[df["won"].isna(), "abbr"].unique())
        raise ValueError(f"FAIL unknown Week 1 result for {missing}")
    return df[df["won"]].copy().reset_index(drop=True)


def field_conditioned_shares(
    teams: list[str],
    base_shares: np.ndarray,
    live: pd.DataFrame,
) -> np.ndarray:
    logits = np.log(np.clip(base_shares, 1e-12, 1.0))
    acc = np.zeros(len(teams), dtype=np.float64)
    team_i = {t: i for i, t in enumerate(teams)}
    n = 0
    for burned in live["abbr"].tolist():
        mask = np.ones(len(teams), dtype=bool)
        if burned in team_i:
            mask[team_i[burned]] = False
        x = np.where(mask, logits, -1e30)
        x = x - np.max(x)
        p = np.exp(x)
        p = p / p.sum()
        acc += p
        n += 1
    return acc / max(n, 1)


def leverage_table(week: pd.DataFrame, crowd: dict[str, float], burned: str) -> pd.DataFrame:
    rows = []
    for row in week.itertuples(index=False):
        team = row.team
        if team == burned:
            continue
        wp = float(row.implied_win_prob)
        sh = float(crowd.get(team, 0.0))
        if wp < 0.60:
            continue
        lev = np.log(max(wp, 1e-6)) - LAMBDA * np.log(max(sh, 0.001))
        rows.append(
            {
                "burned": burned,
                "team": team,
                "win_prob": wp,
                "crowd": sh,
                "leverage": lev,
                "spread": float(row.spread),
            }
        )
    return pd.DataFrame(rows).sort_values("leverage", ascending=False).reset_index(drop=True)


def write_week2(gtw, scalers, beta, current: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    week = week_frame(gtw, 2)
    teams, base_shares, implied = predict_week1(
        week,
        scalers,
        beta,
        current["tau"],
        third_chalk_delta=current["third_delta"],
        safe_third_delta=current["safe_third"],
        fv_gap_gamma=current["fv_gamma"],
    )
    live = load_live_field()
    cond = field_conditioned_shares(teams, base_shares, live)
    crowd = {t: float(s) for t, s in zip(teams, cond, strict=True)}
    rows = []
    for team, sh, imp in zip(teams, cond, implied, strict=True):
        rows.append(
            {
                "team": team,
                "pred_share": float(sh),
                "uncond_share": float(base_shares[teams.index(team)]),
                "implied_win_prob": float(imp),
            }
        )
    pd.DataFrame(rows).sort_values("pred_share", ascending=False).to_csv(
        OUT / "week2_shares.csv", index=False
    )

    p_surv = sum(crowd[t] * float(imp) for t, imp in zip(teams, implied, strict=True))
    chip = POT / max(N_ALIVE_W2 * p_surv, 1.0)
    lines = [
        "# Week 2 (only because Week 1 is close)",
        "",
        f"Kept knobs: steam={current['steam']}, tau={current['tau']:.3f}, "
        f"third_delta={current['third_delta']:.2f}, fv_gamma={current['fv_gamma']:.2f}, "
        f"safe_third={current['safe_third']:.2f}.",
        "",
        f"Official field entering Week 2: **{N_ALIVE_W2:,}** live / **{N_START:,}** start, "
        f"pot **${POT:,.0f}**.",
        "8-live book: JAC×4, PIT×2, LV×2 (Titans died). Burned: JAC / PIT / LV.",
        f"One-week expected chip if the field survives at implied rates: **${chip:,.0f}** "
        "(not a season EV).",
        "",
        "Field-conditioned crowd (survivors cannot re-pick their Week 1 team):",
        "",
        "| team | crowd % | uncond % | implied |",
        "| --- | ---: | ---: | ---: |",
    ]
    order = sorted(teams, key=lambda t: crowd[t], reverse=True)
    for team in order[:12]:
        i = teams.index(team)
        lines.append(
            f"| {team} | {100 * crowd[team]:.1f} | {100 * base_shares[i]:.1f} | "
            f"{100 * implied[i]:.1f} |"
        )
    lines.extend(
        [
            "",
            "Crowd chalk is **SF + TB (~60%)**, then BAL / LAC. The leverage table below is "
            "the overlay among implied favorites (≥60% win prob), not a 'pick SEA' instruction. "
            "Burned JAC/PIT/LV does not change the top of the field much because almost nobody "
            "used those three in Week 2 anyway.",
            "",
            "Top leverage remaining for each burned mask (λ=0.7, crowd floor 0.1%, implied ≥60%):",
            "",
        ]
    )
    book_rows = []
    for burned, n in LIVE_BOOK.items():
        top = leverage_table(week, crowd, burned).head(6)
        lines.append(f"**{burned}×{n} burned `{burned}`**")
        lines.append("")
        lines.append("| team | win_prob | crowd | leverage | spread |")
        lines.append("| --- | ---: | ---: | ---: | ---: |")
        for r in top.itertuples(index=False):
            lines.append(
                f"| {r.team} | {100.0 * r.win_prob:.1f}% | {100.0 * r.crowd:.1f}% | "
                f"{r.leverage:.3f} | {r.spread:+.1f} |"
            )
            book_rows.append({**r._asdict(), "n_tickets": n})
        lines.append("")
    (OUT / "week2_book.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    pd.DataFrame(book_rows).to_csv(OUT / "week2_leverage.csv", index=False)

    report = Path(__file__).resolve().parent / "report.md"
    extra = "\n".join(
        [
            "",
            "## Week 2 (8 live tickets)",
            "",
            f"See `out/week2_book.md`. Field-conditioned top: "
            f"{order[0]} {100 * crowd[order[0]]:.1f}%, "
            f"{order[1]} {100 * crowd[order[1]]:.1f}%, "
            f"{order[2]} {100 * crowd[order[2]]:.1f}%.",
            "",
        ]
    )
    report.write_text(report.read_text(encoding="utf-8") + extra, encoding="utf-8")
    print("wrote week 2 out/week2_book.md", flush=True)
