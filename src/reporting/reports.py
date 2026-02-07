import csv
import os
from datetime import datetime

REPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "reports")

def ensure_dir():
    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR)

def export_csv(filename, headers, data):
    """
    Gera um ficheiro CSV com os dados fornecidos.
    data: lista de listas ou tuplos
    """
    ensure_dir()
    filepath = os.path.join(REPORT_DIR, filename)
    
    try:
        with open(filepath, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(data)
        print(f"[+] Relatório CSV gerado: {filepath}")
        return True
    except Exception as e:
        print(f"[!] Erro ao gerar CSV: {e}")
        return False