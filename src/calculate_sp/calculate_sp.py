from .extract_tickers import ExtractTickers
from src.yf_api.api_fetch import ApiFetch
from yfinance import Ticker
from src.info.info_config import InfoConfig
from src.info.extract_info import ExtractInfo
from src.helper.process_data import ProcessData

class CalculateSP500:

    def calculate_average_values():
        tickers = ExtractTickers.extract_tickers()
        print(tickers)
        data_list = CalculateSP500.extract_ticker_data(tickers)
        

    def extract_ticker_data(tickers):
        data_list = []
        for ticker_symbol in tickers:
            data = ProcessData.process_data(ticker_symbol)
            if not data:
                continue
            print(data.ticker_symbol, data.market_cap, data.pe_ratio)
            data_list.append(data)

        return data_list