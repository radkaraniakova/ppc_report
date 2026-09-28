#!/usr/bin/env python3
"""Javorníky — séria 2, prepracovaná verzia (07–12). Staví na ilustrátorskej sade `kit.py`.

Spusti:  python3 generate_premium.py   → ../svg/07…12
"""
import math
import random

from generate import W, H, f, smooth_path, ridge, y_at, poly
from generate_malba import Poster, title, IX0, IY0, IX1, IY1
import kit as K


def R(base, bumps, seed, wob=0.0, step=14):
    return ridge(base, bumps, x0=-20, x1=W + 20, step=step, wobble=wob, seed=seed)


def bottom_shade(p, col, y0, op=.55):
    g = p.lg([(0, col, 0), (1, col, op)], user=(0, y0, 0, H))
    p.add(f'<rect x="0" y="{y0}" width="{W}" height="{H - y0}" fill="{g}"/>')


# ====================================================================== 07 STRATENEC

def cross_backlit(p, x, yb, h, sw, span, ay, face_top, face_bot, side, rim, seed):
    """Betónový kríž v protisvetle: chladná čelná plocha, tmavý bok, žiariaci lem."""
    rnd = random.Random(seed)
    d = sw * .32
    shape = (f'M{f(x - sw/2)},{f(yb)} V{f(ay + sw*.9)} H{f(x - span/2)} V{f(ay)} H{f(x - sw/2)} V{f(yb - h)} '
             f'H{f(x + sw/2)} V{f(ay)} H{f(x + span/2)} V{f(ay + sw*.9)} H{f(x + sw/2)} V{f(yb)}Z')
    g = p.lg([(0, face_top), (1, face_bot)], user=(0, yb - h, 0, yb))
    out = [f'<path d="{shape}" fill="{rim}" filter="url(#blur3)" opacity=".9"/>',
           f'<path d="M{f(x + sw/2)},{f(yb - h)} l{f(d)},{f(d*.55)} V{f(ay)} h{f(-d)}Z" fill="{side}"/>',
           f'<path d="M{f(x + span/2)},{f(ay)} l{f(d)},{f(d*.55)} v{f(sw*.9)} h{f(-d)}Z" fill="{side}"/>',
           f'<path d="M{f(x + sw/2)},{f(ay + sw*.9)} h{f(span/2 - sw/2 + d)} l0,{f(d*.55)} H{f(x + sw/2 + d)} V{f(yb)} h{f(-d)}Z" fill="{side}"/>',
           f'<path d="M{f(x - span/2)},{f(ay + sw*.9)} h{f(span/2 - sw/2)} l{f(d*.3)},{f(d*.5)} h{f(-(span/2 - sw/2))}Z" fill="{side}" opacity=".8"/>',
           f'<path d="{shape}" fill="{g}"/>']
    cid = K.clip(p, shape)
    tex = []
    for _ in range(int(h * .5)):  # betón: zvislé ťahy + škáry debnenia
        tx = x + rnd.uniform(-span/2, span/2)
        ty = rnd.uniform(yb - h, yb)
        tex.append(K.dab(tx, ty, rnd.uniform(6, 22), rnd.uniform(1, 2.4), math.pi/2 + rnd.uniform(-.08, .08),
                         rnd.choice(["#c9ccd3", "#6d7384", "#9aa0ad"]), .45))
    for k in range(1, 9):
        yy = yb - h * k / 9
        tex.append(f'<path d="M{f(x - span/2)},{f(yy)} H{f(x + span/2)}" stroke="#5c6272" stroke-width=".8" opacity=".5"/>')
    tex.append(f'<path d="{shape}" fill="none" stroke="{rim}" stroke-width="5"/>')
    out.append(f'<g clip-path="url(#{cid})">' + "".join(tex) + "</g>")
    return "".join(out)


