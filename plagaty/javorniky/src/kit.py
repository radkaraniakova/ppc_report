"""Ilustrátorská sada tvarov pre sériu „maľba“ — stromy, postavy, oblaky, svetlo, textúry.

Všetko je čistý SVG vektor: každý motív sa dá v Illustratori/Procreate rozobrať po vrstvách.
"""
import math
import random

from generate import W, H, f, smooth_path, y_at, poly


def clip(p, d):
    cid = p.uid("cp")
    p.defs.append(f'<clipPath id="{cid}"><path d="{d}"/></clipPath>')
    return cid


def slope(pts, x):
    return math.atan2(y_at(pts, x + 6) - y_at(pts, x - 6), 12)


def dab(x, y, L, w, a, col, op=None):
    """Jeden ťah štetcom — zúžený na oboch koncoch."""
    dx, dy = math.cos(a) * L, math.sin(a) * L
    nx, ny = -math.sin(a) * w / 2, math.cos(a) * w / 2
    o = f' opacity="{f(op)}"' if op is not None else ""
    return (f'<path d="M{f(x)},{f(y)} Q{f(x + dx/2 + nx)},{f(y + dy/2 + ny)} {f(x + dx)},{f(y + dy)} '
            f'Q{f(x + dx/2 - nx)},{f(y + dy/2 - ny)} {f(x)},{f(y)}Z" fill="{col}"{o}/>')


def leaf(x, y, L, w, a_deg, col, vein=None):
    s = (f'<path d="M0,0 Q{f(L*.45)},{f(-w)} {f(L)},0 Q{f(L*.45)},{f(w)} 0,0Z" fill="{col}" '
         f'transform="translate({f(x)} {f(y)}) rotate({f(a_deg)})"/>')
    if vein:
        s += (f'<path d="M0,0 L{f(L*.85)},0" stroke="{vein}" stroke-width="{f(max(.6, w*.18))}" '
              f'transform="translate({f(x)} {f(y)}) rotate({f(a_deg)})"/>')
    return s


# ------------------------------------------------------------------ plochy

def hill(p, pts, top, bottom, depth=300, tex=None, n=0, L=16, wid=3.0, op=.35, rim=None, rim_w=3.0,
         rim_op=.9, seed=0, span=None):
    """Kopec: gradient + ťahy po vrstevnici + lemové svetlo na hrane."""
    d = smooth_path(pts, H)
    ys = [q[1] for q in pts]
    g = p.lg([(0, top), (1, bottom)], user=(0, min(ys), 0, min(ys) + depth))
    p.add(f'<path d="{d}" fill="{g}"/>')
    if tex and n:
        rnd = random.Random(seed)
        cid = clip(p, d)
        x0, x1 = span or (pts[0][0], pts[-1][0])
        out = []
        for _ in range(n):
            x = rnd.uniform(x0, x1)
            y = y_at(pts, x) + rnd.random() ** 1.3 * depth
            out.append(dab(x, y, L * rnd.uniform(.5, 1.4), wid * rnd.uniform(.6, 1.3),
                           slope(pts, x) + rnd.uniform(-.15, .15), rnd.choice(tex)))
        p.add(f'<g clip-path="url(#{cid})" opacity="{op}">' + "".join(out) + "</g>")
    if rim:
        cid = clip(p, d)
        p.add(f'<path d="{smooth_path(pts)}" fill="none" stroke="{rim}" stroke-width="{f(rim_w * 2)}" '
              f'opacity="{rim_op}" clip-path="url(#{cid})"/>')
    return d


