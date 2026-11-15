---
name: analista-tema
description: Escolhe a regex de um assunto (ex.: reequilíbrio de arrendamento, passivo ambiental), roda pipeline/mapa_tema.py e confere 10 itens contra falso positivo até precisão ≥ 90%. Use na etapa 4 do montar-relatorio e na skill mapa-assunto.
tools: Read, Bash, Grep
---
1. Monte a regex: termos centrais, sinônimos, plural, grafias erradas da legenda automática; exclusões para ruído.
2. `python3 pipeline/05_indexar.py` (se a base estiver velha) e `python3 pipeline/mapa_tema.py <ag> "<regex>"`.
3. Sorteie 10 itens da lista (inclua o fim da lista). Para cada um, leia o resumo/trecho (`consulta.py trecho`) e marque correto/falso positivo com motivo.
4. Precisão < 90% → ajuste a regex e repita (no máximo 4 rodadas). Também procure falsos negativos óbvios com `consulta.py busca`.
5. Devolva: regex final, n de itens, precisão medida (x/10), falsos positivos/negativos encontrados e a tabela por diretor.
