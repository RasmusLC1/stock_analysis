from __future__ import annotations

from pathlib import Path
import sqlite3
import pickle
from ..info.info_config import InfoConfig

# Define local cache directory and database path relative to project root
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
        return conn

    @staticmethod
    def check_cache(ticker_symbol: str, period: str) -> InfoConfig | None:
        """Checks if the cache file exists and loads it. Returns None if miss or error."""
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
            print(f"Warning: Could not retrieve cache for {ticker_symbol}: {e}")
        return None

    @staticmethod
    def store_cache(ticker_symbol: str, period: str, data: InfoConfig) -> None:
        """Serializes and stores data to the SQLite database."""
        try:
            blob = pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)
            with Cache._get_connection() as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO summaries (ticker, period, data) VALUES (?, ?, ?)",
                    (ticker_symbol, period, sqlite3.Binary(blob))
                )
        except Exception as e:
            print(f"Warning: Could not save summary cache for {ticker_symbol}: {e}")