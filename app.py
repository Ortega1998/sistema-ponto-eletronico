import customtkinter as ctk
import subprocess
import sqlite3
from banco import gerar_hash_senha

# Configuração global de aparência
ctk.set_appearance_mode("System")  # Segue o tema do Windows (Dark/Light)
ctk.set_default_color_theme("blue")

class AppPonto(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Ponto Eletrônico")
        self.geometry("520x480")
        self.resizable(False, False)

        # Abas principais com visual mais espaçado
        self.tabview = ctk.CTkTabview(self, width=480, height=420)
        self.tabview.pack(pady=15, padx=15)
        
        self.aba_ponto = self.tabview.add("  Ponto  ")
        self.aba_relatorio = self.tabview.add("  Relatórios  ")
        self.aba_admin = self.tabview.add("  Administração  ")

        # ==========================================
        # --- ABA PONTO ---
        # ==========================================
        lbl_ponto_titulo = ctk.CTkLabel(self.aba_ponto, text="Controle de Jornada", font=("Arial", 18, "bold"))
        lbl_ponto_titulo.pack(pady=(30, 10))
        
        lbl_ponto_sub = ctk.CTkLabel(self.aba_ponto, text="Clique abaixo para iniciar a leitura do seu QR Code", text_color="gray")
        lbl_ponto_sub.pack(pady=(0, 20))

        self.btn_ponto = ctk.CTkButton(
            self.aba_ponto, text="📸  Iniciar Ponto (Webcam)", 
            command=self.abrir_ponto, height=45, font=("Arial", 14, "bold")
        )
        self.btn_ponto.pack(pady=10, padx=40, fill="x")

        # ==========================================
        # --- ABA RELATÓRIOS ---
        # ==========================================
        lbl_rel_titulo = ctk.CTkLabel(self.aba_relatorio, text="Central de Relatórios", font=("Arial", 18, "bold"))
        lbl_rel_titulo.pack(pady=(30, 10))
        
        lbl_rel_sub = ctk.CTkLabel(self.aba_relatorio, text="Gere relatórios consolidados em PDF com filtros", text_color="gray")
        lbl_rel_sub.pack(pady=(0, 20))

        self.btn_relatorio = ctk.CTkButton(
            self.aba_relatorio, text="📄  Gerar Relatório Filtrado", 
            command=self.gerar_relatorio, height=45, font=("Arial", 14, "bold"),
            fg_color="#2b8a3e", hover_color="#237032" # Verde profissional
        )
        self.btn_relatorio.pack(pady=10, padx=40, fill="x")

        # ==========================================
        # --- ABA ADMIN ---
        # ==========================================
        lbl_adm_titulo = ctk.CTkLabel(self.aba_admin, text="Gerenciamento de Funcionários", font=("Arial", 15, "bold"))
        lbl_adm_titulo.pack(pady=(15, 10))

        # Container centralizado para os campos de entrada
        self.frame_inputs = ctk.CTkFrame(self.aba_admin, fg_color="transparent")
        self.frame_inputs.pack(pady=5)

        self.ent_nome = ctk.CTkEntry(self.frame_inputs, placeholder_text="Nome Completo", width=300, height=35)
        self.ent_nome.pack(pady=6)
        
        self.ent_cargo = ctk.CTkEntry(self.frame_inputs, placeholder_text="Cargo", width=300, height=35)
        self.ent_cargo.pack(pady=6)
        
        self.ent_qr = ctk.CTkEntry(self.frame_inputs, placeholder_text="QR Code ID", width=300, height=35)
        self.ent_qr.pack(pady=6)
        
        self.ent_senha = ctk.CTkEntry(self.frame_inputs, placeholder_text="Senha de Acesso", show="*", width=300, height=35)
        self.ent_senha.pack(pady=6)

        # Botões de Ação Admin
        self.btn_cadastrar = ctk.CTkButton(
            self.aba_admin, text="Adicionar Funcionário", 
            command=self.cadastrar, fg_color="#1f77b4", hover_color="#145a8d",
            height=38, width=200
        )
        self.btn_cadastrar.pack(pady=(10, 5))

        self.btn_excluir = ctk.CTkButton(
            self.aba_admin, text="Excluir por QR ID", 
            command=self.excluir, fg_color="#c92a2a", hover_color="#a61e1e",
            height=35, width=200
        )
        self.btn_excluir.pack(pady=5)

    # --- FUNÇÕES DE CONTROLE ---
    def abrir_ponto(self):
        subprocess.Popen(["python", "main.py"])

    def gerar_relatorio(self):
        subprocess.Popen(["python", "relatorio_filtrado.py"])

    def cadastrar(self):
        nome, cargo, qr, senha = self.ent_nome.get(), self.ent_cargo.get(), self.ent_qr.get(), self.ent_senha.get()
        if all([nome, cargo, qr, senha]):
            try:
                conn = sqlite3.connect("sistema_ponto.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO usuarios (nome, cargo, qrcode_id, senha_hash) VALUES (?, ?, ?, ?)", 
                               (nome, cargo, qr, gerar_hash_senha(senha)))
                conn.commit()
                conn.close()
                print(f"[SUCESSO] Funcionário {nome} cadastrado!")
                # Limpa os campos após o cadastro
                self.ent_nome.delete(0, 'end')
                self.ent_cargo.delete(0, 'end')
                self.ent_qr.delete(0, 'end')
                self.ent_senha.delete(0, 'end')
            except Exception as e:
                print(f"[ERRO] Falha ao cadastrar: {e}")
        else:
            print("[AVISO] Preencha todos os campos para cadastrar.")

    def excluir(self):
        qr = self.ent_qr.get()
        if qr:
            conn = sqlite3.connect("sistema_ponto.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE qrcode_id = ?", (qr,))
            conn.commit()
            conn.close()
            print(f"[SUCESSO] Funcionário com QR ID '{qr}' removido!")
            self.ent_qr.delete(0, 'end')
        else:
            print("[AVISO] Digite o QR Code ID para excluir.")

if __name__ == "__main__":
    app = AppPonto()
    app.mainloop()