import tkinter as tk
from tkinter import ttk, messagebox
import logging
from db_config import conectar
from verificar import verificar_chave

# Configuração do logging
logging.basicConfig(
    filename='../logs.txt',  # salva uma pasta acima
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Função para validar chave
def validar():
    chave = entrada_validacao.get().strip()

    if not chave:
        messagebox.showwarning("Atenção", "Digite uma chave Pix.")
        return

    resultado = verificar_chave(chave)

    if resultado == "suspeita":
        messagebox.showerror("Perigo!", "Essa chave está na lista negra. Transação bloqueada.")
        logging.warning(f"Bloqueio de transação para chave suspeita: {chave}")
    elif resultado == "confiavel":
        messagebox.showinfo("Sucesso", "Chave confiável. Transação autorizada.")
        logging.info(f"Transação aprovada para chave confiável: {chave}")
    elif resultado == "nao_cadastrada":
        resposta = messagebox.askyesno("Chave desconhecida", "Essa chave não está cadastrada. Deseja continuar?")
        if resposta:
            messagebox.showinfo("Prosseguir", "Transação autorizada mesmo sem cadastro.")
            logging.info(f"Transação autorizada para chave não cadastrada: {chave}")
        else:
            messagebox.showinfo("Cancelado", "Transação cancelada.")
            logging.info(f"Transação cancelada pelo usuário para chave: {chave}")
    else:
        messagebox.showerror("Erro", "Erro ao verificar a chave. Verifique os logs.")
        logging.error(f"Erro inesperado ao verificar a chave: {chave}")

# Função para cadastrar chave

def cadastrar_chave():
    chave = entrada_cadastro.get().strip()
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
            messagebox.showinfo("Sucesso", f"Chave '{chave}' cadastrada como {tipo}.")
            entrada_cadastro.delete(0, tk.END)
            var_tipo.set(None)

        conn.close()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao cadastrar chave: {e}")

# Janela principal
janela = tk.Tk()
janela.title("Sistema Pix - Interface Completa")
janela.geometry("420x300")
janela.resizable(False, False)

abas = ttk.Notebook(janela)

# === Aba Cadastro ===
aba_cadastro = ttk.Frame(abas)
abas.add(aba_cadastro, text='Cadastrar Chave')

tk.Label(aba_cadastro, text="Nova chave Pix:", font=("Arial", 12)).pack(pady=10)
entrada_cadastro = tk.Entry(aba_cadastro, width=40, font=("Arial", 11))
entrada_cadastro.pack()

tk.Label(aba_cadastro, text="Tipo da chave:", font=("Arial", 12)).pack(pady=10)
var_tipo = tk.StringVar(value='suspeita')
tk.Radiobutton(aba_cadastro, text="Confiável", variable=var_tipo, value="confiavel", font=("Arial", 11)).pack()
tk.Radiobutton(aba_cadastro, text="Suspeita", variable=var_tipo, value="suspeita", font=("Arial", 11)).pack()

tk.Button(aba_cadastro, text="Cadastrar", command=cadastrar_chave, bg="#28a745", fg="white", font=("Arial", 11)).pack(pady=15)

# === Aba Validação ===
aba_validacao = ttk.Frame(abas)
abas.add(aba_validacao, text='Validar Transação')

tk.Label(aba_validacao, text="Digite a chave Pix:", font=("Arial", 12)).pack(pady=20)
entrada_validacao = tk.Entry(aba_validacao, width=40, font=("Arial", 11))
entrada_validacao.pack()

tk.Button(aba_validacao, text="Verificar", command=validar, bg="#0078D7", fg="white", font=("Arial", 11)).pack(pady=20)

# Exibir as abas
abas.pack(expand=True, fill="both")

janela.mainloop()
