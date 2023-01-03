import streamlit as st
import yfinance as yf 
import pandas as pd 
import cufflinks as cf # use lib to act as connection to plotly
import datetime  
import ssl


#App title 
st.markdown('''
    #Stock Price Data Demo
''')
st.write('---')

#sidebar 
st.sidebar.subheader('Query Parameters')
start_date = st.sidebar.date_input('Start Date',datetime.date(2019,1,1))
end_date = st.sidebar.date_input("End Date",datetime.date(2022,1,31))

#Retrieve ticker data
ssl._create_default_https_context = ssl._create_unverified_context
df = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
ticker_list = df.Symbol.to_list()
tickerSymbol = st.sidebar.selectbox('Stock Ticker',ticker_list)
tickerData = yf.Ticker(tickerSymbol) #ger ticker data
tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)

#ticker information 
string_logo ='<img src=%s>' % tickerData.info['logo_url'] #inplace of string, select logo url from ticker api dictionary
st.markdown(string_logo, unsafe_allow_html=True)

string_name = tickerData.info['longName']
st.header('**%s**' % string_name)
string_sector = tickerData.info['sector']
st.header('**%s**' % string_sector)

string_summary = tickerData.info['longBusinessSummary']
st.info(string_summary)

#ticker data
st.header('**Ticker Data**')
st.write(tickerDf)

#Bollinger Bands
st.header('**Bollinger Bands**')
qf = cf.QuantFig(tickerDf, title='Demo Analysis', legend='top', name='GS')
qf.add_bollinger_bands()
fig = qf.iplot(asFigure=True)
st.plotly_chart(fig)