import mysql.connector
from mysql.connector import Error
from config import DATABASE_CONFIG

# connecting to db
def get_db_connection():
    try:
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to mysql Database : {e}")
        return None


def execute_query(query,params=None):
    # connecting to db
    connection =get_db_connection()
    if connection is None:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        if params:
            cursor.execute(query,params)
        else:
            cursor.execute(query)
        
        if query.strip().upper().startswith("SELECT"):
            result =cursor.fetchall()
        else:
            connection.commit()
            result =cursor.rowcount

        return result
        
    except Error as e:
        print(f"Error in retrieving data : {e}")
        return None
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    


