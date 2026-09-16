# How the Circa Survivor Model Works

This document explains how the Circa Survivor pick model in this repository works: what it models, why each layer exists, and what the numbers mean. It is written for someone with a CS background who is not a statistician.

---

## 1. The reframe: this is not a football model

Survivor *looks* like a football-picking game. It is not.

The football question — who wins Sunday — is already answered by the betting market. You have no edge there. What you *can* model is **people**: how many entries will pick each team, given who is still alive and what each entry has already used.

The framing that drives everything:

> The goal is not to survive. It is to **win**. To win you need other people to lose. Picking a team that 45% of the field also picked means that even when you are right, you have beaten nobody.

So the object being modeled is the **pick distribution**, not game outcomes. Game outcomes enter later only to propagate survival and payouts.

---

## 2. Why entry-level data changes everything

The dataset is every entry’s complete pick history, **2020–2025**: about **53,700** entry-season records (`entry_state.parquet`) and **212,264** individual picks (`picks_long.parquet`). That is not a sample of the contest — it is the full recorded field for those seasons.

### The denominator problem

A naive aggregate is misleading:

- “4% of the pool picked KC this week.”

That is broken because by week 14 most of the pool **cannot** pick KC — they already burned it. Circa Rule 6: each team may be used only once per entry.

So 4% in week 2 and 4% in week 14 mean completely different things. The denominator is not “entries alive” but **entries alive that still have that team available**.

With entry-level data the pipeline computes the exact denominator:

```
eligible(w, T) = entries alive in contest week w that have not already used team T
```

**Implementation (CS angle):** each entry carries a **32-bit burned-team bitmask**. Each pick ORs in the mask for the chosen team. Eligibility for team `T` is an **O(1)** bit test: `(burned & TEAM_MASK[T]) == 0`.

### Endogeneity — why aggregates lie

The deeper problem is **endogeneity** (plain language: the surviving sample is not random).

Entries that still hold KC in week 14 are disproportionately the ones who **planned** to hold KC for week 14. The surviving population is self-selected. Any statistic computed over aggregated cells mixes “how much people like KC” with “who happens to still have KC.”

The fix is not a cleverer aggregate formula. It is to model at the **individual entry** level, where each row’s choice set is explicit and probabilities are normalized over **that entry’s menu** only. That motivates Section 4.

---

## 3. Layer 1 — turning betting lines into probabilities

We need `P(team wins)` from a point spread. The repo fits a one-parameter curve on historical games:

```
P(win) = sigmoid(b · (−spread))
```

With `b ≈ 0.1448` from `winprob_curve.json` / `fitted_model.json` (`winprob_b`).

| Choice | Rationale |
|--------|-----------|
| **No intercept** | Spread 0 must imply exactly 50%. Symmetry is enforced; one fewer parameter and better tail behavior at \|spread\| > 10 than a free intercept. |
| **Fit on data, not σ = 13.5** | **1,871** regular-season games in `games.parquet` (non-playoff), fitted once per favorite side. Real calibration beats a guessed normal. |
| **Favorite side only** | Each game appears once from the favorite’s perspective; the underdog row is the complement, not independent evidence. |

This layer is deliberately dumb. It is where we have no edge, so we accept the market’s answer.

---

## 4. Layer 2 — the crowd model (conditional logit)

This is the core.

### Choice sets and softmax

Each **entry × contest week** is one **discrete choice** over a **menu** that differs per entry:

```
C_iw = { teams playing in contest week w } \ { teams entry i already burned }

score(t)     = x_t · β                    # linear utility
P(i picks t) = exp(score(t)) / Σ_{s ∈ C_iw} exp(score(s))
```

That normalization is **softmax** — the same function as a multi-class classifier’s output layer — but over a **variable-length candidate set per row**. If you have implemented softmax over a dynamic list of logits, you already understand the inference step.

### Why conditional logit, not regression on pick %

1. **One pick per week.** Probabilities within each entry-week must sum to 1.
2. **Heterogeneous choice sets.** Everyone’s menu differs (burned teams). Probabilities are normalized over **each entry’s** menu, which dissolves the endogeneity problem from Section 2.

Alternative rejected: regressing `pick_share` on features at the (week, team) level. That treats all entries as exchangeable and reintroduces the wrong denominator.

### Maximum likelihood — plain terms

We have **212,242** choice observations used in fitting (`fit_conditional_logit.log`: observations in groups collapsed from entry-level picks).

**Maximum likelihood** means: search for β that makes the **actual picks as probable as possible** under the model. Concretely, maximize the sum of log-probabilities assigned to the choices that happened. Optimized with **L-BFGS** on a custom NumPy log-likelihood (gradient-based scalar optimization — nothing exotic).

