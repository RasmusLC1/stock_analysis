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

# Import from your application architecture
# (If tickers.py is inside tests/, use 'from .tickers import TICKERS_100' or keep 'from tickers import TICKERS_100')
from tickers import TICKERS_100, ADDITIONAL_TICKERS_100
from src.stock_service import StockService
from src.valuations.lenses import LENSES
from src.valuations.average_score import average_score

YEARS = 10

def fetch_10yr_cagr(ticker: str) -> float | None:
    """Calculates the 10-year Compound Annual Growth Rate (CAGR) for a ticker."""
    try:
        stock = yf.Ticker(ticker)
        end_date = datetime.today()
        start_date = end_date - timedelta(days=365 * YEARS)
        
        hist = stock.history(start=start_date, end=end_date)
        if hist.empty or len(hist) < 252 * 5:  # Require at least 5 years of active price history
            return None
            
        start_price = hist['Close'].iloc[0]
        end_price = hist['Close'].iloc[-1]
        years = (hist.index[-1] - hist.index[0]).days / 365.25
        
        if years < 5 or start_price <= 0:
            return None
            
        cagr = (end_price / start_price) ** (1 / years) - 1
        return float(cagr)
    except Exception:
        return None


def run_scored_backtest(tickers: list[str]) -> pd.DataFrame:
    results = []
    
    print(f"Running scored backtest across {len(tickers)} tickers...")
    for i, ticker in enumerate(tickers, 1):
        print(f"[{i}/{len(tickers)}] Processing {ticker}...")
        
        # 1. Calculate 10-year historical return benchmark
        cagr = fetch_10yr_cagr(ticker)
        if cagr is None:
            continue
            
        # 2. Fetch stock summary and run through your app's scoring engine
        try:
            summary = StockService.fetch_stock_summary(ticker)
            if not summary:
                continue
                
            # Compute Composite Average Score
            comp_result = average_score(summary)
            
            # Extract individual lens scores if available in your LENSES dictionary
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
            
        # Rate limiting to respect Yahoo Finance API limits
        time.sleep(0.4)

    return pd.DataFrame(results)


if __name__ == "__main__":
    df_results = run_scored_backtest(list(set(TICKERS_100 + ADDITIONAL_TICKERS_100)))
    
    if not df_results.empty:
        print("\n--- Scored Backtest Summary Statistics ---")
        print(df_results.describe())
        
        # Correlation Analysis against 10Yr CAGR
        print("\n--- Correlation with 10-Year Historical CAGR ---")
        numeric_cols = df_results.select_dtypes(include=["number"]).columns
        correlations = df_results[numeric_cols].corr()["10Yr_CAGR_Pct"].sort_values(ascending=False)
        print(correlations)
        
        # Save output
        df_results.to_csv("data/scored_valuation_backtest.csv", index=False)
        print("\nResults successfully saved to scored_valuation_backtest.csv")
    else:
        print("No valid data collected.")