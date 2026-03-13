import random
import string
import os
from config import PASTA_DOWNLOADS

NOMES_BR = [
    "miguel", "arthur", "gael", "heitor", "helena", "alice", "theo", "laura", 
    "davi", "gabriel", "lucas", "matheus", "gustavo", "felipe", "rodrigo", "bruno",
    "marcos", "jose", "carlos", "andre", "luiz", "marcelo", "jorge", "antonio"
]

def formatar_texto(texto, modo_case):
    if modo_case == 'upper': return texto.upper()
    if modo_case == 'capitalize': return texto.capitalize()
    return texto.lower()

def gerar_combo_arquivo(tipo, qtd, len_user, len_pass, case_mode, pass_mode):
    filename = f"combo_{tipo}_{qtd}linhas_{int(random.random()*1000)}.txt"
    filepath = os.path.join(PASTA_DOWNLOADS, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        for _ in range(qtd):
            usuario = ""
            if tipo == "nome_num":
                base = formatar_texto(random.choice(NOMES_BR), case_mode)
                qtd_numeros = max(1, len_user - len(base))
                usuario = f"{base}{''.join(random.choices(string.digits, k=qtd_numeros))}"
            elif tipo == "numerico":
                usuario = ''.join(random.choices(string.digits, k=len_user))
            elif tipo == "letras":
                base = ''.join(random.choices(string.ascii_letters, k=len_user))
                usuario = formatar_texto(base, case_mode)
            elif tipo == "alfa":
                chars = string.ascii_letters + string.digits
                base = ''.join(random.choices(chars, k=len_user))
                usuario = formatar_texto(base, case_mode) if not base.isdigit() else base
            else:
                usuario = "user" + ''.join(random.choices(string.digits, k=4))

            senha = ''.join(random.choices(string.ascii_letters + string.digits, k=len_pass))
            senha = formatar_texto(senha, pass_mode)
            f.write(f"{usuario}:{senha}\n")

    return filepath
  
