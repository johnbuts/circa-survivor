#!/usr/bin/env python3
"""CLI twin of week1/index.html — enumerate pick-book / chip / hedge outcomes.

Examples:
  python chug.py slate
  python chug.py hedge
  python chug.py hedge --hedge wipe --hedge 3cover --hedge wipe+3 --hedge rr3+4:each:10
  python chug.py hedge --detail wipe+3
  python chug.py scenarios --hedge rr3+4:each:25
  python chug.py chip --lose LAC
  python chug.py sandbox --hedge wipe --results BAL=W,TEN=L,PIT=W,LV=W
"""

from __future__ import annotations

import argparse
import itertools
import math
from dataclasses import dataclass
from typing import Iterable

FIELD_START = 20_000
POT = 20_000_000
LAMBDA = 0.7
CROWD_FLOOR = 0.01
DEFAULT_N = 10
DEFAULT_FEE = 1_000
DEFAULT_EACH = 10.0
DEFAULT_BANKROLL = 100.0
DEFAULT_PICKS = {"BAL": 3, "TEN": 3, "PIT": 2, "LV": 2}

GAMES: list[tuple[str, int, str, int, str]] = [
    ("NE", 166, "SEA", -198, "Thu"),
    ("SF", 180, "LAR", -215, "Thu"),
    ("BUF", -106, "HOU", -110, "Sun"),
    ("CHI", -146, "CAR", 124, "Sun"),
    ("CLE", 330, "JAC", -420, "Sun"),
    ("ATL", 136, "PIT", -162, "Sun"),
    ("NYJ", 120, "TEN", -142, "Sun"),
    ("NO", 290, "DET", -360, "Sun"),
    ("TB", 176, "CIN", -210, "Sun"),
    ("BAL", -186, "IND", 156, "Sun"),
    ("WAS", 198, "PHI", -240, "Sun"),
    ("GB", -102, "MIN", -116, "Sun"),
    ("MIA", 168, "LV", -200, "Sun"),
    ("ARI", 450, "LAC", -600, "Sun"),
    ("DAL", -146, "NYG", 124, "Sun"),
    ("DEN", 130, "KC", -154, "Mon"),
]

CROWD_PCT: dict[str, float] = {
    "ARI": 0.0, "ATL": 0.0, "BAL": 1.7, "BUF": 0.4, "CAR": 0.0, "CHI": 1.0,
    "CIN": 2.5, "CLE": 0.0, "DAL": 0.6, "DEN": 0.0, "DET": 16.2, "GB": 0.3,
    "HOU": 0.0, "IND": 0.0, "JAC": 20.2, "KC": 0.6, "LAC": 40.7, "LAR": 0.5,
    "LV": 3.3, "MIA": 0.0, "MIN": 0.0, "NE": 0.0, "NO": 0.0, "NYG": 0.0,
    "NYJ": 0.0, "PHI": 6.0, "PIT": 1.8, "SEA": 1.6, "SF": 0.0, "TB": 0.0,
    "TEN": 2.6, "WAS": 0.0,
}

ML: dict[str, int] = {}
OPP: dict[str, str] = {}
GAME_ID: dict[str, int] = {}
for i, (away, away_ml, home, home_ml, _when) in enumerate(GAMES):
    ML[away] = away_ml
    ML[home] = home_ml
    OPP[away] = home
    OPP[home] = away
    GAME_ID[away] = i
    GAME_ID[home] = i


def american_to_dec(ml: int) -> float:
    if ml > 0:
        return 1 + ml / 100
    return 1 + 100 / abs(ml)


def to_american(dec: float) -> int:
    if dec >= 2:
        return round((dec - 1) * 100)
    if dec > 1:
        return round(-100 / (dec - 1))
    return 0


def fmt_ml(n: int) -> str:
    return f"+{n}" if n > 0 else str(n)


def fmt_money(n: float) -> str:
    sign = "-" if n < 0 else ""
    return f"{sign}${abs(n):,.2f}"


def crowd_share(team: str) -> float:
    return CROWD_PCT.get(team, 0.0) / 100.0


def favorite_of(game: tuple[str, int, str, int, str]) -> str:
    away, away_ml, home, home_ml, _ = game
    return away if away_ml < home_ml else home


def vig_free_p(team: str) -> float:
    opp = OPP[team]
    p_t = 1 / american_to_dec(ML[team])
    p_o = 1 / american_to_dec(ML[opp])
    return p_t / (p_t + p_o)


