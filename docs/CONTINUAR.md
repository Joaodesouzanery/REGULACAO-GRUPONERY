# Como continuar o trabalho em outro chat

## Para o usuário (conectar este repositório em outro chat do Claude)
1. Abra um chat/sessão do Claude Code conectado ao repositório `Joaodesouzanery/REGULACAO-GRUPONERY` (branch `claude/antt-directors-speeches-analysis-93r9hi` — o mais recente; `claude/director-profile-analysis-jnfixz` é a versão anterior).
2. O Claude lê `CLAUDE.md` automaticamente. Diga: «leia docs/CONTINUAR.md e continue de onde paramos» ou faça diretamente suas perguntas.
3. **O que viaja com o repositório:** transcrições, análises, banco, perfis, scripts, instruções, estado e pendências. **O que NÃO viaja:** a memória da conversa, as permissões do seu Mac, e a tarefa agendada semanal (pertence à sua conta: recriar com «crie uma tarefa semanal de monitoramento» + o texto em `docs/tarefa_semanal.txt`).
4. O download de transcrições novas continua sendo no Mac (veja `CLAUDE.md`).

## Estado (atualizado em 05/11/2026)
- Fonte da verdade do estado: `COBERTURA.md` (publicado × transcrito × analisado) e `sem_transcricao.md`.
- ANTT: **todas** as reuniões de diretoria com transcrição estão analisadas, de 2019 a out/2026: 281 reuniões, ≈ 2.350 itens, ≈ 9.250 votos de 20 diretores/substitutos. Única de diretoria sem análise: RD 1042 (28/09/2026), só música.
- Eventos (audiências, participativas, workshops, romeiros): **265 analisados** em `data/analise_eventos/<id>.evento.json` (2017–2026), com resumo, posições, encaminhamentos e falas de diretores (71 falas estruturadas, com minuto e trecho literal). Ficaram sem análise os ≈13 vídeos sem legenda utilizável (ver `sem_transcricao.md`). **Achado:** na grande maioria das audiências quem fala são ouvidores, superintendentes e gerentes; fala de diretor é rara (concentrada em 2024–2026). Ausência de fala de diretor ≠ ausência do diretor: a análise lê as janelas do resumo (abertura, menções, encerramento), não a sessão inteira. A data usada é a falada no encerramento quando difere do título. Falas de diretores pré-2019 (ex.: Jorge Bastos, DG em 2017) estão nos JSON mas não entram no banco (fora da lista de diretores).
- Qualidade: conferência cega em 3 rodadas + eventos (`agencias/antt/qualidade/README.md`): votos ≈ 93–94% (2019–2026), relator/resultado 93–100%, eventos 100% (trechos e falantes). `organizar.py` agora preserva `qualidade/`.
- Planilha: `agencias/antt/exportacoes/votos_diretores.xlsx` (resumo por diretor, diretor × tema, 9.251 votos com link no minuto, divergências/vistas, falas em eventos, mandatos, vacâncias).
- Mandatos/vacância: `data/mandatos.json`, `data/vacancias.json`, `agencias/antt/mandatos/` (9 vacâncias: média 211 d, mediana 191 d); nome completo, Senado e DOU confirmados por notícias/Senado para a maioria (pesquisa de 05/11/2026, com URLs em `fontes_pesquisa_2026_11`); posses NÃO confirmadas; Felipe Queiroz corrigido para fim legal 18/02/2027.
- Banco: `agencias/antt/exportacoes/regulacao.db.gz` (compactado, 27 MB); `data/regulacao.db` é regenerado por `05_indexar.py`.
- Levar para outra conta: `docs/LEVAR_PARA_OUTRA_CONTA.md` e `docs/HISTORICO_E_DECISOES.md`.
- Pendências: datas oficiais de posse/término (ver `data/mandatos.json`, campo `verificar`); nomes incertos de 2019–2021 («Menezes», grafias de Weber Ciloni, Eduardo Marra) a confirmar no DOU; itens sigilosos sem votos; Whisper para as 4 reuniões de diretoria sem texto: script pronto `pipeline/whisper_mac.sh` (rodar no Mac, com aprovação); outras agências: aguardando escolha do cliente (`docs/OUTRAS_AGENCIAS.md`); identificar «Menezes» e «Eduardo Marra»; datas de posse e de renúncia (Ciloni, Porto).
- Monitoramento: tarefa semanal na nuvem (texto em `docs/tarefa_semanal.txt`) + agendamento no Mac (`pipeline/instalar_agendamento_mac.sh`).

