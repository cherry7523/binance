import threading
import time
import queue

import pyupbit


class Producer(threading.Thread):
    def __init__(self, q):
        super().__init__()
        self.q = q
        self.ticker = "KRW-BTC"

    def run(self):
        while True:
            price = pyupbit.get_current_price(self.ticker)
            self.q.put(price)
            time.sleep(2)

class Consumer(threading.Thread):
    def __init__(self, q):
        super().__init__()
        self.q = q

    def run(self):
        while True:
            if not self.q.empty():
     
                price_open = self.q.get()
                price_buy = price_open *1.01
                price_sell = price_open * 1.02
            
            time.sleep (0.2)
q = queue.Queue()
Producer(q).start()
Consumer(q).start()

