"""Seções de consultoria do relatório (lidas de empresa.json), usadas por relatorio_empresa.py:
- temas_consultoria: [{"titulo", "regex", "agencia"?, "desde"?}]  → 1 página por assunto: como cada diretor vota + decisões semelhantes
- item_antecipado: {"titulo", "texto", "agencia", "regex", "calendario": [{"data","reuniao","obs"}], "evidencias": [{"t","txt","vid"}], "leitura"}
- contrato_foco: {"titulo", "texto", "regex", "agencia"}  → linha do tempo das decisões que citam o contrato/área
Toda previsão é inferência a partir do histórico (mapa_tema.py: prior 97%, peso 10)."""
import html, datetime
import mapa_tema

E = html.escape


def fmtd(s):
    try: return datetime.date.fromisoformat(str(s)[:10]).strftime("%d/%m/%Y")
    except Exception: return str(s or "—")


def secoes(EMP, AG_default, NOME_AG, foto_d, LOGO_P, n0):
    S, n = [], n0

    def top(t):
        return f'<header class="top"><span class="num">{n:02d}</span><span>{E(t)}</span>' + (f'<img src="{LOGO_P}" class="logo-p">' if LOGO_P else "") + '</header>'

    for tc in EMP.get("temas_consultoria", []):
        ag = tc.get("agencia", AG_default); n += 1
        m = mapa_tema.mapear(ag, tc["regex"], tc.get("desde"))
        cs = ""
        for d, st in m["por_diretor"].items():
            e = st["ev"]
            evh = (f'<div class="ev2">RD {E(str(e["numero"]))} · {fmtd(e["data"])}: <i>{E((e["justificativa"] or e["voto"] or "")[:90])}</i> '
                   f'<a href="{mapa_tema.link(e["video_id"], e["ts"], e["trecho_t"])}">▶</a></div>') if e else ""
            cs += (f'<div class="tc">{foto_d(ag, d, {})}<div class="tc-n">{E(d)}</div><div class="tc-big">{st["p_acomp"]:.0%}</div>'
                   f'<div class="tc-l">chance de acompanhar o relator</div><div class="tc-s">{st["n"]} votos · relatou {st["rel"]} · divergiu {st["dv"]} · vista {st["vista"]}</div>{evh}</div>')
        its = m["itens"]
        lst = "".join(f'<li><b>RD {E(str(i["numero"]))} · {fmtd(i["data"])}</b> {E((i["assunto"] or "")[:105])} — <i>{E((i["resultado"] or "")[:55])}</i> '
                      f'<a href="{mapa_tema.link(i["video_id"], i["ts"])}">▶</a></li>' for i in its[-5:][::-1])
        des = " · ".join(f"{k} {v}" for k, v in m["desfechos"].most_common())
        per = f'{fmtd(its[0]["data"])} a {fmtd(its[-1]["data"])}' if its else "—"
        S.append(f'<section class="pg tema">{top("Mapeamento · " + NOME_AG[ag])}<h2>{E(tc["titulo"])}</h2>'
                 f'<p class="lead">{len(its)} decisões na base ({per}); {m["unanimes"]} sem divergência. Desfecho para o interessado: {E(des) or "—"}.</p>'
                 f'<div class="tgrid" style="grid-template-columns:repeat({max(len(m["por_diretor"]), 1)},1fr)">{cs}</div>'
                 f'<h3>Decisões semelhantes mais recentes (outras iniciativas)</h3><ul class="lst">{lst}</ul>'
                 '<div class="rod">Chance = histórico de cada diretor no tema (prior 97%, peso 10); diretor com poucos votos no tema fica perto do prior — leia o n. ▶ abre o vídeo no minuto.</div></section>')

    ia = EMP.get("item_antecipado")
    if ia:
        ag = ia.get("agencia", AG_default); n += 1
        m = mapa_tema.mapear(ag, ia["regex"]) if ia.get("regex") else {"por_diretor": {}}
        pu = 1.0
        for st in m["por_diretor"].values(): pu *= st["p_acomp"]
        prev = "".join(f'<tr><td>{E(d)}</td><td>{st["p_acomp"]:.0%}</td><td>{st["n"]}</td></tr>' for d, st in m["por_diretor"].items())
        calh = "".join(f'<li><span>{E(c["data"])}</span><b>{E(c["reuniao"])}</b>{E(c["obs"])}</li>' for c in ia.get("calendario", []))
        evh = "".join(f'<li>{E(x["txt"])} <a href="https://www.youtube.com/watch?v={x["vid"]}&t={max(int(x["t"]) - 3, 0)}s">▶ {int(x["t"]) // 3600}:{int(x["t"]) // 60 % 60:02d}:{int(x["t"]) % 60:02d}</a></li>'
                      for x in ia.get("evidencias", []))
        S.append(f'<section class="pg ante">{top("Análise antecipada · " + NOME_AG[ag])}<h2>{E(ia["titulo"])}</h2><p class="lead">{E(ia["texto"])}</p>'
                 f'<div class="duas"><div><h3>O que foi dito na sessão</h3><ul class="lst">{evh}</ul><h3>Próximas reuniões (calendário oficial)</h3><ul class="cal">{calh}</ul></div>'
                 f'<div><h3>Previsão de voto por diretor (inferência)</h3><table class="tab sm"><thead><tr><th>Diretor</th><th>Acompanha o relator</th><th>n no tema</th></tr></thead><tbody>{prev}</tbody></table>'
                 f'<div class="pu">Chance de decisão unânime nos termos do relator: <b>{pu:.0%}</b></div><p class="nota">{E(ia.get("leitura", ""))}</p></div></div>'
                 '<div class="rod">Fontes públicas: vídeo oficial da reunião e calendário aprovado pela diretoria. Previsão é estimativa a partir do histórico; não substitui o voto nem a publicação oficial.</div></section>')

    cf = EMP.get("contrato_foco")
    if cf:
        ag = cf.get("agencia", AG_default); n += 1
        m = mapa_tema.mapear(ag, cf["regex"])
        tl = "".join(f'<li><span>{fmtd(i["data"])}</span><b>RD {E(str(i["numero"]))} · item {E(str(i["item"]))}</b>{E((i["assunto"] or "")[:150])} — <i>{E((i["resultado"] or "")[:70])}</i> '
                     f'<a href="{mapa_tema.link(i["video_id"], i["ts"])}">▶</a></li>' for i in m["itens"][-8:])
        S.append(f'<section class="pg cfoc">{top("Mapeamento de contrato · " + NOME_AG[ag])}<h2>{E(cf["titulo"])}</h2><p class="lead">{E(cf.get("texto", ""))}</p>'
                 f'<ul class="cal tl">{tl or "<li>Sem decisões na base.</li>"}</ul>'
                 '<div class="rod">Linha do tempo das decisões de diretoria que citam o contrato/área (busca na base; nº do contrato vem da legenda — conferir).</div></section>')
    return S, n


