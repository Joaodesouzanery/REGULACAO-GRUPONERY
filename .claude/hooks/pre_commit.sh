#!/bin/bash
# PreToolUse (Bash): antes de «git commit», roda a checagem de integridade; se falhar, bloqueia (exit 2).
cmd="$(python3 -c 'import json,sys;print(json.load(sys.stdin).get("tool_input",{}).get("command",""))' 2>/dev/null)"
case "$cmd" in *"git commit"*) ;; *) exit 0;; esac
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
out="$(python3 pipeline/checar_integridade.py 2>&1)"; rc=$?
[ $rc -eq 0 ] && exit 0
echo "checar_integridade.py falhou — commit bloqueado (skill cuidados-pipeline):" >&2; echo "$out" | tail -15 >&2; exit 2
