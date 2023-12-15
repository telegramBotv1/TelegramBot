class ExchangeInterface:
    def get_account_balance(self):
        raise NotImplementedError
    
    def open_positions_more(self):
        raise NotImplementedError
    
    def set_leverage(self):
        raise NotImplementedError
