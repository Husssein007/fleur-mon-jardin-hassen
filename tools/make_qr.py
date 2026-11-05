"""Génère le QR Code de marque Fleur mon Jardin (SVG + PNG haute résolution).
Usage : python3 tools/make_qr.py "https://votre-url-finale"
Dépendances : opencv-python, rsvg-convert (librsvg)."""
import sys, re, subprocess, pathlib
import cv2, numpy as np

URL = sys.argv[1] if len(sys.argv) > 1 else "https://claude.ai/artifact/EVopY5keCkyxQnsDsQ5nbf"
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "qr"; OUT.mkdir(exist_ok=True)
GREEN, RED, DEEP, CREAM, CHAMP = "#2B603F", "#A11E36", "#1F4A33", "#FDF5E6", "#E0C9A4"

# 1. Matrix, correction level H (30 %) so the centre logo is safe
p = cv2.QRCodeEncoder_Params(); p.correction_level = cv2.QRCodeEncoder_CORRECT_LEVEL_H
img = cv2.QRCodeEncoder.create(p).encode(URL)
ys, xs = np.where(img == 0)
img = img[ys.min():ys.max()+1, xs.min():xs.max()+1]   # strip encoder's quiet zone
m = (img == 0)
n = m.shape[0]; assert m.shape == (n, n)
Q = 4                      # quiet zone (modules)
S = n + 2*Q

# 2. Logo paths (vector, from the charte)
logo = (ROOT/"assets/symbol.svg").read_text()
vb = re.search(r'viewBox="([^"]+)"', logo).group(1)
inner = logo[logo.index('>')+1: logo.rindex('</svg>')]

# centre reserve: about 22 % of the code width
c = n/2
R = round(n*0.22/2 + .5) + 0.5
def in_center(x, y): return abs(x+.5-c) <= R and abs(y+.5-c) <= R
def in_finder(x, y):
    return (x < 7 and y < 7) or (x >= n-7 and y < 7) or (x < 7 and y >= n-7)

parts = []
for y in range(n):
    for x in range(n):
        if m[y, x] and not in_finder(x, y) and not in_center(x, y):
            parts.append(f'M{x+Q} {y+Q}h1v1h-1z')
mods = f'<path fill="{DEEP}" d="{"".join(parts)}"/>'

def finder(ox, oy):
    ox += Q; oy += Q
    return (f'<rect x="{ox+.5}" y="{oy+.5}" width="6" height="6" rx="1.6" fill="none" stroke="{GREEN}" stroke-width="1"/>'
            f'<rect x="{ox+2}" y="{oy+2}" width="3" height="3" rx=".9" fill="{RED}"/>')
finders = finder(0, 0) + finder(n-7, 0) + finder(0, n-7)

# centre medallion: cream arch-door shape with the rose symbol
cx = cy = S/2; w = 2*R - 1.0; h = w*1.12
x0, y0 = cx - w/2, cy - h/2
arch = (f'<path d="M{x0} {y0+h} V{y0+w/2} A{w/2} {w/2} 0 0 1 {x0+w} {y0+w/2} V{y0+h} Z" '
        f'fill="{CREAM}" stroke="{GREEN}" stroke-width=".35"/>')
lw = w*0.78; lh = lw*80/82
logo_svg = (f'<svg x="{cx-lw/2}" y="{y0+h-lh-w*0.06}" width="{lw}" height="{lh}" viewBox="{vb}">{inner}</svg>')

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="1024" height="1024" shape-rendering="crispEdges">'
       f'<title>QR Code · Fleur mon Jardin Hassen</title>'
       f'<rect width="{S}" height="{S}" fill="{CREAM}"/>{mods}'
       f'<g shape-rendering="geometricPrecision">{finders}{arch}{logo_svg}</g></svg>')
(OUT/"fleur-mon-jardin-qr.svg").write_text(svg)
subprocess.run(["rsvg-convert", "-w", "3000", "-h", "3000", str(OUT/"fleur-mon-jardin-qr.svg"),
                "-o", str(OUT/"fleur-mon-jardin-qr.png")], check=True)

# 3. Print card (A5, 1748x2480 px = 148x210 mm @ 300 dpi)
full = (ROOT/"assets/logo_full.svg").read_text()
fvb = re.search(r'viewBox="([^"]+)"', full).group(1)
finner = full[full.index('>')+1: full.rindex('</svg>')]
W, H = 1748, 2480; aw = 1300; ax = (W-aw)/2; ay = 150
card = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<rect width="{W}" height="{H}" fill="{CHAMP}"/>
<path d="M{ax} {H-140} V{ay+aw/2} A{aw/2} {aw/2} 0 0 1 {ax+aw} {ay+aw/2} V{H-140} Z" fill="{CREAM}"/>
<path d="M{ax+26} {H-166} V{ay+aw/2} A{aw/2-26} {aw/2-26} 0 0 1 {ax+aw-26} {ay+aw/2} V{H-166} Z" fill="none" stroke="{GREEN}" stroke-opacity=".3" stroke-width="3"/>
<svg x="{(W-640)/2}" y="300" width="640" height="401" viewBox="{fvb}">{finner}</svg>
<text x="{W/2}" y="840" text-anchor="middle" font-family="EB Garamond, Garamond, Georgia, serif" font-style="italic" font-size="78" fill="{GREEN}">L’Art de la Beauté Florale</text>
<text x="{W/2}" y="910" text-anchor="middle" font-family="Century Gothic, Questrial, DejaVu Sans, sans-serif" font-size="30" letter-spacing="10" fill="{RED}">SCANNEZ · DÉCOUVREZ · COMMANDEZ</text>
<svg x="{(W-900)/2}" y="980" width="900" height="900" viewBox="0 0 {S} {S}">{svg[svg.index('>')+1: svg.rindex('</svg>')]}</svg>
<text x="{W/2}" y="1985" text-anchor="middle" font-family="Century Gothic, Questrial, DejaVu Sans, sans-serif" font-size="46" letter-spacing="6" fill="{DEEP}">+216 98 537 126</text>
<text x="{W/2}" y="2050" text-anchor="middle" font-family="Century Gothic, Questrial, DejaVu Sans, sans-serif" font-size="26" letter-spacing="9" fill="{GREEN}">WHATSAPP · INSTAGRAM · FACEBOOK · ARIANA</text>
<text x="{W/2}" y="2180" text-anchor="middle" font-family="EB Garamond, Garamond, Georgia, serif" font-style="italic" font-size="52" fill="{GREEN}">Chaque fleur raconte une histoire</text>
</svg>'''
(OUT/"fleur-mon-jardin-qr-carte.svg").write_text(card)
subprocess.run(["rsvg-convert", str(OUT/"fleur-mon-jardin-qr-carte.svg"), "-o", str(OUT/"fleur-mon-jardin-qr-carte.png")], check=True)
print("QR version modules:", n, "URL:", URL)
