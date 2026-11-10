
import { useState } from "react";
import ScoreCard from "./components/ScoreCard";
import FilteredResultsPanel from "./components/FilteredResultsPanel";
import type { ScoreResult } from "./types/stock";
import "./App.css";

function App() {
  const [darkMode, setDarkMode] = useState(true);

  const sampleResult: ScoreResult = {
    score: 87,
    grade: "A",
    breakdown: {
      growth_rate: 85,
      profitability: 94,
      returns: 88,
      valuation: 82,
    },
    coverage: 0.92,
    notes: ["Strong profitability and consistent growth."],
  };

  const sampleText = `
VALUATION
P/E Ratio:                 28.4
P/B Ratio:                 45.2
EV/EBITDA:                 22.1

PROFITABILITY
Return on Equity:          147.2%
Operating Margin:          31.5%
Net Profit Margin:         24.1%

GROWTH
Revenue Growth:            6.1%
Earnings Growth:           8.4%

FINANCIAL HEALTH
Debt / Equity:             1.8
Current Ratio:             0.9

DIVIDENDS
Dividend Yield:            0.42%
Payout Ratio:              15.8%
`;

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

        <div className="search-bar">
          <input
            placeholder="Enter stock ticker (e.g. AAPL)"
            defaultValue="AAPL"
          />
          <button>Analyze</button>
        </div>

        <ScoreCard
          title="Growth Score"
          result={sampleResult}
        />

        <FilteredResultsPanel text={sampleText} />
      </main>
    </div>
  );
}

export default App;
