---
description: Monta o relatório da semana para um cliente (N perguntas → PDF Circle de ~13 páginas, auditado)
argument-hint: "<cliente> <pasta-ou-perguntas>"
---
Pedido: $ARGUMENTS

Siga as skills `relatorio-cliente` e `relatorio-visual`: escreva `clientes/<cliente>/<data>/perguntas.md` (com tags [agencia][diretor][tema][setor]) e uma resposta por pergunta em `respostas/NN.md`; rode o subagente `auditor-respostas` e corrija; gere `python3 pipeline/relatorio_v2.py <pasta> --titulo … --agencia …`; rode o subagente `revisor-visual`; entregue o PDF. `clientes/` nunca vai ao GitHub.
