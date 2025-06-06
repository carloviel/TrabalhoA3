import os
import sqlite3

def get_caminho_db():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_db = os.path.join(base_dir, "pix.db")
    return caminho_db

def conectar():
    caminho_db = get_caminho_db()
    return sqlite3.connect(caminho_db)

def criar_banco():
    caminho_db = get_caminho_db()
    conn = sqlite3.connect(caminho_db)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chaves (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chave_pix TEXT NOT NULL UNIQUE,
            tipo TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    criar_banco()