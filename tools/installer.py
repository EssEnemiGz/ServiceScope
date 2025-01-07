import os
import subprocess

SERVICE_NAME = "monitor-daemon"
SERVICE_FILE = f"/etc/systemd/system/{SERVICE_NAME}.service"
SCRIPT_PATH = os.path.abspath("monitor_daemon.py")
LOG_DIR = os.path.dirname(SCRIPT_PATH)
MONITOR_LOG = os.path.join(LOG_DIR, "monitor.log")
ERROR_LOG = os.path.join(LOG_DIR, "error.log")

def check_root():
    """Check if the script is running as root."""
    if os.geteuid() != 0:
        print("Este instalador necesita privilegios de administrador. Ejecuta el script con 'sudo'.")
        exit(1)

def create_service_file():
    """Create the systemd service file."""
    service_content = f"""
[Unit]
Description=Monitor Daemon Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 {SCRIPT_PATH}
WorkingDirectory={LOG_DIR}
Restart=always
User={os.getenv('USER')}
Group={os.getenv('USER')}
StandardOutput=append:{MONITOR_LOG}
StandardError=append:{ERROR_LOG}

[Install]
WantedBy=multi-user.target
    """
    try:
        with open(SERVICE_FILE, "w") as f:
            f.write(service_content)
        print(f"Archivo de servicio creado: {SERVICE_FILE}")
    except Exception as e:
        print(f"Error al crear el archivo de servicio: {e}")
        exit(1)

def enable_service():
    """Enable the systemd service."""
    try:
        subprocess.run(["systemctl", "daemon-reload"], check=True)
        subprocess.run(["systemctl", "enable", SERVICE_NAME], check=True)
        print(f"Servicio {SERVICE_NAME} habilitado para iniciar al encender.")
    except subprocess.CalledProcessError as e:
        print(f"Error al habilitar el servicio: {e}")
        exit(1)

def start_service():
    """Start the systemd service."""
    try:
        subprocess.run(["systemctl", "start", SERVICE_NAME], check=True)
        print(f"Servicio {SERVICE_NAME} iniciado correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error al iniciar el servicio: {e}")
        exit(1)

def main():
    check_root()
    print("Iniciando instalación del daemon...")
    create_service_file()
    enable_service()
    start_service()
    print(f"Instalación completa. Logs: {MONITOR_LOG}, {ERROR_LOG}")

if __name__ == "__main__":
    main()