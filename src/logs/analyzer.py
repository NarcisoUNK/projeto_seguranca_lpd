import re
import os
import requests
from collections import Counter

def get_ip_location(ip):
    """Consulta API pública para obter país de origem."""
    if ip.startswith(("192.168.", "10.", "127.")):
        return "Local Network"
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,country,countryCode"
        response = requests.get(url, timeout=2)
        data = response.json()
        if data['status'] == 'success':
            return f"{data['country']} ({data['countryCode']})"
    except:
        pass
    return "Desconhecido"

def analyze_ssh(filepath):
    print(f"\n[*] A analisar SSH: {filepath}")
    if not os.path.exists(filepath):
        print("[!] Log não encontrado. Gere os logs primeiro.")
        return

    failed_ips = []
    with open(filepath, "r") as f:
        for line in f:
            if "Failed password" in line:
                # Regex para apanhar o IP
                ip_match = re.search(r'from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
                if ip_match:
                    failed_ips.append(ip_match.group(1))

    print(f"-> Tentativas de Intrusão: {len(failed_ips)}")
    
    if failed_ips:
        print("\n[!] Top 3 Origens de Ataques:")
        # Usa Counter para contar repetições
        for ip, count in Counter(failed_ips).most_common(3):
            print(f"    IP: {ip} | País: {get_ip_location(ip)} | Tentativas: {count}")

def analyze_http(filepath):
    print(f"\n[*] A analisar HTTP: {filepath}")
    if not os.path.exists(filepath):
        print("[!] Log não encontrado.")
        return
        
    count_404 = 0
    with open(filepath, "r") as f:
        lines = f.readlines()
        for line in lines:
            if ' " 404 ' in line:
                count_404 += 1
    print(f"-> Total de pedidos: {len(lines)}")
    print(f"-> Erros 404: {count_404}")

def menu():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ssh_log = os.path.join(base_dir, "dummy_ssh.log")
    http_log = os.path.join(base_dir, "dummy_http.log")
    
    while True:
        print("\n=== ANÁLISE DE LOGS ===")
        print("[1] Gerar Logs de Teste")
        print("[2] Analisar SSH (Auth)")
        print("[3] Analisar HTTP (Web)")
        print("[0] Voltar")
        
        op = input("Opção: ")
        if op == '1':
            import logs.log_test_gen as gen
            gen.generate_ssh_logs()
            gen.generate_http_logs()
        elif op == '2':
            analyze_ssh(ssh_log)
        elif op == '3':
            analyze_http(http_log)
        elif op == '0':
            break