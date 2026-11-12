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
def natural(im, tipo):
    """Cor natural (sem duotom), leve contraste/saturação e o véu escuro EMBUTIDO na imagem (o PDF fica sem transparência)."""
    im = ImageEnhance.Color(ImageEnhance.Contrast(im.convert("RGB")).enhance(1.06)).enhance(1.08)
    W, H = im.size
    m = Image.new("L", (W, H))
    px = m.load()
    for y in range(H):
        for x in range(W):
            if tipo == "capa": a = max(0.0, 0.62 * (1 - x / (0.75 * W)))
            elif tipo == "painel": t = y / H; a = 0.25 * max(0, 1 - t / 0.3) + 0.7 * max(0, (t - 0.55) / 0.45)
            else: t = y / H; a = 0.45 * max(0, 1 - t / 0.32) + 0.85 * max(0, (t - 0.45) / 0.55)
            px[x, y] = int(255 * min(a, 0.9))
    return Image.composite(Image.new("RGB", (W, H), (11, 11, 11)), im, m)
for s, f in FOCO.items():
    src = f"{D}/{f.get('arquivo', s + '.jpg')}"
    if not os.path.exists(src): print("sem foto:", s); continue
    im = Image.open(src).convert("RGB")
    for nome, prop, tam in (("capa", 16 / 9, (1600, 900)), ("painel", 2 / 5, (600, 1500)), ("cartao", 4 / 5, (480, 600))):
        r = natural(recorte(im, prop, *f.get(nome, f["capa"]), lim=f.get("evitar")).resize(tam, Image.LANCZOS), nome)
        r.save(f"{OUT}/{s}_{nome}.jpg", quality=60, optimize=True, progressive=True)
    print(s, "ok", [os.path.getsize(f"{OUT}/{s}_{n}.jpg") // 1024 for n in ("capa", "painel", "cartao")], "KB")
