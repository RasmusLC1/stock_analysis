import tkinter as tk
from tkinter import ttk
from typing import Callable

from .theme import Theme


class HeaderBar(tk.Frame):
  """Title on the left, theme toggle button on the right."""

  def __init__(self, parent, on_toggle_theme: Callable[[], None]):
    super().__init__(parent)
    self.columnconfigure(0, weight=1)

    self.title_label = tk.Label(
        self, text="Yahoo Finance Ticker Lookup", font=("Segoe UI", 14, "bold")
    )
    self.title_label.grid(row=0, column=0, sticky="w")

    self.theme_btn = tk.Button(
        self,
        command=on_toggle_theme,
        font=("Segoe UI", 9),
        relief="groove",
        cursor="hand2",
    )
    self.theme_btn.grid(row=0, column=1, sticky="e")

  def apply_theme(self, t: Theme):
    self.configure(bg=t.bg)
    self.title_label.configure(bg=t.bg, fg=t.fg)
    self.theme_btn.configure(text=t.toggle_text, bg=t.btn_bg, fg=t.btn_fg)


class SearchBar(tk.Frame):
  """Ticker label + entry + search button. Enter key also triggers search."""

  def __init__(
      self, parent, on_search: Callable[[], None], default_ticker: str = "AAPL"
  ):
    super().__init__(parent)
    self.columnconfigure(1, weight=1)

    self.label = tk.Label(self, text="Ticker Symbol:", font=("Segoe UI", 10))
    self.label.grid(row=0, column=0, padx=(0, 10), sticky="w")

    self.entry = tk.Entry(self, font=("Segoe UI", 10), relief="solid", bd=1)
    self.entry.grid(row=0, column=1, padx=5, sticky="ew", ipady=3)
    self.entry.insert(0, default_ticker)
    self.entry.bind("<Return>", lambda _event: on_search())

    self.button = tk.Button(
        self,
        text="Search",
        command=on_search,
        font=("Segoe UI", 10),
        cursor="hand2",
    )
    self.button.grid(row=0, column=2, padx=(8, 0))

  def get_ticker(self) -> str:
    return self.entry.get().strip().upper()

  def apply_theme(self, t: Theme):
    self.configure(bg=t.bg)
    self.label.configure(bg=t.bg, fg=t.fg)
    self.entry.configure(bg=t.entry_bg, fg=t.entry_fg, insertbackground=t.fg)
    self.button.configure(bg=t.btn_bg, fg=t.btn_fg)


class ResultsPanel(tk.LabelFrame):
  """Read-only scrollable text area for the summary output."""

  def __init__(self, parent):
    super().__init__(parent, text=" Summary Info ", font=("Segoe UI", 10, "bold"))
    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)

    self.text = tk.Text(
        self, font=("Consolas", 10), wrap="word", state="disabled", bd=0
    )
    self.text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.text.yview)
    self.scrollbar.grid(row=0, column=1, sticky="ns", pady=5)
    self.text.configure(yscrollcommand=self.scrollbar.set)

  def set_text(self, content: str):
    self.text.configure(state="normal")
    self.text.delete("1.0", tk.END)
    self.text.insert(tk.END, content)
    self.text.configure(state="disabled")

  def apply_theme(self, t: Theme):
    self.configure(bg=t.bg, fg=t.fg)
    self.text.configure(bg=t.text_bg, fg=t.text_fg, insertbackground=t.fg)