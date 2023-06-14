"""
* Write a program to generate an amortization schedule for repaying a loan. There are two interest rates. 
* Inputs: 
    * (1) L (loan amount in dollars), 
    * (2) r1 (annual interest rate in percent for the first n1 periods, so 12 instead of 0.12), 
    * (3) r2 (annual interest rate in percent for the remaining periods), 
    * (4) n1 (number of periods when the interest rate is r1), 
    * (5) n (duration of the loan in years), and 
    * (6) m (the number of payments per annum). 
* Output: 
    * A csv file for the amortization schedule and the total interest paid. The schedule shall have five columns: 
    * (1) Time (0, 1, 2, ...), 
    * (2) The level payment amount, 
    * (3) Interest (the interest part of each payment), 
    * (4) Principal (the principal part of each payment), and 
    * (5) Remaining principal. 
* For example, if L = 10,000,000, r1 = 8%, r2 = 3%, n1 = 10, n = 20, and m = 12. Please check the example output file here and the total interest is 8593339.37. 
* IMPORTANT notes: 
    * (1) The Time column must be integers (no floating-point numbers). 
    * (2) The Payment, Interest, Principal, and Remaining principal columns must be floating-point numbers up to 2 decimal points. 
    * (3) The order of the columns must be respected. 
    * (4) The headers of the columns must be as in the sample file. 
    * (5) Start from Time 0 instead of Time 1. This means the value of the first row will be 0, 0, 0, 0, L. 
"""

import pandas as pd

def amort_sched(L, r1, r2, n1, n, m):
    n1 = n1 / m
    num_payments = n * m
    df = pd.DataFrame(index=range(num_payments + 1), columns=["Time", "Payment", "Interest", "Principal", "Remaining principal"])
    r1_month_perc = float(r1 / 100 / m)
    r2_month_perc = float(r2 / 100 / m)

    payment  = (L / ((1 - (1 + r1_month_perc) ** (-n1 * m)) / (r1_month_perc) +
                    (1 / (1 + r1_month_perc)) ** (n1 * m) * (1 - (1 + r2_month_perc) ** (-(n - n1) * m)) / (r2_month_perc)))
    
    df.iloc[:, 0] = range(num_payments + 1)
    df.iloc[1:, 1] = payment
    
    df.iloc[0, 1:4] = 0
    df.iloc[0, 4] = L
    
    for i in range(int(n1 * m)):
        df.iloc[i + 1, 2] = df.iloc[i, 4] * r1_month_perc
        df.iloc[i + 1, 3] = payment - df.iloc[i + 1, 2]
        df.iloc[i + 1, 4] = df.iloc[i, 4] - df.iloc[i + 1, 3]
    
    for i in range(int(n1 * m), int(n1 * m + (n - n1) * m)):
        df.iloc[i + 1, 2] = df.iloc[i, 4] * r2_month_perc
        df.iloc[i + 1, 3] = payment - df.iloc[i + 1, 2]
        df.iloc[i + 1, 4] = df.iloc[i, 4] - df.iloc[i + 1, 3]
   
    df.iloc[:, 1:5] = df.iloc[:, 1:5].astype(float).round(2)

    total_interest = 0.0
    for i in range(num_payments + 1):
        total_interest += df.iloc[i, 2]
    print('total interest= {:.2f}'.format(total_interest))
    
    #print(df.head(5))
    #print(df.tail(5))

    df.to_csv("amort.csv", index=False)
    print("Finish outputting csv file")

#amort_sched(10000000, 8, 3, 10, 20, 12)
L = int(input("Enter L: "))
r1 = int(input("Enter r1: "))
r2 = int(input("Enter r2: "))
n1 = int(input("Enter n1: "))
n = int(input("Enter n: "))
m = int(input("Enter m: "))
amort_sched(L, r1, r2, n1, n, m)


