"""Gera os recortes fixos das fotos de setor para os relatórios (sempre as mesmas imagens, sem corte feio).
Uso: python3 pipeline/preparar_fotos.py
Entrada: docs/marca/setores/<setor>.jpg + docs/marca/setores/foco.json ({setor: {"capa": [cx, cy], "painel": [cx, cy], "cor": "#hex"}}).
Saída: docs/marca/setores/recortes/<setor>_capa.jpg (16:9, 1280×720) e <setor>_painel.jpg (2:5, 480×1200, faixa lateral da página de cada pergunta),
em duotom com a cor do setor (estilo próprio por setor, arquivo leve)."""
import json, os
from PIL import Image, ImageOps, ImageEnhance
D = "docs/marca/setores"; OUT = f"{D}/recortes"; os.makedirs(OUT, exist_ok=True)
FOCO = json.load(open(f"{D}/foco.json"))
def hexrgb(h): h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def recorte(im, prop, cx, cy, lim=None):
    W, H = im.size; z = 1
    w, h = (W, round(W / prop)) if W / H < prop else (round(H * prop), H)
    x = min(max(round(cx * W - w / 2), 0), W - w); y = min(max(round(cy * H - h / 2), 0), H - h)
    if lim:  # área proibida (ex.: carimbo de data) — empurra o recorte para fora dela
        x0, y0, x1, y1 = [round(v * s) for v, s in zip(lim, (W, H, W, H))]
        if y + h > y0 and x + w > x0 and y < y1 and x < x1: y = max(0, min(y, y0 - h)) if y0 - h >= 0 else y
    return im.crop((x, y, x + w, y + h))
def duotom(im, cor):
    g = ImageEnhance.Contrast(ImageOps.grayscale(im)).enhance(1.12)
    escuro = tuple(int(c * .22) for c in hexrgb(cor)); claro = tuple(min(255, int(245 * .82 + c * .18)) for c in hexrgb(cor))
    tom = ImageOps.colorize(g, escuro, claro, mid=hexrgb(cor))
    return Image.blend(im.convert("RGB"), tom, .78)  # 22% da cor original: foto continua reconhecível
for s, f in FOCO.items():
    src = f"{D}/{f.get('arquivo', s + '.jpg')}"
    if not os.path.exists(src): print("sem foto:", s); continue
    im = Image.open(src).convert("RGB")
    for nome, prop, tam in (("capa", 16 / 9, (1280, 720)), ("painel", 2 / 5, (480, 1200))):
        r = duotom(recorte(im, prop, *f[nome], lim=f.get("evitar")).resize(tam, Image.LANCZOS), f["cor"])
        r.save(f"{OUT}/{s}_{nome}.jpg", quality=68, optimize=True, progressive=True)
    print(s, "ok", [os.path.getsize(f"{OUT}/{s}_{n}.jpg") // 1024 for n in ("capa", "painel")], "KB")
