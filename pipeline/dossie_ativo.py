"""Dossiê de um ATIVO (terminal, arrendamento, concessão): todas as deliberações da diretoria sobre ele, empresas afetadas e voto de cada diretor.
Uso: python3 pipeline/dossie_ativo.py <ag> "<regex do ativo>" "<título>" --marca circle|iris|nery [--excluir "<regex>"] [--subtitulo "..."]
Saída: clientes/_prospeccao/<slug>/dossie.pdf (fora do git). Só dado público; marca perguntada ao usuário (skill marca-relatorio)."""
import sys, os, re, datetime, collections, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import previsao, mapa_tema, design as d
E = d.E
arg = lambda k, x=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else x
AG, RX, TIT = sys.argv[1].lower(), sys.argv[2], sys.argv[3]
d.MARCA = arg("--marca") or sys.exit("Informe --marca (pergunte ao usuário).")
EXC = arg("--excluir"); SUB = arg("--subtitulo", "Deliberações da diretoria, empresas afetadas e voto de cada diretor")
fmtd = lambda s: datetime.date.fromisoformat(str(s)[:10]).strftime("%d/%m/%Y")
corte = lambda t, n: (t or "") if len(t or "") <= n else (t or "")[:n].rsplit(" ", 1)[0] + "…"
limpa = lambda t: re.sub(r"\s*\((legenda|inferido)[^)]*\)", "", t or "").strip(" ;")
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()).strip("-")
OUT = f"clientes/_prospeccao/{slug(TIT)}"; os.makedirs(OUT, exist_ok=True)
c = previsao.conn(AG); R = re.compile(RX, re.I); X = re.compile(EXC, re.I) if EXC else None
IT = [i for i in c.execute("select i.*, r.data, r.numero, r.video_id from itens i join reunioes r on r.id=i.reuniao_id order by r.data, i.id")
      if R.search(f"{i['interessado']} {i['assunto']}") and not (X and X.search(f"{i['interessado']} {i['assunto']}"))]
if not IT: sys.exit("nenhum item")


def rotulo(v):
    t = (v["voto"] or "").lower(); cat = v["categoria"]
    if "vencid" in t: return "vencido(a)"
    if re.search(r"acompanha o (revisor|voto-vista|alber)|acompanha .*voto-vista", t) and cat != "relator": return "acompanhou o voto-vista"
    if re.search(r"concede a vista|presid|prop[õo]e", t): return "presidiu; " + ("concedeu a vista (não votou)" if "vista" in t else "propôs a solução adotada")
    if cat == "revisor_diverge" and re.search(r"adere|proposta única", t): return "divergiu no voto-vista; aderiu à proposta única"
    if cat == "relator": return "relator(a)"
    if cat == "revisor_diverge": return "divergiu (voto-vista)" if "revisor" in t or "vista" in t else "divergiu do relator"
    if cat == "revisor_acompanha": return "acompanhou o voto-vista"
    if cat == "vista" or t.startswith("pede vista"): return "pediu vista"
    if "não votou" in t: return "não votou (vista)"
    if cat == "acompanha": return "acompanhou"
    return corte(v["voto"], 40) or cat


VOT = {i["id"]: list(c.execute("select * from votos where item_id=? order by eh_relator desc, id", (i["id"],))) for i in IT}
DIRS = sorted({v["diretor"] for vs in VOT.values() for v in vs}, key=lambda n: min(i["data"] for i in IT if any(v["diretor"] == n for v in VOT[i["id"]])))
CAN = [(r"A?TU ?-?12 Arrend", "ATU 12 Arrendatária Portuária SPE S.A."), (r"Magnesita", "Magnesita (RHI Magnesita)"), (r"Minfra|Minist[eé]rio da Infra|SNPTA", "Ministério da Infraestrutura (órgão)"),
       (r"Codeba", "Codeba (autoridade portuária)"), (r"Tecon Salvador", "Tecon Salvador"), (r"Intermar", "Intermarítima")]
canon = lambda t: [nome for rx, nome in CAN if re.search(rx, t or "", re.I)]
emp = collections.Counter(n for i in IT for n in canon(i["interessado"]) + canon(i["assunto"]))
n_emp = sum(1 for n in emp if "(órgão)" not in n and "autoridade" not in n); n_org = len(emp) - n_emp
principal = max(IT, key=lambda i: (sum(1 for v in VOT[i["id"]] if v["categoria"] in ("revisor_diverge", "vencido")), len(i["resumo"] or "")))
S = [d.capa(d.kit(d.SETOR_AG.get(AG, "portos"))["capa"], "50% 55%", f"Dossiê do ativo · {d.NOME_AG.get(AG, AG.upper())}", TIT, SUB,
            f"Reuniões públicas da diretoria de {fmtd(IT[0]['data'])} a {fmtd(IT[-1]['data'])}. Só fontes públicas.",
            [(len(IT), "deliberações sobre o ativo"), (f"{IT[0]['data'][:4]}–{IT[-1]['data'][:4]}", "período"), (len(DIRS), "diretores que votaram"),
             (f"{n_emp} + {n_org}", "empresas + órgãos públicos citados")])]
