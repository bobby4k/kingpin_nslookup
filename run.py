"""
    通过 nslookup 找到域名延时最小的IP
    
"""
import time#
import re#
import platform#

from nslookup import Nslookup#
from tcping import Ping#
import urllib3#

# from config_inuse import KP_GLOBAL_REPLACE_HOSTS,KP_GLOBAL_HOST_GROUP,KP_GLOBAL_DATABASE, \
from config import KP_GLOBAL_REPLACE_HOSTS,KP_GLOBAL_HOST_GROUP,KP_GLOBAL_DATABASE, \
    KP_GLOBAL_DNS, KP_GLOBAL_CHECKIP_NUM, KP_GLOBAL_PING_SUCC_RATE#

from ping_thread import multi_ping#
import record as kp_record#

class kp_lookup():
    need_replace = False
    _hosts_filepath = ''
    _hosts_list = {}  ##host 第一个ip
    
    def __init__(self) -> None:
        ##判断操作系统
        self.need_replace = KP_GLOBAL_REPLACE_HOSTS['replace'] if KP_GLOBAL_REPLACE_HOSTS.__contains__('replace') else False
        
        if self.need_replace is False:
            return
        
        if KP_GLOBAL_REPLACE_HOSTS.__contains__('filepath'):
            self._hosts_filepath = KP_GLOBAL_REPLACE_HOSTS['filepath']
            return
        
        syst = platform.system()
        if 'Linux'==syst:
            self._hosts_filepath = '/etc/hosts'
        elif 'Windows'==syst:
            self._hosts_filepath = 'c:\Windows\System32\drivers\etc\hosts'
        else:
            print(f"unkown system: {syst}")
            exit(4000)
    #END init
    
    @staticmethod
    def ns_query(domain):
        """
        根据domain返回ip list

        Args:
            domain (str): 域名

        Returns:
            list: ip list
        """
        dnslist = KP_GLOBAL_DNS if isinstance(KP_GLOBAL_DNS,list) else [KP_GLOBAL_DNS]
        iplist = []
        for dns in dnslist:
            try:
                dns_query = Nslookup(dns_servers=[dns], verbose=False, tcp=False)
                ips_record = dns_query.dns_lookup(domain)
                if len(ips_record.answer)>0:
                    iplist += ips_record.answer
            except Exception as ex:
                print(f"Except dns:{dns} domain:{domain} Ex:{repr(ex)}")
        return iplist
    #END ns_query

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
                timeout=2,
                )
        except Exception as e:
            print(f"{hparse.hostname} Error Raised: {e}")
            return 400
        
        return res.status
        # print(res.data.decode())
    #END url_check


    @staticmethod
    def ping_check(ip,port=80,timeout=1,count=5):
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
        # for ip in iplist:
        #     ret = self.ping_check(ip)
        #     if ret[0] >= KP_GLOBAL_PING_SUCC_RATE:
        #         kp_host_ret.append({'domain':host['domain'],'ip':ip,'delay':ret[1]})

        #多线程优化
        ping_ret = multi_ping(iplist)
        
        i = 0
        for ip in iplist:
            ret = ping_ret[i]
            if ret[0] >= KP_GLOBAL_PING_SUCC_RATE:
                kp_host_ret.append({'domain':host['domain'],'ip':ip,'delay':ret[1]})
            i += 1

        #排序
        kp_host_ret.sort(key=lambda x:x['delay'], reverse=False)

        #第三步 check url
        if host.__contains__('check'):
            i = 0
            j = KP_GLOBAL_CHECKIP_NUM if KP_GLOBAL_CHECKIP_NUM>0 else 100

            for hret in kp_host_ret:
                if self.url_check(host['check'], hret['ip']) == 200:
                    hret.update({'check':1})
                    kp_host_ret[i] = hret
                    print(f"best ip[{i}]:{hret}")
                    j -= 1
                    if j==0:
                        break
                #END if
                i += 1
        
        return kp_host_ret
    #END lookup_one_domain

    def run(self):
        results = []
        for host in KP_GLOBAL_HOST_GROUP:
            ret = self.lookup_one_domain(host)
            if len(ret)==0:
                print(f"{host['domain']}: None ip available!")
            else:
                #记录第一个ip
                self._hosts_list[host['domain']] = ret[0]
                for v in ret:
                    ##如果有check的 则重新纪律
                    if v.__contains__('check') and 1==v['check']:
                        self._hosts_list[host['domain']] = v
                        break

                results += ret
            # break #TEST
        
        if len(results)==0:
            print("None ip available!")
            return

        #记录数据
        kpath = KP_GLOBAL_DATABASE['dsn'] if KP_GLOBAL_DATABASE.__contains__('dsn') else KP_GLOBAL_DATABASE['path']
        match KP_GLOBAL_DATABASE['type']:
            case 'csv':
                total_changes = kp_record.record_to_csv(file=kpath,data=results)
            case 'sqlite':
                total_changes = kp_record.record_to_sqlite(file=kpath,data=results)
            case 'postgres':
                total_changes = kp_record.record_to_postgres(dsn=kpath,data=results)
            case _:
                raise ValueError(f"no support for database:{KP_GLOBAL_DATABASE['type']}")

        print(f"results[{total_changes}] write to {KP_GLOBAL_DATABASE['type']}: {re.sub(r'password=.+','passwd=***',kpath)}")
    #END run
    
    def replace(self):
        filepath = self._hosts_filepath
        hlist = self._hosts_list
        
        for host in KP_GLOBAL_HOST_GROUP:
            if not hlist.__contains__(host['domain']):
                continue
            
            ip = hlist[host['domain']]['ip']
            domains = host['subdomains']+[host['domain']] if host.__contains__('subdomains') else [host['domain']] 
            if len(ip)<4 or len(domains)==0:
                continue
            cc = kp_record.fuzzy_replace_hosts(filepath, domains, ip)
            print(f"\n>>>replace hosts ip:{ip} delay:{hlist[host['domain']]['delay']}ms domains:{domains} rec:{cc}")
    
#END class

def main():
    obj = kp_lookup()
    #拿到iplist 并记录
    obj.run()
    #修改hosts文件
    if obj.need_replace:
        obj.replace()


if __name__ == '__main__':
    main()

