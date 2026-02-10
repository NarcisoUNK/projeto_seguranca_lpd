import socket
import threading
import os
from cryptography.fernet import Fernet

# Configurações
PORTA_PADRAO = 9999

# Caminho exato onde queres guardar a chave do chat
CAMINHO_CHAVE = os.path.join(os.path.dirname(__file__), "keys", "chat_secret.key")

class SecureChat:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.key = self.carregar_ou_criar_chave()
        self.cipher = Fernet(self.key)

    def carregar_ou_criar_chave(self):
       
        # Garante que a pasta keys existe
        pasta_keys = os.path.dirname(CAMINHO_CHAVE)
        if not os.path.exists(pasta_keys):
            os.makedirs(pasta_keys)

        # Se o ficheiro já existe, carrega-o
        if os.path.exists(CAMINHO_CHAVE):
            with open(CAMINHO_CHAVE, "rb") as f:
                return f.read()
        else:
            # Se não existe, gera uma nova e guarda
            print(f"\n[*] A gerar nova chave de encriptação para o Chat...")
            chave_nova = Fernet.generate_key()
            with open(CAMINHO_CHAVE, "wb") as f:
                f.write(chave_nova)
            print(f"[+] Chave guardada em: {CAMINHO_CHAVE}")
            return chave_nova

    def receive_messages(self, connection):
        """Ouve mensagens noutra thread"""
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
        """Modo Hospedeiro (Servidor)"""
        try:
            self.sock.bind(('0.0.0.0', PORTA_PADRAO))
            self.sock.listen(1)
            print(f"\n[+] À espera de conexão na porta {PORTA_PADRAO}...")
            print(f"    (Partilha o ficheiro 'chat_secret.key' com o cliente!)")
            
            conn, addr = self.sock.accept()
            print(f"[+] Conectado com: {addr}")
            
            threading.Thread(target=self.receive_messages, args=(conn,), daemon=True).start()
            self.send_loop(conn)
        except Exception as e:
            print(f"[!] Erro no servidor: {e}")

    def start_client(self, target_ip):
        """Modo Convidado (Cliente)"""
        try:
            print(f"[*] A conectar a {target_ip}...")
            self.sock.connect((target_ip, PORTA_PADRAO))
            print("[+] Conectado! A comunicação é encriptada.")
            
            threading.Thread(target=self.receive_messages, args=(self.sock,), daemon=True).start()
            self.send_loop(self.sock)
        except Exception as e:
            print(f"[!] Erro na conexão: {e}")

    def send_loop(self, connection):
        print("\n--- CHAT SEGURO (AES) ---")
        print("Escreve 'sair' para terminar.\n")
        
        while True:
            msg = input("Eu: ")
            if msg.lower() == 'sair':
                break
            
            encrypted = self.cipher.encrypt(msg.encode())
            try:
                connection.send(encrypted)
            except:
                print("[!] Falha ao enviar.")
                break
        connection.close()

    def menu(self):
        print("\n=== CHAT P2P (ENCRIPTADO) ===")
        print("[1] Hospedar (Servidor)")
        print("[2] Conectar (Cliente)")
        print("[0] Voltar")
        
        op = input("Opção: ")
        if op == "1":
            self.start_server()
        elif op == "2":
            ip = input("IP do Alvo: ")
            self.start_client(ip)