from .extract_tickers import ExtractTickers
from src.helper.process_data import ProcessData
from .calculate_averages import CalculateAverages
from src.caching.cache import Cache
from src.info.extract_info import ExtractInfo
from datetime import datetime


TICKER = "S&P500"

class CalculateSP500:
    
    @staticmethod
    def calculate_average_values():
        current_month_year = datetime.now().strftime("%Y-%m")
        cached_data = Cache.check_cache(TICKER, current_month_year)
        if cached_data is not None:
            print("CACHE FOUND:\t", TICKER)
            return cached_data
        tickers = ExtractTickers.extract_tickers_from_wiki()
        data_list = CalculateSP500.extract_ticker_data(tickers)
        average_values = CalculateAverages.calculate_averages(data_list)
        average_info_config = ExtractInfo.extract_info(average_values, TICKER)

        Cache.store_cache(TICKER, current_month_year, average_info_config)
        print("CACHE STORED")
        return average_info_config
        
    @staticmethod
    def extract_ticker_data(tickers):
        data_list = []
        for ticker_symbol in tickers:
            data = ProcessData.process_data(ticker_symbol)
            if not data:
                continue
            data_list.append(data)

        return data_list