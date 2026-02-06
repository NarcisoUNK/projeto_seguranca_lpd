import socket
from datetime import datetime

def scan_ports(target, start_port, end_port):
    """
    Realiza um scan TCP Connect simples num intervalo de portos.
    Retorna uma lista dos portos abertos.
    """
    print("-" * 60)
    print(f"[*] A iniciar scan ao alvo: {target}")
    print(f"[*] A verificar portos: {start_port} a {end_port}")
    print(f"[*] Inicio: {datetime.now().strftime('%H:%M:%S')}")
    print("-" * 60)

    open_ports = []
    
    try:
        # Tenta resolver o IP (ex: converte google.com em 142.250.x.x)
        target_ip = socket.gethostbyname(target)
        print(f"[*] IP Alvo: {target_ip}\n")
    except socket.gaierror:
        print("[!] Erro: Não foi possível resolver o hostname.")
        return []

    try:
        for port in range(start_port, end_port + 1):
            # Cria o socket (IPv4, TCP)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(0.5) # Timeout rápido (0.5s)
            
            # Tenta conectar. connect_ex retorna 0 se sucesso
            result = sock.connect_ex((target_ip, port))
            
            if result == 0:
                print(f"[+] Porto {port} -> ABERTO")
                open_ports.append(port)
            
            sock.close()

    except KeyboardInterrupt:
        print("\n[!] Scan interrompido pelo utilizador.")
    except socket.error:
        print("\n[!] Erro ao conectar ao servidor.")

    print("-" * 60)
    print(f"[*] Scan terminado.")
    return open_ports 