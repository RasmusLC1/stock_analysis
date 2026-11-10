from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
  name: str
  toggle_text: str  # label for the button that switches to the *other* theme
  bg: str
  fg: str
  entry_bg: str
  entry_fg: str
  text_bg: str
  text_fg: str
  btn_bg: str
  btn_fg: str
  muted_fg: str


DARK = Theme(
    name="dark",
    toggle_text="☀️ Light Mode",
    bg="#1e1e1e",
    fg="#e0e0e0",
    entry_bg="#2d2d2d",
    entry_fg="#ffffff",
    text_bg="#252526",
    text_fg="#d4d4d4",
    btn_bg="#333333",
    btn_fg="#ffffff",
    muted_fg="#9a9a9a",
)

LIGHT = Theme(
    name="light",
    toggle_text="🌙 Dark Mode",
    bg="#f0f0f0",
    fg="#000000",
    entry_bg="#ffffff",
    entry_fg="#000000",
    text_bg="#f9f9f9",
    text_fg="#000000",
    btn_bg="#e0e0e0",
    btn_fg="#000000",
    muted_fg="#555555",
)

# Grade colors are the same in both themes so a grade always looks the same.
# Each entry is (background, foreground).
GRADE_COLORS = {
    "A": ("#2e7d32", "#ffffff"),
    "B": ("#7cb342", "#102000"),
    "C": ("#fbc02d", "#3a2f00"),
    "D": ("#fb8c00", "#2a1500"),
    "F": ("#c62828", "#ffffff"),
    "N/A": ("#616161", "#ffffff"),
}