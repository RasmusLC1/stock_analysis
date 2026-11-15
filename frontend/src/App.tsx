import { useState } from "react";

import Header from "./components/Header";
import SearchBar from "./components/SearchBar";
import LensSelector from "./components/LensSelector";
import StockHeader from "./components/StockHeader";
import WelcomeMessage from "./components/WelcomeMessage";
import ScoreCard from "./components/ScoreCard";
import FilteredResultsPanel from "./components/FilteredResultsPanel";
import BackendStatus from "./components/BackendStatus";

import { useStockAnalysis } from "./hooks/useStockAnalysis";
import { formatStockData } from "./utils/formatStockData";
import { LENSES } from "./constants/lenses";

import "./App.css";

function App() {
  const [darkMode, setDarkMode] = useState(true);
  const s = useStockAnalysis();

  return (
    <div className={darkMode ? "app dark" : "app light"}>
      <Header darkMode={darkMode} onToggle={() => setDarkMode((d) => !d)} />

      <main className="dashboard">
        <h2>Stock Overview</h2>

        <BackendStatus />

        <SearchBar
          ticker={s.ticker}
          loading={s.loading}
          onChange={s.setTicker}
          onSubmit={s.analyze}
        />

        <LensSelector
          lenses={LENSES}
          active={s.activeLens}
          onChange={s.changeLens}
        />

        {s.error && <div className="error-message">{s.error}</div>}

        {s.loading && (
          <p className="loading-message">Retrieving stock information...</p>
        )}

        {s.stock && (
          <>
            <StockHeader stock={s.stock} />

            <ScoreCard
              title={`${s.activeLens} Lens Score`}
              result={s.score}
              isLoading={s.scoreLoading}
            />

            <FilteredResultsPanel text={formatStockData(s.stock)} />
          </>
        )}

        {!s.stock && !s.loading && !s.error && <WelcomeMessage />}
      </main>
    </div>
  );
}

export default App;
