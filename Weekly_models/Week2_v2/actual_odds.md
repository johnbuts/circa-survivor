# Week 2 actual odds vs predicted crowd split

DraftKings lines from `data/2026/raw/nfl_week2_spreads_2026.csv` (as of 2026-09-15). Crowd columns are field-conditioned: 16,978 live entries cannot re-pick their Week 1 team.

- **v1 freeze:** `Week2_v1` leftover nest (`leftover_jac_boost`). From `Week2_v1/out/week2_shares.csv`.
- **v2 freeze:** `Week2_v2` steam + skip-inventory leftover + FV-gap γ=4. From `Week2_v2/out/week2_shares.csv`.

Both put ~57–60% on SF+TB, then BAL. v2 is SF-first and heavier on LAC/NE. v1 is TB-first and still prints PIT at 3.6% as a dog.

## Predicted crowd split

| team | spread | implied | v1 crowd | v2 crowd | Δ (v2−v1) |
| --- | ---: | ---: | ---: | ---: | ---: |
| SF | −13.5 vs MIA | 87.6% | 26.6% | **30.5%** | +3.9 |
| TB | −8.5 vs CLE | 77.4% | **30.2%** | 29.2% | −1.0 |
| BAL | −8.5 vs NO | 77.4% | 11.0% | 10.6% | −0.4 |
| LAC | −7.0 vs LV | 73.4% | 6.0% | 9.1% | +3.1 |
| PHI | −7.0 @ TEN | 73.4% | 4.7% | 4.5% | −0.2 |
| LAR | −7.0 vs NYG | 73.4% | 4.8% | 3.6% | −1.2 |
| KC | −6.5 vs IND | 71.9% | 4.4% | 3.5% | −0.9 |
| CHI | −5.5 vs MIN | 68.9% | 2.7% | 2.4% | −0.3 |
| NE | −5.5 vs PIT | 68.9% | ~0% | 1.9% | +1.9 |
| PIT | +5.5 @ NE | 31.1% | 3.6% | ~0% | −3.6 |
| BUF | −4.5 vs DET | 65.7% | 1.3% | 0.9% | −0.4 |
| GB | −4.5 @ NYJ | 65.7% | 1.2% | 0.9% | −0.3 |
| DAL | −4.5 vs WAS | 65.7% | 1.1% | 0.8% | −0.3 |
| SEA | −4.5 @ ARI | 65.7% | 0.8% | 0.6% | −0.2 |
| CAR | −2.5 @ ATL | 59.0% | 0.8% | 0.9% | +0.1 |
| HOU | −2.5 vs CIN | 59.0% | 0.5% | 0.4% | −0.1 |
| DEN | −2.5 vs JAC | 59.0% | 0.3% | 0.2% | −0.1 |
| everyone else | — | dogs | ~0% | ~0% | — |

Top 3: **v1 TB / SF / BAL (67.8%)**. **v2 SF / TB / BAL (70.3%)**.

## Game board

| kickoff | game | line / total | v1 pick % | v2 pick % |
| --- | --- | --- | --- | --- |
| Thu 8:15 | DET @ **BUF** | BUF −4.5 / 53.5 | BUF 1.3 | BUF 0.9 |
| Sun 1:00 | **CAR** @ ATL | CAR −2.5 / 43.5 | CAR 0.8 | CAR 0.9 |
| Sun 1:00 | NO @ **BAL** | BAL −8.5 / 46.5 | BAL 11.0 | BAL 10.6 |
| Sun 1:00 | MIN @ **CHI** | CHI −5.5 / 48.5 | CHI 2.7 | CHI 2.4 |
| Sun 1:00 | CIN @ **HOU** | HOU −2.5 / 46.5 | HOU 0.5 | HOU 0.4 |
| Sun 1:00 | CLE @ **TB** | TB −8.5 / 40.5 | TB **30.2** | TB **29.2** |
| Sun 1:00 | **GB** @ NYJ | GB −4.5 / 44.5 | GB 1.2 | GB 0.9 |
| Sun 1:00 | PIT @ **NE** | NE −5.5 / 41.5 | PIT 3.6 / NE ~0 | NE 1.9 / PIT ~0 |
| Sun 1:00 | **PHI** @ TEN | PHI −7.0 / 39.5 | PHI 4.7 | PHI 4.5 |
| Sun 4:05 | JAC @ **DEN** | DEN −2.5 / 44.5 | DEN 0.3 | DEN 0.2 |
| Sun 4:05 | LV @ **LAC** | LAC −7.0 / 43.5 | LAC 6.0 | LAC **9.1** |
| Sun 4:25 | **SEA** @ ARI | SEA −4.5 / 41.5 | SEA 0.8 | SEA 0.6 |
| Sun 4:25 | WAS @ **DAL** | DAL −4.5 / 50.5 | DAL 1.1 | DAL 0.8 |
| Sun 4:25 | MIA @ **SF** | SF −13.5 / 45.5 | SF **26.6** | SF **30.5** |
| Sun 8:20 | IND @ **KC** | KC −6.5 / 47.5 | KC 4.4 | KC 3.5 |
| Mon 8:15 | NYG @ **LAR** | LAR −7.0 / 48.5 | LAR 4.8 | LAR 3.6 |

The only material model disagreement on a live ticket is **PIT vs NE**: v1 leftover still dumps 3.6% onto PIT (31% implied), while v2 puts 1.9% on NE and ~0 on PIT. Everything else is the same slate; v2 herds harder onto SF and LAC.
