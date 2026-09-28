#!/usr/bin/env python3
"""Javorníky — séria 2 „maľba“: ilustrované cestovateľské plagáty cez celý formát.

Štýl: vzdušná perspektíva, dramatické svetlo, zrnitá textúra (speckle), malý centrovaný
nadpis dole + „SLOVENSKO“, pečiatka vpravo dole. Spusti: python3 generate_malba.py
"""
import math
import random

from generate import W, H, OUT, f, smooth_path, ridge, y_at, poly

M = 24  # biely okraj ako pri tlačenom printe
IX0, IY0, IX1, IY1 = M, M, W - M, H - M
FONTS = ("@import url('https://fonts.googleapis.com/css2?family=Jost:wght@500;600;700"
         "&family=IBM+Plex+Mono:wght@400;600&display=swap');")


class Poster:
    def __init__(self, title):
        self.title = title
        self.defs = []
        self.body = []
        self._id = 0

    def uid(self, p="g"):
        self._id += 1
        return f"{p}{self._id}"

    def lg(self, stops, x1=0, y1=0, x2=0, y2=1, user=None):
        """Lineárny gradient; stops = [(offset, farba[, opacita])]."""
        i = self.uid("lg")
        units = ""
        if user:
            x1, y1, x2, y2 = user
            units = ' gradientUnits="userSpaceOnUse"'
        st = "".join(
            f'<stop offset="{o}" stop-color="{c}"' + (f' stop-opacity="{s[0]}"' if s else "") + "/>"
            for o, c, *s in stops)
        self.defs.append(f'<linearGradient id="{i}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"{units}>{st}</linearGradient>')
        return f"url(#{i})"

    def rg(self, stops, cx, cy, r):
        i = self.uid("rg")
        st = "".join(
            f'<stop offset="{o}" stop-color="{c}"' + (f' stop-opacity="{s[0]}"' if s else "") + "/>"
            for o, c, *s in stops)
        self.defs.append(f'<radialGradient id="{i}" cx="{cx}" cy="{cy}" r="{r}" gradientUnits="userSpaceOnUse">{st}</radialGradient>')
        return f"url(#{i})"

    def add(self, *parts):
        self.body.extend(parts)

    def render(self, name, speck=0.5, light_speck=0.3, mottle=0.3):
        rnd = random.Random(99)
        dd = "".join(f'<circle cx="{f(rnd.uniform(0, 320))}" cy="{f(rnd.uniform(0, 320))}" r="{f(rnd.uniform(.3, .8))}"/>' for _ in range(1800))
        dl = "".join(f'<circle cx="{f(rnd.uniform(0, 320))}" cy="{f(rnd.uniform(0, 320))}" r="{f(rnd.uniform(.3, .75))}"/>' for _ in range(1300))
        self.defs.append(f'<pattern id="pD" width="320" height="320" patternUnits="userSpaceOnUse"><g fill="#15121c">{dd}</g></pattern>'
                         f'<pattern id="pL" width="320" height="320" patternUnits="userSpaceOnUse" patternTransform="rotate(37)"><g fill="#fffaf0">{dl}</g></pattern>')
        out = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="297mm" height="420mm">',
            f"<title>{self.title}</title>",
            f"<style>{FONTS}.jost{{font-family:Jost,'Futura','Century Gothic',sans-serif}}"
            ".mono{font-family:'IBM Plex Mono',monospace}</style>",
            "<defs>",
            f'<clipPath id="art"><rect x="{IX0}" y="{IY0}" width="{IX1 - IX0}" height="{IY1 - IY0}"/></clipPath>',
            # tmavé a svetlé zrnká — typická „speckle“ textúra
            '<filter id="speckD" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" '
            'baseFrequency="1.1" numOctaves="1" seed="3"/><feColorMatrix type="matrix" values="0 0 0 0 0.08  '
            '0 0 0 0 0.07  0 0 0 0 0.12  0 0 0 11 -6.6"/></filter>',
            '<filter id="speckL" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" '
            'baseFrequency="0.95" numOctaves="1" seed="11"/><feColorMatrix type="matrix" values="0 0 0 0 1  '
            '0 0 0 0 0.97  0 0 0 0 0.9  0 0 0 12 -7.4"/></filter>',
            # maliarska nerovnomernosť plôch
            '<filter id="mottle" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" '
            'baseFrequency="0.012 0.02" numOctaves="4" seed="5"/><feColorMatrix type="saturate" values="0"/></filter>',
            '<filter id="glow" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="3.5" result="b"/>'
            '<feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>',
            '<filter id="blur8" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="8"/></filter>',
            '<filter id="soft" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur stdDeviation="0.7"/></filter>',
            '<filter id="blur3" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>',
            '<filter id="blur20" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="20"/></filter>',
            '<filter id="rough" x="-2%" y="-2%" width="104%" height="104%"><feTurbulence type="fractalNoise" '
            'baseFrequency="0.05" numOctaves="2" seed="4"/><feDisplacementMap in="SourceGraphic" scale="5"/></filter>',
            *self.defs,
            "</defs>",
            f'<rect width="{W}" height="{H}" fill="#F7F2E8"/>',
            '<g clip-path="url(#art)">',
            *self.body,
            f'<rect width="{W}" height="{H}" filter="url(#mottle)" style="mix-blend-mode:overlay" opacity="{mottle}"/>',
            f'<rect width="{W}" height="{H}" fill="url(#pD)" opacity="{speck}"/>',
            f'<rect width="{W}" height="{H}" fill="url(#pL)" opacity="{light_speck}"/>',
            "</g>",
            "</svg>",
        ]
        (OUT / name).write_text("\n".join(out), encoding="utf-8")
        print("✓", name)


# ---------------------------------------------------------------- motívy

def title(p, text, sub, color, y=1318, size=50, spacing=5):
    p.add(f'<text x="{W/2}" y="{y}" class="jost" font-weight="600" font-size="{size}" letter-spacing="{spacing}" '
          f'text-anchor="middle" fill="{color}">{text}</text>',
          f'<text x="{W/2}" y="{y + 26}" class="jost" font-weight="600" font-size="12" letter-spacing="3.5" '
          f'text-anchor="middle" fill="{color}">{sub}</text>')
    # pečiatka — miesto pre tvoje logo
    cx, cy = IX1 - 52, IY1 - 48
    p.add(f'<g opacity=".9"><ellipse cx="{cx}" cy="{cy}" rx="24" ry="17" fill="none" stroke="{color}" stroke-width="2"/>'
          f'<path d="M{cx-15},{cy+6} q7,-12 13,-5 q6,-9 17,5" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round"/></g>')


def cloud(p, cx, cy, w, h, light, shade, seed=1, lit_from_below=False, opacity=1):
    """Kopovitý oblak: svetlá hmota + tieňová časť orezaná do tvaru."""
    rnd = random.Random(seed)
    n = max(4, int(w / (h * 0.55)))
    circles = []
    for i in range(n):
        t = (i + 0.5) / n
        r = h * (0.32 + 0.5 * math.sin(math.pi * t) ** 0.8) * rnd.uniform(0.8, 1.1)
        x = cx - w / 2 + w * t + rnd.uniform(-h * .1, h * .1)
        circles.append((x, cy - r * 0.55, r))
    base = f'<rect x="{f(cx - w/2)}" y="{f(cy - h*.3)}" width="{f(w)}" height="{f(h*.3)}" rx="{f(h*.15)}"/>'
    shape = base + "".join(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}"/>' for x, y, r in circles)
    cid = p.uid("cl")
    p.defs.append(f'<clipPath id="{cid}">{shape}</clipPath>')
    dy = 1 if lit_from_below else -1
    inner = "".join(
        f'<circle cx="{f(x - r*.1)}" cy="{f(y + dy * r*.3)}" r="{f(r*.88)}"/>' for x, y, r in circles)
    p.add(f'<g opacity="{opacity}"><g fill="{shade}">{shape}</g>'
          f'<g fill="{light}" clip-path="url(#{cid})">{inner}</g></g>')


