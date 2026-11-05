# Outras agências — aguardando decisão do usuário/cliente

Nada foi coletado ainda. Quando a agência for escolhida, o processo é o mesmo da ANTT (ver `docs/CONTINUAR.md`, seção «Outra agência»):
1. No Mac: `python3 pipeline/01_coletar.py @<canal> 0` (inventário) e `bash pipeline/coletar_tudo_e_enviar.sh` adaptado ao canal; ajustar em `01_coletar.py` as regex de tipo (reunião de diretoria/colegiado, audiência, consulta).
2. No chat: `03_preparar.py` → análise por subagentes (`prompt_analise.txt`, trocando «ANTT» e a lista de diretores) → `validar.py` → `05_indexar.py` → `organizar.py <sigla>`.
3. Mandatos/vacâncias próprios: `data/<sigla>/mandatos.json` e `data/<sigla>/vacancias.json`; `python3 pipeline/vacancias.py <sigla>`.

## Candidatas (canal oficial no YouTube a confirmar antes da coleta)
| Agência | Setor | Reuniões de diretoria transmitidas? | Observação |
|---|---|---|---|
| ANEEL | energia elétrica | sim (reuniões públicas semanais, longo histórico) | volume alto; votos nominais e sustentação oral |
| ANTAQ | transporte aquaviário/portos | sim | próxima da ANTT (concessões, arrendamentos) |
| ANAC | aviação civil | sim | |
| ANP | petróleo, gás, combustíveis | sim (circuitos deliberativos) | parte das decisões é em circuito, não em vídeo |
| ANS / ANVISA | saúde | sim | ANVISA tem pautas longas e muitos itens sigilosos |
| ANATEL | telecom | sim (Conselho Diretor) | |

Critérios sugeridos: relevância para o cliente, se as reuniões têm votos nominais em vídeo e se existe legenda automática.
