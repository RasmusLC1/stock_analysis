
import { useMemo, useState } from "react";

interface FilteredResultsPanelProps {
  text: string;
}

export default function FilteredResultsPanel({
  text,
}: FilteredResultsPanelProps) {
  const [query, setQuery] = useState("");

  const filteredLines = useMemo(() => {
    const lines = text.split(/\r?\n/);
    const search = query.trim().toLowerCase();

    if (!search) return lines;

    const cleanQuery = search
      .replace(/[\/\-_ ]/g, "");

    const queryTerms = search.split(/\s+/);

    return lines.filter((line) => {
      const lowerLine = line.toLowerCase();

      const cleanLine = lowerLine
        .replace(/[\/\-_ ]/g, "");

      const isDirect = lowerLine.includes(search);

      const isCleanMatch =
        cleanQuery.length > 0 &&
        cleanLine.includes(cleanQuery);

      const isAllTerms = queryTerms.every((term) =>
        lowerLine.includes(term)
      );

      return isDirect || isCleanMatch || isAllTerms;
    });
  }, [text, query]);

  return (
    <section className="results-panel">
      <div className="filter-bar">
        <label htmlFor="metric-filter">Filter:</label>

        <input
          id="metric-filter"
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search financial metrics..."
        />

        {query && (
          <button
            className="clear-filter"
            onClick={() => setQuery("")}
            title="Clear filter"
          >
            ×
          </button>
        )}
      </div>

      <div className="results-content">
        {filteredLines.length > 0 ? (
          filteredLines.map((line, index) => (
            <div className="result-line" key={index}>
              {line || "\u00A0"}
            </div>
          ))
        ) : (
          <p className="empty-results">
            No matching metrics found.
          </p>
        )}
      </div>
    </section>
  );
}