def leverage(team: str) -> float:
    p = vig_free_p(team)
    s = max(crowd_share(team), CROWD_FLOOR)
    return math.log(p) - LAMBDA * math.log(s)


def parse_book(raw: str, n_entries: int) -> dict[str, int]:
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    if not parts:
        raise SystemExit("empty --picks")
    counts: dict[str, int] = {}
    typed = any(":" in p for p in parts)
    for p in parts:
        if ":" in p:
            team, _, n = p.partition(":")
            team = team.strip().upper()
            counts[team] = int(n)
        else:
            team = p.strip().upper()
            counts[team] = 0
    unknown = [t for t in counts if t not in ML]
    if unknown:
        raise SystemExit(f"unknown team(s): {', '.join(unknown)}")
    games = [GAME_ID[t] for t in counts]
    if len(games) != len(set(games)):
        raise SystemExit("cannot hold both sides of one game")
    if typed:
        return counts
    base, rem = divmod(n_entries, len(counts))
    for i, t in enumerate(counts):
        counts[t] = base + (1 if i < rem else 0)
    return counts


def parse_books(values: list[str] | None, n_entries: int) -> list[dict[str, int]]:
    if not values:
        return [dict(DEFAULT_PICKS)]
    return [parse_book(v, n_entries) for v in values]


def combinations(arr: list[str], k: int) -> list[list[str]]:
    return [list(c) for c in itertools.combinations(arr, k)]


def ticket_id(opps: Iterable[str]) -> str:
    return "|".join(sorted(opps))


def parlay_decimal(opps: Iterable[str]) -> float:
    p = 1.0
    for t in opps:
        p *= american_to_dec(ML[t])
    return p


@dataclass(frozen=True)
class Ticket:
    k: int
    picks: tuple[str, ...]
    opps: tuple[str, ...]
    dec: float
    stake: float
    enabled: bool = True

    @property
    def id(self) -> str:
        return ticket_id(self.opps)


@dataclass(frozen=True)
class HedgeSpec:
    name: str
    sizes: tuple[int, ...]
    mode: str  # none | cover | each | split
    amount: float = 0.0


def parse_sizes_token(raw: str, n_picks: int) -> tuple[int, ...]:
    raw = raw.strip().lower().replace(" ", "")
    if raw in {"", "none", "naked"}:
        return ()
    parts: list[int] = []
    for tok in raw.replace("+", ",").split(","):
        if tok in {"wipe", "n"}:
            if n_picks >= 2:
                parts.append(n_picks)
            continue
        if tok.startswith("rr") and tok[2:].isdigit():
            tok = tok[2:]
        if not tok:
            continue
        k = int(tok)
        if k < 2:
            raise SystemExit(f"leg size must be >= 2, got {k}")
        if k <= n_picks:
            parts.append(k)
    return tuple(sorted(set(parts)))


def parse_stake_token(raw: str, each: float, bankroll: float) -> tuple[str, float]:
    raw = (raw or "none").strip().lower()
    if raw in {"none", "0", "naked"}:
        return "none", 0.0
    if raw == "cover":
        return "cover", 0.0
    if raw == "each":
        return "each", each
    if raw == "split":
        return "split", bankroll
    if raw.startswith("each:"):
        return "each", float(raw.split(":", 1)[1])
    if raw.startswith("split:"):
        return "split", float(raw.split(":", 1)[1])
    raise SystemExit(f"unknown stake {raw!r} (none | cover | each[:amt] | split[:amt])")


HEDGE_ALIASES = {
    "none": ("", "none"),
    "naked": ("", "none"),
    "wipe": ("wipe", "cover"),
    "3": ("3", "cover"),
    "3cover": ("3", "cover"),
    "2cover": ("2", "cover"),
    "wipe+3": ("3,wipe", "cover"),
    "wipe,3": ("3,wipe", "cover"),
    "3+wipe": ("3,wipe", "cover"),
    "rr2": ("2", "each"),
    "rr3": ("3", "each"),
    "rr4": ("4", "each"),
    "rr3+4": ("3,4", "each"),
    "rr2+3": ("2,3", "each"),
    "rr2+3+4": ("2,3,4", "each"),
    "full": ("2,3,4,5", "each"),
    "split3+4": ("3,4", "split"),
    "split2+3+4": ("2,3,4", "split"),
    "html": ("3,4", "each"),
}


