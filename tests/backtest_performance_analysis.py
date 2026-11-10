from __future__ import annotations

import sys
from pathlib import Path

# 1. Robust path bootstrap so 'src' and root modules resolve correctly
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import time
from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf

# Import tickers and application scoring architecture
try:
    from tickers import TICKERS_100, ADDITIONAL_TICKERS_100
except ImportError:
    from tests.tickers import TICKERS_100, ADDITIONAL_TICKERS_100

from backend.src.stock_service import StockService
from backend.src.valuations.lenses import LENSES
from backend.src.valuations.average_score import average_score

AMOUNT = 10
YEARS = 3  # Shortened window to align with available yfinance annual history


def fetch_cagr(ticker: str) -> float | None:
    """Calculates the Compound Annual Growth Rate (CAGR) for a ticker over the specified years."""
    try:
        stock = yf.Ticker(ticker)
        end_date = datetime.today()
        start_date = end_date - timedelta(days=365 * YEARS)
        
        hist = stock.history(start=start_date, end=end_date)
        if hist.empty or len(hist) < 252 * 2:  # Require at least ~2 years of active price history
            return None
            
        start_price = hist['Close'].iloc[0]
        end_price = hist['Close'].iloc[-1]
        active_years = (hist.index[-1] - hist.index[0]).days / 365.25
        
        if active_years < 2 or start_price <= 0:
            return None
            
        cagr = (end_price / start_price) ** (1 / active_years) - 1
        return float(cagr)
    except Exception:
        return None


def run_scored_backtest(tickers: list[str]) -> pd.DataFrame:
    results = []
    print(f"Running {YEARS}-year historical backtest across {len(tickers)} tickers...")
    
    cagr_col_name = f"{YEARS}Yr_CAGR_Pct"
    historical_period = f"{YEARS}y"
    
    for i, ticker in enumerate(tickers, 1):
        cagr = fetch_cagr(ticker)
        if cagr is None:
            continue
            
        try:
            # Utilizing the new period parameter to fetch historical context
            summary = StockService.fetch_stock_summary(ticker, period=historical_period)
            if not summary:
                continue
                
            comp_result = average_score(summary)
            
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
                cagr_col_name: round(cagr * 100, 2),
                "Composite_Score": round(comp_result.score, 2) if hasattr(comp_result, "score") else comp_result,
                **{f"Score_{k}": round(v, 2) if v is not None else None for k, v in lens_scores.items()}
            })
        except Exception:
            continue
            
        time.sleep(0.3)

    return pd.DataFrame(results)


def analyze_top_portfolios(df: pd.DataFrame) -> pd.DataFrame:
    """Extracts the top N highest-scoring stocks for each category and calculates portfolio CAGR."""
    score_columns = [
        "Composite_Score", 
        "Score_Growth", 
        "Score_Value", 
        "Score_Health", 
        "Score_Quality"
    ]
    
    portfolio_summary = []
    cagr_col_name = f"{YEARS}Yr_CAGR_Pct"
    
    print("\n" + "="*60)
    print(f"TOP-{AMOUNT} PORTFOLIO PERFORMANCE ANALYSIS (HISTORICAL {YEARS}-YR CAGR)")
    print("="*60)
    
    basket_mean = df[cagr_col_name].mean()
    print(f"Benchmark: Full Universe Basket Average CAGR = {basket_mean:.2f}%\n")
    
    for col in score_columns:
        if col not in df.columns:
            continue
            
        valid_df = df.dropna(subset=[col, cagr_col_name])
        top_n = valid_df.nlargest(AMOUNT, col)
        
        avg_cagr = top_n[cagr_col_name].mean()
        median_cagr = top_n[cagr_col_name].median()
        tickers_list = top_n["Ticker"].tolist()
        
        portfolio_summary.append({
            "Category": col,
            f"Top {AMOUNT} Mean CAGR (%)": round(avg_cagr, 2),
            f"Top {AMOUNT} Median CAGR (%)": round(median_cagr, 2),
            "Top Tickers": ", ".join(tickers_list)
        })
        
        print(f"[{col}]")
        print(f"  -> Average {YEARS}-Yr CAGR: {avg_cagr:.2f}%")
        print(f"  -> Median {YEARS}-Yr CAGR:  {median_cagr:.2f}%")
        print(f"  -> Top {AMOUNT} Tickers:     {', '.join(tickers_list)}\n")

    print("="*60)
    return pd.DataFrame(portfolio_summary)


if __name__ == "__main__":
    all_tickers = list(set(TICKERS_100 + ADDITIONAL_TICKERS_100))
    df_results = run_scored_backtest(all_tickers)
    
    if not df_results.empty:
        df_top_portfolios = analyze_top_portfolios(df_results)
        output_file = f"top_{AMOUNT}_portfolios_{YEARS}yr_cagr.csv"
        df_top_portfolios.to_csv(output_file, index=False)
        print(f"Results saved to {output_file}")
    else:
        print("No valid data collected.")