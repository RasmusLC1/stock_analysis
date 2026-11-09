from .extract_tickers import ExtractTickers
from src.helper.process_data import ProcessData
from .calculate_averages import CalculateAverages
from src.caching.cache import Cache
from src.info.extract_info import ExtractInfo
from datetime import datetime
from src.info.info_config import InfoConfig



TICKER = "S&P500"

class CalculateSP500:
    def __init__(self):
        self.average_values = None
        self.get_average_values()
    
    def get_average_values(self):
        if self.average_values:
            print("AVERAGE VALUES ALREADY CALCULATED")
            return self.average_values
        self._set_average_values()
        return self.average_values

    def _set_average_values(self):
        current_month_year = datetime.now().strftime("%Y-%m")
        cached_data = Cache.check_cache(TICKER, current_month_year)
        if cached_data is not None:
            self.average_values = cached_data
            print("CACHE FOUND:\t", TICKER)
            return
        
        tickers = ExtractTickers.extract_tickers_from_wiki()
        data_list = CalculateSP500._extract_ticker_data(tickers)
        average_values = CalculateAverages.calculate_averages(data_list)
        self.average_values = ExtractInfo.extract_info(average_values, TICKER)
        Cache.store_cache(TICKER, current_month_year, self.average_info_config)
    
    @staticmethod
    def _extract_ticker_data(tickers):
        data_list = []
        for ticker_symbol in tickers:
            data = ProcessData.process_data(ticker_symbol)
            if not data:
                continue
            data_list.append(data)

        return data_list