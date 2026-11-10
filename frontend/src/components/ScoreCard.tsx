
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

export default function ScoreCard({
  title,
  result,
}: ScoreCardProps) {
  const grade = result?.grade ?? "N/A";
  const colors = GRADE_COLORS[grade] ?? GRADE_COLORS["N/A"];

  const scoreText =
    result?.score == null ? "--" : result.score.toFixed(0);

  const breakdown = result
    ? Object.entries(result.breakdown)
        .map(([key, value]) =>
          `${LABELS[key] ?? key} ${value == null ? "-" : value.toFixed(0)}`
        )
        .join("  ·  ")
    : "";

  const detail = !result
    ? "Search for a ticker to evaluate."
    : [
        breakdown,
        result.coverage < 0.6
          ? `⚠ Low data coverage (${(result.coverage * 100).toFixed(0)}%) - treat with caution`
          : `Data coverage ${(result.coverage * 100).toFixed(0)}%`,
        result.notes.length > 0 ? `⚡ ${result.notes[0]}` : "",
      ]
        .filter(Boolean)
        .join("\n");

  return (
    <section className="score-card">
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

      <div className="score-content">
        <h3>{title}</h3>
        <p className="score-detail">{detail}</p>
      </div>
    </section>
  );
}