def glow(p, cx, cy, r, col, op=1.0):
    g = p.rg([(0, col, op), (.35, col, op * .45), (1, col, 0)], cx, cy, r)
    p.add(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{g}"/>')


def rays(p, cx, cy, angles, L, col, op=.12, width=.05):
    out = []
    for a in angles:
        a = math.radians(a)
        dw = width * (0.6 + (hash(round(a, 3)) % 7) / 7)
        pts = [(cx, cy), (cx + math.cos(a - dw) * L, cy + math.sin(a - dw) * L),
               (cx + math.cos(a + dw) * L, cy + math.sin(a + dw) * L)]
        out.append(f'<path d="{poly(pts)}" fill="{col}"/>')
    p.add(f'<g opacity="{op}" filter="url(#blur8)">' + "".join(out) + "</g>")


def fog(p, x, y, w, h, col, op=.7, blur="blur20"):
    p.add(f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(w/2)}" ry="{f(h/2)}" fill="{col}" opacity="{op}" filter="url(#{blur})"/>')


def cloud(p, cx, cy, w, h, light, mid, shade, seed=1, below=False, flat=1.0, op=1.0, tex=True):
    """Maliarsky kopovitý oblak: tieň → stred → svetlo, s ťahmi štetca."""
    rnd = random.Random(seed)
    n = max(5, int(w / (h * .42)))
    cs = []
    for i in range(n):
        t = (i + .5) / n
        r = h * (.22 + .55 * math.sin(math.pi * t) ** .7) * rnd.uniform(.75, 1.15)
        cs.append((cx - w/2 + w*t + rnd.uniform(-h*.15, h*.15), cy - r * .45 * flat, r))
    for _ in range(n // 2):
        r = h * rnd.uniform(.22, .42)
        cs.append((cx + rnd.uniform(-w*.28, w*.28), cy - h * rnd.uniform(.5, .9) * flat, r))
    base = f'<rect x="{f(cx - w/2)}" y="{f(cy - h*.28)}" width="{f(w)}" height="{f(h*.28)}" rx="{f(h*.14)}"/>'
    shape = base + "".join(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}"/>' for x, y, r in cs)
    cid = p.uid("cl")
    p.defs.append(f'<clipPath id="{cid}">{shape}</clipPath>')
    dy = 1 if below else -1
    mid_s = "".join(f'<circle cx="{f(x - r*.08)}" cy="{f(y + dy*r*.2)}" r="{f(r*.92)}"/>' for x, y, r in cs)
    lit_s = "".join(f'<circle cx="{f(x - r*.2)}" cy="{f(y + dy*r*.42)}" r="{f(r*.72)}"/>' for x, y, r in cs)
    strokes = ""
    if tex:
        for _ in range(int(w / 5)):
            x = cx + rnd.uniform(-w/2, w/2)
            y = cy - rnd.uniform(0, h * 1.1)
            strokes += dab(x, y, rnd.uniform(8, 22), rnd.uniform(1.5, 3.5), rnd.uniform(-.2, .2),
                           rnd.choice([light, mid]), .55)
    p.add(f'<g opacity="{op}" filter="url(#soft)"><g fill="{shade}">{shape}</g>'
          f'<g clip-path="url(#{cid})"><g fill="{mid}">{mid_s}</g><g fill="{light}">{lit_s}</g>{strokes}</g></g>')


def wisp(p, x, y, w, h, col, op=.5):
    p.add(f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(w/2)}" ry="{f(h/2)}" fill="{col}" opacity="{op}" filter="url(#blur8)"/>')


def stars(p, n, box, seed=1, col="#fff6e0", band=None):
    """Hviezdy; band = (x0, y0, x1, y1, šírka) → hustejší pás Mliečnej cesty."""
    rnd = random.Random(seed)
    x0, y0, x1, y1 = box
    out = []
    for i in range(n):
        if band and i < n * .55:
            bx0, by0, bx1, by1, bw = band
            t = rnd.random()
            x = bx0 + (bx1 - bx0) * t + rnd.gauss(0, bw * .5)
            y = by0 + (by1 - by0) * t + rnd.gauss(0, bw * .5)
            r = rnd.uniform(.35, 1.1)
        else:
            x, y = rnd.uniform(x0, x1), y0 + (y1 - y0) * rnd.random() ** 1.3
            r = rnd.uniform(.5, 1.7)
        out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{col}" opacity="{f(rnd.uniform(.3, 1))}"/>')
    for _ in range(n // 60):  # jasné hviezdy so štyrmi lúčmi
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1 * .8)
        s = rnd.uniform(4, 8)
        out.append(f'<path d="M{f(x)},{f(y-s)} Q{f(x)},{f(y)} {f(x+s)},{f(y)} Q{f(x)},{f(y)} {f(x)},{f(y+s)} '
                   f'Q{f(x)},{f(y)} {f(x-s)},{f(y)} Q{f(x)},{f(y)} {f(x)},{f(y-s)}Z" fill="{col}" filter="url(#glow)"/>')
    p.add("".join(out))


# ------------------------------------------------------------------ stromy

def spruce_simple(x, y, h, dark, light=None, seed=0):
    """Vzdialený smrek — zúbkovaná silueta, svetlá ľavá polovica."""
    rnd = random.Random(seed)
    w = h * .3
    pts = [(x, y - h)]
    k = 4
    for i in range(1, k + 1):
        t = i / k
        pts.append((x + w * t * .55, y - h + h * t * .92 - h * .06))
        pts.append((x + w * t, y - h + h * t * .92 + rnd.uniform(-1, 1)))
    pts += [(x, y)]
    left = [(2 * x - px, py) for px, py in reversed(pts[1:-1])]
    s = f'<path d="{poly(pts + left)}" fill="{dark}"/>'
    if light:
        s += f'<path d="{poly([(x, y - h)] + left[len(left)//2:] + [(x, y - h * .1)])}" fill="{light}" opacity=".7"/>'
    return s


def spruce(x, y, h, dark, mid, light, seed=0, lit=-1, rim=None, rim_w=1.6):
    """Smrek vetva po vetve: ovisnuté konáre so zdvihnutými koncami, svetlo z boku `lit`."""
    if h < 34:
        return spruce_simple(x, y, h, dark, mid, seed)
    rnd = random.Random(seed)
    n = int(max(8, min(26, h / 10)))
    top = y - h
    out = [f'<path d="M{f(x - h*.012)},{f(y)} L{f(x - h*.006)},{f(top)} L{f(x + h*.006)},{f(top)} L{f(x + h*.012)},{f(y)}Z" fill="{dark}"/>']
    branches = []
    for i in range(n):
        t = (i + 1) / n
        yb = top + h * .93 * t - h * .02
        env = h * .32 * t ** .8 * (.8 + .35 * rnd.random())
        th = h * .075 * (.5 + t)
        for side in (-1, 1):
            L = env * rnd.uniform(.78, 1.1)
            droop = L * rnd.uniform(.4, .65)
            branches.append((i, side, yb, L, droop, th))
    rim_parts = []
    for i, side, yb, L, droop, th in sorted(branches, key=lambda b: -b[0]):  # zdola nahor
        tipx, tipy = x + side * L, yb + droop
        top_pts = []
        for k in range(9):
            s = k / 8
            top_pts.append((x + side * L * s, yb - th * .35 + (droop + th * .35) * s ** 1.6))
        curl = (tipx + side * L * .07, tipy - th * .75)
        under = []
        m = max(4, int(L / 6))
        for k in range(m + 1):
            s = 1 - k / m
            px_ = x + side * L * s
            py_ = yb + th * .45 + (droop - th * .1) * s ** 1.4
            under.append((px_, py_ + (th * .38 if k % 2 else 0) * s))
        shape = top_pts + [curl] + under
        out.append(f'<path d="{poly(shape)}" fill="{dark}"/>')
        band = top_pts + [curl] + [(px_, py_ + th * .45) for px_, py_ in reversed(top_pts)]
        if side == lit:
            out.append(f'<path d="{poly(band)}" fill="{mid}"/>')
            for _ in range(int(L / 9)):
                s = rnd.uniform(.35, 1)
                bx, by = x + side * L * s, yb + (droop) * s ** 1.6 - th * .1
                out.append(dab(bx, by, th * rnd.uniform(.5, .9), th * .22, math.radians(rnd.uniform(60, 120)), light, .9))
        else:
            thin = top_pts + [(px_, py_ + th * .16) for px_, py_ in reversed(top_pts)]
            out.append(f'<path d="{poly(thin)}" fill="{mid}" opacity=".45"/>')
        if rim:
            rim_parts.append(f'M{f(top_pts[3][0])},{f(top_pts[3][1])} ' + " ".join(f'L{f(a)},{f(b)}' for a, b in top_pts[4:]) + f' L{f(curl[0])},{f(curl[1])}')
    out.append(f'<path d="M{f(x)},{f(top - h*.04)} L{f(x + h*.022)},{f(top + h*.07)} L{f(x - h*.022)},{f(top + h*.07)}Z" fill="{dark}"/>')
    if rim:
        out.append(f'<path d="{" ".join(rim_parts)}" fill="none" stroke="{rim}" stroke-width="{rim_w}" stroke-linecap="round" opacity=".45"/>')
    return "".join(out)


def beech(x, y, h, trunk, cols, seed=0, lit=-1, rim=None, leafy=True):
    """Buk: štíhly kmeň s konármi, koruna z lalokov (tieň → stred → svetlo → akcent)."""
    rnd = random.Random(seed)
    dark, mid, light, acc = cols
    tw = h * .045
    ct = y - h * .62
    out = [f'<path d="M{f(x - tw)},{f(y)} C{f(x - tw*.7)},{f(y - h*.3)} {f(x - tw*.5)},{f(ct)} {f(x - tw*.3)},{f(ct - h*.1)} '
           f'L{f(x + tw*.3)},{f(ct - h*.1)} C{f(x + tw*.5)},{f(ct)} {f(x + tw*.7)},{f(y - h*.3)} {f(x + tw)},{f(y)}Z" fill="{trunk}"/>']
    for s in (-1, 1):
        out.append(f'<path d="M{f(x)},{f(y - h*.45)} Q{f(x + s*h*.08)},{f(y - h*.6)} {f(x + s*h*.2)},{f(y - h*.72)}" '
                   f'stroke="{trunk}" stroke-width="{f(tw*.7)}" fill="none" stroke-linecap="round"/>')
    R = h * .36
    cy = y - h * .66
    lobes = [(x + rnd.uniform(-R*.55, R*.55), cy + rnd.uniform(-R*.5, R*.45), R * rnd.uniform(.38, .55)) for _ in range(7)]
    lobes.append((x, cy - R * .35, R * .5))
    lx, ly = lit * .35, -.4
    for col, sc, off, cnt in ((dark, 1.0, 0, 6), (mid, .8, .35, 5), (light, .5, .7, 3)):
        for bx, by, br in lobes:
            for _ in range(cnt):
                a = rnd.uniform(0, 2*math.pi)
                d = rnd.uniform(0, br * .5)
                rr = br * sc * rnd.uniform(.5, .75)
                out.append(f'<ellipse cx="{f(bx + math.cos(a)*d + lx*br*off)}" cy="{f(by + math.sin(a)*d*.8 + ly*br*off)}" '
                           f'rx="{f(rr)}" ry="{f(rr*.85)}" fill="{col}"/>')
    if leafy:  # okrajové lístky a akcenty
        for _ in range(int(h * .6)):
            bx, by, br = rnd.choice(lobes)
            a = rnd.uniform(0, 2*math.pi)
            d = br * rnd.uniform(.85, 1.15)
            out.append(leaf(bx + math.cos(a)*d, by + math.sin(a)*d*.85, h*.028, h*.011, rnd.uniform(0, 360),
                            rnd.choice([dark, mid, acc])))
        for _ in range(int(h * .25)):
            bx, by, br = rnd.choice(lobes)
            out.append(f'<circle cx="{f(bx + rnd.uniform(-br, br)*.7 + lx*br*.6)}" cy="{f(by + rnd.uniform(-br, br)*.6 + ly*br*.6)}" '
                       f'r="{f(h*rnd.uniform(.006, .014))}" fill="{acc}"/>')
    return "".join(out)


def crowns(p, pts, depth, count, palettes, size, seed=0, span=None, clip_d=None):
    """Hustý listnatý les na svahu — malé koruny zoradené odzadu dopredu."""
    rnd = random.Random(seed)
    x0, x1 = span or (pts[0][0], pts[-1][0])
    items = []
    for _ in range(count):
        x = rnd.uniform(x0, x1)
        t = rnd.random() ** 1.4
        y = y_at(pts, x) + 4 + t * depth
        items.append((y, x, t))
    out = []
    for y, x, t in sorted(items):
        r = size * rnd.uniform(.7, 1.2) * (1 + t * .7)
        c = rnd.choice(palettes)
        out.append(f'<ellipse cx="{f(x + r*.5)}" cy="{f(y + r*.2)}" rx="{f(r*.7)}" ry="{f(r*.7)}" fill="{c[0]}"/>'
                   f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(r)}" ry="{f(r*1.12)}" fill="{c[0]}"/>'
                   f'<ellipse cx="{f(x - r*.22)}" cy="{f(y - r*.28)}" rx="{f(r*.72)}" ry="{f(r*.78)}" fill="{c[1]}"/>'
                   f'<ellipse cx="{f(x - r*.42)}" cy="{f(y - r*.52)}" rx="{f(r*.32)}" ry="{f(r*.3)}" fill="{c[2]}"/>')
    g = "".join(out)
    if clip_d:
        g = f'<g clip-path="url(#{clip(p, clip_d)})">{g}</g>'
    p.add(g)


def tree_row(pts, x0, x1, step, fn, rnd, dy=0):
    out = []
    x = x0
    while x < x1:
        out.append(fn(x, y_at(pts, x) + dy, rnd))
        x += step * rnd.uniform(.55, 1.35)
    return "".join(out)


# ------------------------------------------------------------------ rastliny

def tuft(x, y, h, cols, rnd, n=7, lean=0.0):
    out = []
    for _ in range(n):
        a = rnd.uniform(-.55, .55) + lean
        L = h * rnd.uniform(.5, 1)
        ex, ey = x + math.sin(a) * L, y - math.cos(a) * L
        cx_, cy_ = x + math.sin(a) * L * .25 + rnd.uniform(-3, 3), y - L * .55
        w = rnd.uniform(1.5, 3.2)
        out.append(f'<path d="M{f(x - w)},{f(y)} Q{f(cx_)},{f(cy_)} {f(ex)},{f(ey)} Q{f(cx_ + w*.6)},{f(cy_)} {f(x + w)},{f(y)}Z" fill="{rnd.choice(cols)}"/>')
    return "".join(out)


def rowan(x0, y0, x1, y1, s, stem, leaf_cols, berry, berry_hi, seed=0, bend=0.25):
    """Jarabina — pierovité listy a strapce červených bobúľ."""
    rnd = random.Random(seed)
    mx, my = (x0 + x1) / 2 + (y1 - y0) * bend, (y0 + y1) / 2 - (x1 - x0) * bend
    out = [f'<path d="M{f(x0)},{f(y0)} Q{f(mx)},{f(my)} {f(x1)},{f(y1)}" stroke="{stem}" stroke-width="{f(s*.05)}" fill="none" stroke-linecap="round"/>']
    berries = []
    for k in range(1, 8):
        t = k / 8
        bx = (1-t)**2*x0 + 2*(1-t)*t*mx + t*t*x1
        by = (1-t)**2*y0 + 2*(1-t)*t*my + t*t*y1
        tx = 2*(1-t)*(mx-x0) + 2*t*(x1-mx)
        ty = 2*(1-t)*(my-y0) + 2*t*(y1-my)
        base = math.atan2(ty, tx)
        side = 1 if k % 2 else -1
        a = base + side * rnd.uniform(.6, 1.0)
        L = s * rnd.uniform(.8, 1.1)
        ex, ey = bx + math.cos(a) * L, by + math.sin(a) * L
        out.append(f'<path d="M{f(bx)},{f(by)} L{f(ex)},{f(ey)}" stroke="{stem}" stroke-width="{f(s*.022)}"/>')
        for j in range(1, 7):  # lístky v pároch
            u = j / 7
            px_, py_ = bx + (ex - bx) * u, by + (ey - by) * u
            for sd in (-1, 1):
                aa = math.degrees(a) + sd * 62
                out.append(leaf(px_, py_, s * .26, s * .06, aa, rnd.choice(leaf_cols), None))
        out.append(leaf(ex, ey, s * .28, s * .065, math.degrees(a), rnd.choice(leaf_cols)))
        if k % 3 == 1:
            berries.append((bx + math.cos(base + math.pi/2 * -side) * s * .25, by + math.sin(base + math.pi/2 * -side) * s * .25 + s * .2))
    for bx, by in berries:
        for _ in range(16):
            ox, oy = bx + rnd.gauss(0, s * .1), by + rnd.gauss(0, s * .07)
            r = s * rnd.uniform(.04, .055)
            out.append(f'<path d="M{f(bx)},{f(by - s*.2)} L{f(ox)},{f(oy)}" stroke="{stem}" stroke-width="{f(s*.008)}"/>'
                       f'<circle cx="{f(ox)}" cy="{f(oy)}" r="{f(r)}" fill="{berry}"/>'
                       f'<circle cx="{f(ox - r*.35)}" cy="{f(oy - r*.35)}" r="{f(r*.3)}" fill="{berry_hi}"/>')
    return "".join(out)


def bilberry(x, y, s, stem, leaf_cols, berry, bloom, seed=0):
    """Čučoriedkový kríček — drobné lístky, modré bobule s ojíňaním."""
    rnd = random.Random(seed)
    out = []
    for _ in range(5):
        a = math.radians(rnd.uniform(-130, -50))
        L = s * rnd.uniform(.6, 1)
        ex, ey = x + math.cos(a) * L, y + math.sin(a) * L
        out.append(f'<path d="M{f(x)},{f(y)} L{f(ex)},{f(ey)}" stroke="{stem}" stroke-width="{f(s*.025)}"/>')
        for j in range(1, 7):
            u = j / 7
            px_, py_ = x + (ex - x) * u, y + (ey - y) * u
            sd = 1 if j % 2 else -1
            out.append(leaf(px_, py_, s * .17, s * .07, math.degrees(a) + sd * 55, rnd.choice(leaf_cols)))
            if rnd.random() < .3:
                r = s * .045
                bx, by = px_ + sd * s * .06, py_ + s * .06
                out.append(f'<circle cx="{f(bx)}" cy="{f(by)}" r="{f(r)}" fill="{berry}"/>'
                           f'<circle cx="{f(bx - r*.3)}" cy="{f(by - r*.3)}" r="{f(r*.35)}" fill="{bloom}"/>')
    return "".join(out)


def fern(x, y, L, ang, col, leaf_col=None, curl=.25):
    out = []
    a0 = math.radians(ang)
    pts = []
    for k in range(13):
        t = k / 12
        a = a0 - curl * t * t * 2
        if not pts:
            pts.append((x, y))
        else:
            px_, py_ = pts[-1]
            pts.append((px_ + math.cos(a) * L / 12, py_ - math.sin(a) * L / 12))
    out.append(f'<path d="M{f(pts[0][0])},{f(pts[0][1])} ' + " ".join(f'L{f(a)},{f(b)}' for a, b in pts[1:]) +
               f'" stroke="{col}" stroke-width="{f(L*.02)}" fill="none" stroke-linecap="round"/>')
    for k in range(1, 12):
        t = k / 12
        px_, py_ = pts[k]
        dx, dy = pts[k + 1][0] - px_, pts[k + 1][1] - py_
        a = math.degrees(math.atan2(dy, dx))
        ll = L * .3 * (1 - t * .75)
        for s in (-1, 1):
            out.append(leaf(px_, py_, ll, ll * .22, a + s * 60, leaf_col or col))
    return "".join(out)


# ------------------------------------------------------------------ postavy

POSES = {
    # (x, y) v jednotkách výšky postavy, y nahor od zeme; postava hľadí doprava
    "run": dict(head=(.17, .93), neck=(.12, .84), hip=(0, .53),
                legs=[[(.17, .33), (.11, .07), (.21, .03)], [(-.1, .33), (-.28, .27), (-.31, .19)]],
                arms=[[(.21, .69), (.31, .77)], [(-.03, .66), (.03, .57)]], poles=None),
    "hike": dict(head=(.21, .86), neck=(.15, .78), hip=(0, .5),
                 legs=[[(.17, .36), (.14, .07), (.23, .04)], [(-.05, .3), (-.15, .06), (-.08, .02)]],
                 arms=[[(.25, .62), (.33, .6)], [(.06, .6), (-.02, .52)]], poles=[(.47, 0), (-.2, 0)]),
    "cheer": dict(head=(0, .93), neck=(0, .84), hip=(0, .52),
                  legs=[[(.06, .28), (.08, .02), (.15, .0)], [(-.06, .28), (-.09, .02), (-.02, .0)]],
                  arms=[[(.13, .95), (.17, 1.09)], [(-.13, .95), (-.17, 1.09)]], poles=None),
    "stand": dict(head=(.02, .93), neck=(.01, .84), hip=(0, .52),
                  legs=[[(.05, .28), (.06, .02), (.13, .0)], [(-.05, .28), (-.05, .02), (.02, .0)]],
                  arms=[[(.08, .66), (.1, .52)], [(-.08, .66), (-.09, .52)]], poles=[(.2, 0), None]),
}


def figure(x, y, s, col, pose="run", face=1, rim=None, lamp=None, pack=True, hat=False):
    """Bežec/turista so správnymi proporciami — silueta z hrubých ťahov."""
    P = POSES[pose]

    def pt(q):
        return x + face * q[0] * s, y - q[1] * s

    def seg(a, b, w, c):
        (ax, ay), (bx, by) = pt(a), pt(b)
        return f'<path d="M{f(ax)},{f(ay)} L{f(bx)},{f(by)}" stroke="{c}" stroke-width="{f(w*s)}" stroke-linecap="round"/>'

    def body(c, dx=0.0):
        nonlocal x
        x0 = x
        x += dx
        out = []
        hip, neck, head = P["hip"], P["neck"], P["head"]
        shoulder = (neck[0] - .005, neck[1] - .04)
        for leg in P["legs"]:
            out.append(seg(hip, leg[0], .1, c) + seg(leg[0], leg[1], .075, c) + seg(leg[1], leg[2], .055, c))
        out.append(seg(hip, (neck[0], neck[1] - .03), .14, c))
        if pack:
            bx = (hip[0] + neck[0]) / 2 - .07
            by = (hip[1] + neck[1]) / 2 + .06
            X, Y = pt((bx, by))
            out.append(f'<ellipse cx="{f(X)}" cy="{f(Y)}" rx="{f(.06*s)}" ry="{f(.11*s)}" fill="{c}" '
                       f'transform="rotate({f(face * -12)} {f(X)} {f(Y)})"/>')
        for i, arm in enumerate(P["arms"]):
            out.append(seg(shoulder, arm[0], .058, c) + seg(arm[0], arm[1], .05, c))
            if P["poles"] and P["poles"][i]:
                (hx, hy), (gx, gy) = pt(arm[1]), pt(P["poles"][i])
                out.append(f'<path d="M{f(hx)},{f(hy)} L{f(gx)},{f(gy)}" stroke="{c}" stroke-width="{f(max(1, .014*s))}"/>')
        hx, hy = pt(head)
        out.append(f'<circle cx="{f(hx)}" cy="{f(hy)}" r="{f(.072*s)}" fill="{c}"/>')
        if hat:
            out.append(f'<path d="M{f(hx - .09*s)},{f(hy - .03*s)} h{f(.18*s)} l{f(-.03*s)},{f(-.07*s)} h{f(-.12*s)}Z" fill="{c}"/>')
        else:
            out.append(f'<path d="M{f(hx)},{f(hy - .05*s)} l{f(face*.11*s)},{f(.012*s)}" stroke="{c}" stroke-width="{f(.025*s)}" stroke-linecap="round"/>')
        x = x0
        return "".join(out)

    out = ""
    if rim:
        out += body(rim, dx=-1.4) + body(rim, dx=0.0)
    out += body(col, dx=(0.9 if rim else 0))
    if lamp:
        hx, hy = pt(P["head"])
        out += f'<circle cx="{f(hx + face*.06*s)}" cy="{f(hy - .02*s)}" r="{f(max(1.8, .035*s))}" fill="{lamp}" filter="url(#glow)"/>'
    return out


def sheep(x, y, s, wool, shade, head, rnd, face=1, rim=None):
    out = []
    for lx in (-.38, -.22, .22, .36):
        out.append(f'<rect x="{f(x + lx*s)}" y="{f(y - s*.3)}" width="{f(s*.08)}" height="{f(s*.3)}" fill="{head}"/>')
    blobs = [(x + rnd.uniform(-.45, .45)*s, y - s*rnd.uniform(.38, .62), s*rnd.uniform(.16, .24)) for _ in range(11)]
    out.append(f'<ellipse cx="{f(x)}" cy="{f(y - s*.48)}" rx="{f(s*.56)}" ry="{f(s*.24)}" fill="{shade}"/>')
    out += [f'<circle cx="{f(bx)}" cy="{f(by)}" r="{f(br)}" fill="{shade}"/>' for bx, by, br in blobs]
    out += [f'<circle cx="{f(bx - br*.25)}" cy="{f(by - br*.3)}" r="{f(br*.8)}" fill="{wool}"/>' for bx, by, br in blobs]
    hx, hy = x + face * s * .62, y - s * .56
    out.append(f'<ellipse cx="{f(hx)}" cy="{f(hy)}" rx="{f(s*.13)}" ry="{f(s*.18)}" fill="{head}" transform="rotate({face*35} {f(hx)} {f(hy)})"/>')
    out.append(f'<ellipse cx="{f(hx - face*s*.1)}" cy="{f(hy - s*.12)}" rx="{f(s*.09)}" ry="{f(s*.04)}" fill="{head}"/>')
    return "".join(out)


# ------------------------------------------------------------------ stavby

def cabin34(x, y, s, wall_f, wall_s, logs, roof, roof_s, rim, win, win_glow=False, door=None, seed=0):
    """Zrubová drevenica v trojštvrťovom pohľade: štít k divákovi, bočná stena ubieha doprava."""
    rnd = random.Random(seed)
    fw, wh, sd, k = s * 1.5, s * .95, s * 2.3, -.3
    ax, ay = x + fw / 2, y - wh - s * 1.05  # vrchol štítu
    off = (sd, sd * k)
    out = []
    # bočná stena
    side = [(x + fw, y), (x + fw + sd, y + sd * k), (x + fw + sd, y + sd * k - wh), (x + fw, y - wh)]
    out.append(f'<path d="{poly(side)}" fill="{wall_s}"/>')
    for i in range(1, 9):
        yy = y - wh * i / 9
        out.append(f'<path d="M{f(x + fw)},{f(yy)} L{f(x + fw + sd)},{f(yy + sd*k)}" stroke="{logs}" stroke-width="{f(s*.035)}"/>')
    # okná a dvere na bočnej stene
    def sidequad(u0, u1, v0, v1):
        def P(u, v):
            return (x + fw + sd * u, y + sd * k * u - wh * v)
        return [P(u0, v0), P(u1, v0), P(u1, v1), P(u0, v1)]
    for u0 in (.12, .62):
        q = sidequad(u0, u0 + .14, .35, .72)
        out.append(f'<path d="{poly(q)}" fill="{win}"' + (' filter="url(#glow)"' if win_glow else "") + "/>")
        c = sidequad(u0 + .065, u0 + .075, .35, .72)
        out.append(f'<path d="{poly(c)}" fill="{wall_s}"/>')
    dq = sidequad(.38, .5, 0, .8)
    out.append(f'<path d="{poly(dq)}" fill="{door or roof_s}"/>')
    # čelná stena so štítom
    front = [(x, y), (x + fw, y), (x + fw, y - wh), (ax, ay + s * .12), (x, y - wh)]
    out.append(f'<path d="{poly(front)}" fill="{wall_f}"/>')
    for i in range(1, 12):
        yy = y - (wh + s * .95) * i / 12
        if yy > y - wh:
            xa, xb = x, x + fw
        else:
            t = (y - wh - yy) / (s * .93)
            xa, xb = x + fw / 2 * t, x + fw - fw / 2 * t
        if xb - xa > 2:
            out.append(f'<path d="M{f(xa)},{f(yy)} L{f(xb)},{f(yy)}" stroke="{logs}" stroke-width="{f(s*.035)}"/>')
    # hlavy brvien na rohu
    for i in range(9):
        yy = y - wh * (i + .5) / 9
        out.append(f'<ellipse cx="{f(x + fw + s*.02)}" cy="{f(yy)}" rx="{f(s*.06)}" ry="{f(s*.045)}" fill="{logs}"/>')
        out.append(f'<ellipse cx="{f(x - s*.02)}" cy="{f(yy)}" rx="{f(s*.05)}" ry="{f(s*.045)}" fill="{logs}"/>')
    for wx in (x + fw * .2, x + fw * .6):
        out.append(f'<rect x="{f(wx)}" y="{f(y - wh*.72)}" width="{f(fw*.2)}" height="{f(wh*.36)}" fill="{win}"' + (' filter="url(#glow)"' if win_glow else "") + "/>"
                   f'<path d="M{f(wx + fw*.1)},{f(y - wh*.72)} v{f(wh*.36)} M{f(wx)},{f(y - wh*.54)} h{f(fw*.2)}" stroke="{wall_f}" stroke-width="{f(s*.03)}"/>')
    out.append(f'<rect x="{f(ax - s*.1)}" y="{f(ay + s*.5)}" width="{f(s*.2)}" height="{f(s*.18)}" fill="{win}" opacity=".85"/>')
    # strecha — bočná rovina so šindľom
    eave_r = (x + fw + s * .12, y - wh + s * .04)
    roofp = [(ax, ay), (ax + off[0], ay + off[1]), (eave_r[0] + off[0] + s * .1, eave_r[1] + off[1]), eave_r]
    out.append(f'<path d="{poly(roofp)}" fill="{roof}"/>')
    for i in range(1, 10):
        t = i / 10
        pa = (ax + (eave_r[0] - ax) * t, ay + (eave_r[1] - ay) * t)
        out.append(f'<path d="M{f(pa[0])},{f(pa[1])} l{f(off[0])},{f(off[1])}" stroke="{roof_s}" stroke-width="{f(s*.025)}"/>')
    for i in range(24):
        t = rnd.uniform(0, 1)
        u = rnd.uniform(0, 1)
        px_ = ax + (eave_r[0] - ax) * u + off[0] * t
        py_ = ay + (eave_r[1] - ay) * u + off[1] * t
        out.append(f'<path d="M{f(px_)},{f(py_)} l{f(s*.015)},{f(s*.08)}" stroke="{roof_s}" stroke-width="{f(s*.02)}"/>')
    # čelná hrana strechy (lemovka) + lemové svetlo
    out.append(f'<path d="M{f(x - s*.14)},{f(y - wh + s*.05)} L{f(ax)},{f(ay - s*.04)} L{f(eave_r[0])},{f(eave_r[1])}" '
               f'stroke="{roof}" stroke-width="{f(s*.12)}" fill="none" stroke-linejoin="round"/>')
    if rim:
        out.append(f'<path d="M{f(x - s*.14)},{f(y - wh + s*.0)} L{f(ax)},{f(ay - s*.1)} L{f(ax + off[0])},{f(ay + off[1] - s*.1)}" '
                   f'stroke="{rim}" stroke-width="{f(s*.04)}" fill="none" stroke-linejoin="round"/>')
    # komín
    cx_ = ax + off[0] * .7
    cy_ = ay + off[1] * .7 + s * .25
    out.append(f'<path d="M{f(cx_)},{f(cy_)} v{f(-s*.55)} h{f(s*.22)} v{f(s*.5)}Z" fill="{roof_s}"/>')
    return "".join(out), (cx_ + s * .11, cy_ - s * .55)


def house_tiny(x, y, s, wall, roof, win=None):
    out = (f'<rect x="{f(x - s)}" y="{f(y - s*.8)}" width="{f(s*2)}" height="{f(s*.8)}" fill="{wall}"/>'
           f'<path d="M{f(x - s*1.2)},{f(y - s*.75)} L{f(x - s*.3)},{f(y - s*1.6)} L{f(x + s*1.15)},{f(y - s*1.6)} L{f(x + s*1.25)},{f(y - s*.75)}Z" fill="{roof}"/>')
    if win:
        out += f'<rect x="{f(x - s*.5)}" y="{f(y - s*.55)}" width="{f(s*.4)}" height="{f(s*.3)}" fill="{win}" filter="url(#glow)"/>'
    return out


def haystack(x, y, s, lit, mid, dark, straw, pole, seed=0, shadow=None, lit_side=-1):
    """Kopa sena okolo ostrve: kupola, žrď trčí hore, ťahy slamy po tvare."""
    rnd = random.Random(seed)
    w = s * .52
    body = (f'M{f(x - w)},{f(y)} C{f(x - w*1.08)},{f(y - s*.5)} {f(x - w*.7)},{f(y - s*1.05)} {f(x - w*.18)},{f(y - s*1.3)} '
            f'Q{f(x)},{f(y - s*1.38)} {f(x + w*.18)},{f(y - s*1.3)} C{f(x + w*.7)},{f(y - s*1.05)} {f(x + w*1.08)},{f(y - s*.5)} {f(x + w)},{f(y)}Z')
    out = []
    if shadow:
        out.append(f'<path d="M{f(x - w*.9)},{f(y)} Q{f(x + s*.8)},{f(y + s*.02)} {f(x + s*1.6)},{f(y + s*.12)} Q{f(x + s*.6)},{f(y + s*.2)} {f(x - w*.6)},{f(y + s*.07)}Z" fill="{shadow}" opacity=".45"/>')
    out.append(f'<rect x="{f(x - s*.025)}" y="{f(y - s*1.52)}" width="{f(s*.05)}" height="{f(s*.3)}" fill="{pole}"/>')
    out.append(f'<path d="{body}" fill="{mid}"/>')
    cid = f"hay{seed}"
    out.append(f'<clipPath id="{cid}"><path d="{body}"/></clipPath><g clip-path="url(#{cid})">')
    ls = lit_side
    out.append(f'<path d="M{f(x + ls*w*1.2)},{f(y)} C{f(x + ls*w*1.1)},{f(y - s*.8)} {f(x + ls*w*.4)},{f(y - s*1.3)} {f(x - ls*w*.05)},{f(y - s*1.5)} '
               f'C{f(x + ls*w*.1)},{f(y - s*.9)} {f(x + ls*w*.35)},{f(y - s*.4)} {f(x + ls*w*.25)},{f(y)}Z" fill="{lit}"/>')
    out.append(f'<path d="M{f(x - ls*w*1.2)},{f(y)} C{f(x - ls*w*1.1)},{f(y - s*.7)} {f(x - ls*w*.6)},{f(y - s*1.1)} {f(x - ls*w*.25)},{f(y - s*1.4)} '
               f'C{f(x - ls*w*.45)},{f(y - s*.9)} {f(x - ls*w*.6)},{f(y - s*.4)} {f(x - ls*w*.55)},{f(y)}Z" fill="{dark}"/>')
    for _ in range(int(s * 1.6)):
        t = rnd.uniform(0.02, 1)
        yy = y - s * 1.3 * (1 - t) - rnd.uniform(0, s * .05)
        wx = w * math.sin(math.pi / 2 * min(1, t * 1.25)) ** .7
        u = rnd.uniform(-1, 1)
        xx = x + u * wx
        a = math.pi / 2 + u * .5
        col = straw if (u * ls > .1) else rnd.choice([dark, straw, mid])
        out.append(dab(xx, yy, s * rnd.uniform(.06, .14), s * rnd.uniform(.012, .022), a, col, .8))
    out.append(f'<path d="M{f(x - w*1.1)},{f(y - s*.08)} Q{f(x)},{f(y + s*.02)} {f(x + w*1.1)},{f(y - s*.08)} L{f(x + w)},{f(y + 2)} H{f(x - w)}Z" fill="{dark}" opacity=".7"/></g>')
    return "".join(out)
