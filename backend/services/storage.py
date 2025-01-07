"""
This micro service store the data from users servers.
By: EssEnemiGz
"""

from flask import Blueprint, request, abort, Response
import common.session_manager as session
import common.db_manager as db_manager
from flask_cors import CORS
import json

storage_bp = Blueprint('Storage Service', __name__)
CORS(storage_bp, origins='*')

@storage_bp.route("/api/storage/add", methods=["POST"])
def storage_add():
    try:
        data = request.get_json()
        user_email = data.get("user_email")
        routes = data.get("routes")
        cpu_usage = data.get("cpu")
        ram_percentage = data.get("ram_percentage")
        ram_gb = data.get("ram_gb")
        disk_total = data.get("disk_total")
        disk_used = data.get("disk_used")
        network_upload = data.get("network_upload")
        network_download = data.get("network_download")
        
        for value in data.items():
            if value is None:
                abort(400)
            elif isinstance(value, str) and not value.strip():
                abort(400)
        
    except Exception as e:
        print(e)
        abort(400)
        
    try:
        user_id = session.get_user_id(user_email)
        
        db = db_manager.get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO system_logs(user_id, cpu_usage, ram_percentage, ram_gb, disk_usage, disk_total, network_upload, network_download) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);", (user_id, cpu_usage, ram_percentage, ram_gb, disk_used, disk_total, network_upload, network_download))
        
        for route in routes:
            url = route.get("url")
            method = route.get("method", "GET")
            headers = json.dumps(route.get("headers", {}))  # Convertir a JSON si es necesario
            params = json.dumps(route.get("params", {}))  # Convertir a JSON si es necesario
            data_payload = json.dumps(route.get("data", {}))  # Convertir a JSON si es necesario
            json_payload = json.dumps(route.get("json", {}))  # Convertir a JSON si es necesario
            response_time = route.get("response_time")
            status_code = route.get("status_code")

            cursor.execute("""
                INSERT INTO route_logs(user_id, url, method, headers, params, data, json_payload, response_time, status_code)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (user_id, url, method, headers, params, data_payload, json_payload, response_time, status_code))
        
        db.commit()
        cursor.close()
        db.close()
        
        return Response("DONE", status=200)
    except Exception  as e:
        print(e)
        user_id = session.get_user_id(user_email)
        
        db = db_manager.get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO system_logs(user_id, cpu_usage, ram_percentage, ram_gb, disk_usage, disk_total, network_upload, network_download) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);", (user_id, cpu_usage, ram_percentage, ram_gb, disk_used, disk_total, network_upload, network_download))
        
        for route in routes:
            url = route.get("url")
            method = route.get("method", "GET")
            headers = json.dumps(route.get("headers", {}))  # Convertir a JSON si es necesario
            params = json.dumps(route.get("params", {}))  # Convertir a JSON si es necesario
            data_payload = json.dumps(route.get("data", {}))  # Convertir a JSON si es necesario
            json_payload = json.dumps(route.get("json", {}))  # Convertir a JSON si es necesario
            response_time = route.get("response_time")
            status_code = route.get("status_code")

            cursor.execute("""
                INSERT INTO route_logs(user_id, url, method, headers, params, data, json_payload, response_time, status_code)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (user_id, url, method, headers, params, data_payload, json_payload, response_time, status_code))
        
        db.commit()
        cursor.close()
        db.close()
        
        return Response("DONE", status=200)
    
    abort(500)