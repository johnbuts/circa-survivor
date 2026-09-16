# Power rankings + implied odds — end to end

This is the playbook from the 2026 NFL offseason work: consensus power rankings from public lists, then DraftKings moneyline scrape → implied win % on a team-by-week grid. Read this before repeating the pipeline. The kinks below are real bugs we hit; they are easy to reintroduce.

## What we actually produced

Two separate artifacts, not one:

1. **Consensus 2026 power rankings** — average rank of 32 teams across full 1–32 lists. The June offseason run used **17** lists. The Week 1 2026 dated run lives in [`9-1-2026/`](9-1-2026/) and uses **15** camp/preseason lists (see that folder’s `SOURCES.md`).
2. **Implied win % by week** — `team_weekly_implied_odds.csv`: rows = teams, columns = Week 1–18 plus Thanksgiving and Christmas. Cell = that team’s implied win probability that week.

The first is media opinion. The second is market prices. Do not mix them into one table without labeling which is which.

**Store every source, not just the average.** Each 1–32 list is its own CSV (`9-1-2026/sources/{id}.csv` plus `manifest.csv`). If a ranking page also quotes Super Bowl odds, keep those on that source file and in `source_sb_odds.csv`. DraftKings per-game moneylines/spreads/implied % go in `game_implied_odds.csv` next to the weekly grid. Do not throw away the ingredients after you bake the consensus.

---

## Part 1 — Consensus power rankings

### Goal

One 1–32 list that reflects what the market of *lists* actually said, not one writer’s take.

### How we did it

1. Search broadly for 2026 NFL power rankings. For a “right now” run, take the **latest full 1–32 per outlet** inside the stated window (camp / preseason / Week 1 for `9-1-2026/`; post-draft through June 1 for the 17-list below).
2. Keep only lists with a **full 1–32 order**. Write that order to its own file before averaging.
3. Drop syndicated copies (Yahoo reprinting Sporting News, AFI reprinting CBS, team-site recaps of FOX).
4. Average each team’s rank across remaining sources.
5. Report min / max / std so disagreement is visible.

### Sources used for the average (17)

These were the only ones in the numeric average. Full 32-team lists only.

1. https://bleacherreport.com/articles/25423042-br-expert-nfl-power-rankings-every-team-after-2026-nfl-draft
2. https://bleacherreport.com/articles/25433074-updated-nfl-power-rankings-after-myles-garrett-aj-brown-blockbuster-trades
3. https://www.profootballnetwork.com/2026-nfl-power-rankings-memorial-day-edition/
4. https://www.profootballnetwork.com/2026-nfl-power-rankings-myles-garrett-trade/
5. https://www.theringer.com/2026/05/21/nfl/nfl-2026-offseason-power-rankings
6. https://www.thescore.com/nfl/news/3530790/nfl-power-rankings-sizing-up-each-team-after-the-draft
7. https://www.sportingnews.com/us/nfl/news/nfl-power-rankings-2026-post-draft-edition/1884e4c7cc7c1c5604b1da2c
8. https://www.nfl.com/news/nfl-power-rankings-post-2026-nfl-draft
9. https://www.si.com/nfl/nfl-power-rankings-post-draft-2026-conor-orr
10. https://www.si.com/nfl/draft/onsi/news/nfl-draft-created-obvious-winners-and-brutal-losers-in-2026-power-rankings
11. https://fansided.com/nfl/nfl-power-rankings-after-myles-garrett-and-a-j-brown-trades-send-shockwaves
12. https://www.dazn.com/en-CA/news/football/nfl-power-rankings-2026-rams-seahawks-dolphins/clasfn6du89d1xnyxakqn7tqz
13. https://www.foxsports.com/stories/nfl/2026-nfl-power-rankings-how-schedule-release-shook-up-league-hierarchy
14. https://www.sharpfootballanalysis.com/analysis/nfl-power-rankings/
15. https://twsn.net/2026/04/27/2026-post-draft-nfl-power-rankings/
16. https://walterfootball.com/nflpowerrankings.php
17. https://www.espn.com/nfl/story/_/id/48845972/2026-nfl-season-football-power-index-projections-super-bowl-chances-simulations

### Kinks — power rankings

**Do not count “25 sources” as 25 independent lists.** Search hits include republishes, recaps, top-10 YouTube, paywalled PFF, and end-of-last-season lists. We started with ~28 URLs and only 17 were complete, independent 1–32 orders. If you quote a source count, use the number that went into the average.

**Human polls vs models disagree on #1.** CBS / NFL.com / Sporting News / PFSN Memorial Day kept **Seattle** (defending champ). Post–Myles Garrett lists and ESPN FPI moved **Rams** to #1. Averaging is correct; pretending there was a unanimous #1 is not.

