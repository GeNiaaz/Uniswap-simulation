
# About
This application attempts to simulate the mechanism of tokens swap on Uniswap. The mechanism also automatically dictates the price ratio to keep the system in equilibrium. I have written both functional tests as well as benchmark tests to gauge performance.

# Running Code

## Main
Run the command `python3 main.py`

## Tests

### test.py (unit tests):
Run the command `python3 -m unittest -v test`

### benchmark.py (non blocking benchmarks):
Run the command `python3 benchmark.py`

# Design Choices

## Calculating price of trade
I derived the price of a token based upon the price after adding in the tokens to swap.

Why I did this was because after reading on how the exchanges work, the general rationale for this mechanism is to ensure that the larger the amount of coins swapped the more expensive it becomes. To follow the example in the image would not maintain this factor, and hence the price charged is the price after adding in tokens for each swap.

## Arbitrage calculation logic
I chose to go with modelling the maximum profit as a function. I found the differential and equated the differential to zero to find the maxima. 

The reason I believe that a maxima is possible is because profit at both ends (initial state + small ε or from ε away from the equilibrium pooint) would be close to zero if not negative. Going inwards in both directions would lead to an increase in profit. Hence my idea was to find the point where the profit peaks.

My initial intuition was to simply equate the ratio of the amounts of each coin in each exchange together, ie a1 / b1 = a2 / b2, where a represents one of the two exchanges and the numbers represent the ETH / DAI. However, I believe this does not give the maximum possible profit and I will attempt to prove that below:

claim 1: breaking a trade into two smaller consecutive trades results in the same net profit (due to the nature of proportional fees that have no minimum amount)

claim 2 : trades extremely close to equilibrium have negative profit (due to fees)

Therefore, for some nonzero fee, if the current state differs from equilibrium by k, then there exists some ε such that trading (k-ε) is more profitable than trading k

Due to this, I chose to instead model the profit as a function and find the maxima instead.

# Assumptions
1. Fee is inclusive in the input amount when executing swap (This assumes that the amount the user puts into the swap already includes the fee and user does not need to provide additional tokens for the 0.3% fee).
2. Amount of token returned after a swap has taken place is calculated after price impact from the transaction itself
3. An LP can choose to input the amount of ETH and the equivalent value of DAI will be calculated. (it is assumed that the LP has an equivalent value of DAI based on the ETH input, or vice versa).
4. The amount that the user gets when swapping is calculated using the input token's 99.7% value. Because only after this calculation will the 0.3% fee be included to add to the reserves. This allows for the K value to increase accordingly.
