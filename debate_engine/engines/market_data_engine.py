import yfinance as yf
import numpy as np

def fetch_market_data(ticker):

    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")
    info = stock.info

    volatility = np.std(hist["Close"].pct_change()) * (252 ** 0.5)

    return {
        "current_price": info.get("currentPrice"),
        "pe_ratio": info.get("trailingPE"),
        "market_cap": info.get("marketCap"),
        "volatility": round(volatility, 3),
        "one_year_return": round((hist["Close"][-1] / hist["Close"][0]) - 1, 3)
    }