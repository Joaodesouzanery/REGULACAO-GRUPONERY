# Instruções para o Claude neste repositório (ler primeiro)

**Projeto:** perfis analíticos de diretores de agências reguladoras a partir de reuniões públicas no YouTube (piloto: ANTT, canal @canalANTT). Objetivo final: o usuário pergunta no chat (ex.: «em assuntos de empresas de ônibus, o diretor X costuma se envolver? como e por quê?») e você responde com **evidência**: reunião, item, voto, trecho literal e **link do vídeo no minuto exato**.

**Comece por:** `docs/CONTINUAR.md` (estado, comandos, pendências) e `COBERTURA.md`. Perguntas-modelo e formato de resposta: `docs/perguntas_modelo.md`.

## Regras de resposta (obrigatórias)
1. Antes de responder, rode `python3 pipeline/05_indexar.py` (reconstrói `data/regulacao.db`, ~10 s) e consulte com `pipeline/consulta.py` (`perfil`, `tema`, `busca`, `trecho`, `falas`, `mandatos`, `temas`, `diretores`).
2. Cite sempre: reunião (nº/data), item, voto, justificativa, **trecho literal** e **link com &t=segundos**. Diga o **n** (amostra) e a **confiança**.
3. Nada de rótulos sem base («raivoso», «problemático»): use contagens (acompanha, diverge, vista, vencido), argumentos recorrentes e tom registrado como inferência.
4. A legenda do YouTube é automática: nomes, números e valores podem estar errados; minuto de quem só «acompanha o relator» é aproximado. Avise isso quando relevante.
5. Diga o que **não** temos: `sem_transcricao.md`, itens sigilosos, anos ainda não analisados (ver `COBERTURA.md`).
6. Qualidade: conferência por amostra cega (108 itens, 2019–2024; `agencias/antt/qualidade/conferencia_amostra.md`): concordância de ≈ 93% em relator, resultado e voto por diretor (89–99% por ano). Cite essa taxa ao responder sobre anos antigos, lembrando que mede consistência, não verdade absoluta.
7. Mandatos/vacâncias: `data/mandatos.json`, `data/vacancias.json` (estimativas, com fonte e confiança).

## Mapa
- `data/` = fonte de trabalho dos scripts (transcricoes/, analise/*.analise.json, videos.jsonl, mandatos.json, regulacao.db).
- `agencias/<agencia>/` = árvore organizada gerada (`python3 pipeline/organizar.py antt`): reuniões por ano/tipo, diretores, temas, exportações CSV.
- `pipeline/` = 01 coleta, 02 transcrição, 03 preparar leitura, 05 indexar, `validar.py`, `consulta.py`, `cobertura.py`, `organizar.py`, `prompt_analise.txt` (instruções para analisar reuniões, inclusive por subagentes).

## O que só o Mac do usuário faz
O YouTube bloqueia IPs de nuvem: **baixar transcrições** só funciona no Mac (`bash pipeline/coletar_tudo_e_enviar.sh`; agendamento: `bash pipeline/instalar_agendamento_mac.sh`). O chat analisa, indexa, organiza e dá push.

## Commits
Sempre commit e push no branch de trabalho; não abra PR sem pedido. Não versione o banco a cada lote (engorda o `.git`): só em marcos.
