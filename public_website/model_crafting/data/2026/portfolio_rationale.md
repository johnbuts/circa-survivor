# Portfolio rationale — 10 entries, 20 contest weeks

## Portfolio objective

Maximise **P(at least one entry reaches a paying position)** — not the sum of ten individual expected values. Two identical entries always die in the same week; the second contributes **zero** to that objective while costing a full entry fee. Ten entries collapsing to two distinct paths is roughly two entries bought at five times the price.

**Concentration within a week is intentional** (six entries on the same Thanksgiving underdog when leverage is clear). **Identical season paths are a defect** — the portfolio should branch like a tree, not run as parallel lines.

## Allocation rule

1. **Within-week: concentrate** on highest leverage when clearly best.
2. **Per-week cap:** ≤ **6** entries on any team.
3. **Close band:** **0.3** log-nats for near-equivalent plays.
4. **Path distinctness:** all 10 sequences must differ; pairwise overlap ≤ **12** of 20 picks (60%).
5. **Sequential build** with path-overlap penalty `0.4 × overlap` when matching an earlier entry's week pick and paths already share picks — zero penalty when paths have not yet converged.
6. **Thanksgiving:** concentrate on best 1–2 underdog leverage plays.

## Pairwise path overlap matrix

Shared picks out of 20 (cap **≤ 12**).

| | entry_01 | entry_02 | entry_03 | entry_04 | entry_05 | entry_06 | entry_07 | entry_08 | entry_09 | entry_10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| entry_01 | 0 | 2 | 4 | 4 | 3 | 3 | 4 | 6 | 4 | 3 |
| entry_02 | 2 | 0 | 3 | 3 | 3 | 4 | 3 | 4 | 4 | 5 |
| entry_03 | 4 | 3 | 0 | 3 | 2 | 2 | 1 | 2 | 3 | 3 |
| entry_04 | 4 | 3 | 3 | 0 | 4 | 3 | 3 | 2 | 2 | 3 |
| entry_05 | 3 | 3 | 2 | 4 | 0 | 2 | 2 | 4 | 2 | 2 |
| entry_06 | 3 | 4 | 2 | 3 | 2 | 0 | 2 | 2 | 2 | 3 |
| entry_07 | 4 | 3 | 1 | 3 | 2 | 2 | 0 | 2 | 3 | 3 |
| entry_08 | 6 | 4 | 2 | 2 | 4 | 2 | 2 | 0 | 3 | 2 |
| entry_09 | 4 | 4 | 3 | 2 | 2 | 2 | 3 | 3 | 0 | 1 |
| entry_10 | 3 | 5 | 3 | 3 | 2 | 3 | 3 | 2 | 1 | 0 |

Maximum pairwise overlap: **6** (cap 12).

## Week 1 scoring verification

Survival floor: `implied_win_prob >= 0.6`. `CROWD_FLOOR = 0.01` (1%). `LAMBDA = 0.7`.

Top teams by leverage score (eligible set with floor applied):

| rank | team | leverage_score | win_prob | crowd | entries | selected |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | LAR | 2.752 | 0.624 | 0.010 | 6 | yes |
| 2 | DAL | 2.724 | 0.607 | 0.010 | 2 | yes |
| 3 | KC | 2.724 | 0.607 | 0.010 | 2 | yes |
| 4 | CHI | 2.541 | 0.607 | 0.013 | 0 | no |
| 5 | BAL | 2.423 | 0.624 | 0.016 | 0 | no |
| 6 | CIN | 2.303 | 0.624 | 0.019 | 0 | no |
| 7 | PIT | 2.139 | 0.624 | 0.024 | 0 | no |
| 8 | LV | 1.955 | 0.607 | 0.030 | 0 | no |
| 9 | PHI | 1.671 | 0.689 | 0.054 | 0 | no |
| 10 | DET | 1.057 | 0.734 | 0.142 | 0 | no |

LAC (40.7% projected crowd): **0** entries — must be 0.

Selected teams and win probs:

- **LAR** ×6: win_prob **0.624**
- **DAL** ×2: win_prob **0.607**
- **KC** ×2: win_prob **0.607**

## Win-probability verification (full portfolio)

**Minimum win prob** across 200 picks: **0.424** (entry_09, week Th, CHI).

Floor for that week: **0.4**.

### Mean win probability per contest week (10 entries)

