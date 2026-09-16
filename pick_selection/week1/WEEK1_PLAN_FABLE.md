# Week 1 plan (Fable's cut) — 10 entries

Same tooling as `WEEK1_PLAN.md` (`chug.py` on the posted Circa board, crowd shares from the 2026 projection), independent re-derivation. I compared five seatings before picking one; tables below are the actual runs.

## The book

| team | n | vig-free P(win) | crowd | why |
| --- | ---: | ---: | ---: | --- |
| JAC | 2 | 77.6% | 20.2% | the anchor — highest non-holiday win prob on the slate |
| BAL | 3 | 62.5% | 1.7% | fade, free inventory |
| CIN | 3 | 65.2% | 2.5% | fade, free inventory |
| LV  | 2 | 64.1% | 3.3% | fade, free inventory |

**Zero** on LAC (40.7% crowd, the pile you want to watch fall from across the street) and zero on DET. Zero on every Thanksgiving/Christmas team (SEA, PHI, LAR, PIT, GB, CHI, DAL, KC, BUF, DEN, HOU, DET) — those are ration cards, not groceries.

## The hedge

One ticket. **CLE + IND + TB + MIA**, stake **$124.34** (dec 81.42, ≈ +8042). Cover-sized: hits only if all four picks lose, profit replaces the $10,000 in fees.

That is half the price of the old plan's parlay ($245.95). CLE at +330 is a long lever on the wipeout leg — insurance against a rare event should be priced like a rare event, and here it finally is.

No cover-sized 3-legs (they cost $1,191 cash and drag E[week P&L] another −$115, all to be long the same fire twice). No $10 round-robin sprinkles.

## Why this beats the all-fade book (BAL3 CIN3 TEN2 LV2)

Head-to-head from the enumeration (`chug.py compare` / `hedge`):

| metric | all-fade (prior) | JAC barbell (this) |
| --- | ---: | ---: |
| E[entries alive] | 6.24 | **6.66** |
| P(all 10 alive) | 14.7% | **20.3%** |
| P(wipeout) | 2.0% | **1.0%** |
| E[week fees], naked | −$3,762 | **−$3,336** |
| wipe-parlay stake | $246 | **$124** |
| portfolio mark, favs hold | $10,070 | $10,070 |
| portfolio mark, LAC loses | $17,065 (10 live) | $17,065 (10 live) |
| portfolio mark, JAC loses | **$12,642** (10 live) | $10,114 (8 live) |
| portfolio mark, LAC+JAC lose | $26,042 (10 live) | $20,833 (8 live) |

The trade in one sentence: I sell some of the JAC-dies jackpot (a 22.4% event) to buy ~0.4 extra expected survivors, +5.6 points of P(everyone lives), and a $430 smaller expected fee bleed — because week 1 is not the week you cash, it is the week you build branches. Ten entries are seeds, not lottery tickets; the season model's whole objective is *distinct surviving paths*, and 8–10 live entries entering week 2 is worth more than an extra $2.5k of mark in a world where I'm already up.

TEN was the weakest link in the old book (60.7%, the thinnest favorite of the four) and its opponent (NYJ +120) was the most expensive leg in the old parlay. JAC replaces it with +17 points of win probability, at the cost of standing in a mid-size crowd (20%, not 41%).

## Scenario cheat sheet (sandbox runs)

- **Favorites hold:** 10 live, chip ≈ $1,007, mark ≈ buy-in. Boring, correct.
- **LAC dies, my four hold (17.5%):** field → 11,720, chip $1,706, mark **$17.1k**, all 10 alive.
- **JAC dies, fades hold (22.4%):** 8 live × $1,264 = **$10.1k** mark, week P&L −$2,124. The anchor drowning is the same wave that lifts the other eight boats — roughly a wash, not a disaster.
- **LAC and JAC both die:** 8 live × $2,604 = **$20.8k**.
- **All four picks lose (1.0%):** parlay pays, fee P&L ≈ **$0**.

## What I'm knowingly paying for

1. **JAC is real future inventory.** The projection has JAC as the biggest pile in contest week 12 (34.4%). Burning it on 2 of 10 paths spends some of that. The all-fade book burns only junk (TEN/LV). I accept this: 2 paths, not 10, and week 12 has alternatives (WAS projects 38.8% that week).
2. **Correlation with the crowd on 2 tickets.** When JAC loses I lose entries *and* the field shrinks — I bought a small share of the elevator I'm telling you to avoid. Sized at 2/10 deliberately; the compare run at JAC×3 already sagged the JAC-dies mark to $8.8k (7 live) for only +0.13 expected survivors — past 2 the anchor stops paying for itself.
3. **Model crowd shares, closing-ish lines, independence.** Same caveats as `HEDGE_MONEY.md` §8. Marks are mark-to-market, not withdrawable.

## Ticket list

```
Entries:  JAC, JAC, BAL, BAL, BAL, CIN, CIN, CIN, LV, LV
Parlay:   CLE + IND + TB + MIA @ ~+8042, stake $124.34
Total at risk this week: $10,124.34
```

Verify or re-plug: `chug.py compare/hedge/cover/chip/sandbox --picks JAC:2,BAL:3,CIN:3,LV:2`.
