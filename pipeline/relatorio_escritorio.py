"""Relatório para ESCRITÓRIO DE ADVOCACIA (linha atacado / parceria IRIS), só dado público:
1) próximas agendas, 2) como a diretoria votou em pautas parecidas com a atuação do escritório, 3) prospecção (empresas com processo ativo).
Uso: python3 pipeline/relatorio_escritorio.py "Lobo de Rizzo" [--marca iris]
Temas por agência em TEMAS abaixo (editar por escritório). Saída: clientes/_prospeccao/<slug>/relatorio_escritorio.pdf (fora do git)."""
import sys, os, re, json, datetime, collections, unicodedata, statistics
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import previsao, mapa_tema, prazos, retiradas, design as d
from desfecho import desfecho_item
E = d.E
NOMEESC = sys.argv[1]; MARCA = sys.argv[sys.argv.index("--marca") + 1] if "--marca" in sys.argv else "nery"
HOJE = datetime.date.today(); ANO = (HOJE - datetime.timedelta(days=365)).isoformat(); DESDE = "2023-01-01"
fmtd = lambda s: (datetime.date.fromisoformat(str(s)[:10]).strftime("%d/%m/%Y") if len(str(s)) >= 10 else "/".join(reversed(str(s).split("-")))) if s else "—"
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()).strip("-")
OUT = f"clientes/_prospeccao/{slug(NOMEESC)}"; os.makedirs(OUT, exist_ok=True)
TEMAS = {
    "antt": ("Concessões rodoviárias e ferroviárias: reequilíbrio, revisão, prorrogação, relicitação e aditivos",
             r"reequil[ií]brio|revis[aã]o quinquenal|relicita|prorroga[cç][aã]o.*concess|otimiza[cç][aã]o.*contrat|repactua|termo aditivo"),
    "antaq": ("Portos de Santos e São Sebastião: arrendamento, desestatização, reequilíbrio e prorrogação",
              r"(Santos|S[aã]o Sebasti[aã]o).*(arrendamento|desestatiza|reequil|prorroga)|(arrendamento|desestatiza|reequil|prorroga).*(Santos|S[aã]o Sebasti[aã]o)")}
SINAIS = {"antt": "EcoRioMinas|Eco Rio Minas|Ecorodovias|Rodovias do Tiet", "antaq": "S[aã]o Sebasti[aã]o|Santos Port|SPA|desestatiza"}
KIT = d.kit("rodovias"); KITP = d.kit("portos")
S = []


def casos(ag, its, n=3):
    c = previsao.conn(ag); rows = []
    for i in list(reversed(its))[:40]:
        v = c.execute("select * from votos where item_id=? and trecho is not null and trecho<>'' order by eh_relator desc limit 1", (i["id"],)).fetchone()
        if not v: continue
        rows.append([f'{fmtd(i["data"])}<br>{i["numero"]}ª', E((i["assunto"] or "")[:110]), f'<b>{E(v["diretor"])}</b>{" (relator)" if v["eh_relator"] else ""}<br><i>«{E(v["trecho"][:140])}»</i> <a href="{mapa_tema.link(i["video_id"], v["ts"] or i["ts"], v["trecho_t"])}">▶ minuto</a>', E((i["resultado"] or "")[:70])])
        if len(rows) >= n: break
    return d.tabela(["Data", "Assunto", "Fala no minuto", "Resultado"], rows, ["10%", "34%", "40%", "16%"])


ALIAS = [(r"\bAPPA\b|Paranagu[aá] e Antonina|Portos do Paran[aá]", "APPA (Portos do Paraná)"),
         (r"Autoridade Portu[aá]ria de Santos|\bSPA\b|Santos Port Authority|Codesp", "Autoridade Portuária de Santos (SPA)"),
         (r"Eco ?Rio ?Minas|Ecorodovias|Eco ?Rodovias|Eco ?050|Eco ?101|Eco ?135|Ecovias|Ecoponte|Ecosul|Eco ?Noroeste|Ecovia", "Grupo Ecorodovias"),
         (r"Motiva|\bCCR\b|RioSP|ViaCosteira|ViaOeste|AutoBAn|NovaDutra", "Grupo Motiva (ex-CCR)"),
         (r"Santos Brasil", "Santos Brasil"), (r"\bDP World\b", "DP World"), (r"\bRumo\b", "Rumo"), (r"\bVLI\b", "VLI"), (r"\bMRS\b", "MRS Logística"),
         (r"Suape", "Suape"), (r"Portos? RS|Portos do Rio Grande", "Portos RS"), (r"\bEPR\d*\b", "Grupo EPR"), (r"Arteris|Autopista", "Grupo Arteris")]