For a CS reader: it is `argmax_β Σ log P(observed_pick | β, choice_set)` with softmax denominators per row.

### What the fitted numbers mean

| Metric | Value (artifact) | Plain reading |
|--------|------------------|---------------|
| Training mean log-likelihood per choice | **−1.877** (`fitted_model.json`, `model_report.md`) | `exp(−1.877) ≈ 0.153` → model assigns ~**15.3%** average probability to the pick that actually occurred |
| Uniform over menu (typical) | ~**−3.31** log-prob → `exp(−3.31) ≈ 3.7%` | Random guessing among ~27 eligible teams |
| **Implied win prob only** (1 feature) | train LL **−1.9998**, LOO **−1.987** (`ablation_report.md`) | `exp(−2.0) ≈ 13.5%` — market alone gets most of the way |
| Deployable spec (11 features) | LOO mean **−1.919** (`ablation_report.md`) | Behavioural features move ~13.5% → ~15.3% assigned prob — **real but modest** |

**Honest summary:** most predictive power is “people pick likely winners.” The rest is scheduling, primetime, future value, holidays, etc.

#### Example coefficient: `is_primetime`

From `model_coefficients.csv` (deployable):

- `beta_standardized = −0.3406` (binary feature — not mean-centered in the scaler)

On the logit scale, primetime multiplies the **odds** of picking that team by:

```
exp(−0.3406) ≈ 0.71
```

All else equal, entries are about **29% less likely** (on the odds scale) to take a team in a primetime slot.

### Excluded from the likelihood

Rows are dropped when they carry **no preference information**:

| Case | Why excluded |
|------|----------------|
| Zero available teams | Eliminated by rule (e.g. holiday leg with no eligible team) — no choice expressed |
| Exactly one available team | Forced pick — no menu |
| No-pick eliminations | No team selected |

They remain in alive/eligible accounting for survival; including them in the likelihood would bias β.

### IIA caveat

**Independence of irrelevant alternatives (IIA):** adding a new option pulls probability from existing options in proportion to their current shares. Two nearly identical “safe” favorites splitting chalk mildly violates this. Accepted as a known approximation; **nested logit** is the escape hatch if it ever matters enough to justify the complexity.

---

## 5. Three rejected choices worth understanding

### 5a. Team fixed effects — rejected for overfitting AND undeployability

Idea: add 31 team dummies (“everyone loves the Chiefs”) to absorb brand popularity.

From `ablation_report.md`:

| Spec | Mean LOO holdout LL |
|------|---------------------|
| E — full, **no** team FE (10 features) | **−1.959** |
| F — full **with** team FE (41 features) | **−2.045** |

**Overfitting** (plain): more parameters always fit the training seasons better; the test is **held-out seasons**. **Leave-one-season-out (LOO):** fit on five seasons, score on the sixth, rotate, average. Team FE **loses by 0.086 nats** on LOO despite better training fit.

**Undeployability:** 2026 team effects are not observed. A model you cannot score next season is worthless regardless of in-sample fit.

Deployable spec uses **11 features**, no team FE (`DEPLOYABLE_SPEC` in `clogit_core.py`).

### 5b. Future value from actual future betting lines — rejected as data leak

Natural feature: “how many future weeks will this team be favored?”

Using **actual future closing lines** fails twice:

1. **Leakage.** A picker in week 3 did not know week 12’s closing line. Training on it overstates how well the crowd anticipates the future. **Leakage** = giving the model information that would not exist at decision time.
2. **Undeployable.** Scoring 2026 week `w` needs weeks `w+1…18` with **no posted lines** yet.

**Replacement** (`build/ratings.py`): spread-implied power ratings from lines observed **only up to week w**. Fit `spread ≈ −(r_home − r_away + h)` by ridge-regularized least squares, anchored to a prior-season seed in early weeks. From ratings, **project** any future matchup spread. Computable at every historical decision point (no leak) and at every 2026 decision point (deployable).

Feature in model: `best_future_proj_win_prob` (max projected win prob over remaining schedule from those ratings).

### 5c. Closing lines instead of deadline-time lines — accepted tradeoff

Circa’s pick deadline is **Saturday 4:00 PM PT**. Available odds history is **closing lines**, which include post-deadline movement for Sunday/Monday games.

Bias is small (a few tenths of a point). A second odds source costs money. Shipped on closing lines with the limitation stated — a deliberate, disclosed compromise.

---

## 6. The contest calendar problem (a genuinely hard engineering detail)

