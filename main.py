import tkinter as tk
from backend.src.gui.gui import StockAppGUI


def main():
  root = tk.Tk()
  # Initialize the primary GUI window controller
  app = StockAppGUI(root)
  root.mainloop()


if __name__ == "__main__":
  main()