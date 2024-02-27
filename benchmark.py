from Pool import Pool
import time
import threading
from main import swap_fee
from main import arbitrage_calculation

arbitrage_running: bool = True
iteration_count: int = 1000000

def arbitrage_non_blocking(pool1: Pool, pool2: Pool):
    while arbitrage_running:
        result = arbitrage_calculation(pool1, pool2)
    
def run_swap_non_blocking(pool1: Pool, pool2: Pool):
    counter = iteration_count
    while counter > 0:
        counter -= 1
        pool2.swap_token(0.5, 'ETH')
    global arbitrage_running
    arbitrage_running = False

def run_swap_blocking(pool1: Pool, pool2: Pool):
    counter = iteration_count
    while counter > 0:
        counter -= 1
        pool2.swap_token(0.5, 'ETH')
        result = arbitrage_calculation(pool1, pool2)

if __name__ == '__main__':

    # init
    poolA = Pool(total_eth=4000, total_dai=20000, swapFee=swap_fee)
    poolD = Pool(total_eth=8000, total_dai=400000, swapFee=swap_fee)

    ''' start non-blocking code '''
    
    start = time.perf_counter()

    t1 = threading.Thread(target=run_swap_non_blocking, args=(poolA, poolD))
    t2 = threading.Thread(target=arbitrage_non_blocking, args=(poolA, poolD))

    t2.start()
    t1.start()

    t1.join()
    t2.join()

    finish = time.perf_counter()
    print(f"Finished running non-blocking in {round(finish-start, 2)} second(s)")
    
    ''' end non-blocking code '''


    ''' start blocking code '''
    start = time.perf_counter()

    run_swap_blocking(poolA, poolD)

    finish = time.perf_counter()
    print(f"Finished running blocking code in {round(finish-start, 2)} second(s)")
    
    ''' end blocking code '''

    ''' 

    Sample results from running on my machine:
    1000000 iterations
    >> Finished running non-blocking in 0.18 second(s)
    >> Finished running blocking code in 0.23 second(s)

    10000000 iterations
    >> Finished running non-blocking in 1.67 second(s)
    >> Finished running blocking code in 2.34 second(s)
    
    '''