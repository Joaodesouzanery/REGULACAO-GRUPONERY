"""Notas «O que observar» para o cliente (skill notas-ao-cliente) e placar de cada decisão.
Regra: só aparece o que se aplica aos processos/agenda daquele cliente; no máximo 5 notas, ordenadas por urgência
(data nos próximos 30 dias → muda o placar → contexto). Tipos ativos por cliente em empresa.json → notas_ativas (padrão: todos).
Uso como módulo: placar(c, item_id, resultado) · notas(ag, emp, its, cal, cadeiras, hoje) → [(data_ord, tipo, texto_html)]"""
import re, datetime, json, os

FMT = lambda d: datetime.date.fromisoformat(str(d)[:10]).strftime("%d/%m")


def placar(c, iid, resultado="", relator=None):
    r = (resultado or "").lower()
    if re.match(r"\s*retirad", r): return ("retirado de pauta", "neutro")
    if re.match(r"\s*(pedido de )?vista", r) and "aprovad" not in r: return ("pedido de vista", "neutro")
    vs = list(c.execute("select diretor, categoria from votos where item_id=?", (iid,)))
    div = [v["diretor"] for v in vs if v["categoria"] in ("vencido", "revisor_diverge")]
    n = len({v["diretor"] for v in vs})
    if not vs: return ("sem votos registrados", "neutro")
    if re.search(r"vencid[oa] (a relatora|o relator)", r):
        relator = relator or (c.execute("select relator from itens where id=?", (iid,)).fetchone() or [None])[0]
        div = [relator] if relator else div
    m_venc = re.search(r"vencid[oa]s? (?:o |a |os |as )?(?:diretor(?:a)?(?:es)? )?([A-ZÁÉÍÓÚ][\w]+(?: [A-ZÁÉÍÓÚ][\w]+)?)", resultado or "")
    if m_venc and not re.search(r"vencid[oa] (a relatora|o relator)", r): div = [m_venc.group(1)]
    if div:
        m = re.search(r"(\d)\s*[x×]\s*(\d)", r)
        pl = f"{m.group(1)}×{m.group(2)}" if m else f"{n - len(div)}×{len(div)}"
        return (f"maioria {pl}, vencido(a) {', '.join(d.split()[0] for d in div)}", "maioria")
    return (f"unânime {n}×0" if n >= 3 else "sem divergência registrada", "unanime")


def dias_reuniao(x):
    """dias da reunião: virtual da ANTAQ dura 3 dias (campo dias no calendário tem prioridade)."""
    if x.get("dias"): return x["dias"]
    d0 = datetime.date.fromisoformat(x["data"])
    return [(d0 + datetime.timedelta(days=k)).isoformat() for k in range(3)] if x.get("formato") == "virtual" else [x["data"]]


def periodo(x):
    ds = dias_reuniao(x)
    if len(ds) == 1: return FMT(ds[0])
    return ", ".join(datetime.date.fromisoformat(d).strftime("%d") for d in ds[:-1]) + " e " + FMT(ds[-1])


def notas(ag, emp, its, cal, cadeiras=None, hoje=None, link=None, c=None):
    hoje = hoje or datetime.date.today(); H = hoje.isoformat()
    ativos = set(emp.get("notas_ativas") or ["virtual", "retirado", "vista", "mandato_relator", "condicionante", "acompanhamento", "vinculo"])
    out = []
    # 1 reunião virtual próxima
    if "virtual" in ativos:
        for x in cal:
            if x["data"] >= H and x.get("formato") == "virtual":
                out.append((x["data"], "virtual", f"<b>{periodo(x)}</b> · {x['reuniao']}ª reunião <b>virtual</b>, {len(dias_reuniao(x))} dias, <b>sem transmissão</b>: o resultado só aparece na ata (costuma sair dias depois). Itens da empresa nessa pauta não terão vídeo."))
                break
    # 2 itens retirados/vista da última sessão da empresa
    ult = its[-1]["numero"] if its else None
    prox = next((x for x in cal if x["data"] >= H and x.get("formato") != "virtual"), None)
    for i in [i for i in its if i["numero"] == ult]:
        r = (i["resultado"] or "").lower()
        if "retirado" in ativos and "retirad" in r:
            out.append((prox["data"] if prox else "9", "retirado", f"Item {i['item']} da {ult}ª foi <b>retirado de pauta</b>. Tende a voltar numa sessão transmitida" + (f": a próxima é a {prox['reuniao']}ª, em <b>{FMT(prox['data'])}</b>" if prox else "") + " (inferência)."))
        elif "vista" in ativos and re.match(r"\s*(pedido de )?vista", r):
            out.append((prox["data"] if prox else "9", "vista", f"Item {i['item']} da {ult}ª teve <b>pedido de vista</b>: volta em geral em 1 a 2 sessões" + (f" (próxima: {FMT(prox['data'])})" if prox else "") + "."))
    # 3 mandato do relator vence antes da volta
    if "mandato_relator" in ativos and cadeiras:
        rels = {i["relator"] for i in its[-8:] if i["relator"]}
        for cad in cadeiras:
            for o in cad.get("ocupantes", []):
                if o.get("nome_chave") in rels and not o.get("saida") and o.get("fim_legal") and H <= o["fim_legal"] <= (hoje + datetime.timedelta(days=120)).isoformat():
                    out.append((o["fim_legal"], "mandato_relator", f"<b>{FMT(o['fim_legal'])}</b> · termina o mandato de <b>{o['nome_chave']}</b>, relator de processos da empresa. Processo que voltar depois disso pode mudar de relator."))
    # 4 condicionantes, acompanhamento e vínculos declarados pelo analista (empresa.json → notas_manuais)
    for nm in emp.get("notas_manuais", []):
        if nm.get("tipo") in ativos and (nm.get("data") or "9") >= H:
            out.append((nm.get("data") or "9", nm["tipo"], nm["texto"]))
    out.sort(key=lambda x: (0 if x[0] <= (hoje + datetime.timedelta(days=30)).isoformat() else 1, x[0]))
    return out[:5]