def parse_hedge_spec(raw: str, n_picks: int, each: float, bankroll: float) -> HedgeSpec:
    s = raw.strip()
    if not s:
        raise SystemExit("empty --hedge")
    key = s.lower().replace(" ", "")
    if key in HEDGE_ALIASES:
        sizes_s, stake_s = HEDGE_ALIASES[key]
        sizes = parse_sizes_token(sizes_s, n_picks)
        mode, amt = parse_stake_token(stake_s, each, bankroll)
        return HedgeSpec(name=key, sizes=sizes, mode=mode, amount=amt)
    if ":" in s:
        sizes_s, stake_s = s.split(":", 1)
    else:
        sizes_s, stake_s = s, "cover"
    sizes = parse_sizes_token(sizes_s, n_picks)
    mode, amt = parse_stake_token(stake_s, each, bankroll)
    name = f"{'+'.join(str(k) for k in sizes) or 'none'}:{mode}"
    if mode in {"each", "split"}:
        name += f":{amt:g}"
    return HedgeSpec(name=name, sizes=sizes, mode=mode, amount=amt)


def hedge_from_args(args: argparse.Namespace, n_picks: int) -> HedgeSpec:
    each = float(getattr(args, "each", DEFAULT_EACH) or DEFAULT_EACH)
    bankroll = float(getattr(args, "bankroll", DEFAULT_BANKROLL) or DEFAULT_BANKROLL)
    specs = [x for x in (getattr(args, "hedge", None) or []) if x]
    if specs:
        return parse_hedge_spec(specs[0], n_picks, each, bankroll)
    cover = getattr(args, "cover", "none") or "none"
    if cover != "none":
        return parse_hedge_spec(cover, n_picks, each, bankroll)
    sizes_raw = getattr(args, "sizes", "") or ""
    stake_raw = getattr(args, "stake", "none") or "none"
    if sizes_raw:
        return parse_hedge_spec(f"{sizes_raw}:{stake_raw}", n_picks, each, bankroll)
    return HedgeSpec(name="naked", sizes=(), mode="none", amount=0.0)


def default_hedge_menu(n_picks: int, each: float, bankroll: float) -> list[HedgeSpec]:
    names = ["naked", "wipe"]
    if n_picks >= 2:
        names += ["2cover", "rr2"]
    if n_picks >= 3:
        names += ["3cover", "wipe+3", "rr3"]
    if n_picks >= 4:
        names += ["rr4", "rr3+4", "rr2+3+4", "split3+4", "split2+3+4"]
    elif n_picks >= 3:
        names += ["rr2+3"]
    seen: set[str] = set()
    out: list[HedgeSpec] = []
    for name in names:
        spec = parse_hedge_spec(name, n_picks, each, bankroll)
        if spec.name in seen:
            continue
        seen.add(spec.name)
        out.append(spec)
    return out


def build_tickets(
    picks: list[str],
    counts: dict[str, int],
    n_entries: int,
    fee: float,
    spec: HedgeSpec,
) -> list[Ticket]:
    n = len(picks)
    raw: list[Ticket] = []
    for k in spec.sizes:
        if k > n:
            continue
        for group in combinations(picks, k):
            opps = tuple(OPP[t] for t in group)
            dec = parlay_decimal(opps)
            raw.append(Ticket(k=k, picks=tuple(group), opps=opps, dec=dec, stake=0.0))
    if not raw or spec.mode == "none":
        return raw
    if spec.mode == "each":
        return [
            Ticket(k=t.k, picks=t.picks, opps=t.opps, dec=t.dec, stake=spec.amount)
            for t in raw
        ]
    if spec.mode == "split":
        each = spec.amount / len(raw)
        return [
            Ticket(k=t.k, picks=t.picks, opps=t.opps, dec=t.dec, stake=each)
            for t in raw
        ]
    sized = []
    for t in raw:
        dead = n_entries if t.k == n else sum(counts[p] for p in t.picks)
        stake = (dead * fee) / (t.dec - 1) if t.dec > 1 else 0.0
        sized.append(Ticket(k=t.k, picks=t.picks, opps=t.opps, dec=t.dec, stake=stake))
    return sized


def mix_label(tickets: list[Ticket]) -> str:
    if not tickets:
        return "none"
    counts: dict[int, int] = {}
    for t in tickets:
        counts[t.k] = counts.get(t.k, 0) + 1
    return " + ".join(f"{counts[k]}×{k}-leg" for k in sorted(counts))


