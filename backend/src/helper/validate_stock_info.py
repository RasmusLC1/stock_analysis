class ValidateStockInfo:
    
  @staticmethod
  def validate_info(ticker):
    info = ticker.info
    
    # Validate ticker existence
    if (
        not info
        or (
            "regularMarketPrice" not in info
            and "currentPrice" not in info
            and "longName" not in info
        )
    ):
      return None

    return info