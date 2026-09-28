#!/usr/bin/env python3
"""Javorníky — generátor plagátových návrhov (SVG, A3 pomer 1:1,414).

Každý plagát má rovnaký skelet (papier · ilustrácia · textový blok · zrno),
mení sa len ilustrácia. Spusti:  python3 generate.py  → ../svg/*.svg

Plátno 1000 × 1414 jednotiek = A3 (297 × 420 mm). Do Procreate/Illustratora
importuj SVG a zväčši na 3508 × 4961 px (300 dpi) — je to vektor, nič sa nerozmaže.
"""
import math
import random
from pathlib import Path

W, H = 1000, 1414
OUT = Path(__file__).resolve().parent.parent / "svg"

# Paleta z briefu (riso, 5 farieb)
CREAM = "#F0E6D2"
RUST = "#C4522A"
OCHRE = "#E0A02E"
GREEN = "#3A5A40"
DARK = "#2B231A"

# Ilustračné pole a textový blok (spoločný skelet)
PX, PY, PW, PH = 60, 60, 880, 960
TEXT_Y = 1075

FONTS = (
    "@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;"
    "9..144,600;9..144,900&family=Archivo+Black&family=Archivo+Narrow:wght@500;700"
    "&family=IBM+Plex+Mono:wght@400;600&display=swap');"
)


# ---------------------------------------------------------------- helpers

