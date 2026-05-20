from __future__ import annotations

import asyncio
import sys
import time
from pathlib import Path
from urllib.parse import urlparse, urlunparse

import asyncpg

SERVICE_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = SERVICE_ROOT / "src"
MIGRATIONS_DIR = SERVICE_ROOT / "migrations"
APP_DATABASE = "bank_forecasting"

sys.path.insert(0, str(SRC_DIR))
from config import settings  


def admin_dsn(database_url: str) -> str:
    parsed = urlparse(database_url)
    return urlunparse(parsed._replace(path="/postgres"))


def is_admin_migration(path: Path) -> bool:
    return "create_database" in path.name


async def apply_sql_file(dsn: str, path: Path) -> None:
    sql = path.read_text(encoding="utf-8").strip()
    if not sql:
        return

    conn = await asyncpg.connect(dsn=dsn)
    try:
        await conn.execute(sql)
    finally:
        await conn.close()

    print(f"Applied {path.name}")


async def run_migrations() -> None:
    database_url = settings.database_url
    admin_url = admin_dsn(database_url)

    time.sleep(60)

    migration_files = sorted(MIGRATIONS_DIR.glob("*.sql"))
    if not migration_files:
        raise FileNotFoundError(f"No migrations in {MIGRATIONS_DIR}")

    for path in migration_files:
        if is_admin_migration(path):
            await apply_sql_file(admin_url, path)
        else:
            await apply_sql_file(database_url, path)

    print("All migrations applied.")


def main() -> None:
    asyncio.run(run_migrations())


if __name__ == "__main__":
    main()