## Skills (.claude/skills/)
- `cuidados-pipeline` (checklist antes de commit + `pipeline/checar_integridade.py`) · `resposta-com-evidencia` (ficha fixa: `consulta.py ficha`) · `vacancia-agencia` (`vacancias.py` + `agencias/VACANCIA_AGENCIAS.md`) · `relatorio-cliente` (`pipeline/relatorio.py`, pasta `clientes/` fora do git; ver `docs/PRODUTO_CONSULTORIA.md`).
- Todo voto tem `trecho` literal (legenda a partir do minuto) e `trecho_tipo` (`fala_no_minuto` ou `janela_do_item`).

## Painel web e camada de empresas
- Painel (abre no chat, sem baixar): https://claude.ai/artifact/LN3GvfwZijv8PsarfmLiC3 — dados gerados por `python3 pipeline/painel_dados.py <pasta>`; subir cada JSON como asset do artifact e atualizar `datasets/<id>.source.url`.
- Empresas: `data/entidades.json` (ANTT) e `data/anm/entidades.json`; microtemas: `data/microtemas.json` e `data/anm/microtemas.json`.
- Comandos: `consulta.py empresa X | grupo X | microtema X [--diretor Y] | precedentes "texto" | relator X | reincidencia | sustentacoes | tramitacao`; monitor por cliente: `python3 pipeline/monitor.py --dias 7` (config `data/monitor.json`).

## Várias agências
- ANTT (piloto) usa a raiz: `data/`, `agencias/antt/`. Outras agências: `data/<sigla>/` (config em `data/<sigla>/config_agencia.json`: diretores, apelidos, temas, playlists, URL das atas) e `agencias/<sigla>/`.
- Qualquer script para outra agência: `bash pipeline/ag.sh anm python3 pipeline/<script>.py ...` (ex.: `05_indexar.py`, `consulta.py ficha "Mauro Sousa"`, `organizar.py`, `vacancias.py`).
- ANM: config, mandatos (12 nomes 2018–2026, com fontes) e vacâncias iniciais prontos; **falta a coleta no Mac** (abaixo). Atas oficiais da ANM: gov.br/anm/…/atas-da-rop (trazem link do vídeo) → usar como gabarito.

