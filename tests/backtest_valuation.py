from __future__ import annotations

import sys
from pathlib import Path

# Dynamically add the project root directory to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import time
from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf

try:
    from tickers import TICKERS_100
except ImportError:
    from tests.tickers import TICKERS_100


def fetch_10yr_cagr(ticker: str) -> float | None:
    """Calculates the 10-year Compound Annual Growth Rate (CAGR) for a ticker."""
    try:
        stock = yf.Ticker(ticker)
        end_date = datetime.today()
        start_date = end_date - timedelta(days=365 * 10)
        
        hist = stock.history(start=start_date, end=end_date)
        if hist.empty or len(hist) < 252 * 5:  # Require at least 5 years of active data
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


def run_valuation_backtest(tickers: list[str]) -> pd.DataFrame:
    results = []
    
    print(f"Running backtest across {len(tickers)} tickers...")
    for i, ticker in enumerate(tickers, 1):
        print(f"[{i}/{len(tickers)}] Processing {ticker}...")
        
        # 1. Calculate 10-year historical return benchmark
        cagr = fetch_10yr_cagr(ticker)
        if cagr is None:
            continue
            
        # 2. Fetch current valuation metrics or score (using yfinance fundamentals as proxy)
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            pe_ratio = info.get("trailingPE")
            pb_ratio = info.get("priceToBook")
            div_yield = info.get("dividendYield", 0.0) or 0.0
            market_cap = info.get("marketCap")
            
            results.append({
                "Ticker": ticker,
                "10Yr_CAGR": round(cagr * 100, 2),
                "Trailing_PE": pe_ratio,
                "Price_to_Book": pb_ratio,
                "Dividend_Yield": round(div_yield * 100, 2),
                "Market_Cap": market_cap
            })
        except Exception as e:
            print(f"  -> Error fetching fundamentals for {ticker}: {e}")
            continue
            
        # Gentle rate limiting to avoid hitting Yahoo Finance rate limits
        time.sleep(0.5)

    df = pd.DataFrame(results)
    return df


if __name__ == "__main__":
    df_results = run_valuation_backtest(TICKERS_100)
    
    if not df_results.empty:
        print("\n--- Backtest Summary Statistics ---")
        print(df_results.describe())
        
        # Clean data for correlation analysis
        clean_df = df_results.dropna(subset=["Trailing_PE", "10Yr_CAGR"])
        if not clean_df.empty:
            correlation = clean_df["Trailing_PE"].corr(clean_df["10Yr_CAGR"])
            print(f"\nCorrelation between P/E Ratio and 10-Year CAGR: {correlation:.4f}")
            
        # Save results to CSV for inspection
        df_results.to_csv("valuation_backtest_results.csv", index=False)
        print("\nResults successfully saved to valuation_backtest_results.csv")
    else:
        print("No data collected.")