**Do not average lists from different calendar moments without saying so.** Post-draft (late April) vs post-Garrett (June 1) moved Rams, Patriots, Browns, Eagles. Mixing them is fine if you want a season-long consensus; it is not fine if you want “right now after the last trade.” The Week 1 2026 folder is camp/preseason only; it does not re-average the 17 April–June URLs.

**theScore omitted Pittsburgh.** Interpolating PIT at 19 was a one-off. Prefer dropping the source or filling from the page, not guessing.

**Outliers warp std, not just average.** TWSN put Bengals at #2; most lists had them mid-teens. Report std. Do not treat TWSN as a second vote equal to NFL.com without noting it.

**CBS Prisco was referenced but not in the 17.** Only the top of his list was retrieved. Do not silently include a partial list in an average.

---

## Part 2 — DraftKings scrape → implied odds

### Goal

For every 2026 regular-season game, convert posted American moneylines into implied win % for the team playing that week.

### Inputs

| File | Role |
|------|------|
| `9-1-2026/draftkings_raw_scrape.txt` | Copy-paste of DK future/game board (spread / total / moneyline blocks) |
| `../nfl_schedule_2026.tsv` | Official week grid: opponent abbr, `@` = away, blank = bye, Thanksgiving and Christmas as their own columns |
| `build_matchup_implied_odds.py` | Parser + join |
| `9-1-2026/game_implied_odds.csv` | Per-game spread / ML / implied % |
| `9-1-2026/team_weekly_implied_odds.csv` | Team × week output |

June parent copies of the scrape and weekly grid stay untouched. Point `OUT_DIR` in `build_matchup_implied_odds.py` at the dated folder for this run, then:

```bash
python3 /home/johnbuts/mobile_app/sports_circa/Power_Rankings/build_matchup_implied_odds.py
```

Consensus ranks for the latest dated run (entering Week 2):

```bash
python3 /home/johnbuts/mobile_app/sports_circa/Power_Rankings/9-15-2026/average_ranks.py
```

Earlier snapshots stay in [`9-1-2026/`](9-1-2026/) and [`9-9-2026/`](9-9-2026/). Do not overwrite them.

### End-to-end flow

```
DK HTML copy-paste
    → parse each "AWAY-logo / at / HOME-logo" block
    → extract away spread, over, away ML, home spread, under, home ML
    → implied P(win) from moneyline (preferred) or spread (fallback)
    → join to schedule on (away, home)
    → write Team × week CSV
```

### Moneyline → implied probability (no vig removal)

- Favorite (`ml < 0`): `P = |ml| / (|ml| + 100)`
- Dog (`ml > 0`): `P = 100 / (ml + 100)`

Example: NE @ SEA, NE +170 / SEA −205 → 37.04% / 67.21%. Those **sum to more than 100%**. That is book juice. We did **not** normalize to 50/50. If you need fair (no-vig) probs, divide each by the two-way sum. Do not mix vig-implied and no-vig in the same column.

### Spread fallback (7 games had no ML)

`P ≈ Φ(−spread / (13.5 × √2))`  — NFL heuristic, ~13.5 points per SD of margin.

Use only when both moneylines are missing. Do not treat a spread-implied 22.94% as comparable precision to a posted +170.

---

## Kinks — scraping and joining (do not repeat)

### 1. Unicode minus is not ASCII hyphen

DraftKings paste uses `−` (U+2212), not `-`. American-odds regex on `-205` fails until you `replace("\u2212", "-")` on every token. If moneylines all come back `None`, this is the first thing to check.

### 2. Never skip a line “because there is a blank”

First parser skipped one line after the home team name. That shifted every field: juice `+100` became a “spread,” `+3` became a “moneyline.” Symptom: `away_spread is None` for every game, or spreads like `100.0`. **Always walk tokens, never skip a blank as if it were a field.**

### 3. Juice vs moneyline look the same

After the over, the next number is either away ML **or** the home spread if DK omitted the ML.

Wrong rule we used first: “if `|value| ∈ {100, 105, 110, 115, 120, 125, 130}` it is juice, not ML.”

That dropped real moneylines like **−115 / −105** (BUF @ HOU). Result: 66 games “missing” a direction even though the scrape had both sides.

Correct rule: after `O / total / juice`, if the next token is a **spread-sized number** (`abs ≤ 30`), there is no away ML. Otherwise it is the ML. Spread juice is the token **immediately after** the spread, not after the total.

### 4. Do not put home win % in the away cell

First team×team matrix stored:

