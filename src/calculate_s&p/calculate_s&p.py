from .extract_tickers import ExtractTickers
from src.yf_api.api_fetch import ApiFetch
from yfinance import Ticker
from src.info.info_config import InfoConfig
from src.info.extract_info import ExtractInfo

class CalculateSP500:

    def calculate_average_values():
        tickers = ExtractTickers.extract_tickers()
        

    def extract_ticker_data(tickers):
        info_list = []
        for ticker_symbol in tickers:
            ticker: Ticker = ApiFetch.fetch_stock_data(ticker_symbol, "1d")
            if not ticker:
                print("COULD NOT FIND:\t", ticker_symbol)
                continue

            data: InfoConfig = ExtractInfo.extract_info(info, ticker_symbol)
            info_list.append()