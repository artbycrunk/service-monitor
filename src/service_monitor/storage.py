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

