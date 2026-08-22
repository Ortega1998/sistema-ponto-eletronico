import customtkinter as ctk
import banco
import facial_service
from datetime import datetime
from tkinter import messagebox

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Ponto Eletrônico - Completo")
        self.geometry("800x600")
        
        # Garante que o banco está pronto
        banco.inicializar_banco()
        
        # Configuração de abas
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.aba_registro = self.tabview.add("Registro Facial")
        self.aba_relatorio = self.tabview.add("Relatórios")
        self.aba_gestao = self.tabview.add("Gestão / Cadastro")
        
        self.setup_aba_registro()
        self.setup_aba_relatorio()
        self.setup_aba_gestao()

    def setup_aba_registro(self):
        titulo = ctk.CTkLabel(self.aba_registro, text="Registro de Ponto por Reconhecimento Facial", font=("Arial", 16, "bold"))
        titulo.pack(pady=30)
        
        self.entry_nome = ctk.CTkEntry(self.aba_registro, placeholder_text="Digite seu nome cadastrado", width=300, height=40)
        self.entry_nome.pack(pady=10)
        
        btn_ponto = ctk.CTkButton(self.aba_registro, text="Bater Ponto Facial", fg_color="#1f538d", width=220, height=45, command=self.processar_ponto)
        btn_ponto.pack(pady=20)

    def processar_ponto(self):
        nome = self.entry_nome.get().strip()
        if not nome:
            messagebox.showwarning("Atenção", "Digite o nome do funcionário.")
            return
            
        status_facial = facial_service.verificar_e_comparar_ponto(nome)
        
        if status_facial == "nao_cadastrado":
            messagebox.showerror("Erro", "Funcionário não possui rosto cadastrado na pasta 'rostos_cadastrados'!")
            return
            
        if status_facial:
            sucesso_banco = banco.registrar_ponto_no_banco(nome)
            if sucesso_banco:
                messagebox.showinfo("Sucesso", "Ponto registrado com sucesso!")
                self.entry_nome.delete(0, 'end')
                self.carregar_registros()
            else:
                messagebox.showerror("Erro", "Usuário não encontrado no banco de dados.")
        else:
            messagebox.showwarning("Aviso", "Validação facial cancelada ou falhou.")

    def setup_aba_relatorio(self):
        titulo = ctk.CTkLabel(self.aba_relatorio, text="Relatório de Pontos", font=("Arial", 16, "bold"))
        titulo.pack(pady=5)
        
        frame_filtros = ctk.CTkFrame(self.aba_relatorio)
        frame_filtros.pack(pady=5, padx=5, fill="x")
        
        self.entry_filtra_nome = ctk.CTkEntry(frame_filtros, placeholder_text="Filtrar Nome", width=130)
        self.entry_filtra_nome.pack(side="left", padx=3, pady=5)
        
        self.entry_data_ini = ctk.CTkEntry(frame_filtros, placeholder_text="Início (DD/MM/AAAA)", width=130)
        self.entry_data_ini.pack(side="left", padx=3, pady=5)
        
        self.entry_data_fim = ctk.CTkEntry(frame_filtros, placeholder_text="Fim (DD/MM/AAAA)", width=130)
        self.entry_data_fim.pack(side="left", padx=3, pady=5)
        
        btn_filtrar = ctk.CTkButton(frame_filtros, text="Buscar", width=65, command=self.carregar_registros)
        btn_filtrar.pack(side="left", padx=3, pady=5)
        
        btn_exportar = ctk.CTkButton(frame_filtros, text="Excel", fg_color="green", width=65, command=self.exportar_relatorio)
        btn_exportar.pack(side="left", padx=3, pady=5)

        btn_corrigir = ctk.CTkButton(frame_filtros, text="Corrigir", fg_color="orange", text_color="black", width=65, command=self.abrir_janela_correcao)
        btn_corrigir.pack(side="left", padx=3, pady=5)
        
        self.txt_relatorio = ctk.CTkTextbox(self.aba_relatorio, width=740, height=330, font=("Courier", 11))
        self.txt_relatorio.pack(pady=5)
        
        self.carregar_registros()

    def calcular_horas_trabalhadas(self, registros):
        jornadas = {}
        for reg in registros:
            _, nome_func, data_hora_str, tipo = reg
            try:
                dt_obj = datetime.strptime(data_hora_str, "%d/%m/%Y %H:%M:%S")
                data_dia = dt_obj.strftime("%d/%m/%Y")
                chave = (nome_func.upper(), data_dia)
                if chave not in jornadas: jornadas[chave] = []
                jornadas[chave].append((dt_obj, tipo))
            except: 
                continue
                
        totais_por_dia = {}
        for chave, eventos in jornadas.items():
            eventos.sort(key=lambda x: x[0])
            tempo_total_segundos = 0
            entrada_atual = None
            for dt_evt, tipo_evt in eventos:
                if tipo_evt == "Entrada": 
                    entrada_atual = dt_evt
                elif tipo_evt == "Saída" and entrada_atual is not None:
                    diferenca = dt_evt - entrada_atual
                    tempo_total_segundos += diferenca.total_seconds()
                    entrada_atual = None
            horas = int(tempo_total_segundos // 3600)
            minutos = int((tempo_total_segundos % 3600) // 60)
            totais_por_dia[chave] = f"{horas}h {minutos:02d}m"
            
        return totais_por_dia

    def carregar_registros(self):
        self.txt_relatorio.delete("1.0", "end")
        self.txt_relatorio.insert("end", f"{'NOME':<16} | {'DATA E HORA':<20} | {'TIPO'}\n")
        self.txt_relatorio.insert("end", "-"*52 + "\n")
        
        filtro_nome = self.entry_filtra_nome.get().strip() if hasattr(self, 'entry_filtra_nome') else ""
        data_ini = self.entry_data_ini.get().strip() if hasattr(self, 'entry_data_ini') else ""
        data_fim = self.entry_data_fim.get().strip() if hasattr(self, 'entry_data_fim') else ""
        
        try:
            conn = banco.conectar()
            cursor = conn.cursor()
            
            query = "SELECT r.id, u.nome, r.data_hora, r.tipo FROM registros r JOIN usuarios u ON r.usuario_id = u.id WHERE 1=1"
            params = []
            
            if filtro_nome:
                query += " AND u.nome LIKE ? COLLATE NOCASE"
                params.append(f"%{filtro_nome}%")
            if data_ini and len(data_ini) == 10:
                query += " AND SUBSTR(r.data_hora, 7, 4) || SUBSTR(r.data_hora, 4, 2) || SUBSTR(r.data_hora, 1, 2) >= ?"
                params.append(f"{data_ini[6:10]}{data_ini[3:5]}{data_ini[0:2]}")
            if data_fim and len(data_fim) == 10:
                query += " AND SUBSTR(r.data_hora, 7, 4) || SUBSTR(r.data_hora, 4, 2) || SUBSTR(r.data_hora, 1, 2) <= ?"
                params.append(f"{data_fim[6:10]}{data_fim[3:5]}{data_fim[0:2]}")
                
            query += " ORDER BY r.id ASC"
            cursor.execute(query, params)
            resultados = cursor.fetchall()
            conn.close()
            
            if not resultados:
                self.txt_relatorio.insert("end", "Nenhum registro encontrado.\n")
                return
                
            # 1. Exibe a lista detalhada de batidas (Entradas e Saídas)
            for reg in resultados:
                _, nome_func, data_hora_str, tipo = reg
                self.txt_relatorio.insert("end", f"{nome_func[:14].upper():<16} | {data_hora_str:<20} | {tipo}\n")
                
            # 2. Calcula e exibe o resumo de horas trabalhadas por dia logo abaixo
            totais = self.calcular_horas_trabalhadas(resultados)
            
            self.txt_relatorio.insert("end", "\n" + "="*52 + "\n")
            self.txt_relatorio.insert("end", f"{'RESUMO DE HORAS TRABALHADAS POR DIA':^52}\n")
            self.txt_relatorio.insert("end", "-"*52 + "\n")
            self.txt_relatorio.insert("end", f"{'NOME':<20} | {'DATA':<12} | {'TOTAL HORAS'}\n")
            self.txt_relatorio.insert("end", "-"*52 + "\n")
            
            for (nome_func, data_dia), horas_trab in totais.items():
                self.txt_relatorio.insert("end", f"{nome_func[:18]:<20} | {data_dia:<12} | {horas_trab}\n")
                
        except Exception as e:
            self.txt_relatorio.insert("end", f"Erro ao carregar relatórios: {str(e)}")

    def exportar_relatorio(self):
        try:
            import pandas as pd
            conn = banco.conectar()
            query = "SELECT r.id, u.nome, u.cargo, r.data_hora, r.tipo FROM registros r JOIN usuarios u ON r.usuario_id = u.id ORDER BY r.id DESC"
            df = pd.read_sql_query(query, conn)
            conn.close()
            
            if df.empty:
                messagebox.showwarning("Aviso", "Não há registros para exportar.")
                return
                
            caminho_arquivo = "relatorio_pontos.xlsx"
            df.to_excel(caminho_arquivo, index=False)
            messagebox.showinfo("Sucesso", f"Relatório exportado para:\n{caminho_arquivo}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar (verifique pandas/openpyxl):\n{str(e)}")

    def abrir_janela_correcao(self):
        janela_corr = ctk.CTkToplevel(self)
        janela_corr.title("Corrigir Registro")
        janela_corr.geometry("300x180")
        janela_corr.grab_set()
        
        ctk.CTkLabel(janela_corr, text="ID do Registro a Excluir:").pack(pady=10)
        entry_id = ctk.CTkEntry(janela_corr, placeholder_text="Ex: 1")
        entry_id.pack(pady=5)
        
        def executar_correcao():
            reg_id = entry_id.get().strip()
            if not reg_id.isdigit():
                messagebox.showerror("Erro", "Digite um ID numérico válido.")
                return
            try:
                conn = banco.conectar()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM registros WHERE id = ?", (reg_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Sucesso", f"Registro ID {reg_id} removido!")
                janela_corr.destroy()
                self.carregar_registros()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro: {str(e)}")
                
        ctk.CTkButton(janela_corr, text="Excluir Registro", fg_color="red", command=executar_correcao).pack(pady=10)

    def setup_aba_gestao(self):
        titulo = ctk.CTkLabel(self.aba_gestao, text="Painel de Gestão e Cadastro de Usuários", font=("Arial", 16, "bold"))
        titulo.pack(pady=15)
        
        frame_form = ctk.CTkFrame(self.aba_gestao)
        frame_form.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(frame_form, text="Cadastrar Novo Funcionário", font=("Arial", 12, "bold")).pack(pady=5)
        
        self.entry_cad_nome = ctk.CTkEntry(frame_form, placeholder_text="Nome Completo", width=300)
        self.entry_cad_nome.pack(pady=5)
        
        self.entry_cad_cargo = ctk.CTkEntry(frame_form, placeholder_text="Cargo", width=300)
        self.entry_cad_cargo.pack(pady=5)
        
        btn_salvar_usuario = ctk.CTkButton(frame_form, text="Salvar Funcionário e Cadastrar Rosto", fg_color="green", command=self.cadastrar_novo_usuario)
        btn_salvar_usuario.pack(pady=10)

    def cadastrar_novo_usuario(self):
        nome = self.entry_cad_nome.get().strip()
        cargo = self.entry_cad_cargo.get().strip()
        
        if not nome or not cargo:
            messagebox.showwarning("Atenção", "Preencha o nome e o cargo!")
            return
            
        try:
            conn = banco.conectar()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (nome, cargo) VALUES (?, ?)", (nome, cargo))
            conn.commit()
            conn.close()
            
            # Abre a câmera para tirar a foto do rosto imediatamente
            messagebox.showinfo("Aviso", "Funcionário salvo! A câmera abrirá para capturar o rosto. Pressione ESPAÇO.")
            sucesso_foto = facial_service.salvar_foto_cadastro(nome)
            
            if sucesso_foto:
                messagebox.showinfo("Sucesso", f"Usuário {nome} cadastrado com foto facial com sucesso!")
                self.entry_cad_nome.delete(0, 'end')
                self.entry_cad_cargo.delete(0, 'end')
            else:
                messagebox.showwarning("Aviso", "Usuário salvo no banco, mas a captura da foto facial foi cancelada.")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar: {str(e)}")

if __name__ == "__main__":
    app = App()
    app.mainloop()