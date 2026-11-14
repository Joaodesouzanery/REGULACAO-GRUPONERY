---
name: previsao-voto
description: Previsão de voto e placar para um item futuro com pipeline/previsao.py + mapa_tema.py, sempre com backtest, n por diretor e rótulo «inferência». Use quando pedir «como deve votar», «placar provável» ou na etapa 6 do montar-relatorio.
---
1. Mapa do assunto primeiro (skill mapa-assunto, precisão ≥ 90%).
2. `python3 pipeline/previsao.py <ag> "<alias1|alias2>"` (placar + backtest 2025–26 já incluído) e, por assunto, `python3 pipeline/mapa_tema.py <ag> "<regex>"` (prior padrão 97% de acompanhar o relator, peso 10).
3. Exigir no texto: **backtest** (acerto em decisões passadas, n), **n por diretor** no assunto, intervalo/probabilidade, quem é o relator e o rótulo **«inferência — estimativa estatística, não substitui publicação oficial nem orientação jurídica»**.
4. n < 5 para um diretor → dizer «amostra insuficiente» e usar só o padrão geral, avisando.
5. Previsão específica de cliente é **confidencial**: nunca em material de divulgação.
6. Agente **auditor-previsao** confere antes de entrar em qualquer relatório.
