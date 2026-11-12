"""Deixa os PDFs leves para folhear: sem transparência/blur (camadas que o leitor recompõe a cada página),
fontes locais (Inter instalada), véus embutidos nas próprias fotos (preparar_fotos.py) e PDF linearizado/comprimido.
Uso nos geradores: H = leve_html(H) antes de gravar o HTML; leve_pdf(caminho) depois de gerar o PDF."""
import re

def leve_html(h):
    h = re.sub(r'<link[^>]+fonts\.(googleapis|gstatic)\.com[^>]*>', '', h)
    h = h.replace("'Rubik'", "'Inter Display'").replace("Rubik,", "'Inter Display',").replace("font-family:Rubik", "font-family:'Inter Display'")
    h = re.sub(r'backdrop-filter:[^;}"]+;?', '', h)
    h = re.sub(r'box-shadow:[^;}"]+;?', '', h)
    # véus com gradiente transparente → já embutidos nas fotos
    h += "<style>.veu,.q-veu,.sc-veu,.resp-veu{display:none!important}.cartao{background:#161513!important;border-color:#3A3833!important}" \
         ".onda{background:#4A4740!important;height:3px!important}</style>"
    return h

def leve_pdf(path):
    try:
        import pikepdf
    except ImportError:
        return path
    with pikepdf.open(path, allow_overwriting_input=True) as pdf:
        pdf.remove_unreferenced_resources()
        pdf.save(path, linearize=True, compress_streams=True, object_stream_mode=pikepdf.ObjectStreamMode.generate,
                 recompress_flate=True)
    return path
