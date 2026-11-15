---
name: consulta-mensal-cliente
description: Roteiro da conversa mensal (30 min) com o cliente que gera as perguntas do boletim do mês e atualiza clientes/<x>/<pasta>/processos.json. Use antes de cada ciclo mensal ou quando pedir «preparar a conversa com o cliente X».
---
**Antes (15 min):** rode `raio_x.py` e `agenda_comparativa.py` da pasta anterior; liste 3 novidades públicas do mês (pautas, mudança de diretoria, decisão no tema) para abrir a conversa.

**Roteiro (30 min):**
1. Novidades que trouxemos (5 min) — ouvir reação, anotar o que interessou.
2. Processos (10 min) — para cada item do `processos.json`: mudou fase? relator? prazo interno? Há processo novo, encerrado ou sigiloso?
3. Prioridades do mês (10 min) — 3 a 5 perguntas para o boletim, no formato «o diretor X / a diretoria costuma … em …?»; confirmar agência, tema e período.
4. Entregas e formato (5 min) — o que foi útil, o que sobrou, quem recebe.

**Depois (mesmo dia):**
- Atualizar `clientes/<x>/<AAAA-MM>/processos.json` (copiar o anterior e editar) e `perguntas.md`.
- Nada disso vai ao git; nada de dado do cliente em demo ou material de marketing.
- Abrir o ciclo com `montar-relatorio` / `boletim-mensal`.
Pronto quando: `processos.json` e `perguntas.md` do mês existem e o cliente confirmou as perguntas por escrito.