INTERNO = re.compile(r"^(ANTT|ANTAQ|Superintend|Ger[eê]ncia|Diretoria|Ag[eê]ncia|Minist|MPor|MInfra|Uni[aã]o|n[aã]o|Procuradoria|Ouvidoria|interessad|Sindicato|Sind[a-z]+\b|Associa|Federa|Confedera|Autoridade Portu|Companhia Docas|Docas|Portos? (RS|Rio|do Paran)|APPA|Suape|Prefeitura|Estado|Governo|DNIT|TCU|Concess[oõ]es S\.?A)", re.I)
PUBLICO = re.compile(r"Autoridade Portu|Docas|APPA|Portos? RS|Portos Rio|Suape|Minist|MPor|Sindicato|Sindarsul|Associa|Prefeitura|Governo|DNIT", re.I)


def empresas(txt, alias=True):
    out = []
    for parte in re.split(r";|\s/\s| e outr", txt or ""):
        parte = re.sub(r"^SU[A-Z]{2,5}\s*[—–-]\s*", "", parte.strip(" .")).strip()
        if len(parte) < 3 or INTERNO.search(parte) or re.match(r"[\d(a-z]", parte) or re.search(r"advogad|procurador|\bSr\.?|\bSra\.?", parte, re.I): continue
        if not alias: out.append(parte[:80]); continue
        nome = next((can for rx, can in ALIAS if re.search(rx, parte, re.I)), None) or re.split(r"\(|,| - | — ", parte)[0].strip()[:60]
        if PUBLICO.search(nome) or re.search(r"\barea\b|área|\)$|bloqueant", nome, re.I): continue
        if re.search(r"\d{4}\)?$|^[A-Z]{1,3}\)$", nome): continue
        nome = re.sub(r"[.\s]+$", "", nome)
        if len(nome) >= 3 and not re.fullmatch(r"[A-Z]{2,7}", nome) and nome.lower() not in [o.lower() for o in out]: out.append(nome)
    return out


def prospeccao(ag, n=14):
    c = previsao.conn(ag); P = collections.defaultdict(lambda: {"n": 0, "temas": collections.Counter(), "pend": 0, "ult": ""})
    for r in c.execute("select i.id, i.interessado, i.assunto, r.data from itens i join reunioes r on r.id=i.reuniao_id where r.data>=? and i.interessado is not null and i.interessado<>''", (ANO,)):
        t = c.execute("select tema from item_temas where item_id=? limit 1", (r["id"],)).fetchone(); pend = desfecho_item(c, r["id"]) == "pendente"
        for nome in empresas(r["interessado"]):
            nome = next((k for k in P if k.lower() == nome.lower()), nome); p = P[nome]; p["n"] += 1; p["ult"] = max(p["ult"], r["data"])
            p["temas"][(t[0] if t else "outros").replace("_", " ")] += 1; p["pend"] += pend
    top = sorted(P.items(), key=lambda x: -x[1]["n"])[:n]
    return d.tabela(["Empresa ou grupo privado (citado como interessado)", "Itens (12 meses)", "Temas principais", "Pendentes", "Última pauta"],
                    [[f"<b>{E(k)}</b>", v["n"], E(", ".join(t for t, _ in v["temas"].most_common(2))), v["pend"], fmtd(v["ult"])] for k, v in top], ["34%", "12%", "32%", "10%", "12%"])


def diretoria(ag):
    D = "data" if ag == "antt" else f"data/{ag}"; ms = json.load(open(f"{D}/mandatos.json"))
    board, _ = previsao.colegiado_atual(previsao.conn(ag)); L = []
    for nome in board:
        tit = [m for m in ms if m["diretor"] == nome and m.get("situacao") == "titular" and (m.get("fim_legal") or m.get("fim") or "9") >= HOJE.isoformat()]
        m = tit[0] if tit else None
        L.append((m.get("fim_legal") or m.get("fim") or "9") if m else "9", [E(nome), E(m.get("cargo", "Diretor")) if m else "substituto em exercício", "titular" if m else "substituto", fmtd(m.get("fim_legal") or m.get("fim")) if m else "—"]) if False else L.append(((m.get("fim_legal") or m.get("fim") or "9") if m else "9", [E(nome), E(m.get("cargo", "Diretor")) if m else "substituto em exercício", "titular" if m else "substituto", fmtd(m.get("fim_legal") or m.get("fim")) if m else "—"]))
    return [r for _, r in sorted(L, key=lambda x: x[0])]


