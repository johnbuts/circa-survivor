# Week 1 crowd-model iterations

## Latest

- 2026-09-15 — **iter 6: FV-gap retune with leftover kept** (CLOSE).
- Top 3 `JAC/LAC/PIT`. PIT 15.5% vs 16.1% actual. DET 10.0% vs 7.1%.
- See iter 6 below for the table.

## Isolation

All writes are under `model_crafting/Week2_v2/`. Parent `model/`, `data/`, and pick HTML are read-only.

## Close rule

Top 3 JAC, LAC, PIT; JAC/LAC ≤ 3pp; PIT ≤ 5pp; DET ≤ 3pp; top-5 MAE ≤ 3pp; top-3 sum within 5pp of 78.9%.

## Iteration log
### Iter 6 — FV-gap retune with leftover kept

- Date: 2026-09-15
- Change: Re-grid future-value gap penalty 1–6 after leftover skip-inventory is on. Picked gamma=4.0.
- Why: PIT is the leftover plank; DET is still too high. Do not add more PIT bonus.
- Verdict: **KEEP**
- Close: **yes**
- Next: Week 2 live-book projection if close; otherwise stop.

| team | pred % | actual % | err pp | implied |
| --- | ---: | ---: | ---: | ---: |
| JAC | 35.51 | 32.51 | +3.00 | 77.4 |
| LAC | 29.04 | 30.34 | -1.30 | 79.8 |
| PIT | 15.50 | 16.05 | -0.55 | 70.4 |
| DET | 10.04 | 7.08 | +2.96 | 73.4 |
| LV | 3.05 | 5.23 | -2.19 | 60.7 |
| PHI | 3.16 | 3.14 | +0.02 | 68.9 |
| other | 3.71 | 5.64 | -1.93 | — |

- Top 3: `JAC / LAC / PIT` (need JAC / LAC / PIT)
- Top-3 sum: 80.0% (actual 78.9%)
- Top-5 MAE: 2.00 pp (need ≤ 3)
- JAC/LAC/PIT/DET abs err: 3.00 / 1.30 / 0.55 / 2.96 pp
- Predicted HHI: 0.247 (actual ~0.23)
- 2025 Week 1 sanity: top `DEN` 38.4%, HHI 0.213
- Knobs: steam=True, tau=1.000, third_delta=0.00, fv_gamma=4.00, safe_third=0.45

FV-gap retune gamma=4.0 with leftover 0.45. DET 10.0%, PIT 15.5%. Close=True.

### Iter 5 — safe-third leftover (skip smash inventory)

