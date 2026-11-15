---
name: raio-x-processos
description: Gera o documento 3 (raio-X dos processos do cliente — blocos 1, 2, 3 e 8) com pipeline/raio_x.py a partir de clientes/<x>/<pasta>/processos.json e prazos.py. Use quando pedir «raio-X dos processos», «onde estão meus processos» ou na rodada mensal do cliente.
---
- Entrada: `clientes/<x>/<pasta>/processos.json`, **informado pelo cliente** (nº do processo, assunto, fase, relator se souber, datas). Nunca buscar no SEI contornando bloqueio; nunca versionar (`clientes/` fora do git).
- `python3 pipeline/raio_x.py clientes/<x>/<pasta>`
- Blocos: **1** situação de cada processo (fase, relator, última movimentação pública); **2** alertas (prazo vencendo, entrada em pauta via `pautas.py`); **3** prazos — `python3 pipeline/prazos.py` dá mediana e faixa do tipo e compara com ≥ 20 semelhantes (agente `analista-prazos`); **8** resumo executivo do cliente.
- Regras: prazo previsto = **estimativa** com n e faixa; se n < 20, dizer «amostra pequena». Datas do cliente prevalecem sobre a legenda.
- Pronto quando: todo processo do JSON aparece; cada estimativa tem n; `auditor-respostas` passou; bloco de cobertura no fim; `conformidade-entrega` ok.
