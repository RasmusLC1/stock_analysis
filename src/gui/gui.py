import tkinter as tk
from tkinter import messagebox

from .growth_card import GrowthScoreCard
from src.valuations.growth_score import score_company
from ..stock_service import StockService
from .theme import DARK, LIGHT, Theme
from .widgets import HeaderBar, ResultsPanel, SearchBar
from .helper.format import Formatter


class StockAppGUI:
  """Composes the components and wires them to StockService. No widget details live here."""

  def __init__(self, root: tk.Tk):
    self.root = root
    self.root.title("Stock Analysis Starter")
    self.root.geometry("500x480")
    self.root.minsize(440, 420)

    self.theme: Theme = DARK

    self.root.rowconfigure(3, weight=1)  # results panel takes the spare space
    self.root.columnconfigure(0, weight=1)

    self.header = HeaderBar(self.root, on_toggle_theme=self.toggle_theme)
    self.header.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 10))

    self.search_bar = SearchBar(self.root, on_search=self.handle_search)
    self.search_bar.grid(row=1, column=0, sticky="ew", padx=15, pady=5)

    self.score_card = GrowthScoreCard(self.root)
    self.score_card.grid(row=2, column=0, sticky="ew", padx=15, pady=(10, 5))

    self.results = ResultsPanel(self.root)
    self.results.grid(row=3, column=0, sticky="nsew", padx=15, pady=(5, 15))

    self._themed = [self.header, self.search_bar, self.score_card, self.results]
    self.apply_theme()

  # --- theming -------------------------------------------------------------
  def toggle_theme(self):
    self.theme = LIGHT if self.theme is DARK else DARK
    self.apply_theme()

  def apply_theme(self):
    self.root.configure(bg=self.theme.bg)
    for component in self._themed:
      component.apply_theme(self.theme)

  # --- actions -------------------------------------------------------------
  def handle_search(self):
    ticker = self.search_bar.get_ticker()
    try:
      data = StockService.fetch_stock_summary(ticker)  # returns an InfoConfig
      result = score_company(data)
    except Exception as e:
      messagebox.showerror("Error", str(e))
      return

    self.results.set_text(Formatter.format_summary(data))
    self.score_card.show(result)

