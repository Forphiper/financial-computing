"""
Implement the Least Square Monte Carlo method to price an American option. Use 1, x, x^2, x^3 as the basis functions. 

Inputs:
(1) S (stock price), 
(2) K (strike price), 
(3) r (interest rate), 
(4) s (volatility), 
(5) T (time to maturity in years), 
(6) n (number of time steps), 
(7) N (number of simulation paths). 

Output: Option price and the standand error. 

IMPORTANT notes: 
(1) The interest rate and volatility should be in percent. For example, if the interest rate is 1% and volatility 10%, the inputs are 1 and 10, respectively. 
"""

import numpy as np
import warnings

np.random.seed(42)

def american_put_price(S, K, r, s, T, n, N):
    """ Pricing an American put option using Least Square Monte Carlo method
    (1) Initialize variables
    (2) Generate stock price paths using Brownian motion
    (3) Calculate the payoffs of the last period
    (4) Decide whether to early exercise or not at each point
    (5) Calculate average option price and standard error
    """

    # (1) Initialize variables
    r /= 100
    s /= 100
    dt = T / n
    discount_factor = np.exp(-r * dt)

    # (2) Generate stock price paths using Brownian motion
    stock_price_paths = np.zeros((N, n + 1))
    stock_price_paths[:, 0] = S
    num_random_values = (N + 1) // 2
    for time_period in range(1, n + 1):
        normal_random_values = np.random.standard_normal(size=num_random_values)
        # Add the antithetic variates
        normal_random_values = np.append(normal_random_values, -normal_random_values[:num_random_values-1]) if N % 2 != 0 \
                               else np.append(normal_random_values, -normal_random_values)
        stock_price_paths[:, time_period] = stock_price_paths[:, time_period-1] * \
                                            np.exp((r - 0.5 * (s ** 2)) * dt + s * np.sqrt(dt) * normal_random_values)
    
    # (3) Calculate the payoffs of the last period
    curr_cash_flows = np.maximum(0, K - stock_price_paths[:, -1])
    
    # Calculate european price for comparison purpose
    european_price = curr_cash_flows.sum() * np.exp(-r * T) / len(curr_cash_flows)
    
    # (4) Decide whether to early exercise or not at each point
    curr_cash_flows = curr_cash_flows * discount_factor
    for time_period in range(n - 1, 0, -1):
        # Only regress on the paths for which option is in the money
        regression_indices = np.where(stock_price_paths[:, time_period] <= K)[0]
        if len(regression_indices) == 0:
            curr_cash_flows = curr_cash_flows * discount_factor
            continue

        # Let y be the expected value of continuation
        y = curr_cash_flows[regression_indices]
        # Let x be the stock prices at the current time period
        x = stock_price_paths[regression_indices, time_period]
        
        # Flatten both x and y to 1d for regression
        y = y.flatten()
        x = x.flatten()
        
        # Least squares polynomial fit
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', np.RankWarning)
            coefficients = np.polyfit(x, y, deg=3, rcond=None)
        
        # Compare immediate exercise value to the output of regression
        curr_cash_flows[regression_indices] = np.where(K - x >= np.polyval(coefficients, x),
                                                       K - x, curr_cash_flows[regression_indices])
        
        curr_cash_flows = curr_cash_flows * discount_factor

    # (5) Calculate the average option price and standard error
    option_price = curr_cash_flows.sum() / (len(curr_cash_flows))
    if option_price < K - S:
        option_price = K - S
    std_dev = np.std(curr_cash_flows, ddof=1)
    standard_error = std_dev / np.sqrt(len(curr_cash_flows))
    
    return option_price, standard_error, european_price


if __name__ == "__main__":
    # Take inputs and output the answer
    print("American put option pricing")
    S = float(input("Enter S: "))
    K = float(input("Enter K: "))
    r = float(input("Enter r: "))
    s = float(input("Enter s: "))
    T = float(input("Enter T: "))
    n = int(input("Enter n: "))
    N = int(input("Enter N: "))

    american_price, standard_error, european_price = american_put_price(S, K, r, s, T, n, N)
    print(f"American put option price= {american_price:.4f}")
    print(f"Standard error= {standard_error:.4f}")
