"""
* Write a binomial tree program to price a Bermudan option. The early exercise time points are T/4 and 3T/4 from now, where T is the time to maturity. The payoff function is max(K - S + 1,0).
* Inputs:
    * (1) S (stock price),
    * (2) K (strike price),
    * (3) r (annual interest rate continuously compounded),
    * (4) s (annual volatility),
    * (5) T (time to maturity in years),
    * (6) n (number of time steps).
* Output: Option price.
* For example, suppose that S = 100, K = 100, r = 5 (%), s = 30 (%), and T = 0.5 (years). The option price is about 7.8052 at n = 100 and 7.8015 at n = 200.
* IMPORTANT NOTES:
    * (1) The interest rate and volatility should be in percent. For example, if the interest rate is 5% and volatility 30%, the inputs are 5 and 30, respectively.
    * (2) No need to make sure the early exercise dates are aligned with time steps of the tree.
"""


import math

def binomial_tree(S, K, r, s, T, n):
    r = r / 100
    s = s / 100
    
    dt = T / n
    u = math.exp(s * (dt ** 0.5))
    d = 1 / u
    
    r_hat = r * dt
    R = math.exp(r_hat)
    p = (R - d) / (u - d)
    
    option_values = [[0.0 for j in range(i + 1)] for i in range(n + 1)]
    
    for j in range(n + 1):
        option_values[n][j] = max(option_values[n][j], K - S * (u ** (n - j)) * (d ** j) + 1)
    
    for i in range(n - 1, -1, -1):
        for j in range(i + 1):
            option_values[i][j] = (1 / R) * (p * option_values[i + 1][j] + (1 - p) * option_values[i + 1][j + 1])
            
            # check if early exercise is optimal
            if i == n / 4 or i == 3 * n / 4:
                early_exercise_value =  max(0.0,  K - S * (u ** (i - j)) * (d ** j) + 1)
                option_values[i][j] = max(option_values[i][j], early_exercise_value)

    return option_values[0][0]


if __name__ == "__main__":
    S = float(input("Enter S: "))
    K = float(input("Enter K: "))
    r = float(input("Enter r: "))
    s = float(input("Enter s: "))
    T = float(input("Enter T: "))
    n = int(input("Enter n: "))

    print(f"Option price = {round(binomial_tree(S, K, r, s, T, n), 4)}")


"""
# generate testcases
import pandas as pd
import itertools

S_values = [55.8, 100, 150.99]
K_values = [80.45, 100.9, 127]
r_values = [4.2, 5.11, 15]
s_values = [25.82, 30, 30.54]
T_values = [0.5, 1.8, 3.3]
n_values = [100, 200, 300]

prices = []
for values in itertools.product(S_values, K_values, r_values, s_values, T_values, n_values):
    S, K, r, s, T, n = values
    prices.append(round(binomial_tree(S, K, r, s, T, n), 4))

data = [[price] for price in prices]
df = pd.DataFrame(data, columns=['prices'])
df.to_csv('test_prices.csv', index=False)
"""
