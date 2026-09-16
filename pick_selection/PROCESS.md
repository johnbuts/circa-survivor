# Opponent-parlay hedge — playbook

[Open the parlay calculator](file://wsl.localhost/Ubuntu-22.04/home/johnbuts/mobile_app/sports_circa/pick_selection/week1/index.html)

Circa Survivor: each entry picks one NFL team per week. If that team loses, the entry is dead. Ten entries picking among a small set of teams is a correlated book. The hedge is not “bet against football.” It is **buy the opponents of the teams you used**, so that when picks die the sportsbook pays you.

The calculator is a single local HTML file. No server. Change picks, counts, and prices there; this page is the why.

## Inputs

1. **Moneylines** — Circa American odds size parlays (editable on the site). FanDuel is live win-prob / leverage only. The Odds API key lives in `pick_selection/week1/.env` (`ODDS_API_KEY=…`, gitignored). Refresh odds with `uv run python fetch_fd_odds.py` in that folder, then **Refresh FanDuel** (or reload) to load `fanduel_odds.json`. Serve the folder over http so the JSON can load from `file://` fallback. Do not put the key in HTML.
2. **Pick list** — the distinct teams you will actually use this week.
3. **Entry counts** — how many of the `N` entries sit on each pick. Counts must sum to `N`. Dead-entry dollars follow these counts, not a 50/50 split.

Default Week 1 book (Sep 9 portfolio): **LAR 6 / DAL 2 / KC 2** across **10** entries, fee **$1,000**. Board moneylines are DraftKings as of Sep 11 (editable on the site as Circa). NE@SEA and SF@LAR are already final; those two cells keep the last posted DK prices.

## Mapping picks → parlay legs

Each pick has one opponent. That opponent is the leg you bet.

| Pick | DK ML | Opponent | Opponent ML |
| --- | --- | --- | --- |
| LAR | −198 | SF | +164 |
| DAL | −162 | NYG | +136 |
| KC | −148 | DEN | +124 |

A pick **losing** is exactly that opponent **winning**. A 3-leg of SF + NYG + DEN hits only if all three picks lose, which kills every entry sitting on those three teams.

Click any other team on the board to sub. Same-game click swaps sides (LAR → SF) and keeps that team’s entry count. A new game adds a pick. You cannot hold both sides of one game.

## Parlay math (posted Circa MLs, no extra juice)

American → decimal:

- `ml > 0` → `1 + ml / 100`
- `ml < 0` → `1 + 100 / |ml|`

Parlay decimal = product of the leg decimals.

Profit on stake `S` = `S × (decimal − 1)`.

Week 1 3-leg wipeout (SF +164, NYG +136, DEN +124):

- 2.64 × 2.36 × 2.24 = **13.956**
- Profit multiple = **12.956**
- Stake to cover `N × fee` = `$10,000 / 12.956` ≈ **$771.84**

That 3-leg is the wipeout cover: all picks lose, all 10 entries die, the ticket’s profit replaces the $10k in fees.

## 2-leg hedges

Round robin 2s: every combination of 2 opponents. For three picks that is `C(3,2) = 3` tickets.

Each 2-leg hits when those two opponents win (those two picks lose). The leftover pick can still win or lose.

Size a 2-leg off **dead entries on those two teams**, not off `N`:

```
S_2 = (count_A + count_B) × fee / (parlay_decimal − 1)
```

Example, counts LAR 6 / DAL 2 / KC 2:

- SF+NYG (KC wins): 8 entries dead, decimal 6.230, `S ≈ $1,529.52`
- SF+DEN (DAL wins): 8 dead, decimal 5.914, `S ≈ $1,628.13`
- NYG+DEN (LAR wins): 4 dead, decimal 5.286, `S ≈ $933.18`

If that leftover pick also loses, you are in wipeout — see correlation below.

## Round robin

For `n` opponent legs, size `k` produces `C(n,k)` tickets. The Sep 9 default book has **3** picks, so the wipeout ticket is size **3**. Enable size **2** if you want the three 2-legs. Size **4** is empty until you add a fourth pick.

Stake modes:

- **$ per ticket** — same dollar amount on every enabled ticket.
- **Bankroll split** — one pool divided evenly across enabled tickets.

Toggle tickets off without deleting the round-robin set.

## Wipeout correlation (do not double-count)

If all three opponents win, **every 2-leg and the 3-leg all hit**. The 2-legs are subsets of the 3-leg.

If you apply both “cover wipeout” and “cover each 2-loss” suggested stakes, wipeout pays the 3-leg cover **plus** all three 2-leg covers. That is overhedged on total death and expensive on the 2-loss rows. Pick a mix on the site; the scenario table shows the net.

A winning ticket pays `S × decimal` (stake back plus profit). A losing ticket pays `0` (stake gone).

```
bet_net   = payout − total_stake
          = hedge_profit − lost_stakes
week_pnl  = bet_net − dead_entries × fee
```

Size the wipeout 3-leg so `hedge_profit ≈ N × fee`. On that row, if it is the only ticket, `lost_stakes = 0` and `week_pnl ≈ 0`: fees replaced, stake returned. Live entries are still in the contest; this score is only this week’s hedge vs fees burned.

## Using the calculator

1. Confirm prices on the board (edit a number if the line moved).
2. Default picks are LAR / DAL / KC (6 / 2 / 2). Click another team to sub.
3. Type entry counts so they sum to `N`.
4. Check round-robin sizes. Use the cover helper as a starting stake, or type your own.
5. Mark games W/L in the sandbox, or read the full `2^n` table (8 rows when `n = 3`).
6. Scroll to **Crowd split** to see week-1 chip EV if the projected people split is the true field. Click a team to flip a result (favorites win by default).

Yellow rows = exactly one pick survived (a 2-loss for `n = 3`). Red row = wipeout.

## Crowd split and week-1 chip equity

The people-split numbers are **copied** from the already-run 2026 projection (`pick_projections_2026.csv` week 1). The calculator does not resimulate. Field start **20,000**, pot **$20M**.

This panel is **not** the Monte Carlo equity engine (`model/equity.py`). It is a week-1 chip snapshot:

```
field_alive = 20000 × sum(crowd_share of teams that won)
chip EV (live ticket) = 20000000 / field_alive
dead ticket = $0
portfolio = n_ours_alive × chip EV
```

Leverage on each side uses the Circa ML on the page: `log(P_win) − 0.7 × log(max(crowd, 0.01))`.

If JAC (35.4%), LAC (30.7%), and DET (14.2%) all win, almost the whole field survives and chip EV sits near the $1,000 fee. Flip a chalk loss: the field shrinks and every live ticket’s chip EV jumps. That is the test of fading the model’s crowd.