def p07():
    p = Poster("Stratenec")
    rnd = random.Random(7)
    NAVY, NAVY2, NAVY3 = "#16294a", "#2c4a78", "#6f93c2"
    sky = p.lg([(0, "#15508f"), (.35, "#3d88c6"), (.7, "#a6d0e0"), (1, "#f6e3ae")], user=(0, 0, 0, 880))
    p.add(f'<rect width="{W}" height="{H}" fill="{sky}"/>')
    sx, sy = 500, 360
    K.glow(p, sx, sy, 520, "#fff4cf", .9)
    K.rays(p, sx, sy, [a for a in range(0, 360, 13)], 1100, "#fff6d8", op=.16, width=.035)
    for cx, cy, w, h, s in [(170, 150, 380, 110, 1), (820, 110, 360, 100, 2), (900, 380, 260, 70, 3),
                            (110, 470, 240, 60, 4), (660, 250, 220, 55, 5), (360, 90, 180, 45, 6)]:
        K.cloud(p, cx, cy, w, h, "#fffdf4", "#dde8ee", "#a3bfd4", seed=s)
    K.wisp(p, 300, 560, 520, 18, "#ffffff", .5)
    K.wisp(p, 780, 590, 420, 14, "#ffffff", .45)
    # vzdialené oblé Javorníky + Malá Fatra
    far = R(700, [(140, 90, 170), (520, 55, 220), (880, 120, 150)], 3)
    K.hill(p, far, "#97b1c2", "#c6d8de", depth=200, rim="#eef6f5", rim_w=1.5)
    p.add(K.tree_row(far, 0, W, 5, lambda x, y, r: K.spruce_simple(x, y + 6, r.uniform(7, 11), "#86a2b6"), rnd))
    K.fog(p, 500, 760, 1200, 80, "#f4f1e0", .6)
    mid = R(790, [(80, 80, 190), (420, 40, 180), (920, 100, 160)], 4)
    K.hill(p, mid, "#6d8ea3", "#96b1bb", depth=200, rim="#dce9ea", rim_w=1.5)
    p.add(K.tree_row(mid, 0, W, 7, lambda x, y, r: K.spruce_simple(x, y + 8, r.uniform(14, 22), "#4d6c85", "#6f8ea6"), rnd))
    # zlaté lúky s jesennými bučinami
    m2 = R(920, [(130, 170, 230), (840, 190, 220)], 5)
    K.hill(p, m2, "#f0c24a", "#c98d22", depth=300, tex=["#f8d772", "#c48a25", "#e3a93a"], n=500, L=16, wid=2.6, op=.5,
           rim="#fff2c2", rim_w=2.5, seed=5)
    autumn = [("#9a4a1f", "#dc8a2f", "#f3c44e"), ("#7a3520", "#b8552a", "#e0873a"), ("#8a5a18", "#d7a23a", "#f6d56a")]
    K.crowns(p, m2, 90, 700, autumn, 4.2, seed=51, span=(-20, 250))
    K.crowns(p, m2, 90, 700, autumn, 4.2, seed=52, span=(740, 1020))
    p.add(K.tree_row(m2, 40, 200, 22, lambda x, y, r: K.spruce(x, y + r.uniform(40, 90), r.uniform(50, 80), NAVY, NAVY2, NAVY3, seed=int(x)), rnd))
    p.add(K.tree_row(m2, 780, 960, 22, lambda x, y, r: K.spruce(x, y + r.uniform(40, 90), r.uniform(50, 80), NAVY, NAVY2, NAVY3, seed=int(x)), rnd))
    # rozhľadňa v opare za krížmi
    tx, tb = 395, 905
    p.add(f'<g stroke="#7d93a8" stroke-width="2.4" fill="none" opacity=".95">'
          f'<path d="M{tx-20},{tb} L{tx-9},{tb-200} M{tx+20},{tb} L{tx+9},{tb-200}'
          + "".join(f' M{tx-20+11*k/5},{tb-40*k} L{tx+20-11*(k+1)/5},{tb-40*(k+1)} M{tx+20-11*k/5},{tb-40*k} L{tx-20+11*(k+1)/5},{tb-40*(k+1)}' for k in range(5))
          + f'"/></g><rect x="{tx-22}" y="{tb-218}" width="44" height="18" fill="#7d93a8"/>'
          f'<path d="M{tx-28},{tb-218} L{tx},{tb-240} L{tx+28},{tb-218}Z" fill="#6f859a"/>')
    # hrebeň s krížmi
    crest = R(1060, [(500, 150, 330)], 6)
    K.hill(p, crest, "#f3c850", "#b77a1c", depth=380, tex=["#ffe08a", "#b77a1c", "#e9b440", "#9e6414"], n=900, L=20, wid=3,
           op=.55, rim="#fff6d0", rim_w=3, seed=6)
    # dlhé tiene k divákovi
    for x, w in ((255, 60), (745, 60), (500, 80)):
        yb = y_at(crest, x) + 28
        p.add(f'<path d="M{x - w*.6},{yb} L{x + w*.6},{yb} L{x + w*2.2 + (x - 500)*.5},{H} L{x - w*1.4 + (x - 500)*.5},{H}Z" fill="#6b4210" opacity=".28"/>')
    for x, h, sw, span, ay in ((255, 470, 58, 240, 590), (745, 470, 58, 240, 590), (500, 650, 76, 330, 410)):
        yb = y_at(crest, x) + 30
        p.add(cross_backlit(p, x, yb, h, sw, span, ay, "#aeb2bc", "#6c7282", "#27324d", "#fff0c4", x))
        w = sw * 2.1
        p.add(f'<path d="M{f(x - w/2 + 8)},{f(yb - 4)} H{f(x + w/2 - 8)} L{f(x + w/2)},{f(yb + 40)} H{f(x - w/2)}Z" fill="#7a7f8c"/>'
              f'<path d="M{f(x - w/2 + 8)},{f(yb - 4)} H{f(x + w/2 - 8)}" stroke="#fff0c4" stroke-width="3"/>'
              f'<path d="M{f(x + w/2 - 8)},{f(yb - 4)} l14,7 l0,40 l-6,-3Z" fill="#27324d"/>')
    # malý bežec stúpa ku krížom
    rx = 612
    p.add(K.figure(rx, y_at(crest, rx) + 70, 44, "#2a2a38", "hike", face=-1, rim="#fff0c4"))
    p.add(f'<path d="M{rx-4},{f(y_at(crest, rx) + 71)} l40,90 l14,0 l-34,-90Z" fill="#6b4210" opacity=".25"/>')
    # popredie
    fg = R(1225, [(220, 45, 260), (780, 35, 260)], 9)
    K.hill(p, fg, "#e9b23c", "#8a5a14", depth=220, tex=["#ffd46a", "#9a6414", "#c98d22"], n=700, L=26, wid=3.5, op=.6,
           rim="#ffe9a8", rim_w=2.5, seed=9)
    for x, hh, sd in ((-30, 640, 11), (95, 470, 12), (1020, 700, 13), (905, 500, 14), (820, 300, 15)):
        p.add(K.spruce(x, 1270, hh, NAVY, NAVY2, NAVY3, seed=sd, lit=1 if x < 500 else -1, rim="#ffe9b8", rim_w=1.1))
    for _ in range(40):
        x = rnd.uniform(IX0, IX1)
        y = rnd.uniform(1250, H)
        if y > 1235 and 280 < x < 720:
            continue
        p.add(K.tuft(x, y, rnd.uniform(30, 70), ["#16294a", "#2c4a78", "#8a5a14"], rnd, n=6))
    bottom_shade(p, "#3a1f06", 1180, .45)
    title(p, "STRATENEC", "1055 M · JAVORNÍKY · SLOVENSKO", "#fff4d6", y=1300)
    p.render("07-stratenec.svg", speck=.35, light_speck=.3, mottle=.25)


# ====================================================================== 08 KOPANICE

