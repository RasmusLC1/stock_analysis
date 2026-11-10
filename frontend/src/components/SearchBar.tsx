
interface SearchBarProps {
  ticker: string;
  setTicker: (value: string) => void;
  onSearch: () => void;
  loading: boolean;
}

export default function SearchBar({
  ticker,
  setTicker,
  onSearch,
  loading,
}: SearchBarProps) {
  return (
    <div className="search-bar">
      <input
        value={ticker}
        onChange={(e) => setTicker(e.target.value.toUpperCase())}
        onKeyDown={(e) => {
          if (e.key === "Enter") onSearch();
        }}
        placeholder="Enter stock ticker (e.g. AAPL)"
      />

      <button onClick={onSearch} disabled={loading}>
        {loading ? "Loading..." : "Analyze"}
      </button>
    </div>
  );
}
