---
name: notas-ao-cliente
description: Caixa «O que observar» e selos de placar nos documentos do cliente — só notas que se aplicam aos processos e à agenda daquele cliente (reunião virtual de vários dias sem transmissão, item retirado/vista, mandato do relator, condicionante com prazo, acompanhamento previsto, vínculo entre processos), no máximo 5, por urgência. Use ao gerar qualquer documento de cliente ou quando a análise trouxer prazo/condição relevante.
---
# Notas ao cliente
- Código: `pipeline/notas_cliente.py` (`notas()`, `placar()`, `periodo()`); visual: `design.notas_box()`, `design.selo_placar()`, `design.agenda_cards()`.
- **Não mostrar tudo sempre**: a nota só aparece se o fato existe; máximo 5; ordem = data nos próximos 30 dias → muda placar → contexto. Uma linha cada, com data e ação.
- Tipos por cliente: `empresa.json` → `notas_ativas`. Fatos que só a leitura humana tira (condicionante de 180 dias, revisão em 2 anos, vínculo item → outro processo): `empresa.json` → `notas_manuais` [{tipo, data, texto}], datas calculadas marcadas «estimativa».
- Calendário: reunião virtual da ANTAQ = 3 dias sem transmissão (`calendario.json` → `dias`, `transmitida: false`); mostrar o período (ex.: «23, 24 e 25/11») e «resultado só na ata».
- Placar: «unânime 5×0», «maioria 4×1, vencida X», «retirado», «vista» — calculado dos votos e do resultado registrado; quando o resultado diz «vencida a relatora», a vencida é a relatora.
