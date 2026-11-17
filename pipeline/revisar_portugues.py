"""Revisão de português dos documentos (skill revisao-portugues): acentuação, crase óbvia, espaços, aspas e travessão.
Não altera falas literais da legenda (entre «»). Uso: python3 pipeline/revisar_portugues.py <arquivo.html|.md|.pdf|.py> [...] [--corrigir]
--corrigir reescreve .md/.json/.py só nas palavras da lista segura (fora de citações «» e fora de código/URLs). Sai 1 se houver alerta."""
import sys, re, os, html, subprocess

# palavras sem acento → forma correta (lista segura: não existem sem acento em português formal)
PARES = {
    "nao": "não", "sao": "são", "entao": "então", "tambem": "também", "ja": "já", "ate": "até", "apos": "após", "voce": "você",
    "reuniao": "reunião", "reunioes": "reuniões", "decisao": "decisão", "decisoes": "decisões", "votacao": "votação", "sessao": "sessão", "sessoes": "sessões",
    "agencia": "agência", "agencias": "agências", "diretoria": "diretoria", "superintendencia": "superintendência", "audiencia": "audiência", "audiencias": "audiências",
    "previa": "prévia", "previsao": "previsão", "estimativa": "estimativa", "analise": "análise", "analises": "análises", "historico": "histórico",
    "publico": "público", "publica": "pública", "publicas": "públicas", "publicos": "públicos", "orgao": "órgão", "orgaos": "órgãos",
    "processo": "processo", "tramitacao": "tramitação", "concessao": "concessão", "concessoes": "concessões", "autorizacao": "autorização",
    "regulatorio": "regulatório", "regulatoria": "regulatória", "economico": "econômico", "economica": "econômica", "reequilibrio": "reequilíbrio",
    "relatorio": "relatório", "relatorios": "relatórios", "politica": "política", "tecnica": "técnica", "tecnico": "técnico", "juridico": "jurídico",
    "unanime": "unânime", "unanimidade": "unanimidade", "divergencia": "divergência", "divergencias": "divergências", "transmissao": "transmissão",
    "mineracao": "mineração", "aviacao": "aviação", "energia": "energia", "petroleo": "petróleo", "saude": "saúde", "agua": "água", "aguas": "águas",
    "servico": "serviço", "servicos": "serviços", "cliente": "cliente", "numero": "número", "numeros": "números", "proximo": "próximo", "proxima": "próxima",
    "ultimo": "último", "ultima": "última", "periodo": "período", "credito": "crédito", "valido": "válido", "valida": "válida", "minimo": "mínimo",
    "maximo": "máximo", "medio": "médio", "media": "média", "mes": "mês", "meses": "meses", "inicio": "início", "conclusao": "conclusão", "edicao": "edição",
    "informacao": "informação", "informacoes": "informações", "atencao": "atenção", "situacao": "situação", "composicao": "composição", "nomeacao": "nomeação",
    "vacancia": "vacância", "substituicao": "substituição", "reconducao": "recondução", "posicao": "posição", "conferencia": "conferência", "evidencia": "evidência",
}
PARES = {k: v for k, v in PARES.items() if k != v}
CIT = re.compile(r"«[^»]*»")


def texto(p):
    if p.endswith(".pdf"): return subprocess.run(["pdftotext", "-layout", p, "-"], capture_output=True, text=True).stdout
    t = open(p, encoding="utf-8", errors="ignore").read()
    if p.endswith(".html"):
        t = re.sub(r"<style.*?</style>|<script.*?</script>", " ", t, flags=re.S); t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return t


HTMLDOC = False


def alertas(t):
    sem = CIT.sub(" ", t)
    sem = re.sub(r"https?://\S+|`[^`]*`|\b[\w./-]+\.(py|json|md|sh|pdf|html)\b|data/\S+|pipeline/\S+", " ", sem)
    out = []
    for w in re.findall(r"\b[a-zA-Z]+\b", sem):
        k = w.lower()
        if k in PARES: out.append(("acento", w, PARES[k]))
    for m in re.finditer(r"\ba (ela|ele|eles|elas|mim|ti|você)\b", sem): pass
    for m in re.finditer(r"\b(à) (ele|eles|um|uma|partir de|nível)\b", sem, re.I): out.append(("crase", m.group(0), m.group(0).replace("à", "a")))
    for m in re.finditer(r"\b(devido|referente|junto|frente|quanto|em relação|graças) a a\b", sem): out.append(("crase", m.group(0), m.group(0)[:-3] + "à"))
    if len(re.findall(r"\S — \S", sem)) > 3: out.append(("travessão", f"{len(re.findall(r'\S — \S', sem))} travessões no texto corrido", "use vírgula, dois-pontos ou parênteses"))
    for m in (re.finditer(r"\S {2,}\S", sem[:200000]) if not HTMLDOC else []):
        if "\n" not in m.group(0): out.append(("espaço", "espaço duplo", m.group(0)[:30])); break
    if '"' in sem and "«" in t: out.append(("aspas", "aspas retas misturadas com «»", "padronize em «»"))
    return out


def corrigir(p):
    t = open(p, encoding="utf-8").read(); partes = re.split(r"(«[^»]*»|https?://\S+|`[^`]*`)", t)
    def troca(m):
        w = m.group(0); v = PARES.get(w.lower())
        if not v: return w
        return v.capitalize() if w[0].isupper() else v
    for i in range(0, len(partes), 2): partes[i] = re.sub(r"\b[a-zA-Z]+\b", troca, partes[i])
    open(p, "w", encoding="utf-8").write("".join(partes))


if __name__ == "__main__":
    ruim = 0
    for p in [a for a in sys.argv[1:] if not a.startswith("--")]:
        if "--corrigir" in sys.argv and p.endswith((".md", ".json", ".txt")): corrigir(p)
        HTMLDOC = p.endswith((".html", ".pdf")); al = alertas(texto(p)); ruim += len(al)
        c = {}
        for tp, w, s in al: c.setdefault(tp, []).append(f"{w} → {s}")
        print(f"{p}: {len(al)} alerta(s)" + "".join(f"\n  [{tp}] " + "; ".join(sorted(set(v))[:12]) for tp, v in c.items()))
    sys.exit(1 if ruim else 0)
