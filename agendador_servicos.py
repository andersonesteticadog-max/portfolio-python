# Inspirado no motor de casamento de servico e nas validacoes deterministicas
# do agente Luna (WhatsApp + CRM) que desenvolvo na Rostinger, recriado do
# zero e simplificado para fins de portfolio.
import json
import os
import re
import unicodedata
from datetime import datetime

ARQUIVO = "agendamentos.json"
HORARIO_ABERTURA = 9
HORARIO_FECHAMENTO = 18
STOP_WORDS = {"de", "da", "do", "e", "com", "para", "pra", "o", "a"}

SERVICOS = [
    {"nome": "Banho Completo - Pequeno", "preco": 75.0, "duracao_min": 60},
    {"nome": "Banho Completo - Grande", "preco": 95.0, "duracao_min": 60},
    {"nome": "Tosa na Maquina - Pequeno", "preco": 100.0, "duracao_min": 90},
    {"nome": "Tosa na Maquina - Grande", "preco": 140.0, "duracao_min": 90},
    {"nome": "Tosa na Tesoura - Pequeno", "preco": 120.0, "duracao_min": 120},
    {"nome": "Tosa na Tesoura - Grande", "preco": 160.0, "duracao_min": 120},
]


def normalizar(texto):
    texto = unicodedata.normalize("NFD", (texto or "").strip().lower())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


def tokenizar(texto):
    return [t for t in re.split(r"[^a-z0-9]+", normalizar(texto)) if t and t not in STOP_WORDS]


def buscar_servico(nome_busca, porte=None):
    consulta = set(tokenizar(nome_busca))
    if not consulta:
        return "nao_encontrado", None

    for s in SERVICOS:
        if normalizar(s["nome"]) == normalizar(nome_busca):
            return "ok", s

    pontuados = []
    for s in SERVICOS:
        palavras_servico = set(tokenizar(s["nome"]))
        sobreposicao = len(consulta & palavras_servico)
        if sobreposicao:
            pontuados.append((sobreposicao, -len(palavras_servico - consulta), s))

    if not pontuados:
        return "nao_encontrado", None

    pontuados.sort(key=lambda item: (item[0], item[1]), reverse=True)
    melhor_pontuacao = pontuados[0][:2]
    vencedores = [s for pontos in pontuados if pontos[:2] == melhor_pontuacao for s in [pontos[2]]]

    if len(vencedores) > 1 and porte:
        por_porte = [v for v in vencedores if normalizar(porte) in tokenizar(v["nome"])]
        if por_porte:
            vencedores = por_porte

    if len(vencedores) == 1:
        return "ok", vencedores[0]
    return "ambiguo", [v["nome"] for v in vencedores]


def carregar_agendamentos():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_agendamentos(agendamentos):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(agendamentos, f, indent=2, ensure_ascii=False)


def validar_telefone(telefone):
    digitos = re.sub(r"\D", "", telefone or "")
    return digitos if 10 <= len(digitos) <= 11 else None


def validar_data_hora(texto):
    try:
        dh = datetime.strptime(texto, "%Y-%m-%d %H:%M")
    except ValueError:
        return None, "Formato invalido. Use AAAA-MM-DD HH:MM."
    if dh < datetime.now():
        return None, "Essa data/hora ja passou."
    if dh.weekday() == 6:
        return None, "Nao abrimos aos domingos."
    if not (HORARIO_ABERTURA <= dh.hour < HORARIO_FECHAMENTO):
        return None, f"Horario de funcionamento: {HORARIO_ABERTURA}h as {HORARIO_FECHAMENTO}h."
    return dh, None


def existe_conflito(agendamentos, data_hora):
    return any(a["data_hora"] == data_hora.strftime("%Y-%m-%d %H:%M") for a in agendamentos)


