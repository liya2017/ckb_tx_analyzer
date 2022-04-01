#!/usr/bin/python3
from configparser import ConfigParser
import psycopg2
from sqlalchemy import create_engine
import re
import codecs
import subprocess
import platform
def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
 
    # get section, default to postgresql
    db = {}
    
    # Checks to see if section (postgresql) parser exists
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
         
    # Returns an error if a parameter is called that is not listed in the initialization file
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db

def get_postgresql_connection(sql):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        cur.execute(sql)
        conn.commit()
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def insert_data_to_db(tx_time,tx_hash,cycles,ckb_vm):
    sql="INSERT INTO tx_monitor (tx_time, tx_hash, cycles,vm_version) VALUES ('"+tx_time+"','"+tx_hash+"','"+cycles+"','"+ckb_vm+"')"
    print(sql)
    get_postgresql_connection(sql)

def parse_and_insert_data(line):
    tx_time=str(line).split("+")[0].split("'")[1]
    tx_hash=str(line).split("{")[1].split(",")[0].split(":")[1]
    cycles=str(line).split("{")[1].split(",")[1].split(":")[1].split("}")[0]
    ckb_vm="aarch64 ASM"
    insert_data_to_db(tx_time,tx_hash,cycles,ckb_vm)

def log_to_pg_data():
    p = subprocess.Popen('tail -F /Users/xuliya/Downloads/ckb_v0.101.7_x86_64-apple-darwin/data/logs/ckb_tx_monitor.log', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,)    #起一个进程，执行shell命令
    while True:
        line = p.stdout.readline()   #实时获取行
        if line:                   #如果行存在的话
            parse_and_insert_data(line)
            

if __name__ == '__main__':
     log_to_pg_data()
    # sql="INSERT INTO tx_monitor (tx_time, tx_hash, cycles,vm_version) VALUES ('2022-04-01 08:43:21.371','0xa6dc9defa5e418a0a88b3edb67382ef74dfe32ae668942afa634c28cae0e18a3','3427460','arm64')"
    # get_postgresql_connection(sql)