import yfinance as yf


class StockService:
  """Handles data fetching and processing from Yahoo Finance."""

  @staticmethod
  def fetch_stock_summary(ticker_symbol: str) -> dict:
    ticker_symbol = ticker_symbol.strip().upper()
    if not ticker_symbol:
      raise ValueError("Ticker symbol cannot be empty.")

    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info

    # Validate ticker existence
    if (
        not info
        and "regularMarketPrice" not in info
        and "currentPrice" not in info
        and "longName" not in info
    ):
      hist = ticker.history(period="1d")
      if hist.empty:
        raise ValueError(
            f"Could not retrieve valid data for ticker '{ticker_symbol}'."
        )

    # Extract fields safely
    name = info.get("longName", info.get("shortName", ticker_symbol))
    currency = info.get("currency", "USD")
    sector = info.get("sector", "N/A")
    industry = info.get("industry", "N/A")
    market_cap = info.get("marketCap", "N/A")
    pe_ratio = info.get("trailingPE", "N/A")

    # Get latest price safely
    price = info.get("currentPrice", info.get("regularMarketPrice", "N/A"))
    if price == "N/A":
      hist = ticker.history(period="1d")
      if not hist.empty:
        price = round(hist["Close"].iloc[-1], 2)

    # Format Market Cap for readability
    if isinstance(market_cap, (int, float)):
      if market_cap >= 1e12:
        market_cap_str = f"${market_cap / 1e12:.2f}T"
      elif market_cap >= 1e9:
        market_cap_str = f"${market_cap / 1e9:.2f}B"
      elif market_cap >= 1e6:
        market_cap_str = f"${market_cap / 1e6:.2f}M"
      else:
        market_cap_str = f"${market_cap:,.0f}"
    else:
      market_cap_str = "N/A"

    return {
        "symbol": ticker_symbol,
        "name": name,
        "sector": sector,
        "industry": industry,
        "currency": currency,
        "price": price,
        "market_cap": market_cap_str,
        "pe_ratio": pe_ratio,
    }