def p08():
    p = Poster("Kopanice")
    rnd = random.Random(8)
    sky = p.lg([(0, "#141a3a"), (.3, "#2e2f63"), (.55, "#7d4e7f"), (.75, "#e0877f"), (.9, "#f6b98e"), (1, "#fbdcae")], user=(0, 0, 0, 760))
    p.add(f'<rect width="{W}" height="{H}" fill="{sky}"/>')
    K.stars(p, 160, (IX0, IY0, IX1, 330), seed=8)
    p.add(f'<mask id="mn"><rect width="{W}" height="{H}" fill="#fff"/><circle cx="836" cy="126" r="26" fill="#000"/></mask>')
    K.glow(p, 820, 135, 90, "#ffe9c9", .35)
    p.add(f'<circle cx="820" cy="135" r="28" fill="#fbeed2" mask="url(#mn)"/>')
    for cx, cy, w, h, s, o in [(230, 210, 560, 90, 1, 1), (760, 300, 520, 80, 2, 1), (330, 420, 460, 60, 3, .95),
                               (800, 500, 380, 50, 4, .9), (140, 540, 300, 40, 5, .85)]:
        K.cloud(p, cx, cy, w, h, "#ffb3a2", "#b76a86", "#34305f", seed=s, below=True, flat=.55, op=o)
    K.wisp(p, 500, 610, 900, 16, "#ffd3a8", .6)
    K.glow(p, 520, 700, 420, "#ffcf9e", .35)
    far = R(700, [(180, 70, 200), (600, 45, 220), (900, 85, 150)], 31)
    K.hill(p, far, "#8a6aa0", "#a782a6", depth=160, rim="#f7b9a4", rim_w=1.5)
    for x in (120, 310, 470, 690, 860):
        p.add(K.house_tiny(x, y_at(far, x) + 14, 5, "#6d5486", "#5a4474", "#ffd98a"))
    fog_col = "#d7a3b6"
    K.fog(p, 500, 760, 1100, 60, fog_col, .5)
    mid = R(820, [(120, 80, 180), (480, 100, 230), (860, 60, 180)], 32)
    K.hill(p, mid, "#5d4577", "#46345f", depth=220, tex=["#6e5388", "#3e2d55"], n=300, L=14, wid=2.5, op=.5, rim="#f2a39b", rim_w=1.8, seed=32)
    p.add(K.tree_row(mid, 560, 1020, 10, lambda x, y, r: K.spruce_simple(x, y + 10, r.uniform(20, 30), "#3a2b52", "#58427a"), rnd))
    for x in (160, 260, 390):
        p.add(K.house_tiny(x, y_at(mid, x) + 22, 8, "#4a3862", "#35274a", "#ffd27a"))
    for x in (215, 330):
        p.add(K.haystack(x, y_at(mid, x) + 30, 24, "#6e5388", "#58427a", "#3a2b52", "#8a6aa0", "#241a33", seed=x))
    near = R(1000, [(260, 90, 260), (770, 130, 250)], 33)
    K.hill(p, near, "#44325c", "#1c1428", depth=420, tex=["#5a4474", "#2a1f3b", "#6d5486"], n=900, L=22, wid=3, op=.45,
           rim="#e99a98", rim_w=2, seed=33)
    # smreky vľavo s ružovým lemom
    for x, hh, sd in ((40, 460, 1), (150, 380, 2), (-40, 330, 3), (250, 250, 4)):
        p.add(K.spruce(x, 1030, hh, "#1c1428", "#34264a", "#5a4474", seed=sd, lit=1, rim="#f2a39b", rim_w=1.4))
    # drevenica
    hx, hy = 470, 1000
    svg, chim = K.cabin34(hx, hy, 58, "#3b2a36", "#2c1f2b", "#1a1219", "#211722", "#120c12", "#f19a8e", "#ffd27a",
                          win_glow=True, door="#ffcf73", seed=4)
    # svetlo z okien na trávu
    K.glow(p, hx + 150, hy + 20, 170, "#ffcf73", .22)
    p.add(svg)
    p.add(f'<path d="M{f(chim[0])},{f(chim[1])} C{f(chim[0] - 30)},{f(chim[1] - 60)} {f(chim[0] + 40)},{f(chim[1] - 110)} {f(chim[0] + 10)},{f(chim[1] - 180)} '
          f'S{f(chim[0] + 60)},{f(chim[1] - 280)} {f(chim[0] + 30)},{f(chim[1] - 340)}" stroke="#e7a9b4" stroke-width="16" fill="none" '
          f'stroke-linecap="round" opacity=".45" filter="url(#blur8)"/>')
    # drevo pod strechou, lavica, plot
    for i in range(14):
        p.add(f'<circle cx="{hx + 12 + (i % 7) * 11}" cy="{hy - 8 - (i // 7) * 11}" r="5.5" fill="#8a5a44" stroke="#2c1f2b" stroke-width="1.5"/>')
    for i, x in enumerate(range(250, 440, 30)):
        yy = y_at(near, x) + 35 + i * 4
        p.add(f'<path d="M{x},{yy} v-52" stroke="#140e18" stroke-width="6" stroke-linecap="round"/>'
              f'<path d="M{x},{yy - 50} l-4,-6" stroke="#e99a98" stroke-width="2"/>')
    p.add(f'<path d="M250,{f(y_at(near,250)-5)} L440,{f(y_at(near,440)+18)} M250,{f(y_at(near,250)+12)} L440,{f(y_at(near,440)+36)}" stroke="#140e18" stroke-width="4"/>')
    # cesta s mlákami odrážajúcimi oblohu
    path = f'M300,{H} C330,1300 700,1250 700,1160 C700,1090 600,1060 598,1004 L640,1004 C660,1050 780,1090 790,1170 C800,1280 520,1330 640,{H}Z'
    pg = p.lg([(0, "#8a6a8e"), (1, "#4b3a58")], user=(0, 1000, 0, H))
    p.add(f'<path d="{path}" fill="{pg}"/>')
    cid = K.clip(p, path)
    tex = "".join(K.dab(rnd.uniform(360, 840), rnd.uniform(1010, H), rnd.uniform(8, 26), rnd.uniform(1.5, 3), rnd.uniform(-.2, .2),
                        rnd.choice(["#a48aa6", "#3b2d47", "#6b5470"]), .5) for _ in range(260))
    p.add(f'<g clip-path="url(#{cid})">{tex}</g>')
    for cx, cy, rx, ry in ((470, 1290, 70, 11), (720, 1170, 45, 7), (620, 1040, 22, 4)):
        g2 = p.lg([(0, "#f6b98e"), (1, "#7d4e7f")], user=(0, cy - ry, 0, cy + ry))
        p.add(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{g2}"/>')
    # bežec s čelovkou prichádza ku kopanici
    rx_, ry_ = 700, 1150
    beam = p.lg([(0, "#fff0c0", .45), (1, "#fff0c0", 0)], user=(rx_, 0, rx_ - 10, 0))
    p.add(f'<path d="M{rx_ - 4},{ry_ - 62} L{rx_ - 150},{ry_ - 150} L{rx_ - 90},{ry_ - 40}Z" fill="#fff0c0" opacity=".22" filter="url(#blur3)"/>')
    p.add(K.figure(rx_, ry_, 70, "#120c16", "run", face=-1, rim="#f19a8e", lamp="#fff6d0"))
    for _ in range(70):
        x = rnd.uniform(IX0, IX1)
        y = rnd.uniform(1180, H)
        if 280 < x < 720 and y > 1235:
            continue
        p.add(K.tuft(x, y, rnd.uniform(30, 64), ["#140e18", "#2a1f3b", "#3e2d55"], rnd, n=6))
    p.add(K.fern(960, H, 230, 115, "#140e18"))
    p.add(K.fern(20, H - 10, 200, 70, "#140e18"))
    bottom_shade(p, "#0c0812", 1150, .6)
    title(p, "KOPANICE", "JAVORNÍKY · SLOVENSKO", "#fbe3cc", y=1300)
    p.render("08-kopanice.svg", speck=.3, light_speck=.25, mottle=.22)


# ====================================================================== 09 BUČINA

def lynx(x, y, s, body, dark, shade):
    """Rys sediaci čelom k divákovi — golier z bokombrád, strapce na ušiach, škvrny."""
    def P(u, v):
        return f"{f(x + u*s)},{f(y + v*s)}"
    out = []
    # chvost
    out.append(f'<path d="M{P(.4,-.12)} C{P(.7,-.1)} {P(.85,-.02)} {P(.9,-.12)} L{P(.95,-.02)} C{P(.8,.04)} {P(.6,.02)} {P(.4,0)}Z" fill="{body}"/>'
               f'<path d="M{P(.86,-.1)} L{P(.95,-.02)} L{P(.84,.01)}Z" fill="{dark}"/>')
    # telo a stehná
    out.append(f'<path d="M{P(-.58,0)} C{P(-.78,-.35)} {P(-.62,-.95)} {P(-.32,-1.18)} L{P(.32,-1.18)} C{P(.62,-.95)} {P(.78,-.35)} {P(.58,0)}Z" fill="{body}"/>')
    for sd in (-1, 1):
        out.append(f'<ellipse cx="{f(x + sd*.44*s)}" cy="{f(y - .26*s)}" rx="{f(.27*s)}" ry="{f(.26*s)}" fill="{shade}"/>')
    out.append(f'<ellipse cx="{f(x)}" cy="{f(y - .8*s)}" rx="{f(.24*s)}" ry="{f(.34*s)}" fill="#fbf4e4"/>')
    # predné nohy a labky
    for sd in (-1, 1):
        out.append(f'<path d="M{P(sd*.05,-.86)} L{P(sd*.05,-.02)} L{P(sd*.25,-.02)} L{P(sd*.24,-.86)}Z" fill="{body}"/>'
                   f'<ellipse cx="{f(x + sd*.15*s)}" cy="{f(y - .03*s)}" rx="{f(.14*s)}" ry="{f(.065*s)}" fill="{body}"/>'
                   + "".join(f'<path d="M{P(sd*.15 + k*.045, -.07)} v{f(.05*s)}" stroke="{dark}" stroke-width="{f(.012*s)}"/>' for k in (-1, 0, 1)))
    # hlava s golierom (bokombradami)
    L = [(0, -1.8), (-.2, -1.78), (-.34, -1.68), (-.39, -1.52), (-.53, -1.28), (-.41, -1.31), (-.47, -1.14),
         (-.31, -1.21), (-.27, -1.08), (-.13, -1.17), (0, -1.1)]
    pts = L + [(-u, v) for u, v in reversed(L[:-1])]
    out.append(f'<path d="M' + " L".join(P(u, v) for u, v in pts) + f'Z" fill="{body}"/>')
    out.append(f'<path d="M' + " L".join(P(u, v) for u, v in [(-.3, -1.38), (-.46, -1.26), (-.34, -1.27), (-.38, -1.16), (-.24, -1.22)]) + f'" stroke="{dark}" stroke-width="{f(.018*s)}" fill="none"/>')
    out.append(f'<path d="M' + " L".join(P(u, v) for u, v in [(.3, -1.38), (.46, -1.26), (.34, -1.27), (.38, -1.16), (.24, -1.22)]) + f'" stroke="{dark}" stroke-width="{f(.018*s)}" fill="none"/>')
    for sd in (-1, 1):  # uši so strapcami
        out.append(f'<path d="M{P(sd*.34,-1.66)} L{P(sd*.3,-2.02)} L{P(sd*.13,-1.76)}Z" fill="{body}"/>'
                   f'<path d="M{P(sd*.3,-1.72)} L{P(sd*.29,-1.94)} L{P(sd*.19,-1.77)}Z" fill="{dark}"/>'
                   f'<path d="M{P(sd*.3,-2.02)} L{P(sd*.31,-2.18)}" stroke="{dark}" stroke-width="{f(.035*s)}" stroke-linecap="round"/>')
        # oko
        ex = sd * .14
        out.append(f'<path d="M{P(ex - .08, -1.52)} Q{P(ex, -1.6)} {P(ex + .08, -1.52)} Q{P(ex, -1.47)} {P(ex - .08, -1.52)}Z" fill="{dark}"/>'
                   f'<circle cx="{f(x + (ex + .02*sd)*s)}" cy="{f(y - 1.535*s)}" r="{f(.016*s)}" fill="#fbf4e4"/>'
                   f'<path d="M{P(ex + sd*.06, -1.49)} Q{P(ex + sd*.14, -1.42)} {P(ex + sd*.2, -1.3)}" stroke="{dark}" stroke-width="{f(.014*s)}" fill="none"/>'
                   f'<ellipse cx="{f(x + sd*.06*s)}" cy="{f(y - 1.33*s)}" rx="{f(.075*s)}" ry="{f(.055*s)}" fill="#fbf4e4"/>')
    out.append(f'<path d="M{P(-.05,-1.42)} L{P(.05,-1.42)} L{P(0,-1.37)}Z" fill="{dark}"/>'
               f'<path d="M{P(0,-1.37)} v{f(.04*s)} M{P(-.06,-1.31)} Q{P(0,-1.3)} {P(0,-1.33)} Q{P(0,-1.3)} {P(.06,-1.31)}" stroke="{dark}" stroke-width="{f(.012*s)}" fill="none"/>')
    for u in (-.1, 0, .1):
        out.append(f'<path d="M{P(u,-1.78)} L{P(u*1.1,-1.66)}" stroke="{dark}" stroke-width="{f(.014*s)}"/>')
    rnd = random.Random(3)
    for _ in range(26):
        u, v = rnd.uniform(-.6, .6), rnd.uniform(-1.05, -.1)
        if abs(u) < .26 and v < -.5:
            continue
        out.append(f'<ellipse cx="{f(x + u*s)}" cy="{f(y + v*s)}" rx="{f(.035*s)}" ry="{f(.028*s)}" fill="{dark}" opacity=".8"/>')
    for u, v in ((-.15, -.5), (.15, -.45), (-.2, -.3), (.18, -.25)):
        out.append(f'<circle cx="{f(x + u*s)}" cy="{f(y + v*s)}" r="{f(.022*s)}" fill="{dark}"/>')
    return "".join(out)


def beech_trunk(p, x, w, col, hi, eye, rnd, top=0, roots=True):
    """Bukový kmeň: hladká kôra, bočné svetlo, „oká“ po konároch, koreňové nábehy."""
    y1 = H + 10
    d = (f'M{f(x - w*.95)},{y1} C{f(x - w*.55)},{y1 - 60} {f(x - w*.5)},{y1 - 170} {f(x - w*.45)},{y1 - 300} '
         f'C{f(x - w*.4)},700 {f(x - w*.33)},300 {f(x - w*.3)},{top} H{f(x + w*.3)} C{f(x + w*.33)},300 {f(x + w*.4)},700 {f(x + w*.45)},{y1 - 300} '
         f'C{f(x + w*.5)},{y1 - 170} {f(x + w*.55)},{y1 - 60} {f(x + w*.95)},{y1}Z')
    p.add(f'<path d="{d}" fill="{col}"/>')
    p.add(f'<path d="M{f(x - w*.28)},{top} C{f(x - w*.3)},400 {f(x - w*.36)},900 {f(x - w*.42)},{y1} H{f(x - w*.2)} C{f(x - w*.16)},900 {f(x - w*.12)},400 {f(x - w*.12)},{top}Z" fill="{hi}" opacity=".55"/>')
    for _ in range(int(w / 22) + 1):
        yy = rnd.uniform(top + 80, 1200)
        ex = x + rnd.uniform(-w*.15, w*.15)
        ew = w * rnd.uniform(.12, .22)
        p.add(f'<path d="M{f(ex - ew)},{f(yy)} Q{f(ex)},{f(yy - ew*.6)} {f(ex + ew)},{f(yy)} Q{f(ex)},{f(yy + ew*.35)} {f(ex - ew)},{f(yy)}Z" fill="{eye}" opacity=".9"/>'
              f'<path d="M{f(ex - ew*1.8)},{f(yy - ew*.3)} Q{f(ex)},{f(yy - ew*1.3)} {f(ex + ew*1.8)},{f(yy - ew*.3)}" stroke="{eye}" stroke-width="1.4" fill="none" opacity=".6"/>')
    for _ in range(int(w / 4)):
        yy = rnd.uniform(top, 1250)
        p.add(f'<path d="M{f(x - w*.25)},{f(yy)} q{f(w*.2)},-4 {f(w*.4)},0" stroke="{hi}" stroke-width="1.2" fill="none" opacity=".35"/>')


def p09():
    p = Poster("Bučina")
    rnd = random.Random(9)
    TEAL, TEAL2, CORAL, CORAL2, NAVY, CREAM = "#6aa6a2", "#8cc0b8", "#e5735b", "#c65a45", "#1d2946", "#f2e6cf"
    p.add(f'<rect width="{W}" height="{H}" fill="{TEAL}"/>')
    # slnko + kruhy
    p.add(f'<circle cx="500" cy="300" r="48" fill="{CORAL}"/>' +
          "".join(f'<circle cx="500" cy="300" r="{r}" fill="none" stroke="{CORAL}" stroke-width="{w}" opacity=".7"/>' for r, w in ((62, 2), (72, 1.2), (82, .8))))
    for cx, cy, w, h, s in [(330, 380, 170, 36, 1), (690, 350, 190, 40, 2)]:
        K.cloud(p, cx, cy, w, h, CREAM, "#e6dcc4", "#b9d4cc", seed=s, tex=False)
    # vzdialené hrebene s vrstevnicami
    far = R(500, [(250, 80, 200), (720, 60, 200)], 41)
    p.add(f'<path d="{smooth_path(far, H)}" fill="{NAVY}"/>')
    for k in range(1, 5):
        p.add(f'<path d="{smooth_path([(x, y + k*11) for x, y in far])}" stroke="{TEAL}" stroke-width="1" fill="none" opacity=".35"/>')
    p.add(K.tree_row(far, 0, W, 12, lambda x, y, r: f'<ellipse cx="{f(x)}" cy="{f(y + 2)}" rx="{f(r.uniform(7,11))}" ry="{f(r.uniform(11,16))}" fill="{CORAL}"/>'
                     f'<path d="M{f(x)},{f(y+14)} v8" stroke="{CORAL}" stroke-width="2"/>', rnd))
    band = R(585, [(120, 60, 200), (860, 70, 200)], 42)
    p.add(f'<path d="{smooth_path(band, H)}" fill="{CORAL}"/>')
    p.add(K.tree_row(band, 0, W, 9, lambda x, y, r: K.spruce(x, y + 18, r.uniform(44, 66), NAVY, NAVY, TEAL, seed=int(x)), rnd))
    ground = [(x, y + 34) for x, y in band]
    p.add(f'<path d="{smooth_path(ground, H)}" fill="{NAVY}"/>')
    # svetelné lúče do lesa
    for x0, w in ((380, 60), (470, 40), (560, 70)):
        p.add(f'<path d="M{x0},{IY0} L{x0 + w},{IY0} L{x0 + w + 260},{H} L{x0 + 120},{H}Z" fill="{TEAL2}" opacity=".12"/>')
    # cesta
    road = f'M170,{H} C300,1230 560,1100 480,950 C430,850 520,730 494,655 L508,655 C555,730 500,850 545,950 C655,1110 560,1260 800,{H}Z'
    p.add(f'<path d="{road}" fill="{TEAL}"/>')
    cid = K.clip(p, road)
    ruts = "".join(f'<path d="M{a},{H} C{b},1240 {c},1110 {d_},950 C{e},860 {g},730 {h_},660" stroke="{NAVY}" stroke-width="{w}" fill="none" opacity=".4"/>'
                   for a, b, c, d_, e, g, h_, w in ((330, 420, 560, 500, 470, 520, 499, 5), (650, 610, 610, 560, 530, 525, 503, 5)))
    dots = "".join(f'<circle cx="{f(rnd.uniform(170, 800))}" cy="{f(rnd.uniform(660, H))}" r="{f(rnd.uniform(.8, 2.2))}" fill="{NAVY}" opacity=".35"/>' for _ in range(260))
    p.add(f'<g clip-path="url(#{cid})">{ruts}{dots}</g>')
    for cx, cy, rx, ry in ((440, 1210, 88, 15), (600, 1150, 42, 8), (522, 995, 40, 8), (496, 780, 18, 4)):
        p.add(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{CREAM}"/>'
              f'<ellipse cx="{cx - rx*.2}" cy="{cy}" rx="{rx*.25}" ry="{ry*.5}" fill="{CORAL}" opacity=".7"/>')
    # bežec a jeleň v diaľke
    p.add(K.figure(500, 752, 30, CORAL, "run", face=-1, pack=True))
    dx, dy = 655, 700
    deer = (f'<ellipse cx="{dx}" cy="{dy-26}" rx="22" ry="10" fill="{CORAL}"/>'
            f'<path d="M{dx+12},{dy-32} L{dx+24},{dy-58} L{dx+31},{dy-55} L{dx+22},{dy-24}Z" fill="{CORAL}"/>'
            f'<ellipse cx="{dx+33}" cy="{dy-57}" rx="9" ry="4.5" fill="{CORAL}" transform="rotate(22 {dx+33} {dy-57})"/>'
            f'<path d="M{dx+24},{dy-60} l-8,-5 l6,-1Z" fill="{CORAL}"/>'
            f'<path d="M{dx-21},{dy-30} l-5,-4" stroke="{CORAL}" stroke-width="3" stroke-linecap="round"/>'
            + "".join(f'<path d="M{dx + u},{dy - 20} l{v},20" stroke="{CORAL}" stroke-width="2.6" stroke-linecap="round"/>' for u, v in ((-16, -3), (-11, 2), (12, 1), (17, 4)))
            + f'<path d="M{dx+27},{dy-61} C{dx+24},{dy-74} {dx+16},{dy-80} {dx+8},{dy-84} M{dx+22},{dy-72} l-8,-2 M{dx+17},{dy-78} l-3,-8 '
              f'M{dx+30},{dy-62} C{dx+34},{dy-76} {dx+42},{dy-82} {dx+50},{dy-86} M{dx+36},{dy-74} l6,-6 M{dx+43},{dy-80} l1,-8" '
              f'stroke="{CORAL}" stroke-width="2" fill="none" stroke-linecap="round"/>')
    p.add(f'<g transform="translate({dx} {dy}) scale(1.4) translate({-dx} {-dy})">{deer}</g>')
    # kmene bukov
    for x, w in ((330, 34), (672, 36), (215, 58), (795, 66), (70, 118), (945, 128)):
        beech_trunk(p, x, w, NAVY, TEAL, CREAM, rnd)
    # koruna — koralové masy, bukové listy
    for _ in range(20):
        x = rnd.uniform(-80, W + 80)
        y = rnd.uniform(-60, 170) if not (380 < x < 620) else rnd.uniform(-140, -30)
        rx_, ry_ = rnd.uniform(100, 160), rnd.uniform(60, 95)
        p.add(f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(rx_)}" ry="{f(ry_)}" fill="{CORAL}"/>'
              f'<ellipse cx="{f(x + rx_*.15)}" cy="{f(y + ry_*.35)}" rx="{f(rx_*.8)}" ry="{f(ry_*.5)}" fill="{CORAL2}" opacity=".6"/>')
    for _ in range(260):
        x = rnd.uniform(-10, W + 10)
        y = rnd.uniform(-10, 230) if not (380 < x < 620) else rnd.uniform(-10, 70)
        p.add(K.leaf(x, y, rnd.uniform(14, 24), rnd.uniform(5, 8), rnd.uniform(0, 360), rnd.choice([NAVY, CREAM, CORAL2, NAVY]), rnd.choice([CORAL, None])))
    for _ in range(40):  # padajúce lístie
        x, y = rnd.uniform(IX0, IX1), rnd.uniform(240, 1150)
        p.add(K.leaf(x, y, rnd.uniform(10, 16), rnd.uniform(3.5, 5.5), rnd.uniform(0, 360), rnd.choice([CORAL, CREAM]), None))
    # padnutý kmeň a rys
    p.add(f'<path d="M-10,1148 L392,1108 C404,1112 408,1150 398,1160 L-10,1200Z" fill="{CORAL}"/>'
          f'<path d="M-10,1176 L396,1136" stroke="{CORAL2}" stroke-width="5"/>'
          + "".join(f'<path d="M{x},{1150 - x*.1} q14,-4 26,0" stroke="{CORAL2}" stroke-width="2" fill="none"/>' for x in range(20, 360, 45)) +
          f'<ellipse cx="398" cy="1134" rx="14" ry="26" fill="{CREAM}"/>' +
          "".join(f'<ellipse cx="398" cy="1134" rx="{14*k/4}" ry="{26*k/4}" fill="none" stroke="{CORAL}" stroke-width="1.2"/>' for k in (1, 2, 3)))
    p.add(K.leaf(300, 1098, 40, 10, -150, TEAL, NAVY))
    p.add(lynx(215, 1134, 105, CREAM, NAVY, "#d3c6aa"))
    # huby
    for mx, my, ms in ((200, 1300, 24), (236, 1318, 17), (840, 1250, 26)):
        p.add(f'<path d="M{mx - ms*.25},{my} L{mx - ms*.18},{my - ms} H{mx + ms*.18} L{mx + ms*.25},{my}Z" fill="{CREAM}"/>'
              f'<path d="M{mx - ms},{my - ms*.9} Q{mx},{my - ms*2} {mx + ms},{my - ms*.9}Z" fill="{CORAL2}"/>'
              + "".join(f'<circle cx="{mx + u*ms}" cy="{my - ms*v}" r="{ms*.1}" fill="{CREAM}"/>' for u, v in ((-.4, 1.2), (.2, 1.4), (.5, 1.05))))
    for x, a, L in [(40, 70, 230), (110, 100, 170), (880, 110, 240), (960, 85, 190), (800, 70, 150), (690, 95, 100), (300, 88, 90)]:
        p.add(K.fern(x, H - 10, L, a, CORAL, CORAL, curl=.2))
    title(p, "BUČINA", "JAVORNÍKY · SLOVENSKO", CREAM, y=1305)
    p.render("09-bucina.svg", speck=.3, light_speck=.3, mottle=.15)


