from exchanges.okx.okx import OKXExchange
# from exchanges.mexc.mexc import MEXCExchange

class TradeManager:
    def __init__(self, exchange_name, current_order, read_content):
        self.read_content = read_content
        
        self._apikey = self.read_content['apikey']
        self._secretkey = self.read_content['secretkey']
        self._Passphrase = self.read_content['Passphrase']
        
        self.exchanges = {
            "okx": OKXExchange(self._apikey, self._secretkey, self._Passphrase)
            # "mexc": MEXCExchange('your_api_key_mexc', 'your_api_secret_mexc')
        }

        self.exchange = self.exchanges.get(exchange_name)
        self.current_order = current_order
    
    def get_account_balance(self):
        account_balance = self.exchange.get_account_balance()
        print(account_balance)

    def open_position(self):
        margin = float(self.current_order['quantity'])
        mgnMode = "cross" # cross 全仓 # isolated 逐仓
        parameters = {
            "instId": self.current_order['market'],
            "tdMode": mgnMode, 
            "side": self.current_order['side'],
            "posSide": self.current_order['posSide'],
            "ordType": "market",
            "sz": margin * 10
        }

        leverage = {
            "instId": self.current_order['market'],
            "mgnMode": mgnMode,
            "lever": "100"
        }
        # "posSide": self.current_order['posSide'],
        
        self.exchange.set_leverage(leverage)
        self.exchange.place_order(parameters)
        