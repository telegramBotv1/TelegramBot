import sys
from utils.ioFile import create_file_content
from utils.loopExit import exitAsyncio


class ExitCommand(Exception):
    pass

def openPositions(current_order):
    exchange_name = 'okx'
    operation = current_order['operation']

    if exchange_name == 'okx':
        path = './exchanges/okx/key.json'
    elif exchange_name == 'okx':
        path = './exchanges/mexc/key.json'
    else:
        return None

    read_content = create_file_content(path, 'apikey,secretkey,Passphrase')
    if not read_content:    
        # exitAsyncio()
        sys.exit()
        
    from exchanges.tradeManager import TradeManager
    # trade_manager.get_account_balance() # 查询账户资产情况
    switch = {
        '开多': { "side": "buy", "posSide": "long"},
        '开空': { "side": "sell", "posSide": "short"},
        '平多': { "side": "sell", "posSide": "long"},
        '平空': { "side": "buy", "posSide": "short"},
    }
    outerParam = switch.get(operation)

    current_order = {
        **current_order,
        **outerParam
    }
    trade_manager = TradeManager(exchange_name, current_order, read_content)
    trade_manager.open_position()