# ====================================================================== 10 VEĽKÝ JAVORNÍK

def p10():
    p = Poster("Veľký Javorník")
    rnd = random.Random(10)
    sky = p.lg([(0, "#cfd8c4"), (.45, "#f1e6bd"), (1, "#fdf0cf")], user=(0, 0, 0, 640))
    p.add(f'<rect width="{W}" height="{H}" fill="{sky}"/>')
    sx, sy = 230, 385
    K.glow(p, sx, sy, 420, "#fffbe8", 1)
    p.add(f'<circle cx="{sx}" cy="{sy}" r="34" fill="#fffef6"/>')
    K.rays(p, sx, sy, list(range(-60, 80, 9)), 1100, "#fffbe6", op=.22, width=.03)
    for cx, cy, w, h, s in [(230, 120, 520, 140, 1), (780, 90, 560, 160, 2), (620, 270, 380, 90, 3), (90, 300, 240, 60, 4)]:
        K.cloud(p, cx, cy, w, h, "#fffbea", "#efe4bd", "#cdc39a", seed=s, op=.95)
    layers = [(450, "#c5d7cb", "#e6ecd9"), (505, "#aac6bd", "#d2dfd2"), (565, "#8eb1ac", "#bfd2c9"),
              (635, "#729a98", "#a6c2bb"), (715, "#5a8385", "#8eaeaa"), (800, "#476e72", "#7a9c99")]
    for i, (base, c1, c2) in enumerate(layers):
        pts = R(base, [(rnd.uniform(0, W), rnd.uniform(30, 70), rnd.uniform(140, 240)) for _ in range(4)], 50 + i)
        K.hill(p, pts, c1, c2, depth=160, rim="#fffbe6" if i < 5 else "#f6efcf", rim_w=1.2 + i * .2, rim_op=.8)
        if i >= 2:
            p.add(K.tree_row(pts, -10, W + 10, 5 + i, lambda x, y, r, i=i, c1=c1: K.spruce_simple(x, y + 6 + i, r.uniform(7, 11) * (i - 1), c1, c2), rnd))
        for _ in range(2):
            K.fog(p, rnd.uniform(100, 900), base + 45, rnd.uniform(500, 900), 40 + i * 8, "#fdf9ea", .8)
    for cx, cy, w, h, s in [(90, 760, 320, 80, 7), (440, 720, 240, 60, 8), (920, 840, 200, 50, 9)]:
        K.cloud(p, cx, cy, w, h, "#fffdf3", "#ece8d6", "#c9d0c4", seed=s)
    for bx, by, bs in ((330, 560, 1), (356, 578, .8), (380, 566, .7)):
        p.add(f'<path d="M{bx},{by} q{6*bs},{-6*bs} {11*bs},0 q{5*bs},{-6*bs} {11*bs},0" stroke="#3b4b45" stroke-width="2" fill="none"/>')
    # vrcholová lúka
    summit = [(-20, 1080), (120, 990), (330, 880), (500, 800), (640, 762), (800, 752), (1020, 764)]
    d = K.hill(p, summit, "#b4bd57", "#2d4a24", depth=640, tex=["#d6d170", "#5d7a2c", "#8fa23c", "#3b5a28"], n=1600, L=18, wid=2.6,
               op=.55, rim="#fff4c0", rim_w=3, seed=10)
    greens = [("#253d20", "#4a6a2a", "#7f9a36"), ("#2f4a24", "#5b7a2e", "#a3b440"), ("#3a5426", "#86a03a", "#d0c753"),
              ("#44602a", "#a2b344", "#eadb66")]
    reds = [("#4a1d15", "#8f3325", "#c9553a"), ("#5a2a16", "#a4522a", "#d9853f")]
    cid = K.clip(p, d)
    items = []
    for _ in range(700):
        x = rnd.uniform(-20, W + 20)
        dep = rnd.random() ** 1.25
        items.append((y_at(summit, min(max(x, -20), 1020)) + 8 + dep * 660, x, dep))
    out = []
    for y, x, dep in sorted(items):
        r = 3 + dep * 24 * rnd.uniform(.7, 1.2)
        c = rnd.choice(reds) if rnd.random() < .14 else rnd.choice(greens if dep > .25 else greens[2:])
        parts = [(x + rnd.uniform(-r, r), y + rnd.uniform(-r*.3, r*.3), r * rnd.uniform(.45, .75)) for _ in range(5)]
        out += [f'<ellipse cx="{f(a)}" cy="{f(b)}" rx="{f(q*1.3)}" ry="{f(q*.7)}" fill="{c[0]}"/>' for a, b, q in parts]
        out += [f'<ellipse cx="{f(a - q*.25)}" cy="{f(b - q*.25)}" rx="{f(q)}" ry="{f(q*.5)}" fill="{c[1]}"/>' for a, b, q in parts]
        out += [f'<ellipse cx="{f(a - q*.5)}" cy="{f(b - q*.4)}" rx="{f(q*.45)}" ry="{f(q*.22)}" fill="{c[2]}"/>' for a, b, q in parts[:3]]
    p.add(f'<g clip-path="url(#{cid})">' + "".join(out) + "</g>")
    # chodník na vrchol
    p.add(f'<path d="M480,{H} C520,1200 560,1000 640,880 C680,820 720,790 760,772" stroke="#d8c98a" stroke-width="22" fill="none" opacity=".55" stroke-linecap="round"/>'
          f'<path d="M480,{H} C520,1200 560,1000 640,880 C680,820 720,790 760,772" stroke="#b0a060" stroke-width="3" fill="none" opacity=".6" stroke-dasharray="6 10"/>')
    # rázcestník
    sx_, sy_ = 700, 766
    p.add(f'<rect x="{sx_-2}" y="{sy_-78}" width="5" height="80" fill="#3a2f22"/>'
          + "".join(f'<path d="M{sx_ + (3 if dr > 0 else -2)},{sy_ - yy} h{dr*34} l{dr*7},6 l{-dr*7},6 h{-dr*34}Z" fill="#f2ecd8" stroke="#3a2f22" stroke-width="1.3"/>'
                    f'<rect x="{sx_ + (6 if dr > 0 else -30)}" y="{sy_ - yy + 4}" width="24" height="4" fill="{c}"/>'
                    for dr, yy, c in ((1, 76, "#c64a32"), (-1, 62, "#3b6cb0"), (1, 48, "#c64a32")))
          + f'<rect x="{sx_-9}" y="{sy_-94}" width="20" height="14" fill="#f2ecd8" stroke="#3a2f22" stroke-width="1.3"/>'
          f'<rect x="{sx_-9}" y="{sy_-89}" width="20" height="4" fill="#c64a32"/>')
    # partia bežcov v protisvetle
    for fx, pose, face in ((772, "cheer", 1), (806, "stand", -1), (838, "hike", 1), (872, "cheer", -1)):
        p.add(K.figure(fx, y_at(summit, fx) + 4, 58, "#1d2a22", pose, face=face, rim="#fff6cf"))
    # popredie: čučoriedky a tráva ako rám
    for x, y, s_, sd in ((60, 1400, 190, 1), (180, 1415, 150, 2), (880, 1405, 200, 3), (960, 1380, 150, 4), (760, 1420, 120, 5)):
        p.add(K.bilberry(x, y, s_, "#4a2a1c", ["#2f5a26", "#4d7a2c", "#8a3a22", "#b4552e", "#6d8a36"], "#26305e", "#8c98c8", seed=sd))
    for _ in range(40):
        x, y = rnd.uniform(IX0, IX1), rnd.uniform(1260, H)
        if 270 < x < 730 and y > 1230:
            continue
        p.add(K.tuft(x, y, rnd.uniform(40, 90), ["#1d3318", "#3b5a28", "#8fa23c", "#d6d170"], rnd, n=7))
    bottom_shade(p, "#10200e", 1150, .55)
    title(p, "VEĽKÝ JAVORNÍK", "1072 M · JAVORNÍKY · SLOVENSKO", "#fbf4dc", y=1300)
    p.render("10-velky-javornik.svg", speck=.28, light_speck=.3, mottle=.22)


