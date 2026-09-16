# How hedging can (and cannot) make money in Circa Survivor

Week 1, 2026 slate. This is not a pick list. It is a report on the *mechanism*: where cash comes from, what a hedge actually is, and what the numbers do when you try the usual recipes.

Audience: CS / math bachelor. One simile per idea, then the equation.

Generated numbers are from an exact enumeration of all **65,536** week-1 winner combinations (`hedge_econ.py`). Probability of a world is the product of vig-free Circa win probabilities, games independent. Parlay *payouts* use posted Circa decimals, juice included. Crowd shares are the already-run 2026 projection (LAC 40.7%, JAC 20.2%, DET 16.2%). Buy-in is **10 entries × $1,000 = $10,000**. Pot **$20M**, field start **20,000**.

---

## 1. Punchline

Hedging is not a money printer. It is a fire extinguisher you buy from Circa’s parlay desk.

The sportsbook side of the trade has **negative expected value** in every book we ran. That is juice: you are betting Circa’s prices while the world is generated from the fair (vig-free) probabilities implied by those same prices. A parlay is a bundle of slightly unfair coins. Bundle more coins, pay more juice.

The money, if there is any, sits in the *other* building on the same lot: the survivor pool. Your live tickets are a claim on $20M / (how many entries are still alive). When the crowd’s teams lose, that denominator shrinks and each live ticket inflates. Fading 40% of the field is like standing off to the side of a packed elevator: if the cable snaps, you are not in it.

So the general way to “make money on hedging” is:

1. **Put your entries where the crowd is not**, so a chalk death pays you in chip size.
2. **Buy the smallest insurance that covers the fee wipeout you cannot stomach.**
3. **Do not stack cover-sized round-robin legs on top of a cover-sized wipeout parlay.** Those extra legs all hit in the same fire, so you are long disaster twice.

If you skip (1) and only do (2)–(3), you are a well-insured person sitting in the elevator.

---

## 2. Two cashiers, one weekend

Write wealth after week 1 as

```
W = (parlay payout − parlay stake) + (entries still alive) × chip − $10,000
```

with `chip = $20,000,000 / field_alive` and `field_alive = 20,000 × (sum of projected crowd share on winning teams)`.

That is two cashiers:

| cashier | what you buy | how they get paid |
| --- | --- | --- |
| **Parlay desk** | opponents of your pick teams | Circa juice on moneylines |
| **Survivor pool** | 10 claims on $20M | other entries dying |

The first cashier is a vending machine with a 5–10% markup on the snacks. The second is a pie that gets recut every Sunday. Hedging talks to cashier 1. Profit talks to cashier 2.

`chip` is **mark-to-market**, not a wire to your bank. You cannot sell a live Circa entry at $20M / alive. Treat `W` as “what the ticket is worth if the rest of the contest paid out tonight,” which is the right *relative* score for comparing hedges, and the wrong number to spend.

---

## 3. What the slate is doing (no picks involved)

If every Circa favorite wins, crowd share remaining is **99.30%**, field **19,860**, chip **$1,007** — basically the $1,000 fee back, like buying a $1 soda and getting $1.01 in pennies.

Unconditional E[chip] across all 65,536 worlds is **$1,493**, because chip is a mixture with a fat right tail:

| condition | P | E[chip] |
| --- | ---: | ---: |
| LAC, JAC, DET all win | 48.2% | **$1,095** |
| at least one of those three loses | 51.8% | **$1,863** |
| LAC loses | 17.5% | **$2,714** |

LAC is 40.7% of the projected field and only a **17.5%** underdog to lose. That is the whole shape of week 1: a coin that is not fair, with a jackpot glued to the rare side. Fading LAC is buying that jackpot. Riding LAC is selling it.

P(JAC loses) = 22.4%, P(DET loses) = 24.7%. Independent under this model, P(all three chalk teams win) = 48.2%. About half the weekends the elevator cable holds; about half it doesn’t. The *size* of the drop is not half-and-half: LAC falling is the big one.

---

## 4. Six books, no inherited picks

