from flask import Flask, render_template, request
import yfinance as yf
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    price = None
    historical_prices = None
    if request.method == 'POST':
        symbol = request.form['symbol']
        stock = yf.Ticker(symbol)

        # Get current price
        try:
            price = stock.history(period='1d')['Close'].iloc[0]
        except Exception as e:
            price = f"Failed to retrieve data: {str(e)}"

        # Get historical data
        try:
            historical_data = stock.history(period='30d')  # Get 30 days of historical data
            historical_prices = historical_data['Close']
            # Create a plot
            plt.figure(figsize=(10, 5))
            plt.plot(historical_prices.index, historical_prices.values, marker='o', color='b')
            plt.title(f"{symbol} Historical Prices")
            plt.xlabel("Date")
            plt.ylabel("Price (USD)")
            plt.grid()
            # Save the plot
            plt.savefig('static/historical_prices.png')
            plt.close()
        except Exception as e:
            historical_prices = f"Failed to retrieve historical data: {str(e)}"

    # Convert price to string for template rendering
    price_str = str(price) if isinstance(price, (float, int)) else price

    return render_template('index.html', price=price_str, historical_prices=historical_prices)
