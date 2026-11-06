from __future__ import annotations

import sys
from pathlib import Path

# Dynamically add the project root directory to sys.path so 'src' and root modules resolve correctly
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import time
from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf

from tickers import TICKERS_100, ADDITIONAL_TICKERS_100
from src.stock_service import StockService
from src.caching.cache import Cache  # Import your SQLite Cache class
from src.valuations.lenses import LENSES
from src.valuations.average_score import average_score

YEARS = 10

def fetch_10yr_cagr(ticker: str) -> float | None:
    """Calculates the 10-year CAGR using SQLite cache, falling back to yfinance if missing."""
    try:
        # 1. Check SQLite cache for historical price data first
        hist = Cache.check_price_history(ticker, YEARS)
        
        if hist is None or hist.empty:
            # 2. Fetch via yfinance API if not cached
            stock = yf.Ticker(ticker)
            end_date = datetime.today()
            start_date = end_date - timedelta(days=365 * YEARS)
            
            hist = stock.history(start=start_date, end=end_date)
            if hist.empty:
                return None
                
            # 3. Store price history in SQLite cache
            Cache.store_price_history(ticker, YEARS, hist)

        if len(hist) < 252 * 5:  # Require at least 5 years of active price history
            return None
            
        start_price = hist['Close'].iloc[0]
        end_price = hist['Close'].iloc[-1]
        actual_years = (hist.index[-1] - hist.index[0]).days / 365.25
        
        if actual_years < 5 or start_price <= 0:
            return None
            
        cagr = (end_price / start_price) ** (1 / actual_years) - 1
        return float(cagr)
    except Exception:
        return None


def run_scored_backtest(tickers: list[str]) -> pd.DataFrame:
    results = []
    
    print(f"Running scored backtest across {len(tickers)} tickers...")
    for i, ticker in enumerate(tickers, 1):
        # 1. Calculate 10-year historical return benchmark (cached)
        cagr = fetch_10yr_cagr(ticker)
        if cagr is None:
            continue
            
        # 2. Fetch stock summary through StockService (which checks SQLite summary cache)
        try:
            summary = StockService.fetch_stock_summary(ticker, period="1d")
            if not summary:
                continue
                
            # Compute Composite Average Score (includes small-cap Scale Disruptor lens)
            comp_result = average_score(summary)
            
            # Extract individual lens scores
            lens_scores = {}
            for lens_name, scoring_fn in LENSES.items():
                if lens_name != "Average":
                    try:
                        res = scoring_fn(summary)
                        lens_scores[lens_name] = res.score if hasattr(res, "score") else res
                    except Exception:
                        lens_scores[lens_name] = None

            results.append({
                "Ticker": ticker,
                f"{YEARS}Yr_CAGR_Pct": round(cagr * 100, 2),
                "Composite_Score": round(comp_result.score, 2) if hasattr(comp_result, "score") else comp_result,
                **{f"Score_{k}": round(v, 2) if v is not None else None for k, v in lens_scores.items()}
            })
        except Exception as e:
            print(f"  -> Error scoring {ticker}: {e}")
            continue
            
        # Optional brief sleep (only active when fetching from API, cache hits skip this)
        time.sleep(0.1)

    return pd.DataFrame(results)


if __name__ == "__main__":
    all_tickers = list(set(TICKERS_100 + ADDITIONAL_TICKERS_100))
    df_results = run_scored_backtest(all_tickers)
    
    if not df_results.empty:
        print("\n--- Scored Backtest Summary Statistics ---")
        print(df_results.describe())
        
        # Correlation Analysis against 10Yr CAGR
        print("\n--- Correlation with 10-Year Historical CAGR ---")
        numeric_cols = df_results.select_dtypes(include=["number"]).columns
        correlations = df_results[numeric_cols].corr()[f"{YEARS}Yr_CAGR_Pct"].sort_values(ascending=False)
        print(correlations)
        
        # Save output
        output_path = Path("data/scored_valuation_backtest.csv")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df_results.to_csv(output_path, index=False)
        print(f"\nResults successfully saved to {output_path}")
    else:
        print("No valid data collected.")