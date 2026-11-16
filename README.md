# Regulação: inteligência sobre diretorias de agências reguladoras

Base de reuniões públicas de diretoria (vídeo, legenda, análise item a item e voto a voto) das agências **ANTT, ANM, ANTAQ e ANEEL** (ANP a seguir), com perfis de diretores, mandatos, prazos, casos semelhantes e relatórios em PDF para clientes. Cada afirmação traz reunião, item, trecho literal e **link do vídeo no minuto exato**.

## Comece por aqui
| Para | Abra |
|---|---|
| Estado atual, comandos e pendências | `docs/CONTINUAR.md` |
| O que está completo por agência | `COMPLETUDE.md` · `COBERTURA.md` |
| Lista de todos os scripts, skills e agentes | `docs/MAPA.md` |
| Comandos do Mac (coleta) | `docs/MAC_COMANDOS.md` |
| Produto e comercial | `docs/PRODUTO_CONSULTORIA.md` · `proposta2/` |
| Mandatos e vacância (12 agências) | `docs/vacancia_12_agencias.md` · `data/mandatos_agencias.json` |
| Transparência das agências | `docs/transparencia_agencias.md` |

## Pastas
| Pasta | Conteúdo |
|---|---|
| `data/` (ANTT) e `data/<ag>/` | transcrições, análises (`analise/*.analise.json`), eventos, mandatos, cadeiras, calendário, dirigentes; bancos `regulacao.db` (reconstruídos com `05_indexar.py`; o da ANEEL fica fora do git) |
| `agencias/<ag>/` | árvore organizada gerada (`organizar.py`): reuniões por ano, diretores, temas, exportações, qualidade |
| `pipeline/` | coleta (Mac), análise, indexação, consultas, relatórios em PDF (`design.py` é o padrão visual) |
| `docs/` | roteiros, metodologia, marca (fotos e logos), leis |
| `proposta2/` | propostas, contratos-modelo, marketing e comercial |
| `.claude/` | skills, agentes, comandos e hooks do Claude |
| `clientes/` | **nunca vai ao GitHub** (dados de clientes) |

## Como perguntar (no chat com o Claude, nesta pasta)
Exemplos: «Alex Azevedo e empresas de ônibus: como e por quê?», «quem divergiu em 2026 e por quê?», «Felipe Queiroz e free flow», «o que se disse nas audiências sobre pagamento avulso?».
O Claude roda `python3 pipeline/05_indexar.py` (reconstrói `data/regulacao.db`, ~10 s) e consulta:
- `python3 pipeline/consulta.py perfil "<Diretor>" [--tema <tema>]` – votos, relatorias, % de acompanhamento, argumentos recorrentes, evidências.
- `python3 pipeline/consulta.py tema <tema>` / `busca <texto>` – itens por tema/assunto.
- `python3 pipeline/consulta.py trecho <texto> [--tipo audiencia|participativa|diretoria|workshop]` – **fala literal** + link `youtube.com/watch?v=ID&t=SEGs`.
- `python3 pipeline/consulta.py mandatos | diretores | temas`.
Regra de resposta: sempre citar **reunião, item, voto, trecho literal e link no minuto**, com **n** (amostra) e **confiança**; nada de rótulos sem base («raivoso» → contagens, argumentos recorrentes e tom inferido).

## Conteúdo
`data/transcricoes/*.json` (legenda automática com tempos) · `data/analise/*.analise.json` (análise por item, voto e justificativa) · `data/perfis/*.md` · `data/mandatos.json` · `COBERTURA.md` (publicado × transcrito × analisado) · `docs/metodologia.md`.
Limites: legenda automática erra nomes e números; falantes são inferidos pelo contexto; votos de seguidores têm minuto aproximado (campo `confianca`). Reuniões com pedido de vista, retiradas de pauta e itens sigilosos estão marcados.

## Monitoramento de reuniões novas
1. **Mac (semanal)**: `bash pipeline/instalar_agendamento_mac.sh` (launchd, segunda 09:00) → roda `monitorar.sh`: `01_coletar` (descobre vídeos novos) + `02_transcrever` + push. Só o Mac baixa transcrições (o YouTube bloqueia IPs de nuvem).
2. **Nuvem (semanal)**: tarefa agendada do Claude faz `git pull`, lista reuniões de diretoria transcritas e sem análise (`COBERTURA.md`), analisa as novas, atualiza banco/perfis e avisa.
3. **Painel**: `python3 pipeline/cobertura.py` gera `COBERTURA.md`; vídeos sem legenda ficam em `data/sem_legenda.jsonl` com o motivo.

## Reconstruir do zero
`python3 pipeline/03_preparar.py` (gera os .md lidos pelo analista) → análise (`*.analise.json`, validar com `pipeline/validar.py`) → `python3 pipeline/05_indexar.py`.

## Estrutura organizada (para qualquer pessoa/ferramenta que conectar o repositório)
`agencias/antt/` — veja `agencias/antt/README.md`: reuniões por ano/tipo, diretores (perfil, votos, mandato), temas e exportações (CSV, trechos, banco). `data/` é a fonte de trabalho dos scripts; depois de cada atualização rode `python3 pipeline/05_indexar.py && python3 pipeline/organizar.py antt`.

## Mapa do repositório (nov/2026)
| Onde | O quê |
|---|---|
| `data/` | ANTT (piloto): transcrições, análises de reuniões e eventos, mandatos, vacâncias, `entidades.json` (empresas), `microtemas.json`, `monitor.json` |
| `data/anm/` | ANM, mesma estrutura + `atas/indice_atas.json` (121 atas oficiais); rodar scripts via `bash pipeline/ag.sh anm …` |
| `agencias/antt/`, `agencias/anm/` | Árvore organizada: reuniões por ano, diretores, temas, `mandatos/`, `qualidade/` (conferências e cruzamento com atas), `exportacoes/` (planilha `votos_diretores.xlsx`, CSVs, banco compactado), `apresentacao/relatorio.pdf` |
| `agencias/VACANCIA_AGENCIAS.md` | Comparativo de vacância entre agências |
| `pipeline/` | Coleta (Mac), análise, indexação, `consulta.py` (perfil, ficha, empresa, grupo, microtema, precedentes, relator, reincidência, sustentações, tramitação), `relatorio.py` (PDF de cliente), `relatorio_agencia.py` (apresentação), `monitor.py`, `painel_dados.py`, `checar_integridade.py` |
| `proposta2/` | Proposta do 2º produto (Radar Regulatório): catálogo, modelo comercial, operação, roadmap — só documento |
| `.claude/skills/` | Regras de resposta com evidência, cuidados antes de commit, vacância, relatório de cliente, nova agência, lote do Mac, relatório visual, auditoria |
| `.claude/agents/` | Subagentes: analista de reunião, analista de evento, conferente cego, auditor de respostas, revisor visual, pesquisador de mandatos |
| `.claude/commands/` | Atalhos: `/pergunta`, `/relatorio`, `/lote-mac` |
| `docs/` | `CONTINUAR.md` (estado e comandos), produto/consultoria, DOU, outras agências, marca e fotos de setor |
| Painel web | https://claude.ai/artifact/LN3GvfwZijv8PsarfmLiC3 |