def evaluate(
    pick_wins: dict[str, bool],
    picks: list[str],
    counts: dict[str, int],
    tickets: list[Ticket],
    fee: float,
) -> dict:
    live = 0
    dead = 0
    alive: dict[str, int] = {}
    for t in picks:
        c = counts[t]
        if pick_wins[t]:
            alive[t] = c
            live += c
        else:
            dead += c
    payout = 0.0
    stake = 0.0
    profit = 0.0
    hits: list[Ticket] = []
    for tk in tickets:
        if not tk.enabled:
            continue
        stake += tk.stake
        if all(not pick_wins[p] for p in tk.picks):
            payout += tk.stake * tk.dec
            profit += tk.stake * (tk.dec - 1)
            hits.append(tk)
    bet_net = payout - stake
    dead_cost = dead * fee
    return {
        "live": live,
        "dead": dead,
        "alive": alive,
        "payout": payout,
        "stake": stake,
        "profit": profit,
        "bet_net": bet_net,
        "dead_cost": dead_cost,
        "week": bet_net - dead_cost,
        "hits": hits,
    }


def mask_prob_vf(picks: list[str], pick_wins: dict[str, bool]) -> float:
    p = 1.0
    for t in picks:
        wp = vig_free_p(t)
        p *= wp if pick_wins[t] else (1.0 - wp)
    return p


def enumerate_masks(
    picks: list[str],
    counts: dict[str, int],
    tickets: list[Ticket],
    fee: float,
) -> list[dict]:
    n = len(picks)
    rows = []
    for mask in range(1 << n):
        pick_wins = {t: bool(mask & (1 << i)) for i, t in enumerate(picks)}
        wins = sum(1 for t in picks if pick_wins[t])
        r = evaluate(pick_wins, picks, counts, tickets, fee)
        winners = [t for t in picks if pick_wins[t]]
        rows.append({
            **r,
            "wins": wins,
            "losses": n - wins,
            "winners": winners,
            "p": mask_prob_vf(picks, pick_wins),
        })
    rows.sort(key=lambda r: (r["losses"], -r["p"]))
    return rows


def summarize(rows: list[dict], n_picks: int) -> dict:
    ev = sum(r["p"] * r["week"] for r in rows)
    worst = min(rows, key=lambda r: r["week"])
    by_k: dict[int, float] = {}
    p_k: dict[int, float] = {}
    for r in rows:
        p_k[r["losses"]] = p_k.get(r["losses"], 0.0) + r["p"]
        by_k[r["losses"]] = by_k.get(r["losses"], 0.0) + r["p"] * r["week"]
    mean_k = {k: by_k[k] / p_k[k] for k in p_k}
    wipe = next(r for r in rows if r["losses"] == n_picks)
    all_win = next(r for r in rows if r["losses"] == 0)
    p_pos = sum(r["p"] for r in rows if r["week"] >= -1e-9)
    return {
        "ev": ev,
        "worst": worst,
        "mean_k": mean_k,
        "p_k": p_k,
        "wipe": wipe,
        "all_win": all_win,
        "p_pos": p_pos,
    }


def print_tickets(tickets: list[Ticket]) -> None:
    if not tickets:
        print("tickets: none")
        return
    rows = []
    for tk in tickets:
        rows.append([
            f"{tk.k}-leg",
            "+".join(tk.opps),
            " ".join(tk.picks) + " lose",
            fmt_ml(to_american(tk.dec)),
            f"{tk.dec:.3f}",
            fmt_money(tk.stake),
        ])
    print_table(["k", "opponents", "hits when", "ML", "dec", "stake"], rows)


def print_scenario_rows(rows: list[dict]) -> None:
    table = []
    for r in rows:
        hit = ", ".join(f"{h.k}:{'+'.join(h.opps)}" for h in r["hits"]) or "—"
        table.append([
            " ".join(r["winners"]) or "wipeout",
            str(r["live"]),
            f"{r['p']*100:.2f}%",
            hit,
            fmt_money(r["profit"]),
            fmt_money(r["dead_cost"]),
            fmt_money(r["week"]),
        ])
    print_table(
        ["picks that win", "alive", "P(vf)", "tickets hit", "hedge profit", "dead $", "week P&L"],
        table,
    )


def print_loss_bands(summary: dict, n_picks: int) -> None:
    print("by # of pick-team losses:")
    for k in sorted(summary["p_k"]):
        label = "all win" if k == 0 else ("wipeout" if k == n_picks else f"{k} lose")
        print(
            f"  {label:10}  P={summary['p_k'][k]*100:6.2f}%  "
            f"E[P&L]={fmt_money(summary['mean_k'][k]):>12}"
        )


