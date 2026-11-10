---
description: Responde uma pergunta sobre diretor/agência com evidência (ficha fixa, trecho literal, link no minuto)
argument-hint: "<pergunta>"
---
Pergunta: $ARGUMENTS

Siga a skill `resposta-com-evidencia`: rode `python3 pipeline/05_indexar.py` (ou `bash pipeline/ag.sh <sigla> python3 pipeline/05_indexar.py` para ANM/ANTAQ), consulte com `pipeline/consulta.py` (ficha, tema, empresa, grupo, microtema, precedentes…), e responda na ficha fixa: resposta curta, números com n, evidências (reunião, data, item, voto, justificativa, trecho literal, link &t=), confiança e o que não temos.
