import sqlite3
from sqlite3 import Error
import os
import logging

logger = logging.getLogger(__name__)
DB = None


def get_db():
    """Build a valid storage path for a sqlite db."""
    pkg_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    data_dir = os.path.join(pkg_dir, "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    DB_PATH = os.path.join(data_dir, "monitor.db")
    logger.debug(DB_PATH)
    return DB_PATH


def get_connection():
    """Get a valid connection to the sqlite db"""
    global DB
    if not DB:
        try:
            DB = sqlite3.connect(get_db())
            logger.debug(sqlite3.version)
        except Error as e:
            logger.error(e)

    return DB


def create_table():
    """Create a table if it doesnt exists"""
    conn = get_connection()
    create_table = """
    CREATE TABLE IF NOT EXISTS status (
        id integer PRIMARY KEY,
        name text NOT NULL,
        url text NOT NULL,
        pos integer NOT NULL,
        status text,
        timestamp DATETIME DEFAULT (datetime('now','localtime'))
    ); """
    try:
        c = conn.cursor()
        c.execute(create_table)
    except Error as e:
        logger.error(e)


def insert_row(name, url, status, pos):
    """Add a row to the db based on given info.

    Arguments:
        name(str): name associated with the url.
        url(str): the url to check.
        status(str): the response code
        pos(int): the pos of the url in relatioon to the csv.

    """
    conn = get_connection()
    insert_query = """
        INSERT INTO 'status' ('name', 'url', 'status', 'pos')
        VALUES (?, ?, ?, ?);"""
    data_tuple = (name, url, status, pos)
    try:
        c = conn.cursor()
        c.execute(insert_query, data_tuple)
        conn.commit()
    except Error as e:
        logger.error(e)


def get_summary(metric_span=1):
    """Query records based on a given metric span

    Arguments:
        metric_span(int): time in hours to look back from now for valid records.

    Returns:
        list: Fetched records based on query.

    """
    conn = get_connection()
    cursor = conn.cursor()
    summary_query = """SELECT pos, name, url, group_concat(status), group_concat(timestamp)
        FROM status WHERE (timestamp >= datetime('now', '-{0} hour'))
        GROUP BY name, url ORDER BY pos""".format(metric_span)
    logger.debug(summary_query)
    cursor.execute(summary_query, ())
    return cursor.fetchall()
