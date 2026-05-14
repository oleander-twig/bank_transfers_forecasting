import numpy as np
import pandas as pd

LAGS = [1, 2, 3, 4, 5, 6, 7, 8, 12, 16, 26, 52]
WINDOWS = [4, 8, 12, 26]


def build_features_from_pivot(pivot: pd.DataFrame, t_week: int) -> pd.DataFrame:
    """Build feature matrix for target_week=t_week.

    All features use data strictly before t_week (no leakage).
    """
    n = len(pivot)
    feat: dict[str, np.ndarray] = {}

    for lag in LAGS:
        w = t_week - lag
        feat[f"lag_{lag}"] = pivot[w].values if w in pivot.columns else np.zeros(n)

    for window in WINDOWS:
        win_weeks = [w for w in range(t_week - window, t_week) if w in pivot.columns]
        if win_weeks:
            win_data = pivot[win_weeks].values
            feat[f"roll_mean_{window}"] = win_data.mean(axis=1)
            feat[f"roll_std_{window}"] = win_data.std(axis=1)
            feat[f"roll_max_{window}"] = win_data.max(axis=1)
            feat[f"roll_min_{window}"] = win_data.min(axis=1)
        else:
            for s in ("mean", "std", "max", "min"):
                feat[f"roll_{s}_{window}"] = np.zeros(n)

    trend_weeks = [w for w in range(t_week - 12, t_week) if w in pivot.columns]
    if len(trend_weeks) >= 2:
        tw_arr = np.array(trend_weeks, dtype=float)
        tw_c = tw_arr - tw_arr.mean()
        vals = pivot[trend_weeks].values
        cov = (vals * tw_c).mean(axis=1) - vals.mean(axis=1) * tw_c.mean()
        var_x = tw_c.var()
        feat["trend_12w"] = cov / (var_x + 1e-8)
    else:
        feat["trend_12w"] = np.zeros(n)

    w_ly = t_week - 52
    feat["same_week_last_year"] = pivot[w_ly].values if w_ly in pivot.columns else np.zeros(n)

    feat["week"] = np.full(n, t_week)
    feat["week_of_year"] = np.full(n, t_week % 52)

    return pd.DataFrame(feat, index=pivot.index)