Same 10 entries, six different ways to seat them. None of these is “the original board.”

| book | seating | E[alive] | P(all 10 dead) | E[chip portfolio] | E[W] vs $10k | P(W>0) | 5th percentile |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all chalk | LAC×10 | 8.25 | 17.5% | $10,179 | **+$179** | 82.4% | −$10,000 |
| chalk split | LAC×6 JAC×4 | 8.06 | 3.9% | $10,270 | **+$270** | 71.2% | −$2,819 |
| two-team fade | SEA×5 BAL×5 | 6.32 | 13.6% | $9,312 | **−$688** | 45.5% | −$10,000 |
| three-team fade | SEA×4 BAL×3 CIN×3 | 6.38 | 4.7% | $9,394 | **−$606** | 38.6% | −$6,859 |
| four-team fade | SEA×3 BAL×3 CIN×2 PHI×2 | 6.45 | 1.5% | $9,439 | **−$561** | 36.1% | −$7,218 |
| five-team fade | SEA×2 BAL×2 CIN×2 PHI×2 LAR×2 | 6.50 | 0.5% | $9,529 | **−$471** | 35.5% | −$5,754 |

Read this like cache vs throughput.

**Chalk has a positive week-1 mark.** You survive 82.5% of the time with ten identical tickets. When LAC wins, other people’s JAC/DET can still die, so your ten claims are worth a little more than $1,000 each. Mean `W` is +$179. The 5th percentile is **−$10,000**: when LAC loses you are a row of zeros. You also *are* the field. Ten LAC tickets in a 40.7% pile is like cloning yourself in that elevator. Week 2 you still have not beaten anyone.

**Fade has a negative week-1 mark** of about −$500 to −$700. You die more often on your own games (SEA/BAL are ~63% favorites, not 82%). Most weekends the crowd’s favorites also win, chip stays ~$1,100, and you are down entries. The payoff is the other column: **E[W | LAC loses] ≈ +$6,700 to +$7,100** on every fade book. That is the jackpot. You cannot collect it if you were on LAC.

**Splitting chalk (LAC+JAC)** is the only book here that is both slightly +EV on the mean *and* not fully wiped by a single LAC loss (5th pct −$2,819). You still own ~60% of the two biggest piles. The pie barely recuts when you survive.

Diversifying a *fade* book (2 teams → 5) does three things, all mechanical:

- P(wipeout) falls: 13.6% → 0.5% (independent games, product of complements).
- E[alive] rises a little (6.32 → 6.50).
- E[W] rises a little (−$688 → −$471) because you throw away fewer full-fee disasters.

That is not magic. It is `1 − ∏ P(team loses)` going down. The cost is burning more distinct teams, which matters for Thanksgiving / Christmas later. This report does not price that.

---

## 5. Hedge recipes, with numbers

A **k-leg** is a parlay on the *opponents* of k of your pick teams. It hits when those k picks all lose.

**Cover sizing** sets the stake so that if the ticket hits, profit equals the fees on the entries those legs would kill:

```
stake = (dead_entries × $1,000) / (decimal − 1)
```

The n-leg with `dead_entries = 10` is the wipeout cover. A 3-leg uses only the counts on those three picks.

### 5.1 Naked (no tickets)

This is the baseline. Mean `W` is whatever the book does. Tails are whatever P(wipe) is. Like leaving the extinguisher in the truck: zero juice, full fire.

### 5.2 Wipeout parlay only (the actual insurance)

One n-leg, cover-sized.

On the **four-team fade** (SEA/BAL/CIN/PHI):

| | naked | wipe |
| --- | ---: | ---: |
| cash risked | $0 | $182 |
| E[hedge net] | $0 | **−$27** |
| E[W] | −$561 | −$588 |
| 5th percentile | −$7,218 | −$6,788 |
| P(W>0) | 36.1% | 34.4% |
| E[W \| LAC loses] | +$6,879 | +$6,852 |

