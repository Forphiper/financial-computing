# Principles of Financial Computing

## HW1
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

## HW2
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

## HW3
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

## HW4
* Implement the Least Square Monte Carlo method to price an American option. Use 1, x, x^2, x^3 as the basis functions. 
* Inputs
    * (1) S (stock price), 
    * (2) K (strike price), 
    * (3) r (interest rate), 
    * (4) s (volatility), 
    * (5) T (time to maturity in years), 
    * (6) n (number of time steps), 
    * (7) N (number of simulation paths). 
* Output: Option price and the standand error. 
* IMPORTANT notes: 
    * (1) The interest rate and volatility should be in percent. For example, if the interest rate is 1% and volatility 10%, the inputs are 1 and 10, respectively.