# ====================================================================== 11 NOC NA HREBENI

def p11():
    p = Poster("Noc na hrebeni")
    rnd = random.Random(11)
    sky = p.lg([(0, "#060a1e"), (.45, "#121f45"), (.8, "#253e6e"), (1, "#3e5d8c")], user=(0, 0, 0, 820))
    p.add(f'<rect width="{W}" height="{H}" fill="{sky}"/>')
    # Mliečna cesta
    p.add(f'<path d="M-80,640 C200,420 560,260 1080,40 L1080,190 C620,360 260,520 -80,760Z" fill="#6b7fb8" opacity=".22" filter="url(#blur20)"/>'
          f'<path d="M-80,690 C220,470 560,300 1080,100 L1080,130 C600,320 250,500 -80,720Z" fill="#c7b8e6" opacity=".18" filter="url(#blur8)"/>'
          f'<path d="M-40,700 C240,500 600,330 1060,120" stroke="#0b1230" stroke-width="16" fill="none" opacity=".45" filter="url(#blur8)"/>')
    K.stars(p, 1400, (IX0, IY0, IX1, 800), seed=3, band=(-40, 700, 1060, 110, 60))
    # mesiac
    K.glow(p, 800, 190, 190, "#fff1cc", .5)
    p.add(f'<mask id="mn"><rect width="{W}" height="{H}" fill="#fff"/><circle cx="822" cy="176" r="44" fill="#000"/></mask>'
          f'<circle cx="800" cy="190" r="48" fill="#f8ecc6" mask="url(#mn)"/>')
    cols = [("#2c4270", "#1f325a"), ("#21355f", "#16264a"), ("#18284c", "#101c3a"), ("#0f1a36", "#0a1128"), ("#080d1f", "#050814")]
    bases = [690, 780, 890, 1020, 1160]
    ridges = []
    for i, (base, (c1, c2)) in enumerate(zip(bases, cols)):
        bumps = [(rnd.uniform(0, W), rnd.uniform(40, 90) * (1 + i * .3), rnd.uniform(150, 260)) for _ in range(3)]
        if i == 4:
            bumps = [(560, 120, 420)]
        pts = R(base, bumps, 60 + i)
        ridges.append(pts)
        K.hill(p, pts, c1, c2, depth=200, rim="#9fb6e6", rim_w=1 + i * .3, rim_op=.55 + i * .08)
        if i in (1, 2, 3):
            p.add(K.tree_row(pts, -10, W + 10, 9 + i * 5, lambda x, y, r, i=i, c1=c1, c2=c2:
                             K.spruce(x, y + 5 + i * 4, r.uniform(14, 24) * i, c2, c1, "#4f6aa3", seed=int(x), lit=1), rnd))
        if i < 4:
            span = [(90, 520), (420, 930), (40, 540), (360, 700)][i]
            n = [22, 17, 12, 5][i]
            lamps = []
            for k in range(n):
                x = span[0] + (span[1] - span[0]) * (k + rnd.uniform(-.2, .2)) / n
                lamps.append((x, y_at(pts, x) + 5 + i * 4))
            p.add(f'<path d="{smooth_path(lamps)}" stroke="#ffe9a8" stroke-width="{.6 + i*.3}" fill="none" opacity=".25" filter="url(#glow)"/>')
            for x, y in lamps:
                p.add(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(1.3 + i * 1.1)}" fill="#fff2c2" filter="url(#glow)"/>')
        if i == 2:  # kontrola: stan s ohňom
            tx = 780
            ty = y_at(pts, tx) + 22
            K.glow(p, tx, ty - 10, 90, "#ffb35c", .55)
            p.add(f'<path d="M{tx-30},{ty} L{tx},{ty-34} L{tx+30},{ty}Z" fill="#ffcc7a"/><path d="M{tx},{ty-34} L{tx+30},{ty} L{tx+12},{ty}Z" fill="#e89a4a"/>'
                  f'<path d="M{tx-4},{ty} L{tx},{ty-14} L{tx+4},{ty}Z" fill="#6b3a1a"/>'
                  + "".join(f'<circle cx="{tx - 60 + k*13}" cy="{ty - 40 + math.sin(k)*3}" r="1.8" fill="#ffe29a" filter="url(#glow)"/>' for k in range(10)))
            p.add(K.figure(tx + 46, ty, 18, "#0b1020", "stand", face=-1))
    # bežec v popredí
    near = ridges[-1]
    rx = 600
    ry = y_at(near, rx) + 3
    beam = p.lg([(0, "#fff3c4", .5), (1, "#fff3c4", 0)], user=(rx - 20, 0, rx - 330, 0))
    p.add(f'<path d="M{rx - 26},{ry - 82} L{rx - 340},{ry - 40} L{rx - 330},{ry + 22}Z" fill="{beam}"/>')
    K.glow(p, rx - 230, ry + 4, 90, "#fff3c4", .25)
    for _ in range(30):  # osvetlená tráva v kuželi
        x = rx - rnd.uniform(90, 320)
        p.add(K.tuft(x, y_at(near, x) + rnd.uniform(4, 14), rnd.uniform(8, 18), ["#8a8f7a", "#cfcaa0", "#5c6070"], rnd, n=4))
    p.add(K.figure(rx, ry, 92, "#04060d", "hike", face=-1, rim="#a9bfe9", lamp="#fffbe0"))
    for x, hh, sd in ((-20, 560, 1), (90, 400, 2), (1010, 600, 3), (900, 420, 4)):
        p.add(K.spruce(x, H + 30, hh, "#03050c", "#0b1226", "#1a2748", seed=sd, lit=1 if x > 500 else -1, rim="#8fa6d8", rim_w=.9))
    for _ in range(40):
        x, y = rnd.uniform(IX0, IX1), rnd.uniform(1230, H)
        if 270 < x < 730 and y > 1230:
            continue
        p.add(K.tuft(x, y, rnd.uniform(30, 60), ["#03050c", "#0b1226"], rnd, n=6))
    title(p, "NOC NA HREBENI", "105 KM · +4030 M · JAVORNÍKY", "#ece5cf", y=1300)
    p.render("11-noc-na-hrebeni.svg", speck=.15, light_speck=.2, mottle=.2)


