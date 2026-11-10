
from dataclasses import asdict, is_dataclass

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.src.stock_service import StockService

app = FastAPI(title="Stock Analysis API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


# Create an enpoint that returns stock_data
@app.get("/api/stocks/{ticker}")
def get_stock(ticker: str):
    try:
        stock = StockService.fetch_stock_summary(ticker)

        if stock is None:
            raise HTTPException(
                status_code=404,
                detail=f"No stock data found for {ticker.upper()}"
            )

        if is_dataclass(stock):
            stock_data = asdict(stock)
        else:
            stock_data = vars(stock)

        return stock_data

    except HTTPException:
        raise

    except Exception as error:
        print(f"Stock lookup failed: {error}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving stock data."
        )