def mandatos(ag):
    D = "data" if ag == "antt" else f"data/{ag}"; ms = json.load(open(f"{D}/mandatos.json"))
    vig = [m for m in ms if m.get("situacao") == "titular" and (m.get("fim_legal") or m.get("fim") or "9") >= HOJE.isoformat()]
    return [[E(m["diretor"]), E(m.get("cargo", "")), fmtd(m.get("fim_legal") or m.get("fim"))] for m in sorted(vig, key=lambda m: m.get("fim_legal") or m.get("fim") or "9")[:5]]


M = {ag: mapa_tema.mapear(ag, TEMAS[ag][1], DESDE) for ag in TEMAS}
tot = sum(len(M[a]["itens"]) for a in M); dec = sum(M[a]["decididos"] for a in M); dvg = sum(M[a]["divergentes"] for a in M)
S.append(d.capa(KIT["capa"], "50% 55%", "Inteligência regulatória aplicada", NOMEESC, "Agenda, votos da diretoria e oportunidades na ANTT e na ANTAQ",
                f"Preparado para reunião institucional. Só fontes públicas: reuniões gravadas das diretorias, pautas e Diário Oficial. Base até {fmtd(max(M[a]['base_ate'] for a in M))}.",
                [(f"{tot} itens", f"nos temas do escritório desde 2023 ({dec} já decididos)"), (f"{100 * (dec - dvg) / max(dec, 1):.0f}%", f"das {dec} decididas sem voto divergente"), ("2", "agências: ANTT e ANTAQ"), (sum(previsao.conn(a).execute("select count(*) from reunioes").fetchone()[0] for a in M), "reuniões de diretoria analisadas")]))

# 1. Agendas
ant = previsao.conn("antt"); ult = list(ant.execute("select numero, data from reunioes order by data desc limit 4"))
gaps = [(datetime.date.fromisoformat(a["data"]) - datetime.date.fromisoformat(b["data"])).days for a, b in zip(ult, ult[1:])]
prox = datetime.date.fromisoformat(ult[0]["data"]) + datetime.timedelta(days=int(statistics.median(gaps)))
while prox < HOJE: prox += datetime.timedelta(days=int(statistics.median(gaps)))
DUR = prazos.duracoes("antt"); _, AP = prazos.aparicoes("antt"); temas_ids = {i["id"] for i in M["antt"]["itens"]}
pend = []
for k, v in DUR.items():
    if v[3]: continue
    ult_i = AP[k][-1]
    if any(x["id"] in temas_ids for x in AP[k]) and ult_i["data"] >= "2024-01-01": pend.append(dict(ult_i, assunto=ult_i["assunto"], resultado=ult_i["resultado"], processo_k=k))
_w = lambda t: set(w for w in re.findall(r"\w{4,}", (t or "").lower()))
def _decidido_depois(i):
    for j in M["antt"]["itens"]:
        if j["data"] > i["data"] and desfecho_item(ant, j["id"]) != "pendente":
            a, b = _w(i["assunto"]), _w(j["assunto"])
            if a and len(a & b) / len(a | b) >= 0.4: return True
    return False
pend = [i for i in sorted(pend, key=lambda x: x["data"]) if not _decidido_depois(i)][-4:]
cal_aq = [x for x in json.load(open("data/antaq/calendario.json")) if x["data"] >= HOJE.isoformat()][:2]
corpo = (d.grade(d.conceito("", "ANTAQ: calendário oficial", "", texto=d.agenda_cards(cal_aq, 2) + '<p style="font-size:8.5pt">Pauta da próxima reunião ainda não publicada; ela sai cerca de uma semana antes.</p>'),
                 d.conceito("", "ANTT: próxima reunião (estimativa)", "", texto=f'<p>Última reunião na base: <b>{ult[0]["numero"]}ª, {fmtd(ult[0]["data"])}</b>. Pelo intervalo mediano das últimas reuniões ({int(statistics.median(gaps))} dias), a próxima deve cair perto de <b>{fmtd(prox)}</b>. <i>Estimativa: o calendário oficial não foi lido nesta edição.</i></p>'), cols=2)
         + "<h3>Processos do tema ainda sem decisão final na ANTT (sem deliberação posterior na base)</h3>"
         + (d.tabela(["Última sessão · processo", "Assunto", "Situação na última sessão"], [[f'{fmtd(i["data"])} · {i["numero"]}ª<br>{i["processo_k"]}', E((i["assunto"] or "")[:130]), E(i["resultado"] or "pendente")] for i in reversed(pend)], ["18%", "58%", "24%"]) if pend else "<p>Nenhum processo do tema ficou sem decisão posterior desde 2024.</p>")
         + "<h3>Diretoria em exercício (quem votou nas últimas reuniões)</h3>" + d.grade(d.conceito("", "ANTT", "", texto=d.tabela(["Diretor", "Cargo", "Situação", "Fim do mandato"], diretoria("antt"))), d.conceito("", "ANTAQ", "", texto=d.tabela(["Diretor", "Cargo", "Situação", "Fim do mandato"], diretoria("antaq"))), cols=2))
