import pandas as pd
import yfinance as yf
import plotly.io as pio
import plotly.graph_objects as go

pio.templates.default = "plotly_white"

# Define the tickers for Apple and Google
apple_ticker = 'AAPL'
google_ticker = 'GOOGL'

# Define the date range for the last quarter
start_date = '2023-07-01'
end_date = '2023-09-30'

# Fetch historical stock price data using yfinance
apple_data = yf.download(apple_ticker, start=start_date, end=end_date)
google_data = yf.download(google_ticker, start=start_date, end=end_date)

# Calculate daily returns
apple_data['Daily_Return'] = apple_data['Adj Close'].pct_change()
google_data['Daily_Return'] = google_data['Adj Close'].pct_change()

# Create a figure to visualize the daily returns
fig = go.Figure()

fig.add_trace(go.Scatter(x=apple_data.index, y=apple_data['Daily_Return'],
                         mode='lines', name='Apple', line=dict(color='blue')))
fig.add_trace(go.Scatter(x=google_data.index, y=google_data['Daily_Return'],
                         mode='lines', name='Google', line=dict(color='green')))

fig.update_layout(title='Daily Returns for Apple and Google (Last Quarter)',
                  xaxis_title='Date', yaxis_title='Daily Return',
                  legend=dict(x=0.02, y=0.95))

fig.show()

# Calculate cumulative returns for the last quarter
apple_cumulative_return = (1 + apple_data['Daily_Return']).cumprod() - 1
google_cumulative_return = (1 + google_data['Daily_Return']).cumprod() - 1

# Create a figure to visualize the cumulative returns
fig = go.Figure()

fig.add_trace(go.Scatter(x=apple_cumulative_return.index, y=apple_cumulative_return,
                         mode='lines', name='Apple', line=dict(color='blue')))
fig.add_trace(go.Scatter(x=google_cumulative_return.index, y=google_cumulative_return,
                         mode='lines', name='Google', line=dict(color='green')))

fig.update_layout(title='Cumulative Returns for Apple and Google (Last Quarter)',
                  xaxis_title='Date', yaxis_title='Cumulative Return',
                  legend=dict(x=0.02, y=0.95))

fig.show()

# Calculate historical volatility (standard deviation of daily returns)
apple_volatility = apple_data['Daily_Return'].std()
google_volatility = google_data['Daily_Return'].std()

# Create a figure to compare volatility
fig1 = go.Figure()
fig1.add_bar(x=['Apple', 'Google'], y=[apple_volatility, google_volatility],
             text=[f'{apple_volatility:.4f}', f'{google_volatility:.4f}'],
             textposition='auto', marker=dict(color=['blue', 'green']))

fig1.update_layout(title='Volatility Comparison (Last Quarter)',
                   xaxis_title='Stock', yaxis_title='Volatility (Standard Deviation)',
                   bargap=0.5)
fig1.show()

market_data = yf.download('^GSPC', start=start_date, end=end_date)  # S&P 500 index as the market benchmark

# Calculate daily returns for both stocks and the market
apple_data['Daily_Return'] = apple_data['Adj Close'].pct_change()
google_data['Daily_Return'] = google_data['Adj Close'].pct_change()
market_data['Daily_Return'] = market_data['Adj Close'].pct_change()

# Calculate Beta for Apple and Google
cov_apple = apple_data['Daily_Return'].cov(market_data['Daily_Return'])
var_market = market_data['Daily_Return'].var()

beta_apple = cov_apple / var_market

cov_google = google_data['Daily_Return'].cov(market_data['Daily_Return'])
beta_google = cov_google / var_market

# Compare Beta values
if beta_apple > beta_google:
    conclusion = "Apple is more volatile (higher Beta) compared to Google."
else:
    conclusion = "Google is more volatile (higher Beta) compared to Apple."

# Print the conclusion
print("Beta for Apple:", beta_apple)
print("Beta for Google:", beta_google)
print(conclusion)
