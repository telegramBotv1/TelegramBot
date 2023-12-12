from abc import ABC, abstractmethod

# 定义基类
class PerpetualContractTrader(ABC):

    def __init__(self, api_key, api_secret, passphrase, orderJson):
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase
        self.client = None
        
    @abstractmethod
    def initialize_client(self):
        pass

    @abstractmethod
    def place_order(self, symbol, size, side, order_type, price):
        pass

    @abstractmethod
    def partial_close(self, symbol, size, side, order_type, price):
        pass

    @abstractmethod
    def get_open_positions(self, symbol):
        pass


