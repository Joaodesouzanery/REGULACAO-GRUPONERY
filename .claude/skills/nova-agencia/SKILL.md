---
name: nova-agencia
description: Checklist para iniciar (ou retomar) uma nova agência reguladora no projeto — raiz virtual, config, inventário do canal, coleta no Mac, análise por subagentes, conferência, atas, mandatos, vacância, painel e relatório. Use quando o usuário disser «começar a ANTAQ/ANEEL/…», «fazer o mesmo trabalho com a agência X».
---
# Nova agência (modelo: ANM; ANTAQ em andamento)

Tudo roda com `bash pipeline/ag.sh <sigla> <comando>` (cria `data/<sigla>/.raiz` com links para pipeline/, docs/, agencias/).

1. **Config**: `data/<sigla>/config_agencia.json` — diretores (nome canônico + regex de apelidos da legenda), temas e regex, `rx_nomes`, playlists, `atas_url`. Copie de `data/anm/config_agencia.json` e adapte.
2. **Mandatos**: subagente `pesquisador-mandatos` → `data/<sigla>/mandatos.json` (com fontes). Depois skill `vacancia-agencia`.
3. **Inventário** (daqui funciona): `bash pipeline/ag.sh <sigla> python3 pipeline/01_coletar.py @Canal 0` → `data/<sigla>/videos.jsonl`; conte por tipo (diretoria/audiencia/participativa/workshop/outro).
4. **Legendas** (SÓ no Mac — YouTube bloqueia nuvem): `caffeinate -i bash pipeline/coletar_tudo_e_enviar.sh <sigla> @Canal`. Sem legenda → `whisper_mac.sh --agencia <sigla>` (não precisa de ffmpeg).
5. **Análise**: `bash pipeline/ag.sh <sigla> python3 pipeline/03_preparar.py`; crie `data/<sigla>/prompt_analise.txt` (copiar o da ANM, trocar diretores, temas e vocabulário do setor); um subagente `analista-reuniao` por reunião (em paralelo, lotes de ~8); validar → `05_indexar.py`.
6. **Eventos**: `07_preparar_eventos.py` + `prompt_evento.txt`.
7. **Qualidade**: `amostra.py sortear <rodada>` → subagentes `conferente-cego` → `amostra.py comparar <rodada>`; atas oficiais (`cruzar_atas.py`) quando houver.
8. **Enriquecer**: `data/<sigla>/entidades.json`, `microtemas.json`; `planilha_votos.py`; `painel_dados.py`; `organizar.py <sigla>`.
9. **Entrega**: 10 perguntas → skill `relatorio-cliente` + `relatorio-visual`; antes, subagente `auditor-respostas`.
10. Atualize `COBERTURA.md`, `docs/CONTINUAR.md`, `docs/MAC_COMANDOS.md`; skill `cuidados-pipeline` antes de cada commit.
