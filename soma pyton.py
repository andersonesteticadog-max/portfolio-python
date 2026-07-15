import os
from datetime import date

# ─── Suas informações ───────────────────────────────────────────────
nome = "Anderson"  # troque pelo seu nome

# ─── Data de hoje (automático) ──────────────────────────────────────
hoje = date.today()
data_formatada = hoje.strftime("20/05/2026")  # ex: 11/05/2026

# ─── Contar arquivos de uma pasta ───────────────────────────────────
pasta = "C:/Users/SeuNome/Downloads"  # começa na sua pasta pessoal

try:
    todos_itens = os.listdir(pasta)
    total_arquivos = sum(
        1 for item in todos_itens
        if os.path.isfile(os.path.join(pasta, item))
    )
except PermissionError:
    total_arquivos = 0
    print("Aviso: sem permissão para ler a pasta.")

# ─── Exibir tudo formatado ──────────────────────────────────────────
print("=" * 40)
print("       MEU PRIMEIRO SCRIPT PYTHON")
print("=" * 40)
print(f"  Usuário  : {nome}")
print(f"  Data     : {data_formatada}")
print(f"  Pasta    : {pasta}")
print(f"  Arquivos : {total_arquivos} encontrados")
print("=" * 40)

