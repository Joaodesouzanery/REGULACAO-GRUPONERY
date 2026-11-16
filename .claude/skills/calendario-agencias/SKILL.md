---
name: calendario-agencias
description: Cadastra e mantém o calendário oficial de reuniões de diretoria e as pautas publicadas de TODAS as agências (ANTT, ANM, ANTAQ, ANEEL, ANP) em data/<ag>/calendario.json e data/<ag>/pautas/. Use no dia 1, quando sair pauta nova, ou se a completude mostrar «0 / — / 0» na agenda.
---
# Calendário e pautas
1. Agente `pesquisador-calendario` (por agência): acha a página oficial do calendário de reuniões e de pautas (gov.br/<ag>), baixa o PDF/HTML e devolve as datas do semestre (reunião nº, data, hora, formato: presencial/telepresencial/virtual, transmitida ou não) com URL de fonte.
2. Grave `data/<ag>/calendario.json` (mesmo formato da ANTAQ: `{reuniao, data, formato, fonte}`).
3. Pautas: `python3 pipeline/pautas.py <ag>` (parser da ANTAQ; para outra agência adapte o padrão de item/relator/processo em pautas.py e registre o formato aqui).
4. Se o gov.br não abrir da nuvem, peça ao usuário rodar no Mac ou colar o PDF. Nunca inventar data.
5. Atualize `python3 pipeline/completude.py`.
