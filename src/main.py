import sys
import os

# Função para limpar o ecrã (funciona em Windows e Linux)
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
        print("\n[1] Ferramentas de Rede (Scanner, Floods)")
        print("[2] Análise de Logs e Geolocalização")
        print("[3] Segurança (Password Manager, Chat)")
        print("[4] Relatórios e Base de Dados")
        print("[0] Sair")
        
        try:
            choice = input("\nEscolha uma opção: ")
            
            if choice == '1':
                print("\n>> A implementar módulo de rede...")
                input("Enter para continuar...")
            elif choice == '2':
                print("\n>> A implementar módulo de logs...")
                input("Enter para continuar...")
            elif choice == '3':
                print("\n>> A implementar módulo de segurança...")
                input("Enter para continuar...")
            elif choice == '4':
                print("\n>> A implementar relatórios...")
                input("Enter para continuar...")
            elif choice == '0':
                print("\nA sair...")
                sys.exit()
            else:
                print("\n[!] Opção inválida.")
                input("Enter para continuar...")
        except KeyboardInterrupt:
            print("\n\nOperação cancelada.")
            sys.exit()

if __name__ == "__main__":
    main_menu()