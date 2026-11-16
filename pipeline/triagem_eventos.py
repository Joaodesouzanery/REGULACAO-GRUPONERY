"""Triagem de eventos (audiências, workshops, participativas) por prioridade de análise (skill triagem-eventos).
alta = audiência/consulta pública, tomada de subsídios, esclarecimento de leilão, revisão de resolução, tarifa;
baixa = encerramento de P&D, internacionais, painéis acadêmicos, outro idioma (guardados, não analisados).
Uso: python3 pipeline/triagem_eventos.py <ag>   → data/<ag>/eventos_prioridade.json + resumo"""
import sys, os, json, re, collections
AG = sys.argv[1]; D = "data" if AG == "antt" else f"data/{AG}"
ALTA = re.compile(r"audi[eê]ncia p[uú]blica|consulta p[uú]blica|tomada de subs[ií]dios|esclarecimento|leil[aã]o|revis[aã]o (da|de) resolu|resolu[cç][aã]o normativa|tarif|reajuste|revis[aã]o tarif|concess|edital|regulament|sandbox", re.I)
BAIXA = re.compile(r"^public hearing|^webinar|encerramento|p ?& ?d|internacional|international|workshop .*(learn|tariff sandboxes)|semin[aá]rio acad|painel \d|15 anos|anivers|homenagem|teste", re.I)
V = [json.loads(l) for l in open(f"{D}/videos.jsonl")]
ev = [v for v in V if v.get("tipo") not in ("diretoria", "outro") and not v.get("duplicata_de")]
out = {}
for v in ev:
    t = v.get("titulo") or ""
    p = "baixa" if BAIXA.search(t) or re.search(r"\[(en|es)\]", t) else "alta" if ALTA.search(t) or v["tipo"] in ("audiencia", "participativa") else "media"
    out[v["id"]] = {"titulo": t, "tipo": v["tipo"], "data": v.get("data"), "prioridade": p, "texto": os.path.exists(f"{D}/transcricoes/{v['id']}.json"),
                    "analisado": os.path.exists(f"{D}/analise_eventos/{v['id']}.evento.json")}
json.dump(out, open(f"{D}/eventos_prioridade.json", "w"), ensure_ascii=False, indent=1)
c = collections.Counter((x["prioridade"], x["texto"], x["analisado"]) for x in out.values())
print(f"{AG.upper()}: {len(out)} eventos")
for pr in ("alta", "media", "baixa"):
    tot = sum(v for (p, *_), v in c.items() if p == pr); tx = sum(v for (p, t, _), v in c.items() if p == pr and t); an = sum(v for (p, _, a), v in c.items() if p == pr and a)
    print(f"  {pr}: {tot} (com texto {tx}, analisados {an})")