You pay **$27 of expectation** (juice) to lift the left tail a few hundred dollars and to make the all-dead row net to about **$0 on the parlay** instead of −$10,000 of fees. The jackpot column barely moves. That is what good insurance looks like: a small mean haircut, a less ugly ruin.

On the **two-team fade**, the wipe parlay is more expensive because two underdogs parlayed are not longshots stacked four deep: stake **$1,721**, juice **−$132**, 5th percentile from −$10,000 to **−$6,419**. Still insurance. Just a fatter premium, because a 2-leg hits more often than a 4-leg, so Circa’s juice has more surface area.

On **LAC×10** there is no n-leg parlay (one game). The analogue is a straight bet on ARI at +450, sized to cover $10k: stake **$2,222**, E[net] **−$83**. Same story, one coin.

### 5.3 Cover-sized 3-legs (partial death)

Pays when three of your pick teams lose. On four-team fade: 4 tickets, **$1,549** risked, E[hedge net] **−$174**, E[W] **−$736**. The 5th percentile *improves* to −$6,179 versus naked −$7,218, because those “three dead, one live” rows get a check. You paid 6× the wipe juice for a smoother 3-loss band.

Like installing sprinklers in four rooms. Better than nothing in a kitchen fire. You still pay the plumber every week the kitchen does not burn.

### 5.4 Wipe + 3-cover stacked (the trap)

On four-team fade: 5 tickets, **$1,730** risked, E[hedge net] **−$201**, E[W] **−$763**. Worst of both: more juice than wipe alone, and when *all four* lose **every 3-leg and the 4-leg hit together**. Subset parlays are not extra independent insurance. They are the same fire, more nozzles.

On a related 4-team book the stacked cover can print **+$30,000** on the wipeout row. That is not a feature. That is being long the ashes. You spent extra juice all year so that the one weekend everything dies, Circa pays you a multiple of the fees you already lost. Unless your utility function is “I want a yacht if my contest dies,” do not do this.

### 5.5 Tiny round-robin (HTML Fill / Split)

`rr3+4` at $10/ticket on four-team fade: **$50** risked, E[hedge net] **−$6**, E[W] **−$567** vs naked **−$561**. A rounding error. It does not cap ruin. It is like tipping a dollar on each insurance form so you feel involved. Harmless, not a strategy.

### 5.6 Cover-sized 2-legs (overhedge)

On four-team fade: 6 tickets, **$4,675** at risk — almost half the buy-in — juice **−$358**, E[W] **−$919**, 5th percentile **worse** than naked (−$7,221). Two-legs hit often. Cover-sizing them puts real money on events that are not rare. You are no longer buying catastrophe insurance. You are running a second sportsbook account against yourself.

Same pattern on five-team fade: 2-cover juice **−$467**, worst mean of the menu.

---

## 6. The only comparison that matters for “making money”

Hold the four-team fade book fixed. Look at E[W] if the crowd’s elevator falls vs if it holds:

| hedge | E[W] | E[W \| chalk holds] | E[W \| LAC loses] |
| --- | ---: | ---: | ---: |
| naked | −$561 | −$3,009 | **+$6,879** |
| wipe | −$588 | −$3,036 | **+$6,852** |
| rr3+4 $10 | −$567 | −$3,015 | +$6,873 |
| 3cover | −$736 | −$3,184 | +$6,705 |
| wipe+3 | −$763 | −$3,210 | +$6,678 |
| 2cover | −$919 | −$3,367 | +$6,521 |

The jackpot column is ~$6.8k whether you hedge or not, until you start lighting money on fire with 2-covers. The hold column is ~−$3k, which is “chip stayed near a grand and you still dropped some of SEA/BAL/CIN/PHI.” Hedging cannot flip that. Only a different seating (being on LAC) flips it — and then the LAC-loses column becomes **−$10,000** (all chalk) or **−$3,112** (LAC×6 JAC×4).

So:

- **Want the +$6.8k when LAC dies?** Don’t sit on LAC. Hedge does not create that. Seating does.
- **Want to not go to zero when your own four games all lose?** Buy the 4-leg. It costs ~$27 of EV.
- **Want a higher mean than fade?** Sit on chalk, accept that you *are* the field, and that week-1 `W` is a mark you cannot cash.

