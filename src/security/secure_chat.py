import socket
import threading
import os
from cryptography.fernet import Fernet

# Configurações
PORTA_PADRAO = 9999

# Tenta encontrar a chave em locais comuns
PATHS_POSSIVEIS = [
    "data/secret.key",
    "src/security/keys/secret.key",
    "secret.key"
]

class SecureChat:
    def __init__(self):
        self.key = self.load_key()
        if self.key:
            self.cipher = Fernet(self.key)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def load_key(self):
        for path in PATHS_POSSIVEIS:
            if os.path.exists(path):
                return open(path, "rb").read()
        
        print("\n[!] ERRO CRÍTICO: Chave de encriptação não encontrada!")
        print("    Corre primeiro o Password Manager para gerar a chave.")
        return None

    def receive_messages(self, connection):
        while True:
            try:
                data = connection.recv(1024)
                if not data: break
                
                # Desencripta a mensagem recebida
                msg = self.cipher.decrypt(data).decode()
                print(f"\n[Amigo]: {msg}\nEu: ", end="")
            except:
                break
        connection.close()

    def start_server(self):
        try:
            self.sock.bind(('0.0.0.0', PORTA_PADRAO))
            self.sock.listen(1)
            print(f"\n[+] À espera de conexão na porta {PORTA_PADRAO}...")
            
            conn, addr = self.sock.accept()
            print(f"[+] Conectado com: {addr}")
            
            # Thread para ouvir sem bloquear
            threading.Thread(target=self.receive_messages, args=(conn,), daemon=True).start()
            self.send_loop(conn)
        except Exception as e:
            print(f"[!] Erro no servidor: {e}")

    def start_client(self, target_ip):
        try:
            print(f"[*] A conectar a {target_ip}...")
            self.sock.connect((target_ip, PORTA_PADRAO))
            print("[+] Conectado! A comunicação é encriptada.")
            
            # Thread para ouvir sem bloquear
            threading.Thread(target=self.receive_messages, args=(self.sock,), daemon=True).start()
            self.send_loop(self.sock)
        except Exception as e:
            print(f"[!] Erro na conexão: {e}")

    def send_loop(self, connection):
        print("\n--- CHAT SEGURO INICIADO ---")
        print("Escreve 'sair' para terminar.\n")
        
        while True:
            msg = input("Eu: ")
            if msg.lower() == 'sair':
                break
            
            if self.key:
                # Encripta antes de enviar
                encrypted = self.cipher.encrypt(msg.encode())
                try:
                    connection.send(encrypted)
                except:
                    print("[!] Falha ao enviar.")
                    break
        connection.close()

    def menu(self):
        if not self.key: return

        print("\n=== CHAT P2P (ENCRIPTADO AES) ===")
        print("[1] Hospedar (Servidor)")
        print("[2] Conectar (Cliente)")
        print("[0] Voltar")
        
        op = input("Opção: ")
        if op == "1":
            self.start_server()
        elif op == "2":
            ip = input("IP do Alvo: ")
            self.start_client(ip)