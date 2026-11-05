# Qualidade das análises — ANTT (conferência por amostra cega)

Subagentes independentes releram a transcrição **sem ver a análise original** e extraíram de novo relator, resultado e voto de cada diretor (reuniões de diretoria) ou os diretores que falam (eventos). O resultado mede **consistência**, não verdade absoluta: os dois leitores usam a mesma legenda automática.

| Rodada | Amostra | Relator | Resultado | Voto por diretor | Relatório |
|---|---|---|---|---|---|
| 2019–2024 (1ª) | 108 itens / 36 reuniões | 93,5% | 92,6% | 93,5% (447/478) | `conferencia_amostra.md` |
| 2019–2024 (2ª, reuniões novas) | 36 itens / 12 reuniões | 100% | 97,2% | 94,2% (145/154) | `conferencia_2019_2024_b.md` |
| 2025–2026 | 48 itens / 16 reuniões | 100% | 100% | 88,1% (170/193)* | `conferencia_2025_2026.md` |
| Eventos: trechos literais | 74 falas (todas) | — | — | 100% encontradas; 95% (70/74) a até 2 min do minuto citado | `conferencia_eventos.md` |
| Eventos: quem falou | 20 eventos (10 com e 10 sem fala de diretor) | — | — | 100% (20/20) mesmo conjunto de diretores | `conferencia_eventos.md` |

\* Em 2025–2026, 12 das 23 discordâncias são «vista → acompanha»: o diretor pediu vista e depois deu voto-vista convergente. É diferença de convenção de registro, não de fato. Desconsiderando esses casos, a concordância fica em ≈ 94%.

**Taxa para citar nas respostas:** ≈ 93–94% de concordância nos votos por diretor (2019–2026); relator e resultado entre 93% e 100%. 2019 é o ano mais fraco (legendas truncadas, 75–92%).

Reproduzir: `python3 pipeline/amostra.py sortear|comparar [2019_2024|2025_2026|2019_2024_b]` e `python3 pipeline/conferencia_eventos.py trechos|sortear|comparar` (prompts: `pipeline/prompt_conferencia.txt`).
