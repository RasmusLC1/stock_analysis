
import type { ScoreResult } from "../types/stock";

interface ScoreCardProps {
  title: string;
  result: ScoreResult | null;
}

const GRADE_COLORS: Record<string, { bg: string; fg: string }> = {
  A: { bg: "#166534", fg: "#ffffff" },
  B: { bg: "#15803d", fg: "#ffffff" },
  C: { bg: "#ca8a04", fg: "#ffffff" },
  D: { bg: "#ea580c", fg: "#ffffff" },
  F: { bg: "#dc2626", fg: "#ffffff" },
  "N/A": { bg: "#64748b", fg: "#ffffff" },
};

const LABELS: Record<string, string> = {
  growth_rate: "Growth",
  growth_consistency: "Consistency",
  profitability: "Profit",
  returns: "Returns",
  cash_quality: "Cash",
  balance_sheet: "Balance",
  valuation: "Value",
  Price: "Price",
  Earnings: "Earnings",
  "Book/Sales": "Book/Sales",
  EV: "EV",
  "FCF yield": "FCF",
  Safety: "Safety",
  Quality: "Quality",
  Upside: "Upside",
};

const LOW_COVERAGE = 0.6;

export default function ScoreCard({
  title,
  result,
}: ScoreCardProps) {
  const grade = result?.grade ?? "N/A";
  const colors = GRADE_COLORS[grade] ?? GRADE_COLORS["N/A"];

  const scoreText =
    result?.score == null ? "--" : result.score.toFixed(0);

  const coverage = result?.coverage ?? 0;

  const breakdown = result
    ? Object.entries(result.breakdown)
    : [];

  return (
    <section className="score-card">
      {/* Score badge */}
      <div
        className="score-badge"
        style={{
          backgroundColor: colors.bg,
          color: colors.fg,
        }}
      >
        <span className="score-number">{scoreText}</span>

        <span className="score-grade">
          {result ? `Grade ${grade}` : "No data"}
        </span>
      </div>

      {/* Score information */}
      <div className="score-content">
        <h3>{title}</h3>

        {!result ? (
          <p className="score-empty">
            Search for a ticker to evaluate.
          </p>
        ) : (
          <>
            {/* Individual scoring categories */}
            <div className="score-breakdown">
              {breakdown.map(([key, value]) => (
                <div className="score-metric" key={key}>
                  <span className="metric-label">
                    {LABELS[key] ?? key}
                  </span>

                  <span className="metric-value">
                    {value == null ? "--" : value.toFixed(0)}
                  </span>
                </div>
              ))}
            </div>

            {/* Coverage */}
            <div className="score-coverage">
              <div className="coverage-header">
                <span>Data coverage</span>
                <strong>{(coverage * 100).toFixed(0)}%</strong>
              </div>

              <div className="coverage-track">
                <div
                  className={`coverage-fill ${
                    coverage < LOW_COVERAGE ? "low" : ""
                  }`}
                  style={{
                    width: `${Math.max(0, Math.min(100, coverage * 100))}%`,
                  }}
                />
              </div>

              {coverage < LOW_COVERAGE && (
                <p className="coverage-warning">
                  ⚠ Low data coverage - treat with caution
                </p>
              )}
            </div>

            {/* Lens notes */}
            {result.notes.length > 0 && (
              <div className="score-notes">
                ⚡ {result.notes[0]}
              </div>
            )}
          </>
        )}
      </div>
    </section>
  );
}
