import unittest

from main import quadratic_formula, profit_calculation, input_calculation, arbitrage_calculation
from Pool import Pool, Token

class TestAddLiquidity(unittest.TestCase):
    def setUp(self):
        self.poolA = Pool(total_eth=1000, total_dai=2000000, swapFee=0.003)

    def test_add_liquidity_eth_1(self):
        self.poolA = self.poolA.add_liquidity(100, 'ETH')
        self.assertEqual(self.poolA.total_eth, 1100)

    def test_add_liquidity_eth_2(self):
        self.poolA = self.poolA.add_liquidity(1000, 'ETH')
        self.assertEqual(self.poolA.total_eth, 2000)

    def test_add_liquidity_dai_3(self):
        self.poolA = self.poolA.add_liquidity(100, 'DAI')
        self.assertEqual(self.poolA.total_dai, 2000100)

    def test_add_liquidity_dai_4(self):
        self.poolA = self.poolA.add_liquidity(1000, 'DAI')
        self.assertEqual(self.poolA.total_dai, 2001000)

    def test_add_liquidity_eth_fail_1(self):
        self.poolA = self.poolA.add_liquidity(0, 'ETH')
        self.assertIsNone(self.poolA)

    def test_add_liquidity_eth_fail_2(self):
        self.poolA = self.poolA.add_liquidity(-100, 'ETH')
        self.assertIsNone(self.poolA)

    def test_add_liquidity_dai_fail_1(self):
        self.poolA = self.poolA.add_liquidity(0, 'DAI')
        self.assertIsNone(self.poolA)
    
    def test_add_liquidity_dai_fail_2(self):
        self.poolA = self.poolA.add_liquidity(-100, 'DAI')
        self.assertIsNone(self.poolA)

class TestRemoveLiquidity(unittest.TestCase):
    def setUp(self):
        self.poolA = Pool(total_eth=10, total_dai=50, swapFee=0.003)

    def test_remove_liquidity_eth_1(self):
        self.poolA = self.poolA.remove_liquidity(1, 'ETH')
        self.assertEqual(self.poolA.total_eth, 9)

    def test_remove_liquidity_eth_2(self):
        self.poolA = self.poolA.remove_liquidity(10, 'ETH')
        self.assertEqual(self.poolA.total_eth, 0)

    def test_remove_liquidity_dai_1(self):
        self.poolA = self.poolA.remove_liquidity(1, 'DAI')
        self.assertEqual(self.poolA.total_dai, 49)

    def test_remove_liquidity_dai_2(self):
        self.poolA = self.poolA.remove_liquidity(50, 'DAI')
        self.assertEqual(self.poolA.total_dai, 0)

    def test_remove_liquidity_eth_fail_1(self):
        self.poolA = self.poolA.remove_liquidity(0, 'ETH')
        self.assertIsNone(self.poolA)

    def test_remove_liquidity_eth_fail_2(self):
        self.poolA = self.poolA.remove_liquidity(-1, 'ETH')
        self.assertIsNone(self.poolA)

    def test_remove_liquidity_eth_fail_3(self):
        self.poolA = self.poolA.remove_liquidity(11, 'ETH')
        self.assertIsNone(self.poolA)

    def test_remove_liquidity_dai_fail_1(self):
        self.poolA = self.poolA.remove_liquidity(0, 'DAI')
        self.assertIsNone(self.poolA)
    
    def test_remove_liquidity_dai_fail_2(self):
        self.poolA = self.poolA.remove_liquidity(-1, 'DAI')
        self.assertIsNone(self.poolA)
    
    def test_remove_liquidity_dai_fail_3(self):
        self.poolA = self.poolA.remove_liquidity(51, 'DAI')
        self.assertIsNone(self.poolA)