def agendar(agendamentos, cliente_nome, telefone, pet_nome, porte, nome_servico, data_hora_texto):
    tel = validar_telefone(telefone)
    if not tel:
        return {"ok": False, "erro": "Telefone invalido (informe DDD + numero)."}

    dh, erro = validar_data_hora(data_hora_texto)
    if erro:
        return {"ok": False, "erro": erro}

    if existe_conflito(agendamentos, dh):
        return {"ok": False, "erro": "Ja existe um agendamento nesse horario."}

    status, resultado = buscar_servico(nome_servico, porte)
    if status == "ambiguo":
        return {"ok": False, "erro": "Servico ambiguo.", "opcoes": resultado}
    if status == "nao_encontrado":
        return {"ok": False, "erro": f"Servico '{nome_servico}' nao encontrado.",
                "servicos_disponiveis": [s["nome"] for s in SERVICOS]}

    agendamento = {
        "cliente_nome": cliente_nome,
        "telefone": tel,
        "pet_nome": pet_nome,
        "servico": resultado["nome"],
        "preco": resultado["preco"],
        "data_hora": dh.strftime("%Y-%m-%d %H:%M"),
    }
    agendamentos.append(agendamento)
    salvar_agendamentos(agendamentos)
    return {"ok": True, "agendamento": agendamento}


def listar_servicos():
    print("\n=== Servicos ===")
    for s in SERVICOS:
        print(f"- {s['nome']} | R${s['preco']:.2f} | {s['duracao_min']} min")
    print()


def testar_busca():
    nome = input("Digite o nome do servico (pode ser incompleto): ").strip()
    porte = input("Porte do pet (Pequeno/Grande, opcional): ").strip() or None
    status, resultado = buscar_servico(nome, porte)
    if status == "ok":
        print(f"Encontrado: {resultado['nome']} (R${resultado['preco']:.2f})\n")
    elif status == "ambiguo":
        print(f"Ambiguo, opcoes: {', '.join(resultado)}\n")
    else:
        print("Nenhum servico encontrado.\n")


def fazer_agendamento(agendamentos):
    cliente_nome = input("Nome do tutor: ").strip()
    telefone = input("Telefone (com DDD): ").strip()
    pet_nome = input("Nome do pet: ").strip()
    porte = input("Porte do pet (Pequeno/Grande): ").strip()
    nome_servico = input("Servico desejado: ").strip()
    data_hora_texto = input("Data e hora (AAAA-MM-DD HH:MM): ").strip()

    resultado = agendar(agendamentos, cliente_nome, telefone, pet_nome, porte, nome_servico, data_hora_texto)
    if resultado["ok"]:
        a = resultado["agendamento"]
        print(f"\nAgendado! {a['pet_nome']} - {a['servico']} em {a['data_hora']} "
              f"(R${a['preco']:.2f})\n")
    else:
        print(f"\nNao foi possivel agendar: {resultado['erro']}")
        if "opcoes" in resultado:
            print("Opcoes:", ", ".join(resultado["opcoes"]))
        if "servicos_disponiveis" in resultado:
            print("Disponiveis:", ", ".join(resultado["servicos_disponiveis"]))
        print()


def listar_agendamentos(agendamentos):
    if not agendamentos:
        print("Nenhum agendamento.\n")
        return
    print("\n=== Agendamentos ===")
    for i, a in enumerate(agendamentos, start=1):
        print(f"{i}. {a['data_hora']} | {a['pet_nome']} ({a['cliente_nome']}) | "
              f"{a['servico']} | R${a['preco']:.2f}")
    print()


def cancelar_agendamento(agendamentos):
    listar_agendamentos(agendamentos)
    if not agendamentos:
        return
    try:
        num = int(input("Numero do agendamento para cancelar: "))
        if 1 <= num <= len(agendamentos):
            removido = agendamentos.pop(num - 1)
            salvar_agendamentos(agendamentos)
            print(f"Cancelado: {removido['pet_nome']} - {removido['servico']}\n")
        else:
            print("Numero invalido.\n")
    except ValueError:
        print("Digite um numero valido.\n")


def menu():
    print("1 - Listar servicos")
    print("2 - Testar busca de servico (nome incompleto)")
    print("3 - Fazer agendamento")
    print("4 - Listar agendamentos")
    print("5 - Cancelar agendamento")
    print("6 - Sair")


def main():
    agendamentos = carregar_agendamentos()
    print("=== Agendador de Servicos (Pet Shop) ===\n")

    while True:
        menu()
        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            listar_servicos()
        elif opcao == "2":
            testar_busca()
        elif opcao == "3":
            fazer_agendamento(agendamentos)
        elif opcao == "4":
            listar_agendamentos(agendamentos)
        elif opcao == "5":
            cancelar_agendamento(agendamentos)
        elif opcao == "6":
            print("Ate mais!")
            break
        else:
            print("Opcao invalida.\n")


if __name__ == "__main__":
    main()
