"""第 10 类 · 自然与地理：s092–s100（平面 MG，层层远近叠层 + 空气感）"""
from core import *
import math, random


# ---------- 本模块小工具 ----------
def smooth(pts, close_to=None):
    d = f'M{pts[0][0]:.1f},{pts[0][1]:.1f}'
    for i in range(1, len(pts) - 1):
        mx, my = (pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2
        d += f' Q{pts[i][0]:.1f},{pts[i][1]:.1f} {mx:.1f},{my:.1f}'
    d += f' L{pts[-1][0]:.1f},{pts[-1][1]:.1f}'
    if close_to is not None:
        d += f' L{pts[-1][0]:.1f},{close_to} L{pts[0][0]:.1f},{close_to}Z'
    return d


def wave_pts(y, amp, seed, step=160, x0=-80, x1=W + 80, sharp=False):
    random.seed(seed); pts = []; x = x0; ph = random.random() * 6
    while x <= x1 + step:
        k = .5 + .5 * math.sin(x / 300 + ph) if not sharp else random.random()
        pts.append((x, y - amp * (.35 + .65 * k) - random.uniform(0, amp * .15))); x += step
    return pts


def hill(s, y, amp, seed, col, step=160, bottom=H, fade=None):
    fillc = col if fade is None else s.lg([(0, col), (1, fade)])
    return P(smooth(wave_pts(y, amp, seed, step), bottom), fillc)


def ring(x, y, r, col, w, op=1):
    return S(f'M{x - r},{y} a{r},{r} 0 1,0 {2 * r},0 a{r},{r} 0 1,0 {-2 * r},0', col, w, op)


def haze(s, y0, y1, col, op=.8):
    return R(0, y0, W, y1 - y0, s.lg([(0, col, 0), (.6, col, op), (1, col, 0)]))


def sun(x, y, r, col, op_glow=.45):
    return G([C(x, y, r * 2.6, col, op_glow * .5, 'filter="url(#b40)"'), C(x, y, r * 1.5, col, op_glow, 'filter="url(#b20)"'), C(x, y, r, col)])


def bird(x, y, sc, col):
    return S(f'M{x},{y} q{12 * sc},{-10 * sc} {22 * sc},0 q{10 * sc},{-10 * sc} {22 * sc},0', col, 3 * sc)


def palm(x, y, h, lean, trunk, trunk2, leaf, leaf2, sc=1):
    """椰子树：x,y 树根，lean 向右偏移"""
    tx, ty = x + lean, y - h
    it = [S(f'M{x},{y} Q{x + lean * .2},{y - h * .55} {tx},{ty}', trunk, 26 * sc)]
    for k in range(1, 9):
        u = k / 9; px = (1 - u) ** 2 * x + 2 * u * (1 - u) * (x + lean * .2) + u * u * tx; py = (1 - u) ** 2 * y + 2 * u * (1 - u) * (y - h * .55) + u * u * ty
        it.append(S(f'M{px - 12 * sc:.0f},{py:.0f} L{px + 12 * sc:.0f},{py - 4 * sc:.0f}', trunk2, 4 * sc, .8))
    for a, ln, col in [(-170, 170, leaf), (-140, 190, leaf2), (-105, 150, leaf), (-60, 180, leaf2), (-25, 190, leaf), (10, 160, leaf2), (-80, 120, leaf)]:
        r = math.radians(a); ex, ey = tx + ln * sc * math.cos(r), ty + ln * sc * math.sin(r) + 40 * sc
        mx, my = tx + ln * sc * .5 * math.cos(r), ty + ln * sc * .5 * math.sin(r) - 30 * sc
        nx, ny = -math.sin(r) * 26 * sc, math.cos(r) * 26 * sc
        it.append(P(f'M{tx},{ty} Q{mx - nx:.0f},{my - ny:.0f} {ex:.0f},{ey:.0f} Q{mx + nx * .3:.0f},{my + ny * .3:.0f} {tx},{ty}Z', col))
    it += [C(tx - 8 * sc, ty + 10 * sc, 11 * sc, trunk2), C(tx + 10 * sc, ty + 12 * sc, 11 * sc, trunk2)]
    return G(it)


# ============ s092 草原 ============
def grassland():
    s = Scene('s092', '草原', '自然与地理', ['科学', '地理', '民族文化', '生态'],
              dict(sky1='#6EC1EC', sky2='#E3F5FF', sun='#FFF1B8', mtn='#B9D4EA', mtn2='#A6C4E0', far='#BFE3A2', mid='#9DD27C', mid2='#8AC66A', near='#78BA58', near2='#65A84A',
                   river='#9FDDF2', river2='#D8F4FB', yurt='#FFFDF6', yurt2='#E8E1D2', band='#3F86C6', band2='#E2584A', door='#C8463E', sheep='#FFFFFF', sheep2='#3E3A40',
                   horse='#A8683C', horse2='#6E4226', f1='#F7D54A', f2='#F2A0C0', f3='#FFFFFF', eagle='#5A4A42'),
              desc='辽阔草原：远处淡蓝群山、层层起伏的绿色丘陵、蜿蜒小河，白色蒙古包、羊群与骏马，天高云淡。',
              stand={'ground_y': 910, 'x': [480, 1440]})
    s.layer('sky', [R(0, 0, W, 760, s.lg([(0, 'sky1'), (1, 'sky2')])), sun(1580, 170, 60, 'sun')], 'fade', 0)
    s.layer('clouds', [cloud(320, 170, 1.1, op=.95), cloud(900, 110, .7, op=.9), cloud(1300, 250, .55, op=.8), cloud(1760, 330, .45, op=.7)], 'slide-l', .2, loop='drift')
    s.layer('mountains', [hill(s, 600, 170, 3, 'mtn', 220, 760), hill(s, 620, 90, 5, 'mtn2', 180, 760), haze(s, 480, 680, 'sky2', .9)], 'rise', .25)
    s.layer('hills_far', [P(smooth([(-80, 620), (300, 590), (700, 625), (1100, 585), (1500, 615), (2000, 590)], 1080), s.lg([(0, 'far'), (1, 'mid')])),
                          haze(s, 580, 660, 'sky2', .6)], 'rise', .35)
    # 河
    rv = [P('M1180,640 Q1240,660 1120,690 Q960,730 1160,780 Q1400,840 1320,1080 L1620,1080 Q1640,840 1380,770 Q1200,730 1300,690 Q1360,664 1230,640Z', s.lg([(0, 'river2'), (1, 'river')]))]
    s.layer('hills_mid', [P(smooth([(-80, 700), (360, 660), (760, 700), (1180, 668), (1600, 704), (2000, 670)], 1080), s.lg([(0, 'mid'), (1, 'mid2')]))] + rv, 'rise', .45)
    s.layer('river_shine', [S('M1180,700 q20,-4 40,0', '#ffffff', 3, .8), S('M1210,770 q30,-6 60,0', '#ffffff', 4, .8), S('M1420,880 q34,-6 70,0', '#ffffff', 4, .8)], 'fade', 1.0, loop='flow')

    # 蒙古包
    def yurt(x, y, sc):
        w = 120 * sc; h = 70 * sc
        return G([E(x, y, w * 1.2, 12 * sc, '#2a3a20', .15), R(x - w, y - h, 2 * w, h, 'yurt', 6 * sc), R(x - w, y - h, 2 * w, 14 * sc, 'band'), R(x - w, y - h + 22 * sc, 2 * w, 5 * sc, 'band2'),
                  P(f'M{x - w - 10 * sc},{y - h + 4 * sc} Q{x},{y - h - 90 * sc} {x + w + 10 * sc},{y - h + 4 * sc}Z', 'yurt'), P(f'M{x},{y - h - 50 * sc} Q{x + w * .6},{y - h - 30 * sc} {x + w + 10 * sc},{y - h + 4 * sc} L{x},{y - h + 4 * sc}Z', 'yurt2', .6),
                  S(f'M{x - w * .6},{y - h - 26 * sc} Q{x},{y - h - 66 * sc} {x + w * .6},{y - h - 26 * sc}', 'band', 6 * sc), C(x, y - h - 56 * sc, 10 * sc, 'band2'),
                  R(x - 22 * sc, y - 52 * sc, 44 * sc, 52 * sc, 'door', 4 * sc), R(x - 26 * sc, y - 56 * sc, 52 * sc, 8 * sc, 'band', 3)])
    s.layer('yurts', [yurt(420, 700, .9), yurt(640, 712, .65), yurt(1700, 700, .75)], 'pop', .6)

    def sheep(x, y, sc, flip=1):
        it = [E(x, y + 4 * sc, 30 * sc, 5 * sc, '#2a3a20', .15)]
        it += [R(x - 16 * sc, y - 18 * sc, 6 * sc, 22 * sc, 'sheep2', 2), R(x + 10 * sc, y - 18 * sc, 6 * sc, 22 * sc, 'sheep2', 2)]
        for dx, dy, r in [(-16, -28, 14), (0, -34, 16), (16, -28, 14), (-6, -20, 14), (10, -20, 14)]:
            it.append(C(x + dx * sc, y + dy * sc, r * sc, 'sheep'))
        it += [E(x + flip * 30 * sc, y - 30 * sc, 10 * sc, 13 * sc, 'sheep2'), E(x + flip * 24 * sc, y - 38 * sc, 7 * sc, 4 * sc, 'sheep2')]
        return G(it)
    random.seed(12)
    sh = [sheep(x, y, sc, f) for x, y, sc, f in [(820, 760, .8, 1), (880, 772, .7, -1), (760, 784, .9, 1), (940, 790, .75, 1), (700, 760, .6, 1), (1000, 770, .6, -1)]]
    s.layer('sheep', sh, 'pop', .75)

    def horse(x, y, sc, col='horse'):
        return G([E(x, y + 2, 60 * sc, 6 * sc, '#2a3a20', .15), E(x, y - 70 * sc, 56 * sc, 26 * sc, col),
                  *[R(x + dx * sc, y - 60 * sc, 9 * sc, 60 * sc, col, 3) for dx in (-44, -30, 26, 40)],
                  P(f'M{x + 40 * sc},{y - 84 * sc} L{x + 70 * sc},{y - 130 * sc} L{x + 96 * sc},{y - 118 * sc} L{x + 66 * sc},{y - 70 * sc}Z', col),
                  P(f'M{x + 70 * sc},{y - 132 * sc} L{x + 100 * sc},{y - 120 * sc} L{x + 98 * sc},{y - 108 * sc} L{x + 72 * sc},{y - 112 * sc}Z', col),
                  P(f'M{x + 40 * sc},{y - 92 * sc} L{x + 68 * sc},{y - 136 * sc} L{x + 60 * sc},{y - 112 * sc} L{x + 46 * sc},{y - 84 * sc}Z', 'horse2'),
                  P(f'M{x - 54 * sc},{y - 80 * sc} Q{x - 80 * sc},{y - 60 * sc} {x - 70 * sc},{y - 30 * sc} Q{x - 64 * sc},{y - 60 * sc} {x - 50 * sc},{y - 70 * sc}Z', 'horse2')])
    s.layer('horses', [horse(1500, 800, .8), horse(1640, 790, .65, 'horse2')], 'slide-r', .85)
    nr = [P(smooth([(-80, 880), (300, 850), (700, 880), (1100, 870), (1300, 860), (1500, 884), (2000, 850)], 1080), s.lg([(0, 'near'), (1, 'near2')]))]
    random.seed(4)
    for k in range(60):
        x = random.uniform(0, W); y = random.uniform(900, 1060)
        nr.append(S(f'M{x:.0f},{y:.0f} l-6,-16 M{x:.0f},{y:.0f} l2,-20 M{x:.0f},{y:.0f} l8,-14', 'near2', 3, .8))
    s.layer('near', nr, 'rise', .55)
    fw = []
    random.seed(8)
    for k in range(34):
        x = random.uniform(0, 420) if k % 2 else random.uniform(1520, 1900); y = random.uniform(900, 1050)
        fw += [S(f'M{x:.0f},{y:.0f} L{x:.0f},{y - 26:.0f}', 'near2', 3), C(x, y - 30, 7, ['f1', 'f2', 'f3'][k % 3]), C(x, y - 30, 2.6, 'f1' if k % 3 else '#ffffff')]
    s.layer('flowers', fw, 'grow', .95, loop='sway')
    s.layer('eagle', [P('M760,250 Q800,220 840,240 Q880,215 924,232 Q880,244 846,256 L838,262 L830,256 Q796,250 760,250Z', 'eagle')], 'slide-l', 1.1, loop='drift')
    return s


# ============ s093 沙漠绿洲 ============
def desert():
    s = Scene('s093', '沙漠绿洲', '自然与地理', ['科学', '地理', '水资源', '生态'],
              dict(sky1='#8FCDE4', sky2='#FCE6C6', sun='#FFF0C4', far='#F4D2A8', far2='#EFC495', mid='#ECB27A', mid2='#D99A5E', near='#E3A066', near2='#C98048',
                   pool='#3EB8C0', pool2='#9FE3E0', reed='#7BB85E', palm='#3E9A6A', palm2='#5DB57E', trunk='#A9764A', trunk2='#7E5432', camel='#B9763E', camel2='#8E5629',
                   rock='#C98A5A', rock2='#E2AA78', grass='#8CC46A'),
              desc='金色沙漠：层层沙丘由远及近颜色渐深，骆驼商队走过沙脊，中间一汪碧蓝绿洲环绕椰枣树。',
              stand={'ground_y': 920, 'x': [480, 1440]})
    s.layer('sky', [R(0, 0, W, 800, s.lg([(0, 'sky1'), (.75, 'sky2')])), sun(1420, 230, 90, 'sun', .55)], 'fade', 0)
    s.layer('heat', [haze(s, 420, 640, 'sky2', .9)], 'fade', .2)

    def bez(p0, p1, p2, p3, u):
        return tuple((1 - u) ** 3 * a + 3 * u * (1 - u) ** 2 * b + 3 * u * u * (1 - u) * c + u ** 3 * d for a, b, c, d in zip(p0, p1, p2, p3))

    def dune_ctrl(xl, xc, xr, top, base):
        return [((xl, base), (xl + (xc - xl) * .5, base), (xc - (xc - xl) * .3, top), (xc, top)),
                ((xc, top), (xc + (xr - xc) * .2, top), (xr - (xr - xc) * .3, base), (xr, base))]

    def dune_row(ds, base, col, shade, hl=.28):
        it = [R(-10, base - 2, W + 20, H - base + 2, col)]
        for xl, xc, xr, top in ds:
            a, b = dune_ctrl(xl, xc, xr, top, base)
            lit = f'M{xl},{base} C{a[1][0]:.0f},{a[1][1]:.0f} {a[2][0]:.0f},{a[2][1]:.0f} {xc},{top} C{b[1][0]:.0f},{b[1][1]:.0f} {b[2][0]:.0f},{b[2][1]:.0f} {xr},{base}Z'
            sh = (f'M{xc},{top} C{b[1][0]:.0f},{b[1][1]:.0f} {b[2][0]:.0f},{b[2][1]:.0f} {xr},{base} L{xc + (xr - xc) * .18:.0f},{base} '
                  f'C{xc + (xr - xc) * .12:.0f},{top + (base - top) * .6:.0f} {xc + (xr - xc) * .06:.0f},{top + (base - top) * .2:.0f} {xc},{top}Z')
            it += [P(lit, col), P(sh, shade, .75), S(f'M{a[2][0] + (xc - a[2][0]) * .2:.0f},{top + 10:.0f} Q{xc - 10},{top + 1} {xc},{top}', '#ffffff', 3, hl)]
        return G(it)
    far_d = [(-260, 120, 520, 540), (260, 720, 1180, 515), (980, 1380, 1760, 548), (1560, 1880, 2260, 520)]
    s.layer('dunes_far', [dune_row(far_d, 690, 'far', 'far2'), haze(s, 520, 720, 'sky2', .65)], 'rise', .25)

    # 骆驼商队（走在远处沙丘的亮面上）
    def camel(x, y, sc):
        return G([E(x, y - 52 * sc, 40 * sc, 18 * sc, 'camel'), C(x - 8 * sc, y - 66 * sc, 16 * sc, 'camel'),
                  *[R(x + dx * sc, y - 46 * sc, 5 * sc, 46 * sc, 'camel', 2) for dx in (-30, -20, 18, 28)],
                  P(f'M{x + 32 * sc},{y - 58 * sc} Q{x + 48 * sc},{y - 64 * sc} {x + 50 * sc},{y - 88 * sc} L{x + 64 * sc},{y - 88 * sc} L{x + 62 * sc},{y - 80 * sc} L{x + 56 * sc},{y - 78 * sc} Q{x + 54 * sc},{y - 52 * sc} {x + 34 * sc},{y - 46 * sc}Z', 'camel'),
                  R(x - 18 * sc, y - 80 * sc, 18 * sc, 10 * sc, 'camel2', 3)])
    a, _ = dune_ctrl(*far_d[3][:3], far_d[3][3], 690)
    cam = []
    for u in (.5, .62, .74):
        x, y = bez(*a, u); cam.append(camel(x, y + 3, .75))
    s.layer('caravan', [G(cam, 'opacity=".9"')], 'slide-l', .5)
    mid_d = [(-300, 160, 640, 700), (420, 900, 1380, 720), (1200, 1640, 2200, 690)]
    s.layer('dunes_mid', [dune_row(mid_d, 800, 'mid', 'mid2', .35), haze(s, 700, 800, 'sky2', .3)], 'rise', .4)
    # 绿洲
    ox, oy = 960, 800
    oa = [E(ox, oy + 6, 420, 64, 'grass', .9), E(ox, oy, 360, 48, 'pool'), E(ox - 40, oy - 10, 260, 26, 'pool2', .7), E(ox + 60, oy + 10, 140, 10, '#ffffff', .25)]
    random.seed(3)
    for k in range(18):
        x = ox - 400 + k * 47 + random.uniform(-10, 10)
        if abs(x - ox) < 300 and k % 3: continue
        oa += [S(f'M{x:.0f},{oy + 40} Q{x - 6:.0f},{oy + 10} {x - 14:.0f},{oy - 6}', 'reed', 4), S(f'M{x:.0f},{oy + 40} Q{x + 4:.0f},{oy + 6} {x + 10:.0f},{oy - 12}', 'reed', 4)]
    s.layer('oasis', oa, 'grow', .55)
    s.layer('pool_shine', [S(f'M{ox - 160},{oy - 6} q30,-6 60,0', '#ffffff', 4, .8), S(f'M{ox + 60},{oy + 14} q40,-6 80,0', '#ffffff', 4, .7)], 'fade', 1.0, loop='flow')
    s.layer('palms', [palm(640, 830, 300, -40, 'trunk', 'trunk2', 'palm', 'palm2', .95), palm(760, 820, 220, 30, 'trunk', 'trunk2', 'palm2', 'palm', .75),
                      palm(1260, 830, 330, 50, 'trunk', 'trunk2', 'palm', 'palm2', 1.0), palm(1150, 816, 200, -20, 'trunk', 'trunk2', 'palm2', 'palm', .7)], 'grow', .7, loop='sway')
    # 近景沙丘（左右，中间低）
    nd = [P('M-60,880 Q300,800 620,900 Q900,960 1300,920 Q1600,880 1980,820 L1980,1080 L-60,1080Z', s.lg([(0, 'near'), (1, 'near2')]))]
    nd += [P('M-60,880 Q300,800 620,900 Q380,850 -60,920Z', '#ffffff', .18), S('M1500,890 Q1700,860 1980,830', '#ffffff', 3, .3)]
    for k in range(8):
        y = 960 + k * 14; nd.append(S(f'M{80 + k * 30},{y} q60,-10 120,0 t120,0', 'near2', 2, .35))
        nd.append(S(f'M{1400 + k * 20},{y - 30} q60,-10 120,0 t120,0', 'near2', 2, .35))
    s.layer('dunes_near', nd, 'rise', .6)
    rk = [E(260, 900, 80, 14, '#5a3a20', .15), P('M180,900 Q190,840 240,830 Q300,826 320,860 Q336,890 330,900Z', 'rock'), P('M200,880 Q214,846 250,842 Q240,862 200,880Z', 'rock2', .8),
          E(1700, 880, 60, 10, '#5a3a20', .15), P('M1650,880 Q1660,846 1700,842 Q1740,846 1750,880Z', 'rock'), P('M1664,868 Q1676,852 1698,850 Q1688,862 1664,868Z', 'rock2', .8)]
    s.layer('rocks', rk, 'pop', .8)
    s.layer('birds', [bird(1100, 330, 1, 'camel2'), bird(1160, 300, .8, 'camel2')], 'slide-l', 1.0, loop='drift')
    s.layer('sand_drift', [S('M200,940 q80,-12 160,0', '#ffffff', 3, .35), S('M1500,900 q80,-12 160,0', '#ffffff', 3, .35), S('M900,1000 q60,-8 120,0', '#ffffff', 3, .3)], 'fade', 1.1, loop='flow')
    return s


# ============ s094 雪山 ============
def snowmtn():
    s = Scene('s094', '雪山', '自然与地理', ['科学', '地理', '冬季运动', '气候'],
              dict(sky1='#7FB7E8', sky2='#EAF4FD', sun='#FFFFFF', far='#C6D6F0', far2='#AFC2E6', mid='#8FA8D6', mid2='#7790C4', snow='#FFFFFF', snow2='#DCE8F7',
                   lake='#A9D8EE', lake2='#E2F4FC', pine='#3E7C86', pine2='#2E6470', trunk='#6E5246', cabin='#C77B4E', cabin2='#9E5A36', roof='#FFFFFF', win='#FFD27A', smoke='#FFFFFF', flake='#FFFFFF'),
              desc='晴朗雪山：远近三层雪峰（冷蓝到淡紫），山脚冰湖倒映，雪松林与冒着炊烟的小木屋，雪花轻舞。',
              stand={'ground_y': 910, 'x': [480, 1440]})
    s.layer('sky', [R(0, 0, W, 760, s.lg([(0, 'sky1'), (1, 'sky2')])), sun(380, 170, 50, 'sun', .5)], 'fade', 0)
    s.layer('clouds', [cloud(1500, 150, .7, op=.85), cloud(800, 120, .45, op=.7)], 'slide-l', .2)

    def range_(pk, col, shade, bottom, snow_k):
        it = []
        for x, y, w in pk:
            it += [poly([(x - w, bottom), (x, y), (x + w, bottom)], col), poly([(x, y), (x + w, bottom), (x + w * .1, bottom)], shade, .6)]
            h = (bottom - y) * snow_k; sw = w * snow_k
            zig = [(x - sw, y + h)]
            for k in range(1, 6):
                zig.append((x - sw + 2 * sw * k / 6, y + h + (-h * .22 if k % 2 else h * .12)))
            zig.append((x + sw, y + h))
            it.append(poly([(x, y)] + zig[::-1], 'snow'))
            it.append(poly([(x, y), (x + sw, y + h), (x + sw * .66, y + h - h * .22), (x + sw * .2, y + h * .8)], 'snow2', .9))
        return G(it)
    s.layer('peaks_far', [range_([(260, 300, 360), (760, 220, 420), (1240, 280, 380), (1700, 240, 400)], 'far', 'far2', 720, .42), haze(s, 520, 740, 'sky2', .85)], 'rise', .25)
    s.layer('peaks_mid', [range_([(-40, 420, 360), (520, 380, 380), (1460, 360, 420), (2000, 430, 360)], 'mid', 'mid2', 800, .36), haze(s, 640, 800, 'sky2', .7)], 'rise', .4)
    # 冰湖
    lk = [R(0, 760, W, 120, s.lg([(0, 'lake2'), (1, 'lake')]))]
    lk += [G([poly([(520 - 300, 760), (520, 900), (520 + 300, 760)], 'mid', .25), poly([(1460, 940), (1460 - 320, 760), (1460 + 320, 760)], 'mid', .25)], '')]
    s.layer('lake', lk, 'fade', .45)
    s.layer('lake_shine', [S('M300,800 q40,-6 80,0', '#ffffff', 4, .8), S('M1100,830 q50,-6 100,0', '#ffffff', 4, .8), S('M760,790 q30,-4 60,0', '#ffffff', 3, .7)], 'fade', 1.0, loop='flow')

    def snowpine(x, y, sc):
        it = [R(x - 7 * sc, y - 40 * sc, 14 * sc, 40 * sc, 'trunk', 3)]
        for k in range(4):
            w = (80 - k * 16) * sc; yy = y - 30 * sc - k * 50 * sc
            it += [poly([(x - w, yy), (x + w, yy), (x, yy - 90 * sc)], 'pine'), poly([(x, yy), (x + w, yy), (x, yy - 90 * sc)], 'pine2', .5),
                   P(f'M{x - w * .7:.0f},{yy - 22 * sc:.0f} Q{x:.0f},{yy - 40 * sc:.0f} {x + w * .7:.0f},{yy - 22 * sc:.0f} L{x + w * .45:.0f},{yy - 46 * sc:.0f} Q{x:.0f},{yy - 66 * sc:.0f} {x - w * .45:.0f},{yy - 46 * sc:.0f}Z', 'snow', .95)]
        it.append(poly([(x - 14 * sc, y - 210 * sc), (x, y - 240 * sc), (x + 14 * sc, y - 210 * sc)], 'snow'))
        return G(it)
    # 近景雪坡 + 雪松 + 小屋
    sl = [P('M-60,860 Q300,800 700,880 Q1000,930 1300,880 Q1600,830 1980,850 L1980,1080 L-60,1080Z', s.lg([(0, 'snow'), (1, 'snow2')])),
          P('M-60,860 Q300,800 700,880 Q400,846 -60,900Z', 'snow2', .6), P('M1300,880 Q1600,830 1980,850 L1980,880 Q1600,860 1300,880Z', 'snow2', .6)]
    s.layer('snow_slope', sl, 'rise', .55)
    s.layer('pines', [snowpine(x, y, sc) for x, y, sc in [(80, 880, 1.1), (200, 870, .8), (330, 860, .65), (1620, 860, .7), (1740, 870, .95), (1870, 880, 1.15)]], 'grow', .65)
    cx, cy = 470, 870
    cb = [E(cx, cy + 6, 130, 12, '#3a4a6a', .15), R(cx - 100, cy - 100, 200, 100, 'cabin', 6), *[R(cx - 100, cy - 100 + k * 20, 200, 3, 'cabin2', 0, .7) for k in range(1, 5)],
          P(f'M{cx - 126},{cy - 94} L{cx},{cy - 180} L{cx + 126},{cy - 94}Z', 'cabin2'), P(f'M{cx - 136},{cy - 90} L{cx},{cy - 192} L{cx + 136},{cy - 90} L{cx + 116},{cy - 84} L{cx},{cy - 170} L{cx - 116},{cy - 84}Z', 'roof'),
          R(cx + 50, cy - 196, 30, 60, 'cabin2', 4), R(cx + 46, cy - 204, 38, 14, 'roof', 6), R(cx - 70, cy - 76, 50, 44, 'win', 6), R(cx - 46, cy - 76, 3, 44, 'cabin2'), R(cx + 14, cy - 80, 50, 80, 'cabin2', 6),
          P(f'M{cx - 110},{cy} Q{cx},{cy - 20} {cx + 110},{cy}Z', 'snow')]
    s.layer('cabin', cb, 'pop', .8)
    s.layer('cabin_glow', [C(cx - 45, cy - 54, 50, 'win', .45, 'filter="url(#b20)"')], 'fade', 1.0, loop='glow')
    s.layer('smoke', [C(cx + 66, cy - 226, 14, 'smoke', .7), C(cx + 80, cy - 256, 20, 'smoke', .55), C(cx + 100, cy - 292, 26, 'smoke', .4)], 'fade', 1.1, loop='drift')
    random.seed(17)
    s.layer('snowflakes', [C(random.uniform(0, W), random.uniform(40, 900), random.uniform(3, 7), 'flake', random.uniform(.6, .95)) for _ in range(60)], 'fade', 1.2, loop='twinkle')
    return s


# ============ s095 海滩 ============
def beach():
    s = Scene('s095', '海滩', '自然与地理', ['科学', '地理', '海洋', '防溺水'],
              dict(sky1='#4FBDE8', sky2='#D6F3FF', sun='#FFF3B0', island='#7CC4A0', island2='#5EAE88', sea1='#2BA7C6', sea2='#5FD0D6', sea3='#A6ECE6', foam='#FFFFFF',
                   sand='#F8E2B4', sand2='#EDCB8E', wet='#E2C08A', umb='#F2706A', umb2='#FFFFFF', pole='#E9E1D2', towel='#5FB7E0', towel2='#FFD36E',
                   palm='#3FA36E', palm2='#68C48D', trunk='#B7834F', trunk2='#8C5E34', castle='#EBC57F', castle2='#D7A85E', shell='#F7B4A8', star='#F28B4E', sail='#FFFFFF', boat='#E8574A', gull='#FFFFFF'),
              desc='阳光海滩：渐变碧蓝海面与远岛帆船，层层浪花拍上沙滩，椰子树、条纹遮阳伞、沙堡、贝壳与海星。',
              stand={'ground_y': 930, 'x': [520, 1400]})
    s.layer('sky', [R(0, 0, W, 600, s.lg([(0, 'sky1'), (1, 'sky2')])), sun(1500, 170, 66, 'sun', .5)], 'fade', 0)
    s.layer('clouds', [cloud(380, 150, .9, op=.95), cloud(1020, 100, .55, op=.85), cloud(1780, 260, .5, op=.8)], 'slide-l', .2)
    s.layer('island', [P('M1180,560 Q1260,470 1350,500 Q1420,450 1500,520 Q1560,540 1600,560Z', 'island'), P('M1350,500 Q1420,450 1500,520 Q1440,500 1380,540Z', 'island2', .7),
                       palm(1330, 520, 60, 10, 'trunk', 'trunk2', 'island2', 'island2', .25)], 'rise', .25)
    sea = [R(0, 560, W, 300, s.lg([(0, 'sea1'), (.6, 'sea2'), (1, 'sea3')])), R(0, 556, W, 6, 'sky2', 0, .8)]
    for k in range(10):
        y = 590 + k * 22; x0 = (k * 211) % 400 - 100
        for x in range(x0, W, 420): sea.append(S(f'M{x},{y} q20,-5 40,0', '#ffffff', 2 + k * .2, .45))
    s.layer('sea', sea, 'fade', .15)
    s.layer('sailboat', [P('M560,610 L680,610 L660,630 L580,630Z', 'boat'), S('M620,610 L620,500', 'trunk2', 4), P('M624,505 L624,604 L680,604Z', 'sail'), P('M616,520 L616,604 L574,604Z', 'sail', .85)], 'slide-r', .5, loop='bob')
    # 浪花 + 沙滩
    sd = [P('M-60,820 Q300,790 700,812 Q1100,834 1500,806 Q1760,790 1980,804 L1980,1080 L-60,1080Z', s.lg([(0, 'sand'), (1, 'sand2')])),
          P('M-60,820 Q300,790 700,812 Q1100,834 1500,806 Q1760,790 1980,804 L1980,836 Q1700,822 1500,840 Q1100,866 700,846 Q300,826 -60,852Z', 'wet', .45)]
    s.layer('sand', sd, 'rise', .3)
    fm = [P('M-60,812 Q120,792 300,806 Q480,820 700,804 Q900,792 1100,822 Q1300,836 1500,800 Q1700,786 1980,800 L1980,786 Q1700,770 1500,786 Q1300,820 1100,808 Q900,778 700,790 Q480,806 300,792 Q120,778 -60,798Z', 'foam', .95)]
    for x in range(40, W, 110): fm.append(C(x, 806 + 8 * math.sin(x / 140), 9, 'foam', .9))
    s.layer('foam', fm, 'fade', .4, loop='flow')
    s.layer('palms', [palm(150, 940, 520, 140, 'trunk', 'trunk2', 'palm', 'palm2', 1.15), palm(330, 900, 360, 70, 'trunk', 'trunk2', 'palm2', 'palm', .8)], 'grow', .55, loop='sway', origin='150 940')
    # 遮阳伞 + 毛巾
    ux, uy = 1600, 650
    um = [E(ux - 20, 930, 230, 22, '#7a5a30', .15), S(f'M{ux},{uy} L{ux - 30},{930}', 'pole', 10)]
    segs = 6
    for k in range(segs):
        a0 = math.pi + k * math.pi / segs; a1 = a0 + math.pi / segs
        um.append(P(f'M{ux},{uy - 20} L{ux + 230 * math.cos(a0):.0f},{uy + 40 + 60 * math.sin(a0) * .0:.0f} Q{ux + 230 * math.cos((a0 + a1) / 2):.0f},{uy + 20 + 150 * math.sin((a0 + a1) / 2) * .0 + 12:.0f} {ux + 230 * math.cos(a1):.0f},{uy + 40:.0f}Z' if False else
                    f'M{ux},{uy - 110} L{ux - 230 + k * 460 / segs:.0f},{uy} Q{ux - 230 + (k + .5) * 460 / segs:.0f},{uy - 18} {ux - 230 + (k + 1) * 460 / segs:.0f},{uy}Z', 'umb' if k % 2 == 0 else 'umb2'))
    um += [C(ux, uy - 112, 10, 'umb'), P(f'M{ux - 230},{uy} Q{ux},{uy - 140} {ux + 230},{uy} Q{ux},{uy - 80} {ux - 230},{uy}Z', '#ffffff', .0)]
    um += [P(f'M{ux - 200},880 L{ux + 60},860 L{ux + 120},940 L{ux - 150},966Z', 'towel'), P(f'M{ux - 160},874 L{ux - 120},868 L{ux - 70},954 L{ux - 110},960Z', 'towel2')]
    s.layer('umbrella', um, 'drop', .7)
    # 沙堡 + 小桶
    kx, ky = 1180, 920
    cs = [E(kx, ky + 4, 170, 16, '#7a5a30', .15), R(kx - 130, ky - 50, 260, 54, 'castle', 6), R(kx - 70, ky - 110, 140, 64, 'castle', 4), R(kx - 30, ky - 160, 60, 54, 'castle', 4)]
    for bx, by, bw in [(kx - 130, ky - 50, 260), (kx - 70, ky - 110, 140), (kx - 30, ky - 160, 60)]:
        for q in range(int(bw / 26)):
            if q % 2 == 0: cs.append(R(bx + q * 26, by - 14, 22, 16, 'castle', 3))
    cs += [P(f'M{kx - 12},{ky} L{kx - 12},{ky - 26} Q{kx},{ky - 40} {kx + 12},{ky - 26} L{kx + 12},{ky}Z', 'castle2'), S(f'M{kx},{ky - 174} L{kx},{ky - 220}', 'trunk2', 3), poly([(kx, ky - 220), (kx + 34, ky - 210), (kx, ky - 200)], 'umb'),
           R(kx - 100, ky - 30, 30, 4, 'castle2', 2), R(kx + 70, ky - 30, 30, 4, 'castle2', 2),
           P(f'M{kx + 170},{ky - 50} L{kx + 220},{ky - 50} L{kx + 212},{ky} L{kx + 178},{ky}Z', 'towel'), S(f'M{kx + 172},{ky - 50} Q{kx + 195},{ky - 84} {kx + 218},{ky - 50}', 'towel', 4)]
    s.layer('sandcastle', cs, 'pop', .8)

    def star(x, y, r, col):
        pts = []
        for k in range(10):
            a = -math.pi / 2 + k * math.pi / 5; rr = r if k % 2 == 0 else r * .45
            pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
        return poly(pts, col)
    sh = [star(560, 900, 26, 'star'), star(1440, 960, 20, 'shell'), P('M760,900 Q780,870 800,900Z', 'shell'), *[S(f'M780,900 L{770 + k * 5},{884}', '#ffffff', 2, .7) for k in range(5)],
          E(1000, 890, 14, 9, 'shell', .9), E(680, 950, 10, 6, '#ffffff', .8)]
    s.layer('shells', sh, 'pop', .95)
    s.layer('gulls', [bird(760, 300, 1.2, 'gull'), bird(830, 330, 1, 'gull'), bird(900, 280, .8, 'gull')], 'slide-l', 1.1)
    s.layer('sparkle', [C(x, y, 5, '#ffffff', .95) for x, y in [(400, 640), (900, 700), (1300, 620), (1700, 720), (1100, 660)]], 'fade', 1.2, loop='twinkle')
    return s


# ============ s096 乡村田园 ============
def countryside():
    s = Scene('s096', '乡村田园', '自然与地理', ['科学', '劳动', '地理', '乡村生活'],
              dict(sky1='#9FD6F0', sky2='#FFF7E0', sun='#FFE7A0', mtn='#BCD6CC', mtn2='#A8C8BE', field1='#F5D24A', field2='#9FD06E', field3='#C5E39A', field4='#7DBE5C', field5='#F0E3A0',
                   wall='#FBF7EE', wall2='#E9E1D0', roof='#56606E', roof2='#3F4855', door='#9C6B45', win='#7A5A44', tree='#5FAE74', tree2='#9AD48B', trunk='#8A5A3A',
                   pond='#8FD3E8', pond2='#CDEFF7', path='#F1DFC0', duck='#FFFFFF', beak='#F2A33A', fence='#C99B6A', bamboo='#7FBF6A', smoke='#FFFFFF'),
              desc='江南乡村田园：远山如黛，金黄油菜花与嫩绿稻田拼成彩色田块，白墙黛瓦的农舍、池塘与小鸭、竹篱笆。',
              stand={'ground_y': 920, 'x': [520, 1400]})
    s.layer('sky', [R(0, 0, W, 700, s.lg([(0, 'sky1'), (1, 'sky2')])), sun(420, 180, 58, 'sun', .5)], 'fade', 0)
    s.layer('clouds', [cloud(900, 140, .8, op=.95), cloud(1560, 110, .6, op=.85)], 'slide-l', .2, loop='drift')
    s.layer('mountains', [hill(s, 520, 200, 21, 'mtn', 200, 700), hill(s, 560, 110, 23, 'mtn2', 170, 700), haze(s, 440, 640, 'sky2', .85)], 'rise', .25)
    # 彩色田块：沿起伏丘陵的弧形条带拼贴
    fl = []

    def bound(y0, amp, ph):
        return lambda x: y0 - amp * math.sin(x / 420 + ph) - amp * .4 * math.sin(x / 190 + ph * 2)
    bs = [bound(560, 14, 0.3), bound(600, 16, 1.1), bound(648, 18, 1.9), bound(706, 20, 2.6), bound(780, 10, 3.1)]
    palette_rows = [['field3', 'field1', 'field2', 'field5', 'field1', 'field3', 'field2'], ['field1', 'field4', 'field3', 'field1', 'field2', 'field1'],
                    ['field2', 'field1', 'field5', 'field4', 'field1', 'field3', 'field1'], ['field4', 'field1', 'field2', 'field1', 'field3', 'field1']]
    random.seed(5)
    xs_ = list(range(-60, 2001, 20))
    for r_, cols in enumerate(palette_rows):
        top_f, bot_f = bs[r_], bs[r_ + 1]
        n = len(cols); cuts = [-60] + sorted(random.uniform(120, 1800) for _ in range(n - 1)) + [1990]
        for k in range(n):
            xa, xb = cuts[k], cuts[k + 1]
            seg = [x for x in xs_ if xa < x < xb]
            pts = [(xa, top_f(xa))] + [(x, top_f(x)) for x in seg] + [(xb, top_f(xb)), (xb + 30, bot_f(xb + 30))] + [(x, bot_f(x)) for x in reversed(seg)] + [(xa + 30, bot_f(xa + 30))]
            fl.append(poly(pts, cols[k]))
            for q in (1, 2, 3):
                fl.append(S('M' + ' L'.join(f'{x:.0f},{top_f(x) + (bot_f(x) - top_f(x)) * q / 4:.0f}' for x in [xa + 8] + seg + [xb - 8]), '#ffffff', 2, .22))
        fl.append(S('M' + ' L'.join(f'{x},{bot_f(x):.0f}' for x in xs_), 'field4', 3, .45))
    fl.append(haze(s, 520, 640, 'sky2', .55))
    s.layer('fields', fl, 'rise', .35)
    # 树
    s.layer('trees', [blob_tree(x, y, sc, 'tree', 'tree2', 'trunk') for x, y, sc in [(160, 640, .6), (1180, 620, .5), (1750, 660, .7), (1860, 650, .55), (700, 610, .45)]], 'grow', .5)

    # 白墙黛瓦农舍
    def house(x, y, w, h, sc=1):
        it = [E(x + w / 2, y + 4, w * .65, 10, '#3a3a2a', .12), R(x, y - h, w, h, 'wall'), R(x, y - h, w, 10, 'wall2', 0, .6),
              P(f'M{x - 24},{y - h + 6} L{x + 30},{y - h - 50 * sc} L{x + w - 30},{y - h - 50 * sc} L{x + w + 24},{y - h + 6}Z', 'roof'), R(x - 28, y - h - 2, w + 56, 12, 'roof2', 4),
              R(x + 30, y - h - 58 * sc, w - 60, 10, 'roof2', 4)]
        for k in range(int((w - 60) / 18)): it.append(R(x + 36 + k * 18, y - h - 46 * sc, 3, 40 * sc, 'roof2', 0, .5))
        it += [R(x + w / 2 - 22, y - 70, 44, 70, 'door', 4), R(x + 20, y - h + 30, 40, 36, 'win', 3), R(x + w - 60, y - h + 30, 40, 36, 'win', 3)]
        for xx in (x + 20, x + w - 60): it.append(S(f'M{xx + 20},{y - h + 30} L{xx + 20},{y - h + 66} M{xx},{y - h + 48} L{xx + 40},{y - h + 48}', 'wall', 3))
        # 屋脊两端起翘
        it += [P(f'M{x + 30},{y - h - 48 * sc} Q{x + 18},{y - h - 56 * sc} {x + 10},{y - h - 74 * sc} Q{x + 30},{y - h - 62 * sc} {x + 44},{y - h - 58 * sc}Z', 'roof2'),
               P(f'M{x + w - 30},{y - h - 48 * sc} Q{x + w - 18},{y - h - 56 * sc} {x + w - 10},{y - h - 74 * sc} Q{x + w - 30},{y - h - 62 * sc} {x + w - 44},{y - h - 58 * sc}Z', 'roof2')]
        return G(it)
    s.layer('houses', [house(1420, 820, 300, 150), house(1300, 760, 150, 110, .7), house(220, 800, 230, 130, .9)], 'rise', .55)
    s.layer('smoke', [C(1660, 600, 14, 'smoke', .7), C(1676, 570, 20, 'smoke', .55), C(1696, 532, 26, 'smoke', .4)], 'fade', 1.1, loop='drift')
    # 近景地面、小路、池塘
    gd = [P('M-60,800 Q500,770 960,800 Q1400,826 1980,790 L1980,1080 L-60,1080Z', s.lg([(0, 'field2'), (1, 'field4')])),
          P('M900,800 Q880,860 760,920 Q560,1010 420,1080 L760,1080 Q900,980 1000,920 Q1060,860 1020,800Z', 'path')]
    s.layer('ground', gd, 'rise', .15)
    pd = [E(1500, 930, 260, 54, 'pond'), E(1460, 920, 180, 30, 'pond2', .7)]
    for x in (1250, 1270, 1730, 1755):
        pd += [S(f'M{x},940 Q{x - 6},900 {x - 14},880', 'bamboo', 4), E(x - 16, 876, 6, 14, 'door')]
    s.layer('pond', pd, 'fade', .6)

    def duck(x, y, sc):
        return G([E(x, y, 30 * sc, 16 * sc, 'duck'), C(x + 22 * sc, y - 18 * sc, 12 * sc, 'duck'), P(f'M{x + 32 * sc},{y - 20 * sc} L{x + 46 * sc},{y - 16 * sc} L{x + 32 * sc},{y - 13 * sc}Z', 'beak'),
                  C(x + 26 * sc, y - 21 * sc, 2.5 * sc, '#333333'), P(f'M{x - 30 * sc},{y - 4 * sc} L{x - 40 * sc},{y - 16 * sc} L{x - 24 * sc},{y - 10 * sc}Z', 'duck'), E(x - 4 * sc, y - 2 * sc, 14 * sc, 7 * sc, 'wall2', .8)])
    s.layer('ducks', [duck(1420, 926, 1), duck(1540, 944, .8), duck(1600, 918, .65)], 'slide-r', .85, loop='bob')
    # 竹篱笆 + 油菜花近景
    fc = []
    for x in range(0, 640, 34): fc.append(R(x, 860, 12, 90, 'fence', 4))
    fc += [R(0, 880, 640, 8, 'fence', 3), R(0, 916, 640, 8, 'fence', 3)]
    random.seed(9)
    for k in range(40):
        x = random.uniform(0, 600); y = random.uniform(930, 1060)
        fc += [S(f'M{x:.0f},{y:.0f} L{x:.0f},{y - 50:.0f}', 'field4', 3), C(x, y - 54, 9, 'field1'), C(x + 6, y - 46, 7, 'field1'), C(x - 6, y - 44, 6, 'field1')]
    s.layer('fence_flowers', fc, 'grow', .75, loop='sway')
    s.layer('butterflies', [G([E(1000, 500, 12, 8, 'field1', extra='transform="rotate(-30 1000 500)"'), E(1012, 500, 12, 8, 'field1', extra='transform="rotate(30 1012 500)"')]),
                            G([E(700, 760, 10, 7, '#F2A0C0', extra='transform="rotate(-30 700 760)"'), E(710, 760, 10, 7, '#F2A0C0', extra='transform="rotate(30 710 760)"')])], 'fade', 1.2)
    return s


# ============ s097 城市天际线 ============
def skyline():
    s = Scene('s097', '城市天际线', '自然与地理', ['地理', '城市', '社会', '美术'],
              dict(sky1='#6D6BC0', sky2='#E59BB4', sky3='#FFD6A0', sun='#FFE2A8', far='#B7A6D8', mid='#8A7CC0', mid2='#7468AE', near='#56508F', near2='#46407A', win='#FFE08A', win2='#FFF3C8',
                   tower='#E9B7C8', tower2='#C98DAA', river='#7E7CC4', river2='#F2B8B8', bridge='#3E3A6A', rail='#2F2B55', walk='#5A5490', lamp='#FFE7A8', star='#FFFFFF'),
              desc='黄昏城市天际线：紫粉渐变晚霞，远中近三层楼群亮起点点窗灯，电视塔与拱桥，河面倒映霞光，近景滨江步道与路灯。',
              stand={'ground_y': 930, 'x': [480, 1440]})
    s.layer('sky', [R(0, 0, W, 760, s.lg([(0, 'sky1'), (.55, 'sky2'), (1, 'sky3')])), sun(1300, 560, 90, 'sun', .55)], 'fade', 0)
    random.seed(19)
    s.layer('stars', [C(random.uniform(0, W), random.uniform(20, 260), random.uniform(1.5, 3.2), 'star', random.uniform(.5, .9)) for _ in range(40)], 'fade', .2, loop='twinkle')
    s.layer('clouds', [G([E(400, 300, 260, 18, 'sky3', .6), E(520, 286, 160, 14, 'sky3', .5), E(1600, 360, 300, 16, 'sky3', .5), E(1000, 220, 200, 12, 'sky2', .6)])], 'slide-l', .25, loop='drift')

    def city(y, seed, col, wmin, wmax, hmin, hmax, wincol=None, winop=.7, gap=(2, 14), pad=0):
        random.seed(seed); it = []; x = -20
        while x < W:
            w = random.randint(wmin, wmax); h = random.randint(hmin, hmax); kind = random.random()
            it.append(R(x, y - h, w, h + 400, col, 4))
            if kind < .25: it.append(poly([(x, y - h), (x + w / 2, y - h - w * .5), (x + w, y - h)], col))
            elif kind < .45: it += [R(x + w * .3, y - h - 30, w * .4, 32, col, 3), R(x + w / 2 - 2, y - h - 70, 4, 42, col)]
            if wincol:
                for wy in range(int(y - h + 20), int(y) - 10, 26):
                    for wx in range(int(x + 10), int(x + w - 16), 20):
                        if random.random() < .35: it.append(R(wx, wy, 9, 12, wincol, 1, winop))
            x += w + random.randint(*gap)
        return G(it)
    s.layer('city_far', [city(700, 2, 'far', 60, 120, 120, 300), haze(s, 520, 720, 'sky3', .55)], 'rise', .3)
    # 电视塔
    tx = 640
    tw = [S(f'M{tx - 40},700 L{tx},300 L{tx + 40},700', 'tower2', 12), S(f'M{tx},700 L{tx},180', 'tower2', 10), C(tx, 520, 52, 'tower'), C(tx, 350, 34, 'tower'), C(tx, 260, 18, 'tower'),
          S(f'M{tx},180 L{tx},110', 'tower2', 4), C(tx - 16, 510, 14, '#ffffff', .4), C(tx, 108, 5, 'win')]
    s.layer('tv_tower', tw, 'grow', .4, origin=f'{tx} 700')
    s.layer('city_mid', [city(740, 7, 'mid', 70, 140, 120, 330, 'win', .55), R(0, 740, W, 20, 'mid2')], 'rise', .45)
    s.layer('windows_glow', [C(x, y, 80, 'win', .18, 'filter="url(#b40)"') for x, y in [(300, 620), (900, 600), (1500, 640), (1800, 600)]], 'fade', 1.0)
    s.layer('city_near', [city(780, 13, 'near', 90, 170, 80, 250, 'win2', .75, (6, 30))], 'rise', .55)
    # 河 + 倒影
    rv = [R(0, 760, W, 200, s.lg([(0, 'river2'), (1, 'river')])), E(1300, 800, 120, 10, 'sun', .7), E(1300, 830, 80, 6, 'sun', .5), E(1300, 856, 50, 4, 'sun', .4)]
    for k in range(10):
        y = 790 + k * 16
        for x in range((k * 157) % 300 - 100, W, 340): rv.append(S(f'M{x},{y} q30,-4 60,0', '#ffffff', 2, .3))
    s.layer('river', rv, 'fade', .35, loop='flow')
    # 拱桥
    bx0, bx1 = 960, 1920
    br = [P(f'M{bx0},760 Q{(bx0 + bx1) / 2},640 {bx1},760 L{bx1},780 Q{(bx0 + bx1) / 2},670 {bx0},780Z', 'bridge'), R(bx0 - 40, 690, 1000, 14, 'bridge', 4)]
    for k in range(1, 16):
        x = bx0 + k * (bx1 - bx0) / 16; yb = 760 - 120 * 4 * (k / 16) * (1 - k / 16) * .95
        br.append(R(x - 3, 700, 6, yb - 700 + 6, 'bridge'))
    for x in (1180, 1700):
        br += [R(x - 10, 560, 20, 200, 'bridge', 4), S(f'M{x},566 L{x - 180},700 M{x},566 L{x + 180},700 M{x},566 L{x - 100},700 M{x},566 L{x + 100},700', 'bridge', 3)]
    br += [*[C(bx0 + k * 60, 688, 4, 'lamp', .9) for k in range(17)]]
    s.layer('bridge', br, 'slide-r', .65)
    # 滨江步道
    wk = [R(0, 900, W, 180, s.lg([(0, 'walk'), (1, 'near2')])), R(0, 892, W, 12, 'rail'), R(0, 860, W, 8, 'rail', 4)]
    for x in range(20, W, 60): wk.append(R(x, 860, 6, 40, 'rail'))
    for x in (180, 1740):
        wk += [R(x - 6, 640, 12, 260, 'rail', 4), R(x - 18, 890, 36, 14, 'rail', 4), E(x, 640, 26, 14, 'lamp'), P(f'M{x - 30},636 Q{x},604 {x + 30},636Z', 'rail')]
    s.layer('promenade', wk, 'rise', .2)
    s.layer('lamp_glow', [C(x, 650, 70, 'lamp', .45, 'filter="url(#b20)"') for x in (180, 1740)] + [E(x, 910, 120, 16, 'lamp', .35, 'filter="url(#b20)"') for x in (180, 1740)], 'fade', 1.1, loop='glow')
    s.layer('birds', [bird(1000, 420, 1, 'near2'), bird(1060, 450, .8, 'near2'), bird(940, 460, .7, 'near2')], 'slide-l', 1.2)
    return s


# ============ s098 热带雨林 ============
def rainforest():
    s = Scene('s098', '热带雨林', '自然与地理', ['科学', '生物多样性', '地理', '生态'],
              dict(sky1='#BFE8D6', sky2='#F0FBF2', far='#9DD4B2', far2='#86C7A0', mid='#55A97E', mid2='#3F9670', near='#2E7D5C', near2='#1F6A4C', leaf='#2F8A5E', leaf2='#4FB07A', leaf3='#1D5E43',
                   rock='#7E9C90', rock2='#A9C2B6', fall='#E8FAFF', fall2='#BDEBF5', pool='#5CC2C8', pool2='#A8E6E6', moss='#5BAA6A', vine='#3E8E5E',
                   parrot='#E8483B', parrot2='#3F8BD6', parrot3='#F7C54A', flower='#F28B3E', flower2='#F25C8A', fly='#5FC4F0'),
              desc='繁茂热带雨林：层层叠叠的绿色树冠与湿润雾气，中央山崖飞瀑落入碧潭，藤蔓垂挂，大叶龟背竹框住画面，鹦鹉与蓝闪蝶点缀。',
              stand={'ground_y': 920, 'x': [480, 1440]})
    s.layer('sky', [R(0, 0, W, H, s.lg([(0, 'sky1'), (1, 'sky2')])), C(960, 160, 260, '#ffffff', .6, 'filter="url(#b40)"')], 'fade', 0)

    def canopy(y, seed, col, col2, rmin, rmax, n):
        random.seed(seed); it = []
        for k in range(n):
            x = k * (W + 200) / (n - 1) - 100 + random.uniform(-30, 30); r = random.uniform(rmin, rmax)
            it += [C(x, y - r * .2, r, col), C(x - r * .3, y - r * .5, r * .55, col2, .5)]
        it.append(R(0, y, W, H - y, col))
        return G(it)
    s.layer('canopy_far', [canopy(470, 2, 'far', 'sky2', 70, 120, 18), haze(s, 380, 560, 'sky2', .85)], 'rise', .2)
    # 山崖瀑布
    cf = [P('M700,1080 L700,420 Q720,330 820,300 L1100,300 Q1200,320 1220,420 L1220,1080Z', 'rock'), P('M1100,300 Q1200,320 1220,420 L1220,1080 L1120,1080 Q1150,700 1100,300Z', 'rock2', .35),
          P('M690,420 Q720,320 830,296 L1090,296 Q1200,316 1230,420 Q1150,380 960,390 Q780,380 690,420Z', 'moss')]
    for x, y, r in [(740, 330, 60), (820, 300, 70), (1100, 296, 64), (1190, 340, 58), (960, 300, 46)]:
        cf.append(C(x, y, r, 'mid'))
    for x, y, sc in [(720, 520, 1), (1200, 560, -1), (730, 700, 1), (1196, 740, -1)]:
        for k in range(4):
            a = -60 + k * 30
            cf.append(E(x + sc * 30 * math.cos(math.radians(a)), y + 30 * math.sin(math.radians(a)), 30, 9, 'leaf2', extra=f'transform="rotate({a * sc} {x + sc * 30 * math.cos(math.radians(a)):.0f} {y + 30 * math.sin(math.radians(a)):.0f})"'))
    for x in range(760, 1200, 70): cf.append(R(x, 430, 3, 420, 'rock2', 0, .35))
    s.layer('cliff', cf, 'rise', .3)
    s.layer('waterfall', [P('M890,330 L1030,330 Q1040,600 1060,880 L860,880 Q880,600 890,330Z', s.lg([(0, 'fall'), (1, 'fall2')])),
                          *[S(f'M{x},{340} Q{x + (x - 960) * .05:.0f},620 {x + (x - 960) * .15:.0f},870', '#ffffff', 4, .7) for x in (910, 940, 975, 1005)]], 'drop', .45, loop='flow')
    s.layer('mist', [E(960, 870, 300, 56, '#ffffff', .85, 'filter="url(#b20)"'), E(960, 820, 200, 40, '#ffffff', .5, 'filter="url(#b20)"'), R(0, 600, 700, 160, s.lg([(0, 'sky2', 0), (.6, 'sky2', .6), (1, 'sky2', 0)])), R(1220, 600, 700, 160, s.lg([(0, 'sky2', 0), (.6, 'sky2', .6), (1, 'sky2', 0)]))], 'fade', .6, loop='drift')
    cpm = s.clip('<path d="M0,0 L700,0 L700,1080 L0,1080Z M1220,0 L1920,0 L1920,1080 L1220,1080Z"/>')
    s.layer('canopy_mid', [G([canopy(640, 6, 'mid', 'far', 80, 130, 8)], f'clip-path="{cpm}"')], 'rise', .4)
    # 潭水 + 地面
    gd = [P('M-60,860 Q400,830 760,870 Q960,890 1160,870 Q1520,830 1980,860 L1980,1080 L-60,1080Z', s.lg([(0, 'moss'), (1, 'near')])),
          E(960, 905, 330, 54, 'pool'), E(930, 896, 230, 28, 'pool2', .6)]
    s.layer('ground', gd, 'rise', .15)
    s.layer('pool_ripple', [S('M820,910 q30,-6 60,0', '#ffffff', 3, .8), S('M1020,900 q40,-6 80,0', '#ffffff', 3, .8)], 'fade', 1.0)
    # 树干与藤蔓
    tr = [R(130, 0, 70, 880, s.lg([(0, 'near2'), (.5, 'near'), (1, 'near2')], 0, 0, 1, 0)), R(1700, 0, 80, 880, s.lg([(0, 'near2'), (.5, 'near'), (1, 'near2')], 0, 0, 1, 0)),
          P('M110,880 Q165,820 220,880Z', 'near2'), P('M1680,880 Q1740,820 1800,880Z', 'near2')]
    s.layer('trunks', tr, 'slide-l', .5)
    vn = []
    for x0, ln in [(260, 420), (380, 300), (1560, 380), (1460, 260), (620, 220), (1300, 200)]:
        vn.append(S(f'M{x0},0 Q{x0 + 30},{ln * .5} {x0 - 10},{ln}', 'vine', 5))
        for k in range(1, 8):
            u = k / 8; y = ln * u; x = x0 + 30 * 2 * u * (1 - u) - 10 * u * u
            vn.append(E(x + (10 if k % 2 else -10), y, 14, 7, 'leaf2', extra=f'transform="rotate({40 if k % 2 else -40} {x:.0f} {y:.0f})"'))
    s.layer('vines', vn, 'drop', .65, loop='sway')

    # 龟背竹大叶（四角框景）
    def monstera(x, y, sc, rot, col, col2):
        it = [P(f'M0,0 C{-90},{-30} {-120},{-160} 0,{-220} C{120},{-160} {90},{-30} 0,0Z', col), S('M0,-6 Q4,-110 0,-210', col2, 5, .8)]
        for k in range(3):
            yy = -60 - k * 50
            it += [P(f'M{-70 + k * 6},{yy} L{-20},{yy - 10} L{-70 + k * 6},{yy + 8}Z', 'sky2', .9), P(f'M{70 - k * 6},{yy} L{20},{yy - 10} L{70 - k * 6},{yy + 8}Z', 'sky2', .9)]
        it.append(C(-36, -120, 7, 'sky2', .9))
        return G(it, f'transform="translate({x},{y}) rotate({rot}) scale({sc})"')
    fl = [monstera(40, 1080, 1.5, 40, 'leaf', 'leaf3'), monstera(200, 1090, 1.2, 10, 'leaf2', 'leaf3'), monstera(-20, 820, 1.1, 70, 'near', 'leaf3'),
          monstera(1880, 1080, 1.5, -40, 'leaf', 'leaf3'), monstera(1720, 1090, 1.2, -12, 'leaf2', 'leaf3'), monstera(1950, 800, 1.1, -70, 'near', 'leaf3'),
          monstera(80, -20, 1.2, 160, 'near', 'leaf3'), monstera(1840, -20, 1.2, -160, 'near', 'leaf3')]
    s.layer('big_leaves', fl, 'grow', .75)
    # 花
    fw = []
    for x, y, col in [(420, 900, 'flower'), (480, 920, 'flower2'), (1450, 905, 'flower'), (1520, 925, 'flower2'), (560, 880, 'flower2')]:
        for k in range(5):
            a = -math.pi / 2 + (k - 2) * .5
            fw.append(E(x + 18 * math.cos(a), y - 30 + 18 * math.sin(a), 16, 7, col, extra=f'transform="rotate({math.degrees(a):.0f} {x + 18 * math.cos(a):.0f} {y - 30 + 18 * math.sin(a):.0f})"'))
        fw += [S(f'M{x},{y} L{x},{y - 30}', 'leaf3', 4), C(x, y - 30, 6, 'parrot3')]
    s.layer('flowers', fw, 'pop', .85)

    # 鹦鹉
    def parrot(x, y, sc, body, wing, flip=1):
        return G([E(0, 0, 22, 34, body), C(4, -32, 18, body), P('M14,-38 Q30,-36 26,-22 Q20,-28 12,-26Z', 'parrot3'), C(8, -36, 4, '#ffffff'), C(9, -36, 2, '#222222'),
                  P('M-12,-6 Q-30,20 -14,40 Q0,20 8,-4Z', wing), P('M-6,28 L-16,90 L0,90 L6,30Z', body), P('M-2,40 L-6,90 L4,90Z', wing, .8)],
                 f'transform="translate({x},{y}) scale({sc * flip},{sc})"')
    s.layer('parrots', [S('M240,430 Q420,450 600,420', 'near2', 10), parrot(380, 400, 1.1, 'parrot', 'parrot2'), parrot(1560, 500, .95, 'parrot2', 'parrot3', -1), S('M1380,530 Q1500,550 1660,520', 'near2', 10)], 'pop', .95, loop='bob')
    s.layer('butterflies', [G([E(600, 640, 16, 11, 'fly', extra='transform="rotate(-30 600 640)"'), E(616, 640, 16, 11, 'fly', extra='transform="rotate(30 616 640)"')]),
                            G([E(1320, 700, 12, 8, 'fly', extra='transform="rotate(-30 1320 700)"'), E(1332, 700, 12, 8, 'fly', extra='transform="rotate(30 1332 700)"')])], 'fade', 1.2)
    return s


# ============ s099 极地冰川 ============
def glacier():
    s = Scene('s099', '极地冰川', '自然与地理', ['科学', '地理', '气候变化', '动物'],
              dict(sky1='#35507F', sky2='#7FA6D0', sky3='#F4D8E2', aur='#7FF0C8', aur2='#9AD7FF', star='#FFFFFF', ice1='#F2FBFF', ice2='#CDEBF6', ice3='#A3D3E8', ice4='#7FBAD6',
                   sea1='#4F86B4', sea2='#7FB0D4', sea3='#BFDDEE', peng='#26303E', peng2='#FFFFFF', beak='#F2A33A', snow='#FFFFFF'),
              desc='南极冰川的极昼黄昏：淡粉天际与绿色极光，层层冰山与冰崖，冷蓝海面漂着浮冰，近景冰原上站着一群企鹅。',
              stand={'ground_y': 930, 'x': [480, 1440]})
    s.layer('sky', [R(0, 0, W, 720, s.lg([(0, 'sky1'), (.6, 'sky2'), (1, 'sky3')]))], 'fade', 0)
    random.seed(23)
    s.layer('stars', [C(random.uniform(0, W), random.uniform(10, 300), random.uniform(1.4, 3), 'star', random.uniform(.4, .9)) for _ in range(50)], 'fade', .15)
    au = []
    for k, (y, amp, col, op) in enumerate([(200, 60, 'aur', .55), (250, 50, 'aur2', .4), (170, 40, 'aur', .35)]):
        d = f'M-100,{y} C300,{y - amp} 600,{y + amp} 960,{y} S1600,{y - amp} 2020,{y + 20}'
        au.append(S(d, col, 70 - k * 15, op, extra='filter="url(#b20)"'))
        au.append(P(f'M-100,{y} C300,{y - amp} 600,{y + amp} 960,{y} S1600,{y - amp} 2020,{y + 20} L2020,{y - 160} C1600,{y - 200} 1300,{y - 120} 960,{y - 150} C600,{y - 180} 300,{y - 140} -100,{y - 160}Z', s.lg([(0, col, 0), (1, col, op * .5)]), extra='filter="url(#b20)"'))
    s.layer('aurora', au, 'fade', .3, loop='glow')
    s.layer('sun_glow', [E(960, 700, 700, 90, 'sky3', .8, 'filter="url(#b40)"')], 'fade', .2)

    def berg(pts, col, shade, line=None):
        it = [poly(pts, col)]
        if shade:
            n = len(pts); top = min(range(n), key=lambda i: pts[i][1])
            it.append(poly([pts[top]] + [p for p in pts[top + 1:]] + [(pts[top][0] + 10, pts[-1][1])], shade, .55))
        return G(it)
    # 远冰山
    far = [berg([(-40, 720), (120, 560), (260, 600), (380, 520), (520, 720)], 'ice2', 'ice3'), berg([(1300, 720), (1440, 540), (1560, 580), (1680, 500), (1840, 600), (1960, 720)], 'ice2', 'ice3'),
           berg([(700, 720), (820, 620), (920, 650), (1000, 600), (1120, 720)], 'ice2', 'ice3'), haze(s, 600, 740, 'sky3', .6)]
    s.layer('bergs_far', far, 'rise', .3)
    sea = [R(0, 720, W, 360, s.lg([(0, 'sea3'), (.4, 'sea2'), (1, 'sea1')]))]
    for k in range(8):
        y = 740 + k * 20
        for x in range((k * 131) % 300 - 120, W, 360): sea.append(S(f'M{x},{y} q30,-5 60,0', '#ffffff', 2, .35))
    sea += [E(960, 740, 400, 12, 'sky3', .6)]
    s.layer('sea', sea, 'fade', .2, loop='flow')
    # 中景冰崖（右）+ 冰山（左）
    cl = [P('M1180,800 L1220,600 L1300,560 L1420,580 L1520,520 L1680,540 L1800,500 L1980,520 L1980,820 Z', 'ice1'),
          *[P(f'M{x},{y} L{x + 14},{y} L{x + 30},820 L{x + 4},820Z', 'ice3', .6) for x, y in [(1260, 590), (1380, 575), (1500, 530), (1620, 536), (1760, 510), (1880, 512)]],
          P('M1180,800 L1220,600 L1300,560 L1980,520 L1980,600 L1300,620 L1240,660Z', 'snow', .8), R(1180, 800, 800, 20, 'ice4', 0, .5)]
    cl += [berg([(80, 810), (160, 640), (260, 620), (340, 680), (420, 810)], 'ice1', 'ice3'), P('M160,640 L260,620 L300,650 L200,680Z', 'snow'), E(250, 812, 190, 10, 'ice4', .4)]
    s.layer('ice_cliff', cl, 'rise', .45)
    s.layer('floes', [E(700, 800, 90, 14, 'ice1'), E(700, 806, 90, 8, 'ice3', .6), E(1000, 840, 60, 10, 'ice1'), E(1000, 845, 60, 6, 'ice3', .6), E(560, 860, 40, 7, 'ice1')], 'slide-r', .55, loop='bob')
    # 近景冰原
    ig = [P('M-60,900 Q300,870 700,895 Q1000,912 1300,892 Q1600,872 1980,900 L1980,1080 L-60,1080Z', s.lg([(0, 'ice1'), (1, 'ice2')])),
          P('M-60,900 Q300,870 700,895 Q1000,912 1300,892 Q1600,872 1980,900 L1980,916 Q1600,890 1300,910 Q1000,930 700,912 Q300,888 -60,918Z', 'ice3', .6)]
    for x, y in [(300, 980), (900, 1000), (1500, 970)]:
        ig.append(S(f'M{x},{y} l60,-10 l40,12 l50,-6', 'ice3', 3, .6))
    s.layer('ice_field', ig, 'rise', .2)

    def penguin(x, y, sc, flip=1):
        return G([E(0, 4, 34, 7, '#3a5a7a', .2), E(0, -50, 30, 50, 'peng'), E(4 * flip, -44, 20, 40, 'peng2'), C(0, -98, 22, 'peng'), C(8 * flip, -102, 6, 'peng2'), C(9 * flip, -102, 3, 'peng'),
                  P(f'M{16 * flip},-96 L{32 * flip},-92 L{16 * flip},-88Z', 'beak'), E(-24 * flip, -54, 9, 26, 'peng', extra=f'transform="rotate({20 * flip} {-24 * flip} -54)"'),
                  E(-10, 0, 10, 4, 'beak'), E(10, 0, 10, 4, 'beak'), E(-4 * flip, -82, 14, 6, 'beak', .5)], f'transform="translate({x},{y}) scale({sc})"')
    s.layer('penguins', [penguin(1520, 930, 1.1), penguin(1610, 920, .9, -1), penguin(1700, 940, 1.2), penguin(1790, 925, .8, -1), penguin(330, 930, 1.0, -1), penguin(410, 940, .75)], 'pop', .8)
    random.seed(29)
    s.layer('sparkle', [C(random.uniform(100, 1900), random.uniform(560, 880), random.uniform(3, 5), '#ffffff', .9) for _ in range(14)], 'fade', 1.2, loop='twinkle')
    return s


# ============ s100 四季大树 ============
def seasons_tree():
    s = Scene('s100', '四季大树', '自然与地理', ['科学', '四季', '语文', '自然观察'],
              dict(sp='#FCE4EC', su='#D9F1FB', au='#FCE6C8', wi='#E4EAF6', spg='#A8DC8A', sug='#7CC466', aug='#E9B46A', wig='#FFFFFF', wig2='#DCE5F2',
                   blossom='#F7A8C4', blossom2='#FFD6E4', green='#5FB56E', green2='#93D07E', orange='#F29A3E', orange2='#F7C55E', red='#E2654A', snow='#FFFFFF',
                   trunk='#8C5A3A', trunk2='#6E4228', sun='#FFE7A0', moon='#FFF6D8', flake='#FFFFFF'),
              desc='一棵大树分四季：树冠从左到右依次是春天粉花、夏天浓绿、秋天金红、冬天积雪枯枝，背景与地面同步四色渐变，花瓣、落叶、雪花飘落。',
              stand={'ground_y': 930, 'x': [420, 1500]})
    s.layer('sky', [R(0, 0, W, H, s.lg([(0, 'sp'), (.3, 'su'), (.7, 'au'), (1, 'wi')], 0, 0, 1, 0))], 'fade', 0)
    s.layer('sun_moon', [sun(240, 170, 52, 'sun', .5), C(1700, 160, 46, 'moon'), C(1722, 146, 40, 'wi')], 'fade', .15, loop='glow')
    s.layer('clouds', [cloud(620, 140, .5, op=.9), cloud(1350, 120, .45, op=.85)], 'slide-l', .2, loop='drift')
    # 远丘：四色
    hl = [P(smooth([(-60, 760), (240, 700), (520, 740), (800, 690), (1100, 730), (1400, 690), (1700, 735), (1980, 700)], 1080), s.lg([(0, 'spg'), (.3, 'sug'), (.7, 'aug'), (1, 'wig2')], 0, 0, 1, 0)),
          R(0, 640, W, 160, s.lg([(0, '#ffffff', 0), (1, '#ffffff', .35)]))]
    s.layer('hills', hl, 'rise', .25)
    gd = [P('M-60,860 Q480,830 960,850 Q1440,870 1980,840 L1980,1080 L-60,1080Z', s.lg([(0, 'spg'), (.32, 'sug'), (.68, 'aug'), (.86, 'wig'), (1, 'wig')], 0, 0, 1, 0))]
    s.layer('ground', gd, 'rise', .1)
    # 树干与枝
    cx = 960
    tk = [E(cx, 880, 220, 20, '#4a3020', .15), P(f'M{cx - 70},880 Q{cx - 40},700 {cx - 30},560 L{cx + 30},560 Q{cx + 40},700 {cx + 70},880Z', 'trunk'),
          P(f'M{cx + 4},880 Q{cx + 20},700 {cx + 12},560 L{cx + 30},560 Q{cx + 40},700 {cx + 70},880Z', 'trunk2', .5), P(f'M{cx - 90},884 Q{cx - 60},860 {cx - 40},830 L{cx + 40},830 Q{cx + 60},860 {cx + 90},884Z', 'trunk')]
    br = [(cx - 20, 580, cx - 220, 380, 26), (cx - 10, 560, cx - 80, 300, 22), (cx + 10, 560, cx + 70, 290, 22), (cx + 20, 580, cx + 240, 380, 26),
          (cx + 160, 450, cx + 380, 340, 14), (cx + 200, 410, cx + 260, 250, 12), (cx + 300, 370, cx + 460, 420, 10), (cx + 340, 350, cx + 420, 260, 8),
          (cx - 160, 450, cx - 380, 360, 14), (cx - 60, 400, cx - 200, 250, 12)]
    for x0, y0, x1, y1, w in br:
        tk.append(S(f'M{x0},{y0} Q{(x0 + x1) / 2 + (y1 - y0) * .15:.0f},{(y0 + y1) / 2:.0f} {x1},{y1}', 'trunk', w))
    s.layer('trunk', tk, 'grow', .3, origin=f'{cx} 880')
    # 树冠：同一团树冠按四个竖向切片分季（春/夏/秋 树叶，冬 枯枝积雪）
    random.seed(7)
    blobs = []
    for row in range(6):
        y = 160 + row * 70; half = 500 * math.sqrt(max(0, 1 - ((y - 400) / 280) ** 2)) + 10
        n = int(half * 2 / 110) + 1
        for k in range(n):
            x = cx - half + (k + .5 * (row % 2)) * (half * 2 / max(1, n - .5)) + random.uniform(-14, 14)
            blobs.append((x, y + random.uniform(-12, 12), random.uniform(62, 82)))
    bands = [(-1, cx - 270, 'blossom', 'blossom2'), (cx - 270, cx, 'green', 'green2'), (cx, cx + 270, 'orange', 'orange2')]
    cr = []
    for x0, x1, c1, c2 in bands:
        cp = s.clip(f'<rect x="{x0}" y="0" width="{x1 - x0}" height="{H}"/>')
        g = []
        for bx, by, r in blobs: g.append(C(bx, by, r, c1))
        for bx, by, r in blobs: g.append(C(bx - r * .28, by - r * .3, r * .42, c2, .45))
        if c1 == 'blossom':
            for bx, by, r in blobs: g.append(C(bx + r * .3, by + r * .2, 6, '#ffffff', .85))
        if c1 == 'orange':
            for k, (bx, by, r) in enumerate(blobs):
                if k % 3 == 0: g.append(C(bx + r * .2, by + r * .15, r * .34, 'red', .55))
        cr.append(G(g, f'clip-path="{cp}"'))
    s.layer('crown', cr, 'pop', .5, origin=f'{cx} 400')
    # 冬季切片：枯枝 + 积雪
    cpw = s.clip(f'<rect x="{cx + 270}" y="0" width="{W}" height="{H}"/>')
    wb = []
    random.seed(44)

    def grow(x, y, ang, L, w, d):
        r = math.radians(ang); x1, y1 = x + L * math.cos(r), y + L * math.sin(r)
        wb.append((x, y, x1, y1, w))
        if d == 0: return
        for da in (-26 + random.uniform(-6, 6), 22 + random.uniform(-6, 6)):
            grow(x1, y1, ang + da, L * random.uniform(.62, .74), w * .66, d - 1)
    grow(cx + 30, 600, -48, 230, 22, 4)
    grow(cx + 30, 600, -20, 200, 18, 4)
    wg = [C(bx, by, r, 'wig2', .55) for bx, by, r in blobs] + [C(bx - r * .28, by - r * .3, r * .42, '#ffffff', .5) for bx, by, r in blobs]
    for x0, y0, x1, y1, w in wb:
        d = f'M{x0:.0f},{y0:.0f} L{x1:.0f},{y1:.0f}'
        wg += [S(d, 'trunk', w)]
    for x0, y0, x1, y1, w in wb:
        if w < 12: wg.append(S(f'M{x0:.0f},{y0 - w * .45:.0f} L{x1:.0f},{y1 - w * .45:.0f}', 'snow', max(3, w * .55)))
    for x0, y0, x1, y1, w in wb:
        if w < 5: wg.append(C(x1, y1 - 2, 6, 'snow'))
    s.layer('winter_branches', [G(wg, f'clip-path="{cpw}"')], 'fade', .7)
    # 地面四季细节
    random.seed(13)
    det = []
    for k in range(26):   # 春：小花
        x = random.uniform(20, 520); y = random.uniform(900, 1060); det += [S(f'M{x:.0f},{y:.0f} L{x:.0f},{y - 24:.0f}', 'green', 3), C(x, y - 26, 7, 'blossom' if k % 2 else '#ffffff'), C(x, y - 26, 2.5, 'orange2')]
    for k in range(30):   # 夏：草
        x = random.uniform(560, 900); y = random.uniform(900, 1060); det.append(S(f'M{x:.0f},{y:.0f} l-6,-18 M{x:.0f},{y:.0f} l2,-22 M{x:.0f},{y:.0f} l8,-16', 'green', 3, .8))
    for k in range(26):   # 秋：落叶
        x = random.uniform(1040, 1500); y = random.uniform(900, 1060); det.append(E(x, y, 12, 6, 'orange' if k % 2 else 'red', .9, extra=f'transform="rotate({random.randint(0, 180)} {x:.0f} {y:.0f})"'))
    det += [E(1720, 940, 120, 26, 'wig2'), C(1720, 900, 40, 'snow'), C(1720, 852, 28, 'snow'), C(1710, 846, 3, '#333333'), C(1730, 846, 3, '#333333'), P('M1720,852 L1744,858 L1720,862Z', 'orange'),
            S('M1690,896 L1650,870 M1750,896 L1790,868', 'trunk2', 4), R(1700, 818, 40, 10, 'red', 3), R(1708, 796, 24, 24, 'red', 4)]
    s.layer('ground_details', det, 'grow', .8, loop='sway')
    # 飘落物
    random.seed(31)
    fall = []
    for k in range(10): x = random.uniform(150, 700); y = random.uniform(200, 800); fall.append(E(x, y, 8, 5, 'blossom', .9, extra=f'transform="rotate({random.randint(0, 180)} {x:.0f} {y:.0f})"'))
    for k in range(10): x = random.uniform(1100, 1450); y = random.uniform(500, 860); fall.append(E(x, y, 11, 6, 'orange', .9, extra=f'transform="rotate({random.randint(0, 180)} {x:.0f} {y:.0f})"'))
    for k in range(26): fall.append(C(random.uniform(1500, 1920), random.uniform(40, 860), random.uniform(3, 6), 'flake', .95))
    s.layer('falling', fall, 'fade', 1.1, loop='drift')
    s.layer('birds', [bird(700, 220, 1, 'trunk2'), bird(760, 250, .8, 'trunk2')], 'slide-l', 1.2)
    return s


SCENES = [grassland, desert, snowmtn, beach, countryside, skyline, rainforest, glacier, seasons_tree]
