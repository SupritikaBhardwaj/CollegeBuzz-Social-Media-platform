import mysql.connector

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="socialmedia",
            password="pass123",
            database="collegebuzz"
        )
        cursor = conn.cursor()
        return conn, cursor
    except Exception as e:
        print("Error connecting to MySQL:", e)
        return None, None
