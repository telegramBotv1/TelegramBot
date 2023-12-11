from telethon import TelegramClient, events
import tracemalloc
import json

from utils.ioFile import read_file, write_file, has_file
from utils.time import formatTiem
from utils.matchStr import matchStr

class TelethonChen:
    def __init__(self, api_id, api_hash, group_id, proxy):
        self._api_id = api_id
        self._api_hash = api_hash
        self._group_id = group_id
        self._proxy = proxy
        self._client = None
    
    # 创建实例
    def createClient(self): 
        self._client = TelegramClient('session_name', self._api_id, self._api_hash, proxy = self._proxy)

    # 获取所有的消息名称以及id
    async def getMyDialogsList(self, save = False):
        dialogList = []
        async for dialog in self._client.iter_dialogs():
            dialogList.append({
                'dialogName': dialog.name,
                'dialogId': dialog.id
            })
        path = './env/dialogList.json'
        if has_file(path, True):
            write_file(path, dialogList)

        return dialogList

    # 启动服务
    async def startClient(self):
        await self._client.start()

    def storageMessages(self, handleMessage): 
        matchJSON = matchStr(handleMessage.message)

        message_id = handleMessage.id
        message_text = handleMessage.message
        current_time = formatTiem(mode='%Y-%m-%d')
        # 读数据 解析出当天的 然后添加
        path = './env/orderInfo.json'
        if has_file(path, True):
            read_content = read_file(path)
            message = read_content["message"] or "{}"
            read_content = json.loads(message) or {}

        currentInfo = {
            "message_id": message_id,
            "message_text": message_text,
            **matchJSON
        }

        if current_time in read_content:
            pass
        else: 
            read_content[current_time] = []
        
        read_content[current_time].append(currentInfo)
        write_file(path, read_content)

    # 获取群聊消息
    async def watchChats(self,group_entity):
        print('开启监听！')
        @self._client.on(events.NewMessage(chats=group_entity))
        async def handle_new_message(event):
            self.storageMessages(event.message)

    async def main(self):
        tracemalloc.start()
        self.createClient()
        await self.startClient()
        await self.getMyDialogsList(True)
        group_entity = await self._client.get_entity(self._group_id)
        await self.watchChats(group_entity) 
        await self._client.run_until_disconnected()

