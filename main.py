from Pool import Pool

swap_fee: float = 0.003

def quadratic_formula(a: float, b: float, c: float, high_val: float) -> float:
    discriminant = b**2 - 4*a*c
    if discriminant < 0 or a == 0:
        return None
    
    root_1 = (-b + discriminant**0.5) / (2*a)
    root_2 = (-b - discriminant**0.5) / (2*a)

    if root_1 < 0:
        if root_2 > high_val:
            return None
        elif root_2 < 0:
            return None
        else:
            return root_2
    else:
        if root_2 > high_val:
            return root_1
        else:
            return max(root_1, root_2)

def profit_calculation(x: float, a1: float, b1: float, a2: float, b2: float) -> float:
    frac1 = ((1 - swap_fee) * x * a2) / (b2 + (1 - swap_fee) * x)
    frac2 = (x * a1) / (b1 - x)
    return frac1 - frac2

def input_calculation(x: float, a1: float, b1: float) -> float:
    input_without_fee = (x * a1) / (b1 - x)
    return input_without_fee / (1 - swap_fee)

def arbitrage_calculation(poolA: Pool, poolB: Pool) -> float:
    price_ratio_A = poolA.price_ratio()
    price_ratio_B = poolB.price_ratio()
    a1, b2, a2, b2 = 0, 0, 0, 0

    if price_ratio_A > price_ratio_B:
        a1 = poolA.get_amt_eth() 
        b1 = poolA.get_amt_dai()
        a2 = poolB.get_amt_eth()
        b2 = poolB.get_amt_dai()
    elif price_ratio_A < price_ratio_B:
        a1 = poolB.get_amt_eth()
        b1 = poolB.get_amt_dai()
        a2 = poolA.get_amt_eth()
        b2 = poolA.get_amt_dai()
    else:
        return None

    quadratic_a = a1 * b1 * ((1 - swap_fee) ** 2) - (1 - swap_fee) * a2 * b2
    quadratic_b = (1 - swap_fee) * 2 * b1 * b2 * (a1 + a2)
    quadratic_c = b1 * b2 * (a1 * b2 - (1 - swap_fee) * a2 * b1)
    high_val = max(a1, b2, a2, b2)
    quadratic_result = quadratic_formula(quadratic_a, quadratic_b, quadratic_c, high_val)

    if quadratic_result is None:
        return None
    profit = profit_calculation(quadratic_result, a1, b1, a2, b2)
    input_eth = input_calculation(quadratic_result, a1, b1)

    return [input_eth, profit] if profit > 0 and input_eth > 0 else None

if __name__ == "__main__":
    # initialize pools
    poolA = Pool(total_eth=40, total_dai=200, swapFee=swap_fee)
    poolB = Pool(total_eth=20, total_dai=50, swapFee=swap_fee)
    poolC = Pool(total_eth=100, total_dai=200, swapFee=swap_fee)
    poolD = Pool(total_eth=200, total_dai=800, swapFee=swap_fee)

    # simple testcases
    poolA.add_liquidity(10, 'ETH')
    print(poolA)
    poolA.remove_liquidity(5, 'ETH')
    print(poolA)

    poolA.swap_token(3, 'ETH')
    print(poolA)

    input_eth, profit = arbitrage_calculation(poolC, poolD)
    print(f"Input ETH: {input_eth}, Profit: {profit}")

    ''' non Blocking calculation triggering in benchmark.py '''