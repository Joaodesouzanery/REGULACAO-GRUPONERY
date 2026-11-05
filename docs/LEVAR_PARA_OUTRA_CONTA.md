# Levar o projeto para um chat do Claude em OUTRA conta

Tudo que importa está neste repositório (dados, scripts, instruções, estado). O que a outra conta precisa é de **acesso ao repositório**.

## Passo 1 — dar acesso (escolha uma opção)
| Opção | Como | Quando usar |
|---|---|---|
| A (recomendada) | GitHub > repositório `Joaodesouzanery/REGULACAO-GRUPONERY` > Settings > Collaborators > Add people > usuário GitHub da outra conta (permissão Write). A pessoa aceita o convite por e-mail. | A outra conta continua o mesmo trabalho e pode dar push. |
| B | A outra conta faz **Fork** (repositório privado só permite fork se a opção estiver habilitada nas configurações) e conecta o fork. | Cópia independente. |
| C | Settings > Transfer ownership para a outra conta. | Mudança definitiva de dono. |

## Passo 2 — conectar no Claude da outra conta
1. Em claude.ai/code (ou Claude Code no terminal), conecte o GitHub da outra conta e instale o app do Claude no repositório (https://github.com/apps/claude/installations/select_target).
2. Crie uma sessão escolhendo o repositório e o branch `claude/director-profile-analysis-jnfixz` (ou o branch principal, depois de mesclar: pedir ao Claude «faça merge do branch na principal», sem abrir PR se não quiser).
3. O Claude lê `CLAUDE.md` sozinho. **Primeiro prompt para colar:**
> Leia CLAUDE.md, docs/CONTINUAR.md, docs/HISTORICO_E_DECISOES.md e COBERTURA.md. Rode `python3 pipeline/05_indexar.py` e me diga o estado atual (reuniões, eventos, pendências). Depois continue as pendências listadas em «Pendências» de docs/CONTINUAR.md.

## O que viaja × o que não viaja
- **Viaja (está no git):** transcrições (`data/transcricoes/`), análises (`data/analise/`, `data/analise_eventos/`), inventário, mandatos e vacâncias, banco (`data/regulacao.db`, regenerável por `05_indexar.py`), árvore organizada `agencias/antt/`, perfis, relatório de qualidade, prompts dos subagentes (`pipeline/prompt_*.txt`), scripts, documentação.
- **Não viaja:** a memória/histórico da conversa (por isso `docs/HISTORICO_E_DECISOES.md`), o plano local, permissões do Mac, a tarefa semanal na nuvem (é da conta; recriar com o texto de `docs/tarefa_semanal.txt`), o agendamento do Mac (`bash pipeline/instalar_agendamento_mac.sh`).

## Configuração / variáveis
- Nenhuma chave de API nem variável secreta. A análise é feita pelo próprio Claude e subagentes lendo os textos.
- Python 3 padrão para indexar/consultar; `uv run --python 3.12` só para coleta (`yt-dlp`, `youtube-transcript-api`) **no Mac do usuário** (o YouTube bloqueia IPs de nuvem).
- Comando único no Mac: `bash pipeline/coletar_tudo_e_enviar.sh` (baixa transcrições novas e faz push).
- Fluxo de nuvem: `git pull` → `pipeline/cobertura.py` (o que falta) → analisar com subagentes (`pipeline/prompt_analise.txt` para reuniões de diretoria; `pipeline/07_preparar_eventos.py` + `pipeline/prompt_evento.txt` para eventos) → `validar.py`/`validar_evento.py` → `05_indexar.py` → `organizar.py antt` → commit e push.

## Objetivo final (resumo)
Perguntar no chat, por exemplo «em assuntos de empresas de ônibus, o diretor X costuma se envolver? como e por quê?» e receber resposta com evidência: reunião, item, voto, trecho literal e link do YouTube no minuto (`&t=segundos`), sempre com n e confiança, sem rótulos subjetivos. Depois, repetir para outras agências reguladoras (ANAC, ANTAQ etc.).

## Cuidados
- O `.git` é grande (≈ 1 GB, por versões do banco). Não versione o banco a cada lote; não reescreva histórico sem pedido do dono.
- Não abrir PR sem pedido.
