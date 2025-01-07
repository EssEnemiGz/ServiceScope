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
        # Obtener los datos de uso de CPU, RAM y tiempo
        cursor.execute("""
            SELECT cpu_usage, ram_percentage, ram_gb, created_at, network_upload, network_download, disk_total
            FROM system_logs 
            WHERE user_id = %s;
        """, (user_id,))
        system_logs = cursor.fetchall()

        # Obtener el uso de disco más reciente
        cursor.execute("""
            SELECT disk_usage, created_at 
            FROM system_logs 
            WHERE user_id = %s 
            ORDER BY created_at DESC 
            LIMIT 1;
        """, (user_id,))
        disk_usage = cursor.fetchone()

    except psycopg2.errors.InFailedSqlTransaction:
        db = db_manager.get_db_connection()
        cursor = db.cursor()

        cursor.execute("""
            SELECT cpu_usage, ram_percentage, ram_gb, created_at, network_upload, network_download, disk_total 
            FROM system_logs 
            WHERE user_id = %s;
        """, (user_id,))
        system_logs = cursor.fetchall()

        cursor.execute("""
            SELECT disk_usage, created_at 
            FROM system_logs 
            WHERE user_id = %s 
            ORDER BY created_at DESC 
            LIMIT 1;
        """, (user_id,))
        disk_usage = cursor.fetchone()

    # Procesar los datos de system_logs
    if not system_logs:
        return jsonify([])

    data = [
        {
            "cpu_usage": row[0],
            "ram_percentage": row[1],
            "ram_gb": row[2],
            "created_at": row[3].strftime('%d %b %Y %H:%M'),
            "network_upload": row[4],
            "network_download": row[5],
            "disk_total": row[6]
        }
        for row in system_logs
    ]

    if disk_usage:
        data[0].setdefault("disk_usage", disk_usage[0])
    else: 
        data[0].setdefault("disk_usage", 0)
    
    return jsonify(data)