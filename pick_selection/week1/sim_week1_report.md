# Week 1 100k pick-book simulation

Our book: **BAL×3, TEN×3, PIT×2, LV×2**. Crowd shares from the already-run 2026 projection (not resimulated).
Each game: vig-free Circa implied favorite P(win), times Uniform(0.90, 1.10), clip to [0.01, 0.99]. Seed **42**. N = **100,000**.
Draws and scoring run on GPU (CuPy / RTX 3070 Ti): one `(N, 16)` uniform noise matrix, one Bernoulli draw, two matmuls for `n_ours` and field share. CuPy RNG ≠ NumPy RNG, so counts differ from the CPU run at the same seed.
GPU wall time: **0.006s**.
Chip EV = `$20M / field_alive`. Field alive = `20000 × sum(crowd share of winners)`. Percentile bands are the spread of simulated outcomes, not a CI on the mean.

## Remaining entries (ours)

- Mean: **6.035**
- 68%: 3.00 – 8.00
- 95%: 2.00 – 10.00
- 99%: 0.00 – 10.00
- P(wipeout) = 0.0238; P(all 10 alive) = 0.1354

| n | draws |
| --- | ---: |
| 0 | 2385 |
| 1 | 0 |
| 2 | 7835 |
| 3 | 7178 |
| 4 | 6225 |
| 5 | 22667 |
| 6 | 5152 |
| 7 | 18386 |
| 8 | 16631 |
| 9 | 0 |
| 10 | 13541 |

## Chip EV per live ticket

- Mean: **$1,492.05**
- 68%: $1,068.38 – $1,876.17
- 95%: $1,025.64 – $3,389.83
- 99%: $1,010.10 – $6,756.76

## Total equity (n_ours × chip EV)

- Mean: **$8,845.93**
- 68%: $4,390.78 – $12,376.24
- 95%: $2,150.54 – $23,411.37
- 99%: $0.00 – $41,322.80

Identity check: mean(n_ours × chip) = $8,845.93 vs mean(total) $8,845.93.
