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
    if len(alpha) > 10:
        alpha = alpha[:10]
    return [s.upper() for s in alpha]

#extract closing price for stock using yahoo finance library
def get_stock(ticker,start,end):
    try:
        data = yf.download(f'{ticker}',start=start,end=end)['Close'].to_frame(f'{ticker}')
    except TypeError:
        pass
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
    
    def __init__(self,portfolio,ammount):
        self.portfolio = portfolio
        self.ammount = ammount

        self.mu = mean_historical_return(self.portfolio)
        self.S = CovarianceShrinkage(self.portfolio).ledoit_wolf()

        self.ef = EfficientFrontier(self.mu, self.S)
        self.weights = self.ef.max_sharpe()

        self.performance = self.ef.portfolio_performance(verbose=False)

        self.allocation, self.leftover = self.allocate_amt(self.ammount)
        self.pie_graph = self.allocation_pie_graph(self.allocation)
        self.price_graph = self.asset_price_graph(self.portfolio)
    # Investment allocation method
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
        
        

    

    