def spruce(x, y, h, dark, light, tiers=5, seed=0):
    """Štylizovaný smrek z referencie — ovisnuté poschodia so zúbkami."""
    rnd = random.Random(seed)
    out = [f'<rect x="{f(x - h*.018)}" y="{f(y - h*.25)}" width="{f(h*.036)}" height="{f(h*.27)}" fill="{dark}"/>']
    for i in range(tiers):
        t0 = i / tiers
        yt = y - h + h * 0.9 * t0 - h * 0.04
        yb = y - h + h * 0.9 * (i + 1) / tiers + h * 0.08
        w = h * (0.1 + 0.2 * (i + 1) / tiers)
        teeth = 6 + i
        pts = [(x, yt)]
        pts.append((x + w * 0.35, yt + (yb - yt) * .5))
        for k in range(teeth + 1):
            tx = x + w - 2 * w * k / teeth
            pts.append((tx, yb + (h * .03 if k % 2 == 0 else -h * .025) + rnd.uniform(-2, 2)))
        pts.append((x - w * 0.35, yt + (yb - yt) * .5))
        out.append(f'<path d="{poly(pts)}" fill="{dark}"/>')
        lp = [(x, yt), (x - w * 0.35, yt + (yb - yt) * .5), (x - w * .9, yb - h * .01), (x - w * .15, yb - h * .03)]
        out.append(f'<path d="{poly(lp)}" fill="{light}" opacity=".85"/>')
    return "".join(out)


def crown(x, y, r, cols, seed=0, n=14):
    """Koruna listnáča ako zhluk ťahov — svetlo zľava hore."""
    rnd = random.Random(seed)
    out = []
    for layer, col in enumerate(cols):
        for _ in range(n):
            a = rnd.uniform(0, 2 * math.pi)
            d = rnd.uniform(0, r * 0.6)
            ox = x + math.cos(a) * d - layer * r * .12
            oy = y + math.sin(a) * d * .8 - layer * r * .14
            rr = r * rnd.uniform(0.32, 0.5) * (1 - layer * .2)
            out.append(f'<ellipse cx="{f(ox)}" cy="{f(oy)}" rx="{f(rr)}" ry="{f(rr*.85)}" fill="{col}"/>')
    return "".join(out)


def tree_row(pts, x0, x1, step, fn, rnd):
    out = []
    x = x0
    while x < x1:
        out.append(fn(x, y_at(pts, x), rnd))
        x += step * rnd.uniform(0.6, 1.3)
    return "".join(out)


def hill(p, pts, top, bottom, extra=""):
    ys = [q[1] for q in pts]
    g = p.lg([(0, top), (1, bottom)], user=(0, min(ys), 0, max(ys) + 260))
    p.add(f'<path d="{smooth_path(pts, H)}" fill="{g}" {extra}/>')


def grass(x, y, h, col, rnd, n=5):
    if y > 1225 and (270 < x < 730 or x > 890):  # voľno pre nadpis a pečiatku
        return ""
    out = []
    for _ in range(n):
        a = rnd.uniform(-0.5, 0.5)
        L = h * rnd.uniform(.6, 1)
        ex, ey = x + math.sin(a) * L, y - math.cos(a) * L
        cx_, cy_ = x + math.sin(a) * L * .2 + rnd.uniform(-4, 4), y - L * .6
        out.append(f'<path d="M{f(x - 2)},{f(y)} Q{f(cx_)},{f(cy_)} {f(ex)},{f(ey)} Q{f(cx_ + 3)},{f(cy_)} {f(x + 2)},{f(y)} Z" fill="{col}"/>')
    return "".join(out)


def fern(x, y, L, ang, col, leaf=None):
    """Papraď / halúzka — stonka s lístkami."""
    out = []
    a = math.radians(ang)
    ex, ey = x + math.cos(a) * L, y - math.sin(a) * L
    out.append(f'<path d="M{f(x)},{f(y)} L{f(ex)},{f(ey)}" stroke="{col}" stroke-width="3" stroke-linecap="round"/>')
    for k in range(1, 9):
        t = k / 9
        px_, py_ = x + (ex - x) * t, y + (ey - y) * t
        ll = L * 0.28 * (1 - t * .7)
        for s in (-1, 1):
            b = a + s * 0.9
            qx, qy = px_ + math.cos(b) * ll, py_ - math.sin(b) * ll
            out.append(f'<path d="M{f(px_)},{f(py_)} Q{f((px_+qx)/2 + s*3)},{f((py_+qy)/2 - 4)} {f(qx)},{f(qy)} '
                       f'Q{f((px_+qx)/2 - s*2)},{f((py_+qy)/2 + 3)} {f(px_)},{f(py_)} Z" fill="{leaf or col}"/>')
    return "".join(out)


def stars(p, n, y0, y1, seed=1, col="#fff6e0"):
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x = rnd.uniform(IX0, IX1)
        y = y0 + (y1 - y0) * rnd.random() ** 1.4
        r = rnd.uniform(0.6, 1.9) if rnd.random() > .05 else rnd.uniform(2.2, 3)
        out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{col}" opacity="{f(rnd.uniform(.35, 1))}"/>')
    p.add("".join(out))


def lights(pts, xs, dy, col, r=2.6):
    return "".join(f'<rect x="{f(x - r)}" y="{f(y_at(pts, x) + dy - r)}" width="{f(r*2)}" height="{f(r*1.6)}" fill="{col}" filter="url(#glow)"/>'
                   for x in xs)


# =================================================== 07 · STRATENEC (hrdinský pohľad)

