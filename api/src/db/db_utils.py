import mysql.connector as mysql
import os
import logging
from utils.aws import getDatabaseSecrets

"""
    Thank you to the RIT SWEN department for the starter code for this module
    
    Please read the README in this directory before editing this file
"""
logger = logging.getLogger("DB_Utils")
DB_NAME = 'wichacks'
USER = None
PASSWORD = None
HOST = None
PORT = None


def initializeDBSecrets() -> bool:
    global USER, PASSWORD, HOST, PORT
    dbSecrets = getDatabaseSecrets()
    USER = dbSecrets['User']
    PASSWORD = dbSecrets['Password']
    HOST = dbSecrets['Host']
    PORT = dbSecrets['Port']

    if USER is None or PORT is None or HOST is None or PORT is None:
        logger.error("Error Retrieving DB Connection Information")
        return False
    return True


def connect() -> mysql.MySQLConnection:
    """
    Retrieve database connection
    :return: mysql connector connection
    """
    try:
        return mysql.connect(database=DB_NAME,
                             user=USER,
                             password=PASSWORD,
                             host=HOST,
                             port=int(PORT),
                             )
    except Exception as error:
        logger.error("Database Connection Error: %s", error)
        return None


def exec_migration(version) -> bool:
    """
    Execute a migration script
    :param version: Name of the migration script file
    :return: true if migration successful, false if error
    """
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


def exec_get_one(sql, args={}) -> (dict, bool):
    """
    Retrieves single record from the dictionary
    :param sql:
    :param args:
    :return: tuple with first element being return dictionary, second being if error occurred
    """
    conn = connect()
    if conn is None:
        return None, True
    cur = conn.cursor(dictionary=True, buffered=True)
    try:
        cur.execute(sql, args)
        one = cur.fetchone()
        cur.close()
        conn.close()
        return one, False
    except Exception as error:
        logger.error("SQL Execution Error: %s", error)
        conn.rollback()
        cur.close()
        conn.close()
        return None, True


def exec_get_all(sql, args={}) -> dict:
    """
    Retrieves many records from the dictionary
    :param sql:
    :param args:
    :return: list of dictionaries or None if error
    """
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


def exec_commit(sql, args={}) -> dict:
    """
    executes sql statement and commits transaction
    :param sql:
    :param args:
    :return: number of rows affected by the action or None if error
    """
    conn = connect()
    if conn is None:
        return None
    cur = conn.cursor(dictionary=True)
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


def exec_commit_return_autoincremented_id(sql, args={}) -> int:
    """
    executes insertion and returns auto-incremented id of the resulting record
    Make sure the target of the table has an auto-incrementing id
    :param sql: sql of insertion statement
    :param args:
    :return:
    """
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


def exec_commit_return(sql, args={}) -> dict:
    """
    executes an sql statement, commits transaction, and returns one result row
    :param sql:
    :param args:
    :return:
    """
    conn = connect()
    if conn is None:
        return None
    cur = conn.cursor(dictionary=True)
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


def exec_commit_link(insertSQL, linkSql, insertArgs={}, linkArgs={}) -> int:
    """
    executes an insertion, fetches auto-incremented id, executes link sql statement and commits transaction
    to add the auto-incremented id to another record
    :param insertSQL: sql for initial insertion
    :param linkSql: sql for linking returned auto-incremented id to new record
    :param insertArgs:
    :param linkArgs: auto-incremented id will be added to these arguments with name "added_id"
    :return: number of rows affected in linking query or None if error
    """
    conn = connect()
    if conn is None:
        return None
    cur = conn.cursor()
    try:
        cur.execute(insertSQL, insertArgs)
        # LAST_INSERT_ID is connection dependent so will not be impacted by writes on other connections
        # https://dev.mysql.com/doc/refman/8.0/en/information-functions.html#function_last-insert-id
        cur.execute("SELECT LAST_INSERT_ID();")
        one = cur.fetchone()
        if len(one) != 1:
            logger.error("LAST_INSERT_ID returned no values")
            raise Exception("LAST_INSERT_ID returned no values")
        autoIncrementedId = one[0]
        linkArgs["added_id"] = autoIncrementedId
        cur.execute(linkSql, linkArgs)
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
