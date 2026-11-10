---
name: relatorio-empresa
description: Relatório por EMPRESA cliente (até 3 agências: ANTT, ANM, ANTAQ) no formato capa da empresa → processos e calendário → diretoria (minibio, mandato) → decisões setoriais → previsão (placar e % com backtest) → cobertura. Use quando o usuário der o nome/CNPJ de uma empresa ou pedir «relatório da empresa X».
---
# Relatório por empresa

1. Crie `clientes/<cliente>/<pasta>/empresa.json`: `{"nome", "cnpj", "aliases": [nomes, siglas, ativos — ex.: «Vitória a Minas», «Ponta da Madeira»], "agencias": [≤ 3]}`. Teste os aliases com `python3 pipeline/previsao.py <ag> "a1|a2"` (nº de itens) e retire os que pegam outra empresa.
2. Gere: `python3 pipeline/relatorio_empresa.py clientes/<cliente>/<pasta>` → PDF 16:9 (~6–12 págs).
3. Fontes: votos/itens (base), `desfecho.py`, `previsao.py` (taxa de acompanhar o relator por diretor nos temas da empresa, últimos 3 anos, prior 97%; backtest 2025–26), `mandatos.json`, `vacancias.json`, `bios.json` (minibios com fontes — pesquisador-mandatos), cobertura.
4. Antes de entregar: `revisor-visual` e `auditor-respostas`. Diga: nº de processo vem da legenda (conferir no SEI); superintendentes ainda não incluídos; calendário só tem fatos datados (mandatos, vagas, pendências) — pautas futuras não publicadas não entram; CNPJ informado pelo cliente.
