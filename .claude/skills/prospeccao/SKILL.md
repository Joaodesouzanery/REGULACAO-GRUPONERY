---
name: prospeccao
description: Monta e atualiza a lista de possíveis clientes do Grupo Nery (empresas reguladas, escritórios, associações, investidores) em proposta2/comercial/prospects.csv/.xlsx, com motivo de interesse tirado da base e contato institucional público. Use quando pedirem lista de clientes, prospecção ou leads.
---
# Prospecção
1. Motivo de interesse: contagem de decisões da diretoria em que a empresa aparece (`itens.interessado`/assunto via `previsao.conn(ag)`); confira nomes ambíguos com `consulta.py busca`.
2. Contatos: só institucionais públicos (site, fale-conosco, RI, imprensa, página da empresa no LinkedIn). Nunca dado de pessoa física. A nuvem bloqueia sites de empresas: rodar o preenchimento no Mac (`python3 pipeline/contatos_prospects.py` — a criar) ou à mão.
3. Prioridade: A ≥ 10 decisões ou grande grupo; B 3–9; C < 3. Estatais e câmaras (CCEE) ficam C.
4. Gere o xlsx minimalista (cabeçalho azul #003B4C, filtros, congelar painel) e rode `guardiao-dados-cliente`.
