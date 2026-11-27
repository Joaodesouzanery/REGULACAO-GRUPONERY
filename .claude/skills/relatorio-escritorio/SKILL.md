---
name: relatorio-escritorio
description: Relatório para escritório de advocacia ou cliente novo (agenda, como a diretoria votou em pautas parecidas, acompanhamento) com pipeline/relatorio_escritorio.py — com as 7 regras de qualidade que nasceram da revisão externa do relatório Lobo de Rizzo e a conferência obrigatória antes de enviar. Use em qualquer relatório para escritório, associação ou empresa nova.
---
# Relatório para escritório / cliente novo
`python3 pipeline/relatorio_escritorio.py "<Nome>" --marca <iris|circle|nery>` (marca: skill marca-relatorio). Temas por agência em `TEMAS` no script.

## Regras (todas obrigatórias)
1. **Empresas:** nomes normalizados e agrupados (aliases), só empresa privada; nunca órgão público, autoridade portuária, sindicato, associação ou pessoa.
2. **Diretoria:** só quem votou nas últimas reuniões; marcar titular/substituto; fim de mandato com fonte; avisar quando a posse não foi confirmada no DOU. Ordenar por data real.
3. **Interessado completo** (todas as empresas citadas) e **tipo do item**: ato da agência (homologação, sandbox, regulamento) × pedido da empresa.
4. **Percentual sempre com denominador e n escritos.** Divergência só entre itens **decididos** (fora retirados, vistas e pendentes).
5. **Prazos e retiradas:** mesma base no numerador e no denominador; n ao lado; «indicativo» se n < 10; período de início declarado.
6. **«Pendente» só se não houve decisão posterior**, inclusive por assunto parecido (nº de processo pode estar ilegível).
7. **Prospecção não entra no documento do cliente** (só com `--interno`, para uso nosso).
8. Sinais do escritório (assessoria, debêntures etc.) são aderência setorial, nunca «cliente» nem «representação».

## Antes de enviar (nada sai sem os três)
- `python3 pipeline/auditar_falas.py <html>` (trechos e minutos).
- Agente `auditor-respostas` (cada número com SQL próprio).
- Agente `conferente-final` (revisão externa: duplicidade, denominador, histórico × atual, pendente já decidido, marca).
Corrigir no gerador (não no PDF) e gerar de novo.
