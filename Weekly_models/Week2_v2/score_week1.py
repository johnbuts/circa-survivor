"""Score 2026 Week 1 crowd shares. Writes only under Week2_v2."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.special import logsumexp

_CRAFT = Path(__file__).resolve().parent.parent
if str(_CRAFT) not in sys.path:
    sys.path.insert(0, str(_CRAFT))

from build.team_names import CANONICAL
from model.calendar_from_schedule import derive_contest_calendar
from model.clogit_core import (
    GTW_PATH,
    MODEL_JSON_PATH,
    load_fitted_model,
    scaled_logit_beta,
)
from model.features_2026 import (
    TrainingScalers,
    build_game_team_week_2026,
    build_week_features_matrix,
    fit_training_scalers,
    load_posted_spreads,
)
from model.market_ratings_2026 import (
    fit_ratings_from_win_totals,
    load_home_field,
    load_winprob_b,
)

HERE = Path(__file__).resolve().parent
CRAFT = HERE.parent
REPO = CRAFT.parent
OUT = HERE / "out"
ACTUAL_PATH = REPO / "all_picks_2026" / "parsed" / "week1_pick_share.csv"
SCHEDULE_PATH = CRAFT / "data" / "2026" / "raw" / "nfl_schedule_2026.csv"
WIN_TOTALS_PATH = CRAFT / "data" / "2026" / "raw" / "nfl_win_totals_2026.csv"

SEASON = 2026
FOCUS = ("JAC", "LAC", "PIT", "DET", "LV", "PHI")
TOP5_ACTUAL = ("JAC", "LAC", "PIT", "DET", "LV")
ACTUAL_TOP3_SUM = 0.789
ACTUAL_HHI = 0.23

DISPLAY_TO_ABBR = {
    "JAGUARS": "JAC",
    "CHARGERS": "LAC",
    "STEELERS": "PIT",
    "LIONS": "DET",
    "RAIDERS": "LV",
    "EAGLES": "PHI",
    "BENGALS": "CIN",
    "TITANS": "TEN",
    "SEAHAWKS": "SEA",
    "BEARS": "CHI",
    "RAVENS": "BAL",
    "JETS": "NYJ",
    "COWBOYS": "DAL",
    "VIKINGS": "MIN",
    "RAMS": "LAR",
    "DOLPHINS": "MIA",
    "PATRIOTS": "NE",
    "CHIEFS": "KC",
    "TEXANS": "HOU",
    "GIANTS": "NYG",
    "49ERS": "SF",
    "COLTS": "IND",
    "BRONCOS": "DEN",
    "BUCS": "TB",
    "BROWNS": "CLE",
    "PANTHERS": "CAR",
    "CARDINALS": "ARI",
    "PACKERS": "GB",
    "BILLS": "BUF",
    "FALCONS": "ATL",
    "SAINTS": "NO",
    "COMMANDERS": "WAS",
    "WASHINGTON": "WAS",
}


@dataclass(frozen=True)
class Metrics:
    shares: dict[str, float]
    implied: dict[str, float]
    top3: tuple[str, str, str]
    top3_sum: float
    top5_mae: float
    jac_err: float
    lac_err: float
    pit_err: float
    det_err: float
    hhi: float
    focus_mae: float
    close: bool


def load_actual_shares() -> dict[str, float]:
    df = pd.read_csv(ACTUAL_PATH)
    out: dict[str, float] = {t: 0.0 for t in CANONICAL}
    for row in df.itertuples(index=False):
        name = str(row.team).strip().upper()
        abbr = DISPLAY_TO_ABBR.get(name)
        if abbr is None:
            raise ValueError(f"FAIL unknown actual team {name!r}")
        out[abbr] = float(row.share)
    return out


def softmax_shares(logits: np.ndarray) -> np.ndarray:
    lse = logsumexp(logits)
    return np.exp(logits - lse)


def is_close(m: Metrics) -> bool:
    return (
        m.top3 == ("JAC", "LAC", "PIT")
        and m.jac_err <= 0.03
        and m.lac_err <= 0.03
        and m.pit_err <= 0.05
        and m.det_err <= 0.03
        and m.top5_mae <= 0.03
        and abs(m.top3_sum - ACTUAL_TOP3_SUM) <= 0.05
    )


def metrics_from_shares(
    teams: list[str],
    shares: np.ndarray,
    implied: np.ndarray,
    actual: dict[str, float],
) -> Metrics:
    pred = {t: float(s) for t, s in zip(teams, shares, strict=True)}
    impl = {t: float(p) for t, p in zip(teams, implied, strict=True)}
    ranked = tuple(sorted(pred, key=pred.get, reverse=True)[:3])
    top3_sum = sum(pred[t] for t in ranked)
    top5_mae = float(np.mean([abs(pred[t] - actual.get(t, 0.0)) for t in TOP5_ACTUAL]))
    jac_err = abs(pred["JAC"] - actual["JAC"])
    lac_err = abs(pred["LAC"] - actual["LAC"])
    pit_err = abs(pred["PIT"] - actual["PIT"])
    det_err = abs(pred["DET"] - actual["DET"])
    hhi = float(sum(v * v for v in pred.values()))
    focus_mae = float(np.mean([abs(pred[t] - actual.get(t, 0.0)) for t in FOCUS]))
    m = Metrics(
        shares=pred,
        implied=impl,
        top3=ranked,  # type: ignore[arg-type]
        top3_sum=top3_sum,
        top5_mae=top5_mae,
        jac_err=jac_err,
        lac_err=lac_err,
        pit_err=pit_err,
        det_err=det_err,
        hhi=hhi,
        focus_mae=focus_mae,
        close=False,
    )
    return Metrics(**{**m.__dict__, "close": is_close(m)})


def copy_posted_spreads(posted):
    return {week: dict(lookup) for week, lookup in posted.items()}


def apply_pit_steam(posted, pit_line: float = -6.0):
    """Tua-out steam: PIT from -3.5 (Sep 9 book) to about -6."""
    out = copy_posted_spreads(posted)
    key = ("ATL", "PIT")
    if key not in out[1]:
        raise ValueError("FAIL ATL@PIT missing from week 1 spreads")
    out[1][key] = ("PIT", float(pit_line))
    return out


def build_2026_gtw(posted_spreads):
    schedule = pd.read_csv(SCHEDULE_PATH)
    win_totals_df = pd.read_csv(WIN_TOTALS_PATH)
    calendar, game_week, _labels = derive_contest_calendar(schedule, SEASON)
    games_for_fit = schedule.copy()
    games_for_fit["is_neutral"] = games_for_fit["is_neutral"].astype(int)
    win_totals = {
        row.team: float(row.win_total) for row in win_totals_df.itertuples(index=False)
    }
    if set(win_totals.keys()) != set(CANONICAL):
        raise ValueError("FAIL win totals missing teams")
    b = load_winprob_b()
    home_field = load_home_field()
    ratings, _resid = fit_ratings_from_win_totals(
        games_for_fit, win_totals, home_field=home_field, b=b
    )
    gtw, _missing = build_game_team_week_2026(
        SEASON, calendar, game_week, ratings, home_field, b, posted_spreads
    )
    return gtw.reset_index(drop=True)


def week1_frame(gtw: pd.DataFrame) -> pd.DataFrame:
    w = gtw[gtw["contest_week_ord"] == 1].sort_values("team").reset_index(drop=True)
    if len(w) != 32:
        raise ValueError(f"FAIL week 1 rows {len(w)} != 32")
    return w


def leftover_safe_third_index(
    implied: np.ndarray,
    fav7: np.ndarray,
    *,
    mega_thresh: float,
    fav7_skip: float,
) -> int | None:
    """Highest-implied non-mega team that is not a smash-inventory save."""
    n_mega = int((implied >= mega_thresh).sum())
    if n_mega < 2:
        return None
    for idx in np.argsort(-implied):
        i = int(idx)
        if implied[i] >= mega_thresh:
            continue
        if fav7[i] >= fav7_skip:
            continue
        return i
    return None


def predict_week1(
    week_df: pd.DataFrame,
    scalers: TrainingScalers,
    beta: np.ndarray,
    tau: float,
    *,
    third_chalk_delta: float = 0.0,
    safe_third_delta: float = 0.0,
    fv_gap_gamma: float = 0.0,
    mega_thresh: float = 0.75,
    fav7_skip: float = 3.0,
) -> tuple[list[str], np.ndarray, np.ndarray]:
    feat = build_week_features_matrix(week_df, scalers).astype(np.float64)
    logits = feat @ scaled_logit_beta(beta, tau)
    teams = week_df["team"].tolist()
    implied = week_df["implied_win_prob"].to_numpy(dtype=np.float64)
    if third_chalk_delta != 0.0:
        order = np.argsort(-implied)
        n_mega = int((implied >= mega_thresh).sum())
        if n_mega >= 2 and len(order) >= 3:
            logits[int(order[2])] += float(third_chalk_delta)
    if safe_third_delta != 0.0:
        fav7 = week_df["future_weeks_proj_favored_by_7"].to_numpy(dtype=np.float64)
        idx = leftover_safe_third_index(
            implied, fav7, mega_thresh=mega_thresh, fav7_skip=fav7_skip
        )
        if idx is not None:
            logits[idx] += float(safe_third_delta)
    if fv_gap_gamma != 0.0:
        best_fut = week_df["best_future_proj_win_prob"].to_numpy(dtype=np.float64)
        gap = np.maximum(best_fut - implied, 0.0)
        logits -= float(fv_gap_gamma) * gap
    shares = softmax_shares(logits)
    return teams, shares, implied


def score_week1(
    week_df: pd.DataFrame,
    scalers: TrainingScalers,
    beta: np.ndarray,
    actual: dict[str, float],
    *,
    tau: float,
    third_chalk_delta: float = 0.0,
    safe_third_delta: float = 0.0,
    fv_gap_gamma: float = 0.0,
) -> Metrics:
    teams, shares, implied = predict_week1(
        week_df,
        scalers,
        beta,
        tau,
        third_chalk_delta=third_chalk_delta,
        safe_third_delta=safe_third_delta,
        fv_gap_gamma=fv_gap_gamma,
    )
    return metrics_from_shares(teams, shares, implied, actual)


def historical_week1_top(
    train_gtw: pd.DataFrame,
    scalers: TrainingScalers,
    beta: np.ndarray,
    tau: float,
    season: int = 2025,
) -> tuple[str, float, float]:
    w = (
        train_gtw[
            (train_gtw["season"] == season) & (train_gtw["contest_week_ord"] == 1)
        ]
        .sort_values("team")
        .reset_index(drop=True)
    )
    if w.empty:
        raise ValueError(f"FAIL no historical week 1 for {season}")
    feat = build_week_features_matrix(w, scalers).astype(np.float64)
    logits = feat @ scaled_logit_beta(beta, tau)
    shares = softmax_shares(logits)
    i = int(np.argmax(shares))
    return str(w.iloc[i]["team"]), float(shares[i]), float(np.sum(shares * shares))


def load_fit_bundle():
    train_gtw = pd.read_csv(GTW_PATH)
    scalers = fit_training_scalers(train_gtw)
    beta, _names, tau_ll = load_fitted_model(MODEL_JSON_PATH)
    return train_gtw, scalers, beta, float(tau_ll)
