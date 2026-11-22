import type { FormEvent } from "react";

interface SearchBarProps {
  ticker: string;
  loading: boolean;
  onChange: (value: string) => void;
  onSubmit: () => void;
}

function SearchBar({ ticker, loading, onChange, onSubmit }: SearchBarProps) {
  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onSubmit();
  }

  return (
    <form className="search-bar" onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Enter stock ticker (e.g. AAPL)"
        value={ticker}
        onChange={(event) => onChange(event.target.value)}
      />

      <button type="submit" disabled={loading}>
        {loading ? "Analyzing..." : "Analyze"}
      </button>
    </form>
  );
}

export default SearchBar;
