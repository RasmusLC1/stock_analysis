# Stock Analysis tool & Quantitative Backtesting Engine

A modular Python engine designed to scan global markets, evaluate companies across multiple fundamental dimensions, and surface high-conviction secular compounders while filtering out cyclical value traps.

## Architecture

The codebase is built with a clean separation of concerns, dividing data ingestion, core scoring, local caching, and user interface layers:

*   **`src/valuations/`**: The heart of the scoring engine. It houses individual thematic lenses (Growth, Quality, Health, Value, GARP, and Scale Disruptor) that normalize raw fundamentals onto a $0–100$ scale before aggregating them into a weighted composite score.
*   **`src/yf_api/` & `src/info/`**: Handles external data extraction via `yfinance` (`api_fetch.py`) and maps out raw metrics using modular config definitions (`info_config.py`).
*   **`src/caching/` & `src/data_cache/`**: Manages local data persistence using a SQLite database (`stock_summaries.db`) to ensure quick lookups without hammering external APIs.
*   **`src/gui/`**: A native desktop interface (`gui.py`, `score_card.py`, `filtered_results.py`) for visual inspection, card views, and interactive result filtering.
*   **`src/helper/`**: Shared constants, dictionary key mappings, and formatting utilities.

## How It Works

Instead of relying on a single monolithic formula, the engine breaks down stock analysis into specialized thematic **lenses**:

*   **Growth:** Measures top-line acceleration, earnings momentum, margin expansion, and capital efficiency.
*   **Quality:** Evaluates structural moats via consistent gross/operating margins and high returns on equity/assets.
*   **Health:** Checks balance sheet safety, leverage ratios, liquidity, and cash-to-debt buffers (calibrated for asset-heavy compounders).
*   **Value:** Assesses traditional multiples (P/E, P/B, P/S) alongside dividend yield and financial safety margins.
*   **GARP (Growth At a Reasonable Price):** Combines forward P/E, growth projections, and PEG ratios to find reasonable entry points.
*   **Scale Disruptor:** Highlights emerging or high-impact operational dynamics.

## Testing & Backtesting

The `tests/` directory contains a dedicated suite of scripts used to validate historical performance, run historical backtests, and manage the global stock universe:

*   **`find_highest_scores.py`**: The primary top-of-funnel scanner that runs the universe through the multi-lens model and outputs ranked results.
*   **`backtest_valuation.py` & `backtest_lens_scores.py`**: Evaluates how historical model scores correlate with subsequent stock performance.
*   **`backtest_performance_analysis.py`**: Computes multi-year CAGR metrics, generating portfolio CSV outputs (`top_10_portfolios_3yr_cagr.csv`) for strategy validation.
*   **`tickers.py`**: Maintains the global watchlist (~200+ tickers spanning international exchanges).

## Project Structure

```text
stock_analysis/
├── main.py
├── README.md
├── src/
│   ├── stock_service.py
│   ├── caching/
│   ├── data_cache/         # Local SQLite cache (git-ignored)
│   ├── gui/                # Desktop user interface
│   ├── helper/             # Utility keys and formatters
│   ├── info/               # Metric extraction configs
│   ├── valuations/       # Core scoring lenses & logic
│   └── yf_api/           # yfinance API wrappers
├── tests/                # Backtests, performance analysis, & scanning scripts
└── tickers.py            # Global watch list configuration