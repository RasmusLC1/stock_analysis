import tkinter as tk
from typing import Optional
from src.valuations.scoring import ScoreResult
from .theme import GRADE_COLORS, Theme

LOW_COVERAGE = 0.6

_LABELS = {
    # Growth keys
    "growth_rate": "Growth",
    "growth_consistency": "Consistency",
    "profitability": "Profit",
    "returns": "Returns",
    "cash_quality": "Cash",
    "balance_sheet": "Balance",
    "valuation": "Value",
    "Price": "Price",
    # Value keys
    "Earnings": "Earnings",
    "Book/Sales": "Book/Sales",
    "EV": "EV",
    "FCF yield": "FCF",
    "Safety": "Safety",
    "Quality": "Quality",
    "Upside": "Upside",
}


class ScoreCard(tk.Frame):
  """A card showing a score and grade for a specific lens (Growth, Value, etc.)."""

  def __init__(self, parent, title: str):
    super().__init__(parent)
    self.columnconfigure(1, weight=1)

    # Colored badge: big score + grade letter
    self.badge = tk.Frame(self, width=110, height=64)
    self.badge.grid(row=0, column=0, rowspan=2, sticky="ns")
    self.badge.grid_propagate(False)
    self.badge.columnconfigure(0, weight=1)
    self.badge.rowconfigure(0, weight=1)

    self.score_label = tk.Label(self.badge, font=("Segoe UI", 20, "bold"))
    self.score_label.grid(row=0, column=0)
    self.grade_label = tk.Label(self.badge, font=("Segoe UI", 9, "bold"))
    self.grade_label.grid(row=1, column=0, pady=(0, 6))

    # Text next to the badge
    self.caption = tk.Label(
        self, text=title, font=("Segoe UI", 10, "bold"), anchor="w"
    )
    self.caption.grid(row=0, column=1, sticky="sw", padx=(12, 0))

    self.detail = tk.Label(
        self, font=("Segoe UI", 8), anchor="nw", justify="left", wraplength=340
    )
    self.detail.grid(row=1, column=1, sticky="new", padx=(12, 0))

    self._theme: Optional[Theme] = None
    self.clear()

  def show(self, result: ScoreResult):
    bg, fg = GRADE_COLORS.get(result.grade, GRADE_COLORS["N/A"])
    score_text = "--" if result.score is None else f"{result.score:.0f}"
    self._paint_badge(bg, fg, score_text, f"Grade {result.grade}")

    parts = [
        f"{_LABELS.get(k, k)} {'-' if v is None else f'{v:.0f}'}"
        for k, v in result.breakdown.items()
    ]
    text = "  ·  ".join(parts)
    if result.coverage < LOW_COVERAGE:
      text += f"\n⚠ Low data coverage ({result.coverage:.0%}) - treat with caution"
    else:
      text += f"\nData coverage {result.coverage:.0%}"
      
    # Append any lens notes (e.g. Value trap warnings)
    if result.notes:
      text += f"\n⚡ {result.notes[0]}"

    self.detail.configure(text=text)

  def clear(self):
    bg, fg = GRADE_COLORS["N/A"]
    self._paint_badge(bg, fg, "--", "No data")
    self.detail.configure(text="Search for a ticker to evaluate.")

  def apply_theme(self, t: Theme):
    self._theme = t
    self.configure(bg=t.bg)
    self.caption.configure(bg=t.bg, fg=t.fg)
    self.detail.configure(bg=t.bg, fg=t.muted_fg)

  def _paint_badge(self, bg: str, fg: str, score_text: str, grade_text: str):
    self.badge.configure(bg=bg)
    self.score_label.configure(text=score_text, bg=bg, fg=fg)
    self.grade_label.configure(text=grade_text, bg=bg, fg=fg)