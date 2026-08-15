import customtkinter as ctk
import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from datetime import datetime

class JanelaRelatorio(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Filtrar Relatório")
        self.geometry("300x300")

        ctk.CTkLabel(self, text="Nome do Funcionário:").pack(pady=(20, 0))
        self.entry_nome = ctk.CTkEntry(self)
        self.entry_nome.pack(pady=5)

        ctk.CTkLabel(self, text="Data (AAAA-MM-DD):").pack(pady=(10, 0))
        self.entry_data = ctk.CTkEntry(self, placeholder_text="Ex: 2026-08-15")
        self.entry_data.pack(pady=5)

        self.btn_gerar = ctk.CTkButton(self, text="Gerar PDF Filtrado", command=self.gerar_pdf)
        self.btn_gerar.pack(pady=20)

    def gerar_pdf(self):
        nome = self.entry_nome.get()
        data = self.entry_data.get()
        
        conn = sqlite3.connect("sistema_ponto.db")
        cursor = conn.cursor()
        
        query = '''
            SELECT u.nome, u.cargo, r.data_hora, r.tipo
            FROM registros r
            JOIN usuarios u ON r.usuario_id = u.id
            WHERE 1=1
        '''
        params = []
        
        if nome:
            query += " AND u.nome LIKE ?"
            params.append(f"%{nome}%")
        if data:
            query += " AND DATE(r.data_hora) = ?"
            params.append(data)
            
        cursor.execute(query, params)
        registros = cursor.fetchall()
        conn.close()

        if not registros:
            print("Nenhum registro encontrado com esses filtros.")
            return

        # Gerar o PDF (mesma lógica anterior)
        if not os.path.exists("relatorios"): os.makedirs("relatorios")
        nome_pdf = f"relatorios/Relatorio_Filtrado_{datetime.now().strftime('%H%M%S')}.pdf"
        
        c = canvas.Canvas(nome_pdf, pagesize=A4)
        c.drawString(50, 800, f"Relatório Filtrado - Nome: {nome or 'Todos'} | Data: {data or 'Todas'}")
        
        y = 770
        for reg in registros:
            c.drawString(50, y, f"{reg[0]} | {reg[1]} | {reg[2]} | {reg[3]}")
            y -= 20
        c.save()
        print(f"PDF gerado: {nome_pdf}")
        self.destroy()

if __name__ == "__main__":
    app = JanelaRelatorio()
    app.mainloop()