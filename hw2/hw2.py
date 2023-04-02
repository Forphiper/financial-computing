import math
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('S', type=float, action='store', nargs='?', default=100, help='stock price')
parser.add_argument('K', type=float, action='store', nargs='?', default=100, help='strike price')
parser.add_argument('r', type=float, action='store', nargs='?', default=5, help='annual interest rate continuously compounded')
parser.add_argument('s', type=float, action='store', nargs='?', default=30, help='annual volatility')
parser.add_argument('T', type=float, action='store', nargs='?', default=0.5, help='time to maturity in years')
parser.add_argument('n', type=int, action='store', nargs='?', default=100, help='number of time steps')
args = parser.parse_args()

def binomial_tree(S, K, r, s, T, n):
    early_exercise_times = [T / 4, 3 * T / 4]
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
            if (i * dt) in early_exercise_times:
                early_exercise_value = max(0.0, K - S * (u ** (i - j)) * (d ** j) + 1)
                option_values[i][j] = max(option_values[i][j], early_exercise_value)
     
    return option_values[0][0]


print("Inputs: ")
print(f"stock price= {args.S}")
print(f"strike price = {args.K}")
print(f"annual interest rate continuously compounded = {args.r}")
print(f"annual volatility = {args.s}")
print(f"time to maturity in years = {args.T}")
print(f"number of time steps = {args.n}")

print("\n")
print("Output: ")
print(f"Option price = {binomial_tree(args.S, args.K, args.r, args.s, args.T, args.n)}")


