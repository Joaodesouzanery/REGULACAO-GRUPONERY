"""Desfecho de um item para o interessado (empresa): favorável / desfavorável / parcial / neutro.
Usa o texto do voto do RELATOR + resultado + resumo, porque «aprovado por unanimidade» só diz que o voto do relator passou.
Regras (ordem): parcial («parcial provimento», «provimento parcial», «parcialmente»); desfavorável (nega/desprovido/indefere/
não conhece/mantém sanção/aplica multa, cassação, penalidade, advertência, caducidade); favorável (dá provimento/provido/defere/
acolhe/autoriza/homologa/arquiva/anula a sanção/converte em multa menor); senão neutro (normas, editais, atos internos)."""
import re
PARC = re.compile(r"parcial(mente)? provi|provimento parcial|parcialmente|em parte|reduz\w*( d?[ao])? (multa|penalidade|san[çc][ãa]o|valor)|multa reduzida", re.I)
PEND = re.compile(r"sem decis|pedido de vista|vista concedida|sobrestad|suspensa por pedido de vista|retirad[oa] de pauta", re.I)
DESF = re.compile(r"\bneg(a|ou|ado|ada|ar|ando)\b|n[ãa]o provid|desprov|indefer|n[ãa]o conhec|mant[ée]m (a |o )?(multa|penal|cassa|san[çc]|decis|indeferimento)|aplica(r|ndo)? (a )?(multa|cassa|penal|advert|san[çc]|suspens)|cassa[çc][ãa]o|caducidade|declara(r)? a caducidade|n[ãa]o acolh|rejeit", re.I)
FAVO = re.compile(r"d[áa](r)? provimento|(?<!des)(?<!não )(?<!nao )\bprovid[ao]s?\b|deferi|acolh|autoriz|homolog|arquiv|anula(r|ção)? (a )?(multa|san|penal|decis)|cancela(r)? (a )?(multa|auto)|convert|extin[çg]", re.I)
def desfecho(*textos):
    t = re.sub(r"passivos? ambienta(l|is) n[ãa]o conhecid[oa]s?|n[ãa]o conhecid[oa]s? (na|à) data", "passivo ambiental", " ".join(x or "" for x in textos), flags=re.I)  # nome do instituto, não «não conhece»
    if PEND.search(textos[1] or "") and not re.search(r"aprovad|provid|negad|indefer", textos[1] or "", re.I): return "pendente"
    if PARC.search(t): return "parcial"
    d, f = bool(DESF.search(t)), bool(FAVO.search(t))
    if d and not f: return "desfavorável"
    if f and not d: return "favorável"
    if d and f:  # ex.: «nega provimento… mantém» vs «dá provimento»: decide pelo verbo do relator (primeiro texto)
        r = textos[0] or ""
        return "desfavorável" if DESF.search(r) and not FAVO.search(r) else "favorável" if FAVO.search(r) and not DESF.search(r) else "parcial"
    return "neutro"
def desfecho_item(c, item_id):
    rel = c.execute("select group_concat(voto, ' | ') from votos where item_id=? and eh_relator=1", (item_id,)).fetchone()[0]
    res, resumo = c.execute("select resultado, resumo from itens where id=?", (item_id,)).fetchone()
    if re.search(r"vencid[oa] (o |a )?relator|maioria.{0,40}vencid[oa] (o |a )?relator", res or "", re.I):  # relator perdeu: decide pelo resultado
        return desfecho(None, res, resumo)
    return desfecho(rel, res, resumo)
