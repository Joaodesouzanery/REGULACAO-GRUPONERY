---
name: atualizar-mandatos
description: Importa uma tabela de composição de diretorias (PDF/planilha de terceiros, como o «IRIS Diretorias e mandatos», página da agência ou DOU), compara com data/<ag>/mandatos.json e data/mandatos_agencias.json, aponta divergências e aplica as correções com fonte. Use quando o usuário mandar um documento de mandatos ou na checagem mensal.
---
# Atualizar mandatos
1. Leia o documento página por página; para cada agência liste titulares (nome completo, cargo, início, fim), vagas (ex-titular, desde, substituto) e o ato.
2. Compare com a base (`data/mandatos.json` ANTT, `data/<ag>/mandatos.json`, `vacancias.json`, `cadeiras.json`) e monte a tabela «nossa base × documento × ação».
3. Aplique: datas de início/posse/fim legal, `nome_completo`, `situacao` (afastado, interino), fechar quem saiu (fim + `obs` se aproximado), novos substitutos; campo `fonte_iris`/`fonte` com o documento e a data de posição.
4. Agências sem base de votos: só `data/mandatos_agencias.json` (12 agências) e `documentos/agencias/vacancia_12_agencias.md`.
5. Rode `python3 pipeline/vacancias.py`, `python3 pipeline/completude.py`; o `pesquisador-mandatos` confere no DOU o que mudou. Documento de terceiros é fonte secundária: diga isso quando usar.
