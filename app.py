from flask import Flask, render_template
import pandas as pd
import plotly.graph_objects as go
from collect_data import get_market_caps, filename

app = Flask(__name__)


@app.route('/')
def start_page():
    df = pd.read_csv(filename)
    candlestick_chart = go.Figure(data=[go.Candlestick(
        x=df['Open time'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'])])
    candlestick_chart.update_layout(title='Candlestick Chart')

    # get a market caps for 10 coins
    symbols = ['dogecoin', 'ethereum', 'binancecoin', 'ripple', 'litecoin', 'bitcoin-cash', 'cardano', 'polkadot','chainlink', 'stellar']
    market_caps = get_market_caps(symbols)

    labels = list(market_caps.keys())
    values = list(market_caps.values())

    market_caps_chart = go.Figure(data=[go.Pie(labels=labels, values=values)])
    market_caps_chart.update_layout(title="Market Caps Chart")

    return render_template('index.html',
                           candlestick_chart=candlestick_chart.to_html(full_html=False, include_plotlyjs='cdn'),
                           market_caps_chart=market_caps_chart.to_html(full_html=False, include_plotlyjs='cdn'))


if __name__ == '__main__':
    app.run(debug=True)
