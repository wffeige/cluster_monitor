#!encoding:utf-8
__author__ = 'wangfei'
__date__ = '2017/12/27 0027 17:32'

#Function:自动读取配置文件 更新所有主机的参数信息


import os
import sys
import json
import getopt
from MySQL import MySQL
import ConfigParser

base_dir = os.path.split(os.path.realpath(__file__))[0]
configure_file = '%s/config/MySQLConfigure' % base_dir

def usage():
    print "Usage: %s {OPTIONS...}" % sys.argv[0]
    print "-h|--help  print help message"
    print "MySQL DSN:"
    print "  --host, --port, --user, --password, --database, --charset"
    print

def get_info_dict(opt):
    '''
    从configure_file中读取MySQL的连接配置文件，返回dict
    '''
    cf = ConfigParser.ConfigParser()
    cf.read(configure_file)
    kvs = cf.items(opt)
    if kvs:
        return dict(kvs)
    else:
        return 0

'''
自动读取配置文件 进行更新
'''
def auto_check():
    cf = ConfigParser.ConfigParser()
    cf.read(configure_file)
    host_lst =  cf.sections()

    for host in host_lst:
        section = get_info_dict(host)
        myconf_dict =  section
        mysql = MySQL(myconf_dict)
        v = mysql.mysql_status
        if (v == 1):
            mysql.update_global_status()
            mysql.update_procsslist_cache()
            mysql.update_slave_cache()
            mysql.update_variables_cache()
            mysql.update_binlog_size()
    return 1

# def auto_check():
#     cf = ConfigParser.ConfigParser()
#     cf.read(configure_file)
#     # host_lst =  cf.sections()
#
#     host_lst =  ["control"]
#
#     for host in host_lst:
#         section = get_info_dict(host)
#         myconf_dict =  section
#         mysql = MySQL(myconf_dict)
#         v = mysql.mysql_status
#         if (v == 1):
#             mysql.update_binlog_size()

'''
手动传参进行更行
'''
def manual_check():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hn:", ["help", "host=", "port=", "user=", "password=", "database=", "charset="] )
    except getopt.GetoptError, err:
        usage()
        sys.exit(2)
    myconf_dict = {}
    for o, a in opts:
        if o in ("--help"):
            usage()
            sys.exit()
        elif o in ("--host","-h"):
            myconf_dict['host'] = a
        elif o in ("--port","-P"):
            myconf_dict['port'] = a
        elif o in ("--user","-u"):
            myconf_dict['user'] = a
        elif o in ("--password","-p"):
            myconf_dict['password'] = a
        elif o in ("--database"):
            myconf_dict['database'] = a
        elif o in ("--charset"):
            myconf_dict['charset'] = a
    mysql = MySQL(myconf_dict)

    v = mysql.mysql_status
    if (v == 1):
        mysql.update_global_status()
        mysql.update_procsslist_cache()
        mysql.update_slave_cache()
        mysql.update_variables_cache()
        mysql.update_binlog_size()
    print v
    del mysql

def main():
    # manual_check()
    print auto_check()

if __name__ == "__main__":
    main()
