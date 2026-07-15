def ler_nota(mensagem):
    while True:
        try:
            nota = float(input(mensagem))
            if 0 <= nota <= 10:
                return nota
            else:
                print("Nota invalida! Digite um valor entre 0 e 10.")
        except ValueError:
            print("Entrada invalida! Digite um numero.")


def calcular_media(notas):
    return sum(notas) / len(notas)


def situacao(media):
    if media >= 7.0:
        return "APROVADO"
    elif media >= 5.0:
        return "RECUPERACAO"
    else:
        return "REPROVADO"


def main():
    print("=== Sistema de Notas dos Alunos ===\n")

    alunos = []

    while True:
        nome = input("Nome do aluno (ou 'fim' para encerrar): ").strip()
        if nome.lower() == "fim":
            break
        if not nome:
            print("Nome nao pode ser vazio.")
            continue

        try:
            qtd = int(input(f"Quantas notas para {nome}? "))
            if qtd <= 0:
                print("Digite pelo menos 1 nota.")
                continue
        except ValueError:
            print("Digite um numero valido.")
            continue

        notas = []
        for i in range(1, qtd + 1):
            nota = ler_nota(f"  Nota {i}: ")
            notas.append(nota)

        media = calcular_media(notas)
        status = situacao(media)

        alunos.append({"nome": nome, "notas": notas, "media": media, "status": status})
        print(f"  -> Media de {nome}: {media:.2f} | {status}\n")

    if not alunos:
        print("Nenhum aluno cadastrado.")
        return

    print("\n=== Relatorio Final ===")
    print(f"{'Aluno':<20} {'Media':>7}  {'Situacao'}")
    print("-" * 42)
    for a in alunos:
        print(f"{a['nome']:<20} {a['media']:>7.2f}  {a['status']}")

    medias = [a["media"] for a in alunos]
    print("-" * 42)
    print(f"Media geral da turma: {sum(medias) / len(medias):.2f}")


if __name__ == "__main__":
    main()
