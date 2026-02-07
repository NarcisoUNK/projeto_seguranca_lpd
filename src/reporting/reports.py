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
    print("\n=== GERAÇÃO DE RELATÓRIOS ===")
    print("Este módulo é utilizado automaticamente pelas outras ferramentas")
    print("para exportar resultados (Scans, Logs, etc).")
    input("Pressione ENTER para voltar...")