def default_winners(lose: list[str], win: list[str]) -> list[str]:
    forced: dict[int, str] = {}
    for team in win:
        t = team.upper()
        if t not in ML:
            raise SystemExit(f"unknown --win team {t}")
        forced[GAME_ID[t]] = t
    for team in lose:
        t = team.upper()
        if t not in ML:
            raise SystemExit(f"unknown --lose team {t}")
        gid = GAME_ID[t]
        if gid in forced and forced[gid] == t:
            raise SystemExit(f"{t} cannot be both --win and --lose")
        forced[gid] = OPP[t]
    out = []
    for i, g in enumerate(GAMES):
        out.append(forced.get(i, favorite_of(g)))
    return out


def chip_snapshot(winners: list[str], counts: dict[str, int]) -> dict:
    won = set(winners)
    share = sum(crowd_share(t) for t in winners)
    field_alive = FIELD_START * share
    chip = POT / field_alive if field_alive > 0 else 0.0
    ours_alive = sum(n for t, n in counts.items() if t in won)
    ours_dead = sum(counts.values()) - ours_alive
    return {
        "winners": winners,
        "share": share,
        "field_alive": field_alive,
        "field_dead": FIELD_START - field_alive,
        "chip": chip,
        "ours_alive": ours_alive,
        "ours_dead": ours_dead,
        "portfolio": ours_alive * chip,
        "won_picks": [t for t in counts if t in won],
        "lost_picks": [t for t in counts if t not in won],
    }


def book_label(counts: dict[str, int]) -> str:
    return " ".join(f"{t}×{n}" for t, n in counts.items())


def print_table(headers: list[str], rows: list[list[str]]) -> None:
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))
    fmt = "  ".join(f"{{:<{w}}}" for w in widths)
    print(fmt.format(*headers))
    print("  ".join("-" * w for w in widths))
    for row in rows:
        print(fmt.format(*row))


def cmd_slate(_args: argparse.Namespace) -> None:
    rows = []
    for away, away_ml, home, home_ml, when in GAMES:
        fav = away if away_ml < home_ml else home
        rows.append([
            when,
            f"{away} {fmt_ml(away_ml)}",
            f"{home} {fmt_ml(home_ml)}",
            fav,
            f"{CROWD_PCT[away]:.1f}",
            f"{CROWD_PCT[home]:.1f}",
            f"{leverage(away):.2f}",
            f"{leverage(home):.2f}",
            f"{vig_free_p(away)*100:.1f}",
            f"{vig_free_p(home)*100:.1f}",
        ])
    print_table(
        ["when", "away", "home", "fav", "crowdA", "crowdH", "levA", "levH", "pA%", "pH%"],
        rows,
    )
    print()
    ranked = sorted(ML, key=leverage, reverse=True)
    print("leverage rank (vig-free Circa, crowd floor 1%):")
    for i, t in enumerate(ranked[:12], 1):
        print(
            f"  {i:2}  {t:3}  lev {leverage(t):6.3f}  "
            f"p={vig_free_p(t)*100:5.1f}%  crowd={CROWD_PCT[t]:4.1f}%"
        )


def cmd_cover(args: argparse.Namespace) -> None:
    counts = parse_books(args.picks, args.n)[0]
    picks = list(counts)
    n_picks = len(picks)
    print(f"book  {book_label(counts)}   N={args.n}  fee={fmt_money(args.fee)}")
    print("cover stake = (dead entries on those legs × fee) / (decimal − 1)")
    print("wipeout n-leg uses N; a k-leg uses the sum of counts on those k picks.")
    print()
    for k in range(2, n_picks + 1):
        print(f"{k}-leg round robin  C({n_picks},{k})={math.comb(n_picks, k)}")
        for group in combinations(picks, k):
            opps = [OPP[t] for t in group]
            dec = parlay_decimal(opps)
            dead = args.n if k == n_picks else sum(counts[t] for t in group)
            leftover = [t for t in picks if t not in group]
            stake = (dead * args.fee) / (dec - 1) if dec > 1 else 0.0
            left = "/".join(leftover) if leftover else "wipeout"
            print(
                f"  {' + '.join(opps):24}  leftover {left:12}  "
                f"dead {dead:2}  dec={dec:7.3f}  {fmt_ml(to_american(dec)):6}  "
                f"stake {fmt_money(stake)}"
            )
        print()
    print("wipeout correlation: if every pick loses, every k-leg AND the n-leg all hit.")
    print("Do not stack cover-sized 3s with a cover-sized wipe unless you want to be long wipeout.")


