"""Marca comum dos PDFs: parceiro (padrão Circle) + «em parceria com Grupo Nery». Venda só por parceiro revendedor.
Uso nos geradores: from marca import parceria_html, MARCA_CSS → coloque parceria_html() no cartão da capa e na página final.
Trocar parceiro: --parceiro caminho/logo_branco.png (o logo do parceiro substitui o da Circle)."""
import base64, os, sys
def _b64(p):
    return "data:image/png;base64," + base64.b64encode(open(p, "rb").read()).decode() if p and os.path.exists(p) else ""
NERY_B = "docs/marca/grupo_nery/logo_branco.png"; NERY_P = "docs/marca/grupo_nery/logo_preto.png"
def parceiro_logo(claro=True):
    if "--parceiro" in sys.argv: return _b64(sys.argv[sys.argv.index("--parceiro") + 1])
    return _b64("docs/marca/circle/logo_circle_branco.png" if claro else "docs/marca/circle/logo_circle_preto.png")
def parceria_html(fundo_escuro=True):
    n = _b64(NERY_B if fundo_escuro else NERY_P)
    return f'<div class="parc"><span>em parceria com</span>{f"<img src={chr(34)}{n}{chr(34)}>" if n else "Grupo Nery"}</div>'
MARCA_CSS = ".parc{display:flex;align-items:center;gap:10px;margin:0 0 .18in;font-size:8pt;color:#BDB8AE;letter-spacing:.08em;text-transform:uppercase}.parc img{height:.26in;width:auto}"
