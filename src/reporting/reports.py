# Importações necessárias para o ReportLab
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def export_pdf(filename, title, content_lines):
    """
    Gera um PDF simples com título e lista de linhas de texto.
    """
    ensure_dir()
    filepath = os.path.join(REPORT_DIR, filename)
    
    try:
        c = canvas.Canvas(filepath, pagesize=letter)
        width, height = letter
        
        # Cabeçalho
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, title)
        
        c.setFont("Helvetica", 10)
        c.drawString(50, height - 70, f"Data de Geração: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        c.line(50, height - 75, width - 50, height - 75)
        
        # Conteúdo
        y = height - 100
        c.setFont("Helvetica", 12)
        
        for line in content_lines:
            if y < 50: # Nova página se chegar ao fim
                c.showPage()
                y = height - 50
            
            c.drawString(50, y, str(line))
            y -= 20
            
        c.save()
        print(f"[+] Relatório PDF gerado: {filepath}")
        return True
    except Exception as e:
        print(f"[!] Erro ao gerar PDF: {e}")
        return False

def menu():
    while True:
        print("\n=== GERAÇÃO DE RELATÓRIOS (TESTE) ===")
        print("[1] Gerar PDF de Teste (Manual)")
        print("[0] Voltar")
        
        escolha = input("\nEscolha uma opção: ")

        if escolha == "1":
            print("\n--- A Gerar Relatório de Exemplo ---")
            # Dados falsos para testar o motor PDF
            nome_ficheiro = "teste_manual.pdf"
            titulo = "Relatório de Segurança - TESTE MANUAL"
            linhas = [
                "Este é um teste do módulo de relatórios.",
                "----------------------------------------",
                "Item 1: O sistema está funcional.",
                "Item 2: A geração de PDF com ReportLab funciona.",
                "Item 3: O Python é espetacular.",
                "----------------------------------------",
                f"Teste realizado por: {os.getlogin() if hasattr(os, 'getlogin') else 'Utilizador'}"
            ]
            
            # Chama a tua função export_pdf
            sucesso = export_pdf(nome_ficheiro, titulo, linhas)
            
            if sucesso:
                print(f"[SUCCESS] Vai à pasta 'reports' e abre o ficheiro '{nome_ficheiro}'!")
                input("Pressione ENTER para continuar...")
            else:
                print("[ERROR] Falha ao criar o PDF.")
                input("Pressione ENTER para continuar...")

        elif escolha == "0":
            break
        else:
            print("[!] Opção inválida.")