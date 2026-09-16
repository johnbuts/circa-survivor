"""Week 1 Monte Carlo of our pick book on GPU (CuPy). Does not rerun the crowd model."""

from __future__ import annotations

import time
from pathlib import Path

import cupy as cp
import numpy as np

N_SIMS = 100_000
SEED = 42
FIELD_START = 20_000
POT = 20_000_000
OURS = {"BAL": 3, "TEN": 3, "PIT": 2, "LV": 2}

# Circa MLs from week1/index.html
GAMES = [
    ("NE", 166, "SEA", -198),
    ("SF", 180, "LAR", -215),
    ("BUF", -106, "HOU", -110),
    ("CHI", -146, "CAR", 124),
    ("CLE", 330, "JAC", -420),
    ("ATL", 136, "PIT", -162),
    ("NYJ", 120, "TEN", -142),
    ("NO", 290, "DET", -360),
    ("TB", 176, "CIN", -210),
    ("BAL", -186, "IND", 156),
    ("WAS", 198, "PHI", -240),
    ("GB", -102, "MIN", -116),
    ("MIA", 168, "LV", -200),
    ("ARI", 450, "LAC", -600),
    ("DAL", -146, "NYG", 124),
    ("DEN", 130, "KC", -154),
]

CROWD_PCT = {
    "ARI": 0.0, "ATL": 0.0, "BAL": 1.7, "BUF": 0.4, "CAR": 0.0, "CHI": 1.0,
    "CIN": 2.5, "CLE": 0.0, "DAL": 0.6, "DEN": 0.0, "DET": 16.2, "GB": 0.3,
    "HOU": 0.0, "IND": 0.0, "JAC": 20.2, "KC": 0.6, "LAC": 40.7, "LAR": 0.5,
    "LV": 3.3, "MIA": 0.0, "MIN": 0.0, "NE": 0.0, "NO": 0.0, "NYG": 0.0,
    "NYJ": 0.0, "PHI": 6.0, "PIT": 1.8, "SEA": 1.6, "SF": 0.0, "TB": 0.0,
    "TEN": 2.6, "WAS": 0.0,
}

REPORT = Path(__file__).with_name("sim_week1_report.md")


def american_to_dec(ml: int) -> float:
    if ml > 0:
        return 1 + ml / 100
    return 1 + 100 / abs(ml)


def vig_free_fav(away: str, away_ml: int, home: str, home_ml: int) -> tuple[str, str, float]:
    fav, dog, fav_ml, dog_ml = (away, home, away_ml, home_ml) if away_ml < home_ml else (home, away, home_ml, away_ml)
    p_fav = 1 / american_to_dec(fav_ml)
    p_dog = 1 / american_to_dec(dog_ml)
    return fav, dog, p_fav / (p_fav + p_dog)


def slate() -> tuple[list[str], list[str], np.ndarray]:
    favs, dogs, ps = [], [], []
    for away, away_ml, home, home_ml in GAMES:
        fav, dog, p = vig_free_fav(away, away_ml, home, home_ml)
        favs.append(fav)
        dogs.append(dog)
        ps.append(p)
    return favs, dogs, np.asarray(ps, dtype=np.float64)


def crowd_share(team: str) -> float:
    return CROWD_PCT[team] / 100.0


