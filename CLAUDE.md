# Instruções para o Claude neste repositório (ler primeiro)

**Projeto:** perfis analíticos de diretores de agências reguladoras a partir de reuniões públicas no YouTube (piloto: ANTT, canal @canalANTT). Objetivo final: o usuário pergunta no chat (ex.: «em assuntos de empresas de ônibus, o diretor X costuma se envolver? como e por quê?») e você responde com **evidência**: reunião, item, voto, trecho literal e **link do vídeo no minuto exato**.

**Comece por:** `docs/CONTINUAR.md` (estado, comandos, pendências) e `COBERTURA.md`. Perguntas-modelo e formato de resposta: `docs/perguntas_modelo.md`.

## Regras de resposta (obrigatórias)
1. Antes de responder, rode `python3 pipeline/05_indexar.py` (reconstrói `data/regulacao.db`, ~10 s) e consulte com `pipeline/consulta.py` (`perfil`, `tema`, `busca`, `trecho`, `falas`, `mandatos`, `temas`, `diretores`).
2. Cite sempre: reunião (nº/data), item, voto, justificativa, **trecho literal** e **link com &t=segundos**. Diga o **n** (amostra) e a **confiança**.
3. Nada de rótulos sem base («raivoso», «problemático»): use contagens (acompanha, diverge, vista, vencido), argumentos recorrentes e tom registrado como inferência.
4. A legenda do YouTube é automática: nomes, números e valores podem estar errados; minuto de quem só «acompanha o relator» é aproximado. Avise isso quando relevante.
5. Diga o que **não** temos: `sem_transcricao.md`, itens sigilosos, anos ainda não analisados (ver `COBERTURA.md`).
6. Qualidade: conferência por amostra cega (`agencias/antt/qualidade/README.md`): votos por diretor ≈ 94–95% de concordância em 2019–2026 (2019 é o ano mais fraco: 75–92%); relator e resultado entre 93% e 100%; eventos: 100% dos trechos literais encontrados (95% a até 2 min do minuto citado). Cite essa taxa e lembre que mede consistência, não verdade absoluta.
7. Mandatos/vacâncias: `data/mandatos.json` (nome completo, Senado, DOU, fim legal, fontes), `data/vacancias.json`, `agencias/antt/mandatos/README.md`. Posse ainda não confirmada no DOU: diga isso.
9. Planilha: `agencias/antt/exportacoes/votos_diretores.xlsx` (gerada por `pipeline/planilha_votos.py`; `organizar.py` regenera).

8. Eventos (audiências/participativas/workshops): `data/analise_eventos/*.evento.json`; `consulta.py falas <diretor>` e `consulta.py trecho`. Diga que a maioria das audiências não tem fala de diretor e que a análise cobre janelas do resumo, não a sessão inteira.

## Mapa
- `data/` = fonte de trabalho dos scripts (transcricoes/, analise/*.analise.json, videos.jsonl, mandatos.json, regulacao.db).
- `agencias/<agencia>/` = árvore organizada gerada (`python3 pipeline/organizar.py antt`): reuniões por ano/tipo, diretores, temas, exportações CSV.
- `pipeline/` = 01 coleta, 02 transcrição, 03 preparar leitura, 05 indexar, `validar.py`, `consulta.py`, `cobertura.py`, `organizar.py`, `prompt_analise.txt` (instruções para analisar reuniões, inclusive por subagentes).

## O que só o Mac do usuário faz
O YouTube bloqueia IPs de nuvem: **baixar transcrições** só funciona no Mac (`bash pipeline/coletar_tudo_e_enviar.sh`; agendamento: `bash pipeline/instalar_agendamento_mac.sh`). O chat analisa, indexa, organiza e dá push.

## Commits
Sempre commit e push no branch de trabalho; não abra PR sem pedido. Não versione o banco a cada lote (engorda o `.git`): só em marcos.

## Skills (usar sempre)
`.claude/skills/`: **resposta-com-evidencia** (toda pergunta sobre diretor → `consulta.py ficha`, formato fixo com trecho literal e link no minuto), **cuidados-pipeline** (antes de todo commit: `python3 pipeline/checar_integridade.py`), **vacancia-agencia** (`vacancias.py`), **relatorio-cliente** (`pipeline/relatorio.py`; `clientes/` nunca vai ao GitHub). Também: **nova-agencia** (checklist ANTAQ e próximas), **lote-mac** (quando o Mac envia legendas/Whisper), **relatorio-visual** (`pipeline/relatorio_v2.py`, 1 página por pergunta, fotos fixas por setor). Produto: `docs/PRODUTO_CONSULTORIA.md`.

## Subagentes (`.claude/agents/`) e hooks
`analista-reuniao` (1 reunião → .analise.json validado), `conferente-cego` (amostra cega, sem ver a base), `auditor-respostas` (confere cada afirmação de relatório com SQL próprio), `pesquisador-mandatos` (Senado/DOU com fontes). Hooks em `.claude/settings.json`: `git commit` só passa se `checar_integridade.py` passar; início de sessão lembra este roteiro.
