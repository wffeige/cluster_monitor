#Author:'wangfei'
#Date:'2018/1/2 0002 17:52'
#Function:
import os
import sys
import getopt
from  get_diff import get_global_status
from MySQL import MySQL

base_dir=os.path.split(os.path.realpath(__file__))[0]

def usage():
    print "Usage: %s {OPTIONS...}" % sys.argv[0]
    print "-h|--help  print help message"
    print "MySQL DSN:"
    print "  --host, --port, --mode"
    print "  --host   Query the host of mysql server that you configured in config "
    print "  --mode   Query the parameters that you input. mode in [tps,qps,buffer_hit,locak_table_rate] or all global status."
    print ""

def get_status(res_file,parameter,mode):
    cur_result_dict = {}
    cur_result_dict = get_global_status(res_file, parameter)
    return cur_result_dict[mode]

def check_status(type,mode,port,host):
    if type == "galera_status":
        cache_file_current = r'{base_dir}/var/global_status_current_{host}_{port}.tmp'.format(base_dir=base_dir,host=host,port=port)
        parameter = ('wsrep_flow_control_paused','Uptime','wsrep_local_recv_queue','wsrep_local_recv_queue_avg','wsrep_local_send_queue','wsrep_local_send_queue_avg','wsrep_cluster_size','wsrep_cluster_status','wsrep_ready','wsrep_connected','wsrep_cluster_conf_id','wsrep_cluster_state_uuid',)

    elif type == "slave_status":
        cache_file_current = r'{base_dir}/var/slave_status_{host}_{port}.tmp'.format(base_dir=base_dir,host=host,port=port)
        parameter = ('Slave_IO_State','master_host','Master_User','Master_Port','Connect_Retry','IO_Running','SQL_Running','Replicate_Ignore_DB','Replicate_Do_Table','Replicate_Ignore_Table','Replicate_Wild_Do_Table','Last_Errno','Last_Error','Exec_Master_Log_Pos')
    else:
        sys.exit(1)

    if mode in parameter:
        cur_result = get_status(res_file=cache_file_current,parameter=parameter,mode=mode)
        return cur_result
    else:
        sys.exit(1)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["port=", "mode=","host=","type="])
    except getopt.GetoptError, err:
        print err
        sys.exit(1)

    #从参数取值
    opt_dict = {}
    for k, v in opts:
        if k in ("--port"):
            opt_dict['port'] = v
        elif k in ("--mode"):
            opt_dict['mode'] = v
        elif k in ("--host"):
            opt_dict['host'] = v
        elif k in ("--type"):
            opt_dict['type'] = v

    if 'port' in opt_dict.keys():
        port = opt_dict['port']
    else:
        port = '3306'
    if 'mode' in opt_dict.keys():
        mode = opt_dict['mode']
    else:
        mode = 'master_host'
    if 'host' in opt_dict.keys():
        host = opt_dict['host']
    else:
        host = '127.0.0.1'
    if 'type' in opt_dict.keys():
        type = opt_dict['type']
    else:
        type = ''


    print check_status(type=type,mode=mode,port=port,host=host)

if __name__ == "__main__":
    main()