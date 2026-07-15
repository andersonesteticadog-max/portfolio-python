import json
import os

ARQUIVO = "contatos.json"


def carregar_contatos():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_contatos(contatos):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(contatos, f, indent=2, ensure_ascii=False)


def adicionar_contato(contatos):
    nome = input("Nome: ").strip()
    if not nome:
        print("Nome nao pode ser vazio.\n")
        return
    telefone = input("Telefone: ").strip()
    email = input("Email: ").strip()
    contatos.append({"nome": nome, "telefone": telefone, "email": email})
    salvar_contatos(contatos)
    print(f"Contato adicionado: {nome}\n")


def listar_contatos(contatos):
    if not contatos:
        print("Nenhum contato cadastrado.\n")
        return
    print("\n=== Contatos ===")
    for i, c in enumerate(contatos, start=1):
        print(f"{i}. {c['nome']} | Tel: {c['telefone']} | Email: {c['email']}")
    print()


def buscar_contato(contatos):
    termo = input("Digite o nome (ou parte dele) para buscar: ").strip().lower()
    encontrados = [c for c in contatos if termo in c["nome"].lower()]
    if not encontrados:
        print("Nenhum contato encontrado.\n")
        return
    print("\n=== Resultado da busca ===")
    for c in encontrados:
        print(f"{c['nome']} | Tel: {c['telefone']} | Email: {c['email']}")
    print()


def editar_contato(contatos):
    listar_contatos(contatos)
    if not contatos:
        return
    try:
        num = int(input("Numero do contato para editar: "))
        if 1 <= num <= len(contatos):
            contato = contatos[num - 1]
            print(f"Deixe em branco para manter o valor atual.")
            novo_telefone = input(f"Telefone [{contato['telefone']}]: ").strip()
            novo_email = input(f"Email [{contato['email']}]: ").strip()
            if novo_telefone:
                contato["telefone"] = novo_telefone
            if novo_email:
                contato["email"] = novo_email
            salvar_contatos(contatos)
            print("Contato atualizado.\n")
        else:
            print("Numero invalido.\n")
    except ValueError:
        print("Digite um numero valido.\n")


def remover_contato(contatos):
    listar_contatos(contatos)
    if not contatos:
        return
    try:
        num = int(input("Numero do contato para remover: "))
        if 1 <= num <= len(contatos):
            removido = contatos.pop(num - 1)
            salvar_contatos(contatos)
            print(f"Contato removido: {removido['nome']}\n")
        else:
            print("Numero invalido.\n")
    except ValueError:
        print("Digite um numero valido.\n")


def menu():
    print("1 - Adicionar contato")
    print("2 - Listar contatos")
    print("3 - Buscar contato")
    print("4 - Editar contato")
    print("5 - Remover contato")
    print("6 - Sair")


def main():
    contatos = carregar_contatos()
    print("=== Agenda de Contatos ===\n")

    while True:
        menu()
        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            adicionar_contato(contatos)
        elif opcao == "2":
            listar_contatos(contatos)
        elif opcao == "3":
            buscar_contato(contatos)
        elif opcao == "4":
            editar_contato(contatos)
        elif opcao == "5":
            remover_contato(contatos)
        elif opcao == "6":
            print("Ate mais!")
            break
        else:
            print("Opcao invalida.\n")


if __name__ == "__main__":
    main()
