"""Boletim mensal DO CLIENTE (peça 2 do pacote), todo no padrão Grupo Nery (pipeline/design.py):
capa · sumário · 01 Na próxima reunião (alerta pré-pauta) · 02 Suas perguntas (uma página por resposta) · 03 O mês na agência · fim.
Dados: alerta_pauta.py e boletim.py são executados para obter os dados (os PDFs avulsos deles continuam saindo);
respostas em <pasta>/perguntas/respostas/NN.md e perguntas em <pasta>/perguntas/perguntas.md.
Uso: python3 pipeline/boletim_cliente.py clientes/<x>/<pasta> AAAA-MM   → <pasta>/boletim_cliente_<AAAA-MM>.pdf"""
import sys, os, re, json, glob, datetime, runpy, subprocess, collections, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import design as d, mapa_tema

if len(sys.argv) < 3 or not re.match(r"^\d{4}-\d{2}$", sys.argv[2]): sys.exit("Uso: python3 pipeline/boletim_cliente.py clientes/<x>/<pasta> 2026-11   (mês no formato AAAA-MM; gere no chat; a pasta clientes/ não vai para o Mac)")
P, MES = sys.argv[1].rstrip("/"), sys.argv[2]
if not os.path.exists(f"{P}/empresa.json"): sys.exit(f"Pasta do cliente não encontrada: {P}. Os relatórios de cliente são gerados no chat (clientes/ fica fora do git); no Mac rode só a coleta: caffeinate -i bash pipeline/coletar_todas.sh")
EMP = json.load(open(f"{P}/empresa.json")); AG = EMP.get("agencias", ["antaq"])[0]; NOME = d.NOME_AG.get(AG, AG.upper()); E = html.escape
MESES = "janeiro fevereiro março abril maio junho julho agosto setembro outubro novembro dezembro".split()
ano, mm = map(int, MES.split("-"))
ag_mes = (datetime.date(ano, mm, 1) - datetime.timedelta(days=1)).strftime("%Y-%m")  # o mês fechado anterior
NM = MESES[int(ag_mes[5:]) - 1]
KIT = d.kit(EMP.get("setor") or d.SETOR_AG.get(AG, "portos")); FT = EMP.get("foto_capa") or KIT["capa"]; FOCO = EMP.get("foco", "50% 55%"); CLI = EMP.get("logo")
DIV = KIT["divisores"] + [FT] * 3
fmtd = lambda s: datetime.date.fromisoformat(str(s)[:10]).strftime("%d/%m/%Y") if s and re.match(r"\d{4}-\d\d-\d\d", str(s)) else str(s or "")
nome_curto = EMP["nome"].split("(")[0].strip()


def rodar(script, args):
    """executa um script do pipeline e devolve as variáveis globais dele (os dados), sem duplicar a lógica."""
    old = sys.argv; sys.argv = [script] + args
    try: return runpy.run_path(script, run_name="__boletim__")
    finally: sys.argv = old


ROT = {"favorável": "a favor", "parcial": "em parte", "neutro": "sem efeito direto", "desfavorável": "contra", "pendente": "sem decisão"}
# ---------- dados ----------
AL = rodar("pipeline/alerta_pauta.py", [P])
BO = rodar("pipeline/boletim.py", [AG, ag_mes])
c = BO["c"]; yt = BO["yt"]


