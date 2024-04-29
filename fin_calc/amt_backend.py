import pandas as pd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class amortization_schedule:

    def __init__(self,loan_amount, loan_term_years, interest_rate,freq='monthly'):
        self.loan_amount = loan_amount
        # Calculate monthly interest rate
        self.monthly_interest_rate = interest_rate / 12 / 100
        # Calculate total number of payments
        self.loan_term_years = int(loan_term_years)
        self.total_payments = self.loan_term_years * 12
        # Calculate monthly payment
        self.monthly_payment = round((loan_amount * self.monthly_interest_rate) / (1 - (1 + self.monthly_interest_rate) ** -self.total_payments),2)
        self.freq = freq
        # Initialize lists to store schedule data
        self.payment_number = []
        self.remaining_balance = []
        self.principal_paid = []
        self.interest_paid = []
        self.total_interest_paid = []
        self.total_paid = []
        self.schedule = self.generate_schedule()
        self.graph = self.generate_graph(self.schedule)
        #aggregated payment metrics
        self.total_paid = round(self.monthly_payment * self.total_payments, 2)
        self.interest_paid = round(sum(self.interest_paid,2))
    
    def generate_schedule(self): 
        # Initialize balance to the loan amount
        balance = self.loan_amount

        # Generate amortization schedule
        for i in range(1, self.total_payments + 1):
            interest = balance * self.monthly_interest_rate
            principal = self.monthly_payment - interest
            balance -= principal


            self.payment_number.append(i)
            self.remaining_balance.append(round(balance,2))
            self.principal_paid.append(round(principal,2))
            self.interest_paid.append(round(interest,2))
            self.total_paid.append(round(self.monthly_payment * i,2))

            if i == 1:
                self.total_interest_paid.append(interest)
            else:
                self.total_interest_paid.append(self.total_interest_paid[-1]+interest)

        # Create DataFrame for amortization schedule
        schedule_df = pd.DataFrame({
            'Payment Number': self.payment_number,
            'Principal Paid': self.principal_paid,
            'Interest Paid': self.interest_paid,
            'Total Interest Paid':self.total_interest_paid,
            'Total Paid': self.total_paid,
            'Remaining Balance': self.remaining_balance
        })
        #Generate yealry amortization table
        if self.freq == 'yearly':
            yrly_schedule = pd.DataFrame(columns=schedule_df.columns)
            cnt = 12
            for i in range(self.loan_term_years):
                alpha = schedule_df.iloc[cnt-12:cnt]
                var = {'Payment Number':cnt, 'Principal Paid':alpha['Principal Paid'].sum(),
                    'Interest Paid':alpha['Interest Paid'].sum(), 
                    'Total Interest Paid':list(alpha['Total Interest Paid'])[-1],
                    'Total Paid':list(alpha['Total Paid'])[-1],
                    'Remaining Balance':list(alpha['Remaining Balance'])[-1]}
                # print(var)
                df_var = pd.DataFrame(var,index=[0])
                yrly_schedule = pd.concat([yrly_schedule,df_var],ignore_index=True)
                cnt += 12
            return yrly_schedule

        return schedule_df

    def generate_graph(self,df):
        arc = df[['Remaining Balance','Total Interest Paid','Total Paid']]
        fig = px.line(arc,x=list(range(len(arc))),y = arc.columns).update_layout(xaxis_title='Payment Period')
        return fig





