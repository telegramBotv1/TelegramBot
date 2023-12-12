import socks  # pysocks
import tracemalloc
import asyncio
import json
from bin.index import TelethonChen
from utils.ioFile import read_file, write_file, has_file

path = './config/.config.json'
keys = ['api_id', 'api_hash', 'group_id']

if has_file(path, False):
    pass
else:
    write_file(path, {
        "api_id": '',
        "api_hash": '',
        "group_id": 0
    })

read_content = read_file(path)['message']
read_content = json.loads(read_content)

if all(key in read_content and read_content[key] for key in keys):
    pass
else:
    print('请检查.config文件是否有 api_id, api_hash, group_id并不能为空')
    exit()

print(read_content)

api_id, api_hash, group_id = read_content['api_id'], read_content['api_hash'], read_content['group_id']

proxy = (socks.SOCKS5, '127.0.0.1', 7890)
tracemalloc.start()
telethonchen = TelethonChen(api_id, api_hash, group_id, proxy)

if __name__ == '__main__':
    asyncio.run(telethonchen.main())