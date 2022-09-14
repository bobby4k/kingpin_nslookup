"""
    配置域名及ip
    
"""

#数据保存地址
#type: csv, sqlite, postgresql
KP_GLOBAL_DATABASE = {
    'type':'csv',
    'path':'hosts.csv',

    # 'type':'sqlite',
    # 'path':'hosts.sqlite3',

    # 'type':'postgres',
    # 'dsn':"host=localhost dbname=test user=postgres password=pg123",
}

#DNS server
KP_GLOBAL_DNS = '8.8.8.8'
#检查多少个ip可用性,0表示全部
KP_GLOBAL_CHECKIP_NUM = 3
#是否允许ping丢包, 默认100不允许丢包
#   比如: 90表示 允许成功90%即可接受此IP
KP_GLOBAL_PING_SUCC_RATE = 100

#需要监控分析的域名及地址
KP_GLOBAL_HOST_GROUP = [
    
    {
        #主域名 与check中的域名保持一致
        'domain':'cdn.jsdelivr.net',
        #可传入固定IP, 以免domain分析的ip都不可用
        'iplist':[
            '104.16.89.20',  # CloudFlare
            '151.101.2.109',  # Fas
            ],
        #支持多个域名, 
        'subdomains':[
            'cdn.jsdelivr.net',
        ],
        #取延时最小的IP, 检查访问是否正常
        'check':'https://cdn.jsdelivr.net/npm/bootstrap/LICENSE',
    },
]
#END GROUP

