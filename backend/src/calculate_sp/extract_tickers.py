
import pandas as pd
import requests
from io import StringIO

class ExtractTickers:

    @staticmethod
    def extract_tickers_from_wiki():
        tickers = []

        try:
            url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/131.0.0.0 Safari/537.36"
                )
            }

            response = requests.get(
                url,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()

            sp500 = pd.read_html(StringIO(response.text))[0]

            tickers = (
                sp500["Symbol"]
                .str.replace(".", "-", regex=False)
                .tolist()
            )

        except requests.RequestException as e:
            print(f"Could not download data: {e}")

        except Exception as e:
            print(f"Could not extract tickers: {e}")

        return tickers
