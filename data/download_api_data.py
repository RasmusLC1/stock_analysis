from __future__ import annotations

import os
from pathlib import Path
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

from backend.src.stock_service import StockService

# Define local cache directory relative to project root
CACHE_DIR = Path(__file__).resolve().parent.parent.parent / "data_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


class StockDataCache:
    """Manages local CSV caching for ticker historical prices and fundamental summaries."""
    
    @staticmethod
    def get_cache_filepath(ticker: str, years: int) -> Path:
        safe_ticker = ticker.replace(".", "_")  # e.g., ASML.AS -> ASML_AS
        return CACHE_DIR / f"{safe_ticker}_{years}yr_cache.csv"

    @classmethod
    def load_cached_data(cls, ticker: str, years: int) -> pd.DataFrame | None:
        """Loads historical price data from local CSV if it exists."""
        filepath = cls.get_cache_filepath(ticker, years)
        if filepath.exists():
            try:
                df = pd.read_csv(filepath, parse_dates=["Date"], index_col="Date")
                return df
            except Exception:
                return None
        return None

    @classmethod
    def save_cached_data(cls, ticker: str, years: int, df: pd.DataFrame) -> None:
        """Saves historical price dataframe to a local CSV file."""
        filepath = cls.get_cache_filepath(ticker, years)
        try:
            df.to_csv(filepath)
        except Exception as e:
            print(f"Warning: Could not cache data for {ticker}: {e}")

    @classmethod
    def get_or_fetch_history(cls, ticker: str, years: int) -> pd.DataFrame | None:
        """Pulls from local CSV cache if available, otherwise downloads from yfinance and caches."""
        cached_df = cls.load_cached_data(ticker, years)
        if cached_df is not None and not cached_df.empty:
            return cached_df

        # Fetch fresh if not cached
        try:
            stock = yf.Ticker(ticker)
            end_date = datetime.today()
            start_date = end_date - timedelta(days=365 * years)
            
            hist = stock.history(start=start_date, end=end_date)
            if hist.empty:
                return None
                
            # Clean dataframe for CSV storage
            hist_reset = hist.reset_index()
            # Ensure standard column naming
            if "Date" in hist_reset.columns:
                hist_reset.set_index("Date", inplace=True)
            
            cls.save_cached_data(ticker, years, hist_reset)
            return hist_reset
        except Exception:
            return None