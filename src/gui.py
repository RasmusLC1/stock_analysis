import tkinter as tk
from tkinter import messagebox, ttk
from .stock_service import StockService


class StockAppGUI:

  def __init__(self, root: tk.Tk):
    self.root = root
    self.root.title("Stock Analysis Starter")
    self.root.geometry("500x400")
    self.root.minsize(440, 340)

    # Theme State (True = Dark Mode, False = Light Mode)
    self.is_dark_mode = True

    # Color Palettes
    self.themes = {
        "dark": {
            "bg": "#1e1e1e",
            "fg": "#e0e0e0",
            "entry_bg": "#2d2d2d",
            "entry_fg": "#ffffff",
            "text_bg": "#252526",
            "text_fg": "#d4d4d4",
            "btn_bg": "#333333",
            "btn_fg": "#ffffff",
            "labelframe_bg": "#1e1e1e",
            "labelframe_fg": "#e0e0e0",
        },
        "light": {
            "bg": "#f0f0f0",
            "fg": "#000000",
            "entry_bg": "#ffffff",
            "entry_fg": "#000000",
            "text_bg": "#f9f9f9",
            "text_fg": "#000000",
            "btn_bg": "#e0e0e0",
            "btn_fg": "#000000",
            "labelframe_bg": "#f0f0f0",
            "labelframe_fg": "#000000",
        },
    }

    # Configure grid weights
    self.root.rowconfigure(2, weight=1)
    self.root.columnconfigure(0, weight=1)

    self._create_widgets()
    self.apply_theme()

  def _create_widgets(self):
    # Header Frame
    self.header_frame = tk.Frame(self.root)
    self.header_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 10))
    self.header_frame.columnconfigure(0, weight=1)

    self.title_label = tk.Label(
        self.header_frame, text="Yahoo Finance Ticker Lookup", font=("Segoe UI", 14, "bold")
    )
    self.title_label.grid(row=0, column=0, sticky="w")

    self.theme_btn = tk.Button(
        self.header_frame,
        text="☀️ Light Mode",
        command=self.toggle_theme,
        font=("Segoe UI", 9),
        relief="groove",
        cursor="hand2",
    )
    self.theme_btn.grid(row=0, column=1, sticky="e")

    # Search Frame
    self.search_frame = tk.Frame(self.root)
    self.search_frame.grid(row=1, column=0, pady=5, sticky="ew", padx=15)
    self.search_frame.columnconfigure(1, weight=1)

    self.ticker_label = tk.Label(
        self.search_frame, text="Ticker Symbol:", font=("Segoe UI", 10)
    )
    self.ticker_label.grid(row=0, column=0, padx=(0, 10), sticky="w")

    self.ticker_entry = tk.Entry(self.search_frame, font=("Segoe UI", 10), relief="solid", bd=1)
    self.ticker_entry.grid(row=0, column=1, padx=5, sticky="ew", ipady=3)
    self.ticker_entry.insert(0, "AAPL")
    self.ticker_entry.bind("<Return>", lambda event: self.handle_search())

    self.search_btn = tk.Button(
        self.search_frame,
        text="Search",
        command=self.handle_search,
        font=("Segoe UI", 10),
        cursor="hand2",
    )
    self.search_btn.grid(row=0, column=2, padx=(8, 0))

    # Results Display Frame
    self.result_frame = tk.LabelField = tk.LabelFrame(
        self.root, text=" Summary Info ", font=("Segoe UI", 10, "bold")
    )
    self.result_frame.grid(
        row=2, column=0, padx=15, pady=(5, 15), sticky="nsew"
    )
    self.result_frame.rowconfigure(0, weight=1)
    self.result_frame.columnconfigure(0, weight=1)

    self.result_text = tk.Text(
        self.result_frame, font=("Consolas", 10), wrap="word", state="disabled", bd=0
    )
    self.result_text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    self.scrollbar = ttk.Scrollbar(
        self.result_frame, orient="vertical", command=self.result_text.yview
    )
    self.scrollbar.grid(row=0, column=1, sticky="ns", pady=5)
    self.result_text.configure(yscrollcommand=self.scrollbar.set)

  def toggle_theme(self):
    self.is_dark_mode = not self.is_dark_mode
    self.apply_theme()

  def apply_theme(self):
    theme_key = "dark" if self.is_dark_mode else "light"
    t = self.themes[theme_key]

    # Apply background color globally to root and all layout frames
    self.root.configure(bg=t["bg"])
    for widget in [
        self.header_frame,
        self.search_frame,
        self.result_frame,
    ]:
      widget.configure(bg=t["bg"])

    # Update Labels
    self.title_label.configure(bg=t["bg"], fg=t["fg"])
    self.ticker_label.configure(bg=t["bg"], fg=t["fg"])
    self.result_frame.configure(bg=t["labelframe_bg"], fg=t["labelframe_fg"])

    # Update Entry & Text fields
    self.ticker_entry.configure(
        bg=t["entry_bg"], fg=t["entry_fg"], insertbackground=t["fg"]
    )
    self.result_text.configure(
        bg=t["text_bg"], fg=t["text_fg"], insertbackground=t["fg"]
    )

    # Update Buttons & Toggle text
    self.search_btn.configure(bg=t["btn_bg"], fg=t["btn_fg"])
    if self.is_dark_mode:
      self.theme_btn.configure(
          text="☀️ Light Mode", bg=t["btn_bg"], fg=t["btn_fg"]
      )
    else:
      self.theme_btn.configure(
          text="🌙 Dark Mode", bg=t["btn_bg"], fg=t["btn_fg"]
      )

  def handle_search(self):
    ticker_symbol = self.ticker_entry.get().strip()
    try:
      data = StockService.fetch_stock_summary(ticker_symbol)

      output = (
          f"Company: {data['name']} ({data['symbol']})\n"
          f"Sector: {data['sector']} | Industry: {data['industry']}\n"
          f"----------------------------------------\n"
          f"Current Price: {data['price']} {data['currency']}\n"
          f"Market Cap:    {data['market_cap']}\n"
          f"Trailing P/E:  {data['pe_ratio']}\n"
      )

      self.result_text.configure(state="normal")
      self.result_text.delete("1.0", tk.END)
      self.result_text.insert(tk.END, output)
      self.result_text.configure(state="disabled")

    except Exception as e:
      messagebox.showerror("Error", str(e))