from .info_config import InfoConfig
from .market_cap_formatter import MarketCapFormatter

class ExtractInfo:
    @staticmethod
    def extract_info(info, ticker_symbol):
        data = InfoConfig(
        # Extract fields safely
        ticker_symbol = ticker_symbol,
        name = info.get("longName", info.get("shortName", ticker_symbol)),
        currency = info.get("currency", "USD"),
        sector = info.get("sector", "N/A"),
        industry = info.get("industry", "N/A"),
        market_cap = MarketCapFormatter.format_market_cap(info.get("marketCap", "N/A")),
        pe_ratio = info.get("trailingPE", "N/A"),

        # Get latest price safely
        price = info.get("currentPrice", info.get("regularMarketPrice", "N/A"))
        )
        return data