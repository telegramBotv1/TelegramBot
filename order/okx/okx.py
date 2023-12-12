import json
# from okx import Trading, Account
import okx.Trade as Trade
import okx.Account as Account

# import okx.Account_api as Account
# import okx.Trade_api as Trade

from order.baseOrder import PerpetualContractTrader
from utils.ioFile import read_file, write_file, has_file

# OKX交易所的实现
class OKXTrader(PerpetualContractTrader):

    def __init__(self):
        path = '.key.json'
        keys = ['apikey', 'secretkey', 'Passphrase']
        if has_file(path, False):
            pass
        else:
            write_file(path, {
                "apikey": '',
                "secretkey": '',
                "Passphrase": 0
            })

        read_content = read_file(path)['message']
        read_content = json.loads(read_content)

        if all(key in read_content and read_content[key] for key in keys):
            pass
        else:
            print('请检查.config文件是否有 apikey, secretkey, Passphrase并不能为空')
            exit()

        self.apikey, self.secretkey, self.Passphrase = read_content['apikey'], read_content['secretkey'], read_content['Passphrase']

    def initialize_client(self):
        self.trading_api = Trade(self.api_key, self.api_secret, self.passphrase)
        self.account_api = Account(self.api_key, self.api_secret, self.passphrase)

    def place_order(self, size, side, leverage = 50, symbol = 'BTC-USDT-SWAP', order_type = 'market'):
        params = {
            'instId': symbol,                  # 合约名称，例如 'BTC-USDT-210924'
            'tdMode': 'isolated',              # 交易模式，逐仓：isolated, 全仓：cross
            'side': side,                      # 买卖类型，买入：buy，卖出：sell
            'leverage': str(leverage),         # 杠杆 
            'ordType': order_type,             # 订单类型，市价：market，限价：limit
            'sz': str(size),                   # 买入或卖出的数量
        }

        return self.trading_api.place_order(params=params)

    def partial_close(self, symbol, size, side, order_type, price):
        side = 'buy' if side == 'sell' else 'sell'
        return self.place_order(
            symbol=symbol,
            size=size,
            side=side,
            order_type='market' if price is None else 'limit',
            price=price
        )

    def get_open_positions(self, symbol):
       return self.account_api.get_positions()
    
    def main(self):
        okx_trader = OKXTrader(self.apikey, self.secretkey, self.Passphrase) # 创建实例
        okx_trader.initialize_client()
    