def cross3d(x, yb, h, sw, span, arm_y, face, face2, side, crack, seed):
    """Betónový kríž v podhľade — svetlá čelná plocha, tmavý bok, spodok ramena v tieni."""
    rnd = random.Random(seed)
    d = sw * 0.3  # hĺbka boku
    out = []
    # bok drieku a ramena
    out.append(f'<path d="M{f(x + sw/2)},{f(yb - h)} l{f(d)},{f(d*.5)} V{f(yb)} h{f(-d)} Z" fill="{side}"/>')
    out.append(f'<path d="M{f(x + span/2)},{f(arm_y)} l{f(d)},{f(d*.5)} v{f(sw*.9)} h{f(-d)} Z" fill="{side}"/>')
    # spodok ramien (podhľad)
    out.append(f'<path d="M{f(x - span/2)},{f(arm_y + sw*.9)} h{f(span)} l{f(d)},{f(d*.5)} h{f(-span)} Z" fill="{side}"/>')
    # čelo
    out.append(f'<rect x="{f(x - sw/2)}" y="{f(yb - h)}" width="{f(sw)}" height="{f(h)}" fill="{face}"/>')
    out.append(f'<rect x="{f(x - span/2)}" y="{f(arm_y)}" width="{f(span)}" height="{f(sw*.9)}" fill="{face}"/>')
    # tieňové plochy na čele (fazety ako na Jánošíkovi)
    out.append(f'<path d="M{f(x + sw*.1)},{f(yb - h)} h{f(sw*.4)} V{f(yb)} h{f(-sw*.25)} Z" fill="{face2}"/>')
    out.append(f'<path d="M{f(x - span/2)},{f(arm_y + sw*.55)} h{f(span)} v{f(sw*.35)} h{f(-span)} Z" fill="{face2}"/>')
    # praskliny a škáry
    for _ in range(3):
        cx_ = x + rnd.uniform(-sw*.4, sw*.4)
        cy_ = rnd.uniform(yb - h, yb)
        out.append(f'<path d="M{f(cx_)},{f(cy_)} l{f(rnd.uniform(-8,8))},{f(rnd.uniform(10,30))} l{f(rnd.uniform(-6,6))},{f(rnd.uniform(6,18))}" '
                   f'stroke="{crack}" stroke-width="1.4" fill="none" opacity=".7"/>')
    for k in range(1, 6):
        yy = yb - h * k / 6
        out.append(f'<line x1="{f(x - sw/2)}" y1="{f(yy)}" x2="{f(x + sw/2)}" y2="{f(yy)}" stroke="{crack}" stroke-width="1" opacity=".35"/>')
    return "".join(out)


def p07_stratenec():
    p = Poster("Stratenec")
    rnd = random.Random(7)
    NAVY, NAVY2 = "#1f3150", "#34507a"
    GOLD1, GOLD2 = "#e8b93c", "#c78d22"
    sky = p.lg([(0, "#2a78bd"), (.55, "#62aede"), (1, "#cfe7ea")], user=(0, 0, 0, 800))
    p.add(f'<rect width="{W}" height="{H}" fill="{sky}"/>')
    for i, y in enumerate(range(520, 640, 22)):  # jemné vodorovné pruhy pri horizonte
        p.add(f'<rect x="0" y="{y}" width="{W}" height="6" fill="#ffffff" opacity="{.08 + i*.02}"/>')
    for cx, cy, w, h, s in [(180, 170, 330, 90, 1), (760, 120, 260, 70, 2), (880, 330, 220, 60, 3),
                            (120, 430, 260, 55, 4), (640, 440, 200, 45, 5), (420, 80, 160, 40, 6)]:
        cloud(p, cx, cy, w, h, "#f6f8f4", "#b6d0e2", seed=s)
    # vzdialené oblé Javorníky
    far = ridge(700, [(160, 90, 170), (520, 60, 200), (850, 110, 150)], seed=3, x0=0, x1=W)
    hill(p, far, "#9fb3bf", "#c9d9dc")
    mid = ridge(780, [(90, 70, 190), (420, 40, 180), (900, 90, 160)], seed=4, x0=0, x1=W)
    hill(p, mid, "#6f8c9d", "#9db3ba")
    p.add(tree_row(mid, 0, W, 9, lambda x, y, r: spruce(x, y + 12, r.uniform(20, 32), "#3f5a72", "#57748c", tiers=3, seed=int(x)), rnd))
    # zlaté lúky
    m2 = ridge(900, [(150, 150, 230), (820, 170, 220)], seed=5, x0=0, x1=W)
    hill(p, m2, GOLD1, GOLD2)
    for x0, x1 in ((20, 180), (760, 900)):
        p.add(tree_row(m2, x0, x1, 16, lambda x, y, r: spruce(x, y + 30, r.uniform(34, 52), NAVY, NAVY2, tiers=4, seed=int(x)), rnd))
    # rozhľadňa za krížmi
    tx, tb = 760, 850
    p.add(f'<g stroke="#5b6b7a" stroke-width="3" fill="none"><path d="M{tx-22},{tb} L{tx-10},{tb-190} M{tx+22},{tb} L{tx+10},{tb-190}'
          f' M{tx-20},{tb-20} L{tx+17},{tb-80} M{tx+20},{tb-20} L{tx-17},{tb-80} M{tx-16},{tb-80} L{tx+13},{tb-140} M{tx+16},{tb-80} L{tx-13},{tb-140}"/></g>'
          f'<rect x="{tx-24}" y="{tb-208}" width="48" height="18" fill="#5b6b7a"/><path d="M{tx-30},{tb-208} L{tx},{tb-232} L{tx+30},{tb-208} Z" fill="#4a5968"/>')
    # hrebeň s krížmi
    crest = ridge(1060, [(500, 150, 330)], seed=6, x0=0, x1=W)
    hill(p, crest, "#f0c64a", "#b97f1f")
    CF = p.lg([(0, "#e6dccb"), (1, "#b9ad98")], user=(0, 300, 0, 980))
    CF2, CS, CK = "#a99d88", "#26385a", "#6d6456"
    # tiene krížov na tráve
    for x, w in ((270, 150), (730, 150), (500, 200)):
        p.add(f'<ellipse cx="{x + 60}" cy="{y_at(crest, x) + 62}" rx="{w}" ry="16" fill="#8a5a14" opacity=".35"/>')
    for x, yb, h, sw, span, ay in ((270, 950, 470, 60, 250, 600), (730, 950, 470, 60, 250, 600), (500, 940, 640, 78, 330, 430)):
        p.add(cross3d(x, yb, h, sw, span, ay, CF, CF2, CS, CK, x))
        w = sw * 2.1
        p.add(f'<path d="M{f(x - w/2 + 8)},{yb} H{f(x + w/2 - 8)} L{f(x + w/2)},{yb + 55} H{f(x - w/2)} Z" fill="#c5b9a3"/>'
              f'<path d="M{f(x + w/2 - 8)},{yb} l16,8 l0,50 l-8,-3 Z" fill="{CS}"/>'
              f'<rect x="{f(x - w/2)}" y="{yb + 30}" width="{f(w)}" height="25" fill="{CF2}"/>')
    # popredie: smreky a tráva
    for x, hh in ((40, 470), (140, 360), (-20, 300), (870, 380), (970, 480), (790, 260)):
        p.add(spruce(x, 1250, hh, NAVY, NAVY2, tiers=7, seed=x + 50))
    fg = ridge(1215, [(250, 40, 260), (760, 30, 260)], seed=9, x0=0, x1=W)
    hill(p, fg, GOLD1, "#d49c2a")
    for x in range(40, 980, 70):
        p.add(grass(x + rnd.uniform(-20, 20), 1330 + rnd.uniform(0, 50), rnd.uniform(40, 70), NAVY, rnd, n=3))
    title(p, "STRATENEC", "1055 M · JAVORNÍKY · SLOVENSKO", NAVY, y=1300)
    p.render("07-stratenec.svg", speck=.45, light_speck=.35)


# ========================================================= 08 · KOPANICE (súmrak)