| week | mean_win_prob | floor |
| --- | --- | --- |
| 1 | 0.617 | 0.6 |
| 2 | 0.649 | 0.6 |
| 3 | 0.617 | 0.6 |
| 4 | 0.654 | 0.6 |
| 5 | 0.639 | 0.6 |
| 6 | 0.672 | 0.6 |
| 7 | 0.652 | 0.6 |
| 8 | 0.639 | 0.6 |
| 9 | 0.664 | 0.6 |
| 10 | 0.637 | 0.6 |
| 11 | 0.689 | 0.6 |
| Th | 0.505 | 0.4 |
| 12 | 0.625 | 0.55 |
| 13 | 0.609 | 0.55 |
| 14 | 0.644 | 0.55 |
| 15 | 0.602 | 0.55 |
| Ch | 0.511 | 0.4 |
| 16 | 0.655 | 0.55 |
| 17 | 0.624 | 0.55 |
| 18 | 0.696 | 0.55 |

## Holiday overlap (Th ∩ Ch)

- Th teams: `['BUF', 'CHI', 'DAL', 'DEN', 'DET', 'GB', 'KC', 'LAR', 'PHI', 'PIT']`
- Ch teams: `['BUF', 'CHI', 'DEN', 'GB', 'HOU', 'LAR', 'PHI', 'SEA']`
- **Th ∩ Ch**: `['BUF', 'CHI', 'DEN', 'GB', 'LAR', 'PHI']`
- Th only: `['DAL', 'DET', 'KC', 'PIT']`
- Ch only: `['HOU', 'SEA']`

## Leverage score (state-dependent)

```
leverage_score(t) = log(implied_win_prob) - LAMBDA * log(crowd_share_clamped)
  crowd_share_clamped = max(projected_crowd_share, 0.01)
  + [Th|Ch underdog] UNDERDOG_DELTA * log(fav_crowd)
```

### Survival floors (hard filter before scoring)

| weeks | min `implied_win_prob` |
| --- | --- |
| 1–11 | **0.60** |
| Th, Ch | **0.40** |
| 12–18 (excl. legs) | **0.55** |

If no team clears the floor, build fails loudly.

| constant | value |
| --- | --- |
| `LAMBDA` | **0.7** — balances win prob vs crowd; avoids 1% crowd floor dominating |
| `CROWD_FLOOR` | **0.01** (1%) |
| `MAX_ENTRIES_PER_TEAM` | **6** |
| `PATH_OVERLAP_MAX` | **12** |

## Per-week leverage ranking and entry counts

#### Week 1 — allocation

Mode: **MIXED** — close threshold = **0.3** log-nats (≈ 135% leverage ratio).

| rank | team | leverage_score | win_prob | crowd | entries |
| --- | --- | --- | --- | --- | --- |
| 1 | LAR | 2.752✓ | 0.624 | 0.010 | 6 |
| 2 | DAL | 2.724✓ | 0.607 | 0.010 | 2 |
| 3 | KC | 2.724✓ | 0.607 | 0.010 | 2 |
| 4 | BUF | 2.633✓ | 0.554 | 0.010 | 0 |
| 5 | MIN | 2.633✓ | 0.554 | 0.010 | 0 |
| 6 | SEA | 2.633✓ | 0.554 | 0.010 | 0 |
| 7 | TEN | 2.633✓ | 0.554 | 0.010 | 0 |
| 8 | CHI | 2.541✓ | 0.607 | 0.013 | 0 |

Distribution: LAR×6, DAL×2, KC×2

#### Week 2 — allocation

Mode: **BRANCH** — close threshold = **0.3** log-nats (≈ 135% leverage ratio).

| rank | team | leverage_score | win_prob | crowd | entries |
| --- | --- | --- | --- | --- | --- |
| 1 | CHI | 2.761✓ | 0.630 | 0.010 | 4 |
| 2 | BUF | 2.710✓ | 0.599 | 0.010 | 0 |
| 3 | DEN | 2.700✓ | 0.592 | 0.010 | 0 |
| 4 | ATL | 2.627✓ | 0.551 | 0.010 | 0 |
| 5 | HOU | 2.586✓ | 0.529 | 0.010 | 0 |
| 6 | CIN | 2.472✓ | 0.471 | 0.010 | 0 |
| 7 | NE | 2.428 | 0.654 | 0.017 | 4 |
| 8 | CAR | 2.424 | 0.449 | 0.010 | 0 |

Distribution: CHI×4, NE×4, DAL×1, PHI×1

#### Week 3 — allocation

Mode: **BRANCH** — close threshold = **0.3** log-nats (≈ 135% leverage ratio).

