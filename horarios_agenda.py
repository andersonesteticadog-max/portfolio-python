# Inspirado num gap real do agente Luna (WhatsApp + CRM) que desenvolvo na
# Rostinger: hoje quem calcula horario livre e monta o resumo do agendamento
# e o LLM, "no olho". Aqui, as duas coisas viram funcao deterministica em
# Python, sem depender de IA acertar. Recriado do zero para o portfolio.
import json
import os
from datetime import datetime, timedelta

ARQUIVO = "agenda_horarios.json"
ABERTURA = 9
FECHAMENTO = 18
PASSO_MIN = 30
DIAS_SEMANA = ["Segunda-feira", "Terca-feira", "Quarta-feira", "Quinta-feira",
               "Sexta-feira", "Sabado", "Domingo"]

SERVICOS = [
    {"nome": "Banho Completo", "preco": 85.0, "duracao_min": 60},
    {"nome": "Tosa na Maquina", "preco": 130.0, "duracao_min": 90},
    {"nome": "Tosa na Tesoura", "preco": 150.0, "duracao_min": 120},
]


def carregar_agenda():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_agenda(agenda):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(agenda, f, indent=2, ensure_ascii=False)


def horarios_disponiveis(data, duracao_min, agenda):
    """Gera candidatos a cada PASSO_MIN dentro do expediente e descarta os
    que colidem com algum agendamento existente no dia (considerando a
    duracao de cada um, nao so o instante de inicio)."""
    abertura = datetime.strptime(f"{data} {ABERTURA:02d}:00", "%Y-%m-%d %H:%M")
    fechamento = datetime.strptime(f"{data} {FECHAMENTO:02d}:00", "%Y-%m-%d %H:%M")

    ocupados = []
    for a in agenda:
        if a["data_hora"].startswith(data):
            inicio = datetime.strptime(a["data_hora"], "%Y-%m-%d %H:%M")
            fim = inicio + timedelta(minutes=a["duracao_min"])
            ocupados.append((inicio, fim))

    livres = []
    candidato = abertura
    while candidato + timedelta(minutes=duracao_min) <= fechamento:
        fim_candidato = candidato + timedelta(minutes=duracao_min)
        conflito = any(candidato < fim_oc and inicio_oc < fim_candidato
                        for inicio_oc, fim_oc in ocupados)
        if not conflito:
            livres.append(candidato.strftime("%H:%M"))
        candidato += timedelta(minutes=PASSO_MIN)
    return livres


def gerar_resumo(tutor, telefone, pet, servico, data_hora):
    dt = datetime.strptime(data_hora, "%Y-%m-%d %H:%M")
    dia_semana = DIAS_SEMANA[dt.weekday()]
    linhas = [
        "=== Resumo do agendamento ===",
        f"Tutor: {tutor}",
        f"Telefone: {telefone}",
        f"Pet: {pet}",
        f"Servico: {servico['nome']}",
        f"Data: {dt.strftime('%d/%m/%Y')} ({dia_semana})",
        f"Horario: {dt.strftime('%H:%M')}",
        f"Valor: R${servico['preco']:.2f}",
    ]
    return "\n".join(linhas)


def escolher_servico():
    print("\n=== Servicos ===")
    for i, s in enumerate(SERVICOS, start=1):
        print(f"{i}. {s['nome']} | R${s['preco']:.2f} | {s['duracao_min']} min")
    try:
        num = int(input("Escolha o servico (numero): "))
        if 1 <= num <= len(SERVICOS):
            return SERVICOS[num - 1]
    except ValueError:
        pass
    print("Opcao invalida.\n")
    return None


def ver_horarios_livres(agenda):
    servico = escolher_servico()
    if not servico:
        return
    data = input("Data (AAAA-MM-DD): ").strip()
    try:
        dt = datetime.strptime(data, "%Y-%m-%d")
    except ValueError:
        print("Data invalida.\n")
        return
    if dt.weekday() == 6:
        print("Nao abrimos aos domingos.\n")
        return

    livres = horarios_disponiveis(data, servico["duracao_min"], agenda)
    if not livres:
        print(f"Nenhum horario livre em {data} para {servico['nome']}.\n")
    else:
        print(f"\nHorarios livres em {data} para {servico['nome']} "
              f"({servico['duracao_min']} min):")
        print(", ".join(livres) + "\n")


def fazer_agendamento(agenda):
    servico = escolher_servico()
    if not servico:
        return
    data = input("Data (AAAA-MM-DD): ").strip()
    try:
        dt = datetime.strptime(data, "%Y-%m-%d")
    except ValueError:
        print("Data invalida.\n")
        return
    if dt.weekday() == 6:
        print("Nao abrimos aos domingos.\n")
        return

    livres = horarios_disponiveis(data, servico["duracao_min"], agenda)
    if not livres:
        print(f"Nenhum horario livre em {data} para {servico['nome']}.\n")
        return
    print("Horarios livres:", ", ".join(livres))
    horario = input("Escolha um horario da lista acima: ").strip()
    if horario not in livres:
        print("Horario invalido ou indisponivel.\n")
        return

    tutor = input("Nome do tutor: ").strip()
    telefone = input("Telefone: ").strip()
    pet = input("Nome do pet: ").strip()
    if not (tutor and telefone and pet):
        print("Todos os campos sao obrigatorios.\n")
        return

    data_hora = f"{data} {horario}"
    agendamento = {
        "tutor": tutor, "telefone": telefone, "pet": pet,
        "servico": servico["nome"], "preco": servico["preco"],
        "duracao_min": servico["duracao_min"], "data_hora": data_hora,
    }
    agenda.append(agendamento)
    salvar_agenda(agenda)

    print()
    print(gerar_resumo(tutor, telefone, pet, servico, data_hora))
    print()


def listar_agendamentos(agenda):
    if not agenda:
        print("Nenhum agendamento.\n")
        return
    print("\n=== Agendamentos ===")
    for i, a in enumerate(agenda, start=1):
        print(f"{i}. {a['data_hora']} | {a['pet']} ({a['tutor']}) | {a['servico']}")
    print()


def menu():
    print("1 - Listar servicos")
    print("2 - Ver horarios livres num dia")
    print("3 - Fazer agendamento")
    print("4 - Listar agendamentos")
    print("5 - Sair")


def main():
    agenda = carregar_agenda()
    print("=== Agenda com Calculo de Horarios Livres ===\n")

    while True:
        menu()
        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            print()
            for s in SERVICOS:
                print(f"- {s['nome']} | R${s['preco']:.2f} | {s['duracao_min']} min")
            print()
        elif opcao == "2":
            ver_horarios_livres(agenda)
        elif opcao == "3":
            fazer_agendamento(agenda)
        elif opcao == "4":
            listar_agendamentos(agenda)
        elif opcao == "5":
            print("Ate mais!")
            break
        else:
            print("Opcao invalida.\n")


if __name__ == "__main__":
    main()
