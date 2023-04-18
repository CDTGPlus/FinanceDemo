# %%
import yfinance as yf 
import pandas as pd 
import streamlit as st
from pandas.tseries.offsets import DateOffset

# %%
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# %%
tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0].Symbol

# %%
tickers = tickers.to_list()

# %%
#use decorator on streamlit to cache data
@st.cache_data
def getdata():
    df = yf.download(tickers,start='2020-01-01')
    df = df['Close']
    return df 

# %%
df = getdata()

# %%
st.title('Index component performace for S&P 500')

# %%
n = st.number_input('Provide the performance horizon in months:',min_value=1,max_value=24)

# %%
def get_ret(df,n):
    previous_prices = df[:df.index[-1] - DateOffset(months=n)].tail(1).squeeze()
    recent_prices = df.loc[df.index[-1]]
    ret_df = (recent_prices/previous_prices) -1
    return previous_prices.name, ret_df 

# %%
date, ret_df = get_ret(df,n)

# %%
winners, losers = ret_df.nlargest(10), ret_df.nsmallest(10)

# %%
winners.name, losers.name = 'winners','losers'

# %%
st.table(winners)
st.table(losers)

# %%
winnerpick = st.selectbox('Pick a winner stock ticker to visualize performance:',winners.index)
st.line_chart(df[winnerpick][date:])
loserpick = st.selectbox('Pick a loser stock ticker to visualize performance:',losers.index)
st.line_chart(df[loserpick][date:])