Circa **contest weeks ≠ NFL weeks**. Thanksgiving (Wed/Thu/Fri) and the Christmas leg are **separate contest weeks** (Rule 7) → **20 contest weeks**, not 18.

### Why naive date partitioning fails

Partition games into contiguous date ranges → **impossible** in 2020: PIT–BAL was scheduled for Thanksgiving, COVID-postponed to **Wednesday December 2**, while contest week 12 covered **Nov 29–30**. Entries had picked PIT in the **Thanksgiving column**. Date ranges **overlap**; zero valid contiguous partitions.

### Working approach (`build/contest_calendar.py`)

1. Group by NFL week.
2. Split holiday legs by calendar date (Thanksgiving window, Christmas window).
3. Reassign postponed games into the holiday leg when **picks** reference that contest column (data-driven; no hardcoded team/date pairs).
4. **O(n)** over games; no search.

### Hard validations (build fails loudly)

1. Derived contest week count must equal pick-file week columns.
2. Every team picked in a contest week must be among teams **playing** that week — **zero tolerance**.

If the calendar is wrong, picks fall outside the window immediately — errors surface at build time, not as silent corruption downstream.

### Ties (Rule 6a)

A tie is graded as a **loss**. In pick outcomes there are **1,634** `TIE` rows (`picks_long.parquet` / `entry_picks.csv`); treating ties as survivals would corrupt every downstream survival count. Game-level `is_tie` in scores is rare (5 tied games in 2020–2025 schedule data); the contest outcome layer is what matters for elimination.

---

## 7. Layer 3 — Monte Carlo simulation

**Monte Carlo:** when the system is too tangled for closed-form algebra, **simulate many times and count**.

```
for each simulated season:
    for each contest week:
        every surviving entry samples a pick from the crowd model (softmax over its menu)
        game outcomes sampled from implied win probabilities (+ historical tie rate)
        losers eliminated; burned bitmasks update
```

Tie mass: **0.003096** per game (`historical_tie_rate` from `game_team_week.csv`); ties count as losses.

### Why simulate instead of static week projections?

Pick distribution in week `w` depends on which teams the pool has burned, which depends on eliminations in weeks `1…w−1`, which depends on outcomes. A static “week w pick %” assuming the historical burned state is wrong for forward projection. Only simulation propagates state.

### Backtest validation

`backtest_report.md` (500 sims/season, 2021–2025): actual historical `entries_alive` falls inside the simulated **5th–95th percentile band** for **85.0%** of weeks (**85/100**).

Early weeks: in-band **74%**; late weeks: **96%**. Bias: survival often runs **high** (model under-dispersion → eliminations too weak vs reality) — consistent with Section 10.

---

## 8. Layer 4 — the equity engine (turning predictions into decisions)

Everything above models the **field**. It never modeled **you**. The equity engine (`model/equity.py`) adds that.

For each candidate pick:

1. Reconstruct true field state (every alive entry’s burned bitmask).
2. Force your entry onto that team this week.
3. Simulate the rest of the season.
4. Average **dollar payout** across many simulated worlds → **expected value (EV)**.

**EV (plain):** the average dollar outcome if you could replay the same decision many times with the same rules and randomness.

### Payout rules (Rule 19d) — evaluated every week

| Situation | Payout |
|-----------|--------|
| Exactly **1** entry alive | That entry takes the **whole pot** |
| **0** alive | Pot **splits** among everyone who **submitted** a pick that week (you can get paid even though you “lost,” if everyone else lost too) |
| **>1** alive after final week | Split among **finalists** who submitted |

Subtle case: entry eliminated under Rules 8/9 with **no legal pick** did **not submit** → excluded from zero-survivor split. Wrong payout logic misprices the split channel.

### Implementation choices

| Choice | Why |
|--------|-----|
| **Shared game outcomes** | Your entry and the field live in the same simulation; one sampled result applies to everyone. Separate sims per entry would break the correlation structure the contest depends on. |
| **Continuation policy** | After the forced pick, your entry keeps sampling from the **same** crowd model. No tunable “future skill.” Understates your edge equally for all candidates → fair **ranking**; burned bitmask still updates so “spending” a team now costs you later. |

Current equity report (`equity_report.md`, 2025 week 10): **2,000** shared worlds, full field (**1,769** alive), pot **$20M**.

---

## 9. The 2026 projection specifically

### Seeding strength from market win totals

Historical seasons: ratings from observed lines.

2026 beyond week 1: no full-season lines. Options:

| Approach | Verdict |
|----------|---------|
| Decay 2025 ratings toward mean | Simple; ignores offseason moves |
| **Invert posted 2026 win totals** | **Chosen** |

