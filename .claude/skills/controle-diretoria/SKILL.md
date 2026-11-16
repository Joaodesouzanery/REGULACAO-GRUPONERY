---
name: controle-diretoria
description: Monta e mantém o controle da diretoria por cadeira (como o painel da ANTT) para cada agência — data/<ag>/cadeiras.json com cadeira, ocupantes, nº do mandato, titular/substituto, decreto, posse, saída, vagas, ex-diretores e lista tríplice — e o quadro «Controle da diretoria» no relatório. Use ao iniciar agência, quando entra/sai diretor ou na checagem mensal.
---
# Controle da diretoria
1. Agente `pesquisador-mandatos` com o pedido «formato cadeiras.json» (modelo: `data/antaq/cadeiras.json`), a partir de `mandatos.json`/`vacancias.json` + Senado + DOU + página da agência. Campos sem fonte: `a_confirmar: true`.
2. O quadro sai sozinho no relatório (`design.quadro_mandatos(..., ex=True)`): atual em azul, ex em cinza, substitutos em lilás, vago hachurado, faixa «Saíram do colegiado».
3. Confirmar no DOU os campos `a_confirmar` (skill `lacunas-agencias`).
4. Agências feitas: ANTAQ. Pendentes: ANTT, ANM, ANEEL.
