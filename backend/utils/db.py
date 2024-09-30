import mysql.connector
from mysql.connector import Error
from config import Config
from flask import current_app, g
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Connecting to the database
def get_db_connection():
    if 'db' not in g: 
        try:
            g.db = mysql.connector.connect(**Config.DATABASE_CONFIG)
            logger.info("Database connection established.")
        except Error as e:
            logger.error(f"Error connecting to MySQL Database: {e}")
            g.db = None
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None and db.is_connected():
        db.close()
        logger.info("Database connection closed.")


def init_db(app):
    app.teardown_appcontext(close_db)

def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    connection = get_db_connection()
    if connection is None:
        logger.error("Failed to connect to the database.")
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch_one:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
        else:
            connection.commit()
            result = cursor.rowcount

        return result
    except Error as e:
        logger.error(f"Error in executing query: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def check_db_connection():
    connection = get_db_connection()
    if connection is None:
        logger.error("Database connection check failed.")
        return False
    
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        logger.info("Database connection is healthy.")
        return result is not None
    except Error as e:
        logger.error(f"Error checking database connection: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
