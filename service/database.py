import asyncpg
import pandas as pd

from .config import settings

_pool: asyncpg.Pool | None = None


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
    """Fetch weekly target series for given INN list from PostgreSQL.

    Returns DataFrame with columns: inn_id, week, target.
    """
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT inn_id, week, target FROM target_series WHERE inn_id = ANY($1)",
            inn_list,
        )
    if not rows:
        return pd.DataFrame(columns=["inn_id", "week", "target"])
    return pd.DataFrame([dict(r) for r in rows])
