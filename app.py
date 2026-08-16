import customtkinter as ctk
import facial_service
import banco
import csv
from tkinter import filedialog, messagebox

class AppPonto(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Inicializa o banco de dados e as tabelas automaticamente ao abrir o app
        banco.inicializar_banco()

        self.title("Sistema de Ponto Eletrônico - Completo")
        self.geometry("720x600")
        
        ctk.set_appearance_mode("Dark")
        
        # Criação do Sistema de Abas
        self.tabview = ctk.CTkTabview(self, width=670, height=520)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)
        
        self.aba_ponto = self.tabview.add("Registro Facial")
        self.aba_relatorio = self.tabview.add("Relatórios")
        self.aba_gestao = self.tabview.add("Gestão")
        
        self.setup_aba_ponto()
        self.setup_aba_relatorio()
        self.setup_aba_gestao()

    def setup_aba_ponto(self):
        titulo = ctk.CTkLabel(self.aba_ponto, text="Controle de Ponto por Reconhecimento", font=("Arial", 18, "bold"))
        titulo.pack(pady=15)
        
        self.entry_nome = ctk.CTkEntry(self.aba_ponto, placeholder_text="Digite o Nome", width=300)
        self.entry_nome.pack(pady=10)
        
        self.option_cargo = ctk.CTkOptionMenu(
            self.aba_ponto, 
            values=["Faxineira", "Cozinheiro", "Garçom", "Balconista", "Caixa", "Gerente", "RH"], 
            width=300
        )
        self.option_cargo.set("Faxineira")
        self.option_cargo.pack(pady=10)
        
        self.btn_cadastrar = ctk.CTkButton(self.aba_ponto, text="Cadastrar Rosto e Dados", fg_color="green", command=self.fazer_cadastro_facial)
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
        
        self.entry_filtra_nome = ctk.CTkEntry(frame_filtros, placeholder_text="Filtrar por Nome", width=150)
        self.entry_filtra_nome.pack(side="left", padx=5, pady=5)
        
        btn_filtrar = ctk.CTkButton(frame_filtros, text="Buscar", width=75, command=self.carregar_registros)
        btn_filtrar.pack(side="left", padx=5, pady=5)
        
        btn_exportar = ctk.CTkButton(frame_filtros, text="Excel/CSV", fg_color="green", width=90, command=self.exportar_relatorio)
        btn_exportar.pack(side="left", padx=5, pady=5)

        btn_corrigir = ctk.CTkButton(frame_filtros, text="Corrigir Ponto", fg_color="orange", text_color="black", width=100, command=self.abrir_janela_correcao)
        btn_corrigir.pack(side="left", padx=5, pady=5)
        
        self.txt_relatorio = ctk.CTkTextbox(self.aba_relatorio, width=620, height=270, font=("Courier", 11))
        self.txt_relatorio.pack(pady=10)
        
        self.carregar_registros()

    def setup_aba_gestao(self):
        titulo = ctk.CTkLabel(self.aba_gestao, text="Gestão de Funcionários", font=("Arial", 18, "bold"))
        titulo.pack(pady=10)
        
        self.lista_funcionarios = ctk.CTkTextbox(self.aba_gestao, width=620, height=230, font=("Courier", 11))
        self.lista_funcionarios.pack(pady=10)
        
        frame_acoes = ctk.CTkFrame(self.aba_gestao, fg_color="transparent")
        frame_acoes.pack(pady=5)
        
        btn_atualizar = ctk.CTkButton(frame_acoes, text="Atualizar Lista", command=self.carregar_lista_funcionarios, width=140)
        btn_atualizar.pack(side="left", padx=5)
        
        self.entry_deletar = ctk.CTkEntry(frame_acoes, placeholder_text="ID p/ excluir", width=140)
        self.entry_deletar.pack(side="left", padx=5)
        
        btn_excluir = ctk.CTkButton(frame_acoes, text="Excluir", fg_color="red", command=self.excluir_usuario, width=100)
        btn_excluir.pack(side="left", padx=5)
        
        self.carregar_lista_funcionarios()

    def carregar_lista_funcionarios(self):
        self.lista_funcionarios.delete("1.0", "end")
        self.lista_funcionarios.insert("end", f"{'ID':<4} | {'NOME':<25} | {'CARGO'}\n")
        self.lista_funcionarios.insert("end", "-"*50 + "\n")
        try:
            conn = banco.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, cargo FROM usuarios")
            funcionarios = cursor.fetchall()
            conn.close()
            
            if not funcionarios:
                self.lista_funcionarios.insert("end", "Nenhum funcionário cadastrado.\n")
                return
                
            for f in funcionarios:
                self.lista_funcionarios.insert("end", f"{f[0]:<4} | {f[1].upper():<25} | {f[2]}\n")
        except Exception as e:
            self.lista_funcionarios.insert("end", f"Erro: {str(e)}")

    def excluir_usuario(self):
        id_para_excluir = self.entry_deletar.get().strip()
        if not id_para_excluir or not id_para_excluir.isdigit():
            messagebox.showwarning("Aviso", "Digite um ID numérico válido para excluir.")
            return
            
        try:
            conn = banco.conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_para_excluir,))
            conn.commit()
            conn.close()
            
            self.entry_deletar.delete(0, 'end')
            self.carregar_lista_funcionarios()
            messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir: {e}")

    def fazer_cadastro_facial(self):
        nome = self.entry_nome.get().strip()
        cargo = self.option_cargo.get()
        
        if not nome:
            self.lbl_status.configure(text="Erro: Digite o nome!", text_color="yellow")
            return
            
        sucesso = facial_service.salvar_foto_cadastro(nome)
        if sucesso:
            try:
                conn = banco.conectar()
                cursor = conn.cursor()
                # Passamos um qrcode_id único para cada pessoa (ex: QR_Nome)
                cursor.execute(
                    "INSERT INTO usuarios (nome, cargo, qrcode_id, senha_hash) VALUES (?, ?, ?, ?)", 
                    (nome, cargo, f"QR_{nome}", "123")
                )
                conn.commit()
                conn.close()
                self.lbl_status.configure(text=f"Sucesso! {nome.upper()} ({cargo}) cadastrado.", text_color="green")
                self.entry_nome.delete(0, 'end')
                self.carregar_lista_funcionarios()
            except Exception as e:
                self.lbl_status.configure(text=f"Erro banco: {e}", text_color="red")

    def bater_ponto_facial(self):
        nome = self.entry_nome.get().strip()
        if not nome:
            self.lbl_status.configure(text="Erro: Digite seu nome!", text_color="yellow")
            return
        
        resultado = facial_service.verificar_e_comparar_ponto(nome)
        if resultado is True:
            banco.registrar_ponto_no_banco(nome)
            self.lbl_status.configure(text=f"Ponto registrado: {nome.upper()}", text_color="green")
            self.entry_nome.delete(0, 'end')
            self.carregar_registros()
        else:
            self.lbl_status.configure(text="Erro: Rosto não reconhecido!", text_color="red")

    def carregar_registros(self):
        self.txt_relatorio.delete("1.0", "end")
        self.txt_relatorio.insert("end", f"{'ID REG':<8} | {'NOME':<18} | {'DATA/HORA':<20} | {'TIPO'}\n")
        self.txt_relatorio.insert("end", "-"*68 + "\n")
        
        filtro_nome = self.entry_filtra_nome.get().strip()
        
        try:
            conn = banco.conectar()
            cursor = conn.cursor()
            
            query = """
                SELECT r.id, u.nome, r.data_hora, r.tipo 
                FROM registros r 
                JOIN usuarios u ON r.usuario_id = u.id 
                WHERE 1=1
            """
            params = []
            
            if filtro_nome:
                query += " AND u.nome LIKE ? COLLATE NOCASE"
                params.append(f"%{filtro_nome}%")
                
            query += " ORDER BY r.id DESC"
            
            cursor.execute(query, params)
            resultados = cursor.fetchall()
            conn.close()
            
            if not resultados:
                self.txt_relatorio.insert("end", "Nenhum registro encontrado.\n")
                return
                
            for reg in resultados:
                id_reg, nome_func, data_hora, tipo = reg
                self.txt_relatorio.insert("end", f"{id_reg:<8} | {nome_func[:16].upper():<18} | {data_hora:<20} | {tipo}\n")
                
        except Exception as e:
            self.txt_relatorio.insert("end", f"Erro ao carregar relatórios: {str(e)}")

    def exportar_relatorio(self):
        caminho = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Arquivos CSV", "*.csv")])
        if caminho:
            try:
                conn = banco.conectar()
                cursor = conn.cursor()
                cursor.execute("SELECT r.id, u.nome, u.cargo, r.data_hora, r.tipo FROM registros r JOIN usuarios u ON r.usuario_id = u.id")
                dados = cursor.fetchall()
                conn.close()
                
                with open(caminho, 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f, delimiter=";")
                    writer.writerow(["ID Registro", "Nome", "Cargo", "Data/Hora", "Tipo"])
                    writer.writerows(dados)
                messagebox.showinfo("Sucesso", "Relatório exportado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao exportar: {e}")

    def abrir_janela_correcao(self):
        janela_corr = ctk.CTkToplevel(self)
        janela_corr.title("Correção Manual de Ponto")
        janela_corr.geometry("380x250")
        janela_corr.grab_set()
        
        lbl = ctk.CTkLabel(janela_corr, text="Editar Registro por ID", font=("Arial", 14, "bold"))
        lbl.pack(pady=15)
        
        entry_id_reg = ctk.CTkEntry(janela_corr, placeholder_text="ID do Registro", width=250)
        entry_id_reg.pack(pady=8)
        
        entry_nova_data = ctk.CTkEntry(janela_corr, placeholder_text="Novo Horário (DD/MM/AAAA HH:MM)", width=250)
        entry_nova_data.pack(pady=8)
        
        def salvar_correcao():
            id_r = entry_id_reg.get().strip()
            nova_data = entry_nova_data.get().strip()
            
            if not id_r or not nova_data:
                messagebox.showwarning("Aviso", "Preencha todos os campos!")
                return
                
            try:
                conn = banco.conectar()
                cursor = conn.cursor()
                cursor.execute("UPDATE registros SET data_hora = ? WHERE id = ?", (nova_data, id_r))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Sucesso", "Ponto corrigido com sucesso!")
                janela_corr.destroy()
                self.carregar_registros()
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível atualizar: {e}")

        btn_salvar = ctk.CTkButton(janela_corr, text="Salvar Alteração", fg_color="green", command=salvar_correcao)
        btn_salvar.pack(pady=15)

if __name__ == "__main__":
    app = AppPonto()
    app.mainloop()