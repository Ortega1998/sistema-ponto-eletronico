import sqlite3
import hashlib
import os
from datetime import datetime

def conectar():
    db_path = os.path.join(os.path.dirname(__file__), "sistema_ponto.db")
    return sqlite3.connect(db_path)

def inicializar_banco():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, cargo TEXT NOT NULL, qrcode_id TEXT UNIQUE DEFAULT 'PENDENTE', senha_hash TEXT DEFAULT '123')''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS registros (id INTEGER PRIMARY KEY AUTOINCREMENT, usuario_id INTEGER, data_hora TEXT NOT NULL, tipo TEXT NOT NULL, FOREIGN KEY(usuario_id) REFERENCES usuarios(id))''')
    conn.commit()
    conn.close()

def registrar_ponto_no_banco(nome_ou_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE nome LIKE ? COLLATE NOCASE", (nome_ou_id.strip(),))
    usuario = cursor.fetchone()
    if not usuario:
        conn.close()
        return False
    
    usuario_id = usuario[0]
    data_atual_str = datetime.now().strftime("%d/%m/%Y")
    data_hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    cursor.execute("SELECT tipo FROM registros WHERE usuario_id = ? AND data_hora LIKE ? ORDER BY id DESC LIMIT 1", (usuario_id, f"{data_atual_str}%"))
    ultimo = cursor.fetchone()
    tipo = "Saída" if (ultimo and ultimo[0] == "Entrada") else "Entrada"
    
    cursor.execute("INSERT INTO registros (usuario_id, data_hora, tipo) VALUES (?, ?, ?)", (usuario_id, data_hora_atual, tipo))
    conn.commit()
    conn.close()
    return True