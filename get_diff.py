#!encoding:utf-8
__author__ = 'wangfei'
__date__ = '2017/12/27 0027 17:32'

import sys
import getopt
import os

'''
usage:python *.py --port=3306 --mode=tps
mode可以传入自定义参数[tps、qps、buffer_hit],或者mysql的global status参数
'''

def usage():
    print "Usage: %s {OPTIONS...}" % sys.argv[0]
    print "-h|--help  print help message"
    print "MySQL DSN:"
    print "  --host, --port, --mode"
    print "  --host   Query the host of mysql server that you configured in config "
    print "  --mode   Query the parameters that you input. mode in [tps,qps,buffer_hate,locak_table_rate] or all global status."
    print ""

def get_global_status(res_file, parameter):
    if os.path.exists(res_file):
        v_results = []
        for each_para in parameter:
            with open(res_file) as f:
                v_result = [line.split() for line in f.readlines() if each_para in line.split()]
                v_results = v_results + v_result
        # print res_file,v_results
        return dict(v_results)
    else:
        sys.exit(1)

def get_var(res_file,parameter):

    cur_result_dict = {}
    cur_result_dict = get_global_status(res_file, parameter)
    return cur_result_dict

class Common(object):
    def __init__(self,cur_result,per_result,diff_time,mode):
        self.cur_result = cur_result
        self.per_result = per_result
        self.diff_time = diff_time
        self.mode = mode

    def qps(self):
        try:
            res = (int(self.cur_result['Com_select']) + int(self.cur_result['Com_delete']) + int(self.cur_result['Com_insert']) + int(self.cur_result['Com_update']) - int(self.per_result['Com_select']) - int(self.per_result['Com_delete']) - int(self.per_result['Com_insert']) - int(self.per_result['Com_update'])  ) / int(self.diff_time)
            return res
        except Exception as e:
            return -1

    def tps(self):
        try:
            res = (int(self.cur_result['Com_commit']) + int(self.cur_result['Com_rollback']) - int(self.per_result['Com_commit']) - int(self.per_result['Com_rollback'])) / int(self.diff_time)
            return res
        except Exception as e:
            sys.exit(1)

    def buffer_hate(self):
        res = (1- float(self.cur_result['Innodb_buffer_pool_reads'])/float(self.cur_result['Innodb_buffer_pool_read_requests']))
        res = "%.4lf" %res
        return res

    def locak_table_rate(self):
            try:
                sum_lock = (int(self.cur_result['Table_locks_immediate']) - int(self.per_result['Table_locks_immediate'])) + (int(self.cur_result['Table_locks_waited']) - int(self.per_result['Table_locks_waited']))
                if (sum_lock == 0) or (sum_lock < 0):
                    return 0.0
                else:
                    res = (int(self.cur_result['Table_locks_waited']) - int(self.per_result['Table_locks_waited'])) * 100 / sum_lock
                    return res
            except Exception, e:
                sys.exit(1)

    def items(self):
        try:
            res = (int(self.cur_result[self.mode]) - int(self.per_result[self.mode])) / int(self.diff_time)
            res = '%.1lf' % res
            return  res
        except Exception as e:
            sys.exit(1)


'''
mysql 参数差值计算
'''
def diff_calculation(host,port,mode):
    base_dir=os.path.split(os.path.realpath(__file__))[0]
    cache_file_current = r'{base_dir}/var/global_status_current_{host}_{port}.tmp'.format(base_dir=base_dir,host=host,port=port)
    cache_file_past = r'{base_dir}/var/global_status_past_{host}_{port}.tmp'.format(base_dir=base_dir,host=host,port=port)
    if not os.path.isfile(cache_file_past) and not os.path.isfile(cache_file_current):
        print 0
        sys.exit(1)

    parameter_common = ('Connections','Uptime','Com_select','Com_insert','Com_delete','Com_update','Com_rollback','Com_commit','Innodb_buffer_pool_read_requests','Innodb_buffer_pool_reads','Table_locks_immediate','Table_locks_waited')

    # parameter_galera = ('wsrep_cluster_state_uuid','wsrep_cluster_conf_id','wsrep_cluster_size','wsrep_cluster_status','wsrep_ready','wsrep_connected','wsrep_local_state_comment','wsrep_local_recv_queue_avg','wsrep_flow_control_paused','wsrep_local_send_queue_avg','wsrep_flow_control_paused_ns','wsrep_local_cert_failures','wsrep_local_bf_aborts')

    cur_result = get_var(cache_file_current,parameter_common)
    per_result = get_var(cache_file_past,parameter_common)

    try :
        diff_time = int(cur_result['Uptime']) - int(per_result['Uptime'])
    except KeyError as e:
        diff_time = 0

    cls = Common(cur_result=cur_result,per_result=per_result,diff_time=diff_time,mode=mode)

    if diff_time == 0:
        print 0
        sys.exit(1)
    else:
        if mode == 'qps':
            print cls.qps()
        elif mode == 'tps':
            print cls.tps()
        elif mode == 'buffer_hate':
            print cls.buffer_hate()
        elif mode == 'locak_table_rate':
            print cls.locak_table_rate()
        else:
            print cls.items()

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["port=", "mode=","host=","help"])
    except getopt.GetoptError, err:
        print err
        sys.exit(1)

    #从参数取值
    opt_dict = {}
    for k, v in opts:
        if k in ("--help"):
            usage()
            sys.exit()
        if k in ("--port"):
            opt_dict['port'] = v
        elif k in ("--mode"):
            opt_dict['mode'] = v
        elif k in ("--host"):
            opt_dict['host'] = v

    if 'port' in opt_dict.keys():
        port = opt_dict['port']
    else:
        port = '3306'
    if 'mode' in opt_dict.keys():
        mode = opt_dict['mode']
    else:
        mode = 'qps'
    if 'host' in opt_dict.keys():
        host = opt_dict['host']
    else:
        host = '127.0.0.1'

    diff_calculation(host=host,port=port,mode=mode)

if __name__ == "__main__":
    main()