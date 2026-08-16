import sqlite3
import hashlib
from datetime import datetime

from datetime import datetime

def registrar_ponto_no_banco(nome_ou_id):
    conn = conectar()
    cursor = conn.cursor()
    
    # 1. Busca o ID do usuário pelo nome
    cursor.execute("SELECT id FROM usuarios WHERE nome = ?", (nome_ou_id,))
    usuario = cursor.fetchone()
    
    if not usuario:
        conn.close()
        return False
    
    usuario_id = usuario[0]
    data_atual_str = datetime.now().strftime("%d/%m/%Y")
    data_hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    # 2. Verifica qual foi o último registro deste usuário HOJE para definir Entrada ou Saída
    cursor.execute("""
        SELECT tipo, data_hora FROM registros 
        WHERE usuario_id = ? AND data_hora LIKE ? 
        ORDER BY id DESC LIMIT 1
    """, (usuario_id, f"{data_atual_str}%"))
    
    ultimo_registro = cursor.fetchone()
    
    # 3. Lógica automática: Se não tem registro hoje, o primeiro é ENTRADA. 
    # Caso contrário, alterna entre Entrada e Saída.
    if not ultimo_registro:
        tipo = "Entrada"
    else:
        ultimo_tipo = ultimo_registro[0]
        tipo = "Saída" if ultimo_tipo == "Entrada" else "Entrada"
    
    # 4. Insere no banco com o tipo correto
    cursor.execute("""
        INSERT INTO registros (usuario_id, data_hora, tipo) 
        VALUES (?, ?, ?)
    """, (usuario_id, data_hora_atual, tipo))
    
    conn.commit()
    conn.close()
    return True

def conectar():
    return sqlite3.connect("sistema_ponto.db")

def inicializar_banco():
    conn = conectar()
    cursor = conn.cursor()
    
    # Cria tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cargo TEXT NOT NULL,
            qrcode_id TEXT UNIQUE NOT NULL,
            senha_hash TEXT NOT NULL
        )
    ''')
    
    # Cria tabela de registros de ponto
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            data_hora TEXT NOT NULL,
            tipo TEXT NOT NULL,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Banco de dados inicializado com sucesso!")

# Função para converter senha em hash (mais seguro)
def gerar_hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

if __name__ == "__main__":
    inicializar_banco()