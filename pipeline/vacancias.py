"""Estatísticas de vacância de cadeira titular a partir de data/vacancias.json. Uso: python3 pipeline/vacancias.py [agencia]
Gera agencias/<agencia>/mandatos/{README.md,vacancias.csv}."""
import json, sys, os, csv, datetime, statistics
ag = sys.argv[1] if len(sys.argv) > 1 else "antt"
hoje = datetime.date.today()
d = lambda s: datetime.date.fromisoformat(s)
V = json.load(open("data/vacancias.json"))
for v in V:
    v["dias"] = ((d(v["fim"]) if v["fim"] else hoje) - d(v["inicio"])).days + 1; v["aberta"] = v["fim"] is None
os.makedirs(f"agencias/{ag}/mandatos", exist_ok=True)
with open(f"agencias/{ag}/mandatos/vacancias.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["id", "cadeira", "inicio", "fim", "dias", "aberta", "preenchida_por", "interinos", "confianca", "fonte"])
    for v in V: w.writerow([v["id"], v["cadeira"], v["inicio"], v["fim"] or "", v["dias"], v["aberta"], v["preenchida_por"], v["interinos"], v["confianca"], v["fonte"]])
def est(vs):
    ds = [v["dias"] for v in vs]
    return f"{len(ds)} vacâncias · média {statistics.mean(ds):.0f} dias · mediana {statistics.median(ds):.0f} · máx {max(ds)}" if ds else "—"
rec = [v for v in V if v["inicio"] >= "2023-01-01"]; fech = [v for v in V if not v["aberta"]]
# dias-cadeira vagos / dias-cadeira possíveis (5 cadeiras) em 2023-01-01..hoje
ini = datetime.date(2023, 1, 1); tot = (hoje - ini).days * 5
vag = sum(((d(v["fim"]) if v["fim"] else hoje) - max(d(v["inicio"]), ini)).days + 1 for v in rec)
md = [f"# Mandatos e vacâncias — {ag.upper()}", "", f"Atualizado em {hoje}. **Estimativas**: as datas vêm de resultados de busca (Senado, Agência iNFRA, gov.br/ANTTlegis; as páginas oficiais não puderam ser abertas diretamente) e dos votos nas transcrições. Cada linha tem confiança e fonte; confirmar no DOU.", "",
      f"- Todas as vacâncias estimadas (2020–2026): {est(V)}", f"- Só vacâncias encerradas: {est(fech)}", f"- A partir de 2023 (maior confiança): {est(rec)}",
      f"- Fração do tempo com cadeira titular vaga desde 01/01/2023: **{100*vag/tot:.1f}%** dos dias-cadeira ({vag} de {tot}).", "",
      "| Id | Cadeira | Início | Fim | Dias | Preenchida por | Interinos / substitutos | Confiança |", "|---|---|---|---|---|---|---|---|"]
for v in V: md.append(f"| {v['id']} | {v['cadeira']} | {v['inicio']} | {v['fim'] or 'em aberto'} | {v['dias']} | {v['preenchida_por']} | {v['interinos']} | {v['confianca']} |")
md += ["", "## Mandatos (resumo)", "", "Ver `data/mandatos.json` (campos: nomeação no DOU, aprovação no Senado, início/fim estimados, confirmado, fonte). Mandato de diretor da ANTT: 5 anos, sem recondução; substituto convocado por até 180 dias ou até a nomeação de novo titular.",
       "", "## Para outras agências", "Repita com `data/<agencia>/vacancias.json` no mesmo formato e rode `python3 pipeline/vacancias.py <agencia>`; a média de vacância por agência fica em `agencias/<agencia>/mandatos/README.md`."]
open(f"agencias/{ag}/mandatos/README.md", "w").write("\n".join(md) + "\n"); print("\n".join(md[4:9]))
