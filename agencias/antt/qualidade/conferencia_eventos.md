# Conferência dos eventos (audiências, participativas, workshops)

## 1. Trechos literais (todas as falas de diretor, automática)

Para cada fala registrada, procura-se o trecho literal na transcrição a até 10 min do minuto registrado (similaridade ≥ 0,6).

- Trecho encontrado na transcrição: **100.0% (74/74)**
- Encontrado a até 2 min do minuto registrado (link confiável): **94.6% (70/74)**

Detalhe em `conferencia_eventos_trechos.csv`.

## 2. Conferência cega (amostra de 20 eventos: 10 com fala de diretor, 10 sem)

Subagentes releram o resumo do evento (`data/analise_eventos/<id>.md`) e a transcrição **sem ver a análise** e listaram os diretores que falam.

- Concordância sobre «houve fala de diretor?»: **100.0% (20/20)**
- Mesmo conjunto de diretores falantes: **100.0% (20/20)**
- Diretores (por evento) identificados por ambos: **100.0% (10/10)**

Detalhe em `conferencia_eventos.csv`. **Limites:** mesma legenda automática e mesmo tipo de leitura (janelas do resumo, não a sessão inteira); mede consistência, não verdade absoluta.
