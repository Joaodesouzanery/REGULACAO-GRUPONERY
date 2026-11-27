---
name: monitoramento-continuo
description: Produto de Monitoramento Contínuo (Radar de Previsibilidade) por cliente — config em data/radar/<slug>.json, Radar semanal com pipeline/radar.py, alertas no mesmo dia, e-mails automáticos para joaodsouzanery@gmail.com e neryadministrativo@gmail.com pelas tarefas agendadas. Use ao ativar cliente novo, quando a tarefa agendada disparar, ou quando pedirem «radar», «monitoramento», «alerta».
---
# Monitoramento contínuo (Radar)
## Ativar um cliente (1 dia)
1. Perguntar a marca (skill marca-relatorio).
2. Criar `data/radar/<slug>.json` (só dado público): nome, marca, agências, regex de temas e de empresas por agência, nºs de processo públicos, e-mails internos. Processos sigilosos ou estratégia do cliente ficam em `clientes/` (fora do git), nunca aqui.
3. Rodar `python3 pipeline/radar.py <slug>` e conferir (auditor-respostas + conferente-final).

## Rotina automática
- **Mac (seg e qui 09:00, `instalar_agendamento_mac.sh`)**: `monitorar.sh` = `pautas_mac.py` (calendário, pautas e consultas em bruto) + `coletar_todas.sh` (vídeos novos) → GitHub.
- **Nuvem, sexta (tarefa agendada «Radar semanal»)**:
  1. `git pull`; extrair dos brutos novos (`data/<ag>/brutos/<data>/`) o `calendario.json`, `pautas/<n>.json` e `consultas.json` (ler PDFs/HTML; só dado oficial, com fonte).
  2. Analisar só reuniões novas (`.md` sem `.analise.json`) com analista-reuniao em **Sonnet**; validar; indexar.
  3. Para cada `data/radar/*.json`: `python3 pipeline/radar.py <slug>`; conferir; mandar e-mail (conector Gmail) para os dois endereços com o resumo `.md` no corpo e o PDF descrito/anexado.
  4. Commit e push (o PDF fica em `clientes/`, fora do git).
- **Nuvem, dias úteis 18h (tarefa «Alerta diário»)**: `git pull`; extrair brutos novos; `python3 pipeline/radar.py <slug> --novidades` (código 3 = sem novidade → não manda nada); se houver alerta, e-mail curto com os alertas.
## Limites
- O alerta diário usa pauta, calendário, mandatos e a base atual; a leitura do vídeo novo entra na sexta.
- Só fatos com fonte; nunca hipótese de motivo para retirada (skill previsibilidade-regulatoria).
- O envio ao cliente final passa pelo usuário.
