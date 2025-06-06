from db_config import conectar
import logging

def verificar_chave(chave_pix):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT tipo FROM chaves WHERE chave_pix = ?", (chave_pix,))
        resultado = cursor.fetchone()

        conexao.close()

        if resultado:
            tipo = resultado[0]
            logging.info(f"Verificação da chave '{chave_pix}': {tipo}")
            return tipo
        else:
            logging.info(f"Chave '{chave_pix}' não cadastrada.")
            return "nao_cadastrada"

    except Exception as e:
        logging.error(f"Erro ao verificar a chave '{chave_pix}': {e}")
        return "erro"
