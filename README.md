# cluster_monitor

使用方法:
1.wget https://bootstrap.pypa.io/get-pip.py "\n"
2.python get-pip.py "\n"
3.pip install mysql-connector-python "\n"

vim config/MySQLConfigure #添加主机信息 "\n"

[node1] "\n"
host = 127.0.0.1 "\n"
user = root "\n"
password = password "\n"
database = test "\n"
socket = '/var/lib/mysql/mysql.sock' "\n"
port = 3306 "\n"


python mysql_status.py  #连接数据库 获取信息 flush 到本地 "\n"
python get_diff.py --host=192.168.64.35 --mode=buffer_hate #获取buffer pool 的命中率 "\n"
python get_current.py --host=192.168.64.35 --type=galera_status --mode=wsrep_cluster_size #获取galera集群的size "\n"