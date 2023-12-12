from colorama import Fore
from order.okx.okx import okx


def openPositionsMore(quantity):
    print(Fore.GREEN + '开多, 数量:' + str(quantity))
    
    pass

def openPositionsLess(quantity):
    print(Fore.RED + '开空, 数量:' + str(quantity))
    pass

def unwindPositionsMore(quantity):
    print(Fore.GREEN + '平多, 数量:' + str(quantity))
    pass

def unwindPositionsLess(quantity):
    print(Fore.RED + '平空, 数量:' + str(quantity))
    pass