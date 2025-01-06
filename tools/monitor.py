import requests
import logging
import psutil
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
        print(f"Error al realizar la solicitud: {e}")
        return None

def check_status(url, method="GET", **kwargs):
    try:
        r = make_request(url, method, **kwargs)
        data = {
            "service":url,
            "response_time":r.elapsed.total_seconds(),
            "status_code":r.status_code
        }
        return data
    except Exception as e:
        logging.error(e)
        return -1

def main():
    while 1:
        f = open(f"{actual_dir}/config.json", "r")
        data = json.loads(f.read())
        f.close()

        logs = {
            "routes":[],
            "cpu":0,
            "ram_percentege":0,
            "ram_gb":0
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

        logs["cpu"] = cpu_usage
        logs["ram_percentege"] = memory_usage
        logs["ram_gb"] = f"{memory_gb:.2f}"
        logging.info(logs)
        time.sleep(10)

with daemon.DaemonContext(stderr=open('error.log', 'w+')):
    logging.basicConfig(
        filename=f"{actual_dir}/monitor.log",
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    logging.info("El daemon ha iniciado.")
    main()