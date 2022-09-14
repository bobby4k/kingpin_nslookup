"""
    通过 nslookup 找到域名延时最小的IP
    
"""
import time#
import asyncio
from unittest import result#

from nslookup import Nslookup#
from tcping import Ping#
import urllib3#

# from config import KP_GLOBAL_HOST_GROUP#
# from config import KP_GLOBAL_DATABASE#
from config import KP_GLOBAL_DNS#
from config_inuse import KP_GLOBAL_HOST_GROUP#
from config_inuse import KP_GLOBAL_DATABASE#

import record as kp_record#

class kp_lookup():
    
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def ns_query(domain):
        """
        根据domain返回ip list

        Args:
            domain (str): 域名

        Returns:
            list: ip list
        """
        dns_query = Nslookup(dns_servers=[KP_GLOBAL_DNS], verbose=False, tcp=False)
        ips_record = dns_query.dns_lookup(domain)
        return ips_record.answer

    @staticmethod
    def url_check(url,ip):
        hparse = urllib3.util.url.parse_url(url)
        # p.scheme, p.port, p.hostname, p.path,
        if hparse.scheme=='https':
            pool = urllib3.HTTPSConnectionPool(
                ip,
                server_hostname = hparse.hostname,
            )
        elif hparse.scheme=='http':
            pool = urllib3.HTTPConnectionPool(
                ip,
                server_hostname = hparse.hostname,
            )
        else:
            raise ValueError("check url only support http/https")
        
        try:
            res  = pool.urlopen(
                "GET",
                hparse.path,
                headers={"Host":hparse.hostname},
                assert_same_host=False,
                )
        except Exception as e:
            print(f"Error Raised: {e}")
            return 400
        
        return res.status
        # print(res.data.decode())
    #END url_check


    @staticmethod
    def ping_check(ip,port=80,timeout=1,count=2):
        ping = Ping(ip, port=port, timeout=timeout)
        ping.ping(count=count)

        ret = ping.result.rows[0]
        return float(ret.success_rate.rstrip('%')) ,\
            float(ret.average.rstrip('ms'))

    def lookup_one_domain(self,host:dict):
        iplist = host['iplist'] if host.__contains__('iplist') else []
        
        #第一步nslookup
        domains = host['subdomains']+[host['domain']] if host.__contains__('subdomains') else [host['domain']] 
        for dm in domains:
            ipl = self.ns_query(dm)
            if isinstance(ipl,list) and len(ipl)>0:
                iplist += ipl
        #去重
        iplist = list(set(iplist))

        #第二步tcpping
        kp_host_ret = []
        for ip in iplist:
            ret = self.ping_check(ip)
            if ret[0] == 100:
                kp_host_ret.append({'domain':host['domain'],'ip':ip,'delay':ret[1]})
        #排序
        kp_host_ret.sort(key=lambda x:x['delay'], reverse=False)

        #第三步 check url
        if host.__contains__('check'):
            i = 0
            for hret in kp_host_ret:
                if self.url_check(host['check'], hret['ip']) == 200:
                    hret.update({'check':1})
                    kp_host_ret[i] = hret
                    print(f"best ip:{hret}")
                    break
                i += 1
        
        return kp_host_ret
    #END lookup_one_domain

    def run(self):
        results = []
        for host in KP_GLOBAL_HOST_GROUP:
            ret = self.lookup_one_domain(host)
            results += ret
            break

        #纪律数据
        match KP_GLOBAL_DATABASE['type']:
            case 'csv':
                kp_record.record_to_csv(file=KP_GLOBAL_DATABASE['path'],data=results)
            case 'sqlite':
                pass
            case 'postgres':
                pass
            case _:
                raise ValueError(f"no support for database:{KP_GLOBAL_DATABASE['type']}")
    
#END class

def main():
    kp_lookup().run()
    


if __name__ == '__main__':
    main()