| rank | team | leverage_score | win_prob | crowd | entries |
| --- | --- | --- | --- | --- | --- |
| 1 | BAL | 2.713✓ | 0.600 | 0.010 | 0 |
| 2 | LAR | 2.701✓ | 0.593 | 0.010 | 0 |
| 3 | TB | 2.680✓ | 0.581 | 0.010 | 0 |
| 4 | HOU | 2.675✓ | 0.578 | 0.010 | 0 |
| 5 | BUF | 2.604✓ | 0.611 | 0.012 | 4 |
| 6 | NE | 2.598✓ | 0.535 | 0.010 | 0 |
| 7 | CIN | 2.587✓ | 0.529 | 0.010 | 0 |
| 8 | CHI | 2.545✓ | 0.507 | 0.010 | 0 |

Distribution: BUF×4, SEA×3, NYG×2, CAR×1

#### Week 4 — allocation

Mode: **BRANCH** — close threshold = **0.3** log-nats (≈ 135% leverage ratio).

| rank | team | leverage_score | win_prob | crowd | entries |
| --- | --- | --- | --- | --- | --- |
| 1 | SEA | 2.746✓ | 0.620 | 0.010 | 3 |
| 2 | BUF | 2.669✓ | 0.574 | 0.010 | 0 |
| 3 | DET | 2.664✓ | 0.571 | 0.010 | 0 |
| 4 | SF | 2.640✓ | 0.558 | 0.010 | 0 |
| 5 | CIN | 2.633✓ | 0.630 | 0.012 | 3 |
| 6 | HOU | 2.611✓ | 0.542 | 0.010 | 0 |
| 7 | LAR | 2.595✓ | 0.534 | 0.010 | 0 |
| 8 | WAS | 2.578✓ | 0.524 | 0.010 | 0 |

Distribution: CIN×3, SEA×3, KC×2, PIT×2

#### Week 5 — allocation

Mode: **BRANCH** — close threshold = **0.3** log-nats (≈ 135% leverage ratio).

| rank | team | leverage_score | win_prob | crowd | entries |
| --- | --- | --- | --- | --- | --- |
| 1 | WAS | 2.668✓ | 0.574 | 0.010 | 0 |
| 2 | LAC | 2.667✓ | 0.573 | 0.010 | 0 |
| 3 | GB | 2.647✓ | 0.562 | 0.010 | 0 |
| 4 | NYJ | 2.578✓ | 0.524 | 0.010 | 0 |
| 5 | PHI | 2.578✓ | 0.595 | 0.012 | 0 |
| 6 | MIN | 2.573✓ | 0.522 | 0.010 | 0 |
| 7 | NO | 2.486✓ | 0.478 | 0.010 | 0 |
| 8 | CLE | 2.481✓ | 0.476 | 0.010 | 0 |

Distribution: SEA×3, BAL×2, LAR×2, DAL×1, HOU×1, PIT×1

#### Week 6 — allocation

Mode: **BRANCH** — close threshold = **0.3** log-nats (≈ 135% leverage ratio).

| rank | team | leverage_score | win_prob | crowd | entries |
| --- | --- | --- | --- | --- | --- |
| 1 | KC | 2.712✓ | 0.600 | 0.010 | 0 |
| 2 | TB | 2.648✓ | 0.562 | 0.010 | 0 |
| 3 | CHI | 2.640✓ | 0.558 | 0.010 | 0 |
| 4 | HOU | 2.621✓ | 0.547 | 0.010 | 0 |
| 5 | GB | 2.620✓ | 0.547 | 0.010 | 0 |
| 6 | NYG | 2.616✓ | 0.582 | 0.011 | 0 |
| 7 | SEA | 2.581✓ | 0.526 | 0.010 | 0 |
| 8 | DEN | 2.478✓ | 0.474 | 0.010 | 0 |

Distribution: IND×4, SF×3, BAL×2, PHI×1

#### Week 7 — allocation

Mode: **BRANCH** — close threshold = **0.3** log-nats (≈ 135% leverage ratio).

| rank | team | leverage_score | win_prob | crowd | entries |
| --- | --- | --- | --- | --- | --- |
| 1 | SEA | 2.675✓ | 0.578 | 0.010 | 0 |
| 2 | DET | 2.663✓ | 0.571 | 0.010 | 0 |
| 3 | SF | 2.624✓ | 0.549 | 0.010 | 0 |
| 4 | PHI | 2.569✓ | 0.590 | 0.012 | 0 |
| 5 | CHI | 2.554✓ | 0.512 | 0.010 | 0 |
| 6 | TB | 2.531✓ | 0.500 | 0.010 | 0 |
| 7 | CAR | 2.530✓ | 0.500 | 0.010 | 0 |
| 8 | NE | 2.506✓ | 0.488 | 0.010 | 0 |

Distribution: BAL×3, MIN×3, HOU×1, LAR×1, NYJ×1, TEN×1

