# Simulation tables (generated)

Worlds: **65,536** (every week-1 winner combination). Probability mass sums to **1.000000000000**.
Game outcomes: independent, vig-free Circa implied probabilities. Parlay payouts: posted Circa decimals (juice in).
Chip = `$20,000,000 / field_alive`. Buy-in = **$10,000** (10 × $1,000).
Wealth = `hedge_net + ours_alive × chip − buy-in`.

## Slate facts

- Crowd share if every Circa favorite wins: **99.30%** → field alive **19,860** → chip **$1,007**.
- P(LAC loses) = **17.5%** (vig-free). Crowd on LAC: **40.7%**.
- P(JAC loses) = **22.4%**. Crowd **20.2%**.
- P(DET loses) = **24.7%**. Crowd **16.2%**.
- P(LAC, JAC, DET all win) = **48.2%**.
- P(at least one of those three loses) = **51.8%**.
- Chip if LAC loses and other favorites hold: field share drops by 40.7 pp.

## Books with no hedge (naked) — where the money actually is

| book | tickets | E[ours alive] | P(wipe) | E[chip portfolio] | E[wealth vs $10k] | P(wealth>0) | 5th pct wealth |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all chalk | LAC×10 | 8.25 | 17.5% | $10,179 | $179 | 82.4% | -$10,000 |
| chalk split | LAC×6 JAC×4 | 8.06 | 3.9% | $10,270 | $270 | 71.2% | -$2,819 |
| two-team fade | SEA×5 BAL×5 | 6.32 | 13.6% | $9,312 | -$688 | 45.5% | -$10,000 |
| three-team fade | SEA×4 BAL×3 CIN×3 | 6.38 | 4.7% | $9,394 | -$606 | 38.6% | -$6,859 |
| four-team fade | SEA×3 BAL×3 CIN×2 PHI×2 | 6.45 | 1.5% | $9,439 | -$561 | 36.1% | -$7,218 |
| five-team fade | SEA×2 BAL×2 CIN×2 PHI×2 LAR×2 | 6.50 | 0.5% | $9,529 | -$471 | 35.5% | -$5,754 |

## Hedge menu — all chalk

_every ticket on the 41% crowd favorite. Book: `LAC×10`._

| hedge | #tk | risked | E[hedge net] | E[chip] | E[wealth] | P(>0) | 5th pct | median | E[wealth \| chalk holds] | E[wealth \| LAC loses] | P(wipe) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| naked | 0 | $0 | $0 | $10,179 | $179 | 82.4% | -$10,000 | $1,136 | $955 | -$10,000 | 17.5% |
| wipe | 0 | $0 | $0 | $10,179 | $179 | 82.4% | -$10,000 | $1,136 | $955 | -$10,000 | — |

## Hedge menu — chalk split

_the two biggest crowd teams. Book: `LAC×6 JAC×4`._

| hedge | #tk | risked | E[hedge net] | E[chip] | E[wealth] | P(>0) | 5th pct | median | E[wealth \| chalk holds] | E[wealth \| LAC loses] | P(wipe) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| naked | 0 | $0 | $0 | $10,270 | $270 | 71.2% | -$2,819 | $753 | $955 | -$3,112 | 3.9% |
| wipe | 1 | $442 | -$33 | $10,270 | $237 | 62.8% | -$2,719 | $311 | $513 | -$1,219 | — |
| 2cover | 1 | $442 | -$33 | $10,270 | $237 | 62.8% | -$2,719 | $311 | $513 | -$1,219 | — |

## Hedge menu — two-team fade

_thin-crowd favorites, concentrated. Book: `SEA×5 BAL×5`._

| hedge | #tk | risked | E[hedge net] | E[chip] | E[wealth] | P(>0) | 5th pct | median | E[wealth \| chalk holds] | E[wealth \| LAC loses] | P(wipe) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| naked | 0 | $0 | $0 | $9,312 | -$688 | 45.5% | -$10,000 | -$1,639 | -$3,126 | $6,751 | 13.6% |
| wipe | 1 | $1,721 | -$132 | $9,312 | -$820 | 24.9% | -$6,419 | -$1,083 | -$3,258 | $6,620 | — |
| 2cover | 1 | $1,721 | -$132 | $9,312 | -$820 | 24.9% | -$6,419 | -$1,083 | -$3,258 | $6,620 | — |

## Hedge menu — three-team fade

_still fading; one extra independent game. Book: `SEA×4 BAL×3 CIN×3`._

| hedge | #tk | risked | E[hedge net] | E[chip] | E[wealth] | P(>0) | 5th pct | median | E[wealth \| chalk holds] | E[wealth \| LAC loses] | P(wipe) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| naked | 0 | $0 | $0 | $9,394 | -$606 | 38.6% | -$6,859 | -$1,859 | -$3,060 | $6,876 | 4.7% |
| wipe | 1 | $562 | -$63 | $9,394 | -$669 | 31.5% | -$7,191 | -$1,611 | -$3,123 | $6,813 | — |
| 3cover | 1 | $562 | -$63 | $9,394 | -$669 | 31.5% | -$7,191 | -$1,611 | -$3,123 | $6,813 | — |
| wipe+3 | 1 | $562 | -$63 | $9,394 | -$669 | 31.5% | -$7,191 | -$1,611 | -$3,123 | $6,813 | — |
| 2cover | 3 | $3,298 | -$251 | $9,394 | -$857 | 25.1% | -$6,631 | -$1,930 | -$3,311 | $6,625 | — |

