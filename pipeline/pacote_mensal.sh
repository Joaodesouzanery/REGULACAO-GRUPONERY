#!/bin/bash
# Pacote mensal do cliente (skill pacote-mensal): 4 PDFs + checagens + cópia para entrega/.
# Uso: bash pipeline/pacote_mensal.sh clientes/<x>/<pasta> AAAA-MM
set -e
P="${1%/}"; MES="$2"
[ -f "$P/empresa.json" ] || { echo "Pasta do cliente não encontrada: $P (gere no chat; clientes/ não vai ao Mac)"; exit 1; }
[[ "$MES" =~ ^[0-9]{4}-[0-9]{2}$ ]] || { echo "Mês no formato AAAA-MM"; exit 1; }
AG=$(python3 -c "import json;print(json.load(open('$P/empresa.json')).get('agencias',['antaq'])[0])")
NOME=$(python3 -c "import json;print(json.load(open('$P/empresa.json'))['nome'].split('(')[0].strip().replace(' ','_'))")
MESN=$(python3 -c "m='janeiro fevereiro março abril maio junho julho agosto setembro outubro novembro dezembro'.split();print(m[int('$MES'[5:])-1]+'_'+'$MES'[:4])")
echo "== reindexando $AG"; bash pipeline/ag.sh "$AG" python3 pipeline/05_indexar.py >/dev/null
echo "== 1 relatório";  python3 pipeline/relatorio_nery.py "$P"
echo "== 2 boletim";    python3 pipeline/boletim_cliente.py "$P" "$MES"
echo "== 3 raio-X";     python3 pipeline/raio_x.py "$P"
echo "== 4 agenda";     python3 pipeline/agenda_comparativa.py "$P"
echo "== auditoria de falas"
for h in relatorio_empresa boletim_cliente_$MES raio_x_processos agenda_comparativa; do python3 pipeline/auditar_falas.py "$P/$h.html" --ag "$AG" || echo "ATENÇÃO: trecho não encontrado em $h"; done
mkdir -p "$P/entrega"
cp "$P/relatorio_empresa.pdf" "$P/entrega/1_Relatorio_${NOME}_${AG^^}.pdf"
cp "$P/boletim_cliente_$MES.pdf" "$P/entrega/2_Boletim_mensal_${NOME}_${MESN}.pdf"
cp "$P/raio_x_processos.pdf" "$P/entrega/3_Raio-X_dos_Processos.pdf"
cp "$P/agenda_comparativa.pdf" "$P/entrega/4_Agenda_e_Inteligencia_Comparativa.pdf"
[ -f pipeline/planilha_cliente.py ] && python3 pipeline/planilha_cliente.py "$P" >/dev/null 2>&1 || true
echo "== pronto: $P/entrega  (falta no chat: auditor-respostas, guardiao-dados-cliente, revisor-visual, conformidade-entrega)"
