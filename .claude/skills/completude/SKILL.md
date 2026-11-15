---
name: completude
description: Painel de completude de TODAS as agências (ANTT, ANM, ANTAQ, ANEEL, ANP) — vídeos no canal × com texto × analisados, itens e votos, diretoria (foto ≥600, formação, minibio), superintendentes, mandatos confirmados e vagas, agenda/pautas, base de prazos, conferência cega e processos de clientes (SEI informado). Use quando perguntarem «temos tudo?», «qual a completude?», ao fim de cada lote do Mac e antes de vender/entregar.
---
1. `python3 pipeline/05_indexar.py` e `bash pipeline/ag.sh <ag> python3 pipeline/05_indexar.py` nas agências alteradas.
2. `python3 pipeline/completude.py` → imprime a tabela e grava COMPLETUDE.md (vai para o git).
3. Na resposta: mostre a tabela, diga o que falta e a ação (Mac/Whisper, pesquisador-dirigentes, pesquisador-mandatos, calendário, conferente-cego, pedir SEI ao cliente).
4. Documentos 3 e 4 (raio-X e agenda/comparativa) dependem de: calendário oficial (data/<ag>/calendario.json), pautas (pautas.py), processos com nº legível (prazos.py) e processos.json do cliente.