def f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def smooth_path(pts, close_to=None):
    """Catmull-Rom → kubické Bézierove krivky. close_to = y, kam uzavrieť dole."""
    d = f"M{f(pts[0][0])},{f(pts[0][1])}"
    for i in range(len(pts) - 1):
        p0 = pts[max(i - 1, 0)]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[min(i + 2, len(pts) - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{f(c1[0])},{f(c1[1])} {f(c2[0])},{f(c2[1])} {f(p2[0])},{f(p2[1])}"
    if close_to is not None:
        d += f" L{f(pts[-1][0])},{f(close_to)} L{f(pts[0][0])},{f(close_to)} Z"
    return d


def ridge(base, bumps, x0=PX - 30, x1=PX + PW + 30, step=22, wobble=0.0, seed=1):
    """Oblý hrebeň: súčet gaussovských kopcov. bumps = [(x, výška, šírka)]."""
    rnd = random.Random(seed)
    pts = []
    x = x0
    while x <= x1 + step:
        y = base
        for bx, bh, bw in bumps:
            y -= bh * math.exp(-((x - bx) / bw) ** 2)
        y += rnd.uniform(-wobble, wobble)
        pts.append((x, y))
        x += step
    return pts


def band(top, lower, overlap):
    """Plocha medzi hrebeňom a ďalším hrebeňom (+ presah → riso prekryv farieb)."""
    low = [(x, y + overlap) for x, y in reversed(lower)]
    d = smooth_path(top)
    d += " L" + smooth_path(low)[1:] + " Z"
    return d


def y_at(pts, x):
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        if ax <= x <= bx:
            t = (x - ax) / (bx - ax)
            return ay + (by - ay) * t
    return pts[-1][1]


def svg_open(title, bg=CREAM):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="297mm" height="420mm">',
        f"<title>{title}</title>",
        f"<style>{FONTS}"
        ".serif{font-family:Fraunces,'Bitstream Charter',Georgia,serif}"
        ".black{font-family:'Archivo Black','Arial Black',sans-serif}"
        ".narrow{font-family:'Archivo Narrow','Liberation Sans Narrow',sans-serif}"
        ".mono{font-family:'IBM Plex Mono','DejaVu Sans Mono',monospace}"
        ".mul{mix-blend-mode:multiply}"
        "</style>",
        "<defs>",
        # zrno papiera
        '<filter id="grain" x="0" y="0" width="100%" height="100%">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="3" seed="7" stitchTiles="stitch"/>'
        '<feColorMatrix type="saturate" values="0"/>'
        '<feComponentTransfer><feFuncR type="linear" slope="1.6" intercept="-0.2"/>'
        '<feFuncG type="linear" slope="1.6" intercept="-0.2"/><feFuncB type="linear" slope="1.6" intercept="-0.2"/></feComponentTransfer>'
        "</filter>",
        # „dýchajúci“ okraj plochy (ako Nikko Rull / Old Beach)
        '<filter id="rough" x="-2%" y="-2%" width="104%" height="104%">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="4"/>'
        '<feDisplacementMap in="SourceGraphic" scale="4"/></filter>',
        '<filter id="rough2" x="-2%" y="-2%" width="104%" height="104%">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.09" numOctaves="2" seed="9"/>'
        '<feDisplacementMap in="SourceGraphic" scale="3"/></filter>',
        f'<clipPath id="panel"><rect x="{PX}" y="{PY}" width="{PW}" height="{PH}"/></clipPath>',
        # riso raster (tint 50 %) pre vzdialené plochy
        f'<pattern id="dotsG" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(22)">'
        f'<circle cx="3.5" cy="3.5" r="2.1" fill="{GREEN}"/></pattern>',
        f'<pattern id="dotsR" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(-18)">'
        f'<circle cx="3" cy="3" r="1.7" fill="{RUST}"/></pattern>',
        f'<pattern id="dotsD" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
        f'<circle cx="3" cy="3" r="1.3" fill="{DARK}"/></pattern>',
        "</defs>",
        f'<g id="01-papier"><rect width="{W}" height="{H}" fill="{bg}"/></g>',
    ]


def grain(opacity=0.13):
    return (
        f'<g id="09-zrno" class="mul" opacity="{opacity}">'
        f'<rect width="{W}" height="{H}" filter="url(#grain)"/></g>'
    )


def text_block(title, sub, story, data, edition="Edícia 1 / 100", ink=DARK, accent=RUST,
               title_class="black", title_size=104, title_spacing=6):
    """Vrstva 05 · typografia — rovnaký komponent pre celú sériu."""
    y = TEXT_Y
    out = ['<g id="08-typografia">']
    out.append(
        f'<text x="{PX}" y="{y + 78}" class="{title_class}" font-size="{title_size}" '
        f'letter-spacing="{title_spacing}" fill="{ink}">{title}</text>'
    )
    out.append(
        f'<text x="{PX + 2}" y="{y + 122}" class="mono" font-size="17" letter-spacing="3.2" '
        f'fill="{accent}" font-weight="600">{sub}</text>'
    )
    # príbeh — textový blok, plagát niečo rozpráva
    for i, line in enumerate(story):
        out.append(
            f'<text x="{PX}" y="{y + 172 + i * 27}" class="serif" font-size="20.5" fill="{ink}">{line}</text>'
        )
    ly = H - 66
    out.append(f'<line x1="{PX}" y1="{ly - 30}" x2="{PX + PW}" y2="{ly - 30}" stroke="{ink}" stroke-width="1.4"/>')
    out.append(f'<text x="{PX}" y="{ly}" class="mono" font-size="15" letter-spacing="1.5" fill="{ink}">{data}</text>')
    out.append(
        f'<text x="{PX + PW}" y="{ly}" class="mono" font-size="15" letter-spacing="1.5" fill="{ink}" '
        f'text-anchor="end">{edition}  ·  ___________</text>'
    )
    out.append("</g>")
    return "\n".join(out)


def write(name, parts):
    parts.append("</svg>")
    (OUT / name).write_text("\n".join(parts), encoding="utf-8")
    print("✓", name)


# ---------------------------------------------------------------- motívy

def beech(x, y, s, color):
    """Buk ako riso „lízanka“ — koruna + kmeň."""
    return (
        f'<rect x="{f(x - s * 0.08)}" y="{f(y - s * 0.9)}" width="{f(s * 0.16)}" height="{f(s * 0.95)}" fill="{color}"/>'
        f'<ellipse cx="{f(x)}" cy="{f(y - s * 1.25)}" rx="{f(s * 0.52)}" ry="{f(s * 0.66)}" fill="{color}"/>'
    )


def spruce(x, y, s, color):
    return (
        f'<path d="M{f(x)},{f(y - s * 2)} L{f(x + s * 0.5)},{f(y)} L{f(x - s * 0.5)},{f(y)} Z" fill="{color}"/>'
    )


def cottage(x, y, s, wall, roof, window=CREAM, chimney=True, smoke=None):
    """Kopaničiarska drevenica — nízka, strmá strecha, jedno okno."""
    w, h = s * 1.5, s * 0.8
    out = []
    if chimney:
        out.append(f'<rect x="{f(x + w * 0.18)}" y="{f(y - h - s * 0.95)}" width="{f(s * 0.14)}" height="{f(s * 0.5)}" fill="{roof}"/>')
    out.append(f'<rect x="{f(x - w / 2)}" y="{f(y - h)}" width="{f(w)}" height="{f(h + 2)}" fill="{wall}"/>')
    out.append(
        f'<path d="M{f(x - w / 2 - s * 0.18)},{f(y - h + 1)} L{f(x)},{f(y - h - s * 0.85)} '
        f'L{f(x + w / 2 + s * 0.18)},{f(y - h + 1)} Z" fill="{roof}"/>'
    )
    out.append(f'<rect x="{f(x - w * 0.28)}" y="{f(y - h * 0.68)}" width="{f(s * 0.3)}" height="{f(s * 0.3)}" fill="{window}"/>')
    out.append(f'<rect x="{f(x + w * 0.12)}" y="{f(y - h * 0.75)}" width="{f(s * 0.26)}" height="{f(h * 0.75 + 2)}" fill="{roof}"/>')
    if smoke:
        sx, sy = x + w * 0.25, y - h - s * 1.05
        out.append(
            f'<path d="M{f(sx)},{f(sy)} q{f(-s*.3)},{f(-s*.3)} 0,{f(-s*.6)} t0,{f(-s*.6)}" '
            f'fill="none" stroke="{smoke}" stroke-width="{f(s*.09)}" stroke-linecap="round"/>'
        )
    return "".join(out)


def sheep(x, y, s, body, head, flip=False):
    k = -1 if flip else 1
    out = [
        f'<rect x="{f(x - s*.45)}" y="{f(y - s*.2)}" width="{f(s*.12)}" height="{f(s*.42)}" fill="{head}"/>',
        f'<rect x="{f(x + s*.3)}" y="{f(y - s*.2)}" width="{f(s*.12)}" height="{f(s*.42)}" fill="{head}"/>',
        f'<ellipse cx="{f(x)}" cy="{f(y - s*.35)}" rx="{f(s*.72)}" ry="{f(s*.42)}" fill="{body}"/>',
        f'<ellipse cx="{f(x + k*s*.78)}" cy="{f(y - s*.5)}" rx="{f(s*.22)}" ry="{f(s*.17)}" fill="{head}" '
        f'transform="rotate({k*25} {f(x + k*s*.78)} {f(y - s*.5)})"/>',
    ]
    return "".join(out)


def tower(x, y, s, color, stroke=None):
    """10 m rozhľadňa na Stratenci — štíhla vežička s vyhliadkou."""
    sw = stroke or s * 0.07
    h = s * 3
    return (
        f'<g fill="none" stroke="{color}" stroke-width="{f(sw)}" stroke-linejoin="round">'
        f'<path d="M{f(x - s*.45)},{f(y)} L{f(x - s*.22)},{f(y - h)} M{f(x + s*.45)},{f(y)} L{f(x + s*.22)},{f(y - h)}"/>'
        f'<path d="M{f(x - s*.4)},{f(y - h*.25)} L{f(x + s*.35)},{f(y - h*.5)} M{f(x + s*.4)},{f(y - h*.25)} L{f(x - s*.35)},{f(y - h*.5)}'
        f' M{f(x - s*.33)},{f(y - h*.5)} L{f(x + s*.28)},{f(y - h*.75)} M{f(x + s*.33)},{f(y - h*.5)} L{f(x - s*.28)},{f(y - h*.75)}"/>'
        f"</g>"
        f'<rect x="{f(x - s*.4)}" y="{f(y - h - s*.3)}" width="{f(s*.8)}" height="{f(s*.3)}" fill="{color}"/>'
        f'<path d="M{f(x - s*.5)},{f(y - h - s*.3)} L{f(x)},{f(y - h - s*.75)} L{f(x + s*.5)},{f(y - h - s*.3)} Z" fill="{color}"/>'
    )


def crosses(x, y, s, color, gap=None):
    """Tri betónové kríže — vojnový pamätník."""
    gap = gap or s * 0.9
    out = []
    for i, k in enumerate((-1, 0, 1)):
        hh = s * (1.25 if k == 0 else 1.0)
        cx = x + k * gap
        out.append(f'<rect x="{f(cx - s*.09)}" y="{f(y - hh)}" width="{f(s*.18)}" height="{f(hh)}" fill="{color}"/>')
        out.append(f'<rect x="{f(cx - s*.36)}" y="{f(y - hh*.74)}" width="{f(s*.72)}" height="{f(s*.16)}" fill="{color}"/>')
    return "".join(out)


def maple_leaf_pts(cx, cy, R, rot=0.0, teeth=True):
    """Javor horský — 5 lalokov, zúbkovaný okraj. Vráti body obrysu."""
    lobes = [(90, 1.0, 34), (32, 0.9, 30), (148, 0.9, 30), (-24, 0.6, 26), (204, 0.6, 26)]
    pts = []
    n = 540
    for i in range(n):
        th = -90 + 360 * i / n  # začni pri stopke
        r = 0.2
        for a, rr, w in lobes:
            dth = (th - a + 540) % 360 - 180
            if abs(dth) < w * 1.6:
                v = max(0.0, 1 - abs(dth) / (w * 1.6)) ** 0.75
                r = max(r, 0.2 + (rr - 0.2) * v)
        if teeth and r > 0.3:
            ph = (i * 64 / n) % 1.0
            r += 0.045 * (1 - ph) * min(1, (r - 0.3) * 4)
        t = math.radians(th + rot)
        pts.append((cx + R * r * math.cos(t), cy - R * r * math.sin(t)))
    return pts


def poly(pts):
    return "M" + " L".join(f"{f(x)},{f(y)}" for x, y in pts) + " Z"


# =================================================================== 01 · RISO

def p01_riso():
    rnd = random.Random(11)
    s = svg_open("Javorníky — 01 Riso panoráma")
    s.append('<g clip-path="url(#panel)">')

    # 02 · slnko — okrové, nie červené
    s.append(f'<g id="02-slnko" transform="translate(1.5 1)"><circle cx="610" cy="380" r="196" fill="{OCHRE}"/></g>')

    # vzdialený hrebeň — rastrový tint zelenej, na ňom rozhľadňa a kríže (Stratenec)
    far = ridge(560, [(250, 70, 190), (640, 95, 170), (900, 40, 150)], wobble=2, seed=3)
    back = ridge(690, [(160, 110, 170), (470, 70, 160), (780, 120, 190)], wobble=2, seed=5)
    mid = ridge(830, [(90, 95, 150), (400, 150, 210), (820, 60, 160)], wobble=1.5, seed=8)
    front = ridge(1000, [(230, 60, 190), (640, 115, 220), (960, 70, 150)], wobble=1.5, seed=13)

    s.append(f'<g id="03a-vzdialeny" class="mul" transform="translate(1.5 -1)" filter="url(#rough)">'
             f'<path d="{band(far, back, 40)}" fill="url(#dotsG)"/>')
    tx = 655
    s.append(tower(tx, y_at(far, tx) + 4, 16, GREEN))
    s.append(crosses(tx - 64, y_at(far, tx - 64) + 4, 13, GREEN, gap=11))
    s.append("</g>")

    # 03 · zadný hrebeň — zelená + bučina ako clipping mask
    s.append(f'<g id="03-zadny-hreben" class="mul" transform="translate(1.5 -1)" filter="url(#rough)">'
             f'<path d="{band(back, mid, 12)}" fill="{GREEN}"/>')
    x = PX - 10
    while x < PX + PW + 20:
        sz = rnd.uniform(15, 24)
        s.append(beech(x, y_at(back, x) + sz * 0.9, sz, GREEN))
        x += rnd.uniform(15, 27)
    s.append("</g>")

    # 04 · stredný hrebeň — hrdzavá, multiply 92 % → prekryv so zelenou = 4. farba
    s.append(f'<g id="04-stredny-hreben" class="mul" opacity="0.92" transform="translate(-1.5 1)" filter="url(#rough)">'
             f'<path d="{band(mid, front, 40)}" fill="{RUST}"/>')
    s.append("</g>")
    # jesenné buky — okrová, žltá bučina v októbri
    s.append('<g id="04b-buky" transform="translate(1 1.5)" filter="url(#rough)">')
    for bx, bs in ((150, 30), (196, 26), (700, 30), (742, 34), (790, 27)):
        s.append(beech(bx, y_at(mid, bx) + 22, bs, OCHRE))
    s.append("</g>")

    # 05 · kopanica a ovce
    hx = 318
    hy = y_at(mid, hx) + 3
    s.append('<g id="05-kopanica-ovce" filter="url(#rough2)">')
    s.append(cottage(hx, hy, 34, DARK, DARK, window=OCHRE, smoke=DARK))
    s.append(beech(hx + 68, y_at(mid, hx + 68) + 30, 34, DARK))
    for (ox, oy, sz, fl) in [(470, 36, 17, False), (515, 58, 15, True), (430, 70, 16, False)]:
        s.append(sheep(ox, y_at(mid, ox) + oy, sz, CREAM, DARK, fl))
    s.append("</g>")

    # 06 · predný hrebeň — tmavá
    s.append(f'<g id="06-predny-hreben" filter="url(#rough)"><path d="{smooth_path(front, H)}" fill="{DARK}"/></g>')

    # 07 · trasa — prerušovaná krémová, tenká; hore-dole cez kopce
    tr = []
    for xx in range(PX - 20, 700, 14):
        tr.append((xx, y_at(front, xx) + 22))
    # výstup na stredný hrebeň serpentínou
    sx, sy = tr[-1]
    tgt_x = 560
    tgt_y = y_at(mid, tgt_x) + 18
    tr2 = [(sx, sy)]
    for k in range(1, 9):
        t = k / 8
        tr2.append((sx + (tgt_x - sx) * t + 40 * math.sin(t * math.pi * 2.5), sy + (tgt_y - sy) * t))
    tr3 = [(xx, y_at(mid, xx) + 18) for xx in range(tgt_x, 120, -16)]
    s.append(
        f'<g id="07-trasa" fill="none" stroke="{CREAM}" stroke-width="3" stroke-dasharray="9 8" stroke-linecap="round">'
        f'<path d="{smooth_path(tr)}"/>'
        f'<path d="{smooth_path(tr2)}" stroke="{CREAM}"/>'
        f'<path d="{smooth_path(tr3)}"/></g>'
    )
    # vtáky
    for bx, by, bs in [(215, 250, 12), (248, 232, 9), (270, 262, 7)]:
        s.append(f'<path d="M{bx-bs},{by-bs*.4} q{bs*.5},{bs*.1} {bs},{bs*.5} q{bs*.5},{-bs*.4} {bs},{-bs*.5}" '
                 f'fill="none" stroke="{DARK}" stroke-width="2.4" stroke-linecap="round"/>')
    s.append("</g>")

    s.append(text_block(
        "JAVORNÍKY",
        "80 KM OBLÉHO HREBEŇA · SK / CZ · 1072 M N. M.",
        [
            "Žiadne štíty. Len hrebeň, ktorý sa vlní po hranici dve krajiny naraz,",
            "a samoty, kde sa od sedemnásteho storočia žije po svojom.",
            "V októbri tu bučiny horia na žlto a chodníky sú z blata.",
        ],
        "49.33° N  18.21° E  ·  Kopce a miesta  ·  A3",
    ))
    s.append(grain())
    write("01-riso-panorama.svg", s)


# ================================================== 02 · KOPANIČIARSKA TYPOGRAFIA

def p02_typo():
    s = svg_open("Javorníky — 02 Kopaničiarska typografia")
    s.append('<g clip-path="url(#panel)">')
    s.append(f'<rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" fill="{GREEN}"/>')

    # šírky v Archivo Black pri 100 px (zmerané v Chromiu) → každý názov vyplní šírku
    names = [
        ("BACHROŇOVCI", CREAM, 826),
        ("BIELOVCI", OCHRE, 524),
        ("SOLÍKOVCI", CREAM, 611),
        ("OVSENOVCI", OCHRE, 655),
        ("GREGUŠOVCI", CREAM, 742),
        ("U LOVÁSOV", RUST, 645),
    ]
    line_x = PX + 50
    tx0 = line_x + 44
    avail = PX + PW - 34 - tx0
    s.append(f'<line x1="{line_x}" y1="{PY}" x2="{line_x}" y2="{PY + PH}" stroke="{CREAM}" stroke-width="3" '
             f'stroke-dasharray="10 9" opacity=".85"/>')
    y = PY + 40
    for nm, col, w100 in names:
        fs = 100 * avail / w100
        y += fs * 0.74
        s.append(f'<circle cx="{line_x}" cy="{f(y - fs * 0.36)}" r="13" fill="{GREEN}" stroke="{CREAM}" stroke-width="4"/>')
        s.append(f'<text x="{tx0}" y="{f(y)}" class="black" font-size="{f(fs)}" fill="{col}">{nm}</text>')
        y += 36
    # dole: samoty na hrebeni
    hill = ridge(PY + PH - 10, [(300, 70, 240), (760, 95, 230)], wobble=1, seed=21)
    s.append(f'<circle cx="800" cy="{PY + PH - 78}" r="58" fill="{OCHRE}"/>')
    s.append(f'<g filter="url(#rough)"><path d="{smooth_path(hill, H)}" fill="{DARK}"/>')
    rnd = random.Random(4)
    for hx in [150, 262, 395, 540, 655, 800, 890]:
        sz = rnd.uniform(14, 19)
        s.append(cottage(hx, y_at(hill, hx) + 5, sz, CREAM, CREAM, window=DARK, chimney=rnd.random() > .4))
    s.append("</g>")
    s.append("</g>")

    s.append(text_block(
        "~900 SAMÔT",
        "KOPANICE JAVORNÍKOV · OD 17. STOROČIA",
        [
            "Kto sem prišiel klčovať les, dal miestu svoje meno. Rody sa stali adresami",
            "a adresy kontrolami na trati. Kto tadiaľ bežal, pozná ich po poradí —",
            "a vie, pri ktorej sa mu minula voda.",
        ],
        "Kopaničiarske osady  ·  Javorníky  ·  A3",
        title_size=96, title_spacing=3,
    ))
    s.append(grain(0.12))
    write("02-kopaniciarska-typografia.svg", s)


# ======================================================= 03 · LINKOVÁ PANORÁMA

def hatch_fill(pts, spacing, width, color, clip_id, bottom, extra=""):
    """Ryté zvislé šrafovanie — plocha hrebeňa z čiar, hustota = vzdialenosť."""
    out = [f'<clipPath id="{clip_id}"><path d="{smooth_path(pts, bottom)}"/></clipPath>']
    out.append(f'<path d="{smooth_path(pts, bottom)}" fill="{CREAM}"/>')
    top = min(p[1] for p in pts) - 5
    d = []
    x = PX - 30
    k = 0
    while x < PX + PW + 30:
        # čiara začína kúsok pod hranou, dĺžka sa strieda → rytinová textúra
        y1 = y_at(pts, x) + (0 if k % 3 else 4)
        d.append(f"M{f(x)},{f(max(top, y1))} V{f(bottom)}")
        x += spacing
        k += 1
    out.append(f'<path d="{" ".join(d)}" stroke="{color}" stroke-width="{width}" clip-path="url(#{clip_id})" {extra}/>')
    out.append(f'<path d="{smooth_path(pts)}" fill="none" stroke="{color}" stroke-width="1.8"/>')
    return "\n".join(out)


def p03_linka():
    s = svg_open("Javorníky — 03 Linková panoráma")
    s.append('<g clip-path="url(#panel)">')
    s.append(f'<rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" fill="none" stroke="{DARK}" stroke-width="2"/>')

    # slnko — hrdzavý akcent, vodorovné šrafy
    cx, cy, r = 700, 330, 92
    s.append(f'<clipPath id="sun"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>')
    d = " ".join(f"M{cx - r},{y} H{cx + r}" for y in range(cy - r, cy + r, 7))
    s.append(f'<path d="{d}" stroke="{RUST}" stroke-width="3.2" clip-path="url(#sun)"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{RUST}" stroke-width="1.6"/>')
    # oblohové linky pri horizonte
    for i, y in enumerate(range(215, 300, 9)):
        x1 = 110 + (i * 53) % 140
        s.append(f'<line x1="{x1}" y1="{y}" x2="{x1 + 170 + (i*37) % 120}" y2="{y}" stroke="{DARK}" stroke-width=".9"/>')

    # hlavný hrebeň — vrcholy v reálnom poradí po hranici (SV → JZ), výška úmerná n. m.
    peaks = [
        ("Kasárne", 210, None, 105),
        ("Veľký Javorník", 400, 1072, 170),
        ("Stratenec", 505, 1055, 160),
        ("Kohútka", 690, 913, 100),
        ("Makyta", 840, 923, 105),
    ]
    base = 700
    bumps = [(x, (h or 880) * 0 + hh, 70) for _, x, h, hh in peaks] + [(300, 70, 80), (600, 60, 70), (760, 60, 60)]
    main = ridge(base, bumps, step=12, seed=2)
    s.append(hatch_fill(main, 6.5, 1.0, DARK, "hr1", 1100))

    # rozhľadňa + kríže na Stratenci
    sx = 505
    sy = y_at(main, sx) + 2
    s.append(tower(sx, sy, 15, DARK, stroke=1.8))
    s.append(crosses(sx + 40, y_at(main, sx + 40) + 2, 9, DARK, gap=9))

    mid = ridge(830, [(140, 110, 150), (480, 70, 170), (820, 130, 150)], step=12, seed=6)
    s.append(hatch_fill(mid, 4.2, 1.35, DARK, "hr2", 1100))
    near = ridge(960, [(300, 90, 200), (700, 60, 180)], step=12, seed=9)
    s.append(hatch_fill(near, 3.0, 1.9, DARK, "hr3", 1100))
    # osamelá kopanica v popredí — vybraná z rytiny
    hx = 610
    s.append(cottage(hx, y_at(near, hx) + 16, 22, CREAM, CREAM, window=DARK))

    # popisky vrcholov
    for name, x, h, _ in peaks:
        py = y_at(main, x)
        if name == "Stratenec":
            py -= 58
        ly = 610 - (0 if name not in ("Veľký Javorník",) else 40)
        ly = min(ly, py - 26)
        s.append(f'<line x1="{x}" y1="{ly + 8}" x2="{x}" y2="{py - 8}" stroke="{DARK}" stroke-width=".9"/>')
        s.append(f'<text x="{x}" y="{ly - 16}" class="serif" font-size="17" font-style="italic" '
                 f'text-anchor="middle" fill="{DARK}">{name}</text>')
        if h:
            s.append(f'<text x="{x}" y="{ly + 2}" class="mono" font-size="11.5" letter-spacing="1.5" '
                     f'text-anchor="middle" fill="{RUST}">{h} m</text>')
    s.append("</g>")

    s.append(text_block(
        "Javorníky",
        "PANORÁMA HREBEŇA · ČADCA → LYSÁ POD MAKYTOU",
        [
            "Z rozhľadne na Stratenci dovidieť na obe strany hranice naraz.",
            "Hrebeň nemá jediný štít, ktorý by kričal — má osemdesiat kilometrov",
            "ticha, bukov a lúk s čučoriedkami. Plagát do obývačky, nie do šatne.",
        ],
        "Stratenec 1055 m  ·  Veľký Javorník 1072 m  ·  A3",
        title_class="serif", title_size=112, title_spacing=0,
    ).replace('class="serif" font-size="112"', 'class="serif" font-size="112" font-weight="900"'))
    s.append(grain(0.10))
    write("03-linkova-panorama.svg", s)


# ============================================================ 04 · LINORYT

def gouges(rnd, area_pts, n, length, color, angle_fn, width=3.5, below=(10, 200), xs=None):
    """Sekané šrafy — klinové ťahy dlátom po svahu."""
    out = []
    for _ in range(n):
        x = rnd.uniform(*(xs or (PX, PX + PW)))
        top = y_at(area_pts, x)
        y = top + rnd.uniform(*below)
        a = angle_fn(x)
        L = length * rnd.uniform(0.6, 1.2)
        dx, dy = math.cos(a) * L, math.sin(a) * L
        nx, ny = -math.sin(a) * width / 2, math.cos(a) * width / 2
        out.append(
            f'<path d="M{f(x)},{f(y)} L{f(x + dx + nx)},{f(y + dy + ny)} L{f(x + dx - nx)},{f(y + dy - ny)} Z" fill="{color}"/>'
        )
    return "".join(out)


def slope_angle(pts):
    def fn(x):
        y1, y2 = y_at(pts, x - 6), y_at(pts, x + 6)
        return math.atan2(y2 - y1, 12)
    return fn


def log_cabin(x, y, s):
    """Zrubová drevenica — linorytom: tmavý zrub, krémové brvná, šindeľ."""
    w, h = s * 2.3, s * 1.25
    out = [f'<rect x="{f(x - w/2)}" y="{f(y - h)}" width="{f(w)}" height="{f(h)}" fill="{DARK}"/>']
    n = 7
    for i in range(n):
        yy = y - h + (i + 0.55) * h / n
        out.append(f'<path d="M{f(x - w/2 + 4)},{f(yy)} Q{f(x)},{f(yy + 3)} {f(x + w/2 - 4)},{f(yy - 1)}" '
                   f'stroke="{CREAM}" stroke-width="{f(s*.055)}" fill="none" stroke-linecap="round"/>')
    # presahy brvien na rohoch
    for i in range(n):
        yy = y - h + (i + 0.3) * h / n
        for sx in (-1, 1):
            out.append(f'<rect x="{f(x + sx*w/2 - (s*.16 if sx < 0 else 0))}" y="{f(yy)}" width="{f(s*.16)}" '
                       f'height="{f(h/n*.7)}" fill="{DARK}"/>')
    # okno
    out.append(f'<rect x="{f(x - s*.42)}" y="{f(y - h*.72)}" width="{f(s*.5)}" height="{f(s*.5)}" fill="{OCHRE}" stroke="{DARK}" stroke-width="{f(s*.07)}"/>')
    out.append(f'<path d="M{f(x - s*.17)},{f(y - h*.72)} V{f(y - h*.72 + s*.5)} M{f(x - s*.42)},{f(y - h*.72 + s*.25)} H{f(x + s*.08)}" stroke="{DARK}" stroke-width="{f(s*.05)}"/>')
    # strmá strecha so šindľom
    rx0, rx1, ry = x - w/2 - s*.35, x + w/2 + s*.35, y - h + 2
    top = y - h - s * 1.5
    out.append(f'<path d="M{f(rx0)},{f(ry)} L{f(x)},{f(top)} L{f(rx1)},{f(ry)} Z" fill="{DARK}"/>')
    for k in range(1, 6):
        t = k / 6
        yy = top + (ry - top) * t
        hw = (rx1 - rx0) / 2 * t
        out.append(f'<line x1="{f(x - hw + 6)}" y1="{f(yy)}" x2="{f(x + hw - 6)}" y2="{f(yy)}" stroke="{CREAM}" stroke-width="{f(s*.045)}"/>')
    out.append(f'<rect x="{f(x + s*.5)}" y="{f(top + s*.35)}" width="{f(s*.25)}" height="{f(s*.6)}" fill="{DARK}"/>')
    return "".join(out)


def p04_linoryt():
    rnd = random.Random(40)
    s = svg_open("Javorníky — 04 Linoryt")
    s.append('<g clip-path="url(#panel)" filter="url(#rough2)">')
    s.append(f'<rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" fill="{DARK}"/>')

    # obloha — vyrezané vodorovné ťahy
    for i in range(60):
        y = rnd.uniform(PY + 20, 560)
        x = rnd.uniform(PX, PX + PW)
        L = rnd.uniform(20, 70)
        s.append(f'<path d="M{f(x)},{f(y)} l{f(L)},{f(rnd.uniform(-1.5,1.5))} l{f(-L*.1)},2.6 Z" fill="{CREAM}" opacity=".9"/>')

    # veľký javorový list — hrdzavý, ako slnko nad hrebeňom
    lp = maple_leaf_pts(560, 330, 230, rot=-8)
    s.append(f'<path d="{poly(lp)}" fill="{RUST}"/>')
    # žilnatina vyrezaná do listu
    for a, rr in [(82, .95), (24, .85), (140, .85), (-32, .55), (196, .55)]:
        t = math.radians(a)
        ex, ey = 560 + 230 * rr * math.cos(t), 330 - 230 * rr * math.sin(t)
        s.append(f'<path d="M560,330 L{f(ex)},{f(ey)}" stroke="{DARK}" stroke-width="5" stroke-linecap="round"/>')
        for k in range(1, 5):
            px_, py_ = 560 + (ex - 560) * k / 5, 330 + (ey - 330) * k / 5
            for side in (-1, 1):
                aa = t + side * 0.7
                L = 28 * (1 - k / 6)
                s.append(f'<path d="M{f(px_)},{f(py_)} l{f(L*math.cos(aa))},{f(-L*math.sin(aa))}" stroke="{DARK}" stroke-width="2.6" stroke-linecap="round"/>')
    s.append(f'<path d="M560,330 Q575,420 {f(560 + 34)},{f(330 + 150)}" stroke="{RUST}" stroke-width="9" stroke-linecap="round" fill="none"/>')

    # vzdialený hrebeň s krížmi
    far = ridge(610, [(250, 80, 170), (620, 30, 200), (860, 60, 140)], seed=17)
    s.append(f'<path d="{smooth_path(far, H)}" fill="{CREAM}"/>')
    s.append(gouges(rnd, far, 120, 30, DARK, slope_angle(far), width=3, below=(14, 140)))
    s.append(crosses(250, y_at(far, 250) + 3, 30, CREAM, gap=26))
    s.append(f'<path d="{smooth_path([(p[0], p[1] + 8) for p in far])}" stroke="{DARK}" stroke-width="3" fill="none"/>')

    # stredný kopec s drevenicou
    mid = ridge(790, [(180, 60, 180), (520, 130, 220), (900, 40, 150)], seed=19)
    s.append(f'<path d="{smooth_path(mid, H)}" fill="{DARK}"/>')
    s.append(f'<path d="{smooth_path(mid)}" stroke="{CREAM}" stroke-width="4" fill="none"/>')
    s.append(gouges(rnd, mid, 150, 34, CREAM, slope_angle(mid), width=3.2, below=(18, 170)))
    s.append(log_cabin(560, y_at(mid, 560) + 10, 50))
    # ploty a smreky
    for sx_ in [700, 735, 772]:
        s.append(spruce(sx_, y_at(mid, sx_) + 8, 26 + (sx_ % 3) * 6, CREAM))

    # predný svah s ovcou
    front = ridge(960, [(250, 70, 230), (780, 30, 200)], seed=23)
    s.append(f'<path d="{smooth_path(front, H)}" fill="{CREAM}"/>')
    s.append(gouges(rnd, front, 90, 44, DARK, slope_angle(front), width=4.5, below=(20, 120)))
    # ovca — vlna z krúžkov
    ox = 250
    oy = y_at(front, ox) + 80
    s.append(f'<ellipse cx="{ox}" cy="{oy - 42}" rx="92" ry="54" fill="{CREAM}" stroke="{DARK}" stroke-width="5"/>')
    for i in range(34):
        a = rnd.uniform(0, math.pi * 2)
        rr = rnd.uniform(0, 1) ** .5
        cx_, cy_ = ox + math.cos(a) * 70 * rr, oy - 42 + math.sin(a) * 36 * rr
        s.append(f'<circle cx="{f(cx_)}" cy="{f(cy_)}" r="{f(rnd.uniform(6, 10))}" fill="none" stroke="{DARK}" stroke-width="3"/>')
    for lx in (-50, -25, 30, 55):
        s.append(f'<rect x="{ox + lx - 5}" y="{f(oy - 2)}" width="11" height="42" fill="{DARK}"/>')
    s.append(f'<ellipse cx="{ox + 100}" cy="{oy - 64}" rx="30" ry="22" fill="{DARK}" stroke="{CREAM}" stroke-width="4" transform="rotate(25 {ox + 100} {oy - 64})"/>')
    s.append(f'<ellipse cx="{ox + 84}" cy="{oy - 84}" rx="14" ry="6" fill="{DARK}" transform="rotate(-30 {ox + 84} {oy - 84})"/>')
    s.append(f'<circle cx="{ox + 110}" cy="{oy - 70}" r="3.4" fill="{CREAM}"/>')
    # stopa v blate
    s.append(f'<path d="M{PX},{f(y_at(front, PX) + 150)} C300,1010 520,990 {PX + PW},{f(y_at(front, PX+PW) + 60)}" '
             f'stroke="{DARK}" stroke-width="7" stroke-dasharray="3 16" stroke-linecap="round" fill="none"/>')
    s.append("</g>")
    s.append(f'<rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" fill="none" stroke="{DARK}" stroke-width="6" filter="url(#rough2)"/>')

    s.append(text_block(
        "JAVORNÍKY",
        "LINORYT · DREVENICA · JAVOR · OVCA · TRI KRÍŽE",
        [
            "Hory pomenované po strome. Zruby, ktoré postavili ľudia s menom",
            "namiesto adresy. Ovce na klčoviskách a tri betónové kríže na Stratenci,",
            "ktoré pamätajú, že aj tento tichý hrebeň mal svoju vojnu.",
        ],
        "Ručne rezaná matrica  ·  Kopce a miesta  ·  A3",
    ))
    s.append(grain(0.15))
    write("04-linoryt.svg", s)


# ============================================================ 05 · BLATO

def sole_outline(n=160):
    """Obrys podrážky trailovky v lokálnych súradniciach (dĺžka 1, špička hore)."""
    pts = []
    for i in range(n):
        t = i / n * 2 * math.pi
        # y od -0.5 (päta) po 0.5 (špička)
        y = -0.5 * math.cos(t)
        u = y + 0.5  # 0 päta → 1 špička
        # šírka: päta 0.30, klenba 0.24, predná časť 0.37, špička sa zaobľuje
        w = 0.30 + 0.07 * math.exp(-((u - 0.7) / 0.17) ** 2) - 0.06 * math.exp(-((u - 0.4) / 0.1) ** 2)
        w *= math.sin(t) if True else 1
        # mierne asymetrická (palec)
        x = w * 0.5 + (0.03 * math.exp(-((u - 0.85) / 0.1) ** 2) if math.sin(t) > 0 else 0)
        pts.append((x, y))
    return pts


def p05_blato():
    rnd = random.Random(77)
    s = svg_open("Javorníky — 05 Blato")
    cx, cy, L, rot = 505, 490, 820, -14

    def tf(x, y):
        a = math.radians(rot)
        X, Y = x * L, -y * L
        return cx + X * math.cos(a) - Y * math.sin(a), cy + X * math.sin(a) + Y * math.cos(a)

    sole = [tf(x, y) for x, y in sole_outline()]
    s.append(f'<clipPath id="sole"><path d="{poly(sole)}"/></clipPath>')
    s.append('<g clip-path="url(#panel)">')

    # špliechance
    for _ in range(140):
        a = rnd.uniform(0, 2 * math.pi)
        d = rnd.uniform(260, 620) ** 1.0
        x, y = cx + math.cos(a) * d * 0.9, cy + math.sin(a) * d * 1.1
        r = rnd.uniform(1.5, 9) * (1.3 if rnd.random() < .1 else 1)
        s.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{RUST}" class="mul" opacity=".9"/>')

    # stopa: lugy (chevrony) + päta
    lugs = []
    y = 0.46
    row = 0
    while y > -0.08:
        for side in (-1, 1):
            off = 0.035 if row % 2 else 0.0
            x0 = side * (0.035 + off * 0.3)
            lugs.append([(x0, y), (x0 + side * 0.10, y - 0.035), (x0 + side * 0.10, y - 0.068), (x0, y - 0.033)])
            lugs.append([(x0 + side * 0.125, y - 0.042), (x0 + side * 0.2, y - 0.02), (x0 + side * 0.2, y - 0.05), (x0 + side * 0.125, y - 0.072)])
        y -= 0.068
        row += 1
    # klenba — pozdĺžne lugy
    for yy in (-0.12, -0.19):
        for side in (-1, 1):
            lugs.append([(side * 0.03, yy), (side * 0.12, yy - 0.01), (side * 0.12, yy - 0.05), (side * 0.03, yy - 0.04)])
    # päta — priečne bloky
    for yy in (-0.27, -0.34, -0.41):
        for side in (-1, 1):
            lugs.append([(side * 0.02, yy), (side * 0.16, yy + 0.012 * side), (side * 0.16, yy - 0.045), (side * 0.02, yy - 0.05)])

    def lug_path(q, jitter):
        pts = [tf(x + rnd.uniform(-jitter, jitter), y + rnd.uniform(-jitter, jitter)) for x, y in q]
        return poly(pts)

    # hrdzavá vrstva (blato) + tmavá cez multiply s posunom → hnedá, ktorá „nesedí“
    rust_lugs = "".join(f'<path d="{lug_path(q, .004)}"/>' for q in lugs if rnd.random() > .04)
    dark_lugs = "".join(f'<path d="{lug_path(q, .004)}"/>' for q in lugs if rnd.random() > .15)
    s.append(f'<g id="blato-hrdzava" fill="{RUST}" clip-path="url(#sole)" filter="url(#rough)">'
             f'<path d="{poly(sole)}" fill="url(#dotsR)"/>{rust_lugs}</g>')
    s.append(f'<g id="blato-tmava" class="mul" fill="{DARK}" opacity=".62" transform="translate(4 -3)" '
             f'clip-path="url(#sole)" filter="url(#rough2)">{dark_lugs}</g>')
    # rozmazaný okraj podrážky
    s.append(f'<path d="{poly(sole)}" fill="none" stroke="{RUST}" stroke-width="6" stroke-dasharray="40 14 8 22" filter="url(#rough)" class="mul"/>')

    # drobný profil trate vo vnútri — výškový graf 105 km (+4030 m)
    prof = []
    rp = random.Random(105)
    base_x, base_y, pw = 150, 985, 700
    for i in range(71):
        t = i / 70
        e = 0.45 + 0.28 * math.sin(t * math.pi * 3.1 + .4) + 0.18 * math.sin(t * math.pi * 7.3) + rp.uniform(-.04, .04)
        prof.append((base_x + pw * t, base_y - 55 * e))
    s.append(f'<path d="{smooth_path(prof)}" fill="none" stroke="{DARK}" stroke-width="2"/>')
    s.append(f'<text x="{base_x}" y="{base_y + 22}" class="mono" font-size="12" letter-spacing="2" fill="{DARK}">ČADCA</text>')
    s.append(f'<text x="{base_x + pw}" y="{base_y + 22}" class="mono" font-size="12" letter-spacing="2" fill="{DARK}" text-anchor="end">LYSÁ POD MAKYTOU</text>')
    s.append("</g>")

    s.append(text_block(
        "BLATO.",
        "JAVORNÍCKA STOVKA · 105 KM · +4030 M",
        [
            "Chotárne cesty rozryté lesnou technikou, október, dážď a sto päť kilometrov.",
            "Kto to bežal, spozná túto stopu okamžite. Kto nie, nepochopí —",
            "a presne preto je to odznak, nie dekorácia.",
        ],
        "10. 10. 2026  ·  Edícia pretekov  ·  A3",
        title_size=120, title_spacing=2,
    ))
    s.append(grain(0.14))
    write("05-blato.svg", s)


# ============================================================ 06 · MAPA SAMÔT

def p06_mapa():
    rnd = random.Random(900)
    s = svg_open("Javorníky — Bonus Mapa samôt", bg=DARK)
    s.append('<g clip-path="url(#panel)">')
    # hrebeň po hranici: SV (Čadca, hore) → JZ (Lysá pod Makytou, dole)
    ctrl = [(720, 120), (700, 230), (620, 320), (560, 430), (590, 520), (520, 610),
            (430, 690), (390, 790), (330, 880), (250, 960)]
    line = []
    for i in range(len(ctrl) - 1):
        (ax, ay), (bx, by) = ctrl[i], ctrl[i + 1]
        for k in range(10):
            t = k / 10
            line.append((ax + (bx - ax) * t, ay + (by - ay) * t))
    line.append(ctrl[-1])
    # ~900 samôt: husto na SK strane (JV od hrebeňa), riedko na CZ
    dots = []
    while len(dots) < 900:
        p = rnd.choice(line)
        i = line.index(p)
        q = line[min(i + 1, len(line) - 1)]
        tx, ty = q[0] - p[0], q[1] - p[1]
        n = math.hypot(tx, ty) or 1
        nx, ny = ty / n, -tx / n  # normála
        side = 1 if rnd.random() < 0.72 else -1
        d = abs(rnd.gauss(0, 95)) + 18
        # osady v údoliach — zhluky
        if rnd.random() < 0.5:
            d = 60 + (int(d) // 55) * 55 + rnd.gauss(0, 10)
        x = p[0] - nx * d * side + rnd.gauss(0, 12)
        y = p[1] - ny * d * side + rnd.gauss(0, 12)
        if PX + 10 < x < PX + PW - 10 and PY + 10 < y < PY + PH - 10:
            dots.append((x, y))
    s.append(f'<g fill="{CREAM}">' + "".join(
        f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(rnd.uniform(1.6, 3.0))}"/>' for x, y in dots) + "</g>")
    s.append(f'<path d="{smooth_path(ctrl)}" fill="none" stroke="{RUST}" stroke-width="3.2" stroke-linecap="round"/>')
    for name, (x, y), anchor, dx in [("Čadca", ctrl[0], "start", 16), ("Veľký Javorník", ctrl[4], "start", 18),
                                     ("Lysá pod Makytou", ctrl[-1], "end", -16)]:
        s.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{DARK}" stroke="{RUST}" stroke-width="3"/>')
        s.append(f'<text x="{x + dx}" y="{y + 5}" class="mono" font-size="14" letter-spacing="2" fill="{OCHRE}" text-anchor="{anchor}">{name.upper()}</text>')
    for lab, lx, ly in (("CZ", 300, 560), ("SK", 800, 700)):
        s.append(f'<text x="{lx}" y="{ly}" class="black" font-size="54" fill="{CREAM}" opacity=".16" text-anchor="middle">{lab}</text>')
    s.append("</g>")
    s.append(text_block(
        "MAPA SAMÔT",
        "900 BODIEK · JEDNA HREBEŇOVKA",
        [
            "Žiadny obrázok hory. Len miesta, kde niekto postavil dom tak ďaleko",
            "od ostatných, ako sa len dalo — a červená čiara, po ktorej sa medzi",
            "nimi dá prejsť za jeden deň. Ak máte nohy na sto päť kilometrov.",
        ],
        "Kopaničiarske osady  ·  Javorníky  ·  A3",
        ink=CREAM, accent=OCHRE, title_size=96, title_spacing=3,
    ))
    s.append(grain(0.08))
    write("06-bonus-mapa-samot.svg", s)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    p01_riso()
    p02_typo()
    p03_linka()
    p04_linoryt()
    p05_blato()
    p06_mapa()
