# Auditoria completa — 09/11/2026

O que foi conferido, como e com que resultado. Detalhes: `docs/AUDITORIA_dados.json` (automático, `pipeline/auditar.py`) e `docs/AUDITORIA_respostas.md` (afirmação por afirmação).

## 1. Base (ANTT e ANM) — automático
| Verificação | ANTT | ANM |
|---|---|---|
| Itens sem reunião / votos sem item | 0 / 0 | 0 / 0 |
| Reuniões sem vídeo nem ata | 0 | 0 |
| Links: minuto além do fim do vídeo | 2 de 9.249 | 0 de 14.155 |
| Trecho literal encontrado perto do minuto (amostra de 300) | 300/300 | 300/300 |
| Votos duplicados (mesmo diretor, mesmo item) | 6 (voto + voto-vista no mesmo item) | 1 |

## 2. Extração dos votos — conferência cega por amostra
| Rodada | Voto por diretor | Relator | Resultado |
|---|---|---|---|
| ANTT 2019–2024 (108 itens) | 94,6% | 93,5% | 92,6% |
| ANTT 2019–2024 (2ª, 36 itens) | 94,2% | 100% | 97,2% |
| ANTT 2025–2026 (48 itens) | 94,8% | 100% | 100% |
| **ANTT 2019–2026, rodada C sem vazamento (48 itens, nomes em ordem alfabética)** | **94,2%** | **93,8%** | **100%** |
| ANM 2019–2026 (72 itens) | 84,2% (2021–26 ≈ 96%; 2019 = 20%) | 97,2%* | 93,1% |
| ANM × atas oficiais (1.830 itens) | — | 89,8% | 97,9% |
| **ANTAQ 2019–2026 (49 itens, 16 reuniões, nomes em ordem alfabética)** | **92,3%** | **100%** | **100%** |
\* rodada com vazamento parcial (ordem dos nomes); o cruzamento com as atas confirma relator e resultado.

## 3. Relatórios entregues — evidências citadas
Todas as evidências citadas (RD, data, item) existem na base: ANTT 82/82, ANM 84/84.

## 4. Relatórios entregues — afirmações das respostas (leitor independente, SQL próprio)
132 afirmações: 100 confirmadas, 18 imprecisas, 1 sem base, 13 inferências (6 sustentadas, 3 parciais, 4 fracas).
**Erro grave encontrado e corrigido:** o desfecho «favorável/desfavorável à empresa» contava todo «aprovado por unanimidade» como favorável. Nova regra (`pipeline/desfecho.py`) usa o voto do relator: CONCER passou de «90 favoráveis» para **134 desfavoráveis, 23 parciais**; grupo Vale de «41 favoráveis» para **32 desfavoráveis, 10 favoráveis**; a afirmação de que a sustentação oral «muda» o resultado foi retirada (nos recursos não há diferença de mérito; muda o rito). Todas as 18 imprecisões foram corrigidas nos relatórios; padrões apoiados em um único caso foram reescritos como «caso isolado».

## 5. O que continua sendo inferência
Tom e «perfil» (cauteloso, procedimental) são leitura das justificativas, marcados como inferência. Desfecho para a empresa é aproximado (texto do voto do relator). Legenda automática erra nomes e números; 2019–2020 da ANM só como índice.

## 6. Atualização 10/11/2026
- **ANTAQ 2019–2026** entrou na base: 93 reuniões, 3.291 itens, 11.375 votos. Conferência cega: voto por diretor 92,3%, relator e resultado 100%. A maior parte da discordância é «acompanha» × «voto não ouvido» (votação simbólica). As datas de várias sessões vêm do upload do vídeo (anotado em cada análise); conferir com atas do gov.br.
- **Conferência:** o comparador passou a contar «aprovado»/«referendado» sem a palavra «unanimidade» como unânime quando não há voto divergente (antes caía em «outro»). ANM resultado 90,3% → 93,1%.
- **Desfecho para a empresa:** «multa reduzida»/«reduz a multa» agora conta como parcial. Respostas corrigidas com a base atual: CONCER 147 desfavoráveis / 9 parciais / 14 sem mérito; Rumo 15 / 8 favoráveis / 3 parciais / 23 neutros / 10 sem mérito; Vale (ANM) 31 / 7 / 6 / 28. Sustentação oral: 55% desfavorável com sustentação × 63% sem (n = 47).
- **Relatório:** a caixa «desfecho favorável» lia o número de «desfavorável» (regex); corrigido com `(?<!des)`.
- **ANTAQ 2015–2018** (55 reuniões; várias de 2015, publicadas em 2016): conferência cega de 45 itens — voto 96,3%, relator 100%, resultado 95,6%. Eventos ANTAQ: 137 analisados (364 falas de diretores). Base ANTAQ: 148 reuniões, 5.053 itens, 16.048 votos.
- **Skill cobertura-em-toda-resposta** + `pipeline/cobertura_resposta.py`: toda resposta traz canal × texto × analisado, lacunas e taxa da conferência.
