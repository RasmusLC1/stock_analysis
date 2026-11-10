from .info_config import InfoConfig
from .market_cap_formatter import MarketCapFormatter
from backend.src.helper.yf_keys import YahooFinanceKeys as key


class ExtractInfo:

  @staticmethod
  def extract_info(info: dict, ticker_symbol: str) -> InfoConfig:
    return InfoConfig(
        # Required Identifier
        ticker_symbol=ticker_symbol,
        # Basic Info & Profile
        name=info.get(key.LONG_NAME, info.get(key.SHORT_NAME, ticker_symbol)),
        currency=info.get(key.CURRENCY, "USD"),
        financial_currency=info.get(key.FINANCIAL_CURRENCY),
        sector=info.get(key.SECTOR, "N/A"),
        industry=info.get(key.INDUSTRY, "N/A"),
        summary=info.get(key.LONG_BUSINESS_SUMMARY),
        website=info.get(key.WEBSITE),
        # Price & Trading Dynamics
        price=info.get(key.CURRENT_PRICE, info.get(key.REGULAR_MARKET_PRICE)),
        previous_close=info.get(key.PREVIOUS_CLOSE),
        open_price=info.get(key.OPEN),
        day_low=info.get(key.DAY_LOW),
        day_high=info.get(key.DAY_HIGH),
        volume=info.get(key.VOLUME),
        average_volume=info.get(key.AVERAGE_VOLUME),
        # Valuation Metrics
        market_cap=MarketCapFormatter.format_market_cap(
            info.get(key.MARKET_CAP)
        ),
        enterprise_value=info.get(key.ENTERPRISE_VALUE),
        pe_ratio=info.get(key.TRAILING_PE, "N/A"),
        forward_pe=info.get(key.FORWARD_PE),
        peg_ratio=info.get(key.TRAILING_PEG_RATIO)
        or info.get(key.PEG_RATIO),
        price_to_sales=info.get(key.PRICE_TO_SALES_TRAILING_12MONTHS),
        price_to_book=info.get(key.PRICE_TO_BOOK),
        enterprise_to_revenue=info.get(key.ENTERPRISE_TO_REVENUE),
        enterprise_to_ebitda=info.get(key.ENTERPRISE_TO_EBITDA),
        # Profitability & Margins
        profit_margins=info.get(key.PROFIT_MARGINS),
        gross_margins=info.get(key.GROSS_MARGINS),
        operating_margins=info.get(key.OPERATING_MARGINS),
        ebitda_margins=info.get(key.EBITDA_MARGINS),
        return_on_assets=info.get(key.RETURN_ON_ASSETS),
        return_on_equity=info.get(key.RETURN_ON_EQUITY),
        # Income & Cash Flow Statement Highlights
        total_revenue=info.get(key.TOTAL_REVENUE),
        revenue_growth=info.get(key.REVENUE_GROWTH),
        gross_profits=info.get(key.GROSS_PROFITS),
        ebitda=info.get(key.EBITDA),
        net_income=info.get(key.NET_INCOME_TO_COMMON),
        earnings_growth=info.get(key.EARNINGS_GROWTH),
        eps_trailing=info.get(key.EPS_TRAILING_TWELVE_MONTHS)
        or info.get(key.TRAILING_EPS),
        eps_forward=info.get(key.EPS_FORWARD),
        free_cashflow=info.get(key.FREE_CASHFLOW),
        operating_cashflow=info.get(key.OPERATING_CASHFLOW),
        # Balance Sheet & Capital Structure
        total_cash=info.get(key.TOTAL_CASH),
        total_debt=info.get(key.TOTAL_DEBT),
        debt_to_equity=info.get(key.DEBT_TO_EQUITY),
        current_ratio=info.get(key.CURRENT_RATIO),
        quick_ratio=info.get(key.QUICK_RATIO),
        book_value=info.get(key.BOOK_VALUE),
        # Dividends & Capital Return
        dividend_rate=info.get(key.DIVIDEND_RATE),
        dividend_yield=info.get(key.DIVIDEND_YIELD),
        payout_ratio=info.get(key.PAYOUT_RATIO),
        ex_dividend_date=info.get(key.EX_DIVIDEND_DATE),
        # Technicals & Moving Averages
        beta=info.get(key.BETA),
        fifty_two_week_low=info.get(key.FIFTY_TWO_WEEK_LOW),
        fifty_two_week_high=info.get(key.FIFTY_TWO_WEEK_HIGH),
        fifty_day_average=info.get(key.FIFTY_DAY_AVERAGE),
        two_hundred_day_average=info.get(key.TWO_HUNDRED_DAY_AVERAGE),
        # Share Structure & Short Interest
        shares_outstanding=info.get(key.SHARES_OUTSTANDING),
        float_shares=info.get(key.FLOAT_SHARES),
        short_ratio=info.get(key.SHORT_RATIO),
        short_percent_of_float=info.get(key.SHORT_PERCENT_OF_FLOAT),
        held_percent_insiders=info.get(key.HELD_PERCENT_INSIDERS),
        held_percent_institutions=info.get(key.HELD_PERCENT_INSTITUTIONS),
        # Analyst Estimates & Consensus
        target_high_price=info.get(key.TARGET_HIGH_PRICE),
        target_low_price=info.get(key.TARGET_LOW_PRICE),
        target_mean_price=info.get(key.TARGET_MEAN_PRICE),
        target_median_price=info.get(key.TARGET_MEDIAN_PRICE),
        recommendation_key=info.get(key.RECOMMENDATION_KEY),
        number_of_analysts=info.get(key.NUMBER_OF_ANALYST_OPINIONS),
    )