# linha do tempo
lt = [[f"{fmtd(i['data'])}<br>{i['numero']}ª · item {E(str(i['item']))}", E(corte(i["assunto"], 150)), E(corte(i["resultado"], 110))] for i in IT]
S.append(d.tecnica("01 · Linha do tempo", "Todas as deliberações sobre o ativo", d.tabela(["Reunião", "O que estava em julgamento", "Resultado"], lt, ["14%", "52%", "34%"]), AG,
                   "Itens da base de reuniões gravadas; números de processo e nomes vêm da legenda automática e podem ter erro de grafia."))
# uma ficha por deliberação, 2 por página
GR, cur = [], []
for i in IT:
    if cur and len(VOT[cur[0]["id"]]) + len(VOT[i["id"]]) > 11: GR.append(cur); cur = []
    cur.append(i)
    if len(cur) == 2: GR.append(cur); cur = []
if cur: GR.append(cur)
for g in GR:
    k = IT.index(g[0]); corpo = ""
    for i in g:
        rows = []
        for v in VOT[i["id"]]:
            tr = f'<i>«{E(corte(v["trecho"], 95))}»</i> <a href="{mapa_tema.link(i["video_id"], v["ts"] or i["ts"], v["trecho_t"])}">▶ minuto</a>' if v["trecho"] else "—"
            rows.append([f"<b>{E(v['diretor'])}</b>", E(rotulo(v)), tr])
        corpo += (f'<h3>{fmtd(i["data"])} · {i["numero"]}ª reunião, {("item " + E(str(i["item"]).replace("pauta ", "")) + (" da pauta" if "pauta" in str(i["item"]) else ""))}</h3>'
                  f'<p><b>Empresas e órgãos:</b> {E("; ".join(canon(i["interessado"])) or limpa(i["interessado"]))}<br><b>Em julgamento:</b> {E(corte(i["assunto"], 160))}<br>'
                  f'<b>Decisão:</b> {E(i["resultado"] or "")}' + (f'<br><b>Fundamento registrado:</b> {E(corte(i["resumo"], 170))}' if i["resumo"] else "") + "</p>"
                  + d.tabela(["Diretor", "Voto", "Fala no minuto (legenda automática)"], rows, ["18%", "18%", "64%"]))
    S.append(d.tecnica("02 · Deliberações", (f"Decisões e votos ({k + 1}–{k + len(g)} de {len(IT)})" if len(g) > 1 else f"Decisão e votos ({k + 1} de {len(IT)})"), corpo, AG,
                       "Quem só acompanhou, presidiu ou não votou aparece com o trecho da proclamação ou da condução da sessão; o minuto desses votos é aproximado."))
# matriz de votos
ab = {"relator(a)": "R", "acompanhou": "A", "acompanhou o voto-vista": "A·vv", "divergiu (voto-vista)": "D·vv", "divergiu do relator": "D", "pediu vista": "V", "vencido(a)": "venc.", "não votou (vista)": "—", "divergiu no voto-vista; aderiu à proposta única": "D·vv→A"}
mat = [[f"{fmtd(i['data'])}"] + [next((ab.get(rotulo(v), "P" if rotulo(v).startswith("presidiu") else rotulo(v)[:10]) for v in VOT[i["id"]] if v["diretor"] == n), "") for n in DIRS] for i in IT]
S.append(d.tecnica("03 · Quadro de votos", "Como cada diretor votou, deliberação por deliberação", d.tabela(["Data"] + [E(n) for n in DIRS], mat) +
                   '<p style="font-size:8.5pt">R = relator(a) · A = acompanhou · A·vv = acompanhou o voto-vista · D·vv = divergiu com voto-vista · V = pediu vista · venc. = vencido(a) · — = não votou naquela sessão · D·vv→A = divergiu no voto-vista e aderiu à proposta única · P = presidiu (concedeu vista ou propôs a solução) · vazio = não estava na sessão.</p>', AG))
S.append(d.fim("Dossiê feito só com fontes públicas: reuniões gravadas e transmitidas da diretoria, pautas e Diário Oficial. Legenda automática pode errar nomes e números; conferência cega da base: voto por diretor ≈ 94–95% (mede consistência, não verdade absoluta).",
               "Grupo Nery · inteligência regulatória", d.kit(d.SETOR_AG.get(AG, "portos"))["capa"]))
print(d.documento(S, TIT, f"{OUT}/dossie"), len(S), "páginas")
