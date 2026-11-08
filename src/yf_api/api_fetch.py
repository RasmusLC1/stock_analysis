import yfinance as yf

class ApiFetch:
  # Handles data fetching and processing from Yahoo Finance

  @staticmethod
  def fetch_stock_data(ticker_symbol: str, start: str | None = None):
    ticker_symbol = ticker_symbol.strip().upper()
    if not ticker_symbol:
      raise ValueError("Ticker symbol cannot be empty.")

    ticker = yf.Ticker(ticker_symbol)
    hist = ticker.history(start=start) if start else ticker.history(period="1d")
    if hist.empty:
      return None
    return ticker, hist