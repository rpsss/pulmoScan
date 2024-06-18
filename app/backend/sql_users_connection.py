from dotenv import load_dotenv
import os
from google.cloud.sql.connector import Connector, IPTypes
import pymysql.cursors
import bcrypt

load_dotenv()

# Fetch environment variables
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

# Database connection function
def get_db_connection():
    instance_connection_name = "pulmoscanai:europe-west9:pulmoscanai"
    connector = Connector(IPTypes.PUBLIC)
    conn = connector.connect(
            instance_connection_name,
            "pymysql",
            user=DB_USER,
            password=DB_PASSWORD,
            db=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor  # Use DictCursor here
        )
    return conn

print(get_db_connection())

def verify_user(username, password):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return True
    return False

# Password hashing function
def hash_password(password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

# Function to insert a new user
def add_user(username, password):
    hashed_password = hash_password(password)
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
    connection.commit()
    
    cursor.close()
    connection.close()

def save_image_to_db(image_data, label):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("INSERT INTO image_labels (image_data, label) VALUES (%s, %s)", (image_data, label))
    connection.commit()

    cursor.close()
    connection.close()

