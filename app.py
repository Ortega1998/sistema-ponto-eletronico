import customtkinter as ctk
import facial_service
import banco

class AppPonto(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Ponto Eletrônico - Completo")
        self.geometry("650x550")
        
        ctk.set_appearance_mode("Dark")
        
        # Criação do Sistema de Abas
        self.tabview = ctk.CTkTabview(self, width=600, height=480)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Adicionando as Abas
        self.aba_ponto = self.tabview.add("Registro Facial")
        self.aba_relatorio = self.tabview.add("Relatórios")
        
        # Configura o conteúdo de cada aba
        self.setup_aba_ponto()
        self.setup_aba_relatorio()

    def setup_aba_ponto(self):
        titulo = ctk.CTkLabel(self.aba_ponto, text="Controle de Ponto por Reconhecimento", font=("Arial", 18, "bold"))
        titulo.pack(pady=15)
        
        self.entry_nome = ctk.CTkEntry(self.aba_ponto, placeholder_text="Digite seu Nome", width=300)
        self.entry_nome.pack(pady=10)
        
        self.btn_cadastrar = ctk.CTkButton(self.aba_ponto, text="Cadastrar Rosto", fg_color="green", command=self.fazer_cadastro_facial)
        self.btn_cadastrar.pack(pady=8)
        
        self.btn_ponto = ctk.CTkButton(self.aba_ponto, text="Bater Ponto Facial", fg_color="blue", command=self.bater_ponto_facial)
        self.btn_ponto.pack(pady=8)
        
        self.lbl_status = ctk.CTkLabel(self.aba_ponto, text="Aguardando ação...", text_color="gray", font=("Arial", 12))
        self.lbl_status.pack(pady=20)

    def setup_aba_relatorio(self):
        titulo = ctk.CTkLabel(self.aba_relatorio, text="Relatório de Pontos", font=("Arial", 18, "bold"))
        titulo.pack(pady=10)
        
        frame_filtros = ctk.CTkFrame(self.aba_relatorio)
        frame_filtros.pack(pady=5, padx=10, fill="x")
        
        self.entry_filtra_nome = ctk.CTkEntry(frame_filtros, placeholder_text="Filtrar por Nome", width=180)
        self.entry_filtra_nome.pack(side="left", padx=5, pady=5)
        
        self.entry_filtra_data = ctk.CTkEntry(frame_filtros, placeholder_text="Data (DD/MM/AAAA)", width=150)
        self.entry_filtra_data.pack(side="left", padx=5, pady=5)
        
        btn_filtrar = ctk.CTkButton(frame_filtros, text="Buscar", width=90, command=self.carregar_registros)
        btn_filtrar.pack(side="left", padx=5, pady=5)
        
        btn_limpar = ctk.CTkButton(frame_filtros, text="Limpar", fg_color="gray", width=80, command=self.limpar_filtros)
        btn_limpar.pack(side="left", padx=5, pady=5)
        
        self.txt_relatorio = ctk.CTkTextbox(self.aba_relatorio, width=580, height=280)
        self.txt_relatorio.pack(pady=10)
        
        self.carregar_registros()

    def limpar_filtros(self):
        self.entry_filtra_nome.delete(0, 'end')
        self.entry_filtra_data.delete(0, 'end')
        self.carregar_registros()

    def fazer_cadastro_facial(self):
        nome = self.entry_nome.get().strip()
        if not nome:
            self.lbl_status.configure(text="Erro: Digite o nome antes de cadastrar!", text_color="yellow")
            return
            
        self.lbl_status.configure(text="Abrindo câmera para cadastro...", text_color="yellow")
        self.update()
        
        sucesso = facial_service.salvar_foto_cadastro(nome)
        
        if sucesso:
            try:
                conn = banco.conectar()
                cursor = conn.cursor()
                
                cursor.execute("SELECT id FROM usuarios WHERE nome = ?", (nome,))
                existe = cursor.fetchone()
                
                if not existe:
                    cursor.execute("""
                        INSERT INTO usuarios (nome, cargo, qrcode_id, senha_hash) 
                        VALUES (?, ?, ?, ?)
                    """, (nome, "Funcionário", f"QR_{nome}", banco.gerar_hash_senha("123")))
                    conn.commit()
                
                conn.close()
                
                self.lbl_status.configure(text=f"Sucesso! {nome.upper()} cadastrado.", text_color="green")
                self.entry_nome.delete(0, 'end')
                self.carregar_registros()
                
            except Exception as e:
                self.lbl_status.configure(text=f"Erro ao salvar no banco: {str(e)}", text_color="red")
        else:
            self.lbl_status.configure(text="Cadastro facial cancelado.", text_color="red")

    def bater_ponto_facial(self):
        nome = self.entry_nome.get().strip()
        if not nome:
            self.lbl_status.configure(text="Erro: Digite seu nome antes de bater o ponto!", text_color="yellow")
            return

        self.lbl_status.configure(text="Abrindo câmera para validação...", text_color="yellow")
        self.update_idletasks()
        
        resultado = facial_service.verificar_e_comparar_ponto(nome)
        
        if resultado == "nao_cadastrado":
            self.lbl_status.configure(text=f"Aviso: Funcionário '{nome}' não possui cadastro!", text_color="red")
            return
            
        if resultado is True:
            banco.registrar_ponto_no_banco(nome)
            self.lbl_status.configure(text=f"Ponto registrado para: {nome.upper()}!", text_color="green")
            self.entry_nome.delete(0, 'end')
            self.carregar_registros()
        else:
            self.lbl_status.configure(text="Erro: Rosto não confere com o cadastro!", text_color="red")

    def carregar_registros(self):
        self.txt_relatorio.delete("1.0", "end")
        filtro_nome = self.entry_filtra_nome.get().strip()
        filtro_data = self.entry_filtra_data.get().strip()
        
        try:
            conn = banco.conectar()
            cursor = conn.cursor()
            
            query = """
                SELECT u.nome, r.data_hora, r.tipo 
                FROM registros r
                JOIN usuarios u ON r.usuario_id = u.id
                WHERE 1=1
            """
            parametros = []
            
            if filtro_nome:
                query += " AND u.nome LIKE ? COLLATE NOCASE"
                parametros.append(f"%{filtro_nome}%")
                
            if filtro_data:
                query += " AND r.data_hora LIKE ?"
                parametros.append(f"%{filtro_data}%")
                
            query += " ORDER BY r.id DESC"
            
            cursor.execute(query, parametros)
            resultados = cursor.fetchall()
            conn.close()
            
            if not resultados:
                self.txt_relatorio.insert("end", "Nenhum registro encontrado.\n")
                return
                
            for reg in resultados:
                nome_func, data_hora, tipo = reg
                cor_tipo = "🟢 ENTRADA" if tipo == "Entrada" else "🔴 SAÍDA"
                linha = f"Funcionário: {nome_func.upper()} | Data/Hora: {data_hora} | Tipo: {cor_tipo}\n"
                self.txt_relatorio.insert("end", linha)
                
        except Exception as e:
            self.txt_relatorio.insert("end", f"Erro ao carregar relatórios: {str(e)}")

if __name__ == "__main__":
    app = AppPonto()
    app.mainloop()