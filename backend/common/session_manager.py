from common.db_manager import get_db_connection
from werkzeug.security import check_password_hash

db = get_db_connection()

def check_existence(email):
    cursor = db.cursor()
    
    query = "SELECT email FROM users WHERE email = %s;"
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    cursor.close()

    return result is not None

def check_password(email, password):
    cursor = db.cursor()
    
    query = "SELECT password FROM users WHERE email = %s;"
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    cursor.close()
    
    if check_password_hash(result[0], password):
        return True
    
    return False

def get_user_id(email):
    cursor = db.cursor()
    
    query = "SELECT id FROM users WHERE email = %s;"
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    cursor.close()
    
    return result[0]