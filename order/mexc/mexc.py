from order.baseOrder import PerpetualContractTrader

class MXCTrader(PerpetualContractTrader):
    def initialize_client(self):
        # 初始化抹茶的API客户端
        pass

    def place_order(self, symbol, size, side, order_type, price):
        # 下单逻辑
        pass

    def partial_close(self, symbol, size, side, order_type, price):
        # 部分平仓逻辑
        pass

    def get_open_positions(self, symbol):
        # 获取当前开放的仓位
        pass
