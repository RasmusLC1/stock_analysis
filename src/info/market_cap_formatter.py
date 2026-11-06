class MarketCapFormatter:
    # Format Market Cap for readability
    def format_market_cap(market_cap):
        if not isinstance(market_cap, (int, float)):
          return None
        
        if market_cap >= 1e12:
            return f"${market_cap / 1e12:.2f}T"
        elif market_cap >= 1e9:
            return f"${market_cap / 1e9:.2f}B"
        elif market_cap >= 1e6:
            return f"${market_cap / 1e6:.2f}M"
        else:
            return f"${market_cap:,.0f}"