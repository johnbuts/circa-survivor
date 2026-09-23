# Models we use

Labeled on the site at `models.html`. Each row is a different object. Do not mix them.

## 1. Field-conditioned clogit — crowd

**What it predicts:** how Circa entries split their picks this week.

**Not:** who wins the NFL game.

Production spec is `DEPLOYABLE_SPEC` in `model_crafting`. Week 1 close was **iter 6** (skip-inventory leftover, FV-gap γ=4, steam). Week 2 freeze is **Week2_v2** with those knobs held. Field-conditioning uses who is still alive and which teams those tickets already burned.

- Week 1: JAC 35.5 / LAC 29.0 / PIT 15.5 vs Circa PDF 32.51 / 30.34 / 16.05.
- Week 2: SF 30.5 / TB 29.2 / BAL 10.6 vs Circa 39.7 / 35.7 / 4.9. Model had the chalk pair, not the height.

## 2. Market implied win probability

**What it predicts:** P(team wins), from DraftKings moneylines, vig-free.

Chip board, leverage, and “favorite holds” all use this. Spread sigmoid `P = sigmoid(b · −spread)` with `b ≈ 0.1448` is the same idea when we only have a line.

## 3. Circa official PDF — actual crowd

**What it is:** the real pick counts Circa posts.

Week 1: 24,999 tickets (board) / 25,017 start, JAC 32.51 / LAC 30.34 / PIT 16.05.

Week 2: 16,978 live in, **8,464** live out. SF 6,741 · TB 6,061 · LAC 1,357 · BAL 835. PHI ~910 (Circa: “more than 900”). Pot still **$25,017,000**.

Week 3 PDF is not public yet.

## 4. PoolGenius public, Circa-scaled — Week 3 stand-in

**What it is:** generic-survivor popularity (PoolGenius 2026-09-22: KC 41 / GB 13 / DET 10 / SF 9 / SEA 9 / BUF 7), then scaled by who in the Circa live field can still pick that team.

About **80%** of the 8,464 live tickets already used SF, so Circa-scaled SF is ~2%, not 9%. KC is the Week 3 soak (~43.5%). Replace this the day the Circa Week 3 PDF posts.

## 5. Media consensus ranks

Sep 9 and Sep 15 1–32 averages. Input to future-value talk, not a pick model.

## Chip

`chip = $25,017,000 / field still alive`. Entering Week 3 that is about **$2,956** if the rest of the field also survives.
