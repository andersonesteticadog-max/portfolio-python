# Portfolio Python

Exercícios de Python organizados em ordem crescente de complexidade, do básico
até scripts com validação de regras de negócio e algoritmos de agenda.

## Scripts

| Script | O que mostra |
|---|---|
| [`media_alunos.py`](media_alunos.py) | Funções, laços, tratamento de erro (`try`/`except`) e geração de relatório |
| [`lista_tarefas.py`](lista_tarefas.py) | CRUD simples com persistência em arquivo JSON |
| [`agenda_contatos.py`](agenda_contatos.py) | CRUD completo (adicionar, listar, buscar, editar, remover) com JSON |
| [`agendador_servicos.py`](agendador_servicos.py) | Busca fuzzy de serviço (tokenização, normalização, desempate) e validações de negócio (telefone, data, conflito de horário) |
| [`horarios_agenda.py`](horarios_agenda.py) | Cálculo de horários livres por sobreposição de intervalos e geração determinística de resumo de agendamento |

## Como rodar

Requer apenas Python 3 (biblioteca padrão, sem dependências externas):

```
python3 <nome_do_script>.py
```

Cada script é interativo via terminal (menu numerado) e alguns persistem dados
em arquivo `.json` na mesma pasta (ignorado pelo git).

## Autor

Anderson