def md_html(t):
    """markdown simples das respostas → html (negrito, links, listas)."""
    t = E(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2">\1</a>', t)
    t = re.sub(r"\s+—\s+", ", ", t)
    out, ul = [], False
    for ln in t.split("\n"):
        if ln.strip().startswith("- "):
            if not ul: out.append('<ul class="arr sm">'); ul = True
            out.append(f"<li>{ln.strip()[2:]}</li>")
        else:
            if ul: out.append("</ul>"); ul = False
            if ln.strip(): out.append(f"<p>{ln}</p>")
    if ul: out.append("</ul>")
    return "".join(out)


def secoes(md):
    """divide a resposta em seções «**N. Título:** texto»."""
    partes = re.split(r"\n?\*\*(\d+)\.\s*([^*:]+):?\*\*:?", md)
    if len(partes) < 4: return [("Resposta", md)]
    return [(partes[k + 1].strip(), partes[k + 2].strip()) for k in range(1, len(partes) - 2, 3)]


def falas_itens(lista, n=4):
    rows, vistos = [], set()
    for i in lista:
        for v in c.execute("select * from votos where item_id=? and trecho is not null and trecho!='' order by eh_relator desc, id limit 3", (i["id"],)):
            if v["trecho"][:60] in vistos: continue
            vistos.add(v["trecho"][:60])
            rows.append([f'{fmtd(i["data"])}<br><span class="nw">{i["numero"]}ª, item {E(str(i["item"]))}</span>', f'<b>{E(v["diretor"])}</b>{" (relator)" if v["eh_relator"] else ""}<br><span style="color:#6B7780">{E((v["justificativa"] or v["voto"] or "")[:110])}</span>',
                         f'<i>«{E(v["trecho"][:230])}»</i> <a href="{yt(i["video_id"], v["ts"] or i["ts"])}">▶ minuto</a>'])
            if len(rows) >= n: return rows
    return rows


tabf = lambda rows: d.tabela(["Sessão", "Quem e o voto", "O que foi dito (trecho literal da legenda)"], rows, ["12%", "30%", "58%"]) if rows else ""

S = []
perg = [l[2:].split("[")[0].strip() for l in open(f"{P}/perguntas/perguntas.md") if l.startswith("- ")] if os.path.exists(f"{P}/perguntas/perguntas.md") else []
resp = sorted(glob.glob(f"{P}/perguntas/respostas/*.md"))
SEC = [("Na próxima reunião", "alerta pré-pauta: itens, relator e estimativa"), (f"Suas perguntas ({len(resp)})", "resposta com evidência e link no minuto"),
       (f"O mês na {NOME}", f"{NM}: números, decisões, divergências e diretoria")]
S.append(d.capa(FT, FOCO, f"Boletim mensal · {NOME}", nome_curto, f"{MESES[mm - 1]} de {ano}",
                "O que vem na diretoria, o que ela decidiu e as respostas às suas perguntas. Fontes públicas; previsões são estimativas.",
                [(len(AL["itens"][:8]), "itens a acompanhar na próxima reunião"), (len(resp), "perguntas respondidas"), (len(BO["IT"]), f"itens decididos pela diretoria em {NM}"), (BO["n_div"], "itens com divergência no mês")], CLI))
S.append(d.sumario(SEC, DIV[0]))

# ---------- 01 alerta ----------
alvo = AL["alvo"]
S.append(d.divisor(1, SEC[0][0], f"{alvo.get('reuniao')}ª reunião da diretoria{', ' + fmtd(alvo['data']) if alvo.get('data') else ''}: o que interessa à {nome_curto}, quem relata e o que o histórico permite estimar.", DIV[0]))
linhas = []
for x in AL["itens"][:6]:
    origem, txt, rel, rx = x[:4]; lk = x[4] if len(x) > 4 else None
    corpo = f"<p>{E(re.sub(r'\s+—\s+', '. ', txt))}{'. Relator: ' + E(rel) if rel else ''}{f' <a href={chr(34)}{lk}{chr(34)}>▶ minuto</a>' if lk else ''}</p>"
    if rx:
        m = mapa_tema.mapear(AG, rx, "2023-01-01"); pu = 1.0
        for st in m["por_diretor"].values(): pu *= st["p_acomp"]
        corpo += (f'<p style="color:#6B7780">{d.selo("estimativa")} unânime com o relator: <b>{pu:.0%}</b> (tema desde 2023, {len(m["itens"])} decisões). '
                  + ", ".join(f'{E(dn.split()[0])} {st["p_acomp"]:.0%} (n={st["n"]}{", amostra pequena" if st["n"] < 5 else ""})' for dn, st in m["por_diretor"].items()) + "</p>")
    titulo = re.sub(r"^(\d+ª) · item (\S+?):.*", r"Item \2 da \1", txt) if "item" in txt[:20] else txt.split(":")[0][:60]
    linhas.append((f"{titulo} · {origem}", corpo))
pauta = "Pauta publicada." if alvo.get("itens") else "A pauta ainda não foi publicada: os itens vêm da última reunião e dos temas da empresa."
S.append(d.tecnica("01 · Na próxima reunião", f"O que acompanhar na {alvo.get('reuniao')}ª reunião", d.whitepaper("Alerta", linhas, intro=f"<p>{E(pauta)} O relator define o resultado na grande maioria dos casos; a estimativa abaixo vem do histórico de votos de cada diretor no tema do item.</p>"), AG,
                   "Estimativas a partir do histórico de votos (prior 97%, peso 10); não são certeza.", CLI))
sim = AL.get("sim") or []
if sim:
    rows = [[f'{fmtd(s["data"])}<br><span class="nw">{s["numero"]}ª, item {E(str(s["item"]))}</span>', E((s["assunto"] or "")[:150]), E(s["relator"] or ""), E(ROT.get(s["desfecho"], s["desfecho"])), f'<i>{E((s.get("justificativa") or "")[:150])}</i> <a href="{s["link"]}">▶ minuto</a>'] for s in sim]
    S.append(d.tecnica("01 · Na próxima reunião", "Como a diretoria decidiu casos parecidos", d.tabela(["Sessão", "Assunto", "Relator", "Desfecho", "Justificativa do relator"], rows, ["11%", "34%", "11%", "9%", "35%"])
                       + d.conceito("", "O que foi dito nesses casos", "trechos literais com o minuto", texto=tabf(falas_itens(BO["c"].execute(f"select i.*, r.numero, r.data, r.video_id from itens i join reunioes r on r.id=i.reuniao_id where i.id in ({','.join(str(s['id']) for s in sim)}) order by r.data desc").fetchall(), 3))), AG, logo_cliente=CLI))

# ---------- 02 perguntas ----------
S.append(d.divisor(2, SEC[1][0], "Cada pergunta do mês respondida com números, decisões, trecho literal e o link do vídeo no minuto.", DIV[1] if len(DIV) > 1 else FT))
for k, f in enumerate(resp):
    md = open(f).read(); q = perg[k] if k < len(perg) else f"Pergunta {k + 1}"
    md = re.split(r"\n\**Cobertura (desta|da) resposta", md)[0]
    sx = [(t, x) for t, x in secoes(md) if not re.match(r"cobertura", t, re.I)]
    tam = sum(len(x) for _, x in sx)
    grupos = [sx] if tam < 2600 else [sx[:2], sx[2:]] if len(sx) > 2 else [sx]
    for g, sub in enumerate(grupos):
        S.append(d.tecnica("02 · Suas perguntas", q + (" (continuação)" if g else ""), d.whitepaper(f"Pergunta {k + 1}", [(t, md_html(x)) for t, x in sub]), AG, logo_cliente=CLI))

# ---------- 03 o mês ----------
IT, VT, delib = BO["IT"], BO["VT"], BO["delib"]
S.append(d.divisor(3, SEC[2][0], f"Tudo o que a diretoria da {NOME} decidiu em {NM}: números, decisões por tema, quem divergiu e por quê, e a diretoria.", DIV[2] if len(DIV) > 2 else FT))
nums = d.numeros([(len(BO["R"]), "reuniões de diretoria"), (len(IT), "itens em pauta"), (len(delib) - BO["n_div"], "decididos sem divergência"), (BO["n_vista"] + BO["n_ret"], "vistas e retiradas")])
temas = BO["temas"]; rel = BO["rel"]
dest = []
usados = set()
for t, _ in temas.most_common(4):
    i = next((i for i in delib if i["id"] not in usados and c.execute("select 1 from item_temas where item_id=? and tema=?", (i["id"], t)).fetchone()), None)
    if i:
        usados.add(i["id"])
        dest.append((t.replace("_", " ").capitalize(), f'<p><b>{i["numero"]}ª, item {E(str(i["item"]))}, {fmtd(i["data"])}:</b> {E(i["assunto"] or "")}. {E(i["resultado"] or "")}{". Relator: " + E(i["relator"]) if i["relator"] else ""}. <a href="{yt(i["video_id"], i["ts"])}">▶ minuto</a></p><p style="color:#6B7780">{E((i["resumo"] or "")[:260])}</p>'))
S.append(d.tecnica(f"03 · O mês na {NOME}", f"{NM.capitalize()} em números", nums + d.grade(d.conceito("", "Temas mais frequentes", "itens por tema", texto=d.barras([(t.replace("_", " "), n, "itens") for t, n in temas.most_common(7)])),
                                                                                                         d.conceito("", "Quem relatou", "itens relatados no mês", texto=d.barras([(n, v, "relatorias") for n, v in rel.most_common(6)])), cols=2)
                   + d.conceito("", "Empresas e entes em pauta", "pelo índice de entidades e pelo campo «interessado» (nomes vêm da legenda)", texto=d.barras([(e, v, "itens") for e, v in BO["ent"].most_common(3)]))
                   , AG, logo_cliente=CLI))
if dest:
    S.append(d.tecnica(f"03 · O mês na {NOME}", "Outras decisões de destaque", d.whitepaper("Decisões", dest[:3])
                       + d.conceito("", "O que foi dito nessas decisões", "trechos literais com o minuto", texto=tabf(falas_itens([i for i in delib if i["id"] in usados], 2))), AG, logo_cliente=CLI))
dv = [v for v in VT if v["categoria"] in ("vencido", "revisor_diverge", "vista")]
cat = lambda v: "renovou vista" if v["categoria"] == "revisor_diverge" and re.search("vista", v["resultado"] or "", re.I) else {"vencido": "vencido", "revisor_diverge": "divergiu", "vista": "pediu vista"}[v["categoria"]]
rows = [[f'{v["numero"]}ª<br>{fmtd(v["data"])[:5]}', E(v["diretor"]), E(cat(v)), E((v["assunto"] or "")[:110]), f'{E((v["justificativa"] or v["voto"] or "")[:150])}{" <i>«" + E(v["trecho"][:140]) + "»</i>" if v["trecho"] else ""} <a href="{yt(v["video_id"], v["ts"])}">▶ minuto</a>'] for v in dv[:8]]
S.append(d.tecnica(f"03 · O mês na {NOME}", "Quem divergiu ou pediu vista, e por quê", (d.tabela(["Reunião", "Diretor", "O quê", "Assunto", "Justificativa e fala"], rows, ["7%", "12%", "9%", "30%", "42%"]) if rows else "<p>Nenhuma divergência ou vista no mês: todos os itens deliberados seguiram o relator.</p>")
                   + d.conceito("", "O que foi dito nos itens com vista, retirada ou divergência", "trechos literais com o minuto", texto=tabf(falas_itens([i for i in IT if re.search("vista|retirad", (i["resultado"] or "").lower()) or i["id"] in {v["item_id"] for v in dv}], 6 - min(len(rows), 4)))), AG,
                   f"{len(dv)} registro(s) no mês{' (mostrando 8)' if len(dv) > 8 else ''}. Justificativa resumida a partir da fala; o tom não é inferido.", CLI))
vac, venc = BO["vac"], BO["venc"]
volta = [i for i in IT if re.search("vista|retirad", (i["resultado"] or "").lower())]
dire = [("Votaram no mês", "<p>" + E(", ".join(BO["board"])) + "</p>"),
        ("Vagas abertas", "".join(f"<p>{E(v['cadeira'])}: vaga desde {fmtd(v['inicio'])}; interinos: {E(v.get('interinos') or 'não informados')}.</p>" for v in vac) or "<p>Nenhuma vaga aberta.</p>"),
        ("Mandatos que vencem em até 120 dias", "".join(f"<p>{E(m['diretor'])}: mandato até {fmtd(m.get('fim_legal') or m.get('fim'))}.</p>" for m in venc) or "<p>Nenhum.</p>"),
        ("Itens que devem voltar à pauta", "".join(f'<p>{E(i["numero"])}ª: {E((i["assunto"] or "")[:120])} ({E((i["resultado"] or "")[:60])}) <a href="{yt(i["video_id"], i["ts"])}">▶</a></p>' for i in volta[:5]) or "<p>Nenhum item com vista ou retirado.</p>")]
cob = subprocess.run(["python3", "pipeline/cobertura_resposta.py", AG, "-", "-", str(ano)], capture_output=True, text=True).stdout
mcob = re.search(r"reuniões de diretoria: (\d+) no canal · (\d+) com texto · (\d+) analisadas", cob)
rod = (f"Cobertura {ano}: {mcob.group(1)} reuniões de diretoria no canal, {mcob.group(3)} analisadas. " if mcob else "") + "Legenda automática pode errar nomes e valores; itens sigilosos e votos escritos (SEI) não estão nos vídeos."
S.append(d.tecnica(f"03 · O mês na {NOME}", "Diretoria e o que esperar no próximo mês", d.whitepaper("Diretoria", dire), AG, rod, CLI))
S.append(d.fim("Fontes públicas: vídeos oficiais das reuniões, pautas e calendário da agência, Senado e DOU. Previsões e alertas são estimativas; não substituem a publicação oficial nem orientação jurídica.",
               EMP.get("contato", "Circle Consultoria em parceria com Grupo Nery"), DIV[0]))
dst = d.documento(S, f"Boletim {nome_curto} {MES}", f"{P}/boletim_cliente_{MES}")
print(dst, len(S), "páginas", os.path.getsize(dst) // 1024, "KB")
