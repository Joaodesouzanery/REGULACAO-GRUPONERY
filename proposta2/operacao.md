# Operação e lembretes automáticos

| Quando | O quê | Quem | Lembrete |
|---|---|---|---|
| Todo dia (auto) | pautas publicadas + DOU → alertas para clientes | nuvem | (futuro, `pautas.py`) |
| Toda segunda | coleta do YouTube no Mac (`caffeinate -i bash pipeline/coletar_tudo_e_enviar.sh …`), Whisper se houver, push | Mac do operador | tarefa agendada (push no celular) + `pendencias.py` |
| Toda semana | análise das reuniões novas, base, conferência por amostra | chat | mesma tarefa |
| Dia 1 | checagem da diretoria (skill `checagem-mensal`), PDFs de diretoria | chat | tarefa agendada dia 1 |
| Dia 25 | fechar o boletim mensal da agência | chat | tarefa agendada (quando o produto começar) |
| Sob demanda | perguntas, dossiês, comparativos, relatório por empresa | chat | — |

`python3 pipeline/pendencias.py` mostra o que está atrasado (coleta, Whisper, reuniões sem análise, checagem do mês, vídeos novos sem legenda).
