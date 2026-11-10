from __future__ import annotations

from pathlib import Path
import sqlite3
import pickle
import pandas as pd
from ..info.info_config import InfoConfig

CACHE_DIR = Path(__file__).resolve().parent.parent / "data_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = CACHE_DIR / "stock_summaries.db"


class Cache:
    @staticmethod
    def _get_connection():
        conn = sqlite3.connect(DB_PATH)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS summaries (
                ticker TEXT,
                period TEXT,
                data BLOB,
                PRIMARY KEY (ticker, period)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS price_history (
                ticker TEXT,
                years INT,
                data BLOB,
                PRIMARY KEY (ticker, years)
            )
        """)
        return conn

    @staticmethod
    def check_cache(ticker_symbol: str, period: str) -> InfoConfig | None:
        try:
            with Cache._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT data FROM summaries WHERE ticker = ? AND period = ?",
                    (ticker_symbol, period)
                )
                row = cursor.fetchone()
                if row:
                    return pickle.loads(row[0])
        except Exception as e:
            print(f"Warning: Could not retrieve summary cache for {ticker_symbol}: {e}")
        return None

    @staticmethod
    def store_cache(ticker_symbol: str, period: str, data: InfoConfig) -> None:
        try:
            blob = pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)
            with Cache._get_connection() as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO summaries (ticker, period, data) VALUES (?, ?, ?)",
                    (ticker_symbol, period, sqlite3.Binary(blob))
                )
        except Exception as e:
            print(f"Warning: Could not save summary cache for {ticker_symbol}: {e}")

    @staticmethod
    def check_price_history(ticker_symbol: str, years: int) -> pd.DataFrame | None:
        """Retrieves cached historical price dataframe from SQLite."""
        try:
            with Cache._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT data FROM price_history WHERE ticker = ? AND years = ?",
                    (ticker_symbol, years)
                )
                row = cursor.fetchone()
                if row:
                    return pickle.loads(row[0])
        except Exception as e:
            print(f"Warning: Could not retrieve price history cache for {ticker_symbol}: {e}")
        return None

    @staticmethod
    def store_price_history(ticker_symbol: str, years: int, df: pd.DataFrame) -> None:
        """Stores historical price dataframe into SQLite."""
        try:
            blob = pickle.dumps(df, protocol=pickle.HIGHEST_PROTOCOL)
            with Cache._get_connection() as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO price_history (ticker, years, data) VALUES (?, ?, ?)",
                    (ticker_symbol, years, sqlite3.Binary(blob))
                )
        except Exception as e:
            print(f"Warning: Could not save price history cache for {ticker_symbol}: {e}")