Solve for 32 team ratings `r` (centered at 0) such that:

```
for each team t:  Σ_{games g of t} P(t wins g | r, h) ≈ win_total_t
```

32 unknowns, 32 targets, numerical solve (`model/market_ratings_2026.py`).

From `projection_2026_report.md`:

- Max residual vs posted totals: **0.0938** wins
- Home field `h`: **1.5724** points (reused from 2025 week-1 ratings build)
- Win-prob `b`: **0.144762**

### Week 1 uses real spreads

Posted Week 1 and Week 2 spreads exist (`nfl_week1_spreads_2026.csv`, `nfl_week2_spreads_2026.csv`). Any contest week with a posted-spreads CSV uses those lines directly; later weeks use ratings-projected spreads. Best available information per week.

### The standardisation trap (read this twice)

`build_X_alt()` standardises continuous features using the **mean and std of whatever dataframe you pass it**.

If you standardise **2026** features against the **2026** distribution while applying β estimated on **2020–2025**, coefficients operate on the **wrong scale**. Output looks plausible and is **wrong** — no error, no warning.

**Fix used (route b):** standardise 2026 with **training** mean/std from `game_team_week.csv`, then apply `beta_standardized` (`model/features_2026.py`).

**Verification:** score **2025 contest week 10** through the 2026 inference path; max |delta| vs existing pipeline = **0.000000** (`projection_2026_report.md`). When you have no ground truth for the target year, re-deriving a known historical answer through the new path is the cheap proof that wiring is correct.

### Simulation settings (`projection_2026_report.md`)

| Parameter | Value |
|-----------|-------|
| Entries per sim | **20,000** (2025 signup: **18,694**; Rule 19a guarantee: **20,000**) |
| Simulated seasons | **300** |
| Runtime | **138.7 s** |
| Missing kickoff times (`is_primetime = 0`) | **24** games |

Output: `data/2026/pick_projections_2026.csv` — projected % of **entries alive entering each week** that pick each team.

---

## 10. What does NOT work — known limitations

### Under-dispersion (most important)

Real crowds **herd** harder than the model predicts.

**Herfindahl index (HHI):** sum of squared pick shares within a week — higher means more concentrated on a few teams.

From `model_report.md` CHECK 5:

| | Predicted HHI | Actual HHI |
|--|---------------|------------|
| Mean | **0.242** | **0.288** |
| Weeks with predicted < actual | **81.4%** |

Directional consequence: model **understates** chalk concentration → **understates** payoff to **fading** popular teams — the trade the engine is built to find. Projected shares on favorites are likely **too low**, especially **Th** and **Ch** legs.

### Rare events are invisible

`p_sole_winner` ≈ 0 in equity output (`equity_report.md`) because winning outright is ~1-in-thousands. Plain Monte Carlo cannot resolve it; EV is driven almost entirely by **final-week split** channels. Fixing this needs **importance sampling** (bias draws toward rare outcomes, reweight) — not more sims at the same sampler.

### Single-week candidates statistically indistinguishable

`equity_report.md` (2025 week 10):

- Rank-1 vs rank-2 EV gap: **$6,835**
- Paired SE on difference: **±$12,159**
- Gap is **inside** Monte Carlo noise; three runs can yield three different top picks.

**Standard error (plain):** how much the estimate would wobble if you reran with different random seeds.

### Engine does not beat simple baselines (survival)

`equity_backtest.md` — **100** decision points (2021–2025), actual results:

| Policy | Hist. survival rate | Mean field pick share |
|--------|---------------------|------------------------|
| **Equity** | **0.80** | **0.176** |
| Chalk (best available favorite) | **0.88** | 0.267 |
| Modal (follow crowd) | **0.74** | **0.342** |

Equity **fades** the crowd (lower pick share than modal) but does **not** beat chalk on survival. Survival is not the objective (contrarian play trades survival for payoff), but there is **no demonstrated EV edge** in this backtest either.

Note: that backtest’s EV path uses **K=300 subsampled field** for speed; EV magnitudes there are biased upward (see subsampling below). Survival and pick-share metrics use true field state.

### Techniques that failed on contact

| Technique | What went wrong |
|-----------|-----------------|
| **Field subsampling** (K=400, scale counts) | Correctly rescales split **size** but inflates probability of rare “everyone else died” configs. EV inflation up to **~$34,700** per candidate (`equity_report.md`, LAR). **Fix:** simulate full field. |
| **Common random numbers** across candidates | Theoretically should cancel shared noise. **No measurable variance reduction** — paired SE matched independent-difference formula (`equity_report.md`). Dominant variance is whether **your** entry survives; each candidate’s survival hinges on a **different** forced game. |

