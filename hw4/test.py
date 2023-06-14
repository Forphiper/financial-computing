from hw4 import american_put_price
import itertools
import pandas as pd
import numpy as np
from tqdm import tqdm
import time

start_time = time.time()

# Example testcases from the paper
S_values = [val for val in range(36, 46, 2)]
K = 40
r = 6
s_values = [val for val in range(20, 60, 20)]
T_values = [val for val in range(1, 3, 1)]
N = 100000

paper_prices = [4.472, 4.821, 7.091, 8.488,
                3.244, 3.735, 6.139, 7.669,
                2.313, 2.879, 5.308, 6.921,
                1.617, 2.206, 4.588, 6.243,
                1.118, 1.675, 3.957, 5.622]

total_iterations = len(list(itertools.product(S_values, s_values, T_values)))
print(f"Calculating {total_iterations} testcases of the paper...")
column_names = ["S", "s(%)", "T", "Your American price", "standard error", "European price", "Paper American price"]
df = pd.DataFrame(columns=column_names)

print(f"K= {K}, r= {r}%, N= {N}, 50 exercisable points per year")
for index, values in tqdm(enumerate(itertools.product(S_values, s_values, T_values)), total=total_iterations):
    S, s, T = values
    n = T * 50
    american_price, standard_error, european_price = american_put_price(S, K, r, s, T, n, N)
    curr_row_values = [S, s, T, round(american_price, 4), round(standard_error, 4), round(european_price, 4), round(paper_prices[index], 4)]
    df.loc[len(df)] = curr_row_values

df[["S", "s(%)", "T"]] = df[["S", "s(%)", "T"]].astype(int)
print(df)

# Show execution time
end_time = time.time()
execution_time = end_time - start_time
if execution_time >= 60:
    minutes = execution_time // 60
    seconds = execution_time % 60
    print(f"Execution time: {int(minutes)} m {seconds:.4f} s\n")
else:
    print(f"Execution time: {execution_time:.4f} s\n")

# Comparing prices with the paper prices
print("Comparing your calculated prices with the paper prices...")

column_names = ["S", "K", "r(%)", "s(%)", "T", "n", "N", "Your American price", "Paper American price"]
diff_df = pd.DataFrame(columns=column_names)

margin_error = 0.03
for index, value in df["Your American price"].items():
    if value < paper_prices[index] * (1 - margin_error) or value > paper_prices[index] * (1 + margin_error):
        curr_row_values = [df["S"][index], K, r, df["s(%)"][index], 
                           df["T"][index], df["T"][index] * 50, N,
                           round(value, 4), round(paper_prices[index], 4)]
        diff_df.loc[len(diff_df)] = curr_row_values

if diff_df.empty:
    print(f"Your calculated prices are all within a margin of plus or minus {int(margin_error*100)}% of the paper prices!")
else:
    print(f"Some of your calculated prices exceed a margin of plus or minus {int(margin_error*100)}% of the paper prices")
    print("The following are the testcases that are not within the margin of error")
    diff_df[["S", "K", "r(%)", "s(%)", "T", "n", "N"]] = diff_df[["S", "K", "r(%)", "s(%)", "T", "n", "N"]].astype(int)
    print(diff_df)


"""
# Testcases of random inputs
np.random.seed(72)
num_testcases = 20
S_values = np.random.uniform(16500, 17000, num_testcases)
K_values = np.random.uniform(16500, 17000, num_testcases)
r_values = np.random.uniform(3, 15, num_testcases)
s_values = np.random.uniform(5, 50, num_testcases)
T_values = np.random.uniform(1, 10, num_testcases)
n_values = np.random.randint(25, 1000, num_testcases)
N_values = np.random.randint(100, 100000, num_testcases)

print(f"Testing {num_testcases} testcases of random inputs")
column_names = ["S", "K", "r(%)", "s(%)", "T", "n", "N", "American price", "standard error"]
df = pd.DataFrame(columns=column_names)

for S, K, r, s, T, n, N in tqdm(zip(S_values, K_values, r_values, s_values, T_values, n_values, N_values), total=num_testcases):
    american_price, standard_error = american_put_price(S, K, r, s, T, n, N)
    curr_row_values = [S, K, r, s, T, n, N, round(american_price, 4), round(standard_error, 4)]
    df.loc[len(df)] = curr_row_values

df[["n", "N"]] = df[["n", "N"]].astype(int)
print(df)
"""