def cmd_hedge(args: argparse.Namespace) -> None:
    counts = parse_books(args.picks, args.n)[0]
    picks = list(counts)
    n_picks = len(picks)
    each = args.each
    bankroll = args.bankroll
    requested = [x for x in (args.hedge or []) if x]
    if requested:
        specs = [parse_hedge_spec(x, n_picks, each, bankroll) for x in requested]
    else:
        specs = default_hedge_menu(n_picks, each, bankroll)
    detail = (args.detail or "").strip().lower()
    print(f"book  {book_label(counts)}   N={args.n}  fee={fmt_money(args.fee)}")
    print(f"each  {fmt_money(each)}   bankroll {fmt_money(bankroll)}")
    print("P from vig-free Circa, independent games. Week P&L = hedge net − dead fees.")
    print()
    table = []
    scored: list[tuple[HedgeSpec, list[Ticket], list[dict], dict]] = []
    for spec in specs:
        tickets = build_tickets(picks, counts, args.n, args.fee, spec)
        rows = enumerate_masks(picks, counts, tickets, args.fee)
        summary = summarize(rows, n_picks)
        scored.append((spec, tickets, rows, summary))
        risked = sum(t.stake for t in tickets)
        one = summary["mean_k"].get(1, 0.0)
        n1 = summary["mean_k"].get(n_picks - 1, 0.0) if n_picks > 1 else 0.0
        table.append([
            spec.name,
            mix_label(tickets),
            str(len(tickets)),
            fmt_money(risked),
            fmt_money(summary["ev"]),
            fmt_money(summary["worst"]["week"]),
            " ".join(summary["worst"]["winners"]) or "wipeout",
            fmt_money(summary["all_win"]["week"]),
            fmt_money(one) if n_picks > 1 else "—",
            fmt_money(n1) if n_picks > 1 else "—",
            fmt_money(summary["wipe"]["week"]),
            f"{summary['p_pos']*100:.1f}%",
        ])
    print_table(
        [
            "strategy", "mix", "#", "risked", "E[week]", "worst", "worst when",
            "all win", "1 lose", f"{n_picks-1} lose" if n_picks > 1 else "n-1",
            "wipe", "P(≥0)",
        ],
        table,
    )
    print()
    print("aliases: naked | wipe | 2cover | 3cover | wipe+3 | rr2 | rr3 | rr4 | rr3+4 | rr2+3+4 | full")
    print("custom:  --hedge 3,4:each:25   --hedge 2,3,4:cover   --hedge 3,4:split:200")
    print("HTML default sizes are 3+4. wipe+3 cover-sizes both → long wipeout (subsets also hit).")

    show = scored
    if detail:
        show = [x for x in scored if x[0].name == detail or x[0].name.startswith(detail)]
        if not show:
            raise SystemExit(f"no strategy matching --detail {args.detail!r}")
    elif len(scored) == 1:
        show = scored
    else:
        return
    for spec, tickets, rows, summary in show:
        print()
        print(f"=== {spec.name}  {mix_label(tickets)}  risked {fmt_money(sum(t.stake for t in tickets))} ===")
        print_tickets(tickets)
        print()
        print_scenario_rows(rows)
        print()
        print(f"E[week P&L]  {fmt_money(summary['ev'])}")
        print(
            f"worst row    {fmt_money(summary['worst']['week'])}   "
            f"when {(' '.join(summary['worst']['winners']) or 'wipeout')}"
        )
        print_loss_bands(summary, n_picks)


def cmd_scenarios(args: argparse.Namespace) -> None:
    counts = parse_books(args.picks, args.n)[0]
    picks = list(counts)
    spec = hedge_from_args(args, len(picks))
    tickets = build_tickets(picks, counts, args.n, args.fee, spec)
    risked = sum(tk.stake for tk in tickets)
    print(f"book   {book_label(counts)}   N={args.n}  fee={fmt_money(args.fee)}")
    print(f"hedge  {spec.name}   {mix_label(tickets)}   risked={fmt_money(risked)}")
    print_tickets(tickets)
    print()
    rows = enumerate_masks(picks, counts, tickets, args.fee)
    summary = summarize(rows, len(picks))
    print_scenario_rows(rows)
    print()
    print(f"E[week P&L]  {fmt_money(summary['ev'])}   (vig-free Circa, independent games)")
    print(
        f"worst row    {fmt_money(summary['worst']['week'])}   "
        f"when {(' '.join(summary['worst']['winners']) or 'wipeout')}"
    )
    print()
    print_loss_bands(summary, len(picks))


