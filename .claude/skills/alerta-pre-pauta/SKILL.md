---
name: alerta-pre-pauta
description: Gera o alerta pré-pauta (produto D) — itens de interesse do cliente na pauta publicada, relator, como cada diretor votou em casos parecidos e previsão rotulada como inferência — com pipeline/alerta_pauta.py. Use quando sair pauta nova ou pedir «alerta da próxima reunião».
---
1. `python3 pipeline/pautas.py <ag>` (skill agenda-pauta) para ter a pauta atual.
2. `python3 pipeline/alerta_pauta.py clientes/<x>/<pasta> [--agencia <ag>]` (campo opcional `itens_acompanhar` no empresa.json: nº de itens que o cliente pediu para seguir) — cruza a pauta com `empresa.json` (aliases, CNPJ, temas_consultoria, contrato_foco).
3. Para cada item encontrado: relator, casos semelhantes (skill casos-semelhantes), mapa do assunto (mapa-assunto) e, se pedido, previsão (previsao-voto).
4. SLA: até **24 h antes** da reunião quando a pauta foi publicada a tempo; publicada com menos de 48 h → melhor esforço, avisar.
5. Antes de enviar: skill **conformidade-entrega**. Sem item do cliente na pauta → alerta curto «nenhum item identificado», com a lista de termos buscados.
