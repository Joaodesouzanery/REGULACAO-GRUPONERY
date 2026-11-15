---
name: agenda-pauta
description: Coleta e mostra pautas e calendário oficial das próximas reuniões de diretoria (gov.br) com pipeline/pautas.py. Use quando pedir «próximas reuniões», «pauta da ANTAQ», «quando o item X entra em pauta» ou na etapa 7 do montar-relatorio.
---
Comandos (script em construção; conferir `--help`):
- `python3 pipeline/pautas.py <ag>` — baixa e atualiza pautas/calendário publicados.
- `python3 pipeline/pautas.py <ag> --proximas 3` — próximas reuniões (calendário oficial em data/<ag>/calendario.json; padrões de URL em config_agencia.json → pautas_url).

Regras: só a data publicada no gov.br conta como oficial (citar o link e a data de consulta); sem pauta publicada, dizer «pauta ainda não publicada». O que o cliente informou (ex.: «retirado de pauta») fica separado do que a pauta/vídeo mostram. Item retirado ou com vista: buscar o minuto na transcrição da última reunião. Terminar com o bloco de cobertura.
