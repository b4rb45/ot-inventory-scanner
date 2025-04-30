import socket
import ipaddress
import threading
import queue
import sys
import time
import struct
import random
import os

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

def banner():
    print(f"{CYAN}")
    print("""
 ____  _             _      
| __ )| | __ _ _ __ | | __  
|  _ \| |/ _` | '_ \| |/ /  
| |_) | | (_| | | | |   <   
|____/|_|\__,_|_| |_|_|\\_\\ 

        b4rb45 SCADA Scanner
    """)
    print(f"{RESET}")

def load_ports(file_path):
    ports = {}
    try:
        with open(file_path, 'r') as f:
            for line in f:
                if ',' in line:
                    port, name = line.strip().split(',', 1)
                    ports[int(port)] = name.strip()
    except Exception as e:
        print(f"{RED}[!] Error cargando {file_path}: {e}{RESET}")
    return ports

def detect_honeypot(ip, port, response_time):
    return response_time < 0.05

def scan_tcp(ip, port, name, stealth):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        start = time.time()
        result = sock.connect_ex((ip, port))
        elapsed = time.time() - start
        if result == 0:
            banner = fingerprint_tcp(ip, port)
            return (port, name, banner, detect_honeypot(ip, port, elapsed))
    except:
        pass
    finally:
        sock.close()
    if stealth:
        time.sleep(random.uniform(0.2, 1.5))
    return None

def fingerprint_tcp(ip, port):
    try:
        if port == 502:
            s = socket.socket()
            s.settimeout(2)
            s.connect((ip, port))
            s.send(b"\x00\x01\x00\x00\x00\x06\xFF\x2B\x0E\x01\x00")
            r = s.recv(256)
            return "Modbus responde" if r else "Sin respuesta Modbus"
        elif port == 44818:
            s = socket.socket()
            s.settimeout(2)
            s.connect((ip, port))
            encap = struct.pack("<HHII8sI", 0x0063, 0, 0, 0, b'\x00'*8, 0)
            s.sendall(encap)
            resp = s.recv(512)
            return "EtherNet/IP activo" if resp else "No responde EtherNet/IP"
        return "Puerto abierto"
    except:
        return None


def scan_udp(ip, port, name):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)
        if port == 47808:
            payload = b"\x81\x0b\x00\x0c\x01\x20\xff\xff\x00\xff\xff\xff\xff"
            sock.sendto(payload, (ip, port))
            data, _ = sock.recvfrom(512)
            return (port, name, "BACnet activo", False)
    except:
        pass
    return None

def scan_host(ip, tcp_ports, udp_ports, stealth, udp_scan, output):
    found = []
    for port, name in tcp_ports.items():
        result = scan_tcp(ip, port, name, stealth)
        if result:
            found.append(result)
    if udp_scan:
        for port, name in udp_ports.items():
            result = scan_udp(ip, port, name)
            if result:
                found.append(result)
    if found:
        output.put((ip, found))

def thread_scan(hosts, tcp_ports, udp_ports, max_threads, stealth, udp_scan):
    output = queue.Queue()
    threads = []
    for ip in hosts:
        t = threading.Thread(target=scan_host, args=(ip, tcp_ports, udp_ports, stealth, udp_scan, output))
        t.start()
        threads.append(t)
        while threading.active_count() > max_threads:
            time.sleep(0.1)
    for t in threads:
        t.join()
    return list(output.queue)

def main():
    banner()
    segment = input("Segmento CIDR o IP: ").strip()
    try:
        hosts = [str(ip) for ip in ipaddress.ip_network(segment, strict=False).hosts()]
    except:
        print(f"{RED}[!] Segmento inválido{RESET}")
        return

    stealth = input("¿Activar modo stealth? (s/n): ").strip().lower() == 's'
    udp_scan = input("¿Incluir escaneo UDP? (s/n): ").strip().lower() == 's'
    try:
        max_threads = int(input("Máximo de hilos (ej: 50): ").strip())
    except:
        max_threads = 50

    tcp_ports = load_ports("ot_ports_tcp.txt")
    udp_ports = load_ports("ot_ports_udp.txt") if udp_scan else {}

    print(f"\n[*] Escaneando {len(hosts)} hosts con {max_threads} hilos...")
    results = thread_scan(hosts, tcp_ports, udp_ports, max_threads, stealth, udp_scan)

    for ip, services in results:
        print(f"\n{CYAN}[+] {ip}{RESET}")
        for port, name, banner, honeypot in services:
            tag = " [Posible Honeypot]" if honeypot else ""
            print(f"    - Puerto {port}: {name} ({banner}){tag}")

if __name__ == '__main__':
    main()
