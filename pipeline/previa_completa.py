"""Prévia COMPLETA gratuita (10–14 páginas) para prospect, só com dado público: capa, painel com falas, diretoria sem desfoque
e controle por cadeira, temas da empresa analisados, agenda e «o que observar», um processo em detalhe (8 blocos condensado)
e a página «o que vem no pacote completo». Marca «PRÉVIA · válida por 30 dias».
Uso: python3 pipeline/previa_completa.py <ag> "<Empresa>" "<alias1|alias2>" [--foto x.jpg] [--logo y.png]
Saída: clientes/_prospeccao/<slug>/previa/previa_completa.pdf (fora do git)."""
import sys, os, re, json, collections, unicodedata, subprocess, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import previsao, prazos
AG, NOME, ALI = sys.argv[1].lower(), sys.argv[2], sys.argv[3].split("|")
arg = lambda k: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else None
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()).strip("-")
P = f"clientes/_prospeccao/{slug(NOME)}/previa"; os.makedirs(P, exist_ok=True)
D = "data" if AG == "antt" else f"data/{AG}"
cfg = json.load(open(f"{D}/config_agencia.json")) if os.path.exists(f"{D}/config_agencia.json") else {}
c = previsao.conn(AG)
its = [i for i in previsao.itens_empresa(c, ALI) if i["data"] >= "2018-01-01"]
if not its: sys.exit(f"Nenhuma decisão encontrada para {NOME} com esses aliases na {AG.upper()}.")
# temas mais frequentes da empresa → regex do config
cnt = collections.Counter(t for i in its for (t,) in c.execute("select tema from item_temas where item_id=?", (i["id"],)))
rx = {t: r for t, r in (cfg.get("temas") or [])} if isinstance(cfg.get("temas"), list) else {}
temas = [{"titulo": f"{chr(97 + k)}) {t.replace('_', ' ').capitalize()}: como cada diretor vota", "regex": rx.get(t) or re.escape(t.replace("_", " "))} for k, (t, _) in enumerate(cnt.most_common(2))]
emp = {"nome": NOME, "aliases": ALI, "agencias": [AG], "temas_consultoria": temas, "contato": "Grupo Nery · peça a versão completa", "notas_ativas": ["virtual", "retirado", "vista", "mandato_relator"]}
if arg("--foto"): emp["foto_capa"] = arg("--foto")
if arg("--logo"): emp["logo"] = arg("--logo")
json.dump(emp, open(f"{P}/empresa.json", "w"), ensure_ascii=False, indent=1)
# painel automático (3 blocos) a partir dos dados
fmt = lambda s: datetime.date.fromisoformat(s[:10]).strftime("%d/%m/%Y")
tres = [i for i in its if i["data"] >= (datetime.date.today() - datetime.timedelta(days=3 * 365)).isoformat()]
rel = collections.Counter(i["relator"] for i in tres if i["relator"])
ult = its[-3:][::-1]
abertos = [i for i in its[-10:] if re.search(r"vista|retirad|dilig", (i["resultado"] or "").lower())]
p1 = (f"Desde 2018 a diretoria da {AG.upper()} decidiu {len(its)} itens envolvendo a {NOME}, {len(tres)} deles nos últimos 3 anos. "
      f"Quem mais relatou: " + ", ".join(f"{n} ({v})" for n, v in rel.most_common(3)) + ". As decisões mais recentes: "
      + "; ".join(f"{i['numero']}ª ROD ({fmt(i['data'])}), item {i['item']}: {(i['assunto'] or '')[:110]}, {(i['resultado'] or '')[:70]}" for i in ult) + ".")
p2 = ("Em aberto ou com retorno provável: " + "; ".join(f"{i['numero']}ª ROD, item {i['item']}: {(i['assunto'] or '')[:100]} ({(i['resultado'] or '')[:60]})" for i in abertos) + ".") if abertos else \
     "Não há item da empresa com vista, retirada ou diligência pendente nas últimas sessões; o pacote completo acompanha cada nova pauta."
cal = [x for x in (json.load(open(f"{D}/calendario.json")) if os.path.exists(f"{D}/calendario.json") else []) if x["data"] >= datetime.date.today().isoformat()][:2]
p3 = ("Próximas reuniões da diretoria: " + "; ".join(f"{x['reuniao']}ª em {fmt(x['data'])} ({x.get('formato', '')}{', sem transmissão' if x.get('formato') == 'virtual' else ''})" for x in cal) + ". No pacote completo, o alerta sai assim que a pauta é publicada.") if cal else \
     "O calendário oficial e as pautas entram no pacote completo, com alerta antes de cada reunião."
json.dump({"painel": {"paragrafos": [p1, p2, p3], "citacoes": []}}, open(f"{P}/narrativas.json", "w"), ensure_ascii=False, indent=1)
r = subprocess.run(["python3", "pipeline/relatorio_nery.py", P], env={**os.environ, "PREVIA": "1"}, capture_output=True, text=True)
print(r.stdout[-600:], r.stderr[-800:])
