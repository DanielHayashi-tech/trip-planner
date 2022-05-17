import mysql.connector
from mysql.connector import Error

# create a connection to mysql db
def create_connection(hostname, username, userpw, dbname):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=hostname,
            user=username,
            password=userpw,
            database=dbname
        )
        print("connection was successful")
        # check for any errors after trying to connect and if you find, return error as 'e'
    except Error as e:
        print(f"returned '{e}'")
    return connection

# function that will execute my sql queries
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
        # check for any errors after trying to connect and if you find, return error as 'e'
    except Error as e:
        print(f"The error '{e}' occurred")

# function that will read my sql queries
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = []
    try:
        cursor.execute(query)
        table = cursor.fetchall()
        columnNames = [column[0] for column in cursor.description]
        for record in table:
            result.append(dict(zip(columnNames, record )))
        return result
    except Error as e:
        print(f"The error '{e}' occurred")





