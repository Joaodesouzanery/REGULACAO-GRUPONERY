---
name: monitoramento-8-blocos
description: Gera o documento «Monitoramento de processos — os 8 blocos» (visão geral, mapeamento, prazo, agenda, agência, busca, comparativa, visão do cliente) para 1–3 processos de um cliente com pipeline/monitor_8blocos.py. Use quando pedirem acompanhamento de processos específicos ou o 5º documento do pacote.
---
# Monitoramento em 8 blocos
`python3 pipeline/monitor_8blocos.py clientes/<x>/<pasta> "<proc>,<relacionados>" "<proc2>,..."`
- Agrupe o processo principal com recursos/embargos/desdobramentos (aliases em `desfechos_manuais.json`).
- O que depende do SEI aparece como «a informar pelo cliente» (preencha `processos.json` quando o cliente mandar).
- Antes de entregar: avisos de densidade/estouro zerados, `auditar_falas.py` sem «não encontrado», `revisor-visual`.
