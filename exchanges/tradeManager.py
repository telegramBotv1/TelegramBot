from exchanges.okx.okx import OKXExchange
# from exchanges.mexc.mexc import MEXCExchange
import global_const

class TradeManager:
    def __init__(self, exchange_name):
        self._exchange_config = None
        self._exchange_name = exchange_name
        self._apikey = None
        self._secretkey = None
        self._passphrase = None
        self._exchanges = None
        self._exchange = None

    def set_exchange_config(self, exchange_config):
        self._exchange_config = exchange_config
        self._apikey = exchange_config['apikey']
        self._secretkey = exchange_config['secretkey']
        self._passphrase = exchange_config['Passphrase']

    def set_exchanges(self):
        self._exchanges = {
            "okx": OKXExchange(self._apikey, self._secretkey, self._passphrase)
            # "mexc": MEXCExchange('your_api_key_mexc', 'your_api_secret_mexc')
        }
        self._exchange = self._exchanges.get(self._exchange_name)

    def get_account_balance(self):
        account_balance = self._exchange.get_account_balance()
        print(account_balance)

    #  开单方法
    def open_position(self, current_order):
        current_flag = global_const.get_value('flag')
        margin = current_flag == '1' if float(current_order['quantity']) * 10 else float(current_order['quantity'])
        mgnMode = "cross" # cross 全仓 # isolated 逐仓

        parameters = {
            "instId": current_order['market'],
            "tdMode": mgnMode, 
            "side": current_order['side'],
            "posSide": current_order['posSide'],
            "ordType": "market",
            "sz": margin
        }

        leverage = {
            "instId": current_order['market'],
            "mgnMode": mgnMode,
            "lever": "100"
        }
        # "posSide": current_order['posSide'],
        
        # 设置杠杆倍数
        self._exchange.set_leverage(leverage)
        # 开单
        self._exchange.place_order(parameters)
        