import pandas as pd

class loan_amt:

    def __init__(self,ct,principal,interest):
        self.payment = round(ct,2)
        self.principal = round(principal,2)
        self.interest = round(interest,2) 
        self.int_paid = 0
        self.cost_of_loan = principal


    def new_amt(self):
        itr = round(self.interest/100,2)
        period = 0
        balance_list = []
        int_payments = []
        prc_list = []
        period_list = []
        balance_list.append(self.principal)

        while self.principal > 0:
            period += 1
            period_list.append(period)
            period_interest = round(self.principal*itr)
            prc = self.payment - period_interest
            prc_list.append(prc)
            int_payments.append(period_interest)
            self.int_paid += period_interest
            self.principal += period_interest
            if self.principal - self.payment > 0:
                self.principal -= self.payment
                balance_list.append(self.principal)
            else:
                break 
        print(len(period_list))
        print(len(balance_list))
        print(len(int_payments))
        print(len(prc_list))
        print(len(balance_list[1:]+[0]))

        print(balance_list)
        

        self.cost_of_loan += self.int_paid
        amt = {'Periods':period_list,'Balance':balance_list,'Interest':int_payments,'Principal':prc_list,'Ending Balance': balance_list[1:]+[0]}
        # amt = {'Periods':period_list,'Interest':int_payments,'Principal':prc_list}
        table = pd.DataFrame(amt)
        table.set_index('Periods',inplace=True)
        print(table)
        return table

class payment:

    def __init__(self,principal,interest,periods):
        self.principal = principal
        self.interest = interest
        self.n_periods = periods

    
    def calc_payment(self):
        itr = self.interest/100
        pyt = (itr*self.principal)/(1-(1+itr)**(-self.n_periods))
        return pyt



    # interest = itr/100
    # payment = (interest*pv)/(1-(1+interest)**(-pr))
    # return payment
        