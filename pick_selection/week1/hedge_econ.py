#!/usr/bin/env python3
"""Exact week-1 slate enumeration (2^16 worlds) of hedge + chip wealth.

P(world) = product of vig-free Circa win probs, independent games.
Wealth vs $10k buy-in:  hedge_net + ours_alive * chip - N * fee
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np

import chug as C

N_GAMES = 16
N_WORLDS = 1 << N_GAMES
N_ENTRIES = 10
FEE = 1_000.0
BUYIN = N_ENTRIES * FEE
OUT = Path(__file__).with_name("hedge_econ_tables.md")

BOOKS: list[tuple[str, dict[str, int], str]] = [
    ("all chalk", {"LAC": 10}, "every ticket on the 41% crowd favorite"),
    ("chalk split", {"LAC": 6, "JAC": 4}, "the two biggest crowd teams"),
    ("two-team fade", {"SEA": 5, "BAL": 5}, "thin-crowd favorites, concentrated"),
    ("three-team fade", {"SEA": 4, "BAL": 3, "CIN": 3}, "still fading; one extra independent game"),
    ("four-team fade", {"SEA": 3, "BAL": 3, "CIN": 2, "PHI": 2}, "more independent lives, more hedge legs"),
    ("five-team fade", {"SEA": 2, "BAL": 2, "CIN": 2, "PHI": 2, "LAR": 2}, "widest book; 2^5 = 32 pick-masks"),
]

HEDGE_NAMES = ["naked", "wipe", "3cover", "wipe+3", "rr3+4", "2cover"]


def game_arrays() -> tuple[np.ndarray, list[str], list[str], np.ndarray, np.ndarray]:
    p_away = np.empty(N_GAMES, dtype=np.float64)
    away, home = [], []
    c_away = np.empty(N_GAMES, dtype=np.float64)
    c_home = np.empty(N_GAMES, dtype=np.float64)
    for i, (a, _aml, h, _hml, _when) in enumerate(C.GAMES):
        away.append(a)
        home.append(h)
        p_away[i] = C.vig_free_p(a)
        c_away[i] = C.crowd_share(a)
        c_home[i] = C.crowd_share(h)
    return p_away, away, home, c_away, c_home


def worlds(p_away: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    masks = np.arange(N_WORLDS, dtype=np.uint32)
    bits = ((masks[:, None] >> np.arange(N_GAMES, dtype=np.uint32)) & 1).astype(bool)
    logp = np.where(bits, np.log(p_away), np.log(1.0 - p_away)).sum(axis=1)
    prob = np.exp(logp)
    assert abs(float(prob.sum()) - 1.0) < 1e-9, float(prob.sum())
    return bits, prob


def team_win(bits: np.ndarray, away: list[str], home: list[str]) -> dict[str, np.ndarray]:
    win: dict[str, np.ndarray] = {}
    for g, (a, h) in enumerate(zip(away, home)):
        win[a] = bits[:, g]
        win[h] = ~bits[:, g]
    return win


def field_and_chip(
    bits: np.ndarray, c_away: np.ndarray, c_home: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    share = bits * c_away + ~bits * c_home
    field_share = share.sum(axis=1)
    field_alive = C.FIELD_START * field_share
    chip = np.divide(C.POT, field_alive, out=np.zeros_like(field_alive), where=field_alive > 0)
    return field_alive, chip


def hedges_for(book: dict[str, int]) -> list[tuple[str, list]]:
    picks = list(book)
    n = len(picks)
    names = []
    for name in HEDGE_NAMES:
        if name in {"3cover", "wipe+3", "rr3+4"} and n < 3:
            continue
        if name == "rr3+4" and n < 4:
            continue
        if name == "2cover" and n < 2:
            continue
        names.append(name)
    out = []
    for name in names:
        spec = C.parse_hedge_spec(name, n, C.DEFAULT_EACH, C.DEFAULT_BANKROLL)
        tickets = C.build_tickets(picks, book, N_ENTRIES, FEE, spec)
        out.append((name, tickets))
    return out


def ours_alive(book: dict[str, int], win: dict[str, np.ndarray]) -> np.ndarray:
    n = np.zeros(N_WORLDS, dtype=np.float64)
    for t, c in book.items():
        n += c * win[t].astype(np.float64)
    return n


def hedge_net(tickets: list, win: dict[str, np.ndarray]) -> np.ndarray:
    if not tickets:
        return np.zeros(N_WORLDS, dtype=np.float64)
    payout = np.zeros(N_WORLDS, dtype=np.float64)
    stake = 0.0
    for tk in tickets:
        stake += tk.stake
        hit = np.ones(N_WORLDS, dtype=bool)
        for p in tk.picks:
            hit &= ~win[p]
        payout += tk.stake * tk.dec * hit
    return payout - stake


def wmean(x: np.ndarray, p: np.ndarray) -> float:
    return float(np.dot(p, x))


def wquantile(x: np.ndarray, p: np.ndarray, q: float) -> float:
    order = np.argsort(x)
    xs = x[order]
    cs = np.cumsum(p[order])
    return float(xs[np.searchsorted(cs, q, side="left").clip(0, len(xs) - 1)])


def fmt_money(n: float) -> str:
    sign = "-" if n < 0 else ""
    return f"{sign}${abs(n):,.0f}"


def fmt_pct(n: float) -> str:
    return f"{n * 100:.1f}%"


def run() -> str:
    p_away, away, home, c_away, c_home = game_arrays()
    bits, prob = worlds(p_away)
    win = team_win(bits, away, home)
    field_alive, chip = field_and_chip(bits, c_away, c_home)
    lac_lose = ~win["LAC"]
    jac_lose = ~win["JAC"]
    det_lose = ~win["DET"]
    chalk_hold = win["LAC"] & win["JAC"] & win["DET"]
    any_chalk_down = lac_lose | jac_lose | det_lose

    lines = [
        "# Simulation tables (generated)",
        "",
        "Worlds: **65,536** (every week-1 winner combination). "
        f"Probability mass sums to **{float(prob.sum()):.12f}**.",
        "Game outcomes: independent, vig-free Circa implied probabilities. "
        "Parlay payouts: posted Circa decimals (juice in).",
        f"Chip = `$20,000,000 / field_alive`. Buy-in = **{fmt_money(BUYIN)}** "
        f"({N_ENTRIES} × {fmt_money(FEE)}).",
        "Wealth = `hedge_net + ours_alive × chip − buy-in`.",
        "",
    ]

    # Crowd facts
    fav_share = float(
        sum(
            C.crowd_share(a if C.vig_free_p(a) >= 0.5 else h)
            for a, _aml, h, _hml, _ in C.GAMES
        )
    )
    lines += [
        "## Slate facts",
        "",
        f"- Crowd share if every Circa favorite wins: **{fav_share*100:.2f}%** "
        f"→ field alive **{C.FIELD_START * fav_share:,.0f}** → chip **{fmt_money(C.POT / (C.FIELD_START * fav_share))}**.",
        f"- P(LAC loses) = **{fmt_pct(wmean(lac_lose.astype(float), prob))}** "
        f"(vig-free). Crowd on LAC: **{C.CROWD_PCT['LAC']:.1f}%**.",
        f"- P(JAC loses) = **{fmt_pct(wmean(jac_lose.astype(float), prob))}**. Crowd **{C.CROWD_PCT['JAC']:.1f}%**.",
        f"- P(DET loses) = **{fmt_pct(wmean(det_lose.astype(float), prob))}**. Crowd **{C.CROWD_PCT['DET']:.1f}%**.",
        f"- P(LAC, JAC, DET all win) = **{fmt_pct(wmean(chalk_hold.astype(float), prob))}**.",
        f"- P(at least one of those three loses) = **{fmt_pct(wmean(any_chalk_down.astype(float), prob))}**.",
        f"- Chip if LAC loses and other favorites hold: field share drops by 40.7 pp.",
        "",
    ]

    book_rows = []
    hedge_rows_by_book: dict[str, list[list[str]]] = {}
    juice_rows = []

    for book_name, book, _why in BOOKS:
        ours = ours_alive(book, win)
        p_wipe = wmean((ours == 0).astype(float), prob)
        e_ours = wmean(ours, prob)
        hedge_rows_by_book[book_name] = []
        for hname, tickets in hedges_for(book):
            hn = hedge_net(tickets, win)
            wealth = hn + ours * chip - BUYIN
            e_w = wmean(wealth, prob)
            e_hn = wmean(hn, prob)
            e_chip = wmean(ours * chip, prob)
            p_profit = wmean((wealth > 0).astype(float), prob)
            q05 = wquantile(wealth, prob, 0.05)
            q50 = wquantile(wealth, prob, 0.50)
            e_lac = wmean(wealth * lac_lose.astype(float), prob) / max(wmean(lac_lose.astype(float), prob), 1e-18)
            e_hold = wmean(wealth * chalk_hold.astype(float), prob) / max(wmean(chalk_hold.astype(float), prob), 1e-18)
            risked = sum(t.stake for t in tickets)
            row = [
                hname,
                str(len(tickets)),
                fmt_money(risked),
                fmt_money(e_hn),
                fmt_money(e_chip),
                fmt_money(e_w),
                fmt_pct(p_profit),
                fmt_money(q05),
                fmt_money(q50),
                fmt_money(e_hold),
                fmt_money(e_lac),
                fmt_pct(p_wipe) if hname == "naked" else "—",
            ]
            hedge_rows_by_book[book_name].append(row)
            if hname == "naked":
                book_rows.append([
                    book_name,
                    " ".join(f"{t}×{c}" for t, c in book.items()),
                    f"{e_ours:.2f}",
                    fmt_pct(p_wipe),
                    fmt_money(e_chip),
                    fmt_money(e_w),
                    fmt_pct(p_profit),
                    fmt_money(q05),
                ])
            juice_rows.append([book_name, hname, fmt_money(e_hn), fmt_money(risked)])

    lines += [
        "## Books with no hedge (naked) — where the money actually is",
        "",
        "| book | tickets | E[ours alive] | P(wipe) | E[chip portfolio] | E[wealth vs $10k] | P(wealth>0) | 5th pct wealth |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for r in book_rows:
        lines.append("| " + " | ".join(r) + " |")
    lines.append("")

    for book_name, book, why in BOOKS:
        lines += [
            f"## Hedge menu — {book_name}",
            "",
            f"_{why}. Book: `{ ' '.join(f'{t}×{c}' for t, c in book.items()) }`._",
            "",
            "| hedge | #tk | risked | E[hedge net] | E[chip] | E[wealth] | P(>0) | 5th pct | median | E[wealth \\| chalk holds] | E[wealth \\| LAC loses] | P(wipe) |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
        for r in hedge_rows_by_book[book_name]:
            lines.append("| " + " | ".join(r) + " |")
        lines.append("")

    # juice summary: mean E[hedge net] by strategy across fade books
    lines += [
        "## Juice: E[hedge net] is the sportsbook's cut",
        "",
        "Negative hedge net means Circa prices are not a gift. "
        "You are buying insurance at a retail markup.",
        "",
        "| book | hedge | E[hedge net] | cash risked |",
        "| --- | --- | ---: | ---: |",
    ]
    for r in juice_rows:
        if r[1] == "naked":
            continue
        lines.append("| " + " | ".join(r) + " |")
    lines.append("")

    # Conditional chip jump
    chip_hold = wmean(chip * chalk_hold.astype(float), prob) / wmean(chalk_hold.astype(float), prob)
    chip_lac = wmean(chip * lac_lose.astype(float), prob) / wmean(lac_lose.astype(float), prob)
    chip_any = wmean(chip * any_chalk_down.astype(float), prob) / wmean(any_chalk_down.astype(float), prob)
    lines += [
        "## Chip size under crowd events",
        "",
        f"- E[chip | LAC, JAC, DET all win] = **{fmt_money(chip_hold)}**",
        f"- E[chip | LAC loses] = **{fmt_money(chip_lac)}**",
        f"- E[chip | at least one of LAC/JAC/DET loses] = **{fmt_money(chip_any)}**",
        f"- Unconditional E[chip] = **{fmt_money(wmean(chip, prob))}**",
        "",
        "Unconditional chip is a mixture: most mass sits near the favorite-wins world "
        f"(~{fmt_money(chip_hold)}), with a long right tail when chalk dies.",
        "",
        f"Generated by `hedge_econ.py`. Probability checksum {float(prob.sum()):.12f}.",
    ]
    text = "\n".join(lines) + "\n"
    OUT.write_text(text, encoding="utf-8")
    print(text)
    print(f"wrote {OUT}")
    return text


if __name__ == "__main__":
    run()
