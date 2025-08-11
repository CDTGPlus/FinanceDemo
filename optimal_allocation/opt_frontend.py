import streamlit as st
import pandas as pd
import opt_backend

st.title('Portfolio Optimization Manager')

stocks = st.text_area('Enter stock tickers to be used in portfolio')
start = st.date_input('Start', value = pd.to_datetime('2021-01-01'))
end = st.date_input('End', value=pd.to_datetime('today'))
risk_tolerance = st.slider("Select Risk Tolerance", 0, 100, 50)

funds = st.number_input('Enter amount to be invested')

pf_list = opt_backend.stock_parse(stocks)

# Initialize once funds(amount) and stocks have been entered by user
if st.button('Optimize Portfolio'):
    if  stocks and funds > 0:
        portfolio = opt_backend.combine_stocks(pf_list,start,end)
        print("Here is the portfolio")
        print(portfolio)
        investment = opt_backend.eff_alc(portfolio,funds,risk_tolerance)
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

            st.write(f"An error has occurred: {e}")

else:
    st.warning("Please enter all required inputs (stocks and funds).")
         
    

st.cache_data.clear()
