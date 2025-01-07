import requests
import logging
import psutil
import shutil
import daemon
import json
import time
import os

actual_dir = os.path.dirname(os.path.abspath(__file__))

def make_request(url, method, **kwargs):
    """
    Do a HTTP request with the arguments and parameters.

    Args:
        method (str): The HTTP method (GET, POST, PUT, DELETE, etc.).
        url (str): The request URL.
        **kwargs: Additional arguments for `requests.request`, like headers, data, json, params, etc.

    Returns:
        requests.Response: HTTP request response.
    """
    try:
        method = method.upper()
        response = requests.request(method, url, **kwargs)
        return response
    except requests.RequestException as e:
        logging.error(f"Error al realizar la solicitud: {e}")
        return 500

def check_status(url, method="GET", **kwargs):
    try:
        r = make_request(url, method, **kwargs)
        if r is None:
            return None
        return {
            "url": url,
            "method": method,
            "headers": kwargs.get("headers", {}),
            "params": kwargs.get("params", {}),
            "data": kwargs.get("data", {}),
            "json_payload": kwargs.get("json", {}),
            "response_time": r.elapsed.total_seconds(),
            "status_code": r.status_code,
        }
    except Exception as e:
        logging.error(f"Error al verificar el estado: {e}")
        return None

def main():
    while 1:
        f = open(f"{actual_dir}/config.json", "r")
        data = json.loads(f.read())
        f.close()
        
        logs = {
            "routes":[],
            "cpu":0,
            "ram_percentege":0,
            "ram_gb":0,
            "user_email":data.get("user_email", "")
        }

        routes = data.get("routes", [])

        for route in routes:
            url = route.get("url")
            method = route.get("method", "GET")
            headers = route.get("headers", {})
            params = route.get("params", {})
            data = route.get("data", {})
            json_payload = route.get("json", {})
            
            result = check_status(
                method=method,
                url=url,
                headers=headers,
                params=params,
                data=data,
                json=json_payload,
                timeout=5
            )
            if result == -1:
                continue
                
            logs["routes"].append(result)
            
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        memory_usage = memory_info.percent
        memory_gb = memory_info.used / (1024 ** 3)
        net_io = psutil.net_io_counters()
        network_upload = net_io.bytes_sent / (1024 ** 2)
        network_download = net_io.bytes_recv / (1024 ** 2)

        total, used, free = shutil.disk_usage("/")
        disk_total = total / (1024 ** 3)
        disk_used = used / (1024 ** 3)

        logs["cpu"] = cpu_usage
        logs["ram_percentage"] = memory_usage
        logs["ram_gb"] = f"{memory_gb:.2f}"
        logs["disk_total"] = round(disk_total, 2)
        logs["disk_used"] = round(disk_used, 2)
        logs["network_upload"] = round(network_upload, 2)
        logs["network_download"] = round(network_download, 2)
        logging.info(logs)
        
        response = requests.post("http://127.0.0.1:5555/api/storage/add", headers={"Content-Type":"application/json"}, json=logs)
        if response == 500:
            logging.error("Falló el envío de los datos al servidor, código de estado: Desconocido", "Información recibida: VACIO")
        elif response.status_code != 200:
            logging.error("Falló el envío de los datos al servidor, código de estado: ", response.status_code, "Información recibida: ", response.text)
            
        time.sleep(10)

with daemon.DaemonContext(stderr=open('error.log', 'w+')):
    logging.basicConfig(
        filename=f"{actual_dir}/monitor.log",
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    logging.info("El daemon ha iniciado.")
    main()