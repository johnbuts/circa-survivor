# Circa Survivor 2026 Week 1 — previous winners in the field

Source PDF: [`raw__pdf/Circa-Survivor-2026-Week-1-Selections.pdf`](raw__pdf/Circa-Survivor-2026-Week-1-Selections.pdf) (dated 09/12/26, 113 pages).  
Parser: [`parse_week1.py`](parse_week1.py) → [`parsed/week1_entries.csv`](parsed/week1_entries.csv), [`parsed/winner_matches.csv`](parsed/winner_matches.csv), [`parsed/week1_pick_share.csv`](parsed/week1_pick_share.csv).

**Scope:** official last-standing / pot-splitters only (Circa Survivor, not Circa Million). A handle counts as “back” if the 2026 owner name matches the winning handle after stripping case, spaces, and punctuation (`On Top 247` = `ONTOP247`), plus one documented one-letter rename (`PLAYIN N STAYIN` → `PLAYIN N STAYING`).

---

## Headline

**27 of 57 official winning handles are in the 2026 Week 1 field**, across **227 entries**.

The first pass used space-preserving equality and missed five returning champs who only changed spacing (`Artie Blanco` → `ARTIEBLANCO`, `On Top 247` → `ONTOP247`, etc.). Those are in the count now. The PDF scrape itself was already complete — see [Parser audit](#parser-audit).

| Season | Official winning owners | Back in 2026 | Missing |
| --- | ---: | ---: | ---: |
| 2020 (35-way / 33 owners) | 33 | 9 | 24 |
| 2021 | 5 | 1 | 4 |
| 2022 | 2 | 2 | 0 |
| 2023 | 4 | 4 | 0 |
| 2024 | 8 | 7 | 1 (`TY1823`) |
| 2025 | 5 | 4 | 1 (`KICK YOUR KNEES UP`) |
| **Total** | **57** | **27** | **30** |

Recent champs mostly reran. Four of five 2021 millionaire handles are gone; Billy Chippas is back as `ONTOP247` with two tickets. The inaugural 2020 chop is still mostly gone (9 of 33).

The 2026 board itself is **24,999 entries / 6,114 owners**, not the 20,000 the hedge notes assumed. At $1,000 a ticket that is a **$24.999M** entry pool before Circa’s posted prize rules.

---

## Official winners, 2020–2025

Circa Survivor started in **2020** (not 2019). Every season ended in a multi-way chop — there has never been a sole survivor. Local PoolGenius `survived_to_end` in [`model_crafting/data/out/entry_picks.csv`](../model_crafting/data/out/entry_picks.csv) matches Circa / Review-Journal / PR Newswire payout lists in every year.

| Season | Split | Pot / each | Winning handles |
| --- | --- | --- | --- |
| 2020 | 35 entries / 33 owners (18–0) | $2.39M / $68,285.71 | `* THE NUT SQUIRRELS`, `7- Out`, `Artie Blanco`, `BALD RAZORS`, `BOBBYT`, `BOYCOTT 8 PCT`, `CLARKGRIZWOLD`, `COLTS45`, `DaliBones`, `EX-FINANCE`, `Golfing in Hell`, `JakestroJans`, `Joncon16`, `LoveMyBaxter` (×2), `MK INVEST`, `Mucked Nuts.`, `PICKSWCLARS24`, `PLAYIN N STAYIN`, `PRESENCE`, `Pauline Park`, `Practice Squad QB`, `ROBERTRUTTER`, `Rip Wheeler`, `SHAMWOW.`, `Slick Rick11`, `Staying Alive`, `Sting`, `THAWK`, `TIM'S SUNSCREEN` (×2), `Texas Bound.`, `WHAT IS FOOTBALL?`, `WHERE'S LUNCH`, `pointsonthepackage` |
| 2021 | 5 | $7.0M ($1.53M or $1.20M) | `MYCOOL`, `On Top 247`, `RETURN OF SURVIVOR`, `SYRACUSE HAWKEYES`, `CHRIS PIPER` |
| 2022 | 2 | $6.133M / $3,066,500 | `BROWNA`, `JED` |
| 2023 | 4 | $9.267M / $2,316,750 | `CIRCUS MASTER`, `IndianaJet`, `JAX JAGS`, `LAJONESER` |
| 2024 | 8 | $14.266M / $1,783,250 | `C3 Picks`, `DREAM STAKES`, `MEATBALL BROTHERS`, `PUMBAPACK9`, `TY1823`, `VODKA JOHNNY`, `WHATEVERYALLWANT`, `Whiskey Business` |
| 2025 | 5 | $18.718M / $3,743,600 | `DYLAN W`, `GaryA`, `JUICY KEWCHI`, `KICK YOUR KNEES UP`, `REAL BRO` |

Published identities (press, not the PDF):

- **2021:** Michael Sax (`MYCOOL`), Billy Chippas (`On Top 247`), Jeremiah Quinn (`RETURN OF SURVIVOR`), Marc Perlman (`SYRACUSE HAWKEYES`), Chris Piper (`CHRIS PIPER`).
- **2022:** Alex Brown (`BROWNA`); Jeremy Wien / Jeff Abraham / Russell Rosenblum / Mike Buchmiller (`JED`).
- **2023:** Harold Gernsbacher (`CIRCUS MASTER`), Robert Brandt (`IndianaJet`), Kyle Motes & Corey Menter (`JAX JAGS`), Greg Jones (`LAJONESER`).
- **2024:** Chris Dierkes (`C3 Picks`); Zheng Fan & Brian Wood (`DREAM STAKES`); Paul Czyz + partners (`MEATBALL BROTHERS`); Steve Sammarco / Goncalvez / Pellegrino (`PUMBAPACK9`); Jeremy Mintz (`WHATEVERYALLWANT`); Sean Singewald & Chris Pike (`Whiskey Business`). `TY1823` and `VODKA JOHNNY` stayed alias-only.
- **2025:** Dylan Wilkerson & Shannon Schorr (`DYLAN W`); Gabe Patgorski / Fernanda Carriedo / Jason Somerville syndicate (`JUICY KEWCHI`); Casey Diener & Joey Michael (`REAL BRO`); `KICK YOUR KNEES UP` is an anonymous woman; `GaryA` was not named in Circa’s PR.

Gabe Patgorski is the only well-documented **two-time Circa Survivor champion** (2021 + 2025), but he did **not** reuse `MYCOOL`. His 2025 handle `JUICY KEWCHI` is the one in this PDF.

---

## Who is back

Casing in the PDF often differs from the payout handle. Matches below are after normalization; `matched_owner` is the 2026 spelling.

### 2025 champs (4 of 5)

| Handle | 2026 name | Entries | Week 1 book |
| --- | --- | ---: | --- |
| `DYLAN W` | `DYLAN W` | 10 | **Jaguars 10** — all-in on the chalk |
| `GaryA` | `GARYA` | 10 | Steelers 6, Chargers 4 |
| `JUICY KEWCHI` | `JUICY KEwchi` | 10 | Bengals 4, Bears 3, Vikings 2, Raiders 1 |
| `REAL BRO` | `REAL BRO` | 10 | **Chargers 10** — all-in on the other chalk |
| `KICK YOUR KNEES UP` | — | 0 | Not in the field |

`JUICY KEWCHI` fades the three chalk teams. Four Bengals / three Bears is a deliberate anti-crowd book from the Patgorski group. `Love My Baxter` (2020) does the same with 10 Eagles.

`KICK YOUR KNEES UP` (anonymous 2025 winner) did not come back under that name.

### 2024 champs (7 of 8)

| Handle | 2026 name | Entries | Week 1 book |
| --- | --- | ---: | --- |
| `C3 Picks` | `C3 Picks` | 10 | **Steelers 10** |
| `DREAM STAKES` | `DREAM STAKES` | 10 | Steelers 4, Jaguars 4, Raiders 2 |
| `MEATBALL BROTHERS` | `MEATBALL BROTHERS` | 10 | Chargers 4, Jaguars 4, Raiders 2 |
| `PUMBAPACK9` | `PUMBAPACK9` | 10 | Steelers 4, Eagles 2, plus one each Titans / Jaguars / Chargers / Raiders |
| `VODKA JOHNNY` | `VODKA JOHNNY` | 10 | Chargers 4, Jaguars 3, plus Raiders / Lions / Steelers |
| `WHATEVERYALLWANT` | `WhateverYallWant` | 10 | Steelers 7, Jaguars 2, Raiders 1 |
| `Whiskey Business` | `WHISKEY BUSINESS` | 6 | Jaguars 3, Chargers 2, Steelers 1 |
| `TY1823` | — | 0 | Not in the field |

Chris Dierkes (`C3 Picks`) and the JED syndicate both parked **all ten** on Pittsburgh. That is the third-most-owned team (16%), not the two chalk sides.

### 2023 champs (all 4)

| Handle | 2026 name | Entries | Week 1 book |
| --- | --- | ---: | --- |
| `CIRCUS MASTER` | `CIRCUS MASTER` | 4 | Steelers 2, Vikings 1, Jets 1 |
| `IndianaJet` | `INDIANAJET` | 7 | Eagles 3, Steelers 3, Jaguars 1 |
| `JAX JAGS` | `JAX JAGS` | 10 | Jaguars 4, Chargers 4, Steelers 2 |
| `LAJONESER` | `LAJONESER` | 10 | **Chargers 8**, Raiders 1, Jaguars 1 |

Greg Jones (`LAJONESER`) has entered every year since inception; he is back with a full ten and is the most chalk-heavy 2023 champ.

### 2022 champs (both)

| Handle | 2026 name | Entries | Week 1 book |
| --- | --- | ---: | --- |
| `BROWNA` | `browna` | 10 | Steelers 3, Jaguars 2, Chargers 2, Dolphins 1, Lions 1, Bears 1 |
| `JED` | `JED` | 10 | **Steelers 10** |

`browna` is the most diversified returning winner: six different teams, including a Dolphins ticket (27 people in the whole field picked Miami).

### 2021 champs (1 of 5)

| Handle | 2026 name | Entries | Week 1 book |
| --- | --- | ---: | --- |
| `On Top 247` | `ONTOP247` | 2 | Jaguars 1, Chargers 1 |
| `CHRIS PIPER` | — | 0 | Last in the historical file in 2024 |
| `MYCOOL` | — | 0 | Last in 2022 |
| `RETURN OF SURVIVOR` | — | 0 | 2021 only |
| `SYRACUSE HAWKEYES` | — | 0 | Played 2025 (so they *did* come back once), skipped 2026 |

`ONTOP247` is the same compact string Chippas has used every year since 2022 (10 entries in 2023–2025). This year he cut to two tickets, both on chalk.

`HAWKEYE PICKS` / `HAWKEYE7374` are on the 2026 board. They are not `SYRACUSE HAWKEYES`.

Official 2021 payout names are Sax / Chippas / Quinn / Perlman / Piper. Patgorski’s documented 2025 handle is `JUICY KEWCHI` (present). Some outlets call him a two-time champ; that is a person-level claim, not a handle reuse. **`MYCOOL` and `RETURN OF SURVIVOR` are both absent.**

### 2020 chop (9 of 33)

| Handle | 2026 name | Entries | Week 1 book |
| --- | --- | ---: | --- |
| `BALD RAZORS` | `Bald Razors` | 10 | Jaguars 4, Chargers 4, Steelers 1, Raiders 1 |
| `Mucked Nuts.` | `MUCKED NUTS` | 10 | Jaguars 4, Chargers 3, Steelers 3 |
| `TIM'S SUNSCREEN` | `Tim's Sunscreen` | 10 | Chargers 5, Jaguars 5 |
| `pointsonthepackage` | `POINTSONTHEPACKAGE` | 5 | Steelers 2, Chargers 2, Jaguars 1 |
| `PLAYIN N STAYIN` | `PLAYIN N STAYING` | 6 | Chargers 2, Steelers 2, Jaguars 2 |
| `Artie Blanco` | `ARTIEBLANCO` | 4 | Jaguars 2, Chargers 1, Steelers 1 |
| `BOBBYT` | `BOBBY T` | 10 | Jaguars 6, Chargers 2, Lions 2 |
| `LoveMyBaxter` | `Love My Baxter` | 10 | **Eagles 10** — full fade of JAC/LAC/PIT |
| `Slick Rick11` | `SLICK RICK 11` | 3 | Jaguars 3 |

`PLAYIN N STAYING` adds a G (`STAYIN` → `STAYING`). Same owner: six entries every year 2020–2025 under `PLAYIN N STAYIN`, six again in 2026.

The four spacing-only names (`ARTIEBLANCO`, `BOBBY T`, `Love My Baxter`, `SLICK RICK 11`) are the same people in `owner_summary.csv` — they have used those compact strings for years. `Love My Baxter` has entered every season since 2020.

The other 24 inaugural winners are gone under those names, including the Jeff Whitelaw group `WHERE'S LUNCH`. `SHAMWOW` and `Practice Squad QB` were still in the 2025 file and did not show up in 2026.

---

## Who is missing (and why it matters)

**Four of five 2021 millionaires** left the board. Chippas (`ONTOP247`) is the exception, and he only put in two tickets.

**`TY1823` (2024)** and **`KICK YOUR KNEES UP` (2025)** are the only post-2021 champs absent. The latter was anonymous in the Review-Journal writeup; a new alias would be invisible to handle matching. `TY1823` last appears in the 2024 historical file.

**`PARTZ1` / Pete Tarsiewicz** is not in the 2026 PDF. He went 19–1 in both 2024 and 2025 (died on Falcons, then Bengals) and told Yahoo he would enter again. Either he did not, or he renamed.

Handle matching cannot catch a champ who came back as a new string. Syndicates (Hall, Patgorski, Meatballs) routinely split equity across names.

---

## Week 1 field — what the PDF actually is

| | |
| --- | --- |
| Entries | **24,999** |
| Unique owners | **6,114** |
| Max entries / owner | 10 (Circa cap) |
| Owners with 10 entries | 1,227 |
| One-and-done owners | 1,910 |

Ghostscript + the pair regex recovered **every entry cell**. 24,999 unique `OWNER-N` aliases, leftover line text empty, team numbers internally consistent (Jaguars are always `6.`, Chargers `22.`, Steelers `12.`, etc.). The raw extract has 25,000 `PK` tokens; the extra one is the owner name `WEST TEXAS PK`, not a dropped row. So 24,999 is the field, not 25,000 minus a scrape bug.

### Actual Week 1 pick share

| Team | Entries | Share | vs pre-season model (`pick_projections_2026` wk1) |
| --- | ---: | ---: | --- |
| Jaguars | 8,127 | **32.51%** | model had JAC ~20% |
| Chargers | 7,585 | **30.34%** | model had LAC **40.7%** |
| Steelers | 4,013 | **16.05%** | |
| Lions | 1,771 | 7.08% | model had DET **16.2%** |
| Raiders | 1,308 | 5.23% | |
| Eagles | 784 | 3.14% | |
| Bengals | 351 | 1.40% | |
| Everyone else | 1,060 | 4.24% | |

Three teams are **78.9%** of the field (JAC + LAC + PIT). The live crowd inverted the model: Jacksonville is the chalk, not the Chargers, and Detroit was faded hard (7% vs 16%).

The Sep 9 portfolio in [`pick_selection/PROCESS.md`](../pick_selection/PROCESS.md) is **LAR 6 / DAL 2 / KC 2**. Actual shares: Rams 49 (0.20%), Cowboys 81 (0.32%), Chiefs 23 (0.09%). That book sits off a packed elevator — 24,827 of 24,999 entries are somewhere else.

Hedge notes still size the pot at **$20M / 20,000 start**. The PDF says the start is **25k**. Dead-entry math and “$20M / field_alive” both move if the posted prize stayed at the $20M guarantee instead of tracking the $25M entry pool. Worth confirming against Circa’s 2026 prize page before trusting EV from the 20k assumption.

---

## How returning winners are picking vs the crowd

227 winner-handle entries, vs the field’s 32.5 / 30.3 / 16.1 JAC–LAC–PIT split:

| Their Week 1 team | Winner-handle tickets | Their share | Field share |
| --- | ---: | ---: | ---: |
| Jaguars | 63 | 27.8% | 32.5% |
| Steelers | 62 | 27.3% | 16.1% |
| Chargers | 59 | 26.0% | 30.3% |
| Eagles | 15 | 6.6% | 3.1% |
| Raiders | 10 | 4.4% | 5.2% |
| Lions | 4 | 1.8% | 7.1% |
| Bears | 4 | 1.8% | 0.5% |
| Bengals | 4 | 1.8% | 1.4% |
| Other | 6 | 2.6% | — |

Returning winners as a group are still **overweight Pittsburgh** and **underweight Jacksonville**. Eagle share doubled vs the field because `Love My Baxter` put all ten on Philadelphia. The Steelers pile is a few all-10 books (`JED`, `C3 Picks`, `WHATEVERYALLWANT` 7-of-10) plus `GaryA` 6-of-10.

Three all-in stacks sit on single teams: `DYLAN W` 10× Jaguars, `REAL BRO` 10× Chargers, `Love My Baxter` 10× Eagles. If JAX or LAC dies Week 1, a recent champ’s entire stack dies with it.

Two returning winners faded the three chalk teams entirely: `JUICY KEWCHI` (Bengals / Bears / Vikings / Raiders) and `Love My Baxter` (Eagles only).

---

## Notable non-winners still on the board

Not official splitters; still useful context.

| Handle | Why they matter | 2026 |
| --- | --- | --- |
| `THE ENEMY WITHIN` | 2022 finalist, 19–1 (Mike Barth). Died Week 18 after a three-way partial chop with `BROWNA` / `JED`. | **10 entries** — Jaguars 6, Steelers 2, Chargers 2 |
| `PAYDATMANHISMONEY` | 2024 deep run (`max_exit_week` 20 in owner history; not a splitter). | **7 entries** — Jaguars 5, Raiders 1, Steelers 1 |
| `PARTZ1` | 19–1 in 2024 **and** 2025; last 2025 body out (Bengals). | **Absent** |

---

## Repeat-person caveats

1. **Same person, new handle** is invisible. Patgorski already did this once (`JUICY KEWCHI` ≠ `MYCOOL` / `RETURN OF SURVIVOR`).
2. **Galen Hall** said he had equity in two 2025 winning entries and would not name them. Forum guesses (`GaryA`, `DYLAN W`) conflict with press IDs. `GARYA` and `DYLAN W` are both back; that does not prove Hall owns them.
3. **Casey Diener** (`REAL BRO`) is reported to have had a piece of an inaugural-era winning ticket — possible two-time person under different names.
4. `PLAYIN N STAYING` is treated as the 2020 `PLAYIN N STAYIN` owner (six tickets every year, then six again). If that is a different person, drop one from the 27.
5. Compact matching does **not** merge unrelated lookalikes. Rejected on purpose: `COLT 45'S` ≠ `COLTS45`, `THE SQUIRRELS` ≠ `* THE NUT SQUIRRELS`, `Survivor` ≠ `RETURN OF SURVIVOR`, `STINGRAY` ≠ `Sting`, `SLICK RICKS PICKS` ≠ `Slick Rick11`, `HAWKEYE PICKS` ≠ `SYRACUSE HAWKEYES`, `UNCLEARTIE` ≠ `Artie Blanco`.

`JED` is matched only as compact `JED` (ten Steelers tickets). No other 2026 owner compact-equals `JED`.

### Possible, not counted

`STAY IN ALIVE` (10 tickets: Chargers 4, Jaguars 3, Lions 3) is one letter off `Staying Alive` (`STAYINGALIVE` vs `STAYINALIVE`). The 2020–21 winner used `Staying Alive`; a `STAYINALIVE` owner shows up in 2025 (10 entries, out week 9) and again in 2026. Could be the same person dropping the G, or a copycat Bee Gees joke. **Not in the 27.**

---

## Parser audit

The scrape is complete. The first-pass **matcher** was not.

`parse_week1.py` shells `gs -sDEVICE=txtwrite` on the Circa PDF, then pulls every `OWNER-(1–10)` + `##. TEAM PK` pair.

| Check | Result |
| --- | --- |
| Unique aliases | 24,999 |
| Leftover text after regex | none |
| Entry-number holes (owner has `-3` but no `-2`) | none |
| Team-number splits (same team, two jersey #s) | none |
| Raw `\bPK\b` tokens | 25,000 — extra is owner `WEST TEXAS PK` |
| Names ending in `-` / empty owners | none |
| `49ERS` (digit-leading team) | 10 tickets; letters-only team class would have dropped them |

The PDF is three newspaper columns. Long aliases collide with the pick (`THEABSOLUTEGOVERNORS-122. CHARGERS PK`). The regex takes the last `-(1–10)` before the team number, which also fixes `…-1012. STEELERS` → entry 10 on the Steelers.

What was **not** ideal: matching on spaced uppercase, so `On Top 247` missed `ONTOP247`. Matching is now alphanumeric-compact. `PLAYIN N STAYIN` → `PLAYIN N STAYING` is still a hand variant (extra G). A champ who came back as a totally new string is still invisible.

Rerun:

```bash
python3 all_picks_2026/parse_week1.py
```

---

## Sources

- Circa winner PDFs: [2023](https://www.circasports.com/wp-content/uploads/2024/01/Circa-Survivor-2023-Winners.pdf), [2024](https://www.circasports.com/wp-content/uploads/2025/01/Circa-Survivor-2024-Winners.pdf), [2025](https://www.circasports.com/wp-content/uploads/2026/01/Circa-Survivor-2025-Winners.pdf)
- [Circa 2021 recap](https://www.circasports.com/blog/2021-circa-sports-football-contest-recap), [2022 recap](https://www.circalasvegas.com/blog/2022-circa-sports-football-contest-recap/)
- Review-Journal: [2020 35-way](https://www.reviewjournal.com/sports/betting/circa-survivor-winner-relishes-run-to-perfect-18-0-nfl-season-2242497/), [2022](https://www.reviewjournal.com/sports/betting/definitely-got-very-lucky-circa-survivor-winners-tell-6-1m-story-2712582/), [2023](https://www.reviewjournal.com/sports/betting/circa-survivor-winners-share-their-nerve-wracking-9-2m-story-2981394/), [2024 Meatballs](https://www.reviewjournal.com/sports/betting/from-meatballs-to-millions-circa-survivor-winners-share-14-3m-story-3260714/), [2025 $18.7M](https://www.reviewjournal.com/sports/betting/unlv-nursing-student-poker-pros-split-18-7m-circa-survivor-prize-3604182/)
- [PR Newswire Jan 2026](https://www.prnewswire.com/news-releases/circa-sports-pays-out-over-31-million-in-2025-2026-professional-football-contests-302655612.html)
- [Yahoo — PARTZ1](https://sports.yahoo.com/nfl/betting/article/the-result-is-the-result-the-story-of-the-circa-nfl-survivor-contestant-who-lost-on-the-final-week-each-of-the-past-two-years-204738159.html)
- [ESPN 2026 contest weekend](https://www.espn.com/espn/betting/story/_/id/49785676/nfl-survivor-betting-circa-sportsbook-las-vegas-2026)
- Local: `model_crafting/data/out/entry_picks.csv` (`exit_reason=survived_to_end`), `model_crafting/data/out/week_summary.csv`
