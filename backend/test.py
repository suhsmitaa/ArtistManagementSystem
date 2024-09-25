from utils.db import get_db_connection


connection = get_db_connection()

if connection:
    print("working mysql")
else:
    print("Not Working")