"""Indicador de retirada de pauta (Radar de Previsibilidade Regulatória).
Só FATOS: quem retirou, motivo dito na sessão (resultado/resumo), quantas vezes, dias até voltar, desfecho quando voltou,
e taxa de retirada do relator × média da agência. Nunca hipótese de motivo nem adjetivo (ver skill previsibilidade-regulatoria).
Uso: python3 pipeline/retiradas.py <ag> [diretores | processo <nº> | empresa <texto>] [--md arquivo]"""
import sys, os, re, collections, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import previsao
from prazos import aparicoes, _d
from desfecho import desfecho_item

RET = re.compile(r"retirad|sobrestad|adiad", re.I)
MOT = re.compile(r"(a pedido|para (melhor|ouvir|aguardar|análise|analise|instru|diligên|diligen|ajust|complement)|procuradoria|área técnica|area tecnica|sustentação|sustentacao|ausência|ausencia|tempo|falta de quórum|quorum)[^.;]{0,120}", re.I)


def link(vid, ts):
    p = [int(x) for x in re.findall(r"\d+", ts or "")][-3:]
    s = (p[0] * 3600 + p[1] * 60 + p[2]) if len(p) == 3 else (p[0] * 60 + p[1]) if len(p) == 2 else None
    return f"https://www.youtube.com/watch?v={vid}" + (f"&t={max(s - 3, 0)}s" if s is not None else "")


def motivo(r):
    t = " ".join(x for x in (r["resultado"], r["resumo"]) if x)
    m = MOT.search(t)
    return m.group(0).strip() if m else "sem motivo declarado na sessão"


def eventos(ag):
    """Uma linha por retirada de item com nº de processo legível, com o que aconteceu depois."""
    c, P = aparicoes(ag)
    det = {r["id"]: r for r in c.execute("select i.id, i.ts, i.relator, i.interessado, i.resumo, i.resultado, r.video_id from itens i join reunioes r on r.id=i.reuniao_id")}
    out = []
    for proc, its in P.items():
        for k, it in enumerate(its):
            if not RET.search(it["resultado"] or ""): continue
            d = det[it["id"]]; depois = its[k + 1:]
            volta = next((x for x in depois if x["data"] > it["data"]), None)
            dec = next((x for x in depois if desfecho_item(c, x["id"]) != "pendente"), None)
            out.append(dict(processo=proc, data=it["data"], reuniao=it["numero"], relator=d["relator"] or "não identificado", interessado=d["interessado"] or "",
                            assunto=(it["assunto"] or "")[:140], motivo=motivo(d), n_retiradas=sum(1 for x in its[:k + 1] if RET.search(x["resultado"] or "")),
                            dias_ate_voltar=(_d(volta["data"]) - _d(it["data"])).days if volta else None,
                            desfecho=desfecho_item(c, dec["id"]) if dec else "ainda não decidido", link=link(d["video_id"], d["ts"])))
    return c, out


def por_diretor(ag):
    c, ev = eventos(ag)
    from prazos import chave
    tot = collections.Counter(r["relator"] for r in c.execute("select relator, processo from itens where relator is not null and relator<>''") if chave(r["processo"]))
    ret = collections.Counter(e["relator"] for e in ev)
    media = sum(v for k, v in ret.items() if k != "não identificado") / max(sum(tot.values()), 1)
    linhas = []
    for d, n in ret.most_common():
        if d == "não identificado" or tot[d] < 1: continue
        vs = [e["dias_ate_voltar"] for e in ev if e["relator"] == d and e["dias_ate_voltar"] is not None]
        sm = sum(1 for e in ev if e["relator"] == d and e["motivo"] == "sem motivo declarado na sessão")
        linhas.append((d, n, tot[d], n / tot[d], media, sorted(vs)[len(vs) // 2] if vs else None, sm))
    return linhas, media


def main():
    ag = sys.argv[1].lower(); modo = sys.argv[2] if len(sys.argv) > 2 else "diretores"; arg = sys.argv[3] if len(sys.argv) > 3 else ""
    L = []
    if modo == "diretores":
        linhas, media = por_diretor(ag)
        L += [f"# Retiradas de pauta por relator — {ag.upper()}", "", f"Média da agência: {100 * media:.1f} (retiradas ÷ itens relatados, os dois contando só itens com nº de processo legível).", "",
              "| Relator | Retiradas | Itens relatados (nº legível) | Taxa | × média | Mediana de dias até voltar | Sem motivo declarado |", "|---|---|---|---|---|---|---|"]
        L += [f"| {d} | {n} | {t} | {100 * x:.1f}% | {x / m:.1f}× | {v if v is not None else '—'} | {s} |" for d, n, t, x, m, v, s in linhas]
        L += ["", "Fatos contados a partir das reuniões gravadas; «sem motivo declarado» = nenhum motivo foi dito em voz alta na sessão (pode ter sido registrado em documento). Legenda automática pode errar nomes e números."]
    else:
        _, ev = eventos(ag)
        sel = [e for e in ev if (modo == "processo" and arg in e["processo"]) or (modo == "empresa" and re.search(arg, e["interessado"] + " " + e["assunto"], re.I))]
        L += [f"# Retiradas de pauta — {ag.upper()} · {modo} «{arg}»", "", f"{len(sel)} retiradas.", ""]
        for e in sorted(sel, key=lambda x: x["data"]):
            L.append(f"- **{e['data']}** · {e['processo']} · relator {e['relator']} · {e['n_retiradas']}ª retirada · motivo: {e['motivo']} · "
                     f"voltou após {e['dias_ate_voltar']} dias" if e['dias_ate_voltar'] is not None else f"- **{e['data']}** · {e['processo']} · relator {e['relator']} · {e['n_retiradas']}ª retirada · motivo: {e['motivo']} · ainda não voltou à pauta")
            L[-1] += f" · desfecho: {e['desfecho']} · [vídeo no minuto]({e['link']})  \n  {e['assunto']}"
    txt = "\n".join(L); print(txt)
    if "--md" in sys.argv: open(sys.argv[sys.argv.index("--md") + 1], "w").write(txt + "\n")


if __name__ == "__main__":
    main()
