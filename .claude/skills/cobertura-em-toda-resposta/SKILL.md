---
name: cobertura-em-toda-resposta
description: OBRIGATÓRIA em toda resposta sobre diretor, agência, empresa ou assunto — confere o que a base cobre (reuniões no canal × com texto × analisadas, anos faltando, vídeos sem legenda/Whisper, datas de upload, taxa da conferência cega) e põe o bloco «Cobertura desta resposta» no fim. Use junto com resposta-com-evidencia e relatorio-cliente.
---
# Cobertura em toda resposta

1. Antes de responder, rode: `python3 pipeline/cobertura_resposta.py <agencia> ["Diretor"|-] [tema|-] [AAAA-AAAA]` (agências: antt, anm, antaq; outra → «não temos»).
2. Cole o bloco no fim da resposta (ou seção 6 da ficha) — `consulta.py ficha` já inclui.
3. Se o bloco mostrar ⚠️ (anos/eventos com texto ainda não analisados) ou «sem votos neste recorte», diga isso na **resposta curta**, não só no rodapé: «a resposta cobre 2019–2026; 2016–2018 ainda não analisados».
4. Nunca diga «a base está completa» sem este bloco. Completo = inventário do canal = texto = analisado; o que sobrar é lacuna declarada.
5. Em relatórios de cliente, a página «Como ler» e cada pergunta herdam a cobertura da agência/período da pergunta.