def cabin(x, y, s, wall, wall2, roof, rim, win):
    """Drevenica v podvečer — svietiace okná, lemové svetlo na streche."""
    w, h = s * 2.4, s * 1.15
    out = [f'<rect x="{f(x - w/2)}" y="{f(y - h)}" width="{f(w)}" height="{f(h)}" fill="{wall}"/>']
    for i in range(8):
        yy = y - h + (i + .5) * h / 8
        out.append(f'<line x1="{f(x - w/2)}" y1="{f(yy)}" x2="{f(x + w/2)}" y2="{f(yy)}" stroke="{wall2}" stroke-width="{f(s*.05)}"/>')
    # štít
    out.append(f'<path d="M{f(x - w/2 - s*.3)},{f(y - h)} L{f(x - w*.15)},{f(y - h - s*1.3)} L{f(x + w/2 + s*.3)},{f(y - h - s*1.3)} '
               f'L{f(x + w/2 + s*.55)},{f(y - h)} Z" fill="{roof}"/>')
    out.append(f'<path d="M{f(x - w/2 - s*.3)},{f(y - h)} L{f(x - w*.15)},{f(y - h - s*1.3)} L{f(x + w/2 + s*.3)},{f(y - h - s*1.3)}" '
               f'fill="none" stroke="{rim}" stroke-width="{f(s*.06)}" stroke-linejoin="round"/>')
    out.append(f'<rect x="{f(x + w*.22)}" y="{f(y - h - s*1.75)}" width="{f(s*.26)}" height="{f(s*.6)}" fill="{roof}"/>')
    for wx in (x - w*.34, x - w*.02):
        out.append(f'<rect x="{f(wx)}" y="{f(y - h*.72)}" width="{f(s*.42)}" height="{f(s*.42)}" fill="{win}" filter="url(#glow)"/>'
                   f'<path d="M{f(wx + s*.21)},{f(y - h*.72)} v{f(s*.42)} M{f(wx)},{f(y - h*.72 + s*.21)} h{f(s*.42)}" stroke="{wall}" stroke-width="{f(s*.05)}"/>')
    # otvorené dvere + svetlo na zemi
    dx = x + w * .3
    out.append(f'<rect x="{f(dx)}" y="{f(y - h*.82)}" width="{f(s*.4)}" height="{f(h*.82)}" fill="{win}"/>')
    out.append(f'<path d="M{f(dx)},{f(y)} h{f(s*.4)} l{f(s*.9)},{f(s*.9)} h{f(-s*1.3)} Z" fill="{win}" opacity=".35"/>')
    return "".join(out)


def p08_kopanice():
    p = Poster("Kopanice")
    rnd = random.Random(8)
    sky = p.lg([(0, "#18203f"), (.35, "#34366a"), (.62, "#a8607f"), (.8, "#ee9f86"), (1, "#f7d2a6")], user=(0, 0, 0, 760))
    p.add(f'<rect width="{W}" height="{H}" fill="{sky}"/>')
    stars(p, 120, IY0, 300, seed=8)
    for cx, cy, w, h, s, o in [(260, 150, 520, 120, 1, 1), (820, 230, 420, 100, 2, 1), (180, 400, 360, 70, 3, .9),
                               (700, 470, 300, 55, 4, .85), (520, 330, 260, 50, 5, .9)]:
        cloud(p, cx, cy, w, h, "#f39a98", "#272b55", seed=s, lit_from_below=True, opacity=o)
    far = ridge(700, [(200, 80, 200), (600, 50, 200), (900, 90, 150)], seed=31, x0=0, x1=W)
    hill(p, far, "#6a5287", "#8a6a95")
    p.add(lights(far, [140, 330, 520, 610, 790, 880], 18, "#ffd98a", 1.8))
    mid = ridge(830, [(120, 90, 180), (480, 110, 230), (860, 60, 180)], seed=32, x0=0, x1=W)
    hill(p, mid, "#46365f", "#3a2c50")
    p.add(tree_row(mid, 560, 1000, 9, lambda x, y, r: spruce(x, y + 10, r.uniform(22, 34), "#2c2342", "#3e3158", tiers=3, seed=int(x)), rnd))
    p.add(lights(mid, [210, 300, 420, 470], 25, "#ffd98a", 2.2))
    near = ridge(1010, [(250, 90, 260), (760, 130, 250)], seed=33, x0=0, x1=W)
    hill(p, near, "#3a2b49", "#1e1729")
    # buk vľavo
    for x, hh in ((120, 420), (210, 330), (40, 300)):
        p.add(spruce(x, 1030, hh, "#1f1830", "#6b4467", tiers=7, seed=x))
    # cesta k drevenici
    p.add(f'<path d="M430,{H} C470,1250 560,1150 610,1060 C630,1020 640,1000 650,985 L690,985 C690,1010 700,1060 740,1110 C800,1190 800,1300 820,{H} Z" fill="#6b5570" opacity=".9"/>')
    p.add(cabin(640, 985, 62, "#2f2230", "#3f2e3e", "#1c1422", "#f19a8e", "#ffd27a"))
    # dym
    p.add(f'<path d="M712,828 C690,790 740,770 720,730 S760,670 740,630" stroke="#d99aa6" stroke-width="10" fill="none" stroke-linecap="round" opacity=".5" filter="url(#blur8)"/>')
    # plot
    for i, x in enumerate(range(420, 560, 26)):
        yy = 990 + i * 6
        p.add(f'<rect x="{x}" y="{yy - 44}" width="6" height="46" fill="#1a1322"/>')
    p.add(f'<path d="M420,960 L560,990 M420,975 L560,1005" stroke="#1a1322" stroke-width="4"/>')
    # bežec s čelovkou na ceste
    rx, ry = 555, 1140
    p.add(f'<path d="M{rx+6},{ry-62} L{rx+150},{ry-150} L{rx+190},{ry-60} Z" fill="#ffe7a6" opacity=".2"/>'
          f'<g fill="#150f1c"><circle cx="{rx}" cy="{ry-62}" r="9"/><path d="M{rx-7},{ry-52} l14,0 l4,34 l-8,2 l-4,-10 l-10,26 l-10,-4 l10,-30 Z"/>'
          f'<path d="M{rx-2},{ry-18} l18,30 l-8,4 l-14,-26 Z"/><path d="M{rx+4},{ry-48} l20,16 l-4,6 l-18,-12 Z"/></g>'
          f'<circle cx="{rx-7}" cy="{ry-64}" r="3" fill="#fff4c6" filter="url(#glow)"/>')
    for x in range(40, 980, 55):
        p.add(grass(x + rnd.uniform(-15, 15), H - 20, rnd.uniform(40, 70), "#140e1b", rnd, n=3))
    title(p, "KOPANICE", "JAVORNÍKY · SLOVENSKO", "#f6dcc2", y=1300)
    p.render("08-kopanice.svg", speck=.35, light_speck=.28)


# ===================================================== 09 · BUČINA (3 farby, plošne)

