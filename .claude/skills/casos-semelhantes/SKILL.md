---
name: casos-semelhantes
description: Lista precedentes (decisões semelhantes) para um item ou processo, com voto de cada diretor, resultado e link no minuto, usando pipeline/similares.py. Use quando pedir «casos parecidos», «precedentes», «outras iniciativas» ou na etapa 5 do montar-relatorio.
---
- `python3 pipeline/similares.py <ag> "<texto do item ou regex>" [--n 20] [--empresa "<regex>"]`
- Alternativa: a seção «decisões semelhantes» de `python3 pipeline/mapa_tema.py <ag> "<regex>"`.

Pronto quando: ≥ 5 precedentes com reunião, data, item, relator, resultado, votos divergentes e link `&t=`. Conferir manualmente os 5 primeiros contra falso positivo (assunto realmente igual?). Dizer o critério de semelhança, o n e que a legenda automática pode errar nomes e valores. Terminar com cobertura.
