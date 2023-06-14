from hw2 import binomial_tree 
import pandas as pd
import itertools

# generate testcases
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

