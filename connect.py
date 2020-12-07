import mysql.connector
from mysql.connector import errorcode

# Construct connection string
def open(conn):
    try:
        print('Connection established.')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Something is wrong with the username or password.')
            exit(1)
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('Database does not exist.')
            exit(1)
        else:
            print(err)
    else:
        cursor = conn.cursor()

    return cursor
