import pandas as pd
import yfinance as yf
# import datetime
import plotly.express as px
from functools import reduce
from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

# Parse user input, limit portfolio length to 10 assets
def stock_parse(x):
    alpha = x.split(',')
    if len(alpha) > 25:
        alpha = alpha[:25]
    return [s.upper() for s in alpha]

#extract closing price for stock using yahoo finance library
def get_stock(ticker,start,end):
    try:
        # data = yf.download(f'{ticker}',start=start,end=end)['Close'].to_frame(f'{ticker}')
        data = yf.download(f'{ticker}',start=start,end=end)['Close']
    except ValueError as e:
        print(f"Error fetching data for {ticker}: {e}")
    return data 

# method to merge closing prices of distinct assets into single data frame
def combine_stocks(tickers,start,end):
    data_frames = []
    for i in tickers:
        data_frames.append(get_stock(i,start,end))
    # Use reduce object for cummulative merge
    df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['Date'], how='outer'), data_frames)
    df_merged.dropna(axis=1,inplace=True)
    return df_merged

# Efficient allocation object
class eff_alc:
    
    def __init__(self,portfolio,ammount,risk_tolerance=50):
        self.portfolio = portfolio
        self.ammount = ammount
        self.risk_tolerance = risk_tolerance

        self.mu = mean_historical_return(self.portfolio)
        self.S = CovarianceShrinkage(self.portfolio).ledoit_wolf()

        self.ef = EfficientFrontier(self.mu, self.S)
        self.weights = self.optimize_portfolio()

        self.performance = self.ef.portfolio_performance(verbose=False)

        self.allocation, self.leftover = self.allocate_amt(self.ammount)
        self.pie_graph = self.allocation_pie_graph(self.allocation)
        self.price_graph = self.asset_price_graph(self.portfolio)

    # Optimal allocation based on risk tolerance 
    def optimize_portfolio(self):
        if self.risk_tolerance < 30:
            # Risk-averse: Minimize volatility
            self.ef.min_volatility()
        elif self.risk_tolerance > 70:
            # High risk tolerance: Maximize Sharpe ratio
            self.ef.max_sharpe()
        else:
            #dynamically calculate volatility based on user's designated risk tolerance
            target_volatility = 0.1 + (self.risk_tolerance - 30) / 40 * (0.25 - 0.1)
            self.ef.efficient_risk(target_volatility)
        return self.ef.clean_weights()

    # Investment allocation method (based on weights)
    def allocate_amt(self,funds):
        latest_prices = get_latest_prices(self.portfolio)
        da = DiscreteAllocation(self.weights, latest_prices, total_portfolio_value=funds)
        print(da.greedy_portfolio())
        return da.greedy_portfolio()
        
    
    def allocation_pie_graph(self,alc):
        data = {'stock':[x for x in alc.keys()],'segment':[x for x in alc.values()]}
        fig =  px.pie(data, values='segment', names='stock', title='Presumptive Allocation for Portfolio')
        return fig
    
    def asset_price_graph(self,df):
        fig_line = px.line(df, x=df.index, y=df.columns)
        return fig_line
        
        

    

    