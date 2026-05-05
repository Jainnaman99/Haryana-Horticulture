from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import AsyncGenerator
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

load_dotenv()

# ==============================
# Read from .env
# ==============================

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "1433")
DB_NAME = os.getenv("DB_NAME")
DB_INTEGRATED_AUTH = os.getenv("DB_INTEGRATED_AUTH", "True").lower() == "true"

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# ==============================
# Validate required values
# ==============================

if not DB_HOST or not DB_NAME:
    raise ValueError("DB_HOST and DB_NAME must be set in .env")

# ==============================
# Build connection string
# ==============================

if DB_INTEGRATED_AUTH:
    connection_string = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={DB_HOST},{DB_PORT};"
        f"DATABASE={DB_NAME};"
        "Trusted_Connection=yes;"
        "Encrypt=no;"
        "TrustServerCertificate=yes;"
    )
else:
    if not DB_USER or not DB_PASSWORD:
        raise ValueError("DB_USER and DB_PASSWORD required for SQL authentication")

    connection_string = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={DB_HOST},{DB_PORT};"
        f"DATABASE={DB_NAME};"
        f"UID={DB_USER};"
        f"PWD={DB_PASSWORD};"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )

# Encode for SQLAlchemy
params = quote_plus(connection_string)
DATABASE_URL = f"mssql+aioodbc:///?odbc_connect={params}"

# ==============================
# SQLAlchemy Setup
# ==============================

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

Base = declarative_base()

async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# ==============================
# DB Init + Session
# ==============================

async def init_db():
    async with engine.begin() as conn:
        from sqlalchemy import text

        result = await conn.execute(text("SELECT DB_NAME()"))
        print("✅ Connected to DB:", result.scalar())


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session