def lynx(x, y, s, body, dark, light):
    """Rys sediaci na kmeni — strapce na ušiach, golier, krátky chvost."""
    return (
        f'<path d="M{f(x - s*.9)},{f(y)} C{f(x - s*1.1)},{f(y - s*.9)} {f(x - s*.5)},{f(y - s*1.5)} {f(x + s*.1)},{f(y - s*1.4)} '
        f'C{f(x + s*.6)},{f(y - s*1.3)} {f(x + s*.7)},{f(y - s*.5)} {f(x + s*.55)},{f(y)} Z" fill="{body}"/>'
        f'<path d="M{f(x - s*.95)},{f(y - s*.2)} q{f(-s*.35)},{f(-s*.05)} {f(-s*.3)},{f(-s*.35)} l{f(s*.1)},{f(-s*.05)} z" fill="{dark}"/>'
        # hlava
        f'<ellipse cx="{f(x + s*.35)}" cy="{f(y - s*1.65)}" rx="{f(s*.42)}" ry="{f(s*.36)}" fill="{body}"/>'
        f'<path d="M{f(x - s*.05)},{f(y - s*1.55)} l{f(-s*.18)},{f(s*.35)} l{f(s*.25)},{f(-s*.12)} Z" fill="{light}"/>'
        f'<path d="M{f(x + s*.75)},{f(y - s*1.55)} l{f(s*.18)},{f(s*.35)} l{f(-s*.25)},{f(-s*.12)} Z" fill="{light}"/>'
        f'<path d="M{f(x + s*.08)},{f(y - s*1.9)} l{f(-s*.02)},{f(-s*.42)} l{f(s*.22)},{f(s*.3)} Z" fill="{body}"/>'
        f'<path d="M{f(x + s*.6)},{f(y - s*1.9)} l{f(s*.04)},{f(-s*.42)} l{f(-s*.22)},{f(s*.3)} Z" fill="{body}"/>'
        f'<path d="M{f(x + s*.06)},{f(y - s*2.32)} v{f(-s*.18)} M{f(x + s*.64)},{f(y - s*2.32)} v{f(-s*.18)}" stroke="{dark}" stroke-width="{f(s*.05)}"/>'
        f'<circle cx="{f(x + s*.2)}" cy="{f(y - s*1.72)}" r="{f(s*.05)}" fill="{dark}"/><circle cx="{f(x + s*.5)}" cy="{f(y - s*1.72)}" r="{f(s*.05)}" fill="{dark}"/>'
        f'<path d="M{f(x + s*.3)},{f(y - s*1.56)} h{f(s*.1)} l{f(-s*.05)},{f(s*.06)} z" fill="{dark}"/>'
        # škvrny
        + "".join(f'<circle cx="{f(x + dx*s)}" cy="{f(y - dy*s)}" r="{f(s*.06)}" fill="{dark}"/>'
                  for dx, dy in [(-.5, .5), (-.3, .8), (-.6, .9), (-.1, .4), (0, 1), (.2, .6), (-.4, .25), (.3, .3)])
        # predné laby
        + f'<rect x="{f(x + s*.15)}" y="{f(y - s*.9)}" width="{f(s*.16)}" height="{f(s*.9)}" fill="{body}"/>'
        f'<rect x="{f(x + s*.38)}" y="{f(y - s*.9)}" width="{f(s*.16)}" height="{f(s*.9)}" fill="{body}"/>'
    )