def score_weights(favs: list[str], dogs: list[str]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    fav_ours = np.array([OURS.get(t, 0) for t in favs], dtype=np.float64)
    dog_ours = np.array([OURS.get(t, 0) for t in dogs], dtype=np.float64)
    fav_share = np.array([crowd_share(t) for t in favs], dtype=np.float64)
    dog_share = np.array([crowd_share(t) for t in dogs], dtype=np.float64)
    return fav_ours, dog_ours, fav_share, dog_share


def score_winners(winners: list[str]) -> tuple[int, float, float]:
    won = set(winners)
    n_ours = sum(n for t, n in OURS.items() if t in won)
    field = FIELD_START * sum(crowd_share(t) for t in winners)
    chip = POT / field if field > 0 else 0.0
    return n_ours, chip, n_ours * chip


def self_test() -> None:
    favs, dogs, p_fav = slate()
    assert len(GAMES) == 16
    assert p_fav.shape == (16,)
    assert np.all((p_fav > 0) & (p_fav < 1))
    p_dog = 1.0 - p_fav
    assert np.allclose(p_fav + p_dog, 1.0)

    assert abs(0.60 * 1.10 - 0.66) < 1e-12
    assert abs(0.60 * 0.90 - 0.54) < 1e-12
    assert np.clip(0.99 * 1.10, 0.01, 0.99) == 0.99

    n_ours, chip, total = score_winners(favs)
    assert n_ours == 10, n_ours
    share = sum(crowd_share(t) for t in favs)
    assert abs(share - 0.993) < 1e-12, share
    field = FIELD_START * share
    assert abs(field - 19860.0) < 1e-9
    assert abs(chip - POT / 19860.0) < 1e-9
    assert abs(total - 10 * chip) < 1e-9

    n_ours_g, chip_g, total_g = simulate(5, 0)
    assert n_ours_g.min() >= 0 and n_ours_g.max() <= 10
    assert np.allclose(total_g, n_ours_g * chip_g)
    assert cp.cuda.runtime.getDeviceCount() >= 1
    print("self-test ok")


def simulate(n: int, seed: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    favs, dogs, p_fav = slate()
    fo, do, fs, ds = score_weights(favs, dogs)
    p_fav_g = cp.asarray(p_fav)
    fo_g = cp.asarray(fo)
    do_g = cp.asarray(do)
    fs_g = cp.asarray(fs)
    ds_g = cp.asarray(ds)

    rng = cp.random.default_rng(seed)
    noise = rng.uniform(0.90, 1.10, size=(n, 16))
    p = cp.clip(p_fav_g * noise, 0.01, 0.99)
    fav_win = rng.random((n, 16)) < p
    win = fav_win.astype(cp.float64)
    lose = 1.0 - win
    n_ours = win @ fo_g + lose @ do_g
    field_share = win @ fs_g + lose @ ds_g
    chip = POT / (FIELD_START * field_share)
    total = n_ours * chip
    cp.cuda.Stream.null.synchronize()
    return n_ours.get(), chip.get(), total.get()


def bands(x: np.ndarray) -> dict[str, float]:
    return {
        "mean": float(x.mean()),
        "p16": float(np.percentile(x, 16)),
        "p84": float(np.percentile(x, 84)),
        "p2_5": float(np.percentile(x, 2.5)),
        "p97_5": float(np.percentile(x, 97.5)),
        "p0_5": float(np.percentile(x, 0.5)),
        "p99_5": float(np.percentile(x, 99.5)),
    }


def fmt_money(n: float) -> str:
    return f"${n:,.2f}"


def check_nested(b: dict[str, float], name: str) -> None:
    assert b["p16"] >= b["p2_5"] >= b["p0_5"], name
    assert b["p84"] <= b["p97_5"] <= b["p99_5"], name


def write_report(n_ours: np.ndarray, chip: np.ndarray, total: np.ndarray, elapsed: float) -> str:
    hist = np.bincount(n_ours.astype(int), minlength=11)
    assert hist.sum() == N_SIMS
    b_n = bands(n_ours)
    b_c = bands(chip)
    b_t = bands(total)
    check_nested(b_n, "n_ours")
    check_nested(b_c, "chip")
    check_nested(b_t, "total")
    assert np.allclose(total, n_ours * chip)
    assert n_ours.min() >= 0 and n_ours.max() <= 10
    p_wipe = float((n_ours == 0).mean())
    p_all = float((n_ours == 10).mean())
    assert b_n["mean"] > 5
    assert p_wipe < 0.2
    lines = [
        "# Week 1 100k pick-book simulation",
        "",
        "Our book: **BAL×3, TEN×3, PIT×2, LV×2**. Crowd shares from the already-run 2026 projection (not resimulated).",
        "Each game: vig-free Circa implied favorite P(win), times Uniform(0.90, 1.10), clip to [0.01, 0.99]. Seed **42**. N = **100,000**.",
        "Draws and scoring run on GPU (CuPy / RTX 3070 Ti): one `(N, 16)` uniform noise matrix, one Bernoulli draw, two matmuls for `n_ours` and field share. CuPy RNG ≠ NumPy RNG, so counts differ from the CPU run at the same seed.",
        f"GPU wall time: **{elapsed:.3f}s**.",
        "Chip EV = `$20M / field_alive`. Field alive = `20000 × sum(crowd share of winners)`. Percentile bands are the spread of simulated outcomes, not a CI on the mean.",
        "",
        "## Remaining entries (ours)",
        "",
        f"- Mean: **{b_n['mean']:.3f}**",
        f"- 68%: {b_n['p16']:.2f} – {b_n['p84']:.2f}",
        f"- 95%: {b_n['p2_5']:.2f} – {b_n['p97_5']:.2f}",
        f"- 99%: {b_n['p0_5']:.2f} – {b_n['p99_5']:.2f}",
        f"- P(wipeout) = {p_wipe:.4f}; P(all 10 alive) = {p_all:.4f}",
        "",
        "| n | draws |",
        "| --- | ---: |",
    ]
    for k in range(11):
        lines.append(f"| {k} | {int(hist[k])} |")
    lines += [
        "",
        "## Chip EV per live ticket",
        "",
        f"- Mean: **{fmt_money(b_c['mean'])}**",
        f"- 68%: {fmt_money(b_c['p16'])} – {fmt_money(b_c['p84'])}",
        f"- 95%: {fmt_money(b_c['p2_5'])} – {fmt_money(b_c['p97_5'])}",
        f"- 99%: {fmt_money(b_c['p0_5'])} – {fmt_money(b_c['p99_5'])}",
        "",
        "## Total equity (n_ours × chip EV)",
        "",
        f"- Mean: **{fmt_money(b_t['mean'])}**",
        f"- 68%: {fmt_money(b_t['p16'])} – {fmt_money(b_t['p84'])}",
        f"- 95%: {fmt_money(b_t['p2_5'])} – {fmt_money(b_t['p97_5'])}",
        f"- 99%: {fmt_money(b_t['p0_5'])} – {fmt_money(b_t['p99_5'])}",
        "",
        f"Identity check: mean(n_ours × chip) = {fmt_money(float((n_ours * chip).mean()))} vs mean(total) {fmt_money(b_t['mean'])}.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    self_test()
    t0 = time.perf_counter()
    n_ours, chip, total = simulate(N_SIMS, SEED)
    elapsed = time.perf_counter() - t0
    text = write_report(n_ours, chip, total, elapsed)
    REPORT.write_text(text, encoding="utf-8")
    print(text)
    print(f"wrote {REPORT}")
    print(f"gpu {elapsed:.3f}s")


if __name__ == "__main__":
    main()