- Date: 2026-09-15
- Change: If two implied p ≥ 0.75, leftover bonus goes to the next implied team with fewer than 3 remaining weeks projected favored by 7. Grid; picked 0.45.
- Why: Iter 3 leftover hit DET (implied #3). YouTube plug-nose third is PIT, not Thanksgiving DET.
- Verdict: **KEEP**
- Close: **no**
- Next: If DET is still high, retune FV-gap with leftover kept. Do not retune PIT.

| team | pred % | actual % | err pp | implied |
| --- | ---: | ---: | ---: | ---: |
| JAC | 31.91 | 32.51 | -0.60 | 77.4 |
| LAC | 27.22 | 30.34 | -3.12 | 79.8 |
| PIT | 15.80 | 16.05 | -0.26 | 70.4 |
| DET | 11.70 | 7.08 | +4.62 | 73.4 |
| LV | 2.74 | 5.23 | -2.49 | 60.7 |
| PHI | 4.23 | 3.14 | +1.10 | 68.9 |
| other | 6.40 | 5.64 | +0.75 | — |

- Top 3: `JAC / LAC / PIT` (need JAC / LAC / PIT)
- Top-3 sum: 74.9% (actual 78.9%)
- Top-5 MAE: 2.22 pp (need ≤ 3)
- JAC/LAC/PIT/DET abs err: 0.60 / 3.12 / 0.26 / 4.62 pp
- Predicted HHI: 0.218 (actual ~0.23)
- 2025 Week 1 sanity: top `DEN` 38.4%, HHI 0.213
- Knobs: steam=True, tau=1.000, third_delta=0.00, fv_gamma=1.00, safe_third=0.45

Skip-inventory leftover 0.45 went to a non-DET third. Top3 JAC/LAC/PIT. PIT 15.8% vs 16.1, DET 11.7% vs 7.1.

### Iter 4 — future-value gap penalty

- Date: 2026-09-15
- Change: Subtract gamma * max(best_future_proj_win_prob - this_week_implied, 0) from logits. Grid 1–6; picked 1.0.
- Why: Crowd saved DET for Thanksgiving; model treated DET as a Week 1 favorite.
- Verdict: **KEEP**
- Close: **no**
- Next: If still not close, one more combined pass (iter 5) then stop.

| team | pred % | actual % | err pp | implied |
| --- | ---: | ---: | ---: | ---: |
| JAC | 33.85 | 32.51 | +1.34 | 77.4 |
| LAC | 28.87 | 30.34 | -1.47 | 79.8 |
| PIT | 10.68 | 16.05 | -5.37 | 70.4 |
| DET | 12.41 | 7.08 | +5.33 | 73.4 |
| LV | 2.90 | 5.23 | -2.33 | 60.7 |
| PHI | 4.49 | 3.14 | +1.35 | 68.9 |
| other | 6.79 | 5.64 | +1.14 | — |

- Top 3: `JAC / LAC / DET` (need JAC / LAC / PIT)
- Top-3 sum: 75.1% (actual 78.9%)
- Top-5 MAE: 3.17 pp (need ≤ 3)
- JAC/LAC/PIT/DET abs err: 1.34 / 1.47 / 5.37 / 5.33 pp
- Predicted HHI: 0.228 (actual ~0.23)
- 2025 Week 1 sanity: top `DEN` 38.4%, HHI 0.213
- Knobs: steam=True, tau=1.000, third_delta=0.00, fv_gamma=1.00, safe_third=0.00

FV-gap gamma=1.0 moved DET to 12.4% (actual 7.1). PIT 10.7%.

### Iter 3 — third-chalk leftover

- Date: 2026-09-15
- Change: If two teams have implied win prob ≥ 0.75, add a logit bonus to the #3 implied team. Grid 0.5–3.0; picked 0.5.
- Why: YouTube: Steelers as the plug-nose third when JAC and LAC are both mega-chalk.
- Verdict: **REVERT**
- Close: **no**
- Next: Future-value gap penalty for DET/PHI holiday inventory.

| team | pred % | actual % | err pp | implied |
| --- | ---: | ---: | ---: | ---: |
| JAC | 29.92 | 32.51 | -2.59 | 77.4 |
| LAC | 25.89 | 30.34 | -4.46 | 79.8 |
| PIT | 9.85 | 16.05 | -6.20 | 70.4 |
| DET | 19.73 | 7.08 | +12.65 | 73.4 |
| LV | 2.57 | 5.23 | -2.67 | 60.7 |
| PHI | 4.53 | 3.14 | +1.40 | 68.9 |
| other | 7.51 | 5.64 | +1.87 | — |

- Top 3: `JAC / LAC / DET` (need JAC / LAC / PIT)
- Top-3 sum: 75.5% (actual 78.9%)
- Top-5 MAE: 5.71 pp (need ≤ 3)
- JAC/LAC/PIT/DET abs err: 2.59 / 4.46 / 6.20 / 12.65 pp
- Predicted HHI: 0.209 (actual ~0.23)
- 2025 Week 1 sanity: top `DEN` 38.4%, HHI 0.213
- Knobs: steam=True, tau=1.000, third_delta=0.50, fv_gamma=0.00, safe_third=0.00

Best leftover delta=0.5 did not beat the kept model. PIT 9.8%. Revert third-chalk.

### Iter 2 — tau_hhi grid

- Date: 2026-09-15
- Change: Scale utilities by tau in {1.1,1.2,1.3,1.4}; picked tau=1.10.
- Why: Likelihood tau=1 under-herds historically. Iter 0/1 still too flat on the third team.
- Verdict: **REVERT**
- Close: **no**
- Next: Third-chalk leftover bonus (Steelers as the plug-nose third).

| team | pred % | actual % | err pp | implied |
| --- | ---: | ---: | ---: | ---: |
| JAC | 34.70 | 32.51 | +2.20 | 77.4 |
| LAC | 29.59 | 30.34 | -0.75 | 79.8 |
| PIT | 10.22 | 16.05 | -5.83 | 70.4 |
| DET | 12.66 | 7.08 | +5.58 | 73.4 |
| LV | 2.33 | 5.23 | -2.90 | 60.7 |
| PHI | 4.35 | 3.14 | +1.22 | 68.9 |
| other | 6.13 | 5.64 | +0.49 | — |

- Top 3: `JAC / LAC / DET` (need JAC / LAC / PIT)
- Top-3 sum: 77.0% (actual 78.9%)
- Top-5 MAE: 3.45 pp (need ≤ 3)
- JAC/LAC/PIT/DET abs err: 2.20 / 0.75 / 5.83 / 5.58 pp
- Predicted HHI: 0.237 (actual ~0.23)
- 2025 Week 1 sanity: top `DEN` 42.0%, HHI 0.239
- Knobs: steam=True, tau=1.100, third_delta=0.00, fv_gamma=0.00, safe_third=0.00

Best allowed tau=1.10 did not beat the kept model on JAC/LAC/PIT/DET. PIT 10.2%. Concentration is not the PIT story. Revert tau.

### Iter 1 — PIT line steam to -6

- Date: 2026-09-15
- Change: Rebuild week-1 features with ATL@PIT market line PIT -6.0 (Tua out / PoolGenius).
- Why: Iter 0 PIT residual (~2% vs 16%) was blamed on the stale -3.5 Sep 9 line.
- Verdict: **KEEP**
- Close: **no**
- Next: Sharpen softmax with tau_hhi (likelihood tau stayed at 1).

| team | pred % | actual % | err pp | implied |
| --- | ---: | ---: | ---: | ---: |
| JAC | 32.44 | 32.51 | -0.07 | 77.4 |
| LAC | 28.06 | 30.34 | -2.28 | 79.8 |
| PIT | 10.68 | 16.05 | -5.37 | 70.4 |
| DET | 12.97 | 7.08 | +5.89 | 73.4 |
| LV | 2.78 | 5.23 | -2.45 | 60.7 |
| PHI | 4.92 | 3.14 | +1.78 | 68.9 |
| other | 8.15 | 5.64 | +2.50 | — |

- Top 3: `JAC / LAC / DET` (need JAC / LAC / PIT)
- Top-3 sum: 73.5% (actual 78.9%)
- Top-5 MAE: 3.21 pp (need ≤ 3)
- JAC/LAC/PIT/DET abs err: 0.07 / 2.28 / 5.37 / 5.89 pp
- Predicted HHI: 0.216 (actual ~0.23)
- 2025 Week 1 sanity: top `DEN` 38.4%, HHI 0.213
- Knobs: steam=True, tau=1.000, third_delta=0.00, fv_gamma=0.00, safe_third=0.00

Steam helped. PIT 2.4% → 10.7% (actual 16.1). Keep PIT at -6 going forward.

### Iter 0 — baseline parent clogit

- Date: 2026-09-15
- Change: Parent deployable clogit, Sep 9 DK week-1 spreads, tau from likelihood fit (1.000). No extra levers.
- Why: Need a honest Week 1 score before changing anything.
- Verdict: **KEEP**
- Close: **no**
- Next: Move PIT to about -6 (Tua steam) and re-score.

| team | pred % | actual % | err pp | implied |
| --- | ---: | ---: | ---: | ---: |
| JAC | 35.44 | 32.51 | +2.93 | 77.4 |
| LAC | 30.66 | 30.34 | +0.32 | 79.8 |
| PIT | 2.41 | 16.05 | -13.64 | 62.4 |
| DET | 14.17 | 7.08 | +7.09 | 73.4 |
| LV | 3.04 | 5.23 | -2.19 | 60.7 |
| PHI | 5.37 | 3.14 | +2.23 | 68.9 |
| other | 8.90 | 5.64 | +3.26 | — |

- Top 3: `JAC / LAC / DET` (need JAC / LAC / PIT)
- Top-3 sum: 80.3% (actual 78.9%)
- Top-5 MAE: 5.23 pp (need ≤ 3)
- JAC/LAC/PIT/DET abs err: 2.93 / 0.32 / 13.64 / 7.09 pp
- Predicted HHI: 0.245 (actual ~0.23)
- 2025 Week 1 sanity: top `DEN` 38.4%, HHI 0.213
- Knobs: steam=False, tau=1.000, third_delta=0.00, fv_gamma=0.00, safe_third=0.00

Top two are already near (JAC 35.4% vs 32.5, LAC 30.7% vs 30.3). PIT is the miss (2.4% vs 16.1) and DET is too high (14.2% vs 7.1). Order is JAC/LAC/DET.

## Week 2 (8 live tickets)

See `out/week2_book.md`. Field-conditioned top: SF 30.5%, TB 29.2%, BAL 10.6%.
