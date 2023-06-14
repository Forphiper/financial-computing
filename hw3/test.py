from hw3 import trinomial_tree
import pandas as pd
import itertools
from tqdm import tqdm
import time

start_time = time.perf_counter()

S_values = [103.8, 100, 150.99]
K_values = [97.45, 101.9, 168]
r_values = [4.2, 5.11, 15]
s_values = [25.82, 30, 30.54]
T_values = [0.5, 1.8, 3]
H_values = [87.65, 90, 93.4]
n_values = [75, 203, 342]

total_iterations = len(list(itertools.product(S_values, K_values, r_values, s_values, T_values, H_values, n_values)))
print(f"Number of testcases = {total_iterations}")

prices = []
for values in tqdm(itertools.product(S_values, K_values, r_values, s_values, T_values, H_values, n_values), total=total_iterations):
    S, K, r, s, T, H, n = values
    prices.append(round(trinomial_tree(S, K, r, s, T, H, n), 4))

data = [[price] for price in prices]
df = pd.DataFrame(data, columns=['prices'])

file_name = "trinomial_test.csv"
print(f"Outputting a csv file named {file_name}")
df.to_csv(file_name, index=False)

end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.4f} seconds\n")

url = "https://www.csie.ntu.edu.tw/~r11922148/trinomial.csv"
wait_time = 20
print(f"Trying to read data from {url}")
while True:
    try:
        df_url = pd.read_csv(url)
        print("Data read successfully!")
        break
    except Exception as e:
        print(f"Error: {e}")
        print(f"Waiting {wait_time} seconds before trying again...")
        time.sleep(wait_time)

#print(df.head())
#print(df_url.head())

print("Checking if the two DataFrames are the same")
if df.equals(df_url):
    print("DataFrames are the same!")
else:
    print("DataFrames are not the same")
    
    df_diff = df.compare(df_url)
    print("Differeces:")
    print(df_diff)
