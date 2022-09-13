# kingpin_nslookup
根据nslookup查询域名对应ip 选择延时最小的那个

				- 1 域名可是 静态cdn
				- 2 可添加固定ip
				- 3 信息存sqlite
4 支持写/etc/host



curl --resolve www.okx.com:443:13.35.125.81 https://www.okx.com/api/v5/public/time
curl --resolve *:443:13.35.125.81 https://www.okx.com/api/v5/public/time



域名1：
(base) tyrion@LD-Z2G:~$ nslookup okx.com
Server:         172.30.240.1
Address:        172.30.240.1#53

Non-authoritative answer:
Name:   okx.com
Address: 16.163.81.110
Name:   okx.com
Address: 16.163.169.1
Name:   okx.com
Address: 18.162.84.94
Name:   okx.com
Address: 18.166.243.220
Name:   okx.com
Address: 16.162.228.228
Name:   okx.com
Address: 18.162.184.7
Name:   okx.com
Address: 18.167.160.12
Name:   okx.com
Address: 16.163.225.163



nslookup okex.me
Server:         172.30.240.1
Address:        172.30.240.1#53

Non-authoritative answer:
Name:   okex.me
Address: 118.193.240.41
Name:   okex.me
Address: 2001::1f0d:5805


nslookup www.okex.me
Server:         172.30.240.1
Address:        172.30.240.1#53

Non-authoritative answer:
Name:   www.okex.me
Address: 75.126.164.178
Name:   www.okex.me
Address: 2001::c710:9e10


nslookup www.okex.com
Server:         172.30.240.1
Address:        172.30.240.1#53

Non-authoritative answer:
Name:   www.okex.com
Address: ::


nslookup static.okx.com
Server:         172.30.240.1
Address:        172.30.240.1#53

Non-authoritative answer:
static.okx.com  canonical name = dfccd2aelcoyz.cloudfront.net.
Name:   dfccd2aelcoyz.cloudfront.net
Address: 13.35.125.17
Name:   dfccd2aelcoyz.cloudfront.net
Address: 13.35.125.43
Name:   dfccd2aelcoyz.cloudfront.net
Address: 13.35.125.92
Name:   dfccd2aelcoyz.cloudfront.net
Address: 13.35.125.81
Name:   dfccd2aelcoyz.cloudfront.net
Address: 2600:9000:21c4:6000:1e:9215:9ac0:93a1
Name:   dfccd2aelcoyz.cloudfront.net
Address: 2600:9000:21c4:d200:1e:9215:9ac0:93a1
Name:   dfccd2aelcoyz.cloudfront.net
Address: 2600:9000:21c4:5400:1e:9215:9ac0:93a1
Name:   dfccd2aelcoyz.cloudfront.net
Address: 2600:9000:21c4:3600:1e:9215:9ac0:93a1
Name:   dfccd2aelcoyz.cloudfront.net
Address: 2600:9000:21c4:fa00:1e:9215:9ac0:93a1
Name:   dfccd2aelcoyz.cloudfront.net
Address: 2600:9000:21c4:b400:1e:9215:9ac0:93a1
Name:   dfccd2aelcoyz.cloudfront.net
Address: 2600:9000:21c4:6400:1e:9215:9ac0:93a1
Name:   dfccd2aelcoyz.cloudfront.net
Address: 2600:9000:21c4:1400:1e:9215:9ac0:93a1




