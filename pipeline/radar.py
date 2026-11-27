"""Radar de Previsibilidade Regulatória — monitoramento contínuo de um cliente (1–2 páginas + resumo para e-mail).
Quatro sinais + agenda, só FATOS com fonte (skill previsibilidade-regulatoria):
  0. Agenda: próximas reuniões e itens de pauta que tocam os temas/empresas do cliente.
  1. Retiradas de pauta e vistas nos últimos 30 dias (temas/empresas do cliente) + taxa do relator.
  2. Sucessão de diretoria: mandatos que vencem em 180 dias e vagas abertas.
  3. Prazo real × esperado dos processos do cliente (ou dos itens do tema sem decisão).
  4. Consultas públicas abertas no setor (data/<ag>/consultas.json, coletado no Mac).
Config pública (sem dado sigiloso): data/radar/<slug>.json = {nome, marca, agencias, temas:{ag: regex}, empresas:{ag: regex}, processos:{ag:[nº]}, emails}
Uso: python3 pipeline/radar.py <slug> [--novidades]   (--novidades: imprime só se houver alerta; código de saída 3 = sem novidade)"""
import sys, os, re, json, datetime, statistics
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import previsao, mapa_tema, prazos, retiradas, design as d
from desfecho import desfecho_item
E = d.E; HOJE = datetime.date.today(); H = HOJE.isoformat()
CFG = json.load(open(f"data/radar/{sys.argv[1]}.json")); d.MARCA = CFG.get("marca", "nery")
fmtd = lambda s: datetime.date.fromisoformat(str(s)[:10]).strftime("%d/%m/%Y") if s and len(str(s)) >= 10 else (s or "—")
ld = lambda p, x: json.load(open(p)) if os.path.exists(p) else x
Dd = lambda ag: "data" if ag == "antt" else f"data/{ag}"
ALERTAS, BLOCOS, MD = [], [], [f"# Radar de Previsibilidade · {CFG['nome']} · {fmtd(H)}", ""]
desde30 = (HOJE - datetime.timedelta(days=30)).isoformat(); ate180 = (HOJE + datetime.timedelta(days=180)).isoformat()

