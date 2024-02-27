from enum import Enum

class Token(Enum):
    ETH = 'ETH'
    DAI = 'DAI'

class Pool():
    def __init__(self, total_eth: float, total_dai: float, swapFee: float):
        self.total_eth = total_eth
        self.total_dai = total_dai
        self.swapFee = swapFee

    def get_amt_eth(self) -> float:
        return self.total_eth
    
    def get_amt_dai(self) -> float:
        return self.total_dai
    
    def get_k(self) -> float:
        return self.total_eth * self.total_dai
    
    def get_swap_fee(self) -> float:
        return self.swapFee
    
    ''' swap methods '''
    def amt_without_fee(self, amt_token: float) -> float:
        return amt_token * (1 - self.get_swap_fee())
    
    def amt_swap_eth_for_dai(self, amt_eth_swap: float) -> float:
        amt_dai_swap = self.get_amt_dai() - (self.get_k() / (self.get_amt_eth() + amt_eth_swap))
        return abs(amt_dai_swap)
    
    def amt_swap_dai_for_eth(self, amt_dai_swap: float) -> float:
        amt_eth_swap = self.get_amt_eth() - (self.get_k() / (self.get_amt_dai() + amt_dai_swap))
        return abs(amt_eth_swap)
    
    def execute_swap_eth(self, amt_eth_swap: float, amt_dai_swap: float) -> 'Pool':
        self.update_amounts(amtEth=amt_eth_swap, amtDai=amt_dai_swap)
        return self
    
    def execute_swap_dai(self, amt_dai_swap: float, amt_eth_swap: float) -> 'Pool':
        self.update_amounts(amtEth=amt_eth_swap, amtDai=amt_dai_swap)
        return self
    
    def swap_token(self, amt_token: float, token_name: Token) -> 'Pool':
        if amt_token <= 0:
            return None
        if token_name == Token.ETH.value:
            amt_eth_swap = amt_token
            amt_eth_swap_without_fee = self.amt_without_fee(amt_eth_swap)
            amt_dai_swap = - self.amt_swap_eth_for_dai(amt_eth_swap_without_fee)
            return self.execute_swap_eth(amt_eth_swap=amt_eth_swap, amt_dai_swap=amt_dai_swap)
        else:
            amt_dai_swap = amt_token
            amt_dai_swap_without_fee = self.amt_without_fee(amt_dai_swap)
            amt_eth_swap = - self.amt_swap_dai_for_eth(amt_dai_swap_without_fee)
            return self.execute_swap_dai(amt_dai_swap=amt_dai_swap, amt_eth_swap=amt_eth_swap)
    
    ''' add liquidity methods '''
    def add_liquidity_eth(self, amt_eth: float) -> 'Pool':
        amt_dai = (self.get_amt_dai() / self.get_amt_eth()) * amt_eth
        self.update_amounts(amtEth=amt_eth, amtDai=amt_dai)
        return self
    
    def add_liquidity_dai(self, amt_dai: float) -> 'Pool':
        amt_eth = (self.get_amt_eth() / self.get_amt_dai()) * amt_dai
        self.update_amounts(amtEth=amt_eth, amtDai=amt_dai)
        return self
    
    def add_liquidity(self, amt_token: float, token_name: Token) -> 'Pool':
        if amt_token <= 0:
            return None
        if token_name == Token.ETH.value:
            return self.add_liquidity_eth(amt_token)
        else:
            return self.add_liquidity_dai(amt_token)

    ''' remove liquidity methods '''
    def remove_liquidity_eth(self, amt_eth: float) -> 'Pool':
        amt_dai = (self.get_amt_dai() / self.get_amt_eth()) * amt_eth
        self.update_amounts(amtEth=-amt_eth, amtDai=-amt_dai)
        return self
    
    def remove_liquidity_dai(self, amt_dai: float) -> 'Pool':
        amt_eth = (self.get_amt_eth() / self.get_amt_dai()) * amt_dai
        self.update_amounts(amtEth=-amt_eth, amtDai=-amt_dai)
        return self
    
    def remove_liquidity(self, amt_token: float, token_name: Token) -> 'Pool':
        if amt_token <= 0:
            return None
        if token_name == Token.ETH.value:
            if amt_token > self.get_amt_eth():
                return None
            return self.remove_liquidity_eth(amt_token)
        else:
            if amt_token > self.get_amt_dai():
                return None
            return self.remove_liquidity_dai(amt_token)
        
    ''' arbitrage methods '''
    def price_ratio(self):
        return self.get_amt_dai() / self.get_amt_eth()

    def update_amounts(self, amtEth: float, amtDai: float) -> None:
        self.total_eth = self.total_eth + amtEth
        self.total_dai = self.total_dai + amtDai

    def __str__(self):
        return f"{Token.ETH.value}: {self.get_amt_eth()}, {Token.DAI.value}: {self.get_amt_dai()}, K: {self.get_k()}"
