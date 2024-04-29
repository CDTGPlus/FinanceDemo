import streamlit as st
import pandas as pd
import opt_backend

#st.cache_data.clear()
st.title('Portfolio Optimization Manager')

stocks = st.text_input('Enter stock tickers to be used in portfolio')
start = st.date_input('Start', value = pd.to_datetime('2021-01-01'))
end = st.date_input('End', value=pd.to_datetime('today'))

funds = st.number_input('Enter amount to be invested')

pf_list = opt_backend.stock_parse(stocks)
val = funds

if  stocks and funds:
    portfolio = opt_backend.combine_stocks(pf_list,start,end)

    st.dataframe(portfolio)
    try:
        invested = opt_backend.eff_alc(portfolio)
        invested.allocate_amt(val)
        performance = invested.performance
        st.write('Expected performance')
        st.write('Annual Return Return: {:.2f}%'.format(performance[0]*100))
        st.write('Annual Volatility: {:.2f}%'.format(performance[1]*100))
        st.write('Sharpe Ratio: {:.2f}%'.format(performance[2]))
        #st.write(invested.ef.portfolio_performance(verbose=True))
        st.write('Scheduled Allocation')
        allocation = [f'{x}: {y}' for x,y in invested.allocation.items()]
        for al in allocation:
            st.write(al)
        #st.text('Leftover amount in portfolio')
        st.write("Funds remaining: ${:.2f}".format(invested.leftover))
    except ValueError as e:
        st.write('Error:'+str(e))
         
    


st.cache_data.clear()
