# Week 5 numbers (as of 2026-10-07)

Official Circa field entering Week 5: **5,972** live / **25,017** start, pot **$25,017,000**. Chip if the contest paid tonight: **$4,189**.

Run `python3 Weekly_models/Week5/crowd.py` (standard library only). It reads `inputs.json` and writes `out/week5_shares.csv`, `out/week5_book.md`, and `assets/week5-crowd.js` for the hub.

## Correction: field entering Week 3 was 8,610

The site said 8,464 entering Week 3. Circa’s official count was **8,610** ([Circa X](https://x.com/CircaSports/status/2102411970024775807): “8,368 Eliminated ✅ 8,610 Survive to Week 3”). The 8,464 figure was taken before MNF and left out the 146 Rams tickets that won. Week 3 pages are a snapshot and keep the old number.

## Field path

| point | live | eliminated | source |
| --- | ---: | ---: | --- |
| enter Week 3 | 8,610 | 8,368 | [Circa X](https://x.com/CircaSports/status/2102411970024775807) |
| enter Week 4 | 6,292 | 2,318 | [Circa X](https://x.com/CircaSports/status/2104898765954187484) |
| enter Week 5 | 5,972 | 320 | [circasports.com](https://www.circasports.com/circa-survivor) |

## Week 3 Circa actual (of 8,607 picks, 3 no-pick)

[Selections PDF](https://www.circasports.com/wp-content/uploads/2026/09/Circa-Survivor-2026-Week-3-Selections.pdf).

| team | n | % | result |
| --- | ---: | ---: | --- |
| KC | 4,398 | 51.1 | W 24–10 @ MIA |
| SEA | 1,111 | 12.9 | L 31–33 @ WAS |
| DET | 743 | 8.6 | W 31–24 vs NYJ |
| SF | 591 | 6.9 | W 36–30 vs ARI |
| GB | 497 | 5.8 | L 14–35 vs ATL |
| BUF | 431 | 5.0 | W 24–16 vs LAC |
| NO | 405 | 4.7 | L 27–35 vs LV |
| CIN | 108 | 1.3 | L 27–30 @ PIT |
| CAR | 89 | 1.0 | L 18–21 @ CLE |
| PHI | 66 | 0.8 | L 7–27 @ CHI |
| NYG | 58 | 0.7 | W 12–7 vs TEN |

Week 3 stand-in (PoolGenius × Week 2 burns) had KC 43.5 / GB 14.2 / DET 10.9 / SEA 9.8 / BUF 7.7 / SF 2.0. KC was taller than projected, GB was a third of it, and SF was 3× because only Week 2 burns were counted.

## Week 4 Circa actual (of 6,291 picks, 1 no-pick)

[Selections PDF](https://www.circasports.com/wp-content/uploads/2026/10/Circa-Survivor-2026-Week-4-Selections.pdf).

| team | n | % | result |
| --- | ---: | ---: | --- |
| MIN | 2,733 | 43.4 | W 15–10 vs MIA |
| BAL | 2,449 | 38.9 | W 24–18 vs TEN |
| SEA | 442 | 7.0 | W 30–23 vs LAC |
| BUF | 178 | 2.8 | L 26–29 vs NE |
| IND | 161 | 2.6 | W 30–13 vs WAS (London) |
| ARI | 91 | 1.4 | L 24–36 @ NYG |
| GB | 81 | 1.3 | W 17–14 @ TB |
| CHI | 62 | 1.0 | W 23–12 vs NYJ |

Public × availability backtest for Week 4 (from `crowd.py`): BAL 38.6 vs 38.9, MIN 38.5 vs 43.4, SEA 5.5 vs 7.0, BUF 4.4 vs 2.8. Circa runs slightly heavier on the top pick than the public; the Week 5 crowd is not sharpened for that.

## Week 5 crowd (stand-in until the Circa PDF, usually Saturday)

Public base = ½ [PoolGenius 6 Oct](https://poolgenius.teamrankings.com/nfl-survivor-pool-picks/articles/week-5-strategy-advice-help-2026/) (DAL 33 / CIN 22 / HOU 19 / DET 9 / NE 6, tail spread by SurvivorGrid) + ½ [SurvivorGrid](https://www.survivorgrid.com/) 7 Oct (DAL 45.3 / CIN 26.8 / HOU 12.9 / DET 3.3 / JAC 2.0). Then × Circa’s official [Week 5 team availability](https://www.circasports.com/wp-content/uploads/2026/10/Circa-Survivor-2026-Week-5-Team-Availability.pdf) and renormalized.

Availability replaces the old burn estimate: it is Circa’s own count of live tickets that have not used each team. Big burns: SF 11.6% left, KC 26.5% (bye anyway), JAC 49.4%, MIN 53.7%, BAL 58.1%, DET 77.9%, PIT 78.2%.

| team | Circa crowd % | win % (vig-free DK) |
| --- | ---: | ---: |
| DAL | 40.7 | 79.1 |
| CIN | 25.0 | 74.1 |
| HOU | 16.7 | 75.1 |
| DET | 5.0 | 68.5 |
| NE | 4.0 | 63.7 |
| CLE | 2.1 | 46.8 |
| DEN | 1.8 | 62.2 |
| JAC | 1.1 | 74.8 |

Crowd survives at implied rates **73.9%** → expected chip **$5,670**. If DAL alone loses, ~3,319 live and chip ~$7,536.

Byes: KC, CAR. Lines are DraftKings via ESPN’s odds feed, 7 Oct ~21:10 UTC. Big moves since open (JAC now −7 vs PHI in London, ATL −3.5 vs BAL, NE −3.5 vs LV, DET −5.5 @ ARI). PoolGenius reports Ja’Marr Chase likely out (concussion) and Tee Higgins hurt, so CIN may drift. Re-pull lines before locking.

## Our book

Not recorded. The repo has our 3 live tickets into Week 3 (04 JAC→SF, 06 PIT→SF, 10 LV→SF) but no Week 3 or Week 4 picks. The Week 5 chip board prices the field only until the picks are added to `assets/our-book.js`.
