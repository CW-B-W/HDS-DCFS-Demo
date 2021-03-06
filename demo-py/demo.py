#do_sleep = True
do_sleep = False

import os
import sys
import time
from datetime import datetime
# add paths, otherwise python3 launched by DCFS would go wrong
for p in ['', '/usr/lib/python36.zip', '/usr/lib/python3.6', '/usr/lib/python3.6/lib-dynload', '/home/brad/.local/lib/python3.6/site-packages', '/usr/local/lib/python3.6/dist-packages', '/usr/lib/python3/dist-packages']:
    sys.path.append(p)
#sys.path.append('/home/brad/hadoop-3.2.2/bin')
import pandas as pd
from pandasql import sqldf
import sqlalchemy
from sqlalchemy import create_engine
import json
from pymongo import MongoClient
from cassandra.cluster import Cluster
from elasticsearch import Elasticsearch
#elasticsearch lib
from pandas.io.json import json_normalize
from elasticsearch_dsl import Search

''' ========== RabbitMQ ========== '''
import pika, sys

TASKSTATUS_ACCEPTED   = 1
TASKSTATUS_PROCESSING = 2
TASKSTATUS_SUCCEEDED  = 3
TASKSTATUS_FAILED     = 4
TASKSTATUS_ERROR      = 5
TASKSTATUS_UNKNOWN    = 6
def send_task_status(task_id, status, message):
    credentials = pika.PlainCredentials('brad', '00000000')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='192.168.103.52', credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='task_status')

    payload = {
        'task_id': task_id,
        'status': status,
        'message': message
    }
    body = json.dumps(payload)

    channel.basic_publish(exchange='', routing_key='task_status', body=body)
    connection.close()
''' ========== RabbitMQ ========== '''

try:
    taskinfo_filepath = sys.argv[1]
    print(taskinfo_filepath)
    with open(taskinfo_filepath, 'r') as rf:
        task_info = json.load(rf)

    task_id = str(task_info['task_id'])
except Exception as e:
    with open(taskinfo_filepath, 'r') as rf:
        content = rf.readlines()
    print(str(e))
    send_task_status(str(-1), TASKSTATUS_UNKNOWN, str(e))
    exit(1)

send_task_status(task_id, TASKSTATUS_PROCESSING, '')

for i, d in enumerate(task_info['db']):
    db_type = d['type']
    if db_type == 'mysql':
        try:
            username = d['username']
            password = d['password']
            ip       = d['ip']
            port     = d['port']
            db_name  = d['db']
            db_url   = 'mysql+pymysql://%s:%s@%s:%s/%s' % (username, password, ip, port, db_name)
            db_engine          = create_engine(db_url)
            send_task_status(task_id, TASKSTATUS_PROCESSING, "Retrieving data from MySQL")
            if do_sleep:
                time.sleep(5)
            locals()['df%d'%i] = pd.read_sql(d['sql'], con=db_engine)
        except Exception as e:
            print(str(e))
            send_task_status(task_id, TASKSTATUS_FAILED, "Error in retrieving data from MySQL: " + str(e))
            exit(1)
    elif db_type == 'mssql':
        try:
            username = d['username']
            password = d['password']
            ip       = d['ip']
            port     = d['port']
            db_name  = d['db']
            db_url   = 'mssql+pymssql://%s:%s@%s:%s/%s' % (username, password, ip, port, db_name)
            db_engine          = create_engine(db_url)
            send_task_status(task_id, TASKSTATUS_PROCESSING, "Retrieving data from MSSQL")
            if do_sleep:
                time.sleep(5)
            locals()['df%d'%i] = pd.read_sql(d['sql'], con=db_engine)
        except Exception as e:
            print(str(e))
            send_task_status(task_id, TASKSTATUS_FAILED, "Error in retrieving data from MSSQL: " + str(e))
            exit(1)
    elif db_type == 'oracle':
        try:
            username = d['username']
            password = d['password']
            ip       = d['ip']
            port     = d['port']
            db_name  = d['db']
            db_url   = 'oracle+cx_oracle://%s:%s@%s:%s/?service_name=%s' % (username, password, ip, port, db_name)
            db_engine          = create_engine(db_url)
            send_task_status(task_id, TASKSTATUS_PROCESSING, "Retrieving data from OracleDB")
            if do_sleep:
                time.sleep(5)
            locals()['df%d'%i] = pd.read_sql(d['sql'], con=db_engine)
        except Exception as e:
            print(str(e))
            send_task_status(task_id, TASKSTATUS_FAILED, "Error in retrieving data from OracleDB: " + str(e))
            exit(1)
    elif db_type == 'cassandra':
        try:
            
            username = d['username']
            password = d['password']
            ip       = d['ip']
            port     = d['port']
            db_name  = d['db']
            cluster = Cluster([ip],port=port)
            session = cluster.connect()
            rows = session.execute(d['sql'])
