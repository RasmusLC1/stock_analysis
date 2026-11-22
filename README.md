# Stock Analysis Tool & Quantitative Backtesting Engine

A modular full-stack quantitative analysis platform designed to scan global markets, evaluate companies across multiple fundamental dimensions, and surface high-conviction secular compounders while filtering out cyclical value traps.

## Architecture

The codebase separates core quantitative scoring, data ingestion, local caching, REST API delivery, and the interactive web interface:

- **`src/valuations/`**: The core scoring engine. Houses individual thematic lenses (`Growth`, `Quality`, `Health`, `Value`, `GARP`, and `Scale Disruptor`) that normalize raw fundamentals onto a 0–100 scale before aggregating them into a weighted composite score.
- **`src/yf_api/` & `src/info/`**: Handles external data extraction via `yfinance` (`api_fetch.py`) and maps raw financial metrics using modular configuration definitions (`info_config.py`).
- **`src/caching/` & `src/data_cache/`**: Manages local persistence using SQLite (`stock_summaries.db`) to ensure low-latency lookups and minimize external API calls.
- **`src/helper/`**: Shared constants, dictionary key mappings, and formatting utilities.
- **`backend/`**: A FastAPI REST layer (`api.py`) exposing screening results, lens breakdowns, and ticker evaluations to the client.
- **`frontend/`**: A React + TypeScript single-page application (built with Vite) for interactive ticker lookups, lens filtering, and portfolio analysis.

## How It Works

Instead of relying on a single monolithic formula, the engine evaluates equities across specialized thematic **lenses**:

- **Growth:** Measures top-line acceleration, earnings momentum, margin expansion, and capital efficiency.
- **Quality:** Evaluates structural moats via consistent gross/operating margins and high returns on equity/assets.
- **Health:** Checks balance sheet safety, leverage ratios, liquidity, and cash-to-debt buffers (calibrated for capital-intensive compounders).
- **Value:** Assesses traditional multiples (P/E, P/B, P/S) alongside dividend yield and financial safety margins.
- **GARP (Growth At a Reasonable Price):** Combines forward P/E, earnings growth projections, and PEG ratios to identify attractive entry points.
- **Scale Disruptor:** Highlights emerging, high-impact operational scaling dynamics.

## Prerequisites & Dependencies

### Backend (Python 3.10+)
- **API & Server:** `fastapi`, `uvicorn`
- **Data & Quantitative Processing:** `yfinance`, `pandas`, `numpy`
- **Storage:** `sqlite3` (standard library)

### Frontend (Node.js 18+)
- **Framework & Build Tool:** React, TypeScript, Vite (`npm`)

## Getting Started

### 1. Backend Setup & Run
From the project root directory, install the Python dependencies and start the FastAPI server via Uvicorn:

    pip install -r requirements.txt
    python -m uvicorn backend.api:app --reload

The API server runs by default at `[http://127.0.0.1:8000](http://127.0.0.1:8000)` (interactive Swagger docs available at `[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)`).

### 2. Frontend Setup & Run
Open a second terminal, navigate to the `frontend/` directory, install packages, and start the Vite development server:

    cd frontend
    npm install
    npm run dev

## Testing & Backtesting

The `tests/` directory contains scripts used to validate historical performance, run backtests, and manage the global equity universe:

- **`find_highest_scores.py`**: Primary top-of-funnel scanner that evaluates the watchlist through the multi-lens model and outputs ranked results.
- **`backtest_valuation.py` & `backtest_lens_scores.py`**: Evaluates how historical lens scores correlate with subsequent equity returns.
- **`backtest_performance_analysis.py`**: Computes multi-year CAGR metrics and generates portfolio CSV outputs for strategy validation.
- **`tickers.py`**: Maintains the global watchlist (~200+ tickers spanning US and international exchanges).

## Project Structure

```text
stock_analysis/
├── backend/
│   └── api.py
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── types/
│   │   ├── utils/
│   │   ├── App.tsx
│   │   └── main.tsx
│   └── package.json
├── src/
│   ├── caching/
│   │   └── cache.py
│   ├── data_cache/          # Local SQLite cache (git-ignored)
│   ├── helper/
│   │   ├── lens_keys.py
│   │   ├── process_data.py
│   │   ├── validate_stock_info.py
│   │   └── yf_keys.py
│   ├── info/
│   │   ├── extract_info.py
│   │   ├── info_config.py
│   │   └── market_cap_formatter.py
│   ├── valuations/
│   │   ├── average_score.py
│   │   ├── benchmark.py
│   │   ├── dimension.py
│   │   ├── garp_score.py
│   │   ├── growth_score.py
│   │   ├── health_score.py
│   │   ├── lenses.py
│   │   ├── quality_score.py
│   │   ├── scale_disruptor_score.py
│   │   ├── scoring.py
│   │   └── value_score.py
│   ├── yf_api/
│   │   └── api_fetch.py
│   ├── calculate_averages.py
│   ├── calculate_sp.py
│   ├── extract_tickers.py
│   └── stock_service.py
├── tests/
│   ├── backtest_lens_scores.py
│   ├── backtest_performance_analysis.py
│   ├── backtest_valuation.py
│   ├── find_highest_scores.py
│   └── tickers.py
├── .gitignore
├── main.py
├── README.md
└── requirements.txt