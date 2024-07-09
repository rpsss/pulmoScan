from dotenv import load_dotenv
import os
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
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

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

def save_prediction(user_id, image_data, original_prediction):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute("INSERT INTO predictions (user_id, image_data, original_prediction) VALUES (%s, %s, %s)",
                   (user_id, image_data, original_prediction))
    connection.commit()
    
    cursor.close()
    connection.close()

def update_prediction(user_id, image_data, final_prediction):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute("UPDATE predictions SET final_prediction = %s, modified = TRUE WHERE user_id = %s AND image_data = %s",
                   (final_prediction, user_id, image_data))
    connection.commit()
    
    cursor.close()
    connection.close()

def get_user_predictions(user_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM predictions WHERE user_id = %s", (user_id,))
    predictions = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return predictions

# Function to get user ID based on username
def get_user_id(username):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    if user:
        return user['id']
    return None
