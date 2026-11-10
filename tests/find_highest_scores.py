from __future__ import annotations

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pandas as pd

from tickers import TICKERS_100, ADDITIONAL_TICKERS_100
from backend.src.stock_service import StockService
from backend.src.valuations.lenses import LENSES
from backend.src.valuations.average_score import average_score

AMOUNT = 100

def collect_scores(tickers: list[str]) -> pd.DataFrame:
    results = []
    print(f"Scoring {len(tickers)} tickers from cache/service...")
    
    for ticker in tickers:
        try:
            summary = StockService.fetch_stock_summary(ticker, period="1d")
            if not summary:
                continue
                
            comp_result = average_score(summary)
            comp_score = comp_result.score if hasattr(comp_result, "score") else comp_result
            
            lens_scores = {}
            for lens_name, scoring_fn in LENSES.items():
                if lens_name != "Average":
                    try:
                        res = scoring_fn(summary)
                        lens_scores[lens_name] = res.score if hasattr(res, "score") else res
                    except Exception:
                        lens_scores[lens_name] = None

            row = {
                "Ticker": ticker,
                "Composite_Score": round(comp_score, 2) if comp_score is not None else None,
            }
            for k, v in lens_scores.items():
                row[f"Score_{k}"] = round(v, 2) if v is not None else None
            
            results.append(row)
        except Exception:
            continue

    return pd.DataFrame(results)


if __name__ == "__main__":
    all_tickers = list(set(TICKERS_100 + ADDITIONAL_TICKERS_100))
    df = collect_scores(all_tickers)
    
    if df.empty:
        print("No data collected.")
        sys.exit(0)

    print("\n" + "=" * 50)
    print(f"TOP {AMOUNT} COMPOSITE SCORES")
    print("=" * 50)

    col = "Composite_Score"
    top = df.dropna(subset=[col]).sort_values(by=col, ascending=False).head(AMOUNT)
    
    if top.empty:
        print("No data available.")
    else:
        for rank, (_, row) in enumerate(top.iterrows(), 1):
            print(f"{rank:3d}. {row['Ticker']:<8} -> {row[col]:.1f}")