#### Week 8 — allocation

Mode: **BRANCH** — close threshold = **0.3** log-nats (≈ 135% leverage ratio).

| rank | team | leverage_score | win_prob | crowd | entries |
| --- | --- | --- | --- | --- | --- |
| 1 | DET | 2.790✓ | 0.648 | 0.010 | 2 |
| 2 | PHI | 2.717✓ | 0.602 | 0.010 | 1 |
| 3 | LAR | 2.657✓ | 0.682 | 0.013 | 1 |
| 4 | SEA | 2.628✓ | 0.626 | 0.012 | 1 |
| 5 | NYJ | 2.583✓ | 0.527 | 0.010 | 0 |
| 6 | KC | 2.539✓ | 0.504 | 0.010 | 0 |
| 7 | BUF | 2.537✓ | 0.503 | 0.010 | 0 |
| 8 | BAL | 2.524✓ | 0.497 | 0.010 | 0 |

Distribution: DET×2, JAC×2, TB×2, GB×1, LAR×1, PHI×1, SEA×1

#### Week 9 — allocation

Mode: **BRANCH** — close threshold = **0.3** log-nats (≈ 135% leverage ratio).

| rank | team | leverage_score | win_prob | crowd | entries |
| --- | --- | --- | --- | --- | --- |
| 1 | LAR | 2.779✓ | 0.685 | 0.011 | 0 |
| 2 | CHI | 2.724✓ | 0.607 | 0.010 | 3 |
| 3 | NE | 2.705✓ | 0.596 | 0.010 | 0 |
| 4 | DAL | 2.700✓ | 0.592 | 0.010 | 0 |
| 5 | BUF | 2.681✓ | 0.581 | 0.010 | 0 |
| 6 | CIN | 2.650✓ | 0.640 | 0.012 | 3 |
| 7 | LAC | 2.648✓ | 0.563 | 0.010 | 0 |
| 8 | DEN | 2.610✓ | 0.541 | 0.010 | 0 |

Distribution: CHI×3, CIN×3, BAL×1, DET×1, NO×1, PHI×1

#### Week 10 — allocation

Mode: **BRANCH** — close threshold = **0.3** log-nats (≈ 135% leverage ratio).

| rank | team | leverage_score | win_prob | crowd | entries |
| --- | --- | --- | --- | --- | --- |
| 1 | KC | 2.724✓ | 0.607 | 0.010 | 3 |
| 2 | CIN | 2.709✓ | 0.639 | 0.011 | 2 |
| 3 | JAC | 2.704✓ | 0.595 | 0.010 | 0 |
| 4 | DAL | 2.680✓ | 0.581 | 0.010 | 0 |
| 5 | NYG | 2.607✓ | 0.540 | 0.010 | 0 |
| 6 | NE | 2.580✓ | 0.525 | 0.010 | 0 |
| 7 | NO | 2.553✓ | 0.511 | 0.010 | 0 |
| 8 | GB | 2.533✓ | 0.635 | 0.014 | 3 |

Distribution: GB×3, KC×3, CIN×2, BAL×1, HOU×1

#### Week 11 — allocation

Mode: **BRANCH** — close threshold = **0.3** log-nats (≈ 135% leverage ratio).

| rank | team | leverage_score | win_prob | crowd | entries |
| --- | --- | --- | --- | --- | --- |
| 1 | DET | 2.755✓ | 0.626 | 0.010 | 2 |
| 2 | CIN | 2.682✓ | 0.582 | 0.010 | 0 |
| 3 | SF | 2.655✓ | 0.566 | 0.010 | 0 |
| 4 | JAC | 2.578✓ | 0.524 | 0.010 | 0 |
| 5 | BAL | 2.528✓ | 0.662 | 0.015 | 1 |
| 6 | NYG | 2.480✓ | 0.476 | 0.010 | 0 |
| 7 | MIN | 2.388 | 0.434 | 0.010 | 0 |
| 8 | WAS | 2.351 | 0.418 | 0.010 | 0 |

Distribution: DAL×2, DET×2, PHI×2, BAL×1, CHI×1, DEN×1, HOU×1

#### Week Th — allocation

Mode: **BRANCH** — close threshold = **0.3** log-nats (≈ 135% leverage ratio).

| rank | team | leverage_score | win_prob | crowd | entries |
| --- | --- | --- | --- | --- | --- |
| 1 | GB | 1.177✓ | 0.317 | 0.010 | 0 |
| 2 | KC | 1.123✓ | 0.431 | 0.020 | 1 |
| 3 | DAL | 1.085✓ | 0.522 | 0.084 | 1 |
| 4 | LAR | 1.015✓ | 0.683 | 0.136 | 0 |
| 5 | DET | 0.968✓ | 0.576 | 0.114 | 2 |
| 6 | PHI | 0.962✓ | 0.478 | 0.088 | 2 |
| 7 | BUF | 0.640 | 0.569 | 0.179 | 1 |
| 8 | CHI | 0.553 | 0.424 | 0.033 | 1 |

