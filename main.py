import socks  # pysocks
from bin.index import TelethonChen
import tracemalloc
import asyncio
api_id = ''
api_hash = ''
group_id = 0000
proxy = (socks.SOCKS5, '127.0.0.1', 7890)
tracemalloc.start()
telethonchen = TelethonChen(api_id, api_hash, group_id, proxy)

if __name__ == '__main__':
    asyncio.run(telethonchen.main())