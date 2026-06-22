import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_actual_password",  # 👉 change this
        database="flutter_app"
    )
    return connection
