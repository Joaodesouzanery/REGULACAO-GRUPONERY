"""Valida data/analise_eventos/*.evento.json. Uso: python3 pipeline/validar_evento.py"""
import json, glob, re, sys
erros = 0
for f in sorted(glob.glob("data/analise_eventos/*.evento.json")):
    try:
        d = json.load(open(f)); e = d["evento"]
        assert d["meta"]["video_id"] and e["tipo"] in ("audiencia", "participativa", "workshop", "romeiros"), "tipo"
        assert re.match(r"\d{4}-\d\d-\d\d", e.get("data") or ""), "data"
        assert isinstance(e.get("tema"), list) and e.get("objeto") and e.get("resumo"), "campos"
        for x in d.get("falas_diretores", []):
            assert x["diretor"] and re.match(r"\d+:\d\d:\d\d", x["ts"]) and x["resumo"], "fala"
        print("ok  ", f, len(d.get("falas_diretores", [])), "falas")
    except Exception as ex:
        erros += 1; print("ERRO", f, repr(ex))
sys.exit(1 if erros else 0)
