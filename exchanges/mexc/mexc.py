from ..exchangeInterface import ExchangeInterface

class MEXCExchange(ExchangeInterface):
    def __init__(self, api_key, api_secret):
        # initialize MEXC API
        pass
        
    def create_order(self, symbol, qty, price, side):
        print(f"Creating order on MEXC: {side} {qty} of {symbol} at {price}")
        # Implement order creation using MEXC API
        # ...

        return True