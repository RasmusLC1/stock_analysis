import calendar
import tkinter as tk
from datetime import date
from typing import Callable, Optional

from .theme import Theme

ACCENT_BG = "#1976d2"  # selected day / year
ACCENT_FG = "#ffffff"
DEFAULT_MIN_YEAR = 1970  # earliest year in the year chooser when no min_date is given
YEARS_PER_PAGE = 12  # 4 rows x 3 columns


class DatePicker(tk.Frame):
  """
  A button showing the selected date. Clicking it opens a popup month calendar.
  Click the "Month Year" title in the popup to jump to a year chooser.

    picker = DatePicker(parent, on_change=handle_date_change)
    picker.get_date()      # -> datetime.date
    picker.set_date(d)
    picker.Reset()         # back to today

  Dates after `max_date` (default: today) and before `min_date` are disabled.
  Uses only the standard library, so no extra pip install is needed.
  """

  def __init__(
      self,
      parent,
      on_change: Optional[Callable[[date], None]] = None,
      initial: Optional[date] = None,
      min_date: Optional[date] = None,
      max_date: Optional[date] = None,
      label: str = "Date:",
  ):
    super().__init__(parent)
    self._on_change = on_change
    self._min = min_date
    self._max = max_date or date.today()
    self._date = self._clamp(initial or date.today())
    self._theme: Optional[Theme] = None
    self._popup: Optional["_CalendarPopup"] = None

    self.label = tk.Label(self, text=label, font=("Segoe UI", 9, "bold"))
    self.label.grid(row=0, column=0, padx=(0, 8))

    self.button = tk.Button(
        self,
        text=self._format(self._date),
        command=self._toggle_popup,
        font=("Segoe UI", 10),
        cursor="hand2",
        width=12,
    )
    self.button.grid(row=0, column=1)

    self.reset_button = tk.Button(
        self,
        text="↺",
        command=self.Reset,
        font=("Segoe UI", 10),
        cursor="hand2",
        width=3,
    )
    self.reset_button.grid(row=0, column=2, padx=(4, 0))

  # --- public API ----------------------------------------------------------
  def get_date(self) -> date:
    return self._date

  def set_date(self, value: date, notify: bool = True):
    value = self._clamp(value)
    changed = value != self._date
    self._date = value
    self.button.configure(text=self._format(value))
    if changed and notify and self._on_change:
      self._on_change(value)

  def Reset(self):
    if self._popup is not None and self._popup.winfo_exists():
      self._popup.destroy()  # otherwise an open calendar would still highlight the old day
    self._popup = None
    self.set_date(date.today())

  def apply_theme(self, t: Theme):
    self._theme = t
    self.configure(bg=t.bg)
    self.label.configure(bg=t.bg, fg=t.fg)
    for b in (self.button, self.reset_button):
      b.configure(
          bg=t.btn_bg, fg=t.btn_fg, activebackground=t.btn_bg, activeforeground=t.btn_fg
      )
    if self._popup is not None and self._popup.winfo_exists():
      self._popup.apply_theme(t)

  # --- internals -----------------------------------------------------------
  @staticmethod
  def _format(d: date) -> str:
    return d.strftime("%Y-%m-%d") + "  📅"

  def _clamp(self, d: date) -> date:
    if self._max and d > self._max:
      return self._max
    if self._min and d < self._min:
      return self._min
    return d

  def is_allowed(self, d: date) -> bool:
    return not ((self._max and d > self._max) or (self._min and d < self._min))

  def year_bounds(self) -> tuple[int, int]:
    """(first, last) year offered in the year chooser."""
    first = self._min.year if self._min else DEFAULT_MIN_YEAR
    return first, self._max.year

  def _toggle_popup(self):
    if self._popup is not None and self._popup.winfo_exists():
      self._popup.destroy()
      self._popup = None
      return
    self._popup = _CalendarPopup(self, self._date, self._theme)

  def _picked(self, d: date):
    self.set_date(d)
    if self._popup is not None and self._popup.winfo_exists():
      self._popup.destroy()
    self._popup = None


