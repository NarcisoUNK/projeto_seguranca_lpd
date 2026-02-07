import sqlite3
import os

# Define o caminho da base de dados
DB_NAME = "seguranca_lpd.db"
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), DB_NAME)

def get_connection():
    """Cria conexão com a base de dados SQLite."""
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_db():
    """Inicializa as tabelas necessárias."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Tabela para o Password Manager
    # Guardamos tudo como BLOB (bytes) ou TEXT porque vai estar encriptado
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_name TEXT NOT NULL,
            username TEXT NOT NULL,
            encrypted_password BLOB NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"[*] Base de dados inicializada em: {DB_PATH}")

# Inicializa logo ao importar, para garantir que existe
init_db()