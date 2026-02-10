import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from network import scanner
from network import dos_attacks
from network import port_knocking
from security import pass_manager
from security import secure_chat 
from logs import analyzer       
from reporting import reports   

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear_screen()
    print("=" * 60)
    print("     APLICAÇÃO DE SEGURANÇA INFORMÁTICA - LPD 2025/2026")
    print("=" * 60)
    print(f"Aluno: Rafael Narciso (24473)")
    print("-" * 60)

def network_menu():
    while True:
        print("\n--- FERRAMENTAS DE REDE ---")
        print("[1] Port Scanner (TCP Connect)")
        print("[2] UDP Flood (DoS)")
        print("[3] SYN Flood (TCP SYN Packets)")
        print("[4] Port Knocking (Cliente SSH)")
        print("[0] Voltar ao Menu Principal")
        
        opt = input("\nEscolha uma opção: ")

        if opt == '1':
            target = input("Alvo (IP/Domínio): ")
            try:
                start = int(input("Porto Inicial: "))
                end = int(input("Porto Final: "))
                scanner.scan_ports(target, start, end)
            except ValueError:
                print("[!] Erro: Portos devem ser números.")
            input("\nPressione ENTER para continuar...")

        elif opt == '2':
            target = input("Alvo (IP): ")
            try:
                port = int(input("Porto Alvo (ex: 80, 53): "))
                duration = int(input("Duração (segundos): "))
                dos_attacks.udp_flood(target, port, duration)
            except ValueError:
                print("[!] Erro: Valores inválidos.")
            input("\nPressione ENTER para continuar...")
                
        elif opt == '3':
            print("\n[!] NOTA: Este ataque requer privilégios de Administrador.")
            target = input("Alvo (IP): ")
            try:
                port = int(input("Porto Alvo (ex: 80): "))
                count = int(input("Número de Pacotes (ex: 100): "))
                dos_attacks.syn_flood(target, port, count)
            except ValueError:
                print("[!] Erro: Valores inválidos.")
            input("\nPressione ENTER para continuar...")

        elif opt == '4':
            target = input("IP do Servidor: ")
            ports_str = input("Sequência de Portos (ex: 7000,8000,9000): ")
            try:
                ports = [int(p.strip()) for p in ports_str.split(',')]
                port_knocking.knock(target, ports)
            except Exception as e:
                print(f"[!] Erro na sequência: {e}")
            input("\nPressione ENTER para continuar...")
        
        elif opt == '0':
            break
        else:
            print("[!] Opção inválida.")

def main_menu():
    while True:
        print_header()
        print("\n=== MENU PRINCIPAL ===")
        print("[1] Ferramentas de Rede (Scanner, Floods)")
        print("[2] Análise de Logs e Geolocalização")
        print("[3] Segurança (Password Manager, Chat)")
        print("[4] Relatórios e Base de Dados")
        print("[0] Sair")
        
        choice = input("\nEscolha uma opção: ")
        
        if choice == '1':
            network_menu() 
        elif choice == '2':
            analyzer.menu()
        elif choice == '3':
            print("\n--- MÓDULO DE SEGURANÇA ---")
            print("[1] Password Manager (Cofre + 2FA)")
            print("[2] Chat P2P Seguro (AES)")
            print("[0] Voltar")
            
            sub = input("\nOpção: ")
            if sub == '1':
                pass_manager.menu()
            elif sub == '2':
            
                c = secure_chat.SecureChat()
                c.menu()
                    
        elif choice == '4':
            reports.menu()
        elif choice == '0':
            print("\nA sair... Obrigado por usar a aplicação!")
            sys.exit()

if __name__ == "__main__":
    if os.name != 'nt' and os.geteuid() != 0:
        print("\n[!] AVISO: Para usar os ataques de rede, corre com 'sudo python3 main.py'")
    
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n[!] Interrupção forçada. A sair...")
        sys.exit()