S.append(d.tecnica("01 · Próximas agendas", "O que vem pela frente nas duas diretorias", corpo, "antt", "Troca de diretor muda o relator e o placar provável dos processos. Mandatos conforme a base de mandatos; a posse de alguns diretores da ANTT ainda está sem confirmação no Diário Oficial."))

# 2. Votos em pautas parecidas
for ag in ("antt", "antaq"):
    m = M[ag]; rows = [[E(k), s["n"], s["rel"], s["ac"], s["dv"], s["vista"]] for k, s in m["por_diretor"].items()]
    D = prazos.duracoes(ag, desde=DESDE); ks = {prazos.chave(i2["processo"]) for i2 in previsao.conn(ag).execute("select processo from itens where id in (%s)" % ",".join(str(i["id"]) for i in m["itens"]) or "0")} - {None}
    st = [v[0] for k, v in D.items() if k in ks and v[2] > 1 and v[3]]
    corpo = (d.numeros([(len(m["itens"]), f"itens no tema desde 2023 ({m['decididos']} decididos)"), (f'{100 * m["divergentes"] / max(m["decididos"], 1):.0f}%', f'com voto divergente ou vencido, entre {m["decididos"]} decididas'),
                        (f'{statistics.median(st):.0f} dias' if st else "—", f"mediana da 1ª sessão (desde 2023) à decisão, só processos com mais de uma sessão (n = {len(st)}{'; indicativo' if len(st) < 10 else ''})"), (m["desfechos"].get("pendente", 0), "ainda pendentes")])
             + d.grade(d.conceito("", "Como cada diretor em exercício votou no tema", "", texto=d.tabela(["Diretor", "Votos", "Relatou", "Acompanhou", "Divergiu", "Vista"], rows)),
                       d.conceito("", "Desfechos", "", texto=d.barras([(k, v, "itens") for k, v in m["desfechos"].most_common()])), cols=2)
             + "<h3>Casos recentes, com a fala no minuto do vídeo</h3>" + casos(ag, m["itens"]))
    S.append(d.tecnica("02 · Como a diretoria tem votado", TEMAS[ag][0], corpo, ag, "Contagens a partir das reuniões gravadas; «acompanhou» inclui quem só disse que acompanha o relator. Legenda automática pode errar nomes e números."))
    sin = [i for i in previsao.itens_empresa(previsao.conn(ag), SINAIS[ag].split("|")) if i["data"] >= "2022-01-01"][-6:]
    if sin and ag == "antt":
        S.append(d.tecnica("02 · Como a diretoria tem votado", "Concessionárias ligadas à atuação pública do escritório", d.tabela(["Data", "Empresas citadas", "Tipo", "Assunto", "Resultado"],
                 [[fmtd(i["data"]), E("; ".join(empresas(i["interessado"], alias=False)) or "—"), ("ato da agência" if re.search(r"homolog|sandbox|resultado (preliminar|final)|regulament|consulta p", i["assunto"] or "", re.I) or re.match(r"\s*Superintend", i["interessado"] or "") else "processo da empresa"), E((i["assunto"] or "")[:140]), E(i["resultado"] or "")] for i in reversed(sin)], ["10%", "18%", "12%", "44%", "16%"]),
                 ag, "Sinais públicos de aderência setorial (ex.: assessoria em debêntures), não representação do escritório nesses processos. Nomes de SPEs como aparecem na pauta."))

