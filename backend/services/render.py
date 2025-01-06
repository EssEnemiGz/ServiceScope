"""
This micro service send data to frontend.
By: EssEnemiGz
"""

from flask import Blueprint, session, jsonify
from flask_cors import CORS
import common.db_manager as db_manager
import psycopg2

render_bp = Blueprint('Render Service', __name__)
db = db_manager.get_db_connection()
CORS(render_bp, supports_credentials=True)

@render_bp.route("/api/data/realtime", methods=["GET"])
def realtime_data():
    global db
    user_id = session.get("id")
    
    if not user_id:
        return jsonify({"error": "User not logged in"}), 401 
    
    cursor = db.cursor()
    try:
        cursor.execute("SELECT cpu_usage, ram_percentage, ram_gb, created_at FROM system_logs WHERE user_id = %s;", (user_id,))
    except psycopg2.errors.InFailedSqlTransaction:
        db = db_manager.get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT cpu_usage, ram_percentage, ram_gb, created_at FROM system_logs WHERE user_id = %s;", (user_id,))
        
    result = cursor.fetchall()

    if not result:
        return jsonify([])
    
    data = [
        {
            "cpu_usage": row[0],
            "ram_percentage": row[1],
            "ram_gb": row[2],
            "created_at": row[3].strftime('%d %b %Y %H:%M')
        }
        for row in result
    ]
    
    return jsonify(data)