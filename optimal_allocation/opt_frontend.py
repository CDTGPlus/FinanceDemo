import streamlit as st
import pandas as pd
import opt_backend

st.title('Portfolio Optimization Manager')

stocks = st.text_input('Enter stock tickers to be used in portfolio')
start = st.date_input('Start', value = pd.to_datetime('2021-01-01'))
end = st.date_input('End', value=pd.to_datetime('today'))

funds = st.number_input('Enter amount to be invested')

pf_list = opt_backend.stock_parse(stocks)
val = funds
# Initialize once funds(amount) and stocks have been entered by user
if  stocks and funds:
    portfolio = opt_backend.combine_stocks(pf_list,start,end)
    investment = opt_backend.eff_alc(portfolio,val)
    try:
    
        performance = investment.performance
        # Dsiplay summary statistics for portfolio; return, allocation
        st.write('Expected performance')
        st.write('Annual Return: {:.2f}%'.format(performance[0]*100))
        st.write('Annual Volatility: {:.2f}%'.format(performance[1]*100))
        st.write('Sharpe Ratio: {:.2f}%'.format(performance[2]))
        st.write('Scheduled Allocation:')
        allocation = [f'{x}: {y}' for x,y in investment.allocation.items()]
        for al in allocation:
            st.write(al)
        st.write("Funds remaining: ${:.2f}".format(investment.leftover))
        #display asset allocation for portfolio
        st.plotly_chart(investment.pie_graph)
        #for price history, switch between line chart and data frame
        # if toggle does not exist, inittialize it
        if 'price_view' not in st.session_state:
            st.session_state.price_view = False
        # Toggle the price_view state when the button is clicked
        if st.button('Switch Price History View'):
            st.session_state.price_view = not st.session_state.price_view

        # Display the appropriate view based on the toggle state
        if st.session_state.price_view:
            st.dataframe(portfolio)
        else:
            st.plotly_chart(investment.price_graph)
    except ValueError as e:
        st.write('Data not valid')

else:
    st.write("Enter complete data")
         
    

st.cache_data.clear()
