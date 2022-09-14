# kingpin_nslookup
根据nslookup查询域名对应ip列表 记录延时

#### 功能:
- 1 多域名支持
- 2 可添加固定ip
- 3 结果iplist转存支持: csv/sqlite/postgres
- [remove] :fearful:
    - 4 支持写/etc/host
    - 5 时间校队, 邮件通知 服务器时间与本地时间差

#### CURL test:

    curl --resolve *:443:104.16.89.20 https://cdn.jsdelivr.net/npm/bootstrap/LICENSE 


#### 使用说明
- Python>=3.7
- 依赖
    python -m pip install -r requirements.txt
- 修改config.py
    - 添加需要检测的域名
    - 配置需要输出的数据库
- 运行
    cd kingpin_nslookup/
    python run.py

