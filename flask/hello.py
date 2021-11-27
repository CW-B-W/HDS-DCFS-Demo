#!/usr/bin/env python

import json

''' ========== TaskStatus ========== '''
import pika, sys, os, threading

lastest_message = "" # remember to declare `global` in functions
task_status_dict = {}

TASKSTATUS_ACCEPTED   = 1
TASKSTATUS_PROCESSING = 2
TASKSTATUS_SUCCEEDED  = 3
TASKSTATUS_FAILED     = 4
TASKSTATUS_ERROR      = 5
TASKSTATUS_UNKNOWN    = 6
def listen_task_status_queue():
    global lastest_message
    lastest_message = "consuming"
    credentials = pika.PlainCredentials('brad', '00000000')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.103.52', credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='task_status')

    def callback(ch, method, properties, body):
        global lastest_message
        print(" [x] Received %r" % body)
        lastest_message = body.decode('utf-8')
        add_task_status(json.loads(lastest_message))
        print("lastest_message = %s" % lastest_message)

    channel.basic_consume(queue='task_status', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
    print('Consumer finished')

consumer_thread = threading.Thread(target=listen_task_status_queue)
consumer_thread.start()

def add_task_status(task_status):
    global task_status_dict
    task_id = str(task_status['task_id'])
    task_status_dict[task_id] = task_status

def get_task_status(task_id_list):
    global task_status_dict
    res_list = []
    if len(task_id_list) == 0:
        for k in task_status_dict:
            res_list.append(task_status_dict[k])
    for task_id in task_id_list:
        if task_id in task_status_dict:
            res_list.append(task_status_dict[task_id])
    return res_list
''' ========== TaskStatus  ========== '''



''' =============== MongoDB =============== '''
import pandas as pd
from pymongo import MongoClient
from bson import Code

mongo_client = MongoClient('192.168.103.52')

def mongodb_list_all_dbs():
    global mongo_client
    return mongo_client.list_database_names()

def mongodb_list_all_collections(db_name):
    global mongo_client
    db = mongo_client[db_name]
    return db.list_collection_names()


def mongodb_list_all_keys(db_name, collection_name):
    global mongo_client
    db = mongo_client[db_name]
    map = Code("function() { for (var key in this) { emit(key, null); } }")
    reduce = Code("function(key, stuff) { return null; }")
    result = db[collection_name].map_reduce(map, reduce, "myresults")
    return result.distinct('_id')
''' =============== MongoDB =============== '''



''' ================ MySQL ================ '''
import pandas as pd
from pandasql import sqldf
from sqlalchemy import create_engine

def mysql_list_all_dbs(username, password, ip, port='3306'):
#db1_engine = create_engine(r"mysql+pymysql://brad:00000000@Brad-HDS-Master:3306/")
    db1_engine = create_engine("mysql+pymysql://%s:%s@%s:%s/" % (username, password, ip, port))
    df1 = pd.read_sql("SHOW DATABASES;", con=db1_engine)
    return df1.iloc[:,0].tolist()

def mysql_list_all_tables(db_name, username, password, ip, port='3306'):
#db1_engine = create_engine(r"mysql+pymysql://brad:00000000@Brad-HDS-Master:3306/%s" % db_name)
    db1_engine = create_engine("mysql+pymysql://%s:%s@%s:%s/%s" % (username, password, ip, port, db_name))
    df1 = pd.read_sql("SHOW TABLES", con=db1_engine)
    return df1.iloc[:,0].tolist()

def mysql_list_all_keys(db_name, table_name, username, password, ip, port='3306'):
#db1_engine = create_engine(r"mysql+pymysql://brad:00000000@Brad-HDS-Master:3306/%s" % db_name)
    db1_engine = create_engine("mysql+pymysql://%s:%s@%s:%s/%s" % (username, password, ip, port, db_name))
    df_col = pd.read_sql("SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='%s' AND `TABLE_NAME`='%s'" % (db_name, table_name), con=db1_engine);
    return df_col['COLUMN_NAME'].tolist()


''' ================ MySQL ================ '''



''' ================ MSSQL ================ '''
import pandas as pd
from pandasql import sqldf
from sqlalchemy import create_engine

def mssql_list_all_dbs(username, password, ip, port='1433'):
    db1_engine = create_engine("mssql+pymssql://%s:%s@%s:%s/" % (username, password, ip, port))
    df1 = pd.read_sql("SELECT name FROM master.dbo.sysdatabases", con=db1_engine)
    return df1.iloc[:,0].tolist()

def mssql_list_all_tables(db_name, username, password, ip, port='1433'):
    db1_engine = create_engine("mssql+pymssql://%s:%s@%s:%s/%s" % (username, password, ip, port, db_name))
    df1 = pd.read_sql("SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'", con=db1_engine)
    return df1.iloc[:,2].tolist()

def mssql_list_all_keys(db_name, table_name, username, password, ip, port='1433'):
    db1_engine = create_engine("mssql+pymssql://%s:%s@%s:%s/%s" % (username, password, ip, port, db_name))
    df1 = pd.read_sql("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='%s' ORDER BY ORDINAL_POSITION" % table_name, con=db1_engine);
    return df1.iloc[:,0].tolist()


''' ================ MsSQL ================ '''

''' ================ oracle ================ '''
import pandas as pd
from pandasql import sqldf
from sqlalchemy import create_engine
import cx_Oracle
from sqlalchemy import *
#db1_engine = create_engine(r"oracle+cx_oracle://brad:00000000@192.168.103.60:1521/?service_name=XEPDB1")

def oracle_list_all_dbs(username, password, ip, port='1521'):
    db1_engine = create_engine(r"oracle+cx_oracle://%s:%s@%s:%s/?service_name=XEPDB1" % (username, password, ip, port))
    df1 = pd.read_sql("select * from global_name", con=db1_engine)
    return df1.iloc[:,0].tolist()

def oracle_list_all_tables(db_name, username, password, ip, port='1521'):
    #db1_engine = create_engine(r"oracle+cx_oracle://%s:%s@%s:%s/%s" % (username, password, ip, port, db_name))
    #df1 = pd.read_sql("SELECT table_name FROM user_tables", con=db1_engine)
    db1_engine = create_engine(r"oracle+cx_oracle://%s:%s@%s:%s/?service_name=%s" % (username, password, ip, port, db_name))
    df1 = pd.read_sql("SELECT table_name FROM user_tables", con=db1_engine)
    return df1.iloc[:,0].tolist()

def oracle_list_all_keys(db_name, table_name, username, password, ip, port='1521'):
    db1_engine = create_engine(r"oracle+cx_oracle://%s:%s@%s:%s/?service_name=%s" % (username, password, ip, port, db_name))
    df1 = pd.read_sql("SELECT column_name FROM all_tab_cols WHERE table_name = '%s'" % table_name, con=db1_engine);
    return df1.iloc[:,0].tolist()



''' ================ oracle ================ '''
''' ================ cassandra ================ '''
import pandas as pd
from cassandra.cluster import Cluster



def cassandra_list_all_dbs(username, password, ip, port='9042'):
    #db1_engine = create_engine(r"oracle+cx_oracle://%s:%s@%s:%s/?service_name=XEPDB1" % (username, password, ip, port))
    #df1 = pd.read_sql("select * from global_name", con=db1_engine)
    cluster = Cluster([ip],port=9042)
    session = cluster.connect()
    rows = session.execute("DESCRIBE keyspaces;")
    df1 = pd.DataFrame(rows)
    return df1["keyspace_name"].tolist()

def cassandra_list_all_tables(db_name, username, password, ip, port='9042'):
    #db1_engine = create_engine(r"oracle+cx_oracle://%s:%s@%s:%s/%s" % (username, password, ip, port, db_name))
    #df1 = pd.read_sql("SELECT table_name FROM user_tables", con=db1_engine)
    #db1_engine = create_engine(r"oracle+cx_oracle://%s:%s@%s:%s/?service_name=%s" % (username, password, ip, port, db_name))
    #df1 = pd.read_sql("SELECT table_name FROM user_tables", con=db1_engine)
    cluster = Cluster([ip],port=9042)
    session = cluster.connect()
    rows = session.execute("SELECT * FROM system_schema.tables WHERE keyspace_name = '%s'" % (db_name))
    df1 = pd.DataFrame(rows)
    return df1["table_name"].tolist()

def cassandra_list_all_keys(db_name, table_name, username, password, ip, port='9042'):
    #db1_engine = create_engine(r"oracle+cx_oracle://%s:%s@%s:%s/?service_name=%s" % (username, password, ip, port, db_name))
    #df1 = pd.read_sql("SELECT column_name FROM all_tab_cols WHERE table_name = '%s'" % table_name, con=db1_engine);
    cluster = Cluster([ip],port=9042)
    session = cluster.connect()
    rows = session.execute("SELECT * FROM system_schema.columns WHERE keyspace_name = '%s'AND table_name = '%s'" % (db_name, table_name))
    df1 = pd.DataFrame(rows)
    return df1["column_name"].tolist()
    #return df1.iloc[:,0].tolist()



''' ================ cassandra ================ '''

''' ================ Flask ================ '''
from flask import Flask, request, render_template
from flask import render_template
from flask_cors import CORS
#You need to use following line [app Flask(__name__]
app = Flask(__name__, template_folder='template')
CORS(app)

@app.route('/hello')
def hello():
    return 'Hello, Flask'

@app.route('/about/')
def about():
    return 'about Flask'

@app.route('/rabbitMQ')
def mq():
    global lastest_message
    print("/rabbitMQ: lastest_message=%s" % lastest_message)
    return lastest_message

val = 0
@app.route('/value')
def value():
    global val
    val += 1
    return str(val)

''' ----- MongoDB ----- '''
@app.route('/mongo/listdbs', methods=['GET'])
def mongo_dbs():
    ret_dict = {
        'db_list': mongodb_list_all_dbs()
    }
    return ret_dict 

@app.route('/mongo/listcollections', methods=['GET'])
def mongo_collections():
    db_name = request.args.get('db_name')
    ret_dict = {
        'collection_list': mongodb_list_all_collections(db_name)
    }
    return ret_dict 

@app.route('/mongo/listkeys', methods=['GET'])
def mongo_keys():
    db_name = request.args.get('db_name')
    collection_name = request.args.get('collection_name')
    ret_dict = {
        'key_list': mongodb_list_all_keys(db_name, collection_name)
    }
    return ret_dict 

''' ----- MySQL ----- '''
@app.route('/mysql/listdbs', methods=['GET'])
def mysql_dbs():
    try:
        username = request.args.get('username')
        password = request.args.get('password')
        ip       = request.args.get('ip')
        port     = request.args.get('port')
        ret_dict = {
            'db_list': mysql_list_all_dbs(username, password, ip, port)
        }
        return ret_dict 
    except:
        return "Error connecting to MySQL server", 403

@app.route('/mysql/listtables', methods=['GET'])
def mysql_tables():
    try:
        username = request.args.get('username')
        password = request.args.get('password')
        ip       = request.args.get('ip')
        port     = request.args.get('port')
        db_name = request.args.get('db_name')
        ret_dict = {
            'table_list': mysql_list_all_tables(db_name, username, password, ip, port)
        }
        return ret_dict 
    except:
        return "Error connecting to MySQL server", 403


@app.route('/mysql/listkeys', methods=['GET'])
def mysql_keys():
    try:
        username = request.args.get('username')
        password = request.args.get('password')
        ip       = request.args.get('ip')
        port     = request.args.get('port')
        db_name  = request.args.get('db_name')
        table_name = request.args.get('table_name')
        ret_dict = {
            'key_list': mysql_list_all_keys(db_name, table_name, username, password, ip, port)
        }
        return ret_dict 
    except:
        return "Error connecting to MySQL server", 403

''' ----- MSSQL ----- '''
@app.route('/mssql/listdbs', methods=['GET'])
def mssql_dbs():
    try:
        username = request.args.get('username')
        password = request.args.get('password')
        ip       = request.args.get('ip')
        port     = request.args.get('port')
        ret_dict = {
            'db_list': mssql_list_all_dbs(username, password, ip, port)
        }
        return ret_dict 
    except:
        return "Error connecting to MSSQL server", 403

@app.route('/mssql/listtables', methods=['GET'])
def mssql_tables():
    try:
        username = request.args.get('username')
        password = request.args.get('password')
        ip       = request.args.get('ip')
        port     = request.args.get('port')
        db_name = request.args.get('db_name')
        ret_dict = {
            'table_list': mssql_list_all_tables(db_name, username, password, ip, port)
        }
        return ret_dict 
    except:
        return "Error connecting to MSSQL server", 403


@app.route('/mssql/listkeys', methods=['GET'])
def mssql_keys():
    try:
        username = request.args.get('username')
        password = request.args.get('password')
        ip       = request.args.get('ip')
        port     = request.args.get('port')
        db_name  = request.args.get('db_name')
        table_name = request.args.get('table_name')
        ret_dict = {
            'key_list': mssql_list_all_keys(db_name, table_name, username, password, ip, port)
        }
        return ret_dict 
    except:
        return "Error connecting to MSSQL server", 403

''' ----- Oracle ----- '''
@app.route('/oracle/listdbs', methods=['GET'])
def oracle_dbs():
    try:
        username = request.args.get('username')
        password = request.args.get('password')
        ip       = request.args.get('ip')
        port     = request.args.get('port')
        ret_dict = {
            'db_list': oracle_list_all_dbs(username, password, ip, port)
        }
        return ret_dict 
    except:
        return "Error connecting to Oracle server", 403

@app.route('/oracle/listtables', methods=['GET'])
def oracle_tables():
    try:
        username = request.args.get('username')
        password = request.args.get('password')
        ip       = request.args.get('ip')
        port     = request.args.get('port')
        db_name = request.args.get('db_name')
        ret_dict = {
            'table_list': oracle_list_all_tables(db_name, username, password, ip, port)
        }
        return ret_dict 
    except:
        return "Error connecting to Oracle server", 403


@app.route('/oracle/listkeys', methods=['GET'])
def oracle_keys():
    try:
        username = request.args.get('username')
        password = request.args.get('password')
        ip       = request.args.get('ip')
        port     = request.args.get('port')
        db_name  = request.args.get('db_name')
        table_name = request.args.get('table_name')
        ret_dict = {
            'key_list': oracle_list_all_keys(db_name, table_name, username, password, ip, port)
        }
        return ret_dict 
    except:
        return "Error connecting to Oracle server", 403


''' ----- Cassandra ----- '''
@app.route('/cassandra/listdbs', methods=['GET'])
def cassandra_dbs():
    try:
        username = request.args.get('username')
        password = request.args.get('password')
        ip       = request.args.get('ip')
        port     = request.args.get('port')
        ret_dict = {
            'db_list': cassandra_list_all_dbs(username, password, ip, port)
        }
        return ret_dict 
    except:
        return "Error connecting to Cassandra server", 403

@app.route('/cassandra/listtables', methods=['GET'])
def cassandra_tables():
    try:
        username = request.args.get('username')
        password = request.args.get('password')
        ip       = request.args.get('ip')
        port     = request.args.get('port')
        db_name = request.args.get('db_name')
        ret_dict = {
            'table_list': cassandra_list_all_tables(db_name, username, password, ip, port)
        }
        return ret_dict 
    except:
        return "Error connecting to Cassandra server", 403


@app.route('/cassandra/listkeys', methods=['GET'])
def cassandra_keys():
    try:
        username = request.args.get('username')
        password = request.args.get('password')
        ip       = request.args.get('ip')
        port     = request.args.get('port')
        db_name  = request.args.get('db_name')
        table_name = request.args.get('table_name')
        ret_dict = {
            'key_list': cassandra_list_all_keys(db_name, table_name, username, password, ip, port)
        }
        return ret_dict 
    except:
        return "Error connecting to Cassandra server", 403

''' ----- TaskStatus ----- '''
@app.route('/taskstatus', methods=['GET'])
def task_status():
    task_id = request.args.get('task_id')
    try:
        if task_id is None:
            return json.dumps(get_task_status([]))
        else:
            return json.dumps(get_task_status(task_id.split(',')))
    except Exception as e:
        print(e)
        return "Task not found", 400
        


@app.route('/')
def index():
    return render_template('index.html')

''' ================ Flask ================ '''
