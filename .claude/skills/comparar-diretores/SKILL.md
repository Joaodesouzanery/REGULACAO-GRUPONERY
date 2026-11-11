---
name: comparar-diretores
description: Perguntas que comparam diretores («quem diverge mais», «quem relata concessões», «como cada um vota em X») — resposta sempre com TODOS os diretores em exercício lado a lado (mesmos indicadores), e o PDF de diretoria/comparador. Use para qualquer pergunta «quem…» ou «compare os diretores».
---
1. Colegiado em exercício: `previsao.colegiado_atual(conn, 3)` (quem votou nas 3 últimas reuniões). Nunca omita um diretor.
2. Tabela com, para cada um: votos, relatorias, % acompanha o relator (quando não relata), divergências + vistas, temas em que mais relata, desfecho quando relata, presença — últimos 3 anos, ou no tema pedido (`item_temas`).
3. Uma evidência por diretor (RD, data, item, trecho, link &t=).
4. PDF: `python3 pipeline/relatorio_diretoria.py <ag> [saida] --perguntas perguntas.json` (cada pergunta = 1 página; métricas relata|diverge|desfecho|tema).
5. Termine com o bloco de cobertura.
