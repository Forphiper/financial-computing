import pandas as pd

def amort_sched(L, r1, r2, n1, n, m):
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
    
    for i in range(n1 * m):
        df.iloc[i + 1, 2] = df.iloc[i, 4] * r1_month_perc
        df.iloc[i + 1, 3] = payment - df.iloc[i + 1, 2]
        df.iloc[i + 1, 4] = df.iloc[i, 4] - df.iloc[i + 1, 3]
    
    for i in range(n1 * m, n1 * m + (n - n1) * m):
        df.iloc[i + 1, 2] = df.iloc[i, 4] * r2_month_perc
        df.iloc[i + 1, 3] = payment - df.iloc[i + 1, 2]
        df.iloc[i + 1, 4] = df.iloc[i, 4] - df.iloc[i + 1, 3]
   
    df.iloc[:, 1:5] = df.iloc[:, 1:5].astype(float).round(2)
    
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


