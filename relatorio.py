import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def gerar_relatorio_consolidado_pdf():
    # Caminho do banco de dados
    db_path = "sistema_ponto.db"
    
    if not os.path.exists(db_path):
        print(f"Erro: Banco de dados '{db_path}' não encontrado.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Busca registros com nomes dos usuários, ordenados por data/hora mais recente
    cursor.execute('''
        SELECT u.nome, u.cargo, r.data_hora, r.tipo
        FROM registros r
        JOIN usuarios u ON r.usuario_id = u.id
        ORDER BY r.data_hora DESC
    ''')
    
    registros = cursor.fetchall()
    conn.close()

    if not registros:
        print("Nenhum registro encontrado no banco de dados.")
        return

    # Garante que a pasta 'relatorios' exista
    if not os.path.exists("relatorios"):
        os.makedirs("relatorios")

    # Nome do arquivo
    data_atual = datetime.now().strftime("%Y-%m-%d")
    nome_pdf = f"relatorios/Relatorio_Consolidado_{data_atual}.pdf"

    # Criar PDF
    c = canvas.Canvas(nome_pdf, pagesize=A4)
    width, height = A4
    
    # Cabeçalho
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Relatório Consolidado de Pontos")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 70, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    c.line(50, height - 85, width - 50, height - 85)
    
    # Tabela
    y = height - 120
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "NOME")
    c.drawString(180, y, "CARGO")
    c.drawString(330, y, "DATA/HORA")
    c.drawString(480, y, "TIPO")
    
    c.setFont("Helvetica", 9)
    y -= 20
    
    for reg in registros:
        # Verifica se precisa pular página
        if y < 50:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 9)
            
        c.drawString(50, y, str(reg[0]))
        c.drawString(180, y, str(reg[1]))
        c.drawString(330, y, str(reg[2]))
        c.drawString(480, y, str(reg[3]))
        y -= 18
        
    c.save()
    print(f"Sucesso! Relatório consolidado gerado na pasta 'relatorios': {nome_pdf}")

if __name__ == "__main__":
    gerar_relatorio_consolidado_pdf()