### Five seasons is a hard evidence ceiling

~100 independent week-level decisions across 2021–2025. No method invents more history.

---

## 11. How to read the 2026 output

File: `data/2026/pick_projections_2026.csv`

| Structure | Meaning |
|-----------|---------|
| Rows | 32 teams (alphabetical) + **`ENTRIES_ALIVE`** |
| Columns | 20 contest weeks: `1,2,…,11,Th,12,13,14,15,Ch,16,17,18` |
| Cell value | Projected **% of entries alive entering that week** that pick that team (one decimal, e.g. `12.3`) |
| Empty cell | Team does not play that contest week (bye or not in holiday leg) |
| `0.0` | Plays but projected share rounds to zero |
| `ENTRIES_ALIVE` row | Mean entries alive **entering** that week (across 300 sims) |

### Reading instructions

1. **`ENTRIES_ALIVE` is a mean over a bimodal distribution.** If the popular pick wins, much of the field survives; if it loses, a large fraction dies at once. The mean is not a typical world. Historical week-2 survival ranged **44%** (2022) to **97%** (2025) of week-1 entries (`week_summary.csv`). Use for **scale**, not forecast.

2. **Late-week survivor counts are biased high.** Projection: ~**35** alive entering week 18 vs historical finals **5, 3, 4, 18, 6** (2021–2025) and **35** (2020). Under-dispersion spreads picks → weaker simulated eliminations → too many survivors.

3. **Confidence decays with horizon.** Weeks 1–4: posted Week 1–2 lines + market win totals. Later weeks: no injuries, trades, or breakouts modeled. **Shape**, not precision. Re-run as lines post.

4. **Christmas column ~92% not 100%.** Column sum **91.8%** (`projection_2026_report.md`): ~8% of entries alive entering `Ch` have **burned all eight** Christmas-leg teams and are eliminated under Rule 9 **without** a pick. Holding a Christmas-eligible team in reserve has quantifiable value.

---

## 12. Glossary

| Term | Definition |
|------|------------|
| **Conditional logit** | Discrete choice model: pick probability = softmax over **that row’s** feasible alternatives only. |
| **Softmax** | `exp(z_i) / Σ exp(z_j)` — maps logits to a probability vector summing to 1. |
| **Choice set** | Teams an entry may still pick this week: playing minus burned. |
| **Maximum likelihood** | Estimate parameters by maximizing probability of observed choices under the model. |
| **Log-likelihood** | `Σ log P(observed)`; per-choice average LL maps to “typical assigned prob” via `exp(LL)`. |
| **Overfitting** | Parameters that fit training noise hurt performance on unseen seasons. |
| **Leave-one-season-out (LOO)** | Train on all seasons except one; test on held-out season; repeat and average. |
| **Calibration** | Whether predicted probabilities match realized frequencies (slope ≈ 1 in `pred` vs `actual` shares). |
| **Standard error** | Spread of an estimate across repeated Monte Carlo runs — “how much would this number wobble?” |
| **Monte Carlo** | Estimate quantities by simulating randomness many times and averaging counts. |
| **Expected value (EV)** | Mean payout across simulated worlds for a decision. |
| **Endogeneity** | Survivors are not a random subset; aggregate stats confound preference with who is left. |
| **Data leakage** | Training features that would not exist at real decision time. |
| **IIA** | Logit assumption: new option steals share from existing options in proportion to current shares. |
| **Herfindahl index** | `Σ share²` within a week — concentration measure; higher = more herding. |
| **Importance sampling** | Draw from a biased distribution, reweight to estimate rare-event probabilities. |
| **Ridge regularisation** | Penalty on rating deviations from prior when fitting spreads — stabilises early-season ratings. |
| **Bitmask eligibility** | 32-bit mask of burned teams; eligible iff team bit not set. |

---

## Key artifact index

| Topic | Where to look |
|-------|----------------|
| Fitted β, train LL | `model/fitted_model.json`, `data/out/model_coefficients.csv` |
| Ablation / team FE | `data/out/ablation_report.md` |
| Sanity / HHI / calibration | `data/out/model_report.md` |
| Simulator backtest | `data/out/backtest_report.md` |
| Equity (current week) | `data/out/equity_report.md`, `equity_candidates.csv` |
| Equity policy backtest | `data/out/equity_backtest.md` |
| 2026 projection run | `data/out/projection_2026_report.md`, `data/2026/pick_projections_2026.csv` |
| Run 2026 projection | `uv run python -m model.project_2026` |
