import socks  # pysocks
import tracemalloc
import asyncio

from bin.index import TelethonChen
from utils.ioFile import create_file_content


path = './config/.config.json'
read_content = create_file_content(path, 'api_id,api_hash,group_id')
api_id, api_hash, group_id = read_content['api_id'], read_content['api_hash'], read_content['group_id']

proxy = (socks.SOCKS5, '127.0.0.1', 7890)
tracemalloc.start()
telethonchen = TelethonChen(api_id, api_hash, group_id, proxy)


if __name__ == '__main__':
    asyncio.run(telethonchen.main())