CSS = """.parc{display:flex;align-items:center;gap:10px;margin:-.12in 0 .18in;font-size:8pt;color:#BDB8AE;letter-spacing:.08em;text-transform:uppercase}.parc img{height:.26in}
.cli{position:absolute;right:.45in;top:.45in;background:#fff;border-radius:10px;padding:8px 12px}.cli img{height:.5in;display:block}
.tema,.ante,.cfoc{padding:.38in .5in;display:block!important}.fim .logo{width:auto!important;height:.4in;align-self:flex-start}.fim .parc{align-self:flex-start}.parc img{width:auto!important}.tema .duas,.ante .duas{display:grid;grid-template-columns:1.1fr 1fr;gap:.3in}.ante .pu{margin:.1in 0;font-size:10pt}.tema .lead,.ante .lead,.cfoc .lead{font-size:10.5pt;line-height:1.45;margin:0 0 .14in;color:#2B2925}
.tgrid{display:grid;gap:.12in}.tc{background:#fff;border:1px solid #E3DFD6;border-top:4px solid var(--ac);border-radius:10px;padding:.12in;text-align:center;display:flex;flex-direction:column;align-items:center;min-width:0}
.tc .ftd{width:.8in;height:.8in}.tc-n{font-family:Rubik;font-weight:600;font-size:10pt;margin:.06in 0 0}.tc-big{font-family:Rubik;font-size:26pt;line-height:1.1}.tc-l{font-size:7.5pt;color:#6E6A63}.tc-s{font-size:7.8pt;margin:.05in 0}
.ev2{font-size:7.2pt;color:#5E5A52;text-align:left;border-top:1px solid #E3DFD6;padding-top:.04in;margin-top:auto}.lst{margin:0;padding-left:1.1em;font-size:8.6pt;line-height:1.45}.lst a,.ev2 a,.tl a{color:#B08600;font-weight:700;text-decoration:none}
.tema h3,.ante h3{font-size:11.5pt;margin:.16in 0 .06in}.tl li{margin-bottom:.06in}"""
