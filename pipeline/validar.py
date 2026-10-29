"""Valida data/analise/*.analise.json: JSON válido e campos mínimos. Uso: validar.py"""
import json, glob, sys
ok = True
for f in sorted(glob.glob("data/analise/*.analise.json")):
    try:
        d = json.load(open(f))
        assert d["reuniao"]["numero"] and d["reuniao"]["data"], "reuniao sem numero/data"
        for it in d["itens"]:
            assert it.get("id") and it.get("assunto"), f"item sem id/assunto: {it.get('id')}"
            for v in it.get("votos", []): assert v.get("diretor") and v.get("voto"), f"voto incompleto em {it['id']}"
        print("ok  ", f, len(d["itens"]), "itens")
    except Exception as e:
        ok = False; print("ERRO", f, e)
sys.exit(0 if ok else 1)