---

## 7. A general strategy (week 1, then the contest)

Think of three layers, like a network stack. Do not mix layers.

**Layer 0 — seating (this is the edge, if any).**  
Put entries on teams with real win probability and small crowd share. That is `log P(win) − λ log(crowd)` in the HTML. The sim’s fade books are that idea made crude (SEA/BAL/CIN/PHI/LAR, crowd 0.5–6%). This is the only layer that can make `E[W | LAC loses]` large. Hedging never substitutes for it.

**Layer 1 — catastrophe (this is the hedge).**  
One parlay: every opponent, cover-sized to `N × fee`. For four independent-ish favorites that parlay is cheap (~$180) and rarely hits, so juice is small. For two teams it is expensive (~$1,700). For one team it is a straight dog. If you cannot describe the ticket in one sentence (“ARI+NYJ+… hits iff every pick died”), it is not this layer.

**Layer 2 — vanity (optional, cap it).**  
A few small round-robin tickets so a 3-loss weekend is not a full fee bleed. Stake them like a bar tab, not like cover. `rr3+4` at $10–$25 is this. Cover-sized 2-legs and stacked wipe+3 are Layer 2 pretending to be Layer 1. The sim charges you hundreds of dollars of EV for the costume.

**Do not** use Layer 1 to “get extra upside on wipeout.” Wipeout already returns your fees if you sized it. Extra upside on wipeout is a side bet that the contest failed. That is a different hobby.

---

## 8. Caveats a bachelor should actually care about

1. **Independence.** Worlds are `∏ p_g`. Real Sundays share weather, news, and “the league is on tilt.” Wipeout probabilities are a lower bound on how clustered deaths can be. Juice estimates are still the right *sign*.

2. **Vig-free Circa ≠ truth.** We used Circa to both generate worlds and pay parlays, with juice only on the pay side. If Circa is mispriced versus the true NFL, that is a *football* edge, not a hedge-structure edge. This report assumes you have none.

3. **Crowd shares are a model.** LAC at 40.7% is a projection, not a live count. If the real field is 55% on LAC, the jackpot is bigger and fade’s week-1 mean looks worse (more weekends the chip stays tiny). If the real field is 25% on LAC, fade’s jackpot shrinks.

4. **`W` is not cash.** Chip is a 19-week option. Ten correlated LAC tickets that “mark” at +$179 after week 1 are still one injury report from a mass funeral. Fade’s −$600 mark is the price of not being that blob.

5. **Holiday legs are not in this file.** Burning SEA/BAL/CIN/PHI/LAR in week 1 changes Thanksgiving/Christmas menus. A 5-team fade “wins” week-1 variance and can lose Rule 8/9 later. Price that in the season model, not here.

6. **One-team books cannot buy an n-leg.** Hedge is a straight opponent. The ARI +450 cover on 10×LAC costs ~$83 of EV. Still insurance, still not an edge.

---

## 9. What the numbers say you should do

If the goal is **make money in the pool**, the hedge is a side dish:

1. Seat entries off the 40% pile (and off JAC/DET if you can still find ~60%+ win probability).
2. Buy **one** cover-sized opponent parlay of whatever you actually used.
3. Stop. Maybe sprinkle $50 of round robin if you hate 3-loss weekends as a feeling, not as a mean.

If the goal is **make money from Circa parlays**, these numbers say you will not. Every hedge we sized at cover or at $10/ticket had **E[hedge net] ≤ 0**, usually −$6 to −$350 depending on how many legs you fed the vending machine.

The simile to keep: the parlay desk sells umbrellas. The pool pays people who were not standing in the crowd when it rained. Buy one umbrella. Do not buy a tent, four tarps, and a boat, then stand in the crowd anyway.

---

*Tables: `hedge_econ_tables.md` (raw). Recompute: `python hedge_econ.py` from this folder, using the model venv for numpy. Interactive plug-and-chug: `chug.py hedge`.*