# Previsibilidade
corpo = ""
for ag in ("antt", "antaq"):
    lin, med = retiradas.por_diretor(ag); bd, _ = previsao.colegiado_atual(previsao.conn(ag)); lin = [x for x in lin if x[0] in bd]
    corpo += d.conceito("", f"{ag.upper()}: retiradas de pauta por relator", f"média da agência {100 * med:.1f}% (retiradas ÷ itens relatados, só itens com nº de processo legível)", texto=d.tabela(["Relator (diretoria atual)", "Retiradas ÷ itens relatados", "Taxa", "× média", "Mediana até voltar", "Sem motivo declarado"],
                        [[E(a), f"{n} ÷ {t}", f"{100 * x:.1f}%" + (" (n pequeno)" if t < 30 else ""), f"{x / mm:.1f}×", f"{v} dias" if v is not None else "—", s] for a, n, t, x, mm, v, s in lin]))
S.append(d.tecnica("02 · Previsibilidade", "Quem da diretoria atual retira processos de pauta, e quanto tempo levam para voltar", d.grade(*[c for c in corpo.split("</div><div class=\"cc\"")][:1], cols=1) if False else corpo, "antt",
                   "Só fatos: quem retirou, quantas vezes e em quanto tempo voltou. «Sem motivo declarado» = nenhum motivo dito em voz alta na sessão (pode constar em documento)."))

# 3. Prospecção
for ag in ("antt", "antaq"):
    S.append(d.tecnica("03 · Prospecção", f"Empresas com processo na {ag.upper()} nos últimos 12 meses", prospeccao(ag), ag,
                       "Interessados citados nas pautas públicas, sem autoridades portuárias, órgãos públicos, sindicatos e associações. Lista de oportunidade setorial; não indica relação com o escritório."))

# Como acompanhar
S.append(d.tecnica("04 · Como acompanhar", "O que uma rotina contínua entrega ao escritório", d.whitepaper("Entregas", [
    ("Alerta de pauta", "Quando um processo de interesse entra na pauta: relator, como ele votou em casos parecidos e casos semelhantes com link no minuto."),
    ("Alerta de retirada e de atraso", "Processo retirado ou parado além do prazo normal do tipo: aviso no mesmo dia, só com fatos."),
    ("Mapa da diretoria", "Mandatos, vagas, substitutos e quem relata cada tema, atualizado todo mês."),
    ("Monitoramento de 2 a 3 processos", "Linha do tempo, prazo esperado, precedentes e próximos passos, em documento mensal."),
    ("Briefing mensal", "O que mudou nas duas agências e o que vem na pauta, para a equipe e para os clientes do escritório.")]), "antt",
    "Informação pública e análise; sem acesso privilegiado nem antecipação de decisões sigilosas. Previsões são estimativas."))
S.append(d.fim("Base: reuniões gravadas das diretorias da ANTT e da ANTAQ, pautas, calendários e Diário Oficial. Conferência cega por amostra: voto por diretor ≈ 94–95% (mede consistência, não verdade absoluta). Legenda automática pode errar nomes e números.",
               "IRIS · Instituto de Regulação, Inovação e Sustentabilidade · inteligência por Grupo Nery", KIT["capa"]))
pdf = d.documento(S, f"{NOMEESC} · inteligência regulatória", f"{OUT}/relatorio_escritorio")
if MARCA == "iris":  # troca a marca Circle por IRIS (texto) mantendo Grupo Nery menor
    h = open(f"{OUT}/relatorio_escritorio.html").read()
    for k in ("circle_b", "circle_p"):
        h = h.replace(f'<img src="{d.img(k)}" class="lgc">', '<b style="font:800 22pt Inter,sans-serif;color:#fff;letter-spacing:.06em">IRIS</b>')
        h = h.replace(f'<img src="{d.img(k)}" class="hcp">', '<b style="font:800 12pt Inter,sans-serif;color:#003B4C;letter-spacing:.06em;margin-right:8px">IRIS</b>')
        h = h.replace(f'<img src="{d.img(k)}" class="pc">', '<b style="font:800 10pt Inter,sans-serif;color:#003B4C">IRIS</b>')
    open(f"{OUT}/relatorio_escritorio.html", "w").write(h)
    import subprocess
    js = f"const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://{os.path.abspath(OUT)}/relatorio_escritorio.html',{{waitUntil:'networkidle'}});await p.pdf({{path:'{os.path.abspath(OUT)}/relatorio_escritorio.pdf',width:'13.333in',height:'7.5in',printBackground:true}});await b.close();}})();"
    subprocess.run(["node", "-e", js], cwd="/tmp", check=True)
print(pdf, len(S), "páginas")