- `(away, home)` = away implied
- `(home, away)` = **home** implied for the **same** game

That made `NYJ, BUF` an average of (NYJ @ BUF as a dog) **and** (BUF @ NYJ home favorite). Two different games. Cells must mean **row team playing at column team** (or, in the weekly grid, **this team in this week**). Never fill the reverse pair from the same game’s home line.

### 5. Team×team is the wrong grid for a season

NFL teams do not play everyone. 272 games fill 272 ordered pairs, not 992. Empty cells are “no game,” not 0%. The user-facing grid is **Team × week**, not Team × team.

### 6. Thanksgiving and Christmas are not Week 12 / Week 16

The schedule has extra columns. Teams that play Thursday Thanksgiving (e.g. BUF vs KC, CHI @ DET) must land in **Thanksgiving**, not Week 12. Christmas games (BUF @ DEN, LAR @ SEA, HOU @ PHI) must land in **Christmas**. Blank in those columns means that team does not play that holiday slate. BYE is a blank in a numbered week, not a holiday column.

If you flatten “Thanksgiving into Week 12,” you will double-book or drop games.

### 7. Schedule home/away can disagree with the book

Week 9: schedule said CIN hosts ATL. DK listed **CIN at ATL**. Join on exact `(away, home)` missed the game until we fell back to the reversed pair **and still attributed win % to the schedule’s team**, not to whoever DK called home.

Always:

1. Try `(away, home)` from the schedule cell (`@X` → this team away).
2. If the Odds API dump is a **full-season** board and the book flipped home/away for that same game, try the reverse pair and still attribute win % to the schedule’s team.
3. If the dump is **this week only** (16 events), do **not** use the reverse pair — it will stamp this week’s price onto a later rematch. Leave later weeks blank.
4. Log every reverse hit. If you get more than a couple on a full-season dump, the schedule file or the scrape is stale.

### 8. Parser must stop at the date line, not at “More Bets”

A game block ends with `Wed Sep 9th 7:15 PM` then `More Bets`. If you consume past the date into the next game’s logo line, you steal the next matchup. 272 `at` lines in the scrape should yield 272 games. If you get 271 or 273, you merged or split a block.

### 9. Two LA teams, two NY teams

Short names in the scrape are `LA Rams` / `LA Chargers` and `NY Giants` / `NY Jets`. Schedule abbrs are `LAR` / `LAC`, `NYG` / `NYJ`. A map that keys only on `LA` or `NY` will silently swap games. Keep explicit maps both ways (`SHORT_TO_FULL` and `ABBR_TO_FULL`).

### 10. Implied % is not a power ranking

A 78% Thanksgiving cell does not mean that team is 4th in the league. It means the book priced that one game. Power rankings (Part 1) and weekly implied odds (Part 2) answer different questions. For survivor / pick planning, the weekly grid is the one that matches the calendar. For “who is best on paper,” use the dated consensus (`9-1-2026/consensus_power_rankings.csv` for Week 1), not the April–June 17-list unless that is the moment you want.

### 11. Verify with known games before trusting fill rate

Fill rate `545/545` can still be wrong if every cell used the spread fallback. Spot-check at least:

- A big favorite (e.g. SEA −205 vs NE)
- A pick’em / juice both sides (BUF −115 / HOU −105)
- A spread-only game (NYJ @ BUF week 18, no ML)
- One Thanksgiving row and one Christmas row
- One BYE (must be blank)

If those fail, do not ship the CSV.

### 12. Ask mode vs Agent mode

The first script write failed because the session was Ask-only. Implementation has to happen in Agent mode. Documentation can be written anytime; code cannot.

---

## Output contract (weekly CSV)

- First column: full team name, same order as the schedule TSV.
- Columns: `Week 1` … `Week 11`, `Thanksgiving`, `Week 12` … `Week 15`, `Christmas`, `Week 16`–`Week 18`.
- Values: implied win % with two decimals, e.g. `37.04`.
- BYE / no holiday game: empty string, not `0` or `BYE`.
- Two teams in the same game should **not** sum to 100. If they do, you accidentally no-vig’d or used only spreads.

## Planning notes (accuracy)

- Refresh the DK scrape after any trade or line move. The June Garrett/Brown lines are not Week 1 prices.
- Keep the schedule TSV as the source of truth for *when* a team plays; keep DK as the source of truth for *price*.
- If a week has 16 games, you should fill 32 team-cells that week (except byes: 14 games → 28 cells). Holiday weeks fill only the teams that play that day.
- For integral planning (survivor, hedges, opponent parlays), use **this week’s cell**, not season-long rank. A bottom-tier team can still be 70% vs a worse opponent at home.
)
