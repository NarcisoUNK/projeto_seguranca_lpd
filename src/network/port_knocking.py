import socket
import time

def knock(target_ip, ports, delay=0.5, protocol='TCP'):
    """
    Envia pacotes para uma sequência de portos (Port Knocking).
    :param ports: Lista de portos (ex: [7000, 8000, 9000])
    """
    print("-" * 60)
    print(f"[*] A iniciar Port Knocking: {target_ip}")
    print(f"[*] Sequência: {ports}")
    print("-" * 60)

    try:
        for port in ports:
            port = int(port)
            print(f"[*] Knock -> Porto {port}...", end="")
            
            if protocol.upper() == 'UDP':
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(b'', (target_ip, port))
            else:
                # TCP Connect Scan como 'batida'
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.1)
                sock.connect_ex((target_ip, port))
            
            sock.close()
            print(" [OK]")
            time.sleep(delay)
            
        print("-" * 60)
        print("[+] Sequência terminada. Tente aceder via SSH agora.")
        
    except Exception as e:
        print(f"\n[!] Erro: {e}")