from .extract_tickers import ExtractTickers
from src.helper.process_data import ProcessData
from .calculate_averages import CalculateAverages

class CalculateSP500:

    def calculate_average_values():
        tickers = ExtractTickers.extract_tickers_from_wiki()
        data_list = CalculateSP500.extract_ticker_data(tickers)
        average_values = CalculateAverages.calculate_averages(data_list)
        print(average_values)
        

    def extract_ticker_data(tickers):
        data_list = []
        for ticker_symbol in tickers:
            data = ProcessData.process_data(ticker_symbol)
            if not data:
                continue
            data_list.append(data)

        return data_list