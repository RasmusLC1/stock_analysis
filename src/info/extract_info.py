from .info_config import InfoConfig
from .market_cap_formatter import MarketCapFormatter
from src.helper.yf_keys import YahooFinanceKeys as key

class ExtractInfo:
    @staticmethod
    def extract_info(info, ticker_symbol):
        data = InfoConfig(
        # Extract fields safely
        ticker_symbol = ticker_symbol,
        name = info.get(key.LONG_NAME, info.get(key.SHORT_NAME, ticker_symbol)),
        currency = info.get(key.CURRENCY, "USD"),
        sector = info.get(key.SECTOR, "N/A"),
        industry = info.get(key.INDUSTRY, "N/A"),
        market_cap = MarketCapFormatter.format_market_cap(info.get(key.MARKET_CAP, "N/A")),
        pe_ratio = info.get(key.TRAILING_PE, "N/A"),

        # Get latest price safely
        price = info.get("currentPrice", info.get("regularMarketPrice", "N/A"))
        )
        return data