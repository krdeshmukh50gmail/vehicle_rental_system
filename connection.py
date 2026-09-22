import mysql.connector


def create_connection():

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="2829",
        database="vehicle_rental_db"
    )

    return connection


connection = create_connection()

if connection.is_connected():
    print("MySQL Database Connected Successfully!")

