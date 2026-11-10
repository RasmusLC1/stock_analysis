import tkinter as tk
from tkinter import messagebox

from .score_card import ScoreCard
from .filtered_results import FilteredResultsPanel  # Import new component
from backend.src.valuations.lenses import LENSES
from backend.src.stock_service import StockService
from backend.src.calculate_sp.calculate_sp import CalculateSP500
from .theme import DARK, LIGHT, Theme
from .widgets import HeaderBar, SearchBar
from .helper.format import Formatter
from backend.src.helper.lens_keys import LensKeys as key


class StockAppGUI:
  """Composes the components and wires them to StockService."""

  def __init__(self, root: tk.Tk):
    self.root = root
    self.root.title("Stock Analysis Starter")
    self.root.geometry("500x580")
    self.root.minsize(440, 500)


    self.theme: Theme = DARK
    self.current_lens_name = tk.StringVar(value=key.AVERAGE)
    self.current_lens_name.trace_add("write", lambda *_: self.refresh_score_display())

    self.root.rowconfigure(4, weight=1)
    self.root.columnconfigure(0, weight=1)

    self.header = HeaderBar(self.root, on_toggle_theme=self.toggle_theme)
    self.header.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 10))

    self.search_bar = SearchBar(self.root, on_search=self.handle_search)
    self.search_bar.grid(row=1, column=0, sticky="ew", padx=15, pady=5)

    # Lens Selector Dropdown Frame
    self.control_frame = tk.Frame(self.root)
    self.control_frame.grid(row=2, column=0, sticky="ew", padx=15, pady=(5, 0))
    self.control_frame.columnconfigure(1, weight=1)

    self.lens_label = tk.Label(self.control_frame, text="Active Lens:", font=("Segoe UI", 9, "bold"))
    self.lens_label.grid(row=0, column=0, sticky="w", padx=(0, 10))

    self.lens_menu = tk.OptionMenu(self.control_frame, self.current_lens_name, *LENSES.keys())
    self.lens_menu.grid(row=0, column=1, sticky="w")

    # Dynamic Score Card
    self.score_card = ScoreCard(self.root, "Quality & Valuation Score")
    self.score_card.grid(row=3, column=0, sticky="ew", padx=15, pady=(5, 5))

    # New Filterable Results Component
    self.results = FilteredResultsPanel(self.root)
    self.results.grid(row=4, column=0, sticky="nsew", padx=15, pady=(5, 15))

    self.latest_data = None

    self._themed = [self.header, self.search_bar, self.score_card, self.results]

    self.apply_theme()
    self.sp500_values = CalculateSP500()


  def toggle_theme(self):
    self.theme = LIGHT if self.theme is DARK else DARK
    self.apply_theme()

  def apply_theme(self):
    self.root.configure(bg=self.theme.bg)
    
    # Style control frame
    self.control_frame.configure(bg=self.theme.bg)
    self.lens_label.configure(bg=self.theme.bg, fg=self.theme.fg)
    
    bg_color = getattr(self.theme, "card_bg", self.theme.bg)
    self.lens_menu.configure(
        bg=bg_color, 
        fg=self.theme.fg, 
        activebackground=bg_color,
        activeforeground=self.theme.fg
    )
    self.lens_menu["menu"].configure(
        bg=bg_color, 
        fg=self.theme.fg
    )

    # Apply theme to custom components
    for component in self._themed:
      component.apply_theme(self.theme)

  def handle_search(self):
    ticker = self.search_bar.get_ticker()
    try:
      self.latest_data = StockService.fetch_stock_summary(ticker)
    except Exception as e:
      messagebox.showerror("Error", str(e))
      return

    self.results.set_text(Formatter.format_summary(self.latest_data))
    self.refresh_score_display()

  def refresh_score_display(self):
    if not self.latest_data:
      return
    lens_key = self.current_lens_name.get()
    scoring_fn = LENSES.get(lens_key)
    if scoring_fn:
      result = scoring_fn(self.latest_data, self.sp500_values)
      self.score_card.caption.configure(text=f"{lens_key} Lens Score")
      self.score_card.show(result)