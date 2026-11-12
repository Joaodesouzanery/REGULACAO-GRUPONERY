---
name: nova-agencia-rapida
description: Começa uma agência nova em uma sessão (ANEEL, ANAC, ANP, ANATEL, ARTESP…): estrutura, config, prompts, inventário do canal, mandatos/minibios/superintendentes e comando do Mac. Use quando o usuário disser «vamos começar a agência X».
---
1. `python3 pipeline/iniciar_agencia.py <sigla> @Canal "Nome"` (teste antes com `--simular`).
2. Inventário daqui: `bash pipeline/ag.sh <sigla> python3 pipeline/01_coletar.py @Canal 0` → conte por tipo; confira playlists de reuniões de diretoria.
3. Em paralelo (background): `pesquisador-mandatos` (diretores 2015–hoje → mandatos.json, vacancias.json), minibios (bios.json), `pesquisador-dirigentes` (superintendentes.json + fotos oficiais).
4. Preencha `config_agencia.json` (diretores, alias regex, rx_nomes, temas do setor) e a lista de diretores no prompt_analise.txt.
5. Diga ao usuário o comando do Mac: `caffeinate -i bash pipeline/coletar_tudo_e_enviar.sh <sigla> @Canal`.
6. Quando chegar: skill `lote-mac` (03_preparar → analista-reuniao em lotes de ~8 → validar → indexar → amostra cega → eventos → organizar/planilha → vacancias → relatorio_diretoria).
7. Acrescente a sigla em `previsao.DB`, `relatorio_empresa.py` (NOME_AG/SETOR_AG/TEMA_AG), `relatorio_diretoria.py` e `cobertura_resposta.py` (QUAL), e um setor/foto se for novo (agente `curador-fotos`).