Distribution: DET×2, PHI×2, BUF×1, CHI×1, DAL×1, DEN×1, KC×1, PIT×1

#### Week 12 — allocation

Mode: **BRANCH** — close threshold = **0.3** log-nats (≈ 135% leverage ratio).

| rank | team | leverage_score | win_prob | crowd | entries |
| --- | --- | --- | --- | --- | --- |
| 1 | BAL | 2.642✓ | 0.559 | 0.010 | 0 |
| 2 | IND | 2.626✓ | 0.550 | 0.010 | 0 |
| 3 | SEA | 2.578✓ | 0.524 | 0.010 | 0 |
| 4 | LAC | 2.566✓ | 0.518 | 0.010 | 0 |
| 5 | NE | 2.493✓ | 0.482 | 0.010 | 0 |
| 6 | SF | 2.481✓ | 0.476 | 0.010 | 0 |
| 7 | NYJ | 2.474✓ | 0.537 | 0.012 | 0 |
| 8 | MIA | 2.454✓ | 0.463 | 0.010 | 0 |

Distribution: MIN×3, CLE×2, JAC×2, TB×2, CIN×1

#### Week 13 — allocation

Mode: **BRANCH** — close threshold = **0.3** log-nats (≈ 135% leverage ratio).

| rank | team | leverage_score | win_prob | crowd | entries |
| --- | --- | --- | --- | --- | --- |
| 1 | LAR | 2.781✓ | 0.643 | 0.010 | 0 |
| 2 | DET | 2.674✓ | 0.577 | 0.010 | 2 |
| 3 | SF | 2.647✓ | 0.562 | 0.010 | 3 |
| 4 | NE | 2.606✓ | 0.539 | 0.010 | 0 |
| 5 | LAC | 2.533✓ | 0.501 | 0.010 | 0 |
| 6 | HOU | 2.532✓ | 0.501 | 0.010 | 0 |
| 7 | PIT | 2.529✓ | 0.499 | 0.010 | 0 |
| 8 | TB | 2.528✓ | 0.499 | 0.010 | 0 |

Distribution: SF×3, DET×2, GB×2, CHI×1, DEN×1, MIN×1

#### Week 14 — allocation

Mode: **BRANCH** — close threshold = **0.3** log-nats (≈ 135% leverage ratio).

| rank | team | leverage_score | win_prob | crowd | entries |
| --- | --- | --- | --- | --- | --- |
| 1 | LAR | 2.698✓ | 0.591 | 0.010 | 0 |
| 2 | JAC | 2.656✓ | 0.567 | 0.010 | 1 |
| 3 | HOU | 2.634✓ | 0.554 | 0.010 | 2 |
| 4 | CIN | 2.598✓ | 0.535 | 0.010 | 0 |
| 5 | BUF | 2.532✓ | 0.501 | 0.010 | 0 |
| 6 | GB | 2.529✓ | 0.499 | 0.010 | 0 |
| 7 | KC | 2.458✓ | 0.465 | 0.010 | 0 |
| 8 | WAS | 2.415✓ | 0.446 | 0.010 | 0 |

Distribution: DEN×2, HOU×2, ATL×1, CAR×1, DET×1, JAC×1, LAC×1, NE×1

#### Week 15 — allocation

Mode: **BRANCH** — close threshold = **0.3** log-nats (≈ 135% leverage ratio).

| rank | team | leverage_score | win_prob | crowd | entries |
| --- | --- | --- | --- | --- | --- |
| 1 | DEN | 2.859✓ | 0.695 | 0.010 | 2 |
| 2 | LAR | 2.829✓ | 0.674 | 0.010 | 0 |
| 3 | BUF | 2.741✓ | 0.617 | 0.010 | 1 |
| 4 | BAL | 2.737✓ | 0.615 | 0.010 | 0 |
| 5 | HOU | 2.718✓ | 0.603 | 0.010 | 1 |
| 6 | CIN | 2.679✓ | 0.580 | 0.010 | 1 |
| 7 | LAC | 2.665✓ | 0.572 | 0.010 | 2 |
| 8 | KC | 2.647✓ | 0.562 | 0.010 | 1 |

Distribution: DEN×2, LAC×2, WAS×2, BUF×1, CIN×1, HOU×1, KC×1