class _CalendarPopup(tk.Toplevel):
  """
  Two views in one popup:
    "days"  - month grid with prev/next month arrows and a Today shortcut
    "years" - 12 years per page; arrows page through years. Click the title to
              toggle between the two views, click a year to go back to its months.
  """

  def __init__(self, picker: DatePicker, selected: date, theme: Optional[Theme]):
    super().__init__(picker)
    self._picker = picker
    self._selected = selected
    self._year, self._month = selected.year, selected.month
    self._mode = "days"  # "days" or "years"
    self._page = 0  # first year shown in the year view
    self._cal = calendar.Calendar(firstweekday=0)  # weeks start on Monday

    self.title("Select date")
    self.resizable(False, False)
    self.transient(picker.winfo_toplevel())

    # Place just below the button
    self.update_idletasks()
    x = picker.button.winfo_rootx()
    y = picker.button.winfo_rooty() + picker.button.winfo_height() + 4
    self.geometry(f"+{x}+{y}")

    # Header: <  Month Year  >   (the title is a button that toggles the year view)
    self.header = tk.Frame(self)
    self.header.pack(fill="x", padx=8, pady=(8, 4))
    self.header.columnconfigure(1, weight=1)
    self.prev_btn = tk.Button(self.header, text="◀", width=3, command=lambda: self._shift(-1))
    self.prev_btn.grid(row=0, column=0)
    self.title_btn = tk.Button(
        self.header,
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        bd=0,
        cursor="hand2",
        command=self._toggle_mode,
    )
    self.title_btn.grid(row=0, column=1, sticky="ew", padx=4)
    self.next_btn = tk.Button(self.header, text="▶", width=3, command=lambda: self._shift(1))
    self.next_btn.grid(row=0, column=2)

    # Day grid or year grid
    self.grid_frame = tk.Frame(self)
    self.grid_frame.pack(padx=8, pady=4)

    # Footer
    self.footer = tk.Frame(self)
    self.footer.pack(fill="x", padx=8, pady=(4, 8))
    self.today_btn = tk.Button(self.footer, text="Today", command=self._pick_today)
    self.today_btn.pack(side="left")
    self.close_btn = tk.Button(self.footer, text="Close", command=self.destroy)
    self.close_btn.pack(side="right")

    self.bind("<Escape>", lambda _e: self.destroy())
    self._theme = theme
    self._render()
    self.focus_set()

  def apply_theme(self, t: Theme):
    self._theme = t
    self._render()

  # --- navigation ----------------------------------------------------------
  def _toggle_mode(self):
    if self._mode == "days":
      self._mode = "years"
      self._page = (self._year // YEARS_PER_PAGE) * YEARS_PER_PAGE
    else:
      self._mode = "days"
    self._render()

  def _shift(self, delta: int):
    if self._mode == "years":
      self._page += delta * YEARS_PER_PAGE
    else:
      month, year = self._month + delta, self._year
      if month < 1:
        month, year = 12, year - 1
      elif month > 12:
        month, year = 1, year + 1
      self._year, self._month = year, month
    self._render()

  def _pick_year(self, year: int):
    self._year = year
    # If the same month doesn't exist in range for that year, move to the nearest one that does.
    mx, mn = self._picker._max, self._picker._min
    if mx and (year, self._month) > (mx.year, mx.month):
      self._month = mx.month
    if mn and (year, self._month) < (mn.year, mn.month):
      self._month = mn.month
    self._mode = "days"
    self._render()

  def _pick_today(self):
    today = date.today()
    if self._picker.is_allowed(today):
      self._picker._picked(today)

  def _month_has_allowed_days(self, year: int, month: int) -> bool:
    if year < 1 or year > 9999:
      return False
    last = calendar.monthrange(year, month)[1]
    return self._picker.is_allowed(date(year, month, 1)) or self._picker.is_allowed(
        date(year, month, last)
    )

  # --- drawing -------------------------------------------------------------
  def _palette(self) -> dict:
    t = self._theme
    return {
        "bg": t.bg if t else self.cget("bg"),
        "fg": t.fg if t else "black",
        "btn_bg": t.btn_bg if t else self.cget("bg"),
        "btn_fg": t.btn_fg if t else "black",
        "muted": t.muted_fg if t else "gray",
    }

  def _render(self):
    p = self._palette()
    self.configure(bg=p["bg"])
    for frame in (self.header, self.grid_frame, self.footer):
      frame.configure(bg=p["bg"])
    for b in (self.prev_btn, self.next_btn, self.today_btn, self.close_btn):
      b.configure(
          bg=p["btn_bg"], fg=p["btn_fg"],
          activebackground=p["btn_bg"], activeforeground=p["btn_fg"],
      )
    self.title_btn.configure(
        bg=p["bg"], fg=p["fg"], activebackground=p["bg"], activeforeground=p["fg"]
    )

    for child in self.grid_frame.winfo_children():
      child.destroy()

    if self._mode == "years":
      self._render_years(p)
    else:
      self._render_days(p)

  def _render_years(self, p: dict):
    first, last = self._picker.year_bounds()
    page_end = self._page + YEARS_PER_PAGE - 1
    self.title_btn.configure(text=f"{self._page} – {page_end}  ▴")
    self.prev_btn.configure(state="normal" if self._page > first else "disabled")
    self.next_btn.configure(state="normal" if page_end < last else "disabled")

    today_year = date.today().year
    for i in range(YEARS_PER_PAGE):
      year = self._page + i
      allowed = first <= year <= last
      is_selected = year == self._selected.year
      tk.Button(
          self.grid_frame,
          text=str(year),
          width=9,
          relief="flat",
          bd=0,
          font=("Segoe UI", 10, "bold" if year == today_year else "normal"),
          state="normal" if allowed else "disabled",
          bg=ACCENT_BG if is_selected else p["btn_bg"],
          fg=ACCENT_FG if is_selected else p["btn_fg"],
          activebackground=ACCENT_BG if is_selected else p["btn_bg"],
          activeforeground=ACCENT_FG if is_selected else p["btn_fg"],
          disabledforeground=p["muted"],
          cursor="hand2" if allowed else "arrow",
          command=lambda yy=year: self._pick_year(yy),
      ).grid(row=i // 3, column=i % 3, padx=2, pady=3, ipady=4)

  def _render_days(self, p: dict):
    self.title_btn.configure(text=f"{calendar.month_name[self._month]} {self._year}  ▾")

    # Disable navigation into months where every day is out of range
    prev_y, prev_m = (self._year - 1, 12) if self._month == 1 else (self._year, self._month - 1)
    next_y, next_m = (self._year + 1, 1) if self._month == 12 else (self._year, self._month + 1)
    self.prev_btn.configure(
        state="normal" if self._month_has_allowed_days(prev_y, prev_m) else "disabled"
    )
    self.next_btn.configure(
        state="normal" if self._month_has_allowed_days(next_y, next_m) else "disabled"
    )

    for col, name in enumerate(calendar.day_abbr):  # Mon..Sun
      tk.Label(
          self.grid_frame, text=name[:2], width=4, font=("Segoe UI", 8, "bold"),
          bg=p["bg"], fg=p["muted"],
      ).grid(row=0, column=col)

    today = date.today()
    for row, week in enumerate(self._cal.monthdayscalendar(self._year, self._month), start=1):
      for col, day in enumerate(week):
        if day == 0:
          continue
        d = date(self._year, self._month, day)
        allowed = self._picker.is_allowed(d)
        is_selected = d == self._selected
        tk.Button(
            self.grid_frame,
            text=str(day),
            width=4,
            relief="flat",
            bd=0,
            font=("Segoe UI", 9, "bold" if d == today else "normal"),
            state="normal" if allowed else "disabled",
            bg=ACCENT_BG if is_selected else p["btn_bg"],
            fg=ACCENT_FG if is_selected else p["btn_fg"],
            activebackground=ACCENT_BG if is_selected else p["btn_bg"],
            activeforeground=ACCENT_FG if is_selected else p["btn_fg"],
            disabledforeground=p["muted"],
            cursor="hand2" if allowed else "arrow",
            command=lambda dd=d: self._picker._picked(dd),
        ).grid(row=row, column=col, padx=1, pady=1)