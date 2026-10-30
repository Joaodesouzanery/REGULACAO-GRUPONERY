# Regulação — perfis de diretores de agências (piloto: ANTT)

Repositório de **transcrições de reuniões públicas** (YouTube @canalANTT) + **análise por item/voto** + **busca com link no minuto exato do vídeo**.

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
