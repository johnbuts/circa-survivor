# Models we use

Labeled on the site at `models.html`. Each row is a different object. Do not mix them.

## 1. Field-conditioned clogit — crowd

**What it predicts:** how Circa entries split their picks this week.

**Not:** who wins the NFL game.

Production spec is `DEPLOYABLE_SPEC` in `model_crafting`. Week 1 close was **iter 6** (skip-inventory leftover, FV-gap γ=4, steam). Week 2 freeze is **Week2_v2** with those knobs held. Field-conditioning uses who is still alive and which teams those tickets already burned.

- Week 1: JAC 35.5 / LAC 29.0 / PIT 15.5 vs Circa PDF 32.51 / 30.34 / 16.05.
- Week 2: SF 30.5 / TB 29.2 / BAL 10.6 vs Circa 39.7 / 35.7 / 4.9. Model had the chalk pair, not the height.
- Weeks 3–5: not re-fit. The model code imports `model_crafting/`, which is not in this repo, so the weekly stand-in (section 4) carries the crowd.

## 2. Market implied win probability

**What it predicts:** P(team wins), from DraftKings moneylines, vig-free.

Chip board, leverage, and “favorite holds” all use this. Spread sigmoid `P = sigmoid(b · −spread)` with `b ≈ 0.1448` is the same idea when we only have a line.

## 3. Circa official PDF — actual crowd

**What it is:** the real pick counts Circa posts.

Week 1: 24,999 tickets (board) / 25,017 start, JAC 32.51 / LAC 30.34 / PIT 16.05.

Week 2: 16,978 live in, **8,464** live out. SF 6,741 · TB 6,061 · LAC 1,357 · BAL 835. PHI ~910 (Circa: “more than 900”). Pot still **$25,017,000**.

Entering Week 3 the official count was **8,610** (Circa X), not 8,464 — that earlier number left out the 146 MNF Rams tickets.

Week 3 (8,607 picks): KC 4,398 (51.1%) W · SEA 1,111 L · DET 743 W · SF 591 W · GB 497 L · BUF 431 W · NO 405 L. **6,292** live out.

Week 4 (6,291 picks): MIN 2,733 (43.4%) W · BAL 2,449 (38.9%) W · SEA 442 W · BUF 178 L · IND 161 W. **5,972** live out.

Week 5: Circa posted a **team availability** sheet (live tickets that have not used each team). The Week 5 selections PDF is not out yet.

## 4. Public pick %, Circa-scaled — weekly stand-in

**What it is:** generic-survivor popularity (PoolGenius 2026-09-22: KC 41 / GB 13 / DET 10 / SF 9 / SEA 9 / BUF 7), then scaled by who in the Circa live field can still pick that team.

About **80%** of the 8,464 live tickets already used SF, so Circa-scaled SF is ~2%, not 9%. KC is the Week 3 soak (~43.5%). Replace this the day the Circa Week 3 PDF posts.

**Week 5:** ½ PoolGenius (6 Oct: DAL 33 / CIN 22 / HOU 19 / DET 9 / NE 6) + ½ SurvivorGrid (7 Oct), times Circa’s own Week 5 availability. Result: **DAL 40.7 / CIN 25.0 / HOU 16.7 / DET 5.0 / NE 4.0**. Built by `Weekly_models/Week5/crowd.py`. A Week 4 backtest of the same method landed BAL 38.6 vs 38.9 actual and MIN 38.5 vs 43.4.

## 5. Media consensus ranks

Sep 9 and Sep 15 1–32 averages. Input to future-value talk, not a pick model.

## Chip

`chip = $25,017,000 / field still alive`. Entering Week 5 that is **$4,189** (5,972 live). Week 5 expected chip at implied survival is ~$5,670.
