---
name: mapa-assunto
description: Mapeia como cada diretor vota num assunto (ex.: reequilíbrio de arrendamento, passivo ambiental) — relatorias, acompanha, diverge, vista, vencido — com pipeline/mapa_tema.py e conferência de falso positivo. Use quando pedir «como cada diretor vota em X» ou na etapa 4 do montar-relatorio.
---
1. Escolher a regex (agente **analista-tema**): sinônimos, grafias erradas da legenda, excluir termos que geram ruído.
2. `python3 pipeline/mapa_tema.py <ag> "<regex>" [--desde AAAA-MM-DD]` → tabela por diretor + lista de itens.
3. Conferir 10 itens sorteados da lista: o item é mesmo do assunto? Precisão **≥ 90%**; senão, refinar a regex e repetir.
4. Na resposta: todos os diretores em exercício lado a lado (skill comparar-diretores), n por diretor, a regex usada, a precisão medida e exemplos com trecho literal e link no minuto. Tom só como inferência. Terminar com cobertura.
