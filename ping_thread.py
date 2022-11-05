"""
    ping[threading]
"""
from concurrent.futures import ThreadPoolExecutor#
from tcping import Ping#

def ping_check(ip,port=80,timeout=3,count=5):
    try:
        ping = Ping(ip, port=port, timeout=timeout)
        ping.ping(count=count)

        ret = ping.result.rows[0]
        return float(ret.success_rate.rstrip('%')) ,\
            float(ret.average.rstrip('ms'))
    except Exception as ex:
        print(f"Ping Except {ip}:80 ex:{repr(ex)}")
        return 0,0

def multi_ping(iplist):
    # default max_workers = min(32, (os.cpu_count() or 1) + 4)
    pool = ThreadPoolExecutor() #max_workers=10 
    thlist = []
    for ip in iplist:
        th = pool.submit(ping_check,ip)
        thlist.append(th)
    
    ret = []
    for th in thlist:
        # print(th.done(), th.result())
        ret.append(th.result())
    pool.shutdown()
    
    return ret


def main():
    iplist = ['16.163.81.110','18.166.243.220','18.167.160.12']
    ret = multi_ping(iplist)
    print(ret)


if __name__ == '__main__':
    main()










