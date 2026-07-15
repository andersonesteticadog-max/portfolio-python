import json
import os

ARQUIVO = "tarefas.json"


def carregar_tarefas():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_tarefas(tarefas):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(tarefas, f, indent=2, ensure_ascii=False)


def adicionar_tarefa(tarefas):
    descricao = input("Descricao da tarefa: ").strip()
    if not descricao:
        print("Descricao nao pode ser vazia.\n")
        return
    tarefas.append({"descricao": descricao, "concluida": False})
    salvar_tarefas(tarefas)
    print(f"Tarefa adicionada: {descricao}\n")


def listar_tarefas(tarefas):
    if not tarefas:
        print("Nenhuma tarefa cadastrada.\n")
        return
    print("\n=== Tarefas ===")
    for i, t in enumerate(tarefas, start=1):
        status = "[X]" if t["concluida"] else "[ ]"
        print(f"{i}. {status} {t['descricao']}")
    print()


def concluir_tarefa(tarefas):
    listar_tarefas(tarefas)
    if not tarefas:
        return
    try:
        num = int(input("Numero da tarefa concluida: "))
        if 1 <= num <= len(tarefas):
            tarefas[num - 1]["concluida"] = True
            salvar_tarefas(tarefas)
            print("Tarefa marcada como concluida.\n")
        else:
            print("Numero invalido.\n")
    except ValueError:
        print("Digite um numero valido.\n")


def remover_tarefa(tarefas):
    listar_tarefas(tarefas)
    if not tarefas:
        return
    try:
        num = int(input("Numero da tarefa para remover: "))
        if 1 <= num <= len(tarefas):
            removida = tarefas.pop(num - 1)
            salvar_tarefas(tarefas)
            print(f"Tarefa removida: {removida['descricao']}\n")
        else:
            print("Numero invalido.\n")
    except ValueError:
        print("Digite um numero valido.\n")


def menu():
    print("1 - Adicionar tarefa")
    print("2 - Listar tarefas")
    print("3 - Concluir tarefa")
    print("4 - Remover tarefa")
    print("5 - Sair")


def main():
    tarefas = carregar_tarefas()
    print("=== Lista de Tarefas ===\n")

    while True:
        menu()
        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            adicionar_tarefa(tarefas)
        elif opcao == "2":
            listar_tarefas(tarefas)
        elif opcao == "3":
            concluir_tarefa(tarefas)
        elif opcao == "4":
            remover_tarefa(tarefas)
        elif opcao == "5":
            print("Ate mais!")
            break
        else:
            print("Opcao invalida.\n")


if __name__ == "__main__":
    main()
