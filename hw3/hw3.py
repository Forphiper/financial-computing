"""
* Write a trinomial tree program to price a down-and-out barrier call.
* Inputs:
    * (1) S (stock price),
    * (2) K (strike price),
    * (3) r (interest rate),
    * (4) s (annual volatility),
    * (5) T (time to maturity in years),
    * (6) H (barrier), and
    * (7) n (number of time steps).
* Output: Option price.
* For example, suppose that S = 95, K = 100, r = 10 (%), s = 25 (%), H = 90, and T = 1. The option price is about 5.9899 at n = 75 and 5.9977 at n = 400.
* IMPORTANT notes:
    * (1) The interest rate and volatility should be in percent. For example, if the interest rate is 5% and volatility 30%, the inputs are 5 and 30, respectively.
    * (2) The trinomial tree must matches the barrier.
"""


import math
import numpy as np

def trinomial_tree(S, K, r, s, T, H, n):
    r = r / 100
    s = s / 100
    dt = T / n

    h = int(np.floor(np.log(S / H) / (s * np.sqrt(dt))))
    if h < 1 or h > n:
        raise ValueError("Error: h must be between 1 and n.")
    lamb = np.log(S / H) / (h * s * np.sqrt(dt))

    p_u = 1 / (2 * lamb ** 2) + (r - s ** 2 / 2) * np.sqrt(dt) / (2 * lamb * s)
    p_d = 1 / (2 * lamb ** 2) - (r - s ** 2 / 2) * np.sqrt(dt) / (2 * lamb * s)
    p_m = 1 - p_u - p_d

    u = np.exp(lamb * s * np.sqrt(dt))

    # calculate node prices of last step
    call_prices = np.zeros(2 * n + 1)
    node_ids = np.arange(n, -(n + 1), -1)
    call_prices = np.maximum(0, S * u ** node_ids - K)

    # hit
    call_prices[n + h] = 0
    
    for time_step in range(n - 1, -1, -1):
        call_prices[ : -2] = p_u * call_prices[ : -2] + \
                             p_m * call_prices[1 : -1] + \
                             p_d * call_prices[2 : ]

        if time_step >= h:
            # hit
            call_prices[time_step + h] = 0
    
    return call_prices[0] / np.exp(r * T)


if __name__ == "__main__":
    # Public cases
    S = 95
    K = 100
    r = 10
    s = 25
    T = 1
    H = 90
    n = 75
    option_price = trinomial_tree(S, K, r, s, T, H, n)
    print(f"Option price at {n} = {option_price:.4f}")

    n = 400
    option_price = trinomial_tree(S, K, r, s, T, H, n)
    print(f"Option price at {n} = {option_price:.4f}")

    # Take input from user
    S = float(input("Enter S: "))
    K = float(input("Enter K: "))
    r = float(input("Enter r: "))
    s = float(input("Enter s: "))
    T = float(input("Enter T: "))
    H = float(input("Enter H: "))
    n = int(input("Enter n: "))
    print(f"Option price = {trinomial_tree(S, K, r, s, T, H, n):.4f}")

