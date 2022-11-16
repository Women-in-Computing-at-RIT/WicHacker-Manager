import mysql.connector as mysql
import os
import logging

"""
    Thank you to the RIT SWEN department for the starter code for this module
"""
logger = logging.getLogger("DB_Utils")


def connect():
    try:
        return mysql.connect(database=os.environ.get('DBNAME'),
                         user=os.environ.get('DB_USER'),
                         password=os.environ.get('PASSWORD'),
                         host=os.environ.get('HOST'),
                         port=int(os.environ.get('PORT')),
                         )
    except Exception as error:
        logger.error("Database Connection Error: %s", error)
        return None


def exec_migration(version) -> bool:
    conn = connect()
    if conn is None:
        logger.error("Database Connection Error. Script: %s", version)
        return False
    cur = conn.cursor()
    try:
        full_path = os.path.join(os.path.dirname(__file__), f'migration/scripts/{version}')
        cur = conn.cursor()
        sqlStatements = None
        with open(full_path, 'r') as file:
            sqlStatements = file.read().split(';')
        for sqlStatement in sqlStatements:
            cur.execute(sqlStatement)
            cur.close()
            cur = conn.cursor()

        sql = "INSERT INTO Migrations (version, dirtyVersion) VALUES (%(version)s, %(dirty)s);"
        args = {"version": version, "dirty": False}
        cur.execute(sql, args)
        cur.close()
        conn.commit()
        conn.close()
    except Exception as error:
        logger.error("Migration Execution Error. Script: %s Error: %s", version, error)
        conn.rollback()
        cur.close()
        conn.close()
        return False
    return True


def exec_get_one(sql, args={}):
    conn = connect()
    if conn is None:
        return None
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(sql, args)
        one = cur.fetchone()
        cur.close()
        conn.close()
        return one
    except Exception as error:
        logger.error("SQL Execution Error: %s", error)
        conn.rollback()
        cur.close()
        conn.close()
        return None


def exec_get_all(sql, args={}):
    conn = connect()
    if conn is None:
        return None
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(sql, args)
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results
    except Exception as error:
        logger.error("SQL Execution Error: %s", error)
        conn.rollback()
        cur.close()
        conn.close()
        return None


def exec_commit(sql, args={}):
    conn = connect()
    if conn is None:
        return None
    cur = conn.cursor()
    try:
        cur.execute(sql, args)
        result = cur.rowcount
        cur.close()
        conn.commit()
        conn.close()
        return result
    except Exception as error:
        logger.error("SQL Execution Error: %s", error)
        conn.rollback()
        cur.close()
        conn.close()
        return None


def exec_commit_return_autoincremented_id(sql, args={}):
    conn = connect()
    if conn is None:
        return None
    cur = conn.cursor()
    try:
        cur.execute(sql, args)
        # LAST_INSERT_ID is connection dependent so will not be impacted by writes on other connections
        # https://dev.mysql.com/doc/refman/8.0/en/information-functions.html#function_last-insert-id
        cur.execute("SELECT LAST_INSERT_ID();")
        one = cur.fetchone()
        cur.close()
        conn.commit()
        conn.close()
        if len(one) != 1:
            logger.error("LAST_INSERT_ID returned no values")
            raise Exception("LAST_INSERT_ID returned no values")
        return one[0]
    except Exception as error:
        logger.error("SQL Execution Error: %s", error)
        conn.rollback()
        cur.close()
        conn.close()
        return None


def exec_commit_return(sql, args={}):
    conn = connect()
    if conn is None:
        return None
    cur = conn.cursor()
    try:
        cur.execute(sql, args)
        one = cur.fetchone()
        conn.commit()
        conn.close()
        return one
    except Exception as error:
        logger.error("SQL Execution Error: %s", error)
        conn.rollback()
        cur.close()
        conn.close()
        return None
