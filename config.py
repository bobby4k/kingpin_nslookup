"""
    配置域名及ip
    
"""

#数据保存地址
#type: csv, sqlite, postgresql
KP_GLOBAL_DATABASE = {
    'type':'csv',
    'path':'hosts.csv',
    # 'type':'sqlite',
    # 'path':'sqlite.db',
    # 'type':'postgres',
    # 'dsn':'',
}

#DNS server
KP_GLOBAL_DNS = '8.8.8.8'

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
        'check':'https://{domain}/npm/bootstrap/LICENSE',
    },
]
#END GROUP