class TestUpdateAmounts(unittest.TestCase):
    def setUp(self):
        self.poolA = Pool(total_eth=10, total_dai=50, swapFee=0.003)

    def test_update_amounts_1(self):
        self.poolA.update_amounts(10, 50)
        self.assertEqual(self.poolA.total_eth, 20)
        self.assertEqual(self.poolA.total_dai, 100)

    def test_update_amounts_2(self):
        self.poolA.update_amounts(0, 0)
        self.assertEqual(self.poolA.total_eth, 10)
        self.assertEqual(self.poolA.total_dai, 50)

    def test_update_amounts_3(self):
        self.poolA.update_amounts(-10, -50)
        self.assertEqual(self.poolA.total_eth, 0)
        self.assertEqual(self.poolA.total_dai, 0)

    def test_update_amounts_4(self):
        self.poolA.update_amounts(-10, 50)
        self.assertEqual(self.poolA.total_eth, 0)
        self.assertEqual(self.poolA.total_dai, 100)
    
    def test_update_amounts_5(self):
        self.poolA.update_amounts(10, -50)
        self.assertEqual(self.poolA.total_eth, 20)
        self.assertEqual(self.poolA.total_dai, 0)

class TestSwap(unittest.TestCase):
    def setUp(self):
        self.poolA = Pool(total_eth=10, total_dai=50, swapFee=0.003)

    def test_amt_without_fee_1(self):
        self.assertAlmostEqual(self.poolA.amt_without_fee(10), 9.97, places=2)

    def test_amt_without_fee_2(self):
        self.assertAlmostEqual(self.poolA.amt_without_fee(1000), 997, places=2)

    def test_amt_swap_eth_for_dai(self):
        self.assertAlmostEqual(self.poolA.amt_swap_eth_for_dai(2), 8.33, places=2)

    def test_amt_swap_dai_for_eth(self):
        self.assertAlmostEqual(self.poolA.amt_swap_dai_for_eth(10), 1.67, places=2)

    def test_swap_eth(self):
        self.poolA.swap_token(2, 'ETH')
        self.assertAlmostEqual(self.poolA.total_eth, 12, places=2)
        self.assertAlmostEqual(self.poolA.total_dai, 41.687, places=2)

    def test_swap_dai(self):
        self.poolA.swap_token(13, 'DAI')
        self.assertAlmostEqual(self.poolA.total_eth, 7.941, places=2)
        self.assertAlmostEqual(self.poolA.total_dai, 63, places=2)

class TestArbitrageHelper(unittest.TestCase):
    def test_quadratic_1(self):
        self.assertEqual(quadratic_formula(1, -4, 0, 10 ** 6), 4)

    def test_quadratic_2(self):
        self.assertIsNone(quadratic_formula(1, 5, 6, 10 ** 6))

    def test_quadratic_3(self):
        self.assertEqual(quadratic_formula(1, -6, -7, 10 ** 6), 7)

    def test_quadratic_4(self):
        self.assertIsNone(quadratic_formula(0, 0, 0, 10 ** 6))

class TestArbitrage(unittest.TestCase):
    def setUp(self):
        self.poolA = Pool(total_eth=20, total_dai=400, swapFee=0.003)
        self.poolB = Pool(total_eth=40, total_dai=100, swapFee=0.003)
        self.poolC = Pool(total_eth=40, total_dai=800, swapFee=0.003)
        self.poolD = Pool(total_eth=40, total_dai=800.001, swapFee=0.003)

    def test_arbitrage_exists(self):
        res = arbitrage_calculation(self.poolA, self.poolB)
        self.assertAlmostEqual(res[0], 7.34, places=2)
        self.assertAlmostEqual(res[1], 13.34, places=2)

    def test_arbitrage_not_exist_1(self):
        res = arbitrage_calculation(self.poolA, self.poolC)
        self.assertIsNone(res)
    
    def test_arbitrage_not_exist_2(self):
        res = arbitrage_calculation(self.poolA, self.poolD)
        self.assertIsNone(res)

if __name__ == "__main__":
    unittest.main()
