---
name: transparencia-agencias
description: Avalia e compara a TRANSPARÊNCIA e a FACILIDADE de acompanhar cada agência reguladora (vídeos das reuniões, legenda, pautas e atas publicadas, calendário, votos por escrito, composição e currículos, sigilo, reuniões virtuais sem transmissão) e gera o quadro comparativo docs/transparencia_agencias.md. Use para material comercial, relatório de setor ou quando perguntarem «qual agência é mais transparente/fácil de acompanhar».
---
# Transparência das agências
1. Agente `auditor-transparencia` por agência, com os critérios abaixo (nota 0–2 cada, com evidência e URL; dado da base quando houver):
   - **Reuniões transmitidas** (% de reuniões de diretoria com vídeo público; base: videos.jsonl × calendário/atas)
   - **Legenda disponível** (% com legenda; base: transcrições × «SEM_LEGENDA»)
   - **Pauta antecipada** (publicada com quantos dias; formato legível)
   - **Atas e votos escritos** (publicados? em quanto tempo?)
   - **Calendário anual** (existe? cumprido?)
   - **Composição e currículos** (página com diretores, mandatos, substitutos, lista tríplice)
   - **Sigilo** (% de itens sigilosos ou reuniões virtuais sem transmissão)
   - **Facilidade** (busca, dados abertos, links estáveis, bloqueio a robôs)
2. `python3 pipeline/transparencia.py` junta as notas (`data/<ag>/transparencia.json`) e escreve `docs/transparencia_agencias.md` (tabela comparativa + ranking + ressalvas). Números da base entram automaticamente.
3. Nada de nota sem evidência; diferencie «não existe» de «não encontrado».
