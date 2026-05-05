from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

async def exec_sp(db: AsyncSession, sp_name: str, params: dict) -> list[dict]:
    """
    Executes a stored procedure asynchronously.
    Returns all rows as list of dicts.
    """
    param_str = ", ".join([f"@{k}=:{k}" for k in params])
    sql = text(f"EXEC {sp_name} {param_str}")
    result = await db.execute(sql, params)
    columns = result.keys()
    return [dict(zip(columns, row)) for row in result.fetchall()]


async def exec_sp_one(db: AsyncSession, sp_name: str, params: dict) -> Optional[dict]:
    """
    Executes a stored procedure asynchronously.
    Returns first row as dict or None.
    """
    rows = await exec_sp(db, sp_name, params)
    return rows[0] if rows else None