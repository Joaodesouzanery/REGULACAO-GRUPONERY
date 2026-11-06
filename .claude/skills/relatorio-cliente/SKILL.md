---
name: relatorio-cliente
description: Gera o relatório da consultoria para um cliente a partir das perguntas da semana (pacote de N perguntas sobre diretores/agências/temas). Use quando o usuário disser «perguntas do cliente X», «relatório da semana», «dossiê pré-pauta» ou colar perguntas de cliente.
---
# Relatório para cliente (consultoria)

1. Salve as perguntas em `clientes/<cliente>/<AAAA-semNN>/perguntas.md` (uma por linha começando com `- `; opcional `[diretor: X] [tema: Y]`). `clientes/` NÃO vai para o GitHub.
2. Para cada pergunta, monte a ficha (skill `resposta-com-evidencia`) e grave em `clientes/<cliente>/<AAAA-semNN>/respostas/NN.md`. Revise: trecho literal relevante, links funcionando, números batendo com a planilha.
3. `python3 pipeline/relatorio.py clientes/<cliente>/<AAAA-semNN>` → `relatorio.docx` (capa, sumário executivo, uma seção por pergunta, anexo de metodologia/confiabilidade/cobertura).
4. Entregue o .docx ao usuário (ele é quem envia ao cliente). Registre no `clientes/<cliente>/historico.md` o que foi entregue.
5. Nunca invente: sem dado → diga que não temos e por quê (cobertura em `COBERTURA.md`).
