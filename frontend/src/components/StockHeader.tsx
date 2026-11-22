import type { StockData } from "../services/stockApi";

interface StockHeaderProps {
  stock: StockData;
}

function StockHeader({ stock }: StockHeaderProps) {
  return (
    <section className="stock-header">
      <h2>{stock.name || stock.ticker_symbol}</h2>

      <p>
        {stock.ticker_symbol}
        {stock.sector ? ` · ${stock.sector}` : ""}
        {stock.currency ? ` · ${stock.currency}` : ""}
      </p>

      <h3>
        {stock.price ?? "N/A"} {stock.currency ?? ""}
      </h3>
    </section>
  );
}

export default StockHeader;
