"""
This micro service manage the session section, like login and register.
By: EssEnemiGz
"""

from flask import Blueprint, request, abort, session, jsonify
from werkzeug.security import generate_password_hash
import common.db_manager as db_manager
import common.session_manager as session_manager

sessions_bp = Blueprint('Sessions Service', __name__)
db = db_manager.get_db_connection()

@sessions_bp.route("/api/session/login", methods=["POST"])
def login():
    try:
        password = request.form.get("password")
        email = request.form.get("email")
        
        if None in [password, email]:
            abort(400)
    except:
        abort(400)
    
    if not session_manager.check_existence(email):
        abort(404) # User not found
        
    if not session_manager.check_password(email, password):
        abort(401) # Wrong password
        
    user_id = session_manager.get_user_id(email)
    session['id'] = user_id
    session['email'] = email
    session.permanent = True
    
    return jsonify({"redirect":"/dashboard"})
    
@sessions_bp.route("/api/session/register", methods=["POST"])
def register():
    cursor = db.cursor()
    try:
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        
        if None in [username, password, email]:
            abort(400)
    except:
        abort(400)
    
    if session_manager.check_existence(email):
        abort(404) # User already exists
        
    password_hashed = generate_password_hash(password)
    query = "INSERT INTO users(username, password, email) VALUES(%s, %s, %s);"
    try:
        cursor.execute(query, (username, password_hashed, email))
        db.commit()
    except:
        abort(500)
        
    user_id = session_manager.get_user_id(email)
    session['id'] = user_id
    session['email'] = email
    session.permanent = True
    
    return jsonify({"redirect":"/dashboard"})