def cmd_chip(args: argparse.Namespace) -> None:
    counts = parse_books(args.picks, args.n)[0]
    lose = [x.strip() for x in (args.lose or "").split(",") if x.strip()]
    win = [x.strip() for x in (args.win or "").split(",") if x.strip()]
    winners = default_winners(lose, win)
    snap = chip_snapshot(winners, counts)
    chalk = ["LAC", "JAC", "DET"]
    chalk_dead = [t for t in chalk if t not in snap["winners"]]
    print(f"book  {book_label(counts)}")
    print(
        f"flips  lose={','.join(t.upper() for t in lose) or '—'}  "
        f"win={','.join(t.upper() for t in win) or '—'}  (else Circa favorite)"
    )
    if chalk_dead:
        print(f"chalk down: {', '.join(chalk_dead)}")
    else:
        print("chalk holds: LAC JAC DET all win")
    print()
    print(f"field alive   {snap['field_alive']:,.1f}   ({snap['share']*100:.2f}% of crowd)")
    print(f"field dead    {snap['field_dead']:,.1f}")
    print(f"our alive     {snap['ours_alive']}  ({' '.join(snap['won_picks']) or '—'})")
    print(f"our dead      {snap['ours_dead']}  ({' '.join(snap['lost_picks']) or '—'})")
    print(f"chip / live   {fmt_money(snap['chip'])}")
    print(f"portfolio     {fmt_money(snap['portfolio'])}")
    print()
    print("our entries:")
    rows = []
    i = 1
    won = set(snap["winners"])
    for t, n in counts.items():
        live = t in won
        for _ in range(n):
            rows.append([
                f"{t}-{i}", t, f"{CROWD_PCT[t]:.1f}",
                "live" if live else "dead",
                fmt_money(snap["chip"] if live else 0.0),
            ])
            i += 1
    print_table(["entry", "pick", "crowd%", "status", "chip EV"], rows)


def cmd_sandbox(args: argparse.Namespace) -> None:
    counts = parse_books(args.picks, args.n)[0]
    picks = list(counts)
    spec = hedge_from_args(args, len(picks))
    tickets = build_tickets(picks, counts, args.n, args.fee, spec)
    results: dict[str, bool] = {}
    for part in (args.results or "").split(","):
        part = part.strip()
        if not part:
            continue
        team, _, val = part.partition("=")
        team = team.strip().upper()
        val = val.strip().upper()
        if team not in counts:
            raise SystemExit(f"{team} is not in the book")
        if val not in {"W", "L"}:
            raise SystemExit(f"result for {team} must be W or L")
        results[team] = val == "W"
    missing = [t for t in picks if t not in results]
    if missing:
        raise SystemExit(f"mark every pick W/L; missing {', '.join(missing)}")
    r = evaluate(results, picks, counts, tickets, args.fee)
    live_teams = [t for t in picks if results[t]]
    hit = " · ".join("+".join(h.opps) for h in r["hits"]) or "no tickets hit"
    print(f"book   {book_label(counts)}")
    print(f"hedge  {spec.name}  {mix_label(tickets)}  risked {fmt_money(sum(tk.stake for tk in tickets))}")
    marked = " ".join(f"{t}={'W' if results[t] else 'L'}" for t in picks)
    print(f"result {marked}")
    print()
    print(f"entries alive  {r['live']}   ({' '.join(live_teams) or 'all dead'})")
    print(f"dead entry $   {fmt_money(r['dead_cost'])}")
    print(f"hedge profit   {fmt_money(r['profit'])}   tickets: {hit}")
    print(f"hedge net      {fmt_money(r['bet_net'])}")
    print(f"week P&L       {fmt_money(r['week'])}")
    if args.chip:
        lose = [t for t in picks if not results[t]]
        extra_lose = [x.strip() for x in (args.lose or "").split(",") if x.strip()]
        extra_win = [x.strip() for x in (args.win or "").split(",") if x.strip()]
        winners = default_winners(lose + extra_lose, extra_win)
        snap = chip_snapshot(winners, counts)
        print()
        print(f"chip / live    {fmt_money(snap['chip'])}   field {snap['field_alive']:,.0f}")
        print(f"portfolio      {fmt_money(snap['portfolio'])}")


