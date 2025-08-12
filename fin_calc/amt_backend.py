import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


#Amortization schedule class
#Amortization schedule class
class amortization_schedule:

    def __init__(self,loan_amount, loan_term_years, interest_rate,user_payment,freq='monthly'):
        self.freq = freq
        self.loan_amount = loan_amount
        self.interest = (interest_rate/100) if interest_rate > 1 else interest_rate
        self.loan_term_years = int(loan_term_years)

        if self.freq == 'monthly':
            self.interest_rate = self.interest / 12
            self.total_payments = self.loan_term_years * 12

        else:
            self.interest_rate = self.interest
            self.total_payments = self.loan_term_years

        self.payment = round((loan_amount * self.interest_rate) / (1 - (1 + self.interest_rate) ** -self.total_payments),2)
        if user_payment > self.payment:
            self.payment = user_payment
        # Initialize lists to store schedule data
        self.payment_number = []
        self.remaining_balance = []
        self.principal_paid = []
        self.interest_paid = []
        self.total_interest_paid = []
        self.total_paid = []

        self.total_amount_paid = round(self.payment * self.total_payments, 2)
        self.total_itr_paid = None


    def generate_schedule(self):
        # Initialize balance to the loan amount
        balance = self.loan_amount

        # Generate amortization schedule
        for i in range(1, self.total_payments + 1):
            interest = balance * self.interest_rate
            principal = self.payment - interest
            balance -= principal


            self.payment_number.append(i)
            self.remaining_balance.append(round(balance,2))
            self.principal_paid.append(round(principal,2))
            self.interest_paid.append(round(interest,2))
            self.total_paid.append(round(self.payment * i,2))

            if i == 1:
                self.total_interest_paid.append(round(interest,2))
            else:
                self.total_interest_paid.append(round(self.total_interest_paid[-1]+interest,2))

        self.total_itr_paid = round(sum(self.interest_paid),2)

        # Create DataFrame for amortization schedule
        schedule_df = pd.DataFrame({
            'Payment Number': self.payment_number,
            'Principal Paid': self.principal_paid,
            'Interest Paid': self.interest_paid,
            'Total Interest Paid':self.total_interest_paid,
            'Total Paid': self.total_paid,
            'Remaining Balance': self.remaining_balance
        })

        schedule_df = schedule_df.set_index('Payment Number')
        return schedule_df

    def generate_graph(self,df):
        arc = df[['Remaining Balance','Total Interest Paid','Total Paid']]
        fig = px.line(arc,x=list(range(len(arc))),y = arc.columns).update_layout(xaxis_title='Payment Period')
        return fig
    

#Annuity schedule class
class annuity:

    def __init__(self,principal,cont,interest,term):
        self.principal = principal
        self.cont = cont
        self.interest = (interest/100) if interest > 1 else interest
        self.term = round(term)
        self.annuity_table = self.generate_annuity_schedule(self.principal,self.cont,
                                                            self.interest,self.term)
        self.ending_balance = self.annuity_table.iloc[-1]['Balance']
        self.total_additions = sum(self.annuity_table['Addition'])-self.principal
        self.total_interest = round(sum(self.annuity_table['Gain']),2)
        self.graph = self.generate_annuity_graph(self.annuity_table)
    #generate annuity table
    def generate_annuity_schedule(self,principal,cont,interest,term):
        #initial amount, set as principal plut first contribution
        amt = principal + cont
        period = []
        addition = []
        gain = []
        balance = []

        for i in range(term):
            period.append(i+1)
            if i > 0:
                addition.append(cont)
            else:
                addition.append(principal+cont)
            #interest for the current term
            ti = (amt*interest)
            var = amt + ti
            gain.append(round(ti,2))
            balance.append(round(var,2))
            amt += (ti+cont)
        
        data = pd.DataFrame({'Year':period,'Addition':addition,'Gain':gain,
                            'Balance':balance})
        return data

    #generate graph for annuity return
    def generate_annuity_graph(self,df):
        data = df[['Addition','Gain','Balance']].copy()
        #reassing initial addition as inital contribution
        data.at[0,'Addition']= self.cont
        #set column as cummulative sum of addition
        data['Addition'] = data['Addition'].cumsum()
        #set column as cummulative sum of gain
        data['Gain'] = data['Gain'].cumsum()
        fig = px.bar(data,title='Annuity Return')
        return fig


#class to determine return (NPV and IRR) based on individual cash flows
class investment_ret:
    
    def __init__(self,initial,cf,interest):
        self.cash_flows = [initial] + cf
        self.interest = (interest/100) if interest > 1 else interest
        self.npv = self.nominal_npv(self.cash_flows,self.interest) 
        self.graph = self.generate_graph(self.cash_flows)

    #add cash flow, account for interest
    def nominal_npv(self,cash_flows,inter):
        income = cash_flows[0]
        for i in range(1,len(cash_flows)):
            alpha = cash_flows[i]/((1+inter)**(i))
            income += alpha 
        return income
    
    #converge lower and upper bound to obtain present value that equals 0 or is close within tolerance margin
    def nominal_IRR(self,cash_flows):
        lower_bound = -1.0
        upper_bound = 1.0
        #tolerance (margin of error)
        tol=1e-6
        iteration = 0 

        while iteration < 1000:
            mid_rate = (lower_bound + upper_bound) / 2
            mid_npv = self.nominal_npv(cash_flows,mid_rate)

            if abs(mid_npv) < tol:
                return round((mid_rate*100),2)
            
            if mid_npv > 0:
                lower_bound = mid_rate
            else:
                upper_bound = mid_rate

            iteration +=1 
        raise ValueError("IRR did not converge")
    
    def generate_graph(self,cash_flows):
        series = pd.Series(cash_flows)
        fig = px.line(series,labels={'variable':'return'}, title='Cash Flows History')
        return fig

#process user input as array of numbers
def process_input(data):
    #Aggregate input into valid numerical array
    if ',' not in data:
        return 'Please enter data in valid format'
    alpha = []
    for x in  data.split(','):  
        valid = True
        negative = False
        cnt = 0
        var = ''
        
        for n in x:
            if n == '-':
                negative = True 
                continue
            if n == ' ':
                continue
            if n.isnumeric() == False and n != '.':
                valid = False
            if n == '.':
                cnt += 1
    
            var += n
            if cnt > 1:
                valid = False
                
            if valid == False:
                break

        if valid == True:
            var = float(var)
            if negative == True:
                var = -(var)
            alpha.append(var)
    return alpha