#### Week Ch — allocation

Mode: **BRANCH** — close threshold = **0.3** log-nats (≈ 135% leverage ratio).

| rank | team | leverage_score | win_prob | crowd | entries |
| --- | --- | --- | --- | --- | --- |
| 1 | LAR | 1.970✓ | 0.511 | 0.023 | 0 |
| 2 | SEA | 0.932 | 0.489 | 0.095 | 0 |
| 3 | PHI | 0.853 | 0.605 | 0.144 | 2 |
| 4 | DEN | 0.740 | 0.483 | 0.041 | 3 |
| 5 | CHI | 0.617 | 0.552 | 0.177 | 0 |
| 6 | BUF | 0.536 | 0.517 | 0.181 | 3 |
| 7 | GB | 0.462 | 0.448 | 0.054 | 2 |
| 8 | HOU | -0.765 | 0.395 | 0.228 | 0 |

Distribution: BUF×3, DEN×3, GB×2, PHI×2

#### Week 16 — allocation *(LOW CONFIDENCE)*

Mode: **BRANCH** — close threshold = **0.3** log-nats (≈ 135% leverage ratio).

| rank | team | leverage_score | win_prob | crowd | entries |
| --- | --- | --- | --- | --- | --- |
| 1 | DAL | 2.741✓ | 0.617 | 0.010 | 2 |
| 2 | KC | 2.737✓ | 0.615 | 0.010 | 1 |
| 3 | CIN | 2.722✓ | 0.605 | 0.010 | 0 |
| 4 | TEN | 2.562✓ | 0.516 | 0.010 | 0 |
| 5 | TB | 2.544✓ | 0.507 | 0.010 | 0 |
| 6 | ATL | 2.517✓ | 0.493 | 0.010 | 0 |
| 7 | LV | 2.497✓ | 0.484 | 0.010 | 0 |
| 8 | MIN | 2.462✓ | 0.591 | 0.014 | 3 |

Distribution: MIN×3, DAL×2, NE×2, KC×1, LAC×1, PIT×1

#### Week 17 — allocation *(LOW CONFIDENCE)*

Mode: **BRANCH** — close threshold = **0.3** log-nats (≈ 135% leverage ratio).

| rank | team | leverage_score | win_prob | crowd | entries |
| --- | --- | --- | --- | --- | --- |
| 1 | LAR | 2.764✓ | 0.632 | 0.010 | 0 |
| 2 | GB | 2.646✓ | 0.561 | 0.010 | 2 |
| 3 | CHI | 2.602✓ | 0.537 | 0.010 | 0 |
| 4 | BAL | 2.590✓ | 0.531 | 0.010 | 0 |
| 5 | LAC | 2.556✓ | 0.513 | 0.010 | 0 |
| 6 | PHI | 2.534✓ | 0.502 | 0.010 | 0 |
| 7 | SF | 2.527✓ | 0.498 | 0.010 | 0 |
| 8 | KC | 2.505✓ | 0.487 | 0.010 | 0 |

Distribution: GB×2, NE×2, ATL×1, BUF×1, DAL×1, IND×1, JAC×1, PIT×1

#### Week 18 — allocation *(LOW CONFIDENCE)*

Mode: **BRANCH** — close threshold = **0.3** log-nats (≈ 135% leverage ratio).

| rank | team | leverage_score | win_prob | crowd | entries |
| --- | --- | --- | --- | --- | --- |
| 1 | LAR | 2.750✓ | 0.623 | 0.010 | 0 |
| 2 | PHI | 2.744✓ | 0.619 | 0.010 | 0 |
| 3 | DAL | 2.659✓ | 0.569 | 0.010 | 0 |
| 4 | GB | 2.611✓ | 0.542 | 0.010 | 0 |
| 5 | DEN | 2.607✓ | 0.540 | 0.010 | 0 |
| 6 | JAC | 2.591✓ | 0.531 | 0.010 | 0 |
| 7 | CHI | 2.568✓ | 0.519 | 0.010 | 0 |
| 8 | MIN | 2.491✓ | 0.481 | 0.010 | 0 |

Distribution: CAR×4, SF×3, HOU×2, NE×1

## Thanksgiving allocation

Games: GB@LAR, CHI@DET, PHI@DAL, KC@BUF, DEN@PIT. Favorites/underdogs from `implied_win_prob`.

### Game-level chalk