def cmd_compare(args: argparse.Namespace) -> None:
    books = parse_books(args.picks, args.n)
    lose_sets = [
        ("favs hold", []),
        ("LAC lose", ["LAC"]),
        ("JAC lose", ["JAC"]),
        ("DET lose", ["DET"]),
        ("LAC+JAC lose", ["LAC", "JAC"]),
        ("all chalk die", ["LAC", "JAC", "DET"]),
    ]
    print(f"N={args.n}  fee={fmt_money(args.fee)}  chip = $20M / field_alive")
    print()
    headers = ["book", "E[n]", "P(wipe)", "P(all 10)"] + [name for name, _ in lose_sets]
    rows = []
    for counts in books:
        picks = list(counts)
        n = len(picks)
        e_n = 0.0
        p_wipe = 0.0
        p_all = 0.0
        for mask in range(1 << n):
            pick_wins = {t: bool(mask & (1 << i)) for i, t in enumerate(picks)}
            p = mask_prob_vf(picks, pick_wins)
            live = sum(counts[t] for t in picks if pick_wins[t])
            e_n += p * live
            if live == 0:
                p_wipe += p
            if live == sum(counts.values()):
                p_all += p
        cells = [book_label(counts), f"{e_n:.2f}", f"{p_wipe*100:.1f}%", f"{p_all*100:.1f}%"]
        for _name, lose in lose_sets:
            snap = chip_snapshot(default_winners(lose, []), counts)
            cells.append(f"{snap['ours_alive']}/{fmt_money(snap['portfolio'])}")
        rows.append(cells)
    print_table(headers, rows)
    print()
    print("chip cells = ours_alive / portfolio chip EV  (favorites win except named losers)")


def build_parser() -> argparse.ArgumentParser:
    shared = argparse.ArgumentParser(add_help=False)
    shared.add_argument("--picks", action="append", help="BAL:3,TEN:3,PIT:2,LV:2")
    shared.add_argument("--n", type=int, default=DEFAULT_N)
    shared.add_argument("--fee", type=float, default=DEFAULT_FEE)
    shared.add_argument("--each", type=float, default=DEFAULT_EACH, help="fill-each dollar amount")
    shared.add_argument("--bankroll", type=float, default=DEFAULT_BANKROLL, help="split-bankroll pool")
    shared.add_argument(
        "--hedge", action="append", default=[],
        help="strategy spec (repeatable). aliases or sizes:stake e.g. rr3+4:each:10",
    )
    shared.add_argument("--cover", default="none", help="legacy alias for --hedge (wipe | 3 | wipe,3)")
    shared.add_argument("--sizes", default="", help="2,3,4  (used with --stake if no --hedge)")
    shared.add_argument("--stake", default="none", help="none | cover | each[:amt] | split[:amt]")
    shared.add_argument("--lose", default="", help="comma teams forced to lose")
    shared.add_argument("--win", default="", help="comma teams forced to win")
    p = argparse.ArgumentParser(
        description="Plug-and-chug week-1 pick-book / chip / hedge outcomes.",
        parents=[shared],
    )
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("slate", help="full week-1 board: ML, crowd, leverage", parents=[shared])
    sub.add_parser("cover", help="cover-sized stake for every k-leg round robin", parents=[shared])
    hg = sub.add_parser("hedge", help="compare round-robin / cover / fill / split strategies", parents=[shared])
    hg.add_argument("--detail", default="", help="dump tickets + 2^n rows for this strategy name")
    sub.add_parser("scenarios", help="2^n pick-outcome rows for one hedge", parents=[shared])
    sub.add_parser("chip", help="field / chip EV given flipped games", parents=[shared])
    sb = sub.add_parser("sandbox", help="mark each pick W/L and score hedge", parents=[shared])
    sb.add_argument("--results", required=True, help="BAL=W,TEN=L,PIT=W,LV=W")
    sb.add_argument("--chip", action="store_true", help="also print chip snapshot")
    sub.add_parser("compare", help="several books × chalk-loss chip snapshots", parents=[shared])
    return p


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.cmd is None:
        parser.print_help()
        print("\n--- default dump: hedge menu ---\n")
        args.hedge = []
        args.detail = ""
        cmd_hedge(args)
        return
    {
        "slate": cmd_slate,
        "cover": cmd_cover,
        "hedge": cmd_hedge,
        "scenarios": cmd_scenarios,
        "chip": cmd_chip,
        "sandbox": cmd_sandbox,
        "compare": cmd_compare,
    }[args.cmd](args)


if __name__ == "__main__":
    main()
