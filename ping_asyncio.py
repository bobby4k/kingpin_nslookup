"""
    ping[asyncio]
"""
import asyncio#
from tcping import Ping#

async def ping_check(ip,port=80,timeout=1,count=5):
    ping = Ping(ip, port=port, timeout=timeout)
    ping.ping(count=count)

    ret = ping.result.rows[0]
    return float(ret.success_rate.rstrip('%')) ,\
        float(ret.average.rstrip('ms'))

async def multi_ping(iplist):
    F = [ping_check(ip) for ip in iplist]
    ret = await asyncio.gather(*F)
    return ret


async def main():
    iplist = ['16.163.81.110','18.166.243.220','18.167.160.12']
    ret = await multi_ping(iplist)
    print(ret)


if __name__ == '__main__':
    asyncio.run(main())