for ag in CFG["agencias"]:
    c = previsao.conn(ag); rx = re.compile(CFG["temas"].get(ag, "$^") + ("|" + CFG["empresas"][ag] if CFG.get("empresas", {}).get(ag) else ""), re.I)
    toca = lambda t: bool(rx.search(t or ""))
    # 0. agenda
    cal = [x for x in ld(f"{Dd(ag)}/calendario.json", []) if x["data"] >= H][:2]
    pautas = []
    for x in cal:
        p = ld(f"{Dd(ag)}/pautas/{x['reuniao']}.json", {})
        for it in p.get("itens", []):
            if toca(" ".join(str(it.get(k, "")) for k in ("assunto", "interessado", "processo"))): pautas.append((x, it))
    ag_html = d.agenda_cards(cal, 2) if cal else "<p>Calendário oficial ainda não coletado para esta agência.</p>"
    if pautas:
        ALERTAS.append(f"{ag.upper()}: {len(pautas)} item(ns) do seu tema na pauta de {fmtd(pautas[0][0]['data'])}")
        ag_html += d.tabela(["Reunião", "Processo", "Interessado", "Assunto", "Relator"], [[f"{x['reuniao']}ª · {fmtd(x['data'])}", E(it.get("processo", "")), E(it.get("interessado", "")), E(it.get("assunto", "")[:120]), E(it.get("relator", ""))] for x, it in pautas])
    elif cal:
        ag_html += "<p>Pauta publicada sem item do seu tema, ou pauta ainda não publicada.</p>"
    # 1. retiradas e vistas recentes
    rec = [r for r in c.execute("select i.id, i.assunto, i.interessado, i.resultado, i.relator, i.ts, r.data, r.numero, r.video_id from itens i join reunioes r on r.id=i.reuniao_id where r.data>=?", (desde30,))
           if toca(f"{r['assunto']} {r['interessado']}") and re.match(r"\s*(retirad|pedido de vista|vista|sobrestad|adiad)", r["resultado"] or "", re.I)]
    lin, med = retiradas.por_diretor(ag); taxa = {a: (n, t, x) for a, n, t, x, m, v, s in lin}
    if rec: ALERTAS.append(f"{ag.upper()}: {len(rec)} retirada(s)/vista(s) no seu tema nos últimos 30 dias")
    ret_html = d.tabela(["Sessão", "Assunto", "O que aconteceu", "Relator (retiradas ÷ itens relatados)"], [[f"{fmtd(r['data'])} · {r['numero']}ª", E((r['assunto'] or '')[:120]),
                         f"{E((r['resultado'] or '')[:90])} <a href='{mapa_tema.link(r['video_id'], r['ts'])}'>▶ minuto</a>", E(r["relator"] or "—") + (f" ({taxa[r['relator']][0]} ÷ {taxa[r['relator']][1]})" if r["relator"] in taxa else "")] for r in rec]) if rec else "<p>Nenhuma retirada ou vista no seu tema nos últimos 30 dias.</p>"
    # 2. sucessão
    ms = [m for m in ld(f"{Dd(ag)}/mandatos.json", []) if m.get("situacao") == "titular" and H <= (m.get("fim_legal") or m.get("fim") or "0") <= ate180]
    vag = [v for v in ld(f"{Dd(ag)}/vacancias.json", []) if not v.get("fim")]
    if ms or vag: ALERTAS.append(f"{ag.upper()}: " + ", ".join([f"mandato de {m['diretor']} vence em {fmtd(m.get('fim_legal') or m.get('fim'))}" for m in ms] + [f"cadeira vaga desde {fmtd(v.get('inicio'))} ({v.get('cadeira', '').split('(')[0].strip()}), ocupada por substituto" for v in vag]))
    suc_html = ("".join(f"<p>• Mandato de <b>{E(m['diretor'])}</b> ({E(m.get('cargo', ''))}) vence em <b>{fmtd(m.get('fim_legal') or m.get('fim'))}</b>.</p>" for m in ms)
                + "".join(f"<p>• Cadeira vaga: {E(v.get('cadeira', ''))} desde {fmtd(v.get('inicio'))}.</p>" for v in vag)) or "<p>Nenhum mandato vencendo em 180 dias e nenhuma vaga aberta.</p>"
    # 3. prazo real × esperado
    DUR = prazos.duracoes(ag); procs = [prazos.chave(p) for p in CFG.get("processos", {}).get(ag, [])]
    alvo = [k for k in procs if k in DUR] if procs else []
    if not procs:
        _, AP = prazos.aparicoes(ag)
        alvo = [k for k, v in DUR.items() if not v[3] and any(toca(f"{x['assunto']}") for x in AP[k]) and v[0] < 3 * 365]
    pr_rows = []
    for k in alvo[:6]:
        dias, tema, n, dec = DUR[k]; e = prazos.estatistica(DUR, tema)
        if not e: continue
        acima = dias > e["p75"]
        if acima and not dec: ALERTAS.append(f"{ag.upper()}: processo {k} há {dias} dias sem decisão (75% dos parecidos decidem em até {e['p75']:.0f})")
        pr_rows.append([k, tema.replace("_", " "), f"{dias} dias" + (" (decidido)" if dec else ""), f"{e['mediana']:.0f} dias (faixa {e['p25']:.0f}–{e['p75']:.0f}; n = {e['n']})", "acima do normal" if acima else "dentro do normal"])
    pr_html = d.tabela(["Processo", "Tipo", "Tempo na diretoria", "Mediana dos parecidos", "Situação"], pr_rows) if pr_rows else "<p>Sem processo do cliente cadastrado nesta agência e sem item do tema parado.</p>"
    # 4. consultas públicas
    cp = [x for x in ld(f"{Dd(ag)}/consultas.json", []) if (x.get("fim") or "") >= H and toca(f"{x.get('titulo', '')} {x.get('tema', '')}")]
    if cp: ALERTAS.append(f"{ag.upper()}: {len(cp)} consulta(s) pública(s) aberta(s) no seu tema")
    cp_html = d.tabela(["Consulta", "Tema", "Prazo para contribuir", "Link"], [[E(x.get("numero", "")), E(x.get("titulo", "")[:120]), fmtd(x.get("fim")), f"<a href='{x.get('url', '')}'>abrir</a>"] for x in cp]) if cp else ("<p>Nenhuma consulta aberta no seu tema.</p>" if os.path.exists(f"{Dd(ag)}/consultas.json") else "<p>Consultas públicas desta agência ainda não coletadas (Mac).</p>")
    corpo = d.grade(d.conceito("", "Agenda", "", texto=ag_html), d.conceito("", "Sucessão de diretoria", "", texto=suc_html), cols=2) + "<h3>Retiradas de pauta e vistas (30 dias)</h3>" + ret_html + "<h3>Prazo real × esperado</h3>" + pr_html + "<h3>Consultas públicas abertas</h3>" + cp_html
    BLOCOS.append(d.tecnica(f"Radar · {fmtd(H)}", f"{ag.upper()}: o que mudou e o que vem", corpo, ag, "Só fatos com fonte: pautas, calendário, reuniões gravadas e Diário Oficial. Prazos: mediana dos processos parecidos que passaram por mais de uma sessão."))

MD += (["**Alertas:**"] + [f"- {a}" for a in ALERTAS]) if ALERTAS else ["Sem novidade que exija ação nesta semana."]
MD += ["", "PDF anexo. Fatos com fonte (pautas, reuniões gravadas, Diário Oficial); legenda automática pode errar nomes e números."]
if "--novidades" in sys.argv and not ALERTAS: print("sem novidades"); sys.exit(3)
out = f"clientes/{sys.argv[1]}/radar"; os.makedirs(out, exist_ok=True)
pdf = d.documento(BLOCOS, f"Radar · {CFG['nome']}", f"{out}/radar_{H}")
open(f"{out}/radar_{H}.md", "w").write("\n".join(MD) + "\n")
print("\n".join(MD)); print(pdf)
