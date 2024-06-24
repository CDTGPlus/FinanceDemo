import streamlit as st
import pandas as pd
from amt_backend import *


page_icon = ':money_with_wings:'
st.set_page_config('Financial Calculator',page_icon=page_icon)
#user enters financial caculation option
option = st.sidebar.radio('Menu', ['Amortization','Annuity','NPV and IRR'])


if option == 'Amortization':
    #amortization, validate all parameters are entered, select yearly or monthly periods
    st.title('Amortization Schedule')

    freq_option = st.selectbox('Select Payment Frequency',('Yearly','Monthly'))

    if freq_option == 'Yearly':
        freq = 'yearly'
    else:
        freq = 'monthly'
    
    principal = st.number_input('Enter Loan Principal:',format="%.2f")
    payment_period = st.number_input('Enter loan term in years:',format="%.2f")
    interest = st.number_input('Enter Interest Rate')
    #display amortization metrics, table and graph(line)
    if principal and payment_period and interest:
        amt = amortization_schedule(principal,payment_period,interest,freq)
        st.write('Montly Payment: $',str(amt.monthly_payment))
        st.write('Total paid: $',str(amt.total_paid))
        st.write('Total Interest: $',str(amt.interest_paid))
        st.plotly_chart(amt.graph)
        df = amt.schedule
        st.table(df.style.format({col: '{:.2f}' for col in df.columns if pd.api.types.is_float_dtype(df[col])}))

    else:
        st.write('Enter Complete Data')



if option == 'Annuity':
    st.title('Annuity Schedule')
    principal = st.number_input('Enter Starting Pirncipal')
    contribution = st.number_input('Enter Contribution per Period')
    interest = st.number_input('Enter Interest Rate')
    per_n = st.number_input('Enter Number of Periods')
    #display annuity metrics, table and graph(stacked bar chart)
    if principal and contribution and interest and per_n:
        annuity_n = annuity(principal,contribution,interest,per_n)
        st.write("Ending Balance:",str(annuity_n.ending_balance))
        st.write("Starting Principal:",str(annuity_n.principal))
        st.write("Total Additions:",str(annuity_n.total_additions))
        st.write("Total Interest Earned:",str(annuity_n.total_interest))
        st.plotly_chart(annuity_n.graph)
        df = annuity_n.annuity_table
        st.table(df.style.format({col: '{:.2f}' for col in df.columns if pd.api.types.is_float_dtype(df[col])}))
        

    else:
        st.write('Enter Complete Data')

elif option == 'NPV and IRR':
    #user enters initial investment, interest and periodic cash flows
    st.title('Net Present Value & Internal Rate of Return')
    initial = st.number_input('Enter Initial investment')
    if initial > 0:
        initial = -(initial)
    cash_flows = st.text_area('Enter subsequent cash flows separated by " , " (comma):')
    cf = process_input(cash_flows)
    interest_rate = st.number_input('Enter interest rate:')

    if initial and (type(cf) == list):
        
        ret = investment_ret(initial,cf,interest_rate)
        
        st.write('Net Present Value:',str(round(ret.npv, 2)))
        try:
            
            st.write(f'Internal Rate or Return: {ret.nominal_IRR(ret.cash_flows)} %')
        except ValueError as e:
            st.error(str(e))

        st.plotly_chart(ret.graph)
    else:
        st.write('Enter Complete Data')

        