## No Mac (o que só ele faz)
1. Ficar no branch certo: `git fetch origin && git checkout claude/antt-directors-speeches-analysis-93r9hi && git pull`.
2. Whisper (aprovado para as 4 reuniões sem legenda): `brew install ffmpeg` (uma vez) e `caffeinate -i bash pipeline/whisper_mac.sh`.
3. DOU (posses) pelo terminal: cadastro gratuito no INLABS (https://inlabs.in.gov.br), depois
   `export INLABS_EMAIL='...' INLABS_SENHA='...'` e `python3 pipeline/baixar_dou_mac.py` (ANTT) / `python3 pipeline/baixar_dou_mac.py --agencia anm`; depois `git add data/fontes_dou && git commit -m DOU && git push`.
4. ANM, coleta completa: `caffeinate -i bash pipeline/coletar_tudo_e_enviar.sh anm PLoP8nQ7f1EABonZ_nYkKU9xsGx6L6PjY8` (varre o canal inteiro da ANM + a playlist e diz quantas reuniões estão fora dela); sem legenda: `caffeinate -i bash pipeline/whisper_mac.sh --agencia anm`.
5. Relatório de cliente (PDF, Grupo Nery): gerado no chat (`pipeline/relatorio.py`); imagens de setor em `docs/marca/setores/<setor>.jpg`.

## Comandos
```
python3 pipeline/validar.py                 # valida data/analise/*.analise.json
python3 pipeline/05_indexar.py              # reconstrói o banco (data/regulacao.db)
python3 pipeline/cobertura.py               # COBERTURA.md e sem_transcricao.md
python3 pipeline/organizar.py antt          # regenera agencias/antt/
python3 pipeline/consulta.py perfil "Alex Azevedo" [--tema onibus]
python3 pipeline/consulta.py trecho "pagamento avulso" [--tipo audiencia]
python3 pipeline/consulta.py falas Felipe | mandatos | temas | diretores | tema <tema> | busca <texto>
python3 pipeline/planilha_votos.py          # planilha xlsx de votos por diretor
python3 pipeline/amostra.py comparar 2025_2026  # conferência por amostra (rodadas: 2019_2024, 2019_2024_b, 2025_2026)
bash pipeline/whisper_mac.sh                # (no Mac) transcrição por áudio das reuniões sem legenda
python3 pipeline/03_preparar.py             # gera data/analise/<id>.md (leitura) das transcrições novas
```

## Como analisar reuniões pendentes (inclusive em paralelo)
1. `python3 pipeline/cobertura.py` → lista de reuniões de diretoria transcritas sem análise.
2. `python3 pipeline/03_preparar.py`. 3. Dividir em lotes de ~200 KB de `data/analise/<id>.md` e passar cada lote a um subagente com `pipeline/prompt_analise.txt` (esquema, regras, validação). 4. `python3 pipeline/validar.py`; `05_indexar.py`; regenerar perfis; commit/push.
Modelo de esquema: `data/analise/Zyxhofbj7g0.analise.json`.

## Outra agência
Criar `agencias/<sigla>/`, coletar com `python3 pipeline/01_coletar.py @canalXXX 0` no Mac (adaptar tipos/regex em `01_coletar.py`), transcrever (`02_transcrever.py`), analisar e indexar como acima; manter diretores/mandatos próprios em `mandatos.json`.

## Limites
Legenda automática (erros de nomes/números), falantes inferidos, minuto aproximado nos votos «acompanha», itens sigilosos fora da transmissão, vídeos sem legenda. Não faça afirmações sobre intenção/emoção; use dados.

## Estado em 10/11/2026 (ANTAQ e relatório v4)
- **ANTAQ:** 93 reuniões de diretoria 2019–2026 analisadas (3.291 itens, 11.375 votos), base `data/antaq/regulacao.db` (`bash pipeline/ag.sh antaq python3 pipeline/05_indexar.py`). Conferência cega: voto 92,3%, relator/resultado 100% (`agencias/antaq/qualidade/`). Vacâncias em `data/antaq/vacancias.json` (vaga de Flávia Takafashi aberta desde 19/02/2026).
- **Pendências ANTAQ:** 2016–2018 (55 reuniões com legenda) e eventos (120 audiências, 7 participativas, 10 workshops) — subagente `analista-evento`; datas de várias sessões vêm do upload (conferir nas atas do gov.br); Parte 1 da 465ª e 466ª voltou à fila da coleta no Mac; entidades/microtemas da ANTAQ.
- **Whisper:** nenhuma transcrição Whisper chegou ao GitHub até 10/11 (ANTT 4 reuniões; ANM sem legenda). Ver `docs/MAC_COMANDOS.md`.
- **Relatório:** `pipeline/relatorio_v2.py` (v4): capa, sumário em cartões de foto, 1 página por pergunta, «como ler»; ~13 páginas, < 1 MB. Fotos por setor em `docs/marca/setores/` (Openverse/Wikimedia, créditos) → `preparar_fotos.py`.
