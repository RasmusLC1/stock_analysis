import tkinter as tk
from typing import Optional
from .theme import Theme


class FilteredResultsPanel(tk.Frame):
    """A panel containing a search filter bar and a scrollable text view for financial data."""

    def __init__(self, parent):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self._raw_text: str = ""
        self._theme: Optional[Theme] = None

        # Filter entry search bar at the top of the panel
        filter_frame = tk.Frame(self)
        filter_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        filter_frame.columnconfigure(1, weight=1)

        self.filter_label = tk.Label(filter_frame, text="Filter:", font=("Segoe UI", 8, "bold"))
        self.filter_label.grid(row=0, column=0, sticky="w", padx=(0, 6))

        self.filter_var = tk.StringVar()
        self.filter_var.trace_add("write", lambda *_: self._apply_filter())
        
        self.filter_entry = tk.Entry(filter_frame, textvariable=self.filter_var, font=("Segoe UI", 9))
        self.filter_entry.grid(row=0, column=1, sticky="ew")

        # Text display area below the filter
        text_frame = tk.Frame(self)
        text_frame.grid(row=1, column=0, sticky="nsew")
        text_frame.rowconfigure(0, weight=1)
        text_frame.columnconfigure(0, weight=1)

        self.text_widget = tk.Text(
            text_frame, 
            wrap="word", 
            font=("Consolas", 9), 
            borderwidth=0, 
            highlightthickness=0
        )
        self.text_widget.grid(row=0, column=0, sticky="nsew")
        self.text_widget.configure(state="disabled")

        # Optional vertical scrollbar
        scrollbar = tk.Scrollbar(text_frame, command=self.text_widget.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.text_widget.configure(yscrollcommand=scrollbar.set)

    def set_text(self, text: str):
        """Load raw text into the panel and apply current filter."""
        self._raw_text = text
        self._apply_filter()

    def _apply_filter(self):
        query = self.filter_var.get().strip().lower()
        lines = self._raw_text.splitlines()

        if not query:
            self._update_text_display(lines)
            return

        # 1. Clean query for fuzzy matching (remove punctuation like /, -, _, spaces)
        clean_query = query.replace("/", "").replace("-", "").replace(" ", "")
        query_terms = query.split()

        filtered_lines = []
        for line in lines:
            line_lower = line.lower()
            clean_line = line_lower.replace("/", "").replace("-", "").replace(" ", "")

            # Match criteria (any of these will show the line):
            # A) Direct substring match (e.g. "margin")
            is_direct = query in line_lower
            
            # B) Punctuation-stripped match (e.g. searching "pe" catches "p/e")
            is_clean_match = clean_query in clean_line
            
            # C) Multi-term keyword match (e.g. searching "net profit" catches lines containing both)
            is_all_terms = all(term in line_lower for term in query_terms)

            if is_direct or is_clean_match or is_all_terms:
                filtered_lines.append(line)

        self._update_text_display(filtered_lines)

    def _update_text_display(self, lines: list[str]):
        display_text = "\n".join(lines)
        self.text_widget.configure(state="normal")
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert("1.0", display_text)
        self.text_widget.configure(state="disabled")

    def apply_theme(self, t: Theme):
        self._theme = t
        self.configure(bg=t.bg)
        
        # Style filter elements
        for child in self.winfo_children():
            try:
                child.configure(bg=t.bg)
            except tk.TclError:
                pass

        self.filter_label.configure(bg=t.bg, fg=t.fg)
        self.filter_entry.configure(
            bg=t.card_bg if hasattr(t, "card_bg") else t.bg,
            fg=t.fg,
            insertbackground=t.fg
        )

        # Style text display box
        self.text_widget.configure(
            bg=t.card_bg if hasattr(t, "card_bg") else t.bg,
            fg=t.fg,
            selectbackground=t.muted_fg,
            selectforeground=t.bg
        )