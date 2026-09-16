"""Run Week 1 score → compare → one-lever iterate. Writes only under Week2_v2."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path

import pandas as pd

from score_week1 import (
    ACTUAL_HHI,
    ACTUAL_TOP3_SUM,
    FOCUS,
    OUT,
    apply_pit_steam,
    build_2026_gtw,
    historical_week1_top,
    load_actual_shares,
    load_fit_bundle,
    load_posted_spreads,
    score_week1,
    week1_frame,
)
from score_week1 import Metrics

HERE = Path(__file__).resolve().parent
TODAY = date.today().isoformat()


@dataclass
class Round:
    iter_id: int
    title: str
    change: str
    why: str
    keep: bool
    next_step: str
    learned: str
    metrics: Metrics
    hist_team: str
    hist_top: float
    hist_hhi: float
    steam: bool
    tau: float
    third_delta: float
    fv_gamma: float
    safe_third: float


def primary_loss(m: Metrics) -> float:
    return m.jac_err + m.lac_err + m.pit_err + m.det_err


def better(new: Metrics, old: Metrics) -> bool:
    if new.close and not old.close:
        return True
    if primary_loss(new) < primary_loss(old) - 1e-6:
        return True
    if abs(primary_loss(new) - primary_loss(old)) < 1e-6 and new.top5_mae < old.top5_mae:
        return True
    return False


def hist_ok(top_share: float, baseline_top: float) -> bool:
    return top_share <= baseline_top + 0.08


def shares_table(m: Metrics, actual: dict[str, float]) -> str:
    lines = [
        "| team | pred % | actual % | err pp | implied |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    rest_pred = 0.0
    rest_act = 0.0
    for team in FOCUS:
        p = 100 * m.shares[team]
        a = 100 * actual[team]
        lines.append(
            f"| {team} | {p:.2f} | {a:.2f} | {p - a:+.2f} | {100 * m.implied[team]:.1f} |"
        )
    for team, a in actual.items():
        if team in FOCUS:
            continue
        rest_pred += m.shares.get(team, 0.0)
        rest_act += a
    lines.append(
        f"| other | {100 * rest_pred:.2f} | {100 * rest_act:.2f} | "
        f"{100 * (rest_pred - rest_act):+.2f} | — |"
    )
    return "\n".join(lines)


def round_md(r: Round, actual: dict[str, float]) -> str:
    m = r.metrics
    verdict = "KEEP" if r.keep else "REVERT"
    close = "yes" if m.close else "no"
    return "\n".join(
        [
            f"### Iter {r.iter_id} — {r.title}",
            "",
            f"- Date: {TODAY}",
            f"- Change: {r.change}",
            f"- Why: {r.why}",
            f"- Verdict: **{verdict}**",
            f"- Close: **{close}**",
            f"- Next: {r.next_step}",
            "",
            shares_table(m, actual),
            "",
            f"- Top 3: `{m.top3[0]} / {m.top3[1]} / {m.top3[2]}` (need JAC / LAC / PIT)",
            f"- Top-3 sum: {100 * m.top3_sum:.1f}% (actual {100 * ACTUAL_TOP3_SUM:.1f}%)",
            f"- Top-5 MAE: {100 * m.top5_mae:.2f} pp (need ≤ 3)",
            f"- JAC/LAC/PIT/DET abs err: {100 * m.jac_err:.2f} / {100 * m.lac_err:.2f} / "
            f"{100 * m.pit_err:.2f} / {100 * m.det_err:.2f} pp",
            f"- Predicted HHI: {m.hhi:.3f} (actual ~{ACTUAL_HHI:.2f})",
            f"- 2025 Week 1 sanity: top `{r.hist_team}` {100 * r.hist_top:.1f}%, HHI {r.hist_hhi:.3f}",
            f"- Knobs: steam={r.steam}, tau={r.tau:.3f}, third_delta={r.third_delta:.2f}, "
            f"fv_gamma={r.fv_gamma:.2f}, safe_third={r.safe_third:.2f}",
            "",
            r.learned,
            "",
        ]
    )


def write_csv(iter_id: int, m: Metrics, actual: dict[str, float]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for team in sorted(m.shares):
        rows.append(
            {
                "team": team,
                "pred_share": m.shares[team],
                "actual_share": actual.get(team, 0.0),
                "implied_win_prob": m.implied[team],
            }
        )
    pd.DataFrame(rows).to_csv(OUT / f"iter_{iter_id}.csv", index=False)


def write_report(rounds: list[Round], actual: dict[str, float]) -> None:
    latest = rounds[-1]
    m = latest.metrics
    status = [
        "# Week 1 crowd-model iterations",
        "",
        "## Latest",
        "",
        f"- {TODAY} — **iter {latest.iter_id}: {latest.title}** "
        f"({'CLOSE' if m.close else 'not close'}).",
        f"- Top 3 `{m.top3[0]}/{m.top3[1]}/{m.top3[2]}`. "
        f"PIT {100 * m.shares['PIT']:.1f}% vs 16.1% actual. "
        f"DET {100 * m.shares['DET']:.1f}% vs 7.1%.",
        f"- See iter {latest.iter_id} below for the table.",
        "",
        "## Isolation",
        "",
        "All writes are under `model_crafting/Week2_v2/`. Parent `model/`, `data/`, "
        "and pick HTML are read-only.",
        "",
        "## Close rule",
        "",
        "Top 3 JAC, LAC, PIT; JAC/LAC ≤ 3pp; PIT ≤ 5pp; DET ≤ 3pp; top-5 MAE ≤ 3pp; "
        "top-3 sum within 5pp of 78.9%.",
        "",
        "## Iteration log",
        "",
    ]
    body = "\n".join(round_md(r, actual) for r in reversed(rounds))
    (HERE / "report.md").write_text("\n".join(status) + body, encoding="utf-8")


def score_config(
    *,
    steam: bool,
    tau: float,
    third_delta: float,
    fv_gamma: float,
    safe_third: float,
    gtw_base,
    gtw_steam,
    scalers,
    beta,
    actual,
    train_gtw,
):
    week = week1_frame(gtw_steam if steam else gtw_base)
    m = score_week1(
        week,
        scalers,
        beta,
        actual,
        tau=tau,
        third_chalk_delta=third_delta,
        safe_third_delta=safe_third,
        fv_gap_gamma=fv_gamma,
    )
    hist_team, hist_top, hist_hhi = historical_week1_top(train_gtw, scalers, beta, tau)
    return m, hist_team, hist_top, hist_hhi


def pick_tau(current, gtw_base, gtw_steam, scalers, beta, actual, train_gtw, hist0_top):
    best = None
    best_m = None
    for tau in (1.10, 1.20, 1.30, 1.40):
        m, team, top, hhi = score_config(
            steam=current["steam"],
            tau=tau,
            third_delta=current["third_delta"],
            fv_gamma=current["fv_gamma"],
            safe_third=current["safe_third"],
            gtw_base=gtw_base,
            gtw_steam=gtw_steam,
            scalers=scalers,
            beta=beta,
            actual=actual,
            train_gtw=train_gtw,
        )
        if not hist_ok(top, hist0_top):
            continue
        if best_m is None or better(m, best_m):
            best = (tau, m, team, top, hhi)
            best_m = m
    return best


def pick_third(current, gtw_base, gtw_steam, scalers, beta, actual, train_gtw, hist0_top):
    best = None
    best_m = None
    for delta in (0.5, 1.0, 1.5, 2.0, 2.5, 3.0):
        m, team, top, hhi = score_config(
            steam=current["steam"],
            tau=current["tau"],
            third_delta=delta,
            fv_gamma=current["fv_gamma"],
            safe_third=current["safe_third"],
            gtw_base=gtw_base,
            gtw_steam=gtw_steam,
            scalers=scalers,
            beta=beta,
            actual=actual,
            train_gtw=train_gtw,
        )
        if not hist_ok(top, hist0_top):
            continue
        if best_m is None or better(m, best_m):
            best = (delta, m, team, top, hhi)
            best_m = m
    return best


def pick_fv(current, gtw_base, gtw_steam, scalers, beta, actual, train_gtw, hist0_top):
    best = None
    best_m = None
    for gamma in (1.0, 2.0, 3.0, 4.0, 5.0, 6.0):
        m, team, top, hhi = score_config(
            steam=current["steam"],
            tau=current["tau"],
            third_delta=current["third_delta"],
            fv_gamma=gamma,
            safe_third=current["safe_third"],
            gtw_base=gtw_base,
            gtw_steam=gtw_steam,
            scalers=scalers,
            beta=beta,
            actual=actual,
            train_gtw=train_gtw,
        )
        if not hist_ok(top, hist0_top):
            continue
        if best_m is None or better(m, best_m):
            best = (gamma, m, team, top, hhi)
            best_m = m
    return best


def pick_safe_third(current, gtw_base, gtw_steam, scalers, beta, actual, train_gtw, hist0_top):
    best = None
    best_m = None
    for delta in (0.25, 0.35, 0.45, 0.50, 0.55, 0.60, 0.70):
        m, team, top, hhi = score_config(
            steam=current["steam"],
            tau=current["tau"],
            third_delta=current["third_delta"],
            fv_gamma=current["fv_gamma"],
            safe_third=delta,
            gtw_base=gtw_base,
            gtw_steam=gtw_steam,
            scalers=scalers,
            beta=beta,
            actual=actual,
            train_gtw=train_gtw,
        )
        if not hist_ok(top, hist0_top):
            continue
        if best_m is None or better(m, best_m):
            best = (delta, m, team, top, hhi)
            best_m = m
    return best


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    actual = load_actual_shares()
    train_gtw, scalers, beta, tau_ll = load_fit_bundle()
    posted = load_posted_spreads()
    print("building 2026 gtw (baseline spreads)...", flush=True)
    gtw_base = build_2026_gtw(posted)
    print("building 2026 gtw (PIT -6 steam)...", flush=True)
    gtw_steam = build_2026_gtw(apply_pit_steam(posted, -6.0))

    current = {
        "steam": False,
        "tau": tau_ll,
        "third_delta": 0.0,
        "fv_gamma": 0.0,
        "safe_third": 0.0,
    }
    rounds: list[Round] = []

    m0, t0, top0, hhi0 = score_config(
        steam=False,
        tau=tau_ll,
        third_delta=0.0,
        fv_gamma=0.0,
        safe_third=0.0,
        gtw_base=gtw_base,
        gtw_steam=gtw_steam,
        scalers=scalers,
        beta=beta,
        actual=actual,
        train_gtw=train_gtw,
    )
    write_csv(0, m0, actual)
    rounds.append(
        Round(
            iter_id=0,
            title="baseline parent clogit",
            change="Parent deployable clogit, Sep 9 DK week-1 spreads, tau from likelihood fit "
            f"({tau_ll:.3f}). No extra levers.",
            why="Need a honest Week 1 score before changing anything.",
            keep=True,
            next_step="Move PIT to about -6 (Tua steam) and re-score.",
            learned=(
                f"Top two are already near (JAC {100 * m0.shares['JAC']:.1f}% vs 32.5, "
                f"LAC {100 * m0.shares['LAC']:.1f}% vs 30.3). "
                f"PIT is the miss ({100 * m0.shares['PIT']:.1f}% vs 16.1) and DET is too high "
                f"({100 * m0.shares['DET']:.1f}% vs 7.1). Order is {m0.top3[0]}/{m0.top3[1]}/{m0.top3[2]}."
            ),
            metrics=m0,
            hist_team=t0,
            hist_top=top0,
            hist_hhi=hhi0,
            steam=False,
            tau=tau_ll,
            third_delta=0.0,
            fv_gamma=0.0,
            safe_third=0.0,
        )
    )
    best_m = m0
    print(f"iter 0 close={m0.close} top3={m0.top3} PIT={m0.shares['PIT']:.4f}", flush=True)

    # Iter 1 steam
    m1, t1, top1, hhi1 = score_config(
        steam=True,
        tau=current["tau"],
        third_delta=0.0,
        fv_gamma=0.0,
        safe_third=0.0,
        gtw_base=gtw_base,
        gtw_steam=gtw_steam,
        scalers=scalers,
        beta=beta,
        actual=actual,
        train_gtw=train_gtw,
    )
    keep1 = better(m1, best_m) and hist_ok(top1, top0)
    write_csv(1, m1, actual)
    if keep1:
        current["steam"] = True
        best_m = m1
        learned = (
            f"Steam helped. PIT {100 * m0.shares['PIT']:.1f}% → {100 * m1.shares['PIT']:.1f}% "
            f"(actual 16.1). Keep PIT at -6 going forward."
        )
        nxt = "Sharpen softmax with tau_hhi (likelihood tau stayed at 1)."
    else:
        learned = (
            f"Steam alone is not enough. PIT only {100 * m1.shares['PIT']:.1f}% vs 16.1 "
            f"(was {100 * m0.shares['PIT']:.1f}%). Line move does not create a 16% plank. Revert steam."
        )
        nxt = "Try tau_hhi on the baseline (no steam)."
    rounds.append(
        Round(
            iter_id=1,
            title="PIT line steam to -6",
            change="Rebuild week-1 features with ATL@PIT market line PIT -6.0 (Tua out / PoolGenius).",
            why="Iter 0 PIT residual (~2% vs 16%) was blamed on the stale -3.5 Sep 9 line.",
            keep=keep1,
            next_step=nxt,
            learned=learned,
            metrics=m1,
            hist_team=t1,
            hist_top=top1,
            hist_hhi=hhi1,
            steam=True,
            tau=current["tau"],
            third_delta=0.0,
            fv_gamma=0.0,
            safe_third=0.0,
        )
    )
    print(f"iter 1 keep={keep1} PIT={m1.shares['PIT']:.4f}", flush=True)
    if best_m.close:
        write_report(rounds, actual)
        return

    # Iter 2 tau
    picked = pick_tau(
        current, gtw_base, gtw_steam, scalers, beta, actual, train_gtw, top0
    )
    if picked is None:
        m2, t2, top2, hhi2 = score_config(
            steam=current["steam"],
            tau=1.2,
            third_delta=current["third_delta"],
            fv_gamma=current["fv_gamma"],
            safe_third=current["safe_third"],
            gtw_base=gtw_base,
            gtw_steam=gtw_steam,
            scalers=scalers,
            beta=beta,
            actual=actual,
            train_gtw=train_gtw,
        )
        tau2 = 1.2
        keep2 = False
        learned = "Every tau>1 blew past the 2025 Week 1 top-share guardrail. Revert tau."
        nxt = "Third-chalk leftover bonus on the #3 implied team."
    else:
        tau2, m2, t2, top2, hhi2 = picked
        keep2 = better(m2, best_m)
        if keep2:
            current["tau"] = tau2
            best_m = m2
            learned = (
                f"tau={tau2:.2f} cut focus error. PIT {100 * m2.shares['PIT']:.1f}%, "
                f"DET {100 * m2.shares['DET']:.1f}%. 2025 W1 top share {100 * top2:.1f}% "
                f"(baseline {100 * top0:.1f}%)."
            )
            nxt = "If PIT still low, add a third-chalk leftover bonus."
        else:
            learned = (
                f"Best allowed tau={tau2:.2f} did not beat the kept model on JAC/LAC/PIT/DET. "
                f"PIT {100 * m2.shares['PIT']:.1f}%. Concentration is not the PIT story. Revert tau."
            )
            nxt = "Third-chalk leftover bonus (Steelers as the plug-nose third)."
    write_csv(2, m2, actual)
    rounds.append(
        Round(
            iter_id=2,
            title="tau_hhi grid",
            change=f"Scale utilities by tau in {{1.1,1.2,1.3,1.4}}; picked tau={tau2:.2f}.",
            why="Likelihood tau=1 under-herds historically. Iter 0/1 still too flat on the third team.",
            keep=keep2,
            next_step=nxt,
            learned=learned,
            metrics=m2,
            hist_team=t2,
            hist_top=top2,
            hist_hhi=hhi2,
            steam=current["steam"] if keep2 else current["steam"],
            tau=tau2,
            third_delta=current["third_delta"],
            fv_gamma=current["fv_gamma"],
            safe_third=current["safe_third"],
        )
    )
    print(f"iter 2 keep={keep2} tau={tau2} PIT={m2.shares['PIT']:.4f}", flush=True)
    if best_m.close:
        write_report(rounds, actual)
        return

    # Iter 3 third chalk
    picked = pick_third(
        current, gtw_base, gtw_steam, scalers, beta, actual, train_gtw, top0
    )
    if picked is None:
        m3, t3, top3, hhi3 = score_config(
            steam=current["steam"],
            tau=current["tau"],
            third_delta=1.5,
            fv_gamma=current["fv_gamma"],
            safe_third=current["safe_third"],
            gtw_base=gtw_base,
            gtw_steam=gtw_steam,
            scalers=scalers,
            beta=beta,
            actual=actual,
            train_gtw=train_gtw,
        )
        d3 = 1.5
        keep3 = False
        learned = "Third-chalk grid failed the 2025 guardrail. Revert."
        nxt = "Future-value gap penalty to pull DET down."
    else:
        d3, m3, t3, top3, hhi3 = picked
        keep3 = better(m3, best_m)
        if keep3:
            current["third_delta"] = d3
            best_m = m3
            learned = (
                f"Leftover bonus {d3:.1f} on the third implied favorite moved PIT to "
                f"{100 * m3.shares['PIT']:.1f}% (actual 16.1). Order {m3.top3[0]}/{m3.top3[1]}/{m3.top3[2]}."
            )
            nxt = "If DET still high, penalize future_value_gap."
        else:
            learned = (
                f"Best leftover delta={d3:.1f} did not beat the kept model. "
                f"PIT {100 * m3.shares['PIT']:.1f}%. Revert third-chalk."
            )
            nxt = "Future-value gap penalty for DET/PHI holiday inventory."
    write_csv(3, m3, actual)
    rounds.append(
        Round(
            iter_id=3,
            title="third-chalk leftover",
            change=(
                "If two teams have implied win prob ≥ 0.75, add a logit bonus to the "
                f"#3 implied team. Grid 0.5–3.0; picked {d3:.1f}."
            ),
            why="YouTube: Steelers as the plug-nose third when JAC and LAC are both mega-chalk.",
            keep=keep3,
            next_step=nxt,
            learned=learned,
            metrics=m3,
            hist_team=t3,
            hist_top=top3,
            hist_hhi=hhi3,
            steam=current["steam"],
            tau=current["tau"],
            third_delta=d3,
            fv_gamma=current["fv_gamma"],
            safe_third=current["safe_third"],
        )
    )
    print(f"iter 3 keep={keep3} delta={d3} PIT={m3.shares['PIT']:.4f}", flush=True)
    if best_m.close:
        write_report(rounds, actual)
        return

    # Iter 4 FV gap
    picked = pick_fv(
        current, gtw_base, gtw_steam, scalers, beta, actual, train_gtw, top0
    )
    if picked is None:
        m4, t4, top4s, hhi4 = score_config(
            steam=current["steam"],
            tau=current["tau"],
            third_delta=current["third_delta"],
            fv_gamma=3.0,
            safe_third=current["safe_third"],
            gtw_base=gtw_base,
            gtw_steam=gtw_steam,
            scalers=scalers,
            beta=beta,
            actual=actual,
            train_gtw=train_gtw,
        )
        g4 = 3.0
        keep4 = False
        learned = "FV-gap grid failed the 2025 guardrail. Revert."
        nxt = "Stop unless close; do not invent a 2026-only intercept."
    else:
        g4, m4, t4, top4s, hhi4 = picked
        keep4 = better(m4, best_m)
        if keep4:
            current["fv_gamma"] = g4
            best_m = m4
            learned = (
                f"FV-gap gamma={g4:.1f} moved DET to {100 * m4.shares['DET']:.1f}% "
                f"(actual 7.1). PIT {100 * m4.shares['PIT']:.1f}%."
            )
            nxt = "If still not close, one more combined pass (iter 5) then stop."
        else:
            learned = (
                f"Best gamma={g4:.1f} did not beat the kept model on the four focus errors. "
                f"DET {100 * m4.shares['DET']:.1f}%. Revert FV-gap."
            )
            nxt = "Iter 5: keep the best combo; stop if no further gain."
    write_csv(4, m4, actual)
    rounds.append(
        Round(
            iter_id=4,
            title="future-value gap penalty",
            change=(
                "Subtract gamma * max(best_future_proj_win_prob - this_week_implied, 0) "
                f"from logits. Grid 1–6; picked {g4:.1f}."
            ),
            why="Crowd saved DET for Thanksgiving; model treated DET as a Week 1 favorite.",
            keep=keep4,
            next_step=nxt,
            learned=learned,
            metrics=m4,
            hist_team=t4,
            hist_top=top4s,
            hist_hhi=hhi4,
            steam=current["steam"],
            tau=current["tau"],
            third_delta=current["third_delta"],
            fv_gamma=g4,
            safe_third=current["safe_third"],
        )
    )
    print(f"iter 4 keep={keep4} gamma={g4} DET={m4.shares['DET']:.4f}", flush=True)
    if best_m.close:
        write_report(rounds, actual)
        return

    # Iter 5: leftover on plug-nose third, skipping smash-inventory saves (DET).
    picked = pick_safe_third(
        current, gtw_base, gtw_steam, scalers, beta, actual, train_gtw, top0
    )
    if picked is None:
        m5, t5, top5, hhi5 = score_config(
            steam=current["steam"],
            tau=current["tau"],
            third_delta=current["third_delta"],
            fv_gamma=current["fv_gamma"],
            safe_third=0.5,
            gtw_base=gtw_base,
            gtw_steam=gtw_steam,
            scalers=scalers,
            beta=beta,
            actual=actual,
            train_gtw=train_gtw,
        )
        d5 = 0.5
        keep5 = False
        learned = "Safe-third grid failed the 2025 guardrail. Revert."
        nxt = "If DET is still the leftover sink, raise the FV-gap penalty."
    else:
        d5, m5, t5, top5, hhi5 = picked
        keep5 = better(m5, best_m)
        if keep5:
            current["safe_third"] = d5
            best_m = m5
            learned = (
                f"Skip-inventory leftover {d5:.2f} went to a non-DET third. "
                f"Top3 {m5.top3[0]}/{m5.top3[1]}/{m5.top3[2]}. "
                f"PIT {100 * m5.shares['PIT']:.1f}% vs 16.1, DET {100 * m5.shares['DET']:.1f}% vs 7.1."
            )
            nxt = "If DET is still high, retune FV-gap with leftover kept. Do not retune PIT."
        else:
            learned = (
                f"Best safe-third delta={d5:.2f} did not beat the kept model. "
                f"PIT {100 * m5.shares['PIT']:.1f}%. Revert leftover."
            )
            nxt = "Stop unless close; do not add a 2026 team intercept."
    write_csv(5, m5, actual)
    rounds.append(
        Round(
            iter_id=5,
            title="safe-third leftover (skip smash inventory)",
            change=(
                "If two implied p ≥ 0.75, leftover bonus goes to the next implied team "
                f"with fewer than 3 remaining weeks projected favored by 7. Grid; picked {d5:.2f}."
            ),
            why="Iter 3 leftover hit DET (implied #3). YouTube plug-nose third is PIT, not Thanksgiving DET.",
            keep=keep5,
            next_step=nxt,
            learned=learned,
            metrics=m5,
            hist_team=t5,
            hist_top=top5,
            hist_hhi=hhi5,
            steam=current["steam"],
            tau=current["tau"],
            third_delta=current["third_delta"],
            fv_gamma=current["fv_gamma"],
            safe_third=d5,
        )
    )
    print(f"iter 5 keep={keep5} safe_third={d5} PIT={m5.shares['PIT']:.4f} close={m5.close}", flush=True)
    if best_m.close:
        write_report(rounds, actual)
        from week2 import write_week2
        write_week2(gtw_steam, scalers, beta, current)
        return

    # Iter 6: retune FV-gap with leftover kept (DET still high, PIT already moved).
    picked = pick_fv(
        current, gtw_base, gtw_steam, scalers, beta, actual, train_gtw, top0
    )
    if picked is None:
        m6, t6, top6, hhi6 = score_config(
            steam=current["steam"],
            tau=current["tau"],
            third_delta=current["third_delta"],
            fv_gamma=current["fv_gamma"],
            safe_third=current["safe_third"],
            gtw_base=gtw_base,
            gtw_steam=gtw_steam,
            scalers=scalers,
            beta=beta,
            actual=actual,
            train_gtw=train_gtw,
        )
        g6 = current["fv_gamma"]
        keep6 = False
        learned = "FV retune failed the 2025 guardrail. Revert."
        nxt = "Stop. Leave the last miss in this report."
    else:
        g6, m6, t6, top6, hhi6 = picked
        keep6 = better(m6, best_m)
        if keep6:
            current["fv_gamma"] = g6
            best_m = m6
            learned = (
                f"FV-gap retune gamma={g6:.1f} with leftover {current['safe_third']:.2f}. "
                f"DET {100 * m6.shares['DET']:.1f}%, PIT {100 * m6.shares['PIT']:.1f}%. Close={m6.close}."
            )
            nxt = "Week 2 live-book projection if close; otherwise stop."
        else:
            learned = (
                f"Best gamma={g6:.1f} with leftover did not beat the kept model. "
                f"DET {100 * m6.shares['DET']:.1f}%. Revert the retune."
            )
            nxt = "Stop. Leave the last miss in this report."
    write_csv(6, m6, actual)
    rounds.append(
        Round(
            iter_id=6,
            title="FV-gap retune with leftover kept",
            change=(
                "Re-grid future-value gap penalty 1–6 after leftover skip-inventory is on. "
                f"Picked gamma={g6:.1f}."
            ),
            why="PIT is the leftover plank; DET is still too high. Do not add more PIT bonus.",
            keep=keep6,
            next_step=nxt,
            learned=learned,
            metrics=m6,
            hist_team=t6,
            hist_top=top6,
            hist_hhi=hhi6,
            steam=current["steam"],
            tau=current["tau"],
            third_delta=current["third_delta"],
            fv_gamma=g6,
            safe_third=current["safe_third"],
        )
    )
    print(f"iter 6 keep={keep6} gamma={g6} DET={m6.shares['DET']:.4f} close={m6.close}", flush=True)
    write_report(rounds, actual)
    if best_m.close:
        from week2 import write_week2
        write_week2(gtw_steam, scalers, beta, current)


if __name__ == "__main__":
    main()
