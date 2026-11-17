---
name: revisao-portugues
description: Garante português correto em TODOS os documentos (PDF/HTML de cliente, apresentação, e-mails, posts, README): acentuação, crase óbvia, espaços, aspas «», travessão só onde precisa — sem mexer nas falas literais da legenda. Use antes de entregar qualquer documento e ao escrever texto novo em scripts ou narrativas.
---
# Revisão de português
1. **Automático na geração**: `design.documento()` (e monitoramento/demo via `sem_travessao`) corrige acentos de rótulos vindos de nomes técnicos (ex.: `servicos_terminais` → «serviços terminais») e troca travessão de texto corrido por vírgula. Falas entre «» e URLs não são tocadas.
2. **Conferência**: `python3 pipeline/revisar_portugues.py <arquivos .html/.pdf/.md>` → alertas por tipo (acento, crase, travessão, espaço, aspas). Entrega só com 0 alertas (exceto dentro de falas literais).
3. **Corrigir fonte**: `--corrigir` em .md/.json (só palavras da lista segura). Em scripts Python, corrija à mão o texto fixo.
4. **Revisão humana de estilo**: agente `revisor-portugues` (lê o texto e aponta concordância, regência, frase longa, termo técnico errado).
5. Falas literais da legenda ficam como estão: o documento já avisa que a legenda é automática.
6. Ao achar erro novo recorrente, inclua o par em `PARES` no `revisar_portugues.py`.
