---
name: contratos
description: Gera a minuta de contrato (parceiro revendedor, termos do cliente final e DPA LGPD) a partir de clientes/<x>/contrato.json e dos modelos em proposta2/contrato/; confere com o agente revisor-contratual. Use quando pedir «contrato do parceiro X», «minuta para o cliente Y» ou ao fechar venda.
---
**Sempre modelo para revisão por advogado; não é aconselhamento jurídico.** A minuta fica em `clientes/<x>/contrato/` (fora do git), nunca em `proposta2/`.

1. Ler `proposta2/contrato/` (clausulas_parceiro.md, clausulas_cliente_final.md, dpa_lgpd.md, checklist_contrato.md) e `proposta2/modelo_comercial.md` (preços).
2. Ler ou criar `clientes/<x>/contrato.json`. Campos:
```json
{"tipo": "parceiro|cliente_final",
 "licenciante": {"razao_social": "", "cnpj": ""},
 "parceiro": {"razao_social": "", "cnpj": "", "representante": ""},
 "cliente": {"razao_social": "", "cnpj": ""},
 "plano": "Essencial|Profissional|Completo|Avulso", "fundador": {"ativo": true, "qtd": 2},
 "preco_mensal": 0, "perguntas_mes": 5, "prazo_resposta_dias_uteis": 5,
 "faturamento": {"quem": "parceiro"}, "repasse_dias": 10,
 "exclusividade": {"ativa": false, "escopo": "", "meta_clientes": 0, "meta_receita": 0, "prazo_meses": 0},
 "nao_concorrencia_meses": 12, "registro_dias": 90,
 "aviso_dias": 60, "multa_meses": 3, "foro": "",
 "encarregado": {"nome": "", "email": ""},
 "autorizacao_divulgacao": {"tem": false, "arquivo": "", "escopo": ""}}
```
3. Preço: conferir se o valor ≥ tabela (fundador só se `fundador.ativo` e houver vaga entre os 2 primeiros). Abaixo da tabela → parar e perguntar.
4. Substituir `{{campo}}` / `{{campo|padrão}}`; cláusulas opcionais (exclusividade) somem se inativas. Nenhum `{{` pode sobrar (`grep -n "{{" clientes/<x>/contrato/*.md`).
5. Rodar o agente **revisor-contratual** (seção A do checklist). Só entregar com 0 FALHA.
6. Registrar em `clientes/<x>/historico.md`: versão, data, quem revisou (advogado: pendente/ok).