| game | favorite | fav_win_prob | fav_crowd | underdog | dog_crowd |
| --- | --- | --- | --- | --- | --- |
| GB@LAR | LAR | 0.683 | 0.136 | GB | 0.003 |
| CHI@DET | DET | 0.576 | 0.114 | CHI | 0.033 |
| PHI@DAL | DAL | 0.522 | 0.084 | PHI | 0.088 |
| KC@BUF | BUF | 0.569 | 0.179 | KC | 0.020 |
| DEN@PIT | PIT | 0.510 | 0.259 | DEN | 0.085 |

### Per-entry picks

| entry | team | win_prob | crowd | leverage | role |
| --- | --- | --- | --- | --- | --- |
| entry_01 | DEN | 0.490 | 0.085 | 5.8 | underdog: contrarian vs PIT crowd 25.9% |
| entry_02 | KC | 0.431 | 0.020 | 21.6 | underdog: contrarian vs BUF crowd 17.9% |
| entry_03 | PHI | 0.478 | 0.088 | 5.4 | underdog: leverage / eligibility |
| entry_04 | DET | 0.576 | 0.114 | 5.1 | favorite: leverage / eligibility |
| entry_05 | BUF | 0.569 | 0.179 | 3.2 | favorite: leverage / eligibility |
| entry_06 | DAL | 0.522 | 0.084 | 6.2 | favorite: leverage / eligibility |
| entry_07 | PIT | 0.510 | 0.259 | 2.0 | favorite: leverage / eligibility |
| entry_08 | DET | 0.576 | 0.114 | 5.1 | favorite: leverage / eligibility |
| entry_09 | CHI | 0.424 | 0.033 | 12.8 | underdog: contrarian vs DET crowd 11.4% |
| entry_10 | PHI | 0.478 | 0.088 | 5.4 | underdog: leverage / eligibility |

### Spread across games

| game | entries on | count |
| --- | --- | --- |
| GB@LAR | — | 0 |
| CHI@DET | DET, DET, CHI | 3 |
| PHI@DAL | PHI, DAL, PHI | 3 |
| KC@BUF | KC, BUF | 2 |
| DEN@PIT | DEN, PIT | 2 |

### Team distribution (10 entries)

| team | count |
| --- | --- |
| DET | 2 |
| PHI | 2 |
| BUF | 1 |
| CHI | 1 |
| DAL | 1 |
| DEN | 1 |
| KC | 1 |
| PIT | 1 |
| **distinct teams** | **8** |

## Christmas allocation

Games: HOU@PHI, GB@CHI, BUF@DEN, LAR@SEA. Favorites/underdogs from `implied_win_prob`.

### Game-level chalk

| game | favorite | fav_win_prob | fav_crowd | underdog | dog_crowd |
| --- | --- | --- | --- | --- | --- |
| HOU@PHI | PHI | 0.605 | 0.144 | HOU | 0.228 |
| GB@CHI | CHI | 0.552 | 0.177 | GB | 0.054 |
| BUF@DEN | BUF | 0.517 | 0.181 | DEN | 0.041 |
| LAR@SEA | LAR | 0.511 | 0.023 | SEA | 0.095 |

### Per-entry picks

| entry | team | win_prob | crowd | leverage | role |
| --- | --- | --- | --- | --- | --- |
| entry_01 | GB | 0.448 | 0.054 | 8.3 | underdog: contrarian vs CHI crowd 17.7% |
| entry_02 | BUF | 0.517 | 0.181 | 2.9 | favorite: leverage / eligibility |
| entry_03 | GB | 0.448 | 0.054 | 8.3 | underdog: contrarian vs CHI crowd 17.7% |
| entry_04 | PHI | 0.605 | 0.144 | 4.2 | favorite: leverage / eligibility |
| entry_05 | DEN | 0.483 | 0.041 | 11.8 | underdog: contrarian vs BUF crowd 18.1% |
| entry_06 | PHI | 0.605 | 0.144 | 4.2 | favorite: leverage / eligibility |
| entry_07 | BUF | 0.517 | 0.181 | 2.9 | favorite: leverage / eligibility |
| entry_08 | DEN | 0.483 | 0.041 | 11.8 | underdog: contrarian vs BUF crowd 18.1% |
| entry_09 | DEN | 0.483 | 0.041 | 11.8 | underdog: contrarian vs BUF crowd 18.1% |
| entry_10 | BUF | 0.517 | 0.181 | 2.9 | favorite: leverage / eligibility |

### Spread across games

| game | entries on | count |
| --- | --- | --- |
| HOU@PHI | PHI, PHI | 2 |
| GB@CHI | GB, GB | 2 |
| BUF@DEN | BUF, DEN, BUF, DEN, DEN, BUF | 6 |
| LAR@SEA | — | 0 |

### Team distribution (10 entries)

