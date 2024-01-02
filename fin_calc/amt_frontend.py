import streamlit as st
import pandas as pd
import amt_backend


page_icon = ':compass:'
st.set_page_config(page_icon=page_icon)

option = st.selectbox('Select Financial Function',('Amortization Schedule','Payment Calculator'))

if option == 'Amortization Schedule':


    st.title('Amortization Schedule :money_with_wings:')

    principal = st.number_input('Enter Loan Principal:',format="%.2f")
    period_payment = st.number_input('Enter Payment amount per period:',format="%.2f")
    interest = st.number_input('Enter Interest Rate')

    if period_payment and principal and interest:
        check = principal * (interest/100)
        if check >= period_payment:
            st.write('Error: Payment Per Period is not enough to cover amortization expenses :umbrella_with_rain_drops:')
        else:
            
            amortization_schedule = amt_backend.loan_amt(period_payment,principal,interest)
            df = amortization_schedule.new_amt()
            st.write('Total Interest Paid: $',round(amortization_schedule.int_paid,2))
            st.write('Total Cost of Loan $',round(amortization_schedule.cost_of_loan,2))
            st.table(df.style.format({col: '{:.2f}' for col in df.columns if pd.api.types.is_float_dtype(df[col])}))

            # st.table(df.style.format({col: '{:.2f}' for col in df.columns if pd.api.types.is_float_dtype(df[col])}))
else:

    st.title('Period Payment Calculator :dollar:')

    principal = st.number_input('Enter Loan Principal:',format="%.2f")
    interest = st.number_input('Enter Interest Rate',format="%.2f")
    periods = st.number_input('Enter Number of Payment Periods')

    if principal and interest and periods:
        payment = amt_backend.payment(principal,interest,periods)
        st.write('The recommened payment per scheduled period is $:',round(payment.calc_payment(),2))

st.cache_data.clear()

