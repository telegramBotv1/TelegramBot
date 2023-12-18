from telethon import TelegramClient, events
from exchanges.tradeManager import TradeManager
import json

from utils.ioFile import read_file, write_file, has_file
from utils.time import formatTiem
from utils.matchStr import matchStr
import global_const


class telethon_client:
    def __init__(self, api_id, api_hash, group_id, proxy):
        self._api_id = api_id
        self._api_hash = api_hash
        self._group_id = group_id
        self._proxy = proxy
        self._telegram_client = TelegramClient('session_name', self._api_id, self._api_hash, proxy = self._proxy)
        self.exchange_name = 'okx'
        self.trade_manager = TradeManager(self.exchange_name)


    # 获取所有的消息名称以及id
    async def get_my_dialogsList(self, save = False):
        dialogList = []
        async for dialog in self._telegram_client.iter_dialogs():
            dialogList.append({
                'dialogName': dialog.name,
                'dialogId': dialog.id
            })

        if(save):
            path = './config/dialogList.json'
            if has_file(path, True):
                write_file(path, dialogList)

        return dialogList

    # 启动服务
    async def start_client(self):
        print('telegram服务启动')
        await self._telegram_client.start()

    # 监听消息
    def storage_messages(self, handleMessage): 
        print('监听到! 正在处理')
        matchJSON = matchStr(handleMessage.message)
        message_id = handleMessage.id
        # message_text = handleMessage.message
        current_time = formatTiem(mode='%Y-%m-%d')
        # 读数据 解析出当天的 然后添加
        path = './config/orderInfo.json'
        if has_file(path, True):
            read_content = read_file(path)
            message = read_content["message"] or "{}"
            read_content = json.loads(message) or {}

        currentInfo = {
            "message_id": message_id,
            # "message_text": message_text,
            **matchJSON
        }

        if current_time in read_content:
            pass
        else: 
            read_content[current_time] = []
        
        read_content[current_time].append(currentInfo)
        write_file(path, read_content)

        return currentInfo

    # 获取群聊消息
    async def watch_chats(self,group_entity):
        print('正在监听……')
        @self._telegram_client.on(events.NewMessage(chats=group_entity))
        async def handle_new_message(event):
            try:
                current_order = self.storage_messages(event.message)
            except BaseException as error:
                current_order = False
                print('解析文本错误')

            if current_order:
                self.exchange_interface(current_order)
    
    def exchange_interface(self, current_order):
        operation = current_order['operation']
        switch = {
            '开多': { 'side': 'buy', 'posSide': 'long'},
            '开空': { 'side': 'sell', 'posSide': 'short'},
            '平多': { 'side': 'sell', 'posSide': 'long'},
            '平空': { 'side': 'buy', 'posSide': 'short'},
        }
        outerParam = switch.get(operation)
        current_order = {
            **current_order,
            **outerParam
        }

        self.trade_manager.open_position(current_order)


    # 配置开单实例的一些参数 
    def set_exchange_config(self):
        exchange_config_center = read_file('./exchanges/' + self.exchange_name + '/key.json')
        exchange_config_center = json.loads(exchange_config_center["message"])
        self.trade_manager.set_exchange_config(exchange_config_center)
        self.trade_manager.set_exchanges()


    async def run(self, exchange_name):
        self.exchange_name = exchange_name
        global_const._init()
        global_const.set_value('flag', "1") # 真实交易 0 模拟交易 1 使用字符串

        await self.start_client()
        await self.get_my_dialogsList(True)
        group_entity = await self._telegram_client.get_entity(self._group_id)
        await self.watch_chats(group_entity) 
        self.set_exchange_config()
        await self._telegram_client.run_until_disconnected()