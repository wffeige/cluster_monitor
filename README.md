# cluster_monitor

使用方法:
1.wget https://bootstrap.pypa.io/get-pip.py
2.python get-pip.py
3.pip install mysql-connector-python

vim config/MySQLConfigure #添加主机信息

[node1]
host = 127.0.0.1
user = root
password = password
database = test
socket = '/var/lib/mysql/mysql.sock'
port = 3306


python mysql_status.py  #连接数据库 获取信息 flush 到本地
python get_diff.py --host=192.168.64.35 --mode=buffer_hate #获取buffer pool 的命中率
python get_current.py --host=192.168.64.35 --type=galera_status --mode=wsrep_cluster_size #获取galera集群的size