## Hedge menu — four-team fade

_more independent lives, more hedge legs. Book: `SEA×3 BAL×3 CIN×2 PHI×2`._

| hedge | #tk | risked | E[hedge net] | E[chip] | E[wealth] | P(>0) | 5th pct | median | E[wealth \| chalk holds] | E[wealth \| LAC loses] | P(wipe) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| naked | 0 | $0 | $0 | $9,439 | -$561 | 36.1% | -$7,218 | -$1,370 | -$3,009 | $6,879 | 1.5% |
| wipe | 1 | $182 | -$27 | $9,439 | -$588 | 34.4% | -$6,788 | -$1,454 | -$3,036 | $6,852 | — |
| 3cover | 4 | $1,549 | -$174 | $9,439 | -$736 | 26.5% | -$6,179 | -$1,871 | -$3,184 | $6,705 | — |
| wipe+3 | 5 | $1,730 | -$201 | $9,439 | -$763 | 25.5% | -$6,361 | -$2,053 | -$3,210 | $6,678 | — |
| rr3+4 | 5 | $50 | -$6 | $9,439 | -$567 | 35.9% | -$7,077 | -$1,419 | -$3,015 | $6,873 | — |
| 2cover | 6 | $4,675 | -$358 | $9,439 | -$919 | 27.7% | -$7,221 | -$3,153 | -$3,367 | $6,521 | — |

## Hedge menu — five-team fade

_widest book; 2^5 = 32 pick-masks. Book: `SEA×2 BAL×2 CIN×2 PHI×2 LAR×2`._

| hedge | #tk | risked | E[hedge net] | E[chip] | E[wealth] | P(>0) | 5th pct | median | E[wealth \| chalk holds] | E[wealth \| LAC loses] | P(wipe) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| naked | 0 | $0 | $0 | $9,529 | -$471 | 35.5% | -$5,754 | -$1,534 | -$2,948 | $7,069 | 0.5% |
| wipe | 1 | $64 | -$12 | $9,529 | -$482 | 35.1% | -$5,763 | -$1,581 | -$2,960 | $7,057 | — |
| 3cover | 10 | $3,043 | -$341 | $9,529 | -$812 | 22.9% | -$6,571 | -$2,484 | -$3,290 | $6,728 | — |
| wipe+3 | 11 | $3,107 | -$353 | $9,529 | -$823 | 22.7% | -$6,635 | -$2,548 | -$3,301 | $6,716 | — |
| rr3+4 | 15 | $150 | -$19 | $9,529 | -$489 | 34.2% | -$5,600 | -$1,666 | -$2,967 | $7,050 | — |
| 2cover | 10 | $6,121 | -$467 | $9,529 | -$937 | 34.1% | -$7,683 | -$3,517 | -$3,415 | $6,602 | — |

## Juice: E[hedge net] is the sportsbook's cut

Negative hedge net means Circa prices are not a gift. You are buying insurance at a retail markup.

| book | hedge | E[hedge net] | cash risked |
| --- | --- | ---: | ---: |
| all chalk | wipe | $0 | $0 |
| chalk split | wipe | -$33 | $442 |
| chalk split | 2cover | -$33 | $442 |
| two-team fade | wipe | -$132 | $1,721 |
| two-team fade | 2cover | -$132 | $1,721 |
| three-team fade | wipe | -$63 | $562 |
| three-team fade | 3cover | -$63 | $562 |
| three-team fade | wipe+3 | -$63 | $562 |
| three-team fade | 2cover | -$251 | $3,298 |
| four-team fade | wipe | -$27 | $182 |
| four-team fade | 3cover | -$174 | $1,549 |
| four-team fade | wipe+3 | -$201 | $1,730 |
| four-team fade | rr3+4 | -$6 | $50 |
| four-team fade | 2cover | -$358 | $4,675 |
| five-team fade | wipe | -$12 | $64 |
| five-team fade | 3cover | -$341 | $3,043 |
| five-team fade | wipe+3 | -$353 | $3,107 |
| five-team fade | rr3+4 | -$19 | $150 |
| five-team fade | 2cover | -$467 | $6,121 |

## Chip size under crowd events

- E[chip | LAC, JAC, DET all win] = **$1,095**
- E[chip | LAC loses] = **$2,714**
- E[chip | at least one of LAC/JAC/DET loses] = **$1,863**
- Unconditional E[chip] = **$1,493**

Unconditional chip is a mixture: most mass sits near the favorite-wins world (~$1,095), with a long right tail when chalk dies.

Generated by `hedge_econ.py`. Probability checksum 1.000000000000.
