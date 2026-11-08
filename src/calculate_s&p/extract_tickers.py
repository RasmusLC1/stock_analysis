import pandas as pd

class ExtractTickers:

    def extract_tickers():
        url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        sp500 = pd.read_html(url)[0]
        tickers = sp500["Symbol"].str.replace(".", "-", regex=False).tolist()
        return tickers