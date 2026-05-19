import asyncpg
import pandas as pd

from config import settings

_pool: asyncpg.Pool | None = None

HISTORY_COLUMNS = ["inn_id", "week", "target"]
PROFILE_COLUMNS = [
    "inn_id",
    "ipul",
    "id_region",
    "main_okved_group",
    "diff_datopen_report_date_flg",
]


async def get_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(dsn=settings.database_url)
    return _pool


async def close_pool() -> None:
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None


async def fetch_history(inn_list: list[int]) -> pd.DataFrame:
    """Fetch weekly target series for given INN list from PostgreSQL."""
    if not inn_list:
        return pd.DataFrame(columns=HISTORY_COLUMNS)

    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT inn_id, week, target
            FROM target_series
            WHERE inn_id = ANY($1)
            ORDER BY inn_id, week
            """,
            inn_list,
        )
    if not rows:
        return pd.DataFrame(columns=HISTORY_COLUMNS)

    df = pd.DataFrame([dict(r) for r in rows])
    df = df.drop_duplicates(subset=["inn_id", "week"], keep="last")
    df["inn_id"] = df["inn_id"].astype(int)
    df["week"] = df["week"].astype(int)
    df["target"] = df["target"].astype(float)
    return df.sort_values(["inn_id", "week"], ignore_index=True)


async def fetch_profiles(inn_list: list[int]) -> pd.DataFrame:
    """Fetch client profiles for XGBoost categorical features."""
    if not inn_list:
        return pd.DataFrame(columns=PROFILE_COLUMNS)

    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT DISTINCT ON (inn_id)
                inn_id,
                ipul,
                id_region,
                main_okved_group,
                diff_datopen_report_date_flg
            FROM profiles
            WHERE inn_id = ANY($1)
            ORDER BY inn_id, report_date DESC NULLS LAST
            """,
            inn_list,
        )
    if not rows:
        return pd.DataFrame(columns=PROFILE_COLUMNS)

    df = pd.DataFrame([dict(r) for r in rows])
    df["inn_id"] = df["inn_id"].astype(int)
    for col in PROFILE_COLUMNS[1:]:
        df[col] = df[col].astype("int32")
    return df.sort_values("inn_id", ignore_index=True)
