import http.server
import socketserver
from datetime import datetime
import os
import time
import socket
import fcntl
import struct
import glob

# Funções de coleta de informações do sistema

def get_system_time():
    """Retorna a data e hora atual do sistema"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_uptime():
    """Retorna o uptime do sistema em segundos"""
    with open('/proc/uptime', 'r') as f:
        return float(f.readline().split()[0])

def get_cpu_model_speed():
    """Retorna o modelo e a velocidade da CPU"""
    model = ""
    speed = ""
    with open('/proc/cpuinfo', 'r') as f:
        for line in f:
            if "model name" in line:
                model = line.split(":")[1].strip()
            if "cpu MHz" in line:
                speed = line.split(":")[1].strip() + " MHz"
                break
    return model, speed

def get_cpu_usage():
    """Retorna o uso da CPU (%)"""
    with open('/proc/stat', 'r') as f:
        first_line = f.readline().split()
        total_time_1 = sum(int(value) for value in first_line[1:])
        idle_time_1 = int(first_line[4])

    time.sleep(0.5)

    with open('/proc/stat', 'r') as f:
        first_line = f.readline().split()
        total_time_2 = sum(int(value) for value in first_line[1:])
        idle_time_2 = int(first_line[4])

    total_time_delta = total_time_2 - total_time_1
    idle_time_delta = idle_time_2 - idle_time_1

    cpu_usage = 100 * (1 - (idle_time_delta / total_time_delta))
    return round(cpu_usage, 2)

def get_memory_info():
    """Retorna a memória total e usada (MB)"""
    with open('/proc/meminfo', 'r') as f:
        mem_info = f.read()

    mem_total = int([line for line in mem_info.split('\n') if "MemTotal" 
in line][0].split()[1]) // 1024
    mem_free = int([line for line in mem_info.split('\n') if "MemFree" in 
line][0].split()[1]) // 1024
    mem_used = mem_total - mem_free

    return mem_total, mem_used

def get_system_version():
    """Retorna a versão do sistema"""
    with open('/proc/version', 'r') as f:
        return f.readline().strip()

def get_running_processes():
    """Retorna uma lista de processos em execução (PID e nome)"""
    processes = []
    for pid in os.listdir('/proc'):
        if pid.isdigit():
            try:
                with open(f'/proc/{pid}/comm', 'r') as f:
                    processes.append((pid, f.readline().strip()))
            except FileNotFoundError:
                continue
    return processes

def get_disk_info():
    """Retorna a lista de partições de disco"""
    partitions = []
    with open('/proc/partitions', 'r') as f:
        for line in f.readlines()[2:]:
            partitions.append(line.split()[-1])
    return partitions

def get_usb_devices():
    """Retorna a lista de dispositivos USB conectados"""
    devices = []
    usb_devices = glob.glob('/sys/bus/usb/devices/*')
    for device in usb_devices:
        try:
            with open(f'{device}/product', 'r') as f:
                devices.append((device.split('/')[-1], 
f.readline().strip()))
        except FileNotFoundError:
            continue
    return devices

def get_ip_address(ifname):
    """Retorna o endereço IP do adaptador de rede"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,
        struct.pack('256s', ifname[:15].encode('utf-8'))
    )[20:24])

def get_network_interfaces():
    """Retorna uma lista de adaptadores de rede e seus IPs"""
    interfaces = []
    for ifname in os.listdir('/sys/class/net/'):
        try:
            ip = get_ip_address(ifname)
            interfaces.append((ifname, ip))
        except OSError:
            continue
    return interfaces

# Classe para servir a página HTML com as informações do sistema

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Coleta de informações do sistema
            cpu_model, cpu_speed = get_cpu_model_speed()
            uptime = get_uptime()
            cpu_usage = get_cpu_usage()
            mem_total, mem_used = get_memory_info()
            version = get_system_version()
            processes = get_running_processes()
            disks = get_disk_info()
            usb_devices = get_usb_devices()
            network_interfaces = get_network_interfaces()

            html_content = f"""
            <html>
            <head>
                <title>Informacoes do Sistema</title>
                <style>
                    body {{ font-family: Arial, sans-serif; }}
                    table {{ border-collapse: collapse; width: 100%; }}
                    th, td {{ padding: 8px 12px; border: 1px solid #ddd; 
}}
                </style>
            </head>
            <body>
                <h1>Informacoes do Sistema</h1>
                <p><b>Data e Hora:</b> {get_system_time()}</p>
                <p><b>Uptime:</b> {uptime} segundos</p>
                <p><b>Modelo da CPU:</b> {cpu_model} ({cpu_speed})</p>
                <p><b>Uso da CPU:</b> {cpu_usage}%</p>
                <p><b>Memoria Total:</b> {mem_total} MB</p>
                <p><b>Memoria Usada:</b> {mem_used} MB</p>
                <p><b>Versao do Sistema:</b> {version}</p>

                <h2>Processos em Execucao</h2>
                <table>
                    <tr><th>PID</th><th>Nome</th></tr>
                    {"".join([f"<tr><td>{pid}</td><td>{name}</td></tr>" 
for pid, name in processes])}
                </table>

                <h2>Particoes de Disco</h2>
                <ul>
                    {"".join([f"<li>{disk}</li>" for disk in disks])}
                </ul>

                <h2>Dispositivos USB</h2>
                <ul>
                    {"".join([f"<li>{port} - {name}</li>" for port, name 
in usb_devices])}
                </ul>

                <h2>Adaptadores de Rede e IPs</h2>
                <ul>
                    {"".join([f"<li>{iface}: {ip}</li>" for iface, ip in 
network_interfaces])}
                </ul>
            </body>
            </html>
            """

            # Resposta HTTP
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html_content.encode("utf-8"))
        else:
            # Se a URL não for a raiz, exibe o comportamento padrão
            super().do_GET()

# Configurar o servidor
PORT = 8000
Handler = MyRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Servidor rodando na porta {PORT}")
    httpd.serve_forever()

