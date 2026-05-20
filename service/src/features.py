import numpy as np
import pandas as pd

CAT_COLS = ["ipul", "id_region", "main_okved_group", "diff_datopen_report_date_flg"]
MAX_LAG = 70


def _lags_row_at_cutoff(n: int, weeks: np.ndarray, y: np.ndarray, max_lag: int = MAX_LAG) -> dict:
    """Одна строка лагов для недели n (эквивалент shift)."""
    mask = (weeks <= n) & (weeks >= n - max_lag)
    idx = np.flatnonzero(mask)

    w = weeks[idx]
    yy = y[idx]
    pos = int(np.where(w == n)[0][0])

    row = {}
    for lag in range(1, max_lag + 1):
        j = pos - lag
        row[f"lag_{lag}"] = float(yy[j])

    return row


def transform_data_for_prediction(
    df: pd.DataFrame,
    prof: pd.DataFrame,
    inns: list[str],
    n_start_week: int,
    horizons: int,
) -> pd.DataFrame:
    inn_groups = {gid: g for gid, g in df.groupby("inn_id", sort=False)}

    res = []
    for inn in inns:
        df_inn = inn_groups.get(inn)

        g = df_inn.sort_values("week")
        weeks = g["week"].to_numpy()
        y = g["target"].to_numpy(dtype=float)

        row = _lags_row_at_cutoff(n_start_week, weeks, y)

        values = row.values()
        row["lag_max"] = max(values)
        row["lag_min"] = min(values)
        row["lag_mean"] = sum(values) / len(values)
        row["inn_id"] = inn

        res.append(row)

    res_df = pd.DataFrame(res)

    l = len(res_df)
    res_df = res_df.loc[res_df.index.repeat(horizons)].copy()
    res_df["horizon"] = list(range(1, horizons + 1)) * l

    res_df = res_df.merge(prof, on="inn_id", how="inner")
    for col in CAT_COLS:
        res_df[col] = res_df[col].astype("category")
    res_df = res_df.drop(columns=["inn_id"], errors="ignore")

    lag_target_cols = [
        c for c in res_df.columns if c.startswith("lag_") or c in ("target", "trns_amount")
    ]
    res_df[lag_target_cols] = res_df[lag_target_cols].map(lambda x: np.log(x + 1))

    return res_df