# ====================================================================== 12 MAKYTA

def p12():
    p = Poster("Makyta")
    rnd = random.Random(12)
    NAVY, NAVY2, NAVY3 = "#1c2f52", "#34507a", "#7d9dc6"
    sky = p.lg([(0, "#256fb3"), (.55, "#6fb2da"), (1, "#e9eedb")], user=(0, 0, 0, 640))
    p.add(f'<rect width="{W}" height="{H}" fill="{sky}"/>')
    K.glow(p, 80, 560, 420, "#fff4d0", .55)
    for cx, cy, w, h, s in [(250, 190, 460, 130, 1), (800, 140, 420, 120, 2), (590, 360, 320, 80, 3), (110, 450, 220, 50, 4), (920, 430, 200, 50, 5)]:
        K.cloud(p, cx, cy, w, h, "#fffdf5", "#dfe9ee", "#9fbbd1", seed=s)
    K.wisp(p, 500, 520, 700, 14, "#ffffff", .5)
    far = R(610, [(280, 60, 200), (720, 140, 160)], 71)  # Makyta vpravo
    K.hill(p, far, "#8da7ba", "#bccfd6", depth=160, rim="#f3f6ef", rim_w=1.5)
    p.add(K.tree_row(far, -10, W + 10, 5, lambda x, y, r: K.spruce_simple(x, y + 5, r.uniform(8, 12), "#7b98ab"), rnd))
    K.fog(p, 500, 660, 1100, 60, "#eef1e4", .6)
    mid = R(770, [(150, 110, 220), (600, 60, 200), (900, 90, 160)], 72)
    d = K.hill(p, mid, "#a9502a", "#7e3a22", depth=260)
    autumn = [("#8e3f22", "#c96a2b", "#eaa23e"), ("#9a4a1f", "#dc8a2f", "#f3c44e"), ("#7a3520", "#b8552a", "#e0873a"),
              ("#6e4a1a", "#b98a2a", "#e8c45a"), ("#5a3a1c", "#8f6a2a", "#c9a24a")]
    K.crowns(p, mid, 150, 2600, autumn, 4.2, seed=72, clip_d=d)
    for gx in (140, 420, 610, 880):
        p.add(K.tree_row(mid, gx - 40, gx + 40, 14, lambda x, y, r: K.spruce(x, y + r.uniform(40, 110), r.uniform(40, 62), NAVY, NAVY2, NAVY3, seed=int(x)), rnd))
    meadow = R(940, [(250, 110, 260), (800, 60, 240)], 73)
    K.hill(p, meadow, "#f0c452", "#c98f24", depth=300, tex=["#ffe08a", "#c98f24", "#e3ae3a"], n=700, L=18, wid=2.6, op=.5, rim="#fff2c2", rim_w=2, seed=73)
    # drevenica s dymom
    hx = 700
    hy = y_at(meadow, hx) + 42
    svg, chim = K.cabin34(hx, hy, 30, "#8a6444", "#5e3f2a", "#3e2a1c", "#4a3326", "#2a1d15", "#fff0c8", "#f1d9a0", seed=2)
    p.add(f'<path d="M{hx},{hy} L{hx + 160},{hy + 18} L{hx + 150},{hy + 30} L{hx},{hy + 8}Z" fill="#9a6a1c" opacity=".35"/>')
    p.add(svg)
    p.add(f'<path d="M{f(chim[0])},{f(chim[1])} C{f(chim[0] + 20)},{f(chim[1] - 40)} {f(chim[0] - 10)},{f(chim[1] - 80)} {f(chim[0] + 30)},{f(chim[1] - 130)}" '
          f'stroke="#f4f0e6" stroke-width="12" fill="none" opacity=".6" stroke-linecap="round" filter="url(#blur8)"/>')
    # stádo, bača a pes
    flock = sorted((y_at(meadow, sx) + 60 + rnd.uniform(0, 130), sx) for sx in [rnd.uniform(380, 660) for _ in range(20)])
    for sy, sx in flock:
        s_ = 12 + (sy - 880) * .07
        p.add(f'<ellipse cx="{f(sx + s_*.8)}" cy="{f(sy)}" rx="{f(s_*.9)}" ry="{f(s_*.12)}" fill="#9a6a1c" opacity=".35"/>')
        p.add(K.sheep(sx, sy, s_, "#fbf7ec", "#d6cbb2", "#2a2622", rnd, face=1 if rnd.random() < .6 else -1))
    bx = 560
    by = y_at(meadow, bx) + 175
    p.add(f'<ellipse cx="{bx + 30}" cy="{by}" rx="40" ry="5" fill="#9a6a1c" opacity=".35"/>')
    p.add(K.figure(bx, by, 64, "#2c2420", "stand", face=1, hat=True, pack=False))
    p.add(f'<g fill="#1e1a18"><ellipse cx="{bx + 50}" cy="{by - 12}" rx="14" ry="7"/><circle cx="{bx + 64}" cy="{by - 20}" r="6"/>'
          f'<path d="M{bx + 38},{by - 12} l-8,-8" stroke="#1e1a18" stroke-width="3"/>'
          + "".join(f'<rect x="{bx + u}" y="{by - 8}" width="3" height="8"/>' for u in (40, 44, 55, 59)) +
          f'</g><ellipse cx="{bx + 54}" cy="{by - 11}" rx="6" ry="4" fill="#f3efe4"/>')
    # popredie — kopy sena na ostrvách a žrďový plot
    fg = R(1140, [(260, 70, 300), (820, 40, 250)], 74)
    K.hill(p, fg, "#e9b43e", "#8f5f16", depth=300, tex=["#ffd774", "#a06a18", "#d4992c"], n=900, L=24, wid=3.2, op=.55, rim="#ffeab0", rim_w=2.5, seed=74)
    for i, x in enumerate(range(560, 1020, 64)):
        yy = y_at(fg, x) + 20
        p.add(f'<path d="M{x},{yy} v-70" stroke="#4a3322" stroke-width="7" stroke-linecap="round"/>'
              f'<path d="M{x},{yy - 70} v40" stroke="#c9a070" stroke-width="2"/>')
        if x + 64 < 1020:
            y2 = y_at(fg, x + 64) + 20
            p.add(f'<path d="M{x},{yy - 52} L{x + 64},{y2 - 52} M{x},{yy - 26} L{x + 64},{y2 - 26}" stroke="#5a3e28" stroke-width="5"/>'
                  f'<path d="M{x},{yy - 55} L{x + 64},{y2 - 55}" stroke="#d6ad76" stroke-width="1.5"/>')
    for x, s_, sd in ((380, 115, 3), (170, 225, 1), (880, 210, 4)):
        p.add(K.haystack(x, y_at(fg, x) + s_ * .42, s_, "#f0cf72", "#c99b3e", "#7e5a22", "#fbe7a6", "#3a2b1c", seed=sd, shadow="#6b420c", lit_side=-1))
    p.add(K.rowan(-30, 560, 250, 700, 110, "#3b2418", ["#6b7a2c", "#8a9a38", "#b9a43e", "#c96a2b"], "#c8321e", "#ff9d7d", seed=5, bend=-.1))
    for _ in range(45):
        x, y = rnd.uniform(IX0, IX1), rnd.uniform(1240, H)
        if 270 < x < 730 and y > 1230:
            continue
        p.add(K.tuft(x, y, rnd.uniform(30, 75), [NAVY, "#7e5a22", "#c98f24"], rnd, n=6))
    bottom_shade(p, "#4a2a06", 1170, .4)
    title(p, "MAKYTA", "JAVORNÍKY · SLOVENSKO", "#fff6de", y=1300)
    p.render("12-makyta.svg", speck=.32, light_speck=.3, mottle=.22)


if __name__ == "__main__":
    import sys
    which = sys.argv[1:] or ["07", "08", "09", "10", "11", "12"]
    for k in which:
        globals()[f"p{k}"]()
