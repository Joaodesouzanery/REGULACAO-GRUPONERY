---
name: previsibilidade-regulatoria
description: Radar de Previsibilidade Regulatória — indicador de retirada de pauta (pipeline/retiradas.py), sucessão de diretoria, prazo esperado × real e consultas abertas, por empresa. Use em alertas para cliente/parceiro (Circle), demos de concessionárias e quando perguntarem «por que tiraram de pauta?».
---
# Radar de Previsibilidade Regulatória
1. Retiradas: `python3 pipeline/retiradas.py <ag> processo <nº>` (do cliente) e `... diretores` (taxa do relator × média da agência, mediana de dias até voltar, retiradas sem motivo declarado).
2. Sucessão: mandato do relator e vagas (`data/<ag>/mandatos.json`, `vacancias.py`, `cadeiras.json`).
3. Prazo: `prazos.py` (processo do cliente × semelhantes); atraso acima do percentil 75 = alerta.
4. Consultas/agenda: calendário e pautas (`pautas.py`).

## Linguagem obrigatória
- Permitido: «retirado de pauta pelo relator», «motivo dito na sessão: …», «sem motivo declarado na sessão», «taxa 1,5× a média da agência», «voltou após N dias», sempre com link no minuto.
- Proibido em qualquer documento, e-mail ou conversa: hipótese de motivo, «propina», «corrupção», «vantagem», «favorecimento», «suspeito», adjetivo sobre o diretor.
- Suspeita de irregularidade: orientar canal oficial (CGU, Comissão de Ética Pública, ouvidoria da agência, MP). Nunca explorar comercialmente (Lei 12.846/2013 responsabiliza a empresa objetivamente).
