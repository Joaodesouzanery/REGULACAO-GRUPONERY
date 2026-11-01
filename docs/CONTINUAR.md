# Como continuar o trabalho em outro chat

## Para o usuário (conectar este repositório em outro chat do Claude)
1. Abra um chat/sessão do Claude Code conectado ao repositório `Joaodesouzanery/REGULACAO-GRUPONERY` (branch `claude/director-profile-analysis-jnfixz`, ou o branch principal depois de mesclar).
2. O Claude lê `CLAUDE.md` automaticamente. Diga: «leia docs/CONTINUAR.md e continue de onde paramos» ou faça diretamente suas perguntas.
3. **O que viaja com o repositório:** transcrições, análises, banco, perfis, scripts, instruções, estado e pendências. **O que NÃO viaja:** a memória da conversa, as permissões do seu Mac, e a tarefa agendada semanal (pertence à sua conta: recriar com «crie uma tarefa semanal de monitoramento» + o texto em `docs/tarefa_semanal.txt`).
4. O download de transcrições novas continua sendo no Mac (veja `CLAUDE.md`).

## Estado (atualize ao fim de cada sessão)
- Atualizado em 01/11/2026. Fonte da verdade do estado: `COBERTURA.md` (publicado × transcrito × analisado) e `sem_transcricao.md`.
- ANTT: reuniões de diretoria analisadas de jan/2023 a out/2026 (120 reuniões, ≈ 3.800 votos). Em andamento: 2022, depois 2021, 2020, 2019 (limite: 2019). Audiências, participativas e workshops: indexados como fala literal e menções a diretores; sem análise item a item.
- Pendências conhecidas: datas oficiais de posse/término (ver `data/mandatos.json`, `verificar`); itens sigilosos sem votos; RD 1042 (28/09/2026) só tem música.

## Comandos
```
python3 pipeline/validar.py                 # valida data/analise/*.analise.json
python3 pipeline/05_indexar.py              # reconstrói o banco (data/regulacao.db)
python3 pipeline/cobertura.py               # COBERTURA.md e sem_transcricao.md
python3 pipeline/organizar.py antt          # regenera agencias/antt/
python3 pipeline/consulta.py perfil "Alex Azevedo" [--tema onibus]
python3 pipeline/consulta.py trecho "pagamento avulso" [--tipo audiencia]
python3 pipeline/consulta.py falas Felipe | mandatos | temas | diretores | tema <tema> | busca <texto>
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
