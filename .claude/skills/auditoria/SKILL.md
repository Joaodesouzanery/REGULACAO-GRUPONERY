---
name: auditoria
description: Auditoria completa da base e dos relatórios — integridade, links no minuto, trechos literais, conferência cega, e afirmação por afirmação das respostas entregues. Use quando o usuário pedir «conferência», «auditoria», «os dados são confiáveis?», ou antes de entregar um pacote importante.
---
# Auditoria

1. **Base (automático):** `python3 pipeline/auditar.py` (ANTT, ANM, ANTAQ): órfãos, links além do fim do vídeo, trecho literal perto do minuto (amostra 300), duplicados, evidências citadas nos relatórios existem. Saída: `docs/AUDITORIA_dados.json`.
2. **Extração (cega):** `amostra.py sortear <rodada>` → subagentes `conferente-cego` → `amostra.py comparar <rodada>`. Nomes em ordem alfabética (sem vazar o relator).
3. **Atas oficiais:** `cruzar_atas.py` quando houver atas (ANM 97,9% resultado; ANTAQ: gov.br).
4. **Respostas entregues:** subagente `auditor-respostas` por relatório — cada número, tendência e evidência contra SQL próprio. Desfecho para empresa só via `pipeline/desfecho.py`.
5. **Coerência texto × números:** quando `desfecho.py` ou a base mudam, recalcule com `consulta.py empresa|grupo|sustentacoes` e corrija as respostas curtas (ex.: nov/2026: CONCER 134→147 desfavoráveis após correção do regex; «multa reduzida» passou a contar como parcial).
6. **Visual:** subagente `revisor-visual`.
7. Registre em `docs/AUDITORIA.md` (data, o que mudou, taxas) e diga ao usuário o que foi corrigido. Taxas medem consistência, não verdade absoluta.
