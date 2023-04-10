import pandas as pd
import yfinance as yf
import datetime
from functools import reduce
from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices


def stock_parse(x):
    return [s.upper() for s in list(x.split(','))]


def get_stock(ticker,start,end):
    try:
        data = yf.download(f'{ticker}',start=start,end=end)['Close'].to_frame(f'{ticker}')
    except TypeError:
        pass
    #print(data.head())
    return data 

def combine_stocks(tickers,start,end):
    data_frames = []
    for i in tickers:
        data_frames.append(get_stock(i,start,end))
        
    df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['Date'], how='outer'), data_frames)
    df_merged.dropna(axis=1,inplace=True)
    #print(df_merged.head())
    return df_merged


class eff_alc:
    
    def __init__(self,portfolio):
        self.portfolio = portfolio

        self.mu = mean_historical_return(self.portfolio)
        self.S = CovarianceShrinkage(self.portfolio).ledoit_wolf()

        self.ef = EfficientFrontier(self.mu, self.S)
        self.weights = self.ef.max_sharpe()

        self.performance = self.ef.portfolio_performance(verbose=False)

        self.allocation = None
        self.leftover = None

    def allocate_amt(self,funds=10000):
        latest_prices = get_latest_prices(self.portfolio)
        da = DiscreteAllocation(self.weights, latest_prices, total_portfolio_value=funds)
        self.allocation, self.leftover = da.greedy_portfolio()

    

    