def p09_bucina():
    p = Poster("Bučina")
    rnd = random.Random(9)
    TEAL, CORAL, NAVY, CREAM = "#6ba7a3", "#e5735b", "#1e2a47", "#f2e6cf"
    p.add(f'<rect width="{W}" height="{H}" fill="{TEAL}"/>')
    p.add(f'<circle cx="500" cy="250" r="50" fill="{CORAL}"/>' +
          "".join(f'<circle cx="500" cy="250" r="{r}" fill="none" stroke="{CORAL}" stroke-width="2" opacity=".6"/>' for r in (66, 76)))
    for cx, cy, w, h, s in [(360, 330, 150, 34, 1), (660, 300, 170, 38, 2)]:
        cloud(p, cx, cy, w, h, CREAM, "#cfe0d8", seed=s)
    # vzdialený hrebeň — koralová bučina
    far = ridge(470, [(300, 70, 200), (700, 50, 200)], seed=41, x0=0, x1=W)
    p.add(f'<path d="{smooth_path(far, H)}" fill="{CORAL}"/>')
    p.add(tree_row(far, 0, W, 13, lambda x, y, r: f'<ellipse cx="{f(x)}" cy="{f(y + 4)}" rx="{f(r.uniform(9,13))}" ry="{f(r.uniform(12,18))}" fill="{CORAL}"/>', rnd))
    # tmavý les so smrekmi
    mid = ridge(560, [(160, 60, 200), (840, 70, 200)], seed=42, x0=0, x1=W)
    p.add(f'<path d="{smooth_path(mid, H)}" fill="{NAVY}"/>')
    p.add(tree_row(mid, 0, W, 11, lambda x, y, r: spruce(x, y + 14, r.uniform(34, 54), NAVY, NAVY, tiers=4, seed=int(x)), rnd))
    # lúč svetla cez les
    p.add(f'<path d="M430,560 L570,560 L700,{H} L300,{H} Z" fill="{TEAL}" opacity=".18"/>')
    # blatistá chotárna cesta
    p.add(f'<path d="M200,{H} C320,1230 560,1100 480,940 C430,840 520,720 492,600 L510,600 C560,720 500,840 545,940 C650,1110 560,1250 780,{H} Z" fill="{TEAL}"/>')
    p.add(f'<path d="M330,{H} C420,1240 560,1110 500,950 C470,860 520,720 500,610" stroke="{NAVY}" stroke-width="5" fill="none" opacity=".45"/>'
          f'<path d="M640,{H} C600,1240 610,1110 560,950 C530,860 525,720 506,610" stroke="{NAVY}" stroke-width="5" fill="none" opacity=".45"/>')
    for (cx, cy, rx, ry) in [(450, 1200, 80, 15), (590, 1150, 40, 8), (525, 990, 38, 8), (495, 780, 18, 4)]:
        p.add(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{CREAM}" opacity=".9"/>')
    # bežec v diaľke
    bx, by = 500, 740
    p.add(f'<g fill="{CORAL}"><circle cx="{bx}" cy="{by - 30}" r="5"/><path d="M{bx-4},{by-25} h8 l3,16 l6,12 -4,2 -7,-10 -6,12 -4,-2 5,-14 Z"/></g>')
    # jeleň
    dx, dy = 650, 700
    p.add(f'<g fill="{CORAL}"><ellipse cx="{dx}" cy="{dy-24}" rx="22" ry="11"/><rect x="{dx-18}" y="{dy-18}" width="4" height="20"/><rect x="{dx+12}" y="{dy-18}" width="4" height="20"/>'
          f'<path d="M{dx+16},{dy-30} l10,-18 l8,2 l-6,20 Z"/></g>'
          f'<path d="M{dx+30},{dy-48} l-6,-14 M{dx+30},{dy-48} l6,-16 M{dx+27},{dy-55} l-8,-4 M{dx+33},{dy-58} l8,-5" stroke="{CORAL}" stroke-width="2.4"/>')
    # kmene bukov — hladká sivá kôra, rozšírené korene
    for x, w, s in [(70, 96, 1), (215, 52, 2), (330, 30, 3), (672, 32, 4), (790, 58, 5), (935, 110, 6)]:
        p.add(f'<path d="M{x - w*.9},{H} C{x - w*.5},{H-80} {x - w*.45},{H-200} {x - w*.4},{900} C{x - w*.35},600 {x - w*.3},300 {x - w*.3},0 '
              f'H{x + w*.3} C{x + w*.3},300 {x + w*.35},600 {x + w*.4},900 C{x + w*.45},{H-200} {x + w*.5},{H-80} {x + w*.9},{H} Z" fill="{NAVY}"/>')
        p.add(f'<path d="M{x - w*.28},0 C{x - w*.25},400 {x - w*.3},900 {x - w*.3},{H} H{x - w*.12} C{x - w*.12},900 {x - w*.1},400 {x - w*.12},0 Z" fill="{TEAL}" opacity=".6"/>')
        r2 = random.Random(s)
        for _ in range(int(w / 6)):
            yy = r2.uniform(150, 1250)
            p.add(f'<path d="M{f(x - w*.25)},{f(yy)} q{f(w*.25)},-5 {f(w*.45)},0" stroke="{CREAM}" stroke-width="1.6" fill="none" opacity=".45"/>')
    # koruna — koralové masy s lístkami
    for _ in range(18):
        x = rnd.uniform(-60, W + 60)
        y = rnd.uniform(-60, 150) if not (360 < x < 640) else rnd.uniform(-120, -10)
        p.add(f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(rnd.uniform(90, 150))}" ry="{f(rnd.uniform(55, 90))}" fill="{CORAL}"/>')
    for _ in range(140):
        x = rnd.uniform(0, W)
        y = rnd.uniform(0, 190) if not (360 < x < 640) else rnd.uniform(0, 60)
        a = rnd.uniform(0, 180)
        col = rnd.choice([NAVY, CREAM, "#c95a45"])
        p.add(f'<path d="M0,0 q7,-9 16,0 q-9,9 -16,0 Z" fill="{col}" opacity=".75" transform="translate({f(x)} {f(y)}) rotate({f(a)})"/>')
    # padajúce lístie
    for _ in range(26):
        x, y = rnd.uniform(IX0, IX1), rnd.uniform(220, 1100)
        p.add(f'<path d="M0,0 q5,-7 12,0 q-7,7 -12,0 Z" fill="{CORAL}" transform="translate({f(x)} {f(y)}) rotate({f(rnd.uniform(0,180))})"/>')
    # rys na padnutom kmeni
    p.add(f'<path d="M20,1150 L380,1115 L388,1165 L20,1200 Z" fill="{CORAL}"/>'
          f'<path d="M20,1172 L384,1140" stroke="#c95a45" stroke-width="4"/>'
          f'<ellipse cx="384" cy="1140" rx="13" ry="26" fill="{CREAM}"/><ellipse cx="384" cy="1140" rx="6" ry="12" fill="{CORAL}"/>')
    p.add(lynx(215, 1135, 74, CREAM, NAVY, TEAL))
    for x, a, L in [(40, 70, 190), (100, 100, 150), (880, 110, 210), (950, 80, 170), (820, 70, 150), (660, 95, 90), (300, 85, 80)]:
        p.add(fern(x, H - 30, L, a, CORAL))
    title(p, "BUČINA", "JAVORNÍKY · SLOVENSKO", CREAM, y=1305)
    p.render("09-bucina.svg", speck=.3, light_speck=.3, mottle=.18)


# ================================================= 10 · VEĽKÝ JAVORNÍK (more hmly)

def p10_velky_javornik():
    p = Poster("Veľký Javorník")
    rnd = random.Random(10)
    sky = p.lg([(0, "#e7deae"), (.6, "#f3eccb"), (1, "#f8f3dc")], user=(0, 0, 0, 600))
    p.add(f'<rect width="{W}" height="{H}" fill="{sky}"/>')
    p.add(f'<circle cx="250" cy="420" r="260" fill="{p.rg([(0, "#fffbe6", .95), (1, "#fffbe6", 0)], 250, 420, 260)}"/>')
    for cx, cy, w, h, s in [(200, 130, 460, 130, 1), (760, 90, 520, 150, 2), (560, 250, 380, 90, 3)]:
        cloud(p, cx, cy, w, h, "#fbf6df", "#e0d6a8", seed=s, opacity=.9)
    layers = [(430, "#c3d5c6", "#dfe6d2"), (490, "#a6c2b8", "#cfdccd"), (555, "#88aba7", "#b8cdc3"),
              (630, "#6b9493", "#9fbcb4"), (720, "#557f82", "#86a8a3")]
    for i, (base, c1, c2) in enumerate(layers):
        pts = ridge(base, [(rnd.uniform(0, W), rnd.uniform(30, 70), rnd.uniform(120, 220)) for _ in range(4)], seed=50 + i, x0=0, x1=W)
        hill(p, pts, c1, c2)
        if i >= 2:
            p.add(tree_row(pts, 0, W, 7, lambda x, y, r, i=i: spruce(x, y + 8, r.uniform(10, 16) * (i - 1), c1, c2, tiers=3, seed=int(x)), rnd))
        # hmla medzi vrstvami
        p.add(f'<ellipse cx="{rnd.uniform(200, 800)}" cy="{base + 40}" rx="600" ry="{30 + i*6}" fill="#fbf8ea" opacity=".75" filter="url(#blur20)"/>')
    for cx, cy, w, h, s in [(120, 760, 300, 80, 7), (430, 700, 220, 60, 8)]:
        cloud(p, cx, cy, w, h, "#fdfbf0", "#dfe3d4", seed=s)
    # vtáky
    for bx, by in [(150, 560), (180, 585), (205, 570)]:
        p.add(f'<path d="M{bx},{by} q6,-5 10,0 q4,-5 10,0" stroke="#3b4b45" stroke-width="2" fill="none"/>')
    # popredný vrchol — oblá lúka s čučoriedkami
    summit = [(IX0 - 10, 1100), (150, 980), (350, 860), (520, 770), (650, 735), (800, 730), (980, 745), (1010, 750)]
    hill(p, summit, "#a2b04a", "#2e4a26")
    greens = [("#253d20", "#3f5d28", "#6f8a33"), ("#2f4a24", "#56722c", "#93a83a"),
              ("#3a5426", "#7d9536", "#c4bf4c"), ("#44602a", "#9aab3e", "#e0d15a")]
    reds = [("#5e2418", "#a63d2b", "#d9683a")]
    clumps = []
    for _ in range(620):
        x = rnd.uniform(-20, W + 20)
        ytop = y_at(summit, min(max(x, IX0), 1000))
        depth = rnd.random() ** 1.3
        y = ytop + 10 + depth * 680
        clumps.append((y, x, depth))
    for y, x, depth in sorted(clumps):
        r = 4 + depth * 26 * rnd.uniform(.7, 1.2)
        c = rnd.choice(reds) if rnd.random() < .05 else rnd.choice(greens if depth > .25 else greens[2:])
        # ker = zhluk drobných lístkových ťahov, nie guľa
        parts = []
        for k in range(5):
            ox, oy = x + rnd.uniform(-r, r), y + rnd.uniform(-r * .3, r * .3)
            rr = r * rnd.uniform(.45, .75)
            parts.append((ox, oy, rr))
        p.add("".join(f'<ellipse cx="{f(ox)}" cy="{f(oy)}" rx="{f(rr*1.3)}" ry="{f(rr*.7)}" fill="{c[0]}"/>' for ox, oy, rr in parts))
        p.add("".join(f'<ellipse cx="{f(ox - rr*.2)}" cy="{f(oy - rr*.25)}" rx="{f(rr*1.0)}" ry="{f(rr*.5)}" fill="{c[1]}"/>' for ox, oy, rr in parts))
        p.add("".join(f'<ellipse cx="{f(ox - rr*.45)}" cy="{f(oy - rr*.4)}" rx="{f(rr*.45)}" ry="{f(rr*.22)}" fill="{c[2]}"/>' for ox, oy, rr in parts[:3]))
    # svetlejšia plošina vrcholu s chodníkom
    p.add(f'<path d="M560,760 C640,740 800,738 1000,748 L1000,770 C820,760 700,770 580,790 Z" fill="#c8c46a" opacity=".8"/>')
    # rázcestník + bežci na vrchole
    sx, sy = 700, 752
    p.add(f'<rect x="{sx}" y="{sy - 70}" width="5" height="72" fill="#3a2f22"/>'
          f'<path d="M{sx+5},{sy-66} h30 l6,6 -6,6 h-30 Z M{sx},{sy-50} h-30 l-6,6 6,6 h30 Z" fill="#e8e0c8" stroke="#3a2f22" stroke-width="1.5"/>'
          f'<path d="M{sx+5},{sy-66} h30 l6,6 -6,6 h-30 Z" fill="#c64a32"/>')
    for fx, arms in [(780, True), (810, False), (838, True)]:
        fy = 750
        arm = (f'<path d="M{fx-3},{fy-40} l-9,-16 M{fx+3},{fy-40} l9,-16" stroke="#1f2a24" stroke-width="3.5" stroke-linecap="round"/>' if arms else
               f'<path d="M{fx-3},{fy-36} l-7,12 M{fx+3},{fy-36} l7,12" stroke="#1f2a24" stroke-width="3.5" stroke-linecap="round"/>')
        p.add(f'<g fill="#1f2a24"><circle cx="{fx}" cy="{fy-50}" r="5"/><path d="M{fx-5},{fy-44} h10 l2,26 h-14 Z"/>'
              f'<path d="M{fx-6},{fy-18} h5 v18 h-5 Z M{fx+1},{fy-18} h5 v18 h-5 Z"/></g>' + arm)
    title(p, "VEĽKÝ JAVORNÍK", "1072 M · JAVORNÍKY · SLOVENSKO", "#f5efd7", y=1300)
    p.render("10-velky-javornik.svg", speck=.3, light_speck=.3)


# =================================================== 11 · NOC NA HREBENI (čelovky)

def p11_noc():
    p = Poster("Noc na hrebeni")
    rnd = random.Random(11)
    sky = p.lg([(0, "#080d24"), (.5, "#16244d"), (1, "#35507e")], user=(0, 0, 0, 820))
    p.add(f'<rect width="{W}" height="{H}" fill="{sky}"/>')
    p.add(f'<path d="M-50,420 C200,260 600,180 1050,40 L1050,160 C640,300 260,380 -50,520 Z" fill="#8fa6d6" opacity=".12" filter="url(#blur20)"/>')
    stars(p, 420, IY0, 760, seed=3)
    # mesiac
    p.add(f'<circle cx="790" cy="200" r="120" fill="{p.rg([(0, "#fff3cf", .35), (1, "#fff3cf", 0)], 790, 200, 120)}"/>'
          f'<mask id="moon"><rect width="{W}" height="{H}" fill="#fff"/><circle cx="810" cy="188" r="42" fill="#000"/></mask>'
          f'<circle cx="790" cy="200" r="46" fill="#f8ecc6" mask="url(#moon)"/>')
    ridges = []
    cols = [("#2f4674", "#233760"), ("#243963", "#1b2c52"), ("#1a2b50", "#132142"), ("#111c38", "#0c142b"), ("#0a1022", "#070b18")]
    bases = [700, 790, 900, 1040, 1180]
    for i, (base, (c1, c2)) in enumerate(zip(bases, cols)):
        bumps = [(rnd.uniform(0, W), rnd.uniform(40, 90) * (1 + i*.3), rnd.uniform(140, 260)) for _ in range(3)]
        if i == 4:
            bumps = [(620, 110, 420)]
        pts = ridge(base, bumps, seed=60 + i, x0=0, x1=W)
        ridges.append(pts)
        hill(p, pts, c1, c2)
        if i in (1, 2, 3):
            p.add(tree_row(pts, 0, W, 12 + i * 6, lambda x, y, r, i=i: spruce(x, y + 6 + i * 3, r.uniform(14, 24) * i, c2, c1, tiers=3 + i, seed=int(x)), rnd))
        # reťaz čeloviek po hrebeni tejto vrstvy
        if i < 4:
            span = [(120, 520), (430, 900), (60, 560), (380, 760)][i]
            n = [16, 13, 10, 5][i]
            for k in range(n):
                x = span[0] + (span[1] - span[0]) * (k + rnd.uniform(-.25, .25)) / n
                y = y_at(pts, x) + 6 + i * 4
                r = 1.4 + i * 1.1
                p.add(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="#fff2bf" filter="url(#glow)"/>')
    # bežec v popredí so svetelným kužeľom
    near = ridges[-1]
    rx = 640
    ry = y_at(near, rx) + 4
    beam = p.lg([(0, "#fff3c4", .5), (1, "#fff3c4", 0)], user=(rx - 10, 0, rx - 300, 0))
    p.add(f'<path d="M{rx-8},{ry-80} L{rx-300},{ry-45} L{rx-290},{ry+14} Z" fill="{beam}"/>')
    p.add(f'<ellipse cx="{rx-230}" cy="{f(y_at(near, rx-230)+6)}" rx="70" ry="9" fill="#fff3c4" opacity=".18" filter="url(#blur8)"/>')
    p.add(f'<g fill="#05070f"><circle cx="{rx}" cy="{ry-80}" r="11"/>'
          f'<path d="M{rx-9},{ry-68} h18 l4,40 l-10,2 l-6,-12 l-12,30 l-12,-5 l12,-35 Z"/>'
          f'<path d="M{rx-2},{ry-26} l20,26 l-9,5 l-16,-24 Z"/><path d="M{rx+6},{ry-62} l24,18 l-5,7 l-22,-14 Z"/></g>'
          f'<path d="M{rx+28},{ry-46} L{rx+44},{ry+2} M{rx-10},{ry-54} L{rx-34},{ry+2}" stroke="#05070f" stroke-width="3"/>'
          f'<circle cx="{rx-9}" cy="{ry-82}" r="3.5" fill="#fffbe0" filter="url(#glow)"/>')
    title(p, "NOC NA HREBENI", "105 KM · +4030 M · JAVORNÍKY", "#e9e3cf", y=1300)
    p.render("11-noc-na-hrebeni.svg", speck=.2, light_speck=.22)


# ======================================================= 12 · MAKYTA (seno, ovce)

def haystack(x, y, s, c1, c2, c3, seed):
    """Kopa sena okolo ostrve (kôl trčí hore) — typické pre Kysuce a Javorníky."""
    rnd = random.Random(seed)
    out = [f'<rect x="{f(x - s*.035)}" y="{f(y - s*1.72)}" width="{f(s*.07)}" height="{f(s*.4)}" fill="#3a2b1c"/>']
    body = (f'M{f(x - s*.5)},{f(y)} C{f(x - s*.55)},{f(y - s*.45)} {f(x - s*.35)},{f(y - s*1.0)} {f(x - s*.12)},{f(y - s*1.32)} '
            f'Q{f(x)},{f(y - s*1.42)} {f(x + s*.12)},{f(y - s*1.32)} C{f(x + s*.35)},{f(y - s*1.0)} {f(x + s*.55)},{f(y - s*.45)} {f(x + s*.5)},{f(y)} Z')
    cid = f"hs{seed}"
    out.append(f'<clipPath id="{cid}"><path d="{body}"/></clipPath>')
    out.append(f'<path d="{body}" fill="{c1}"/>')
    out.append(f'<g clip-path="url(#{cid})"><path d="M{f(x + s*.05)},{f(y - s*1.5)} C{f(x + s*.2)},{f(y - s*.9)} {f(x + s*.15)},{f(y - s*.4)} {f(x + s*.2)},{f(y)} H{f(x + s)} V{f(y - s*1.5)} Z" fill="{c2}"/>')
    for _ in range(110):  # ťahy sena smerom dole
        t = rnd.uniform(0.05, 1)
        yy = y - s * 1.35 * (1 - t)
        xx = x + rnd.uniform(-s * .55, s * .55)
        L = rnd.uniform(10, 26) * s / 200
        out.append(f'<path d="M{f(xx)},{f(yy)} q{f(rnd.uniform(-4, 4))},{f(L*.5)} {f(rnd.uniform(-6, 6))},{f(L)}" stroke="{rnd.choice([c3, "#e8c569"])}" stroke-width="{f(rnd.uniform(1.2, 2.4))}" fill="none" opacity=".75"/>')
    out.append(f'<path d="M{f(x - s*.52)},{f(y - s*.12)} Q{f(x)},{f(y - s*.02)} {f(x + s*.52)},{f(y - s*.12)} L{f(x + s*.5)},{f(y)} H{f(x - s*.5)} Z" fill="{c3}" opacity=".6"/></g>')
    out.append(f'<ellipse cx="{f(x + s*.35)}" cy="{f(y + 4)}" rx="{f(s*.65)}" ry="{f(s*.07)}" fill="#7a4f14" opacity=".35"/>')
    return "".join(out)


def sheep2(x, y, s, wool, shade, head, flip=False):
    k = -1 if flip else 1
    return (f'<rect x="{f(x - s*.4)}" y="{f(y - s*.25)}" width="{f(s*.1)}" height="{f(s*.3)}" fill="{head}"/>'
            f'<rect x="{f(x + s*.25)}" y="{f(y - s*.25)}" width="{f(s*.1)}" height="{f(s*.3)}" fill="{head}"/>'
            f'<ellipse cx="{f(x)}" cy="{f(y - s*.45)}" rx="{f(s*.6)}" ry="{f(s*.36)}" fill="{wool}"/>'
            f'<ellipse cx="{f(x)}" cy="{f(y - s*.33)}" rx="{f(s*.55)}" ry="{f(s*.2)}" fill="{shade}"/>'
            f'<ellipse cx="{f(x + k*s*.62)}" cy="{f(y - s*.55)}" rx="{f(s*.18)}" ry="{f(s*.13)}" fill="{head}"/>')


def p12_makyta():
    p = Poster("Makyta")
    rnd = random.Random(12)
    NAVY, NAVY2 = "#1f3150", "#34507a"
    sky = p.lg([(0, "#2d7cc0"), (.6, "#71b8df"), (1, "#d6ebe8")], user=(0, 0, 0, 650))
    p.add(f'<rect width="{W}" height="{H}" fill="{sky}"/>')
    for cx, cy, w, h, s in [(230, 200, 420, 120, 1), (800, 150, 380, 110, 2), (560, 360, 300, 70, 3), (120, 470, 200, 45, 4)]:
        cloud(p, cx, cy, w, h, "#f7f9f4", "#b8d1e2", seed=s)
    far = ridge(610, [(300, 80, 220), (760, 130, 160)], seed=71, x0=0, x1=W)
    hill(p, far, "#8ea9ba", "#b9ccd2")
    p.add(tree_row(far, 0, W, 8, lambda x, y, r: spruce(x, y + 10, r.uniform(12, 18), "#7b98ab", "#9cb5c3", tiers=3, seed=int(x)), rnd))
    # jesenná bučina na strednom svahu — husté koruny
    mid = ridge(760, [(150, 110, 220), (600, 60, 200), (900, 90, 160)], seed=72, x0=0, x1=W)
    hill(p, mid, "#a9502a", "#7e3a22")
    rows = []
    for _ in range(1100):
        x = rnd.uniform(-10, W + 10)
        y = y_at(mid, min(max(x, 0), W)) + 8 + rnd.random() ** 1.5 * 150
        rows.append((y, x))
    for y, x in sorted(rows):
        r = rnd.uniform(6, 11) * (1 + (y - y_at(mid, min(max(x, 0), W))) / 300)
        c = rnd.choice([("#8e3f22", "#c96a2b", "#eaa23e"), ("#9a4a1f", "#dc8a2f", "#f3c44e"), ("#7a3520", "#b8552a", "#e0873a")])
        p.add(f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(r)}" ry="{f(r*1.1)}" fill="{c[0]}"/>'
              f'<ellipse cx="{f(x - r*.2)}" cy="{f(y - r*.25)}" rx="{f(r*.75)}" ry="{f(r*.8)}" fill="{c[1]}"/>'
              f'<ellipse cx="{f(x - r*.35)}" cy="{f(y - r*.45)}" rx="{f(r*.3)}" ry="{f(r*.3)}" fill="{c[2]}" opacity=".8"/>')
    for gx in (140, 420, 610, 880):
        p.add(tree_row(mid, gx - 40, gx + 40, 16, lambda x, y, r: spruce(x, y + r.uniform(40, 110), r.uniform(40, 60), NAVY, NAVY2, tiers=4, seed=int(x)), rnd))
    p.add(tree_row(mid, 99999, 0, 12, lambda x, y, r: spruce(x, y + 60, r.uniform(50, 70), NAVY, NAVY2, tiers=4, seed=int(x)), rnd))
    # zlatá lúka s drevenicou a ovcami
    meadow = ridge(940, [(250, 110, 260), (800, 60, 240)], seed=73, x0=0, x1=W)
    hill(p, meadow, "#eec150", "#cf9528")
    hx = 760
    hy = y_at(meadow, hx) + 30
    p.add(f'<rect x="{hx-40}" y="{hy-36}" width="80" height="36" fill="#6b4a2c"/><rect x="{hx+10}" y="{hy-36}" width="30" height="36" fill="#4d3420"/>'
          f'<path d="M{hx-50},{hy-34} L{hx},{hy-80} L{hx+50},{hy-34} Z" fill="#3c2c22"/><rect x="{hx-26}" y="{hy-26}" width="12" height="12" fill="#f4dd92"/>')
    flock = sorted((y_at(meadow, sx) + 50 + rnd.uniform(0, 120), sx) for sx in [rnd.uniform(420, 700) for _ in range(16)])
    for sy, sx in flock:
        p.add(sheep2(sx, sy, 16 + (sy - 900) * .06, "#f4efe2", "#d8cdb6", "#2a2622", flip=rnd.random() < .5))
    # popredie — kopy sena na ostrvách
    fg = ridge(1150, [(250, 70, 300), (820, 40, 250)], seed=74, x0=0, x1=W)
    hill(p, fg, "#e6b43e", "#b37a1c")
    for x, s, sd in [(330, 150, 3), (160, 250, 1), (880, 290, 4)]:
        p.add(haystack(x, y_at(fg, x) + s * .5, s, "#d6a843", "#a57a2e", "#6e5024", sd))
    for x in range(30, 990, 40):
        p.add(grass(x + rnd.uniform(-15, 15), H - 20 - rnd.uniform(0, 80), rnd.uniform(35, 75), NAVY, rnd, n=3))
    title(p, "MAKYTA", "JAVORNÍKY · SLOVENSKO", NAVY, y=1300)
    p.render("12-makyta.svg", speck=.4, light_speck=.35)


if __name__ == "__main__":
    p07_stratenec()
    p08_kopanice()
    p09_bucina()
    p10_velky_javornik()
    p11_noc()
    p12_makyta()