#            local()['df%d'%i] = df1
#            db_url   = 'oracle+cx_oracle://%s:%s@%s:%s/?service_name=%s' % (username, password, ip, port, db_name)
#            db_engine          = create_engine(db_url)
            send_task_status(task_id, TASKSTATUS_PROCESSING, "Retrieving data from Cassandra")
            if do_sleep:
                time.sleep(5)
            locals()['df%d'%i] = pd.DataFrame(rows)
        except Exception as e:
            print(str(e))
            send_task_status(task_id, TASKSTATUS_FAILED, "Error in retrieving data from Cassandra: " + str(e))
            exit(1)
    elif db_type == 'elasticsearch':
        try:
            username = d['username']
            password = d['password']
            ip       = d['ip']
            port     = d['port']
            db_name  = d['db']

            es=Elasticsearch(hosts=ip, port=port)
            result=es.sql.query(body={'query': d['sql']})
            col = []
            l = len(result['columns'])
            for x in range(l):
                col.append(result['columns'][x]['name'])
            #df = pd.DataFrame(result['rows'],columns =col)
            send_task_status(task_id, TASKSTATUS_PROCESSING, "Retrieving data from Elasticsearch")
            if do_sleep:
                time.sleep(5)
            locals()['df%d'%i] = pd.DataFrame(result['rows'],columns =col)
        except Exception as e:
            print(str(e))
            send_task_status(task_id, TASKSTATUS_FAILED, "Error in retrieving data from Elasticsearch: " + str(e))
            exit(1)
    elif db_type == 'mongodb':
        try:
            username = d['username']
            password = d['password']
            ip       = d['ip']
            port     = d['port']
            db_name  = d['db']
            tbl_name = d['collection']
            mongo_client = MongoClient(ip, int(port))
            mongo_db     = mongo_client[db_name]
            filterj      = d['filter']
            send_task_status(task_id, TASKSTATUS_PROCESSING, "Retrieving data from MongoDB")
            if do_sleep:
                time.sleep(5)
            mongo_cursor = mongo_db[tbl_name].find({}, filterj)
            locals()['df%d'%i] = pd.DataFrame(list(mongo_cursor))
        except Exception as e:
            print(str(e))
            send_task_status(task_id, TASKSTATUS_FAILED, "Error in retrieving data from MongoDB: " + str(e))
            exit(1)
    else:
        print("Unsupported DB type " + db_type)
        send_task_status(task_id, TASKSTATUS_FAILED, "Unsupported DB type " + db_type)
        exit(1)
    print(locals()['df%d'%i])

if len(task_info['db']) < 2:
    df_joined = df0
else:
    # use pandasql to join tables
    try:
        pysqldf   = lambda q: sqldf(q, globals())
        send_task_status(task_id, TASKSTATUS_PROCESSING, "Joining two tables")
        if do_sleep:
            time.sleep(10)
        df_joined = pysqldf(task_info['join_sql'])
        columns_order = task_info['hds']['columns']
        df_joined = df_joined.reindex(columns_order, axis=1)
    except Exception as e:
        print(str(e))
        send_task_status(task_id, TASKSTATUS_FAILED, "Error in joining the two tables: " + str(e))
        exit(1)
print(df_joined)



# save to csv
ts = str(datetime.now().timestamp())
os.makedirs("/tmp/dcfs", exist_ok=True)
tmp_sql_path = '/tmp/dcfs/joined_' + task_id + ts + '.sql'
tmp_csv_path = '/tmp/dcfs/joined_' + task_id + ts + '.csv'
table_name = task_info['hds']['table']
with open(tmp_sql_path, 'w') as wf:
    wf.write(task_info['hds']['sql'])
df_joined.to_csv(tmp_csv_path, index=False, header=False)


''' ========== Phoenix ========== '''
import subprocess
#phoenix_home = os.environ['PHOENIX_HOME']
phoenix_home = "/home/brad/phoenix-hbase-2.3-5.1.2-bin"
if 'ip' in task_info['hds']:
    hds_ip = task_info['hds']['ip']
else:
    hds_ip = '192.168.103.151'
cmd = phoenix_home+"/bin/psql.py %s -t \"%s\" %s %s" % (hds_ip, table_name.upper(), tmp_sql_path, tmp_csv_path)
process = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
stdout, stderr = process.communicate()
exit_code = process.wait()
if exit_code != 0:
    print(stderr.decode('utf-8'))
    send_task_status(task_id, TASKSTATUS_FAILED, "Failed to import table into HDS\n" + stderr.decode('utf-8'))
    exit(1)
else:
    send_task_status(task_id, TASKSTATUS_PROCESSING, "Successfully import table into HDS")
''' ========== Phoenix ========== '''

send_task_status(task_id, TASKSTATUS_SUCCEEDED, "Job finished")
exit()
