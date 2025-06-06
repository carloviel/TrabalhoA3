import tkinter as tk
from tkinter import messagebox
import sqlite3

def conectar():
    return sqlite3.connect('pix.db')

def cadastrar_chave():
    chave = entrada_chave.get().strip()
    tipo = var_tipo.get()

    if not chave:
        messagebox.showwarning("Atenção", "Digite uma chave Pix.")
        return

    if not tipo:
        messagebox.showwarning("Atenção", "Selecione o tipo da chave.")
        return

    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM chaves WHERE chave_pix = ?", (chave,))
        if cursor.fetchone():
            messagebox.showinfo("Info", "Essa chave já está cadastrada.")
        else:
            cursor.execute("INSERT INTO chaves (chave_pix, tipo) VALUES (?, ?)", (chave, tipo))
            conn.commit()
            messagebox.showinfo("Sucesso", f"Chave '{chave}' cadastrada como {tipo} com sucesso.")
            entrada_chave.delete(0, tk.END)
            var_tipo.set(None)

        conn.close()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao cadastrar chave: {e}")

# Janela
janela = tk.Tk()
janela.title("Cadastro de Chave Pix")
janela.geometry("400x250")
janela.resizable(False, False)

# Widgets
tk.Label(janela, text="Nova chave Pix:", font=("Arial", 12)).pack(pady=10)
entrada_chave = tk.Entry(janela, width=40, font=("Arial", 11))
entrada_chave.pack()

tk.Label(janela, text="Tipo da chave:", font=("Arial", 12)).pack(pady=10)
var_tipo = tk.StringVar(value="suspeita")
tk.Radiobutton(janela, text="Confiável", variable=var_tipo, value="confiavel", font=("Arial", 11)).pack()
tk.Radiobutton(janela, text="Suspeita", variable=var_tipo, value="suspeita", font=("Arial", 11)).pack()

tk.Button(janela, text="Cadastrar", command=cadastrar_chave, bg="#28a745", fg="white", font=("Arial", 11)).pack(pady=15)

janela.mainloop()
