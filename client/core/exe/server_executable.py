#!/usr/bin/env python2.7
import time
import psycopg2
import sys

from core import custom

connection = None


def connect():
    try:
        global connection
        connection = psycopg2.connect("dbname=amicoin host=localhost user=amicoin password=amicoin1")
        return True
    except:
        return False


def get_pow(attempt=1):
    if connection is not None:
        cursor = connection.cursor()
        SQL = "SELECT * FROM job WHERE completed = true and rewarded = false and assigned_to <> '' LIMIT 1;"
        cursor.execute(SQL)
        fetch = cursor.fetchone()
        if fetch is not None:
            result = {'group_id': fetch[0], 'job_id': fetch[1], 'job_file': fetch[2], 'assigned_to': fetch[3].strip(),
                      'expiration': fetch[4], 'completed': fetch[5], 'rewarded': fetch[6], 'resultfile': fetch[7]}
        else:
            result = None
        return result
    elif attempt <= 10 and connect() is True:
        return get_pow(attempt + 1)
    else:
        return None


def set_rewarded(pubkey, jobid, attempt=1):
    if connection is not None:
        cursor = connection.cursor()
        sql_query = "UPDATE job SET rewarded = true WHERE assigned_to = %s and job_id = %s and " \
                    "completed = true and rewarded = false;"
        data = (pubkey, jobid,)
        cursor.execute(sql_query, data)
        connection.commit()
        cursor.close()
        return True
    elif attempt <= custom.max_sql_attempts and connect() is True:
        return set_rewarded(attempt + 1)
    else:
        return False


rewarded_pubkey = ''
while True:
    result = get_pow()
    if result is not None:
        rewarded_pubkey = result['assigned_to']
        rewarded_jobid = result['job_id']
        print rewarded_pubkey
        sys.stdout.flush()
        set_rewarded(rewarded_pubkey, rewarded_jobid)
        time.sleep(10)
    else:
        time.sleep(10)
