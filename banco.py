import sqlite3
import hashlib

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