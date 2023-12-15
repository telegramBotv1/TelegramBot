import okx.Account as Account
import okx.Trade as Trade

from exchanges.exchangeInterface import ExchangeInterface

class OKXExchange(ExchangeInterface):
    def __init__(self, api_key, api_secret, passphrase):
        flag = "1"  # 真实交易 0 模拟交易 1
        self.accountAPI = Account.AccountAPI(api_key, api_secret, passphrase, False, flag, debug=False)
        self.TradeAPI = Trade.TradeAPI(api_key, api_secret, passphrase, False, flag, debug=False)
        
    def get_account_balance(self):
        result = self.accountAPI.get_account_balance()
        return result
    
    def set_leverage(self, parameters):
        result = self.accountAPI.set_leverage(**parameters)
        if result["code"] == '0':
            for item in result['data']:
                print("\n" + '杠杆设置成功,信息如下')
                print('instId: ' + item['instId'])
                print('lever: ' + item['lever'])
                print('mgnMode: ' + item['mgnMode'])
                print('posSide: ' + item['posSide'])
                print('=======================')
        else:
            print(result)
    
    def place_order(self, parameters):
        order_result = self.TradeAPI.place_order(**parameters)
        if order_result['code'] == '0':
            print('开单成功')
            order_id = order_result['data'][0]['ordId']
            #去调用订单信息接口获取当前订单信息
            if order_id:
                self.get_order(parameters['instId'], order_id)
        else:
            print(order_result)


    def get_order(self, instId, ordId):
        order_result = self.TradeAPI.get_order(instId, ordId)    
        print(order_result)

