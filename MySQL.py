#!encoding:utf-8
__author__ = 'wangfei'
__date__ = '2017/12/27 0027 17:32'

__metaclass__ = type

import os
import sys
import getopt
import mysql.connector
from mysql.connector import errorcode

base_dir = os.path.split(os.path.realpath(__file__))[0]
logfile = r'%s/logs/%s.log' % (base_dir, os.path.basename(__file__).split('.')[0])
cache_path = r'%s/var/%s.tmp' % (base_dir, os.path.basename(__file__).split('.')[0])
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def path_is_exist(path):
    if os.path.exists(path):
        pass
    else:
        os.makedirs(path)

class MySQL:
    my_config = {}

    def mysql_config(self, config):
        # Default config
        conf_keys = config.keys()
        if ('host' not in conf_keys):
            self.my_config['host'] = '127.0.0.1'
        else:
            self.my_config['host'] = config['host']

        if ('port' not in conf_keys):
            self.my_config['port'] = 3306
        else:
            self.my_config['port'] = int(config['port'])

        if ('user' not in conf_keys):
            self.my_config['user'] = 'root'
        else:
            self.my_config['user'] = config['user']

        if ('password' not in conf_keys):
            self.my_config['password'] = 'rootroot'
        else:
            self.my_config['password'] = config['password']

        if ('database' not in conf_keys):
            self.my_config['database'] = ''
        else:
            self.my_config['database'] = config['database']

        if ('charset' not in conf_keys):
            self.my_config['charset'] = 'utf8'
        else:
            self.my_config['charset'] = config['charset']

    def __init__(self, config):
        #mysql_status=1 up
        #mysql_status=0 down
        try:
            self.mysql_config(config)
            self.cnx = mysql.connector.connect(**self.my_config)
            self.mysql_status = int(1)
        except mysql.connector.Error as err:
            # print err
            self.mysql_status = int(0)

    def resultSet(self, sql):
        try:
            self.cursor = self.cnx.cursor()
            self.cursor.execute(sql)
            rs = self.cursor.fetchall()
        except mysql.connector.Error as err:
            return 0
        return rs

        #更新global status数据 进行新旧替换
    def update_global_status(self):
        try:
            base_dir=os.path.split(os.path.realpath(__file__))[0]
            path_is_exist("{base_dir}/var".format(base_dir=base_dir))
            self.cache_file_current = r'{base_dir}/var/global_status_current_{ip}_{port}.tmp'.format(base_dir=base_dir,ip=self.my_config['host'],port=self.my_config['port'])
            self.cache_file_past = r'{base_dir}/var/global_status_past_{ip}_{port}.tmp'.format(base_dir=base_dir,ip=self.my_config['host'],port=self.my_config['port'])
            # print self.cache_file_current ,'\n',self.cache_file_past

            status_rs = self.resultSet("show global status")
            if status_rs is None:
                None
            else:
                if os.path.isfile(self.cache_file_current):
                    os.rename(self.cache_file_current, self.cache_file_past)
                else:
                    pass
                with open(self.cache_file_current, 'w') as f:
                    for row in status_rs:
                        f.write(row[0] + "\t" + row[1] + "\n")
        except Exception as e:
            sys.exit(1)

    #更新Binlog 信息
    def update_binlog_size(self):
        try:
            self.cache_file_current = r'{base_dir}/var/binlog_size_current_{host}_{port}.tmp'.format(base_dir=base_dir,host=self.my_config['host'],port=self.my_config['port'])
            self.cache_file_past = r'{base_dir}/var/binlog_size_{host}_{port}.tmp'.format(base_dir=base_dir,host=self.my_config['host'],port=self.my_config['port'])
            master_log_rs = self.resultSet("show master logs")
            if master_log_rs is None or master_log_rs ==0 :
                None
            else:
                if os.path.isfile(self.cache_file_current):
                    os.rename(self.cache_file_current, self.cache_file_past)
                else:
                    pass
                with open(self.cache_file_current, 'w') as f:
                    # print rs
                    for row in master_log_rs:
                        f.write(str(row[0]) + "\t" + str(row[1]) + "\n")
        except Exception as e:
            sys.exit(1)

    #更新show full processlist数据"Id User Host db Command Time State Info Progress"
    def update_procsslist_cache(self):
        try:
            self.cache_file_current = r'{base_dir}/var/full_processlist_{ip}_{port}.tmp'.format(base_dir=base_dir,ip=self.my_config['host'],port=self.my_config['port'])
            process_rs = self.resultSet("show full processlist")
            if process_rs is None:
                None
            else:
                with open(self.cache_file_current, 'w') as f:
                    for row in process_rs:
                        f.write(str(row[0]) + "\t" + str(row[1]) + "\t" + str(row[2]) + "\t" + str(row[3]) + "\t" + str(row[4]) + "\t"  + str(row[5]) + "\t" + str(row[6]) + "\n")
                f.close
        except Exception as e:
            sys.exit(1)
        
    def update_slave_cache(self):
        try:
            self.cache_file_current = r'{base_dir}/var/slave_status_{ip}_{port}.tmp'.format(base_dir=base_dir,ip=self.my_config['host'],port=self.my_config['port'])
            rs = self.resultSet("show slave status")
            if rs is None:
                None
            else:
                with open(self.cache_file_current, 'w') as f:
                    for row in rs:
                        f.write(
                                "master_host " + row[1] + "\n"
                                +"Master_User " + row[2] + "\n"
                                +"Master_Port " + str(row[3]) + "\n"
                                +"Connect_Retry " + str(row[4]) + "\n"
                                +"IO_Running " + row[10] + "\n"
                                +"SQL_Running " + row[11] + "\n"
                                # +"Replicate_Ignore_DB " + row[13] + "\n"
                                # +"Replicate_Do_Table " + row[14] + "\n"
                                # +"Replicate_Ignore_Table " + row[15] + "\n"
                                # +"Replicate_Wild_Do_Table " + row[16] + "\n"
                                # +"Last_Errno " + str(row[18]) + "\n"
                                # +"Last_Error " + row[19] + "\n"
                                +"Exec_Master_Log_Pos " + str(row[21]) + "\n"
                                +"Seconds_Behind_Master " + str(row[32])
                                )
                f.close
        except Exception as e:
            sys.exit(1)

    def update_variables_cache(self):
        try:
            self.cache_file_current = r'{base_dir}/var/global_variables_{ip}_{port}.tmp'.format(base_dir=base_dir,ip=self.my_config['host'],port=self.my_config['port'])
            rs = self.resultSet("show global variables")
            if rs is None:
                None
            else:
                with open(self.cache_file_current, 'w') as f:
                    for row in rs:
                        f.write(row[0] + "\t" + row[1] + "\n")
                f.close()
        except Exception as e:
            sys.exit(1)

    def __del__(self):
        try:
            self.cursor.close()
        except AttributeError:
            pass
        try:
            self.cnx.close()
        except AttributeError:
            pass
