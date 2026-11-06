# Qualidade das análises — ANTT (conferência por amostra cega)

Subagentes independentes releram a transcrição **sem ver a análise original** e extraíram de novo relator, resultado e voto de cada diretor (reuniões de diretoria) ou os diretores que falam (eventos). O resultado mede **consistência**, não verdade absoluta: os dois leitores usam a mesma legenda automática.

| Rodada | Amostra | Relator | Resultado | Voto por diretor | Relatório |
|---|---|---|---|---|---|
| 2019–2024 (1ª) | 108 itens / 36 reuniões | 93,5% | 92,6% | 94,6% (452/478) | `conferencia_amostra.md` |
| 2019–2024 (2ª, reuniões novas) | 36 itens / 12 reuniões | 100% | 97,2% | 94,2% (145/154) | `conferencia_2019_2024_b.md` |
| 2025–2026 | 48 itens / 16 reuniões | 100% | 100% | 94,8% (183/193) | `conferencia_2025_2026.md` |
| Eventos: trechos literais | 74 falas (todas) | — | — | 100% encontradas; 95% (70/74) a até 2 min do minuto citado | `conferencia_eventos.md` |
| Eventos: quem falou | 20 eventos (10 com e 10 sem fala de diretor) | — | — | 100% (20/20) mesmo conjunto de diretores | `conferencia_eventos.md` |

Convenção (desde 06/11/2026): «voto-vista» conta como acompanha/diverge; «vista» só para quem apenas pediu vista. Com a convenção antiga, 2025–2026 ficava em 88,1% (12 discordâncias eram só de rótulo). Cada relatório lista as discordâncias **por diretor**, com RD e item.

**Taxa para citar nas respostas:** ≈ 94–95% de concordância nos votos por diretor (2019–2026); relator e resultado entre 93% e 100%. 2019 é o ano mais fraco (legendas truncadas, 75–92%).

Reproduzir: `python3 pipeline/amostra.py sortear|comparar [2019_2024|2025_2026|2019_2024_b]` e `python3 pipeline/conferencia_eventos.py trechos|sortear|comparar` (prompts: `pipeline/prompt_conferencia.txt`).
