from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# List of top 50 S&P 500 stocks (as of a recent date)
TOP_50_SP500_TICKERS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "FB", "TSLA", "NVDA", "JPM", "JNJ", "V", "PG", "UNH", "DIS", "HD", "MA", "PYPL",
    "VZ", "ADBE", "NFLX", "INTC", "KO", "NKE", "MRK", "T", "PEP", "PFE", "CSCO", "XOM", "ABT", "CMCSA", "ABBV", "CVX",
    "ACN", "MDT", "CRM", "MCD", "TMO", "NEE", "DHR", "COST", "LLY", "WMT", "AMGN", "HON", "TXN", "PM", "UNP", "QCOM",
    "LIN", "BMY"
]

@app.route('/fetch_stock_data', methods=['GET'])
def fetch_stock_data():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)  # Fetch last 6 months of data
    stock_data = fetch_sp500_data(start_date, end_date)
    recommendations = rsi_based_recommendation(stock_data)
    return jsonify(recommendations)

def fetch_sp500_data(start_date, end_date):
    data = []
    company_names = {}
    for stock in TOP_50_SP500_TICKERS:
        stock_data = get_stock_data(stock, start_date, end_date)
        try:
            company_info = yf.Ticker(stock).info
            company_name = company_info.get('longName', stock)
        except Exception as e:
            print(f"Error fetching company name for {stock}: {e}")
            company_name = stock  # Use ticker as a fallback
        company_names[stock] = company_name
        # print(f"Fetched data for {stock}:\n{stock_data.head()}") 
        data.append(stock_data)
    return pd.concat(data, keys=TOP_50_SP500_TICKERS, names=["Symbol", "Date"]), company_names

def get_stock_data(symbol, start_date, end_date):
    stock = yf.Ticker(symbol)
    hist = stock.history(start=start_date, end=end_date)
    stock_data = hist[['Close']]
    # print(f"Stock data for {symbol}:\n{stock_data.head()}") 
    return stock_data

def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)

    avg_gain = gain.rolling(window=window, min_periods=window).mean()
    avg_loss = loss.rolling(window=window, min_periods=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

def rsi_based_recommendation(stock_data):
    stock_data, company_names = stock_data 
    buy_recommendations = []
    sell_recommendations = []
    for symbol, data in stock_data.groupby(level=0):
        data['RSI'] = calculate_rsi(data)
        current_price = data['Close'].iloc[-1]
        company_name = company_names[symbol]
        # print(f"Data for {symbol} with RSI:\n{data[['Close', 'RSI']].tail()}") 
        if data['RSI'].iloc[-1] < 30:  # Buy signal if RSI is below 30
            # print(f"Buy signal detected for {symbol} (RSI: {data['RSI'].iloc[-1]})") 
            buy_recommendations.append({"symbol": symbol, "company": company_name, "recommendation": "Buy", "RSI": data['RSI'].iloc[-1], "price": current_price})
        elif data['RSI'].iloc[-1] > 70:  # Sell signal if RSI is above 70
            # print(f"Sell signal detected for {symbol} (RSI: {data['RSI'].iloc[-1]})")  
            sell_recommendations.append({"symbol": symbol, "company": company_name, "recommendation": "Sell", "RSI": data['RSI'].iloc[-1], "price": current_price})
    
    # Sort recommendations by RSI
    buy_recommendations = sorted(buy_recommendations, key=lambda x: x['RSI'])
    sell_recommendations = sorted(sell_recommendations, key=lambda x: x['RSI'], reverse=True)
    
    # Return top 5 buy and top 5 sell recommendations
    return buy_recommendations[:5] + sell_recommendations[:5]

if __name__ == '__main__':
    app.run(debug=True)
