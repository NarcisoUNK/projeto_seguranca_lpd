import sys
import os

# Adiciona o diretório atual ao path para garantir que encontra os módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from network import scanner  # Importa o nosso novo módulo

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear_screen()
    print("=" * 60)
    print("     APLICAÇÃO DE SEGURANÇA INFORMÁTICA - LPD 2025/2026")
    print("=" * 60)
    print(f"Aluno: NarcisoUNK (24473)")
    print("-" * 60)

def main_menu():
    while True:
        print_header()
        print("\n=== MENU PRINCIPAL ===")
        print("[1] Ferramentas de Rede (Scanner, Floods)")
        print("[2] Análise de Logs e Geolocalização")
        print("[3] Segurança (Password Manager, Chat Seguro)")
        print("[4] Relatórios e Base de Dados")
        print("[0] Sair")
        
        try:
            choice = input("\nEscolha uma opção: ")
            
            if choice == '1':
                print("\n=== PORT SCANNER ===")
                target = input("Alvo (IP ou domínio, ex: scanme.nmap.org): ")
                try:
                    p_start = int(input("Porto Inicial (ex: 20): "))
                    p_end = int(input("Porto Final (ex: 80): "))
                    
                    # Chama a função do nosso ficheiro scanner.py
                    scanner.scan_ports(target, p_start, p_end)
                    
                except ValueError:
                    print("[!] Erro: Os portos devem ser números inteiros.")
                
                input("\nPressione ENTER para voltar...")

            elif choice == '2':
                print("\n>> [Em Desenvolvimento] Módulo de Logs...")
                input("Pressione ENTER para voltar...")
            elif choice == '3':
                print("\n>> [Em Desenvolvimento] Módulo de Segurança...")
                input("Pressione ENTER para voltar...")
            elif choice == '4':
                print("\n>> [Em Desenvolvimento] Módulo de Relatórios...")
                input("Pressione ENTER para voltar...")
            elif choice == '0':
                print("\nA sair...")
                sys.exit()
            else:
                print("\n[!] Opção inválida.")
                input("Tentar novamente...")
        except KeyboardInterrupt:
            print("\nCancelado.")
            sys.exit()

if __name__ == "__main__":
    main_menu()