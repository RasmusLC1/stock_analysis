
import { useState, type FormEvent } from "react";

import ScoreCard from "./components/ScoreCard";
import FilteredResultsPanel from "./components/FilteredResultsPanel";
import BackendStatus from "./components/BackendStatus";

import {
  fetchStock,
  fetchStockScore,
} from "./services/stockApi";

import type { StockData } from "./services/stockApi";
import type { ScoreResult } from "./types/stock";

import "./App.css";

function App() {
  // Theme
  const [darkMode, setDarkMode] = useState(true);

  // Stock information
  const [ticker, setTicker] = useState("AAPL");
  const [stock, setStock] = useState<StockData | null>(null);

  // Loading and error states
  const [loading, setLoading] = useState(false);
  const [scoreLoading, setScoreLoading] = useState(false);
  const [error, setError] = useState("");

  // Score information
  const [score, setScore] = useState<ScoreResult | null>(null);

  // Available scoring lenses
  const availableLenses = [
    "Average",
    "Growth",
    "Value",
    "Health",
    "Quality",
    "Garp",
    "Scale Disruptor",
  ];

  const [activeLens, setActiveLens] = useState("Average");

  // Handle stock analysis
  async function handleAnalyze(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const searchTicker = ticker.trim();

    if (!searchTicker) {
      setError("Please enter a stock ticker.");
      return;
    }

    setLoading(true);
    setScoreLoading(false);
    setError("");
    setStock(null);
    setScore(null);

    try {
      const [stockResult, scoreResult] = await Promise.all([
        fetchStock(searchTicker),
        fetchStockScore(searchTicker, activeLens),
      ]);

      setStock(stockResult);
      setScore(scoreResult);

    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "An unexpected error occurred."
      );
    } finally {
      setLoading(false);
    }
  }

  // Handle changing the scoring lens
  async function handleLensChange(lens: string) {
    setActiveLens(lens);

    if (!stock) {
      return;
    }

    setScoreLoading(true);
    setError("");

    try {
      const result = await fetchStockScore(
        stock.ticker_symbol,
        lens
      );

      setScore(result);

    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to calculate stock score."
      );
    } finally {
      setScoreLoading(false);
    }
  }

  // Format stock data for the results panel
  function formatStockData(data: StockData): string {
    const sections: Record<string, string[]> = {
      "COMPANY INFORMATION": [
        "name",
        "ticker_symbol",
        "sector",
        "industry",
        "currency",
        "financial_currency",
        "summary",
        "website",
      ],

      "VALUATION & PRICING": [
        "price",
        "previous_close",
        "open_price",
        "day_low",
        "day_high",
        "market_cap",
        "enterprise_value",
        "pe_ratio",
        "forward_pe",
        "peg_ratio",
        "price_to_sales",
        "price_to_book",
        "enterprise_to_revenue",
        "enterprise_to_ebitda",
      ],

      "PROFITABILITY & GROWTH": [
        "profit_margins",
        "gross_margins",
        "operating_margins",
        "ebitda_margins",
        "return_on_assets",
        "return_on_equity",
        "total_revenue",
        "revenue_growth",
        "gross_profits",
        "ebitda",
        "net_income",
        "earnings_growth",
        "eps_trailing",
        "eps_forward",
      ],

      "FINANCIAL HEALTH": [
        "free_cashflow",
        "operating_cashflow",
        "total_cash",
        "total_debt",
        "debt_to_equity",
        "current_ratio",
        "quick_ratio",
        "book_value",
      ],

      "DIVIDENDS & MARKET SENTIMENT": [
        "dividend_rate",
        "dividend_yield",
        "payout_ratio",
        "beta",
        "recommendation_key",
        "number_of_analysts",
        "target_mean_price",
      ],

      "TECHNICALS & SHARE STRUCTURE": [
        "fifty_two_week_low",
        "fifty_two_week_high",
        "fifty_day_average",
        "two_hundred_day_average",
        "volume",
        "average_volume",
        "shares_outstanding",
        "float_shares",
        "short_ratio",
        "short_percent_of_float",
        "held_percent_insiders",
        "held_percent_institutions",
      ],
    };

    return Object.entries(sections)
      .map(([section, fields]) => {
        const lines = fields
          .filter(
            (field) =>
              data[field] !== null &&
              data[field] !== undefined
          )
          .map((field) => {
            const label = field
              .replace(/_/g, " ")
              .replace(/\b\w/g, (letter) =>
                letter.toUpperCase()
              );

            return `${label}: ${data[field]}`;
          });

        return lines.length > 0
          ? `${section}\n${lines.join("\n")}`
          : "";
      })
      .filter(Boolean)
      .join("\n\n");
  }

  return (
    <div className={darkMode ? "app dark" : "app light"}>
      <header className="header">
        <h1>Stock Analysis</h1>

        <button
          onClick={() => setDarkMode(!darkMode)}
          className="theme-button"
        >
          {darkMode ? "☀ Light mode" : "☾ Dark mode"}
        </button>
      </header>

      <main className="dashboard">
        <h2>Stock Overview</h2>

        <BackendStatus />

        {/* Stock search */}
        <form
          className="search-bar"
          onSubmit={handleAnalyze}
        >
          <input
            type="text"
            placeholder="Enter stock ticker (e.g. AAPL)"
            value={ticker}
            onChange={(event) =>
              setTicker(event.target.value)
            }
          />

          <button type="submit" disabled={loading}>
            {loading ? "Analyzing..." : "Analyze"}
          </button>
        </form>

        {/* Lens selector */}
        <div className="lens-selector">
          <label htmlFor="lens-select">
            Active Lens:
          </label>

          <select
            id="lens-select"
            value={activeLens}
            onChange={(event) =>
              handleLensChange(event.target.value)
            }
          >
            {availableLenses.map((lens) => (
              <option key={lens} value={lens}>
                {lens}
              </option>
            ))}
          </select>
        </div>

        {/* Error message */}
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {/* Loading message */}
        {loading && (
          <p className="loading-message">
            Retrieving stock information...
          </p>
        )}

        {/* Stock results */}
        {stock && (
          <>
            <section className="stock-header">
              <h2>
                {stock.name || stock.ticker_symbol}
              </h2>

              <p>
                {stock.ticker_symbol}
                {stock.sector
                  ? ` · ${stock.sector}`
                  : ""}
                {stock.currency
                  ? ` · ${stock.currency}`
                  : ""}
              </p>

              <h3>
                {stock.price ?? "N/A"}{" "}
                {stock.currency ?? ""}
              </h3>
            </section>

            {/* Scoring results */}
            <ScoreCard
              title={`${activeLens} Lens Score`}
              result={score}
              isLoading={scoreLoading}
            />

            {/* Full stock information */}
            <FilteredResultsPanel
              text={formatStockData(stock)}
            />
          </>
        )}

        {/* Welcome screen */}
        {!stock && !loading && !error && (
          <div className="welcome-message">
            <h3>Welcome to Stock Analysis</h3>

            <p>
              Enter a stock ticker above to retrieve
              financial information from your Python backend.
            </p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
