class Formatter:

  @staticmethod
  def format_summary(data) -> str:
    # Helper to safely format percentages
    def fmt_pct(val):
      if val is None:
        return "N/A"
      return f"{val * 100:.2f}%"

    # Helper to format large raw numbers gracefully if they aren't already strings
    def fmt_val(val):
      if val is None:
        return "N/A"
      if isinstance(val, (int, float)):
        if val >= 1e12:
          return f"${val / 1e12:.2f}T"
        elif val >= 1e9:
          return f"${val / 1e9:.2f}B"
        elif val >= 1e6:
          return f"${val / 1e6:.2f}M"
        return f"${val:,.2f}"
      return str(val)

    return (
        f"=== {data.name} ({data.ticker_symbol}) ===\n"
        f"Sector: {data.sector} | Industry: {data.industry}\n"
        f"--------------------------------------------------\n"
        f"📊 VALUATION & PRICING\n"
        f"  Current Price:    {data.price} {data.currency}\n"
        f"  Market Cap:       {data.market_cap}\n"
        f"  Enterprise Value: {fmt_val(data.enterprise_value)}\n"
        f"  Trailing P/E:     {data.pe_ratio}\n"
        f"  Forward P/E:      {data.forward_pe}\n"
        f"  PEG Ratio:        {data.peg_ratio}\n"
        f"  Price-to-Book:    {data.price_to_book}\n"
        f"  Price-to-Sales:   {data.price_to_sales}\n\n"
        f"📈 PROFITABILITY & GROWTH\n"
        f"  Profit Margins:   {fmt_pct(data.profit_margins)}\n"
        f"  Operating Margins:{fmt_pct(data.operating_margins)}\n"
        f"  Return on Equity: {fmt_pct(data.return_on_equity)}\n"
        f"  Return on Assets: {fmt_pct(data.return_on_assets)}\n"
        f"  Revenue Growth:   {fmt_pct(data.revenue_growth)}\n"
        f"  Earnings Growth:  {fmt_pct(data.earnings_growth)}\n\n"
        f"🛡️ FINANCIAL HEALTH & BALANCE SHEET\n"
        f"  Total Cash:       {fmt_val(data.total_cash)}\n"
        f"  Total Debt:       {fmt_val(data.total_debt)}\n"
        f"  Debt-to-Equity:   {data.debt_to_equity}\n"
        f"  Current Ratio:    {data.current_ratio}\n"
        f"  Quick Ratio:      {data.quick_ratio}\n\n"
        f"💰 DIVIDENDS & MARKET SENTIMENT\n"
        f"  Dividend Yield:   {fmt_pct(data.dividend_yield)}\n"
        f"  Payout Ratio:     {fmt_pct(data.payout_ratio)}\n"
        f"  Beta (Volatility):{data.beta}\n"
        f"  Analyst Target:   {data.target_mean_price}\n"
        f"  Consensus Rating: {str(data.recommendation_key).upper()}\n"
    )