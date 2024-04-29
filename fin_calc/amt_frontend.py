import streamlit as st
import pandas as pd
from amt_backend import *


page_icon = ':dollar:'
st.set_page_config(page_icon=page_icon)

st.title('Amortization Schedule :money_with_wings:')

option = st.selectbox('Select Payment Frequency',('Yearly','Monthly'))

if option == 'Yearly':
    freq = 'yearly'
else:
    freq = 'monthly'


principal = st.number_input('Enter Loan Principal:',format="%.2f")
payment_period = st.number_input('Enter loan term in years:',format="%.2f")
interest = st.number_input('Enter Interest Rate')

if principal and payment_period and interest:
    amt = amortization_schedule(principal,payment_period,interest,freq)
    st.write('Montly Payment: $',amt.monthly_payment)
    st.write('Total paid: $',amt.total_paid)
    st.write('Total Interest: $',amt.interest_paid)
    st.plotly_chart(amt.graph)
    df = amt.schedule
    st.table(df.style.format({col: '{:.2f}' for col in df.columns if pd.api.types.is_float_dtype(df[col])}))

else:
    st.write('Enter Complete Data')
    

# st.cache_data.clear()