| team | count |
| --- | --- |
| BUF | 3 |
| DEN | 3 |
| GB | 2 |
| PHI | 2 |
| **distinct teams** | **4** |

## Weeks 16–18 — LOW CONFIDENCE

Filled for legality; projected spreads are weak and resting starters are not modeled. See per-week notes above.

## Hard constraint verification

### Constraint 1 — no team reuse within an entry

**PASS** — all 10 entries have 20 distinct picks.
### Constraint 2 — Thanksgiving eligibility (Rule 8)

**PASS** — every entry held an unburned Th-leg team entering Th and played it.

- **entry_01**: Th **DEN** (Th∩Ch — reserves another Ch team); unburned entering Th: ['DEN', 'GB', 'PIT']
- **entry_02**: Th **KC** (Th-only — Ch freer); unburned entering Th: ['BUF', 'DAL', 'DEN', 'KC', 'PIT']
- **entry_03**: Th **PHI** (Th∩Ch — reserves another Ch team); unburned entering Th: ['BUF', 'DAL', 'DEN', 'GB', 'KC', 'PHI']
- **entry_04**: Th **DET** (Th-only — Ch freer); unburned entering Th: ['CHI', 'DEN', 'DET', 'GB', 'PHI', 'PIT']
- **entry_05**: Th **BUF** (Th∩Ch — reserves another Ch team); unburned entering Th: ['BUF', 'DEN', 'DET', 'GB', 'PIT']
- **entry_06**: Th **DAL** (Th-only — Ch freer); unburned entering Th: ['BUF', 'DAL', 'DEN', 'DET', 'KC', 'PHI']
- **entry_07**: Th **PIT** (Th-only — Ch freer); unburned entering Th: ['BUF', 'GB', 'PIT']
- **entry_08**: Th **DET** (Th-only — Ch freer); unburned entering Th: ['DEN', 'DET']
- **entry_09**: Th **CHI** (Th∩Ch — reserves another Ch team); unburned entering Th: ['CHI', 'DEN', 'GB', 'PIT']
- **entry_10**: Th **PHI** (Th∩Ch — reserves another Ch team); unburned entering Th: ['BUF', 'DAL', 'DEN', 'DET', 'PHI', 'PIT']
### Constraint 3 — Christmas eligibility (Rule 9)

**PASS** — every entry held an unburned Ch-leg team entering Ch and played it.

- **entry_01**: Ch **GB**; unburned entering Ch: ['GB']; Ch still available after portfolio: []
- **entry_02**: Ch **BUF**; unburned entering Ch: ['BUF']; Ch still available after portfolio: []
- **entry_03**: Ch **GB**; unburned entering Ch: ['GB', 'HOU']; Ch still available after portfolio: ['HOU']
- **entry_04**: Ch **PHI**; unburned entering Ch: ['GB', 'PHI']; Ch still available after portfolio: []
- **entry_05**: Ch **DEN**; unburned entering Ch: ['DEN', 'GB']; Ch still available after portfolio: []
- **entry_06**: Ch **PHI**; unburned entering Ch: ['BUF', 'HOU', 'PHI']; Ch still available after portfolio: []
- **entry_07**: Ch **BUF**; unburned entering Ch: ['BUF']; Ch still available after portfolio: []
- **entry_08**: Ch **DEN**; unburned entering Ch: ['DEN']; Ch still available after portfolio: []
- **entry_09**: Ch **DEN**; unburned entering Ch: ['DEN']; Ch still available after portfolio: []
- **entry_10**: Ch **BUF**; unburned entering Ch: ['BUF', 'HOU']; Ch still available after portfolio: []
### Constraint 4 — picks are teams playing that contest week

**PASS** — verified for all 200 picks (bye weeks respected).

### Max 6 entries per team per week

**PASS** — no team exceeds 6 entries in any contest week.

## Th team distribution

| team | entries |
| --- | --- |
| DET | 2 |
| PHI | 2 |
| BUF | 1 |
| CHI | 1 |
| DAL | 1 |
| DEN | 1 |
| KC | 1 |
| PIT | 1 |

## Ch team distribution

| team | entries |
| --- | --- |
| BUF | 3 |
| DEN | 3 |
| GB | 2 |
| PHI | 2 |

## Limitations (plain statement)

> Crowd projections come from a model that under-predicts herding in about 81% of historical weeks, so real crowd concentration will likely be HIGHER than projected. That makes the contrarian positions here, if anything, better than they appear — but it also means the projected shares themselves are soft. Win probabilities for weeks 2+ are projected from market win totals, not posted lines, and degrade with horizon. This portfolio is a defensible starting allocation derived from the model, NOT a proven-optimal portfolio; no optimality claim is made or verified.
