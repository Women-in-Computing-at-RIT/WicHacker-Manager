import psycopg2
import os
import logging

"""
    Thank you to the RIT SWEN department for the starter code for this module
"""

FORMAT = '%(level)s %(asctime)s %(message)s %(err)s %(migrationFile)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger("DB_Utils")

def connect():
    return psycopg2.connect(dbname=os.environ.get('DBNAME'),
                            user=os.environ.get('USER'),
                            password=os.environ.get('PASSWORD'),
                            host=os.environ.get('HOST'),
                            port=os.environ.get('PORT'))

def exec_migration(path) -> bool:
    versionList = path.split()
    if len(versionList) != 2:
        logInfo = {"level": "CRITICAL", "err": None, "migrationFile": path}
        logger.error("Migration File Format Incorrect. Aborting Further Migration, shut down application to avoid conflicts", extra=logInfo)
        return False
    version = versionList[1]
    conn = None
    try:
        conn = connect()
    except Exception as err:
        logInfo = {"level": "CRITICAL", "err": err, "migrationFile": path}
        logger.error("Database Connection Error", extra=logInfo)
        return False

    try:
        full_path = os.path.join(os.path.dirname(__file__), f'migration/{path}')
        cur = conn.cursor()
        with open(full_path, 'r') as file:
            cur.execute(file.read())

        sql = "UPDATE migrations SET version=%(version)s, dirtyVersion=%(dirty)s WHERE migration_id=1"
        args = {"version": version, "dirty": False}
        cur.execute(sql, args)

        conn.commit()
        conn.close()
    except Exception as error:
        logInfo = {"level": "CRITICAL", "err": error, "migrationFile": version}
        logger.error("Migration Execution Error", extra=logInfo)
        conn.close()
        return False
    return True

def exec_get_one(sql, args={}):
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql, args)
    one = cur.fetchone()
    conn.close()
    return one

def exec_get_all(sql, args={}):
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql, args)
    # https://www.psycopg.org/docs/cursor.html#cursor.fetchall

    list_of_tuples = cur.fetchall()
    conn.close()
    return list_of_tuples

def exec_commit(sql, args={}):
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql, args)
    result = cur.rowcount
    conn.commit()
    conn.close()
    return result

def exec_commit_return(sql, args={}):
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql, args)
    one = cur.fetchone()
    conn.commit()
    conn.close()
    return one