import os
import pyotp
import sys
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from database import db_manager

# --- GESTÃO DE CHAVES ASSIMÉTRICAS (RSA)  ---
KEY_DIR = os.path.join(os.path.dirname(__file__), "keys")

def generate_keys():
    """Gera par de chaves RSA (Pública e Privada) se não existirem."""
    if not os.path.exists(KEY_DIR):
        os.makedirs(KEY_DIR)
    
    private_path = os.path.join(KEY_DIR, "private.pem")
    public_path = os.path.join(KEY_DIR, "public.pem")

    if not os.path.exists(private_path):
        print("[*] A gerar chaves RSA de 2048 bits...")
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        
        # Guardar chave privada
        with open(private_path, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))

        # Guardar chave pública
        with open(public_path, "wb") as f:
            f.write(private_key.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

def load_keys():
    """Carrega as chaves do disco para memória."""
    generate_keys()
    with open(os.path.join(KEY_DIR, "private.pem"), "rb") as f:
        priv = serialization.load_pem_private_key(f.read(), password=None)
    with open(os.path.join(KEY_DIR, "public.pem"), "rb") as f:
        pub = serialization.load_pem_public_key(f.read())
    return priv, pub

# --- FUNÇÕES DE CRIPTOGRAFIA ---
def encrypt_pwd(password):
    _, public_key = load_keys()
    return public_key.encrypt(
        password.encode(),
        padding.OAEP(padding.MGF1(hashes.SHA256()), hashes.SHA256(), None)
    )

def decrypt_pwd(encrypted_data):
    private_key, _ = load_keys()
    return private_key.decrypt(
        encrypted_data,
        padding.OAEP(padding.MGF1(hashes.SHA256()), hashes.SHA256(), None)
    ).decode()

# --- 2FA (TOTP)  ---
# Segredo fixo apenas para demonstração académica
SECRET_2FA = "JBSWY3DPEHPK3PXP" 

def check_2fa():
    totp = pyotp.TOTP(SECRET_2FA)
    print(f"\n[DEMO] Código 2FA atual: {totp.now()}") # Mostra o código para facilitar testes
    code = input("Insira o código 2FA (6 dígitos): ")
    return totp.verify(code)

# --- MENUS ---
def add_entry():
    site = input("URL/Serviço: ")
    user = input("Username: ")
    pwd = input("Password: ")
    
    enc_pwd = encrypt_pwd(pwd)
    
    conn = db_manager.get_connection()
    conn.cursor().execute("INSERT INTO passwords (service_name, username, encrypted_password) VALUES (?, ?, ?)", 
                          (site, user, enc_pwd))
    conn.commit()
    conn.close()
    print("[+] Password encriptada e guardada.")

def list_entries():
    if not check_2fa():
        print("[!] Falha na autenticação 2FA.")
        return

    conn = db_manager.get_connection()
    rows = conn.cursor().execute("SELECT * FROM passwords").fetchall()
    conn.close()
    
    print("\n--- COFRE DE PASSWORDS ---")
    for row in rows:
        try:
            dec = decrypt_pwd(row[3])
            print(f"ID: {row[0]} | Site: {row[1]} | User: {row[2]} | Pass: {dec}")
        except:
            print(f"[Erro na desencriptação do ID {row[0]}]")

def menu():
    while True:
        print("\n=== PASSWORD MANAGER ===")
        print("[1] Adicionar Nova Password")
        print("[2] Consultar Passwords (2FA)")
        print("[0] Voltar")
        op = input("Opção: ")
        if op == '1': add_entry()
        elif op == '2': list_entries()
        elif op == '0': break