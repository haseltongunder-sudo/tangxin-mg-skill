"""第 6 类 艺术与劳动：s052–s060（平面 MG 风格）"""
from core import *
import math, random


# ---------- 小工具 ----------
def shadow(x, y, rx, ry, op=.14):
    return E(x, y, rx, ry, '#2a1f35', op, 'filter="url(#b6)"')


def rot(items, a, cx, cy):
    return G(items if isinstance(items, list) else [items], f'transform="rotate({a:.1f} {cx:.1f} {cy:.1f})"')


def leafy(x, y, sc, c1, c2, n=7, spread=2.4, ln=60):
    it = []
    for k in range(n):
        a = -math.pi / 2 + (k - (n - 1) / 2) * spread / n
        lx, ly = x + math.cos(a) * ln * .55 * sc, y + math.sin(a) * ln * .55 * sc
        it.append(E(lx, ly, ln * .55 * sc, ln * .2 * sc, c1 if k % 2 else c2, extra=f'transform="rotate({math.degrees(a):.0f} {lx:.0f} {ly:.0f})"'))
    return G(it)


def potted(x, y, sc, pot, pot2, c1, c2, n=7):
    return G([shadow(x, y + 4, 46 * sc, 8 * sc), leafy(x, y - 54 * sc, sc * 1.2, c1, c2, n),
              P(f'M{x - 34 * sc},{y - 60 * sc} L{x + 34 * sc},{y - 60 * sc} L{x + 26 * sc},{y} L{x - 26 * sc},{y}Z', pot),
              R(x - 38 * sc, y - 66 * sc, 76 * sc, 14 * sc, pot2, 4 * sc)])


def window(s, x, y, w, h, sky1, sky2, frame='#ffffff', extra_items=None):
    it = [R(x - 14, y - 14, w + 28, h + 28, frame, 14, extra='filter="url(#shs)"'), R(x, y, w, h, s.lg([(0, sky1), (1, sky2)]), 6)]
    if extra_items:
        cp = s.clip(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6"/>')
        it.append(G(extra_items, f'clip-path="{cp}"'))
    it += [R(x + w / 2 - 4, y, 8, h, frame), R(x, y + h / 2 - 4, w, 8, frame), R(x - 24, y + h + 8, w + 48, 16, frame, 6)]
    return G(it)


def ring(x, y, rx, ry, col, w, op=1):
    """椭圆描边（用路径，避免重复 style 属性）"""
    return S(f'M{x - rx:.1f},{y:.1f} a{rx:.1f},{ry:.1f} 0 1,0 {2 * rx:.1f},0 a{rx:.1f},{ry:.1f} 0 1,0 {-2 * rx:.1f},0', col, w, op)


def yarn(x, y, r, col, col2):
    it = [C(x, y, r, col)]
    for k in range(4):
        a = -50 + k * 30
        it.append(rot([ring(x, y, r * .95, r * .45 - k * 2, col2, max(2, r * .07), .7)], a, x, y))
    it.append(C(x - r * .35, y - r * .4, r * .22, '#ffffff', .3))
    return G(it)


# ============ s052 美术教室 ============
def artroom():
    s = Scene('s052', '美术教室', '艺术与劳动', ['美术', '绘画', '色彩', '艺术'],
              dict(wall1='#F1EAF7', wall2='#E2D6EF', dado='#C9B6E2', floor1='#E8CDA6', floor2='#D2B086', wood='#C98F5A', wood2='#A06B3E',
                   canvas='#FFFDF6', sky='#BFE6F7', sun='#FFD36E', hill='#8ED081', hill2='#5FB7B0', vase='#5FA3D9', petal='#F7C13E', petal2='#F28C3A', stem='#5BA86A',
                   plaster='#FBF7F2', plaster2='#E3DCD3', plaster3='#CFC6BB', jar='#E8F5FA', brush='#E8B26A', ink='#3B3550',
                   p1='#F2584A', p2='#F7A23E', p3='#F7D648', p4='#7CC67A', p5='#4FB3D9', p6='#5B74D6', p7='#9B6CD3', p8='#E86BA6',
                   win1='#9BD7F5', win2='#E3F5FF', string='#9C8AB8'),
              desc='明亮的美术教室：墙上大幅十二色相环，两侧画架（向日葵静物与风景画），石膏几何体、颜料罐与画笔，晾画绳上挂着孩子们的作品。',
              stand={'ground_y': 900, 'x': [600, 1320]})
    bg = [R(0, 0, W, 780, s.lg([(0, 'wall1'), (1, 'wall2')])), R(0, 640, W, 140, 'dado', 0, .45), R(0, 636, W, 8, 'dado')]
    s.layer('wall', bg, 'fade', 0)
    # 十二色相环
    cx, cy, r0, r1 = 960, 330, 110, 210
    cols = ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8']
    hue = ['#F2584A', '#F57E3F', '#F7A23E', '#F7C641', '#E9DC4A', '#9CCF5A', '#4FB878', '#41B3B0', '#4FA3D9', '#5B74D6', '#8A62D0', '#D45FA8']
    wh = [C(cx, cy, r1 + 22, '#ffffff', extra='filter="url(#sh)"')]
    for k in range(12):
        a0 = (k * 30 - 105) * math.pi / 180; a1 = a0 + 30 * math.pi / 180
        p = lambda r, a: (cx + r * math.cos(a), cy + r * math.sin(a))
        x0, y0 = p(r1, a0); x1, y1 = p(r1, a1); x2, y2 = p(r0, a1); x3, y3 = p(r0, a0)
        wh.append(P(f'M{x0:.1f},{y0:.1f} A{r1},{r1} 0 0,1 {x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f} A{r0},{r0} 0 0,0 {x3:.1f},{y3:.1f}Z', hue[k], extra='stroke="#ffffff" stroke-width="4"'))
    wh += [C(cx, cy, r0 - 14, '#ffffff'), poly([(cx, cy - 70), (cx + 61, cy + 35), (cx - 61, cy + 35)], hue[0], .9), poly([(cx, cy + 70), (cx - 61, cy - 35), (cx + 61, cy - 35)], hue[9], .55)]
    s.layer('color_wheel', wh, 'zoom', .3, origin=f'{cx} {cy}')
    # 窗
    s.layer('window', [window(s, 90, 120, 300, 380, 'win1', 'win2', extra_items=[cloud(200, 230, .55), C(330, 520, 140, 'hill', .8)])], 'pop', .2)
    # 晾画绳 + 作品
    dl = [S('M0,40 Q480,120 960,60 Q1440,120 1920,40', 'string', 3)]
    random.seed(4)
    for k, x in enumerate([180, 420, 640, 1280, 1500, 1740]):
        u = x / 1920; local = (u * 2) % 1; y = (1 - local) ** 2 * (40 if u < .5 else 60) + 2 * local * (1 - local) * 120 + local ** 2 * (60 if u < .5 else 40)
        w_, h_ = 120, 92; ang = random.uniform(-6, 6)
        pic = [R(x - w_ / 2, y, w_, h_, 'canvas', 4, extra='filter="url(#shs)"'), R(x - w_ / 2 + 8, y + 8, w_ - 16, h_ - 16, ['sky', 'win2', 'wall1'][k % 3], 2)]
        if k % 3 == 0: pic += [C(x + 20, y + 30, 14, 'sun'), P(f'M{x - 52},{y + 84} Q{x - 20},{y + 44} {x + 10},{y + 70} Q{x + 34},{y + 50} {x + 52},{y + 84}Z', 'hill')]
        elif k % 3 == 1: pic += [C(x - 18, y + 46, 18, cols[k % 8]), C(x + 18, y + 40, 14, cols[(k + 3) % 8]), R(x - 2, y + 56, 4, 24, 'stem')]
        else: pic += [P(f'M{x - 40},{y + 70} L{x},{y + 22} L{x + 40},{y + 70}Z', cols[(k + 4) % 8]), R(x - 30, y + 66, 60, 10, cols[(k + 1) % 8], 2)]
        pic += [R(x - 6, y - 8, 12, 18, 'wood2', 3)]
        dl.append(rot(pic, ang, x, y))
    s.layer('drying_line', dl, 'drop', .5, loop='sway')
    fl = [R(0, 780, W, 300, s.lg([(0, 'floor1'), (1, 'floor2')]))] + [S(f'M0,{y} L{W},{y}', 'floor2', 3, .45) for y in (820, 880, 960)]
    random.seed(9)
    for _ in range(9): fl.append(E(random.uniform(150, 1800), random.uniform(840, 1040), random.uniform(10, 26), random.uniform(5, 10), cols[random.randint(0, 7)], .55))
    s.layer('floor', fl, 'rise', .1)
    # 后柜 + 石膏几何体
    cb = [R(1440, 560, 420, 220, 'wood', 10, extra='filter="url(#sh)"'), R(1456, 600, 190, 160, 'wood2', 6, .5), R(1654, 600, 190, 160, 'wood2', 6, .5), R(1430, 552, 440, 16, 'wood2', 6),
          shadow(1550, 552, 70, 6), C(1550, 494, 56, s.rg([(0, 'plaster'), (.7, 'plaster2'), (1, 'plaster3')], .38, .35)),
          R(1630, 452, 96, 100, 'plaster', 4), poly([(1630, 452), (1726, 452), (1746, 436), (1650, 436)], 'plaster2'), poly([(1726, 452), (1746, 436), (1746, 536), (1726, 552)], 'plaster3'),
          poly([(1800, 400), (1840, 552), (1760, 552)], 'plaster2'), poly([(1800, 400), (1840, 552), (1806, 552)], 'plaster3', .8)]
    s.layer('still_life', cb, 'rise', .45)

    def easel(x, ground, art):
        return G([shadow(x, ground, 150, 12, .18), S(f'M{x},{ground - 560} L{x - 120},{ground} M{x},{ground - 560} L{x + 120},{ground} M{x},{ground - 520} L{x + 20},{ground - 20}', 'wood2', 14),
                  R(x - 150, ground - 210, 300, 20, 'wood', 6), R(x - 150, ground - 540, 300, 330, 'canvas', 6, extra='filter="url(#sh)"'), *art])
    # 左画架：向日葵静物
    ex = 360; g = 900
    sf = [R(ex - 136, g - 526, 272, 302, 'wall1', 4)]
    sf += [P(f'M{ex - 40},{g - 230} Q{ex - 56},{g - 300} {ex - 26},{g - 330} L{ex + 26},{g - 330} Q{ex + 56},{g - 300} {ex + 40},{g - 230}Z', 'vase')]
    for fx, fy, rr in [(ex - 50, g - 420, 34), (ex + 40, g - 440, 38), (ex - 4, g - 486, 30)]:
        sf.append(S(f'M{ex},{g - 330} L{fx},{fy}', 'stem', 5))
        sf += [E(fx + rr * math.cos(a), fy + rr * math.sin(a), rr * .55, rr * .25, 'petal', extra=f'transform="rotate({math.degrees(a):.0f} {fx + rr * math.cos(a):.0f} {fy + rr * math.sin(a):.0f})"') for a in [q * math.pi / 6 for q in range(12)]]
        sf += [C(fx, fy, rr * .6, 'wood2'), C(fx, fy, rr * .35, 'petal2', .6)]
    s.layer('easel_left', [easel(ex, g, sf)], 'slide-l', .6)
    # 右画架：风景画（半成品）
    rx_ = 1600
    ls = [R(rx_ - 136, g - 526, 272, 302, 'sky', 4), C(rx_ + 60, g - 460, 28, 'sun'), P(f'M{rx_ - 136},{g - 300} Q{rx_ - 60},{g - 400} {rx_ + 10},{g - 330} Q{rx_ + 80},{g - 380} {rx_ + 136},{g - 320} L{rx_ + 136},{g - 224} L{rx_ - 136},{g - 224}Z', 'hill'),
          P(f'M{rx_ - 136},{g - 260} Q{rx_},{g - 300} {rx_ + 136},{g - 250} L{rx_ + 136},{g - 224} L{rx_ - 136},{g - 224}Z', 'hill2'),
          R(rx_ - 136, g - 526, 100, 302, 'canvas', 0, .55)]
    s.layer('easel_right', [easel(rx_, g, ls)], 'slide-r', .65)
    # 颜料与笔筒（近景小桌）
    tb = [shadow(1170, 930, 150, 12, .18), R(1040, 820, 260, 22, 'wood', 8), R(1060, 842, 14, 90, 'wood2'), R(1266, 842, 14, 90, 'wood2'),
          R(1070, 742, 56, 78, 'jar', 10, .9), *[S(f'M{1086 + k * 12},{760} L{1078 + k * 16},{700 - k * 8}', 'brush', 6) for k in range(3)],
          *[C(1078 + k * 16, 696 - k * 8, 7, cols[k + 2]) for k in range(3)]]
    for k, col in enumerate(['p1', 'p3', 'p5', 'p4']):
        x = 1160 + k * 34; tb += [R(x - 14, 790, 28, 30, col, 6), R(x - 14, 784, 28, 10, 'plaster', 4)]
    # 调色板
    tb += [P('M1110,815 C1060,812 1060,780 1100,776 C1150,770 1200,784 1200,800 C1200,816 1160,818 1110,815Z', 'wood', .0)]
    s.layer('paints', tb, 'pop', .85)
    pl = [shadow(560, 930, 120, 10, .15), P('M470,915 C420,912 420,860 480,850 C560,836 660,856 660,884 C660,912 600,918 470,915Z', 'wood'), C(500, 890, 14, 'floor1'),
          *[C(540 + k * 26, 870 + (k % 2) * 16, 11, cols[k]) for k in range(5)]]
    s.layer('palette', pl, 'pop', 1.0)
    s.layer('sparkle', [P(f'M{x},{y - 16} L{x + 4},{y - 4} L{x + 16},{y} L{x + 4},{y + 4} L{x},{y + 16} L{x - 4},{y + 4} L{x - 16},{y} L{x - 4},{y - 4}Z', 'sun') for x, y in [(700, 220), (1220, 160), (1240, 500), (690, 470)]], 'pop', 1.1, loop='twinkle')
    return s


# ============ s053 陶艺室 ============
def pottery():
    s = Scene('s053', '陶艺室', '艺术与劳动', ['美术', '陶艺', '劳动', '传统工艺'],
              dict(wall1='#F7E4D3', wall2='#EDCDB3', brickw='#E6BFA0', floor1='#D8CFC4', floor2='#C2B7AA', shelf='#A9774E', shelf2='#875A36',
                   clay='#C98458', clay2='#A9663F', clay3='#E3A57A', g1='#5FA8A0', g2='#F1E6D2', g3='#E2A64A', g4='#6E8FCC', g5='#D9705A', g6='#9BBF86',
                   kiln='#C0674A', kiln2='#9E513A', kbrick='#D78463', fire='#FF9A3D', fire2='#FFD36E', wheel='#5D6A78', wheel2='#8796A6', water='#9FD3E8',
                   lamp='#FFE3A3', leaf='#7DB57E', leaf2='#A9D69B', sack='#E9D9B8', sack2='#CDB98F', win1='#A9DDF5', win2='#EAF7FF'),
              desc='温暖的陶艺工作室：拉坯机上正在成形的陶罐，墙上木架摆满各色釉陶，左侧砖砌窑炉透出火光，陶土袋与工具。',
              stand={'ground_y': 910, 'x': [560, 1260]})
    bg = [R(0, 0, W, 800, s.lg([(0, 'wall1'), (1, 'wall2')]))]
    for y in range(560, 800, 40):
        for x in range(-((y // 40) % 2) * 60, W, 120): bg.append(R(x + 3, y + 3, 114, 34, 'brickw', 5, .5))
    s.layer('wall', bg, 'fade', 0)
    s.layer('window', [window(s, 820, 110, 280, 260, 'win1', 'win2', extra_items=[cloud(920, 200, .5), C(1060, 400, 120, 'leaf', .8)])], 'pop', .2)
    # 搁架与陶器
    def vessel(x, y, kind, col, sc=1.0):
        if kind == 'vase':
            d = f'M{x - 14 * sc},{y - 96 * sc} L{x + 14 * sc},{y - 96 * sc} Q{x + 10 * sc},{y - 76 * sc} {x + 30 * sc},{y - 50 * sc} Q{x + 44 * sc},{y - 20 * sc} {x + 24 * sc},{y} L{x - 24 * sc},{y} Q{x - 44 * sc},{y - 20 * sc} {x - 30 * sc},{y - 50 * sc} Q{x - 10 * sc},{y - 76 * sc} {x - 14 * sc},{y - 96 * sc}Z'
        elif kind == 'bowl':
            d = f'M{x - 44 * sc},{y - 36 * sc} L{x + 44 * sc},{y - 36 * sc} Q{x + 40 * sc},{y} {x + 16 * sc},{y} L{x - 16 * sc},{y} Q{x - 40 * sc},{y} {x - 44 * sc},{y - 36 * sc}Z'
        elif kind == 'jar':
            d = f'M{x - 22 * sc},{y - 76 * sc} L{x + 22 * sc},{y - 76 * sc} Q{x + 46 * sc},{y - 60 * sc} {x + 40 * sc},{y - 26 * sc} Q{x + 36 * sc},{y} {x + 20 * sc},{y} L{x - 20 * sc},{y} Q{x - 36 * sc},{y} {x - 40 * sc},{y - 26 * sc} Q{x - 46 * sc},{y - 60 * sc} {x - 22 * sc},{y - 76 * sc}Z'
        else:  # cup
            d = f'M{x - 24 * sc},{y - 52 * sc} L{x + 24 * sc},{y - 52 * sc} L{x + 20 * sc},{y} L{x - 20 * sc},{y}Z'
        it = [P(d, col)]
        if kind == 'cup': it.append(S(f'M{x + 22 * sc},{y - 40 * sc} q{18 * sc},0 {14 * sc},{20 * sc} q-2,{10 * sc} {-16 * sc},{10 * sc}', col, 6 * sc))
        it += [R(x - 30 * sc, y - (60 if kind != 'bowl' else 26) * sc, 60 * sc, 6 * sc, '#ffffff', 3, .25), E(x - 12 * sc, y - 40 * sc, 5 * sc, 12 * sc, '#ffffff', .3)]
        return G(it)
    sh = []
    for y in (250, 420, 590):
        sh += [R(1250, y, 600, 18, 'shelf', 6, extra='filter="url(#shs)"'), R(1270, y + 18, 14, 22, 'shelf2'), R(1816, y + 18, 14, 22, 'shelf2')]
    items = [[('vase', 'g1'), ('bowl', 'g3'), ('jar', 'g2'), ('cup', 'g4'), ('vase', 'g5')], [('jar', 'g6'), ('cup', 'g5'), ('vase', 'g4'), ('bowl', 'g2'), ('cup', 'g1')], [('bowl', 'g5'), ('vase', 'g3'), ('jar', 'g1'), ('cup', 'g6'), ('jar', 'g4')]]
    for r_, y in enumerate((250, 420, 590)):
        for k, (kind, col) in enumerate(items[r_]): sh.append(vessel(1310 + k * 118, y, kind, col, .95))
    s.layer('shelves', sh, 'slide-r', .45)
    fl = [R(0, 800, W, 280, s.lg([(0, 'floor1'), (1, 'floor2')]))] + [S(f'M0,{y} L{W},{y}', 'floor2', 3, .5) for y in (840, 920)]
    s.layer('floor', fl, 'rise', .1)
    # 窑炉
    kx = 300
    kn = [shadow(kx, 900, 230, 16, .22), R(kx - 210, 360, 420, 540, 'kiln', 30, extra='filter="url(#sh)"'), R(kx - 210, 360, 420, 40, 'kiln2', 20)]
    for y in range(420, 890, 44):
        for x in range(kx - 200 + ((y // 44) % 2) * 40, kx + 190, 80): kn.append(R(x, y, 72, 36, 'kbrick', 6, .55))
    kn += [P(f'M{kx - 110},860 L{kx - 110},640 A110,110 0 0,1 {kx + 110},640 L{kx + 110},860Z', 'kiln2'), P(f'M{kx - 86},860 L{kx - 86},650 A86,86 0 0,1 {kx + 86},650 L{kx + 86},860Z', s.lg([(0, 'fire2'), (1, 'fire')])),
           R(kx - 40, 250, 80, 120, 'kiln2', 8), R(kx - 54, 240, 108, 24, 'kiln', 8), C(kx + 150, 480, 24, 'wheel'), C(kx + 150, 480, 14, 'wheel2'), R(kx - 150, 460, 60, 40, 'wheel', 6), R(kx - 142, 468, 44, 24, 'water', 3)]
    for k in range(3):
        x = kx - 50 + k * 50; kn.append(vessel(x, 840, ['vase', 'jar', 'cup'][k], 'clay3', .8))
    s.layer('kiln', kn, 'rise', .3)
    s.layer('kiln_glow', [C(kx, 760, 150, 'fire', .45, 'filter="url(#b40)"'), P(f'M{kx - 30},860 Q{kx - 40},800 {kx},760 Q{kx + 40},800 {kx + 30},860Z', 'fire2', .8)], 'fade', .9, loop='glow')
    # 拉坯机
    wx = 1480; wy = 760
    wl = [shadow(wx, 910, 220, 14, .2), R(wx - 180, wy + 20, 360, 110, 'wheel', 24, extra='filter="url(#sh)"'), R(wx - 160, wy + 30, 320, 20, 'wheel2', 8, .6),
          R(wx - 30, wy + 130, 60, 30, 'wheel', 6), R(wx - 170, wy + 140, 40, 20, 'wheel', 6), R(wx + 130, wy + 140, 40, 20, 'wheel', 6),
          P(f'M{wx - 170},{wy + 20} Q{wx},{wy - 30} {wx + 170},{wy + 20}Z', 'wheel2'), E(wx, wy, 120, 18, 'wheel2'), E(wx, wy - 4, 112, 14, '#B8C4D0'),
          S(f'M{wx - 200},{wy + 70} q-40,0 -40,40 l0,60', 'wheel', 10), R(wx - 290, wy + 160, 80, 30, 'wheel', 8)]
    s.layer('wheel', wl, 'rise', .55)
    pot = [P(f'M{wx - 46},{wy - 6} Q{wx - 80},{wy - 70} {wx - 52},{wy - 130} Q{wx - 34},{wy - 160} {wx - 36},{wy - 190} L{wx + 36},{wy - 190} Q{wx + 34},{wy - 160} {wx + 52},{wy - 130} Q{wx + 80},{wy - 70} {wx + 46},{wy - 6}Z', s.lg([(0, 'clay2'), (.4, 'clay'), (1, 'clay2')], 0, 0, 1, 0)),
           E(wx, wy - 190, 36, 8, 'clay2'), E(wx, wy - 190, 26, 5, '#7E4A2C'),
           *[S(f'M{wx - 60 + k * 2},{wy - 40 - k * 26} q{60 - k * 2},10 {120 - k * 4},0', 'clay3', 3, .6) for k in range(4)]]
    s.layer('pot_on_wheel', pot, 'grow', .75, loop='bob', origin=f'{wx} {wy}')
    # 工具与陶土袋
    tl = [shadow(1080, 905, 120, 10, .16), R(980, 790, 200, 112, 'sack', 30), R(980, 790, 200, 30, 'sack2', 20), P('M1040,792 Q1080,760 1120,792Z', 'sack2'),
          E(1080, 880, 80, 12, 'sack2', .5), shadow(1260, 905, 70, 8), R(1200, 830, 120, 74, 'water', 12, .85), R(1194, 822, 132, 16, 'wheel2', 6),
          S('M1230,830 L1210,770', 'shelf', 6), C(1206, 760, 12, 'sack'), shadow(1750, 905, 90, 10), R(1680, 860, 140, 46, 'shelf', 8), R(1690, 836, 50, 26, 'clay', 8), R(1750, 840, 56, 22, 'clay3', 8)]
    s.layer('tools', tl, 'pop', .9)
    lp = []
    for x in (700, 1480):
        lp += [S(f'M{x},0 L{x},90', 'shelf2', 3), P(f'M{x - 56},150 Q{x},70 {x + 56},150Z', 'g3'), E(x, 152, 58, 9, 'lamp'), C(x, 170, 80, 'lamp', .4, 'filter="url(#b40)"')]
    s.layer('lamps', lp, 'drop', 1.0, loop='glow')
    s.layer('plant', [potted(1880, 800, .9, 'g5', 'clay2', 'leaf', 'leaf2'), potted(600, 800, .8, 'g1', 'shelf2', 'leaf', 'leaf2')], 'grow', 1.1, loop='sway')
    return s


# ============ s054 合唱舞台 ============
def choirstage():
    s = Scene('s054', '合唱舞台', '艺术与劳动', ['音乐', '合唱', '表演', '艺术节'],
              dict(back1='#6F5AA8', back2='#4F3F86', shell='#8B77C2', shell2='#A493D4', gold='#F2C14E', gold2='#D9A23A', val='#2F8C88', val2='#22706D',
                   riser='#E9E2F5', riser2='#C9BFE3', riser3='#B0A4D6', floor1='#C98E5B', floor2='#A86E40', piano='#24222C', piano2='#3A3744',
                   stand='#3A3744', spot='#FFF3C4', star='#FFE48A', rose='#F28BA0', rose2='#F7B7C4', leaf='#5FA873', foot='#FFE7A8'),
              desc='校园艺术节合唱舞台：紫色声学穹壳背景，三层合唱台阶，三角钢琴与指挥谱架，聚光灯与星星串灯，舞台前沿一排脚灯。',
              stand={'ground_y': 880, 'x': [560, 1360]})
    s.layer('back', [R(0, 0, W, 760, s.lg([(0, 'back1'), (1, 'back2')]))], 'fade', 0)
    sh = []
    for k in range(6):
        r = 860 - k * 120
        sh.append(P(f'M{960 - r},760 A{r},{r * .78} 0 0,1 {960 + r},760Z', 'shell' if k % 2 == 0 else 'shell2', .55 if k % 2 == 0 else .4))
    for k in range(-6, 7):
        a = -math.pi / 2 + k * .22
        sh.append(S(f'M960,760 L{960 + 900 * math.cos(a):.0f},{760 + 700 * math.sin(a):.0f}', 'shell2', 3, .25))
    s.layer('shell', sh, 'zoom', .2, origin='960 760')
    # 顶部帷幔
    vl = [R(0, 0, W, 70, 'val2')]
    for k in range(12):
        x = k * 160
        vl.append(P(f'M{x},60 Q{x + 80},150 {x + 160},60Z', 'val'))
    vl += [R(0, 56, W, 10, 'gold'), *[C(80 + k * 160, 136, 10, 'gold') for k in range(12)]]
    s.layer('valance', vl, 'drop', .35)
    # 星星串灯
    st = [S('M0,200 Q480,280 960,210 Q1440,280 1920,200', 'gold2', 2.5)]
    for k in range(17):
        u = k / 16; local = (u * 2) % 1; y = (1 - local) ** 2 * (200 if u < .5 else 210) + 2 * local * (1 - local) * 280 + local ** 2 * (210 if u < .5 else 200)
        x = u * 1920; y += 20
        pts = [(x + (14 if q % 2 == 0 else 6) * math.cos(-math.pi / 2 + q * math.pi / 5), y + (14 if q % 2 == 0 else 6) * math.sin(-math.pi / 2 + q * math.pi / 5)) for q in range(10)]
        st += [S(f'M{x},{y - 22} L{x},{y - 14}', 'gold2', 2), poly(pts, 'star'), C(x, y, 22, 'star', .3, 'filter="url(#b6)"')]
    s.layer('star_lights', st, 'drop', .5, loop='twinkle')
    # 舞台地板
    fl = [R(0, 760, W, 320, s.lg([(0, 'floor1'), (1, 'floor2')]))] + [S(f'M{x},760 L{x + (x - 960) * .4:.0f},1080', 'floor2', 3, .45) for x in range(0, W + 1, 120)]
    fl += [R(0, 1010, W, 70, 'floor2'), R(0, 1006, W, 6, 'gold2')]
    s.layer('floor', fl, 'rise', .1)
    # 合唱台阶（三层，弧形平面化为梯形）
    rs = [shadow(960, 800, 640, 18, .2)]
    for k, (w_, y, h) in enumerate([(1200, 740, 60), (1000, 680, 60), (800, 620, 60)]):
        rs += [R(960 - w_ / 2, y, w_, h, 'riser' if k % 2 == 0 else 'riser2', 10, extra='filter="url(#shs)"'), R(960 - w_ / 2, y, w_, 10, 'riser3', 4, .6)]
    s.layer('risers', rs, 'rise', .4)
    s.layer('spots', [beam(560, 640, 520, 820, 0, 800, s, .25), beam(1280, 1360, 1100, 1400, 0, 800, s, .25), beam(920, 1000, 800, 1120, 0, 760, s, .3),
                      E(960, 760, 360, 50, 'spot', .35, 'filter="url(#b20)"')], 'fade', .8, loop='glow')
    # 三角钢琴（右，侧面）
    px = 1560
    pn = [shadow(px + 40, 880, 260, 16, .25),
          P(f'M{px - 180},640 L{px + 140},640 C{px + 260},640 {px + 270},560 {px + 200},540 C{px + 120},520 {px + 60},470 {px - 20},470 L{px - 180},470Z', 'piano', extra='filter="url(#sh)"'),
          P(f'M{px - 180},470 L{px - 20},470 L{px + 80},380 L{px - 150},420Z', 'piano2'), S(f'M{px - 20},470 L{px + 80},380', 'gold2', 3),
          R(px - 200, 600, 120, 26, 'piano2', 4), R(px - 196, 604, 112, 12, '#ffffff'),
          R(px - 170, 640, 22, 220, 'piano', 6), R(px + 120, 640, 22, 220, 'piano', 6), R(px + 210, 610, 18, 240, 'piano', 6), E(px - 159, 864, 18, 6, 'gold'), E(px + 131, 864, 18, 6, 'gold'),
          R(px - 30, 830, 70, 10, 'gold', 3), R(px - 300, 720, 110, 24, 'piano2', 8), R(px - 290, 744, 12, 116, 'piano'), R(px - 202, 744, 12, 116, 'piano')]
    s.layer('piano', pn, 'slide-r', .6)
    # 指挥台与谱架（左）
    cx_ = 360
    cd = [shadow(cx_, 880, 160, 12, .22), R(cx_ - 140, 820, 280, 60, 'gold2', 10), R(cx_ - 140, 820, 280, 12, 'gold', 6),
          S(f'M{cx_ + 40},820 L{cx_ + 40},640', 'stand', 8), S(f'M{cx_ + 40},820 L{cx_},846 M{cx_ + 40},820 L{cx_ + 80},846', 'stand', 6),
          rot([R(cx_ - 50, 560, 180, 110, 'stand', 6), R(cx_ - 40, 568, 160, 92, '#ffffff', 4, .95)] + [R(cx_ - 30, 584 + q * 16, 140, 2, 'back1', 0, .6) for q in range(5)], -12, cx_ + 40, 640),
          S(f'M{cx_ - 60},600 L{cx_ - 120},540', 'stand', 4), C(cx_ - 120, 540, 5, '#ffffff')]
    s.layer('podium', cd, 'slide-l', .65)
    # 花篮
    fb = []
    for x in (110, 1830):
        fb += [shadow(x, 1000, 70, 8), P(f'M{x - 56},900 L{x + 56},900 L{x + 40},1000 L{x - 40},1000Z', 'gold2'), leafy(x, 900, 1.2, 'leaf', 'leaf', 7)]
        for k in range(7):
            a = -math.pi / 2 + (k - 3) * .38; fx, fy = x + 56 * math.cos(a), 880 + 50 * math.sin(a)
            fb += [C(fx, fy, 18, 'rose' if k % 2 else 'rose2'), C(fx, fy, 7, 'rose', .8)]
    s.layer('flowers', fb, 'grow', .9, loop='sway')
    fo = []
    for x in range(80, W, 160): fo += [P(f'M{x - 30},1010 L{x + 30},1010 L{x + 22},990 L{x - 22},990Z', 'piano2'), E(x, 990, 20, 6, 'foot'), C(x, 980, 40, 'foot', .35, 'filter="url(#b20)"')]
    s.layer('footlights', fo, 'fade', 1.0, loop='glow')
    nt = []
    for x, y, sc in [(620, 360, 1), (1300, 330, .8), (760, 470, .7), (1180, 460, .9)]:
        nt += [E(x, y, 16 * sc, 12 * sc, 'star', extra=f'transform="rotate(-20 {x} {y})"'), R(x + 12 * sc, y - 60 * sc, 5 * sc, 60 * sc, 'star'), P(f'M{x + 12 * sc},{y - 60 * sc} q{26 * sc},{8 * sc} {22 * sc},{34 * sc} q{-5 * sc},{-18 * sc} {-22 * sc},{-20 * sc}Z', 'star')]
    s.layer('notes', nt, 'pop', 1.15, loop='bob')
    return s


# ============ s055 木工劳技室 ============
def woodshop():
    s = Scene('s055', '木工劳技室', '艺术与劳动', ['劳动', '木工', '劳动技术', '动手实践'],
              dict(wall1='#E3EDDD', wall2='#CFE0C6', peg='#E8CFA4', peg2='#D3B27E', hole='#B99668', top='#D9A566', top2='#B98146', leg='#9A6638', leg2='#7E512B',
                   plank1='#F0C891', plank2='#E3B577', plank3='#CF9C5E', metal='#8C98A6', metal2='#C2CAD4', red='#E8584A', orange='#F2973E', yellow='#F2C14E', blue='#4F8FC9', green='#6FB27C',
                   floor1='#D7D2C8', floor2='#BFB8AC', shav='#F6DDB2', bird='#5FA8A0', roof='#E57766', win1='#A9DDF5', win2='#EAF7FF', goggle='#9FD8F0'),
              desc='劳动技术木工教室：洞洞板上挂着锯、锤、尺、角尺等工具，厚实木工台带台钳，木板堆、锯木马、做好的小鸟屋与刨花。',
              stand={'ground_y': 910, 'x': [600, 1300]})
    s.layer('wall', [R(0, 0, W, 800, s.lg([(0, 'wall1'), (1, 'wall2')])), *[R(0, y, W, 3, 'wall2', 0, .7) for y in range(60, 800, 60)]], 'fade', 0)
    s.layer('window', [window(s, 1500, 120, 300, 260, 'win1', 'win2', extra_items=[cloud(1600, 210, .5), C(1760, 400, 120, 'green', .7)])], 'pop', .2)
    # 洞洞板 + 工具
    px, py, pw, ph = 380, 110, 860, 400
    pg = [R(px, py, pw, ph, 'peg', 14, extra='filter="url(#sh)"')]
    for yy in range(py + 22, py + ph - 10, 32):
        for xx in range(px + 22, px + pw - 10, 32): pg.append(C(xx, yy, 4, 'hole'))
    # 手锯
    pg += [P(f'M{px + 60},{py + 70} L{px + 300},{py + 70} L{px + 300},{py + 120} L{px + 90},{py + 140}Z', 'metal2'),
           *[poly([(px + 90 + k * 14, py + 139 - k * .95), (px + 97 + k * 14, py + 150 - k * 1), (px + 104 + k * 14, py + 138 - k * .95)], 'metal2') for k in range(15)],
           R(px + 290, py + 54, 70, 84, 'red', 22), R(px + 312, py + 80, 28, 34, 'peg', 10)]
    # 锤子
    pg += [R(px + 420, py + 60, 18, 200, 'leg', 8), R(px + 380, py + 50, 100, 38, 'metal', 8), R(px + 380, py + 50, 24, 38, 'metal2', 6)]
    # 角尺
    pg += [P(f'M{px + 520},{py + 60} L{px + 550},{py + 60} L{px + 550},{py + 260} L{px + 700},{py + 260} L{px + 700},{py + 290} L{px + 520},{py + 290}Z', 'yellow')]
    for k in range(10): pg.append(R(px + 550, py + 75 + k * 18, 12 if k % 2 else 18, 3, 'leg'))
    # 螺丝刀、凿子
    for k, col in enumerate(['blue', 'orange', 'green']):
        x = px + 740 + k * 34; pg += [R(x - 11, py + 50, 22, 70, col, 10), R(x - 4, py + 120, 8, 90, 'metal')]
    # 卷尺、夹子
    pg += [C(px + 110, py + 260, 50, 'yellow'), C(px + 110, py + 260, 22, 'metal2'), R(px + 150, py + 290, 60, 14, 'metal2', 3),
           R(px + 250, py + 230, 30, 120, 'metal', 6), R(px + 230, py + 230, 100, 24, 'metal', 6), R(px + 230, py + 330, 100, 20, 'blue', 6),
           S(f'M{px + 360},{py + 350} L{px + 470},{py + 350}', 'top2', 18), R(px + 470, py + 338, 40, 24, 'orange', 6)]
    s.layer('pegboard', pg, 'drop', .3)
    fl = [R(0, 800, W, 280, s.lg([(0, 'floor1'), (1, 'floor2')]))] + [S(f'M0,{y} L{W},{y}', 'floor2', 3, .5) for y in (840, 910, 1000)]
    s.layer('floor', fl, 'rise', .1)
    # 木板堆（左）
    pk = [shadow(170, 880, 160, 12, .2)]
    for k, (h, col) in enumerate([(520, 'plank1'), (480, 'plank2'), (560, 'plank3'), (440, 'plank1'), (500, 'plank2')]):
        x = 40 + k * 56; pk.append(rot([R(x, 880 - h, 46, h, col, 6), R(x + 6, 900 - h, 6, h - 40, '#ffffff', 3, .2)], -6 + k * 1.5, x + 23, 880))
    s.layer('planks', pk, 'slide-l', .45)
    # 木工台
    bx0, bx1, by = 420, 1500, 640
    bn = [shadow((bx0 + bx1) / 2, 900, 560, 16, .2), R(bx0 + 30, by + 40, 40, 220, 'leg'), R(bx1 - 70, by + 40, 40, 220, 'leg'), R(bx0 + 70, by + 180, bx1 - bx0 - 140, 26, 'leg2', 4),
          R(bx0, by, bx1 - bx0, 54, s.lg([(0, 'top'), (1, 'top2')]), 8, extra='filter="url(#sh)"'), R(bx0, by, bx1 - bx0, 8, '#F2C68C', 4)]
    for x in range(bx0 + 120, bx1, 200): bn.append(R(x, by + 8, 3, 46, 'top2', 0, .6))
    # 台钳（左端）
    bn += [R(bx0 - 40, by - 10, 90, 80, 'metal', 8), R(bx0 - 80, by + 24, 60, 14, 'metal2', 4), C(bx0 - 84, by + 31, 12, 'metal'), R(bx0 + 50, by - 40, 30, 50, 'plank2', 4)]
    s.layer('bench', bn, 'rise', .3)
    # 台上：小鸟屋、木块、护目镜、刨子
    bh = 1180
    tp = [shadow(bh, by, 90, 6), R(bh - 60, by - 120, 120, 120, 'bird', 6), poly([(bh - 80, by - 116), (bh, by - 190), (bh + 80, by - 116)], 'roof'), C(bh, by - 70, 20, 'leg2'),
          R(bh - 4, by - 40, 8, 26, 'leg'), R(bh - 22, by - 16, 44, 6, 'leg')]
    tp += [shadow(860, by, 120, 6), R(760, by - 50, 200, 50, 'plank1', 6), R(774, by - 74, 120, 24, 'top2', 6), R(800, by - 92, 26, 20, 'red', 6)]  # 刨子
    tp += [R(560, by - 40, 60, 40, 'plank2', 4), R(626, by - 30, 40, 30, 'plank3', 4), poly([(680, by), (740, by), (710, by - 50)], 'plank1')]
    tp += [E(1360, by - 16, 32, 18, 'goggle', .9), E(1424, by - 16, 32, 18, 'goggle', .9), S(f'M1328,{by - 16} Q1392,{by - 50} 1456,{by - 16}', 'orange', 6), R(1386, by - 22, 12, 8, 'orange')]
    s.layer('bench_items', tp, 'pop', .6)
    # 锯木马 + 木板（右）
    sx = 1720
    sh = [shadow(sx, 900, 170, 12, .2), S(f'M{sx - 120},740 L{sx - 160},900 M{sx - 120},740 L{sx - 80},900 M{sx + 120},740 L{sx + 80},900 M{sx + 120},740 L{sx + 160},900', 'leg', 16),
          R(sx - 150, 724, 300, 26, 'leg2', 6), R(sx - 190, 690, 380, 34, 'plank1', 6), S(f'M{sx + 20},690 L{sx + 20},724', 'top2', 3, .8)]
    s.layer('sawhorse', sh, 'slide-r', .7)
    random.seed(3)
    sv = []
    for _ in range(14):
        x = random.choice([random.uniform(500, 1500), random.uniform(1550, 1880)]); y = random.uniform(880, 1050) if x > 1500 or random.random() < .5 else by - 4
        r = random.uniform(8, 16)
        sv.append(S(f'M{x - r},{y} a{r},{r} 0 1,1 {r * 1.6},{-r * .4} a{r * .6},{r * .6} 0 1,0 {-r * .8},{r * .3}', 'shav', 4))
    s.layer('shavings', sv, 'fade', .85)
    lp = [S('M960,0 L960,40', 'leg2', 3), R(700, 40, 520, 24, 'metal', 12), R(714, 60, 492, 8, '#FFF6D6'), P('M700,68 L1220,68 L1400,640 L520,640Z', s.lg([(0, '#FFF6D6', .4), (1, '#FFF6D6', 0)]))]
    s.layer('lamp', lp, 'drop', .9, loop='glow')
    s.layer('plant', [potted(1860, 640, .8, 'roof', 'leg2', 'green', 'wall2')], 'grow', 1.0, loop='sway', origin='1860 640')
    return s


# ============ s056 烹饪教室 ============
def cooking():
    s = Scene('s056', '烹饪教室', '艺术与劳动', ['劳动', '烹饪', '营养', '生活技能'],
              dict(wall1='#FFF4DC', wall2='#F7E4BD', tile='#D5EEE6', tile2='#BFE3D7', cab='#5FAFA6', cab2='#4C958D', top='#F4F1EA', top2='#DCD6CA',
                   hood='#C9D1DA', hood2='#A9B4C0', steel='#B8C2CC', pot='#E8584A', pot2='#C9463A', pan='#3A3F48', fire='#4F8FE8', fire2='#9FC6FF',
                   fridge='#F7F7F4', fridge2='#E0E2E0', wood='#D9A566', wood2='#B98146', tomato='#EF5A45', carrot='#F2973E', green='#6DBA6A', green2='#A9D98A',
                   egg='#FFF7E8', yolk='#FFC93E', jar='#FFFFFF', red='#F2836B', yellow='#F7C55E', win1='#A9DDF5', win2='#EAF7FF', steam='#FFFFFF'),
              desc='明亮的烹饪教室：薄荷色瓷砖墙，灶台上汤锅冒着热气、平底锅煎蛋，吸油烟机、挂杆厨具、调料架，砧板上的番茄胡萝卜与冰箱。',
              stand={'ground_y': 910, 'x': [580, 1300]})
    s.layer('wall', [R(0, 0, W, 800, s.lg([(0, 'wall1'), (1, 'wall2')]))], 'fade', 0)
    tl = [R(0, 360, W, 330, 'tile')]
    for y in range(360, 690, 44): tl.append(R(0, y, W, 3, 'tile2'))
    for y in range(360, 690, 44):
        for x in range(((y - 360) // 44 % 2) * 44, W, 88): tl.append(R(x, y, 3, 44, 'tile2'))
    s.layer('tiles', tl, 'fade', .1)
    s.layer('window', [window(s, 120, 110, 300, 210, 'win1', 'win2', extra_items=[cloud(220, 190, .5), C(380, 330, 90, 'green', .7)]),
                       *[potted(170 + k * 90, 336, .55, ['red', 'yellow', 'cab'][k], 'wood2', 'green', 'green2') for k in range(3)]], 'pop', .2)
    # 吸油烟机（中心偏左）
    hx = 760
    hd = [P(f'M{hx - 60},0 L{hx + 60},0 L{hx + 60},190 L{hx - 60},190Z', 'hood2'), P(f'M{hx - 200},300 L{hx + 200},300 L{hx + 80},190 L{hx - 80},190Z', 'hood', extra='filter="url(#sh)"'),
          R(hx - 210, 296, 420, 22, 'hood2', 6), R(hx - 180, 318, 360, 6, '#FFF6D6', 3)]
    s.layer('hood', hd, 'drop', .3)
    # 挂杆与厨具
    ut = [R(1060, 250, 460, 10, 'steel', 5)]
    for k, kind in enumerate(['ladle', 'spat', 'whisk', 'pan', 'ladle']):
        x = 1100 + k * 90
        ut.append(S(f'M{x},258 L{x},274', 'hood2', 3))
        if kind == 'ladle': ut += [R(x - 5, 274, 10, 130, 'steel', 4), P(f'M{x - 26},400 A26,26 0 0,0 {x + 26},400Z', 'steel')]
        elif kind == 'spat': ut += [R(x - 5, 274, 10, 90, 'wood2', 4), R(x - 22, 360, 44, 56, 'wood', 8)]
        elif kind == 'whisk': ut += [R(x - 6, 274, 12, 60, 'red', 5)] + [ring(x, 380, 8 + q * 7, 48, 'steel', 3) for q in range(3)]
        else: ut += [R(x - 5, 274, 10, 60, 'pan', 4), C(x, 370, 40, 'pan'), C(x, 370, 30, '#4A505A')]
    s.layer('utensils', ut, 'drop', .5, loop='sway')
    # 调料架
    sp = [R(1600, 260, 260, 14, 'wood2', 5, extra='filter="url(#shs)"'), R(1600, 400, 260, 14, 'wood2', 5, extra='filter="url(#shs)"')]
    for row, y in enumerate((260, 400)):
        for k in range(4):
            x = 1630 + k * 62; col = ['red', 'yellow', 'green', 'carrot', 'tomato', 'cab', 'yolk', 'green2'][row * 4 + k]
            sp += [R(x - 20, y - 70, 40, 70, 'jar', 10, .9), R(x - 20, y - 40, 40, 40, col, 8, .85), R(x - 22, y - 82, 44, 16, 'wood', 5)]
    s.layer('spice_rack', sp, 'slide-r', .45)
    fl = [R(0, 800, W, 280, s.lg([(0, '#E9DCC8'), (1, '#D6C5AC')]))]
    for x in range(0, W, 120):
        for y in (800, 900, 1000): fl.append(R(x + ((y // 100) % 2) * 60, y, 116, 96, '#ffffff', 4, .18))
    s.layer('floor', fl, 'rise', .1)
    # 橱柜 + 台面
    cb = [R(0, 720, W, 120, 'cab', 0), R(0, 690, W, 34, s.lg([(0, 'top'), (1, 'top2')]), 6), R(0, 690, W, 6, '#ffffff', 0, .7)]
    for x in range(20, W, 240): cb += [R(x, 736, 220, 70, 'cab2', 10, .45), R(x + 90, 752, 40, 8, 'yellow', 4)]
    s.layer('counter', cb, 'rise', .2)
    # 灶台
    st = [R(hx - 170, 676, 340, 20, 'pan', 6), C(hx - 85, 676, 30, 'fire', .6), C(hx + 85, 676, 30, 'fire', .6)]
    st += [shadow(hx - 85, 672, 90, 6), R(hx - 160, 560, 150, 116, 'pot', 18), R(hx - 172, 552, 174, 20, 'pot2', 8), R(hx - 190, 580, 30, 14, 'pot2', 6), R(hx - 12, 580, 30, 14, 'pot2', 6),
           R(hx - 150, 576, 30, 80, '#ffffff', 10, .2)]
    st += [E(hx + 85, 664, 80, 14, 'pan'), R(hx + 160, 658, 140, 12, 'pan', 6), E(hx + 85, 660, 66, 9, '#4A505A'), E(hx + 70, 658, 30, 7, 'egg'), C(hx + 72, 657, 9, 'yolk')]
    s.layer('stove', st, 'pop', .55)
    s.layer('flames', [P(f'M{x - 26},678 Q{x - 20},656 {x - 8},666 Q{x},640 {x + 8},666 Q{x + 20},656 {x + 26},678Z', 'fire') for x in (hx - 85, hx + 85)] +
            [C(hx - 85, 670, 40, 'fire2', .4, 'filter="url(#b6)"')], 'fade', .9, loop='glow')
    s.layer('steam', [S(f'M{x},540 q-18,-30 0,-60 q18,-30 0,-60 q-18,-30 0,-60', 'steam', 8, .75) for x in (hx - 120, hx - 85, hx - 50)], 'fade', 1.1, loop='flow')
    # 砧板与蔬菜
    cbx = 1240
    cu = [shadow(cbx, 690, 150, 6), R(cbx - 150, 668, 300, 24, 'wood', 10), C(cbx + 130, 680, 8, 'wood2'),
          C(cbx - 80, 646, 26, 'tomato'), P(f'M{cbx - 92},{622} l12,8 l12,-8 l-12,-4Z', 'green'), E(cbx - 20, 660, 24, 10, 'tomato'), E(cbx + 14, 660, 18, 9, 'tomato', .9),
          rot([P(f'M{cbx + 40},652 L{cbx + 150},640 L{cbx + 150},666Z', 'carrot'), P(f'M{cbx + 150},640 l20,-14 l-4,18 l16,6 l-32,4Z', 'green')], -4, cbx + 90, 655),
          R(cbx - 40, 640, 120, 8, 'steel', 3, extra=f'transform="rotate(-8 {cbx + 20} 644)"'), R(cbx + 70, 628, 40, 12, 'pan', 4, extra=f'transform="rotate(-8 {cbx + 20} 644)"')]
    cu += [shadow(1440, 690, 70, 6), P('M1380,636 L1500,636 Q1496,690 1440,690 Q1384,690 1380,636Z', 'jar'), C(1410, 628, 16, 'green2'), C(1440, 620, 18, 'green'), C(1470, 630, 14, 'yellow'),
           P('M1380,636 L1500,636 Q1496,690 1440,690 Q1384,690 1380,636Z', 'cab', .25)]
    s.layer('cutting_board', cu, 'pop', .7)
    # 冰箱
    fx = 1760
    fr = [shadow(fx, 900, 140, 12, .2), R(fx - 130, 300, 260, 600, 'fridge', 24, extra='filter="url(#sh)"'), R(fx - 130, 520, 260, 6, 'fridge2'), R(fx + 90, 360, 12, 120, 'steel', 6), R(fx + 90, 560, 12, 160, 'steel', 6),
          R(fx - 100, 340, 60, 40, 'red', 6, extra=f'transform="rotate(-6 {fx - 70} 360)"'), C(fx - 10, 360, 14, 'yellow'), R(fx - 100, 600, 70, 90, '#ffffff', 4, .9, extra=f'transform="rotate(4 {fx - 65} 645)"'),
          R(fx - 90, 616, 50, 6, 'cab', 3), R(fx - 90, 632, 40, 6, 'cab', 3), R(fx - 90, 648, 46, 6, 'cab', 3)]
    s.layer('fridge', fr, 'slide-r', .65)
    # 近景：餐桌一角放鸡蛋碗
    s.layer('egg_bowl', [shadow(300, 900, 110, 10), P('M200,840 L400,840 Q392,900 300,900 Q208,900 200,840Z', 'cab'), E(300, 840, 100, 14, 'cab2'),
                         E(260, 830, 22, 28, 'egg'), E(300, 822, 22, 28, 'egg'), E(340, 830, 22, 28, 'egg')], 'pop', .9)
    return s


# ============ s057 创客空间 ============
def makerspace():
    s = Scene('s057', '创客空间', '艺术与劳动', ['科学', '信息科技', '编程', '创客'],
              dict(wall1='#E4EEFA', wall2='#CFDDF2', hex='#D7E4F6', navy='#2E3F66', navy2='#40568A', orange='#F28C3E', orange2='#F7B26A', lime='#9AD56A', teal='#3FB8B0',
                   pink='#F27C9A', yellow='#F7D04E', top='#F4F6FA', top2='#D9DFE8', leg='#8794A8', cork='#D9B07A', cork2='#C89A62', paper='#FFFFFF', blue='#5B8FE0',
                   screen='#1F2A44', code1='#7FE0C8', code2='#F7D04E', code3='#F28CB0', metal='#B5BFCC', metal2='#8A96A8', print='#3FB8B0', floor1='#C9D3E0', floor2='#B3BFCF', gear='#9FB4D6', gear2='#8AA2CA'),
              desc='校园创客空间：六边形墙面与大齿轮装饰，3D 打印机正在打印、笔记本电脑上的彩色代码、编程小车与机械臂，空中悬停的无人机和灵感软木板。',
              stand={'ground_y': 910, 'x': [600, 1320]})
    bg = [R(0, 0, W, 800, s.lg([(0, 'wall1'), (1, 'wall2')]))]
    for r_ in range(10):
        for k in range(22):
            x = k * 96 + (r_ % 2) * 48; y = r_ * 84
            pts = [(x + 40 * math.cos(math.pi / 6 + q * math.pi / 3), y + 40 * math.sin(math.pi / 6 + q * math.pi / 3)) for q in range(6)]
            bg.append(poly(pts, 'hex', .55))
    s.layer('wall', bg, 'fade', 0)

    def gear(x, y, r, n, col, hole):
        pts = []
        for k in range(n * 2):
            a0 = k * math.pi / n
            rr = r if k % 2 == 0 else r * .82
            pts += [(x + rr * math.cos(a0 - math.pi / n / 2.4), y + rr * math.sin(a0 - math.pi / n / 2.4)), (x + rr * math.cos(a0 + math.pi / n / 2.4), y + rr * math.sin(a0 + math.pi / n / 2.4))]
        return G([poly(pts, col), C(x, y, r * .5, hole), C(x, y, r * .18, col)])
    s.layer('gears', [gear(960, 220, 150, 14, 'gear', 'wall1'), gear(1170, 330, 80, 10, 'gear2', 'wall1'), gear(800, 380, 60, 8, 'gear2', 'wall1')], 'zoom', .25, loop='sway', origin='960 220')
    # 软木板
    ck = [R(90, 110, 420, 300, 'cork', 14, extra='filter="url(#sh)"'), R(104, 124, 392, 272, 'cork2', 8, .35)]
    for x, y, w_, h_, col, a in [(130, 150, 140, 110, 'blue', -4), (300, 140, 170, 120, 'paper', 3), (150, 280, 120, 90, 'yellow', 5), (300, 285, 170, 90, 'paper', -3)]:
        it = [R(x, y, w_, h_, col, 4, extra='filter="url(#shs)"'), C(x + w_ / 2, y + 8, 7, 'orange')]
        if col == 'blue':
            it += [S(f'M{x + 20},{y + 80} L{x + 60},{y + 40} L{x + 90},{y + 70} L{x + 120},{y + 30}', '#ffffff', 3), C(x + 60, y + 40, 5, '#ffffff')]
        elif col == 'paper':
            it += [ring(x + 40, y + h_ / 2 + 6, 22, 22, 'blue', 3), R(x + 80, y + 36, 70, 6, 'blue', 3, .6), R(x + 80, y + 54, 50, 6, 'blue', 3, .6), R(x + 80, y + 72, 60, 6, 'blue', 3, .6)]
        else:
            it += [C(x + w_ / 2, y + 44, 18, 'orange'), R(x + w_ / 2 - 8, y + 62, 16, 14, 'navy', 3)]
        ck.append(rot(it, a, x + w_ / 2, y + h_ / 2))
    s.layer('corkboard', ck, 'slide-l', .4)
    # 置物架 + LED 灯带
    sh = []
    for y in (240, 420):
        sh += [R(1460, y, 380, 16, 'navy2', 6, extra='filter="url(#shs)"')]
    sh += [R(1490, 160, 70, 80, 'orange', 8), R(1580, 180, 60, 60, 'teal', 8), R(1660, 140, 50, 100, 'yellow', 8), C(1770, 200, 40, 'pink'), C(1770, 200, 16, 'wall1'),
           R(1490, 350, 110, 70, 'navy', 8), *[C(1510 + k * 22, 370, 6, ['lime', 'pink', 'yellow', 'teal'][k]) for k in range(4)], R(1620, 330, 60, 90, 'metal', 8), R(1700, 360, 110, 60, 'lime', 10)]
    s.layer('shelves', sh, 'slide-r', .45)
    led = []
    for y in (256, 436):
        for k in range(16): led.append(C(1474 + k * 23, y + 6, 4, ['pink', 'yellow', 'lime', 'teal'][k % 4]))
    s.layer('led', led, 'fade', 1.0, loop='twinkle')
    fl = [R(0, 800, W, 280, s.lg([(0, 'floor1'), (1, 'floor2')]))] + [S(f'M{x},800 L{x + (x - 960) * .35:.0f},1080', 'floor2', 3, .5) for x in range(0, W + 1, 160)]
    s.layer('floor', fl, 'rise', .1)
    # 工作台
    bn = [shadow(960, 900, 760, 16, .18), R(160, 680, 1600, 34, s.lg([(0, 'top'), (1, 'top2')]), 8, extra='filter="url(#sh)"'), R(160, 680, 1600, 6, '#ffffff', 0, .7)]
    for x in (200, 920, 1700): bn += [R(x, 714, 20, 190, 'leg', 4)]
    bn += [R(200, 840, 1520, 12, 'leg', 4)]
    s.layer('bench', bn, 'rise', .25)
    # 3D 打印机（左）
    p3 = 400
    pr = [shadow(p3, 680, 140, 8), R(p3 - 130, 400, 260, 280, 'navy', 14, extra='filter="url(#sh)"'), R(p3 - 110, 420, 220, 220, 'wall1', 6, .9),
          R(p3 - 110, 436, 220, 10, 'metal2', 3), R(p3 - 30, 430, 60, 40, 'orange', 6), poly([(p3 - 8, 470), (p3 + 8, 470), (p3, 484)], 'metal2'),
          R(p3 - 90, 620, 180, 14, 'metal2', 3)]
    for k in range(7):
        w_ = 70 - abs(k - 2) * 6; pr.append(R(p3 - w_ / 2, 620 - (k + 1) * 14, w_, 13, 'print', 3, .9 - k * .04))
    pr += [R(p3 + 70, 650, 40, 20, 'screen', 4), C(p3 + 80, 660, 4, 'lime'), C(p3 - 160, 560, 46, 'orange2'), C(p3 - 160, 560, 18, 'navy'), R(p3 - 136, 540, 8, 6, 'navy')]
    s.layer('printer', pr, 'pop', .55)
    # 笔记本电脑
    lx = 1050
    lp = [shadow(lx, 680, 170, 8), P(f'M{lx - 180},680 L{lx + 180},680 L{lx + 160},664 L{lx - 160},664Z', 'metal2'),
          R(lx - 150, 470, 300, 196, 'metal', 12, extra='filter="url(#shs)"'), R(lx - 136, 484, 272, 168, 'screen', 6)]
    random.seed(6)
    for k in range(8):
        ind = random.choice([0, 0, 20, 40]); w1 = random.randint(40, 120); w2 = random.randint(30, 80)
        lp += [R(lx - 120 + ind, 500 + k * 18, w1, 8, ['code1', 'code2', 'code3'][k % 3], 4), R(lx - 112 + ind + w1, 500 + k * 18, w2, 8, ['code2', 'code3', 'code1'][k % 3], 4, .8)]
    s.layer('laptop', lp, 'pop', .65)
    # 编程小车
    cx = 1350
    car = [shadow(cx, 680, 100, 7), R(cx - 90, 600, 180, 60, 'orange', 16), R(cx - 70, 572, 140, 36, 'navy2', 8), C(cx - 40, 590, 10, 'code1'), C(cx + 40, 590, 10, 'code1'),
           C(cx - 56, 664, 24, 'navy'), C(cx - 56, 664, 10, 'metal'), C(cx + 56, 664, 24, 'navy'), C(cx + 56, 664, 10, 'metal'), S(f'M{cx + 50},572 L{cx + 70},536', 'navy', 3), C(cx + 70, 532, 6, 'pink')]
    # 小机械臂
    ax = 1620
    car += [shadow(ax, 680, 70, 6), R(ax - 50, 650, 100, 30, 'navy', 8), C(ax, 640, 22, 'navy2'), S(f'M{ax},640 L{ax - 40},540 L{ax + 50},500', 'yellow', 22), C(ax - 40, 540, 14, 'navy2'),
            S(f'M{ax + 50},500 l20,-20 M{ax + 50},500 l26,6', 'metal2', 8)]
    s.layer('robots', car, 'pop', .8)
    # 无人机（悬停）
    dx, dy = 1280, 160
    dr = [S(f'M{dx - 110},{dy} L{dx + 110},{dy}', 'navy', 10), R(dx - 46, dy - 20, 92, 40, 'navy2', 14), C(dx, dy, 10, 'lime')]
    for x in (dx - 110, dx + 110): dr += [R(x - 5, dy - 20, 10, 20, 'navy'), E(x, dy - 22, 60, 7, 'metal', .7)]
    dr += [S(f'M{dx - 30},{dy + 20} L{dx - 40},{dy + 40} M{dx + 30},{dy + 20} L{dx + 40},{dy + 40}', 'navy', 5)]
    s.layer('drone', dr, 'drop', 1.0, loop='bob')
    # 地面纸箱/工具箱
    s.layer('toolbox', [shadow(1720, 980, 110, 10), R(1620, 910, 200, 70, 'pink', 10), R(1620, 900, 200, 22, 'navy2', 8), S('M1690,904 L1690,886 Q1690,878 1700,878 L1740,878 Q1750,878 1750,886 L1750,904', 'navy', 8),
                        shadow(200, 980, 90, 10), R(120, 900, 160, 80, 'cork', 6), R(120, 900, 160, 18, 'cork2', 4), S('M200,900 L200,980', 'cork2', 4)], 'rise', .9)
    return s


# ============ s058 稻田插秧 ============
def ricefield():
    s = Scene('s058', '稻田插秧', '艺术与劳动', ['劳动', '农业', '二十四节气', '粮食'],
              dict(sky1='#A8DDF5', sky2='#F3FAEE', sun='#FFE08A', m1='#B9DCCB', m2='#96C9AE', m3='#77B592', terr1='#BFE2A2', terr2='#A3D486', terr3='#8CC56E',
                   water='#BFE5EE', water2='#A3D6E4', water3='#D9F1F4', seed='#5DB25A', seed2='#9AD86E', ridge='#9BC774', ridge2='#7FAE5A', mud='#B08A62',
                   hat='#E9C87C', hat2='#C9A458', basket='#C99A5E', basket2='#A67A44', bird='#FFFFFF', beak='#F2B33D', willow='#7DBF6A', willow2='#A9D98A', trunk='#8A6A4A', swallow='#2F3B4E'),
              desc='春天的水田插秧：远山与梯田，水面倒映天空，左半边已插好整齐的秧苗行，右半边还是水面，田埂上放着秧把、斗笠和竹篮，白鹭与燕子。',
              stand={'ground_y': 900, 'x': [540, 1380]})
    s.layer('sky', [R(0, 0, W, 640, s.lg([(0, 'sky1'), (1, 'sky2')])), C(1500, 170, 150, 'sun', .4, 'filter="url(#b40)"'), C(1500, 170, 60, 'sun')], 'fade', 0)
    s.layer('clouds', [cloud(420, 150, .8, op=.9), cloud(1100, 100, .55, op=.85), cloud(1780, 210, .6, op=.85)], 'slide-l', .2, loop='drift')
    s.layer('mountains', [P('M0,520 Q200,380 420,470 Q620,330 860,460 Q1060,360 1260,450 Q1500,320 1720,440 Q1840,400 1920,430 L1920,640 L0,640Z', 'm1'),
                          P('M0,580 Q300,470 600,560 Q900,480 1200,560 Q1500,470 1920,560 L1920,640 L0,640Z', 'm2')], 'rise', .2)
    # 梯田（远处山坡上一层层弧带）
    tr = []
    for k in range(5):
        y = 560 + k * 18
        tr.append(P(f'M0,{y} Q480,{y - 30 + k * 4} 960,{y} Q1440,{y + 30 - k * 4} 1920,{y} L1920,{y + 18} Q1440,{y + 48 - k * 4} 960,{y + 18} Q480,{y - 12 + k * 4} 0,{y + 18}Z', ['terr1', 'terr2', 'terr3'][k % 3]))
        tr.append(S(f'M0,{y} Q480,{y - 30 + k * 4} 960,{y} Q1440,{y + 30 - k * 4} 1920,{y}', 'water3', 3, .8))
    s.layer('terraces', tr, 'rise', .3)
    # 柳树（左右）
    wl = []
    for x, sc, flip in [(120, 1.0, 1), (1820, .9, -1)]:
        wl += [R(x - 14 * sc, 380, 28 * sc, 300, 'trunk', 8), E(x, 360, 160 * sc, 110 * sc, 'willow'), E(x + 40 * flip, 330, 100 * sc, 70 * sc, 'willow2', .6)]
        for k in range(9):
            xx = x - 140 * sc + k * 35 * sc; wl.append(S(f'M{xx},{380} q{10 * flip},{120} {-6 * flip},{240 - abs(k - 4) * 20}', 'willow', 5, .9))
    s.layer('willows', wl, 'grow', .4, loop='sway')
    # 水田
    wf = [R(0, 640, W, 440, s.lg([(0, 'water3'), (.5, 'water'), (1, 'water2')])),
          E(1500, 760, 120, 18, 'sun', .45, 'filter="url(#b6)"'), cloud(560, 740, .5, '#ffffff', .35)]
    # 远近两块田的田埂（水平）
    wf += [R(0, 700, W, 14, 'ridge', 6, .9), R(0, 712, W, 4, 'ridge2', 0, .6)]
    s.layer('paddy', wf, 'fade', .1)
    s.layer('ripples', [S(f'M{x},{y} q30,-8 60,0 t60,0', '#ffffff', 3, .7) for x, y in [(1100, 780), (1350, 820), (1600, 760), (1250, 900), (1520, 870), (1700, 940)]], 'fade', .9, loop='flow')
    # 秧苗行（左半，近大远小）
    sd = []
    for row, (y, sc) in enumerate([(690, .45), (750, .6), (800, .75), (860, .9), (940, 1.1), (1040, 1.35)]):
        n = int(980 / (70 * sc))
        for k in range(n):
            x = 20 + k * 70 * sc + (row % 2) * 20 * sc
            if x > 980 - row * 30: break
            sd += [E(x, y + 2, 16 * sc, 4 * sc, 'water2', .9),
                   S(f'M{x},{y} q{-6 * sc},{-18 * sc} {-16 * sc},{-34 * sc} M{x},{y} q{1 * sc},{-22 * sc} {2 * sc},{-42 * sc} M{x},{y} q{6 * sc},{-18 * sc} {16 * sc},{-32 * sc}', 'seed', 4 * sc),
                   S(f'M{x},{y - 4 * sc} q{-3 * sc},{-10 * sc} {-8 * sc},{-22 * sc}', 'seed2', 3 * sc)]
    s.layer('seedlings', sd, 'grow', .5, loop='sway')
    # 近景田埂（角色站位）
    rg = [P('M0,880 Q480,860 960,876 Q1440,892 1920,872 L1920,940 Q1440,960 960,944 Q480,930 0,948Z', 'ridge'), P('M0,930 Q480,914 960,926 Q1440,940 1920,922 L1920,948 Q1440,966 960,952 Q480,940 0,956Z', 'mud', .8)]
    random.seed(4)
    for _ in range(40):
        x = random.uniform(0, W); rg.append(S(f'M{x:.0f},880 l-4,-12 m4,12 l5,-14', 'ridge2', 3))
    s.layer('ridge', rg, 'rise', .35)
    # 秧把、斗笠、竹篮
    it = []
    for x in (1460, 1520):
        it += [shadow(x, 884, 26, 5), R(x - 14, 864, 28, 18, 'mud', 6), S(f'M{x - 10},866 l-10,-40 M{x},866 l0,-46 M{x + 10},866 l10,-40 M{x - 4},866 l-4,-44 M{x + 4},866 l4,-44', 'seed', 5), R(x - 15, 852, 30, 6, 'hat2', 3)]
    it += [shadow(1660, 884, 70, 7), P('M1600,880 Q1660,830 1720,880Z', 'hat'), E(1660, 880, 80, 12, 'hat'), E(1660, 878, 60, 7, 'hat2', .6), C(1660, 838, 6, 'hat2')]
    it += [shadow(380, 884, 70, 7), P('M320,812 L440,812 L424,880 L336,880Z', 'basket'), *[R(326 + k * 4, 822 + k * 14, 108 - k * 8, 4, 'basket2', 2, .7) for k in range(4)], S('M330,812 Q380,760 430,812', 'basket2', 6),
           *[S(f'M{350 + k * 16},812 l{(k - 2) * 4},-26', 'seed', 4) for k in range(5)]]
    s.layer('tools', it, 'pop', .8)
    # 白鹭
    eg = []
    for x, y, sc, flip in [(1250, 780, 1, 1), (1650, 720, .7, -1)]:
        f = flip
        eg += [S(f'M{x},{y} L{x - 6 * f},{y + 60 * sc} M{x + 10 * f},{y} L{x + 14 * f},{y + 60 * sc}', 'swallow', 3 * sc), E(x + 4 * f, y - 20 * sc, 42 * sc, 22 * sc, 'bird'),
               S(f'M{x + 34 * f},{y - 26 * sc} q{14 * f},{-30 * sc} {4 * f},{-54 * sc}', 'bird', 9 * sc), C(x + 40 * f, y - 82 * sc, 11 * sc, 'bird'),
               poly([(x + 48 * f, y - 84 * sc), (x + 80 * f, y - 80 * sc), (x + 48 * f, y - 77 * sc)], 'beak'), C(x + 42 * f, y - 84 * sc, 2.5 * sc, 'swallow'),
               P(f'M{x - 34 * f},{y - 20 * sc} L{x - 60 * f},{y - 6 * sc} L{x - 30 * f},{y - 8 * sc}Z', 'bird'), E(x + 4 * f, y + 66 * sc, 28 * sc, 4 * sc, 'water2')]
    s.layer('egrets', eg, 'pop', 1.0, loop='bob')
    sw = [S(f'M{x},{y} q12,-12 24,-2 q10,-14 26,-4', 'swallow', 4) for x, y in [(700, 220), (780, 260), (860, 200)]]
    s.layer('swallows', sw, 'slide-r', 1.1, loop='drift')
    return s


# ============ s059 校园菜园 ============
def schoolgarden():
    s = Scene('s059', '校园菜园', '艺术与劳动', ['劳动', '种植', '科学', '自然观察'],
              dict(sky1='#9ED8F5', sky2='#F1FAF7', bld='#FBEBD2', bld2='#F2D7B3', roof='#E2715E', win='#BFE3F5', win2='#FFFFFF',
                   fence='#FFFFFF', fence2='#E1E6EA', grass1='#A6D68A', grass2='#86C46E', soil='#9C6B48', soil2='#7E5236', bed='#C9925A', bed2='#A8723F',
                   leaf='#5BAA5E', leaf2='#8ED07C', leaf3='#3F8C4E', tomato='#EF5A45', carrot='#F2973E', corn='#F7D048', eggplant='#7B4A9C', sun='#FFD36E', sunf='#F7C13E', sunf2='#7A4E2C',
                   can='#5FB7D6', can2='#3E97BB', barrow='#F2836B', barrow2='#D0644E', path='#EAD8B4', fly1='#F7A6C0', fly2='#FFD36E', stake='#C9A27A'),
              desc='阳光下的校园菜园：教学楼与白色栅栏前三块木框菜畦，番茄架、青菜、胡萝卜、茄子与玉米，向日葵、喷壶、小推车和翩翩蝴蝶。',
              stand={'ground_y': 910, 'x': [560, 1360]})
    s.layer('sky', [R(0, 0, W, 700, s.lg([(0, 'sky1'), (1, 'sky2')])), C(1700, 140, 140, 'sun', .3, 'filter="url(#b40)"'), C(1700, 140, 56, 'sun')], 'fade', 0)
    s.layer('clouds', [cloud(300, 140, .7, op=.9), cloud(1100, 90, .55, op=.85)], 'slide-l', .2, loop='drift')
    # 教学楼
    bl = [R(260, 260, 1400, 380, s.lg([(0, 'bld'), (1, 'bld2')]), 8, extra='filter="url(#shs)"'), R(240, 240, 1440, 30, 'roof', 8),
          R(860, 160, 200, 100, 'bld', 6), poly([(840, 166), (1080, 166), (960, 110)], 'roof'), C(960, 205, 30, '#ffffff'), C(960, 205, 24, 'win'), S('M960,205 L960,188 M960,205 L972,212', 'roof', 3)]
    for r_ in range(3):
        for k in range(10):
            x = 300 + k * 136
            if 860 < x + 40 < 1060 and r_ == 2: continue
            y = 300 + r_ * 110
            bl += [R(x, y, 90, 70, 'win', 6), R(x, y, 90, 14, 'win2', 4, .6), R(x + 43, y, 4, 70, 'win2', 0, .8)]
    bl += [R(900, 520, 120, 120, 'roof', 6), R(910, 530, 46, 110, 'win', 3), R(964, 530, 46, 110, 'win', 3)]
    s.layer('building', bl, 'rise', .2)
    s.layer('trees', [blob_tree(x, 660, .6, 'leaf', 'leaf2', 'stake') for x in (120, 1800)], 'grow', .35, loop='sway')
    gd = [R(0, 640, W, 440, s.lg([(0, 'grass1'), (1, 'grass2')])), P('M860,700 L1060,700 L1200,1080 L720,1080Z', 'path')]
    s.layer('ground', gd, 'rise', .1)
    fn = [R(0, 650, W, 10, 'fence'), R(0, 680, W, 10, 'fence')]
    for x in range(10, W, 44): fn += [P(f'M{x},710 L{x},640 L{x + 11},624 L{x + 22},640 L{x + 22},710Z', 'fence'), R(x + 18, 640, 4, 70, 'fence2', 0, .7)]
    s.layer('fence', fn, 'rise', .3)
    # 向日葵（栅栏前）
    sf = []
    for x, h in [(80, 300), (170, 360), (1760, 340), (1860, 290)]:
        y = 720 - h
        sf += [S(f'M{x},720 L{x},{y}', 'leaf3', 8), E(x - 24, y + 120, 28, 12, 'leaf', extra=f'transform="rotate(-30 {x - 24} {y + 120})"'), E(x + 24, y + 170, 28, 12, 'leaf2', extra=f'transform="rotate(30 {x + 24} {y + 170})"')]
        sf += [E(x + 32 * math.cos(a), y + 32 * math.sin(a), 20, 9, 'sunf', extra=f'transform="rotate({math.degrees(a):.0f} {x + 32 * math.cos(a):.0f} {y + 32 * math.sin(a):.0f})"') for a in [q * math.pi / 7 for q in range(14)]]
        sf += [C(x, y, 22, 'sunf2'), C(x - 5, y - 5, 8, '#9A6A3E')]
    s.layer('sunflowers', sf, 'grow', .5, loop='sway')

    def bed(x, y, w, h):
        return G([shadow(x + w / 2, y + h, w / 2 + 10, 10, .18), R(x, y, w, h, 'bed', 8, extra='filter="url(#shs)"'), R(x + 10, y - 6, w - 20, 22, 'soil', 8), R(x, y + h / 2, w, 4, 'bed2', 0, .7),
                  R(x - 6, y - 6, 16, h + 6, 'bed2', 4), R(x + w - 10, y - 6, 16, h + 6, 'bed2', 4)])
    # 左畦：番茄架 + 茄子
    b1 = [bed(260, 800, 400, 70)]
    for x in (320, 420):
        b1 += [S(f'M{x},806 L{x},560', 'stake', 6)]
        for k in range(6):
            y = 790 - k * 38; side = 1 if k % 2 else -1
            b1 += [S(f'M{x},{y} q{side * 22},-10 {side * 34},-26', 'leaf3', 4), E(x + side * 36, y - 28, 24, 10, 'leaf', extra=f'transform="rotate({side * -30} {x + side * 36} {y - 28})"')]
        for dx, dy in [(-24, 640), (20, 690), (-16, 740), (26, 600)]: b1 += [C(x + dx, dy, 15, 'tomato'), C(x + dx - 4, dy - 4, 4, '#ffffff', .5), P(f'M{x + dx - 7},{dy - 14} l7,5 l7,-5Z', 'leaf3')]
    for x in (520, 600):
        b1 += [leafy(x, 800, 1.1, 'leaf', 'leaf2', 6), E(x - 14, 770, 14, 30, 'eggplant', extra=f'transform="rotate(20 {x - 14} 770)"'), E(x + 16, 766, 12, 26, 'eggplant', extra=f'transform="rotate(-15 {x + 16} 766)"'),
               P(f'M{x - 24},{742} l10,-8 l10,8Z', 'leaf3')]
    s.layer('bed_left', b1, 'rise', .5)
    # 右畦：青菜 + 胡萝卜 + 玉米
    b2 = [bed(1260, 800, 420, 70)]
    for k in range(4):
        x = 1300 + k * 52
        b2 += [C(x, 790, 26, 'leaf2'), C(x - 10, 784, 16, 'leaf'), C(x + 10, 782, 14, 'leaf', .8)]
    for k in range(4):
        x = 1520 + k * 40
        b2 += [P(f'M{x - 10},800 L{x + 10},800 L{x},826Z', 'carrot'), S(f'M{x},796 l-10,-36 M{x},796 l0,-42 M{x},796 l10,-36', 'leaf', 5)]
    # 玉米（后排高）
    for x in (1300, 1380, 1460):
        b2 += [S(f'M{x},790 L{x},500', 'leaf3', 8), S(f'M{x},700 q40,-20 60,-70', 'leaf', 8), S(f'M{x},620 q-40,-20 -60,-70', 'leaf2', 8), S(f'M{x},560 q30,-20 40,-50', 'leaf', 6),
               E(x + 14, 640, 12, 34, 'corn', extra=f'transform="rotate(14 {x + 14} 640)"'), P(f'M{x + 8},{608} q10,-24 20,-28 q-4,14 -10,30Z', 'stake'), S(f'M{x},500 l-10,-24 M{x},500 l8,-26', 'stake', 4)]
    s.layer('bed_right', b2, 'rise', .6)
    # 近景：喷壶、小推车
    fg = [shadow(1500, 1000, 90, 10), R(1440, 920, 120, 80, 'can', 20), S('M1560,940 L1640,890', 'can2', 14), E(1644, 886, 14, 9, 'can2'), S('M1460,930 Q1500,870 1540,930', 'can2', 10),
          shadow(360, 1000, 140, 12), P('M240,900 L460,900 L430,970 L270,970Z', 'barrow'), R(232, 892, 236, 16, 'barrow2', 6), C(300, 990, 26, 'soil2'), C(300, 990, 10, 'fence2'),
          S('M460,904 L540,860', 'barrow2', 10), S('M290,970 L280,1000 M420,970 L430,1000', 'barrow2', 8), C(320, 886, 20, 'soil'), C(360, 880, 24, 'soil'), C(400, 886, 18, 'soil')]
    s.layer('foreground', fg, 'pop', .8)
    bf = []
    for x, y, col in [(720, 520, 'fly1'), (1180, 600, 'fly2'), (1560, 460, 'fly1')]:
        bf += [E(x - 12, y - 8, 14, 18, col, extra=f'transform="rotate(-30 {x - 12} {y - 8})"'), E(x + 12, y - 8, 14, 18, col, extra=f'transform="rotate(30 {x + 12} {y - 8})"'),
               E(x - 9, y + 10, 9, 11, col, .8), E(x + 9, y + 10, 9, 11, col, .8), R(x - 3, y - 14, 6, 30, 'sunf2', 3)]
    s.layer('butterflies', bf, 'fade', 1.0, loop='bob')
    return s


# ============ s060 编织手工台 ============
def weaving():
    s = Scene('s060', '编织手工台', '艺术与劳动', ['劳动', '手工', '编织', '传统工艺'],
              dict(wall1='#FBE6E2', wall2='#F2D0CA', stripe='#F6DAD4', wood='#D9A873', wood2='#B9824E', table='#E8BE8A', table2='#C99A62',
                   y1='#F28B82', y2='#F7C55E', y3='#7FC7B8', y4='#8FA8E6', y5='#C49BE0', y6='#9ED27C', y7='#F7A86A', cream='#FFF7EC',
                   red='#D8423A', red2='#B8312B', gold='#F2C14E', basket='#D2A266', basket2='#AE7E46', hoop='#C99A62', linen='#FFFBF2', leaf='#6DB57E', floor1='#D9B48C', floor2='#C29C72', lamp='#FFE3A3'),
              desc='温馨的编织手工角：墙上挂着木框织布机（彩色经纬条纹）、毛线格子柜与红色中国结，长桌上毛线团、正在编织的围巾、刺绣绷和藤编篮。',
              stand={'ground_y': 910, 'x': [560, 1360]})
    bg = [R(0, 0, W, 800, s.lg([(0, 'wall1'), (1, 'wall2')]))] + [R(x, 0, 40, 800, 'stripe', 0, .5) for x in range(0, W, 110)]
    s.layer('wall', bg, 'fade', 0)
    # 织布机（墙面中央记忆点）
    lx, ly, lw, lh = 700, 120, 520, 400
    lm = [R(lx - 30, ly - 20, lw + 60, 34, 'wood2', 10, extra='filter="url(#sh)"'), R(lx - 30, ly + lh - 14, lw + 60, 34, 'wood2', 10, extra='filter="url(#sh)"'),
          R(lx - 10, ly - 20, 26, lh + 40, 'wood', 6), R(lx + lw - 16, ly - 20, 26, lh + 40, 'wood', 6), R(lx + 16, ly + 14, lw - 32, lh - 28, 'cream')]
    bands = [('y1', 40), ('y2', 30), ('y3', 50), ('cream', 16), ('y4', 40), ('y5', 30), ('y7', 44), ('y6', 30)]
    y = ly + lh - 14
    for col, h in bands:
        y -= h
        lm.append(R(lx + 16, y, lw - 32, h, col))
        # 纹理：交错小块表现经纬
        for k in range(int((lw - 32) / 16)):
            for q in range(int(h / 10)):
                if (k + q) % 2 == 0: lm.append(R(lx + 16 + k * 16, y + q * 10, 16, 10, '#ffffff', 0, .12))
    top_y = y
    # 菱形图案（在 y3 带上）
    for k in range(6):
        cx_ = lx + 70 + k * 76; cy_ = ly + lh - 14 - 40 - 30 - 25
        lm.append(poly([(cx_, cy_ - 18), (cx_ + 18, cy_), (cx_, cy_ + 18), (cx_ - 18, cy_)], 'cream', .9))
    # 未织部分：经线
    for k in range(32): lm.append(R(lx + 26 + k * 15, ly + 14, 2.5, top_y - ly - 14, 'wood2', 0, .7))
    lm += [R(lx + 30, top_y - 36, lw - 60, 14, 'wood', 7), P(f'M{lx + lw - 40},{top_y - 52} L{lx + lw + 40},{top_y - 52} L{lx + lw + 60},{top_y - 30} L{lx + lw + 40},{top_y - 8} L{lx + lw - 40},{top_y - 8}Z', 'wood2')]
    for k in range(8): lm.append(R(lx + 4 + k * 66, ly + lh + 18, 10, 40 + (k % 3) * 12, bands[k % 8][0], 4))
    s.layer('loom', lm, 'drop', .3)
    # 毛线格子柜（右）
    cb = [R(1440, 160, 400, 420, 'wood', 14, extra='filter="url(#sh)"')]
    cols = ['y1', 'y2', 'y3', 'y4', 'y5', 'y6', 'y7', 'y1', 'y3']
    for r_ in range(3):
        for k in range(3):
            x = 1460 + k * 128; y = 180 + r_ * 132
            cb.append(R(x, y, 116, 118, 'wood2', 8, .55))
            col = cols[r_ * 3 + k]
            cb += [yarn(x + 38, y + 82, 32, col, 'wood2'), yarn(x + 82, y + 86, 28, cols[(r_ * 3 + k + 4) % 9], 'wood2'), yarn(x + 60, y + 44, 26, cols[(r_ * 3 + k + 2) % 9], 'wood2')]
    s.layer('yarn_cubbies', cb, 'slide-r', .45)
    # 中国结（左）
    kx, ky = 330, 170
    kt = [S(f'M{kx},0 L{kx},{ky - 40}', 'red2', 4), C(kx, ky - 46, 10, 'gold')]
    kt += [rot([R(kx - 70, ky - 70, 140, 140, 'red', 22)], 45, kx, ky + 30)]
    for k in range(-2, 3):
        kt.append(rot([R(kx - 70, ky + 30 + k * 26 - 4, 140, 8, 'red2', 4, .7), R(kx + k * 26 - 4, ky - 40, 8, 140, 'red2', 4, .7)], 45, kx, ky + 30))
    for a in (0, 90, 180, 270):
        ex_ = kx + 112 * math.cos(math.radians(a)); ey_ = ky + 30 + 112 * math.sin(math.radians(a))
        if a == 90: continue
        kt.append(C(ex_, ey_, 18, 'red'))
    kt += [R(kx - 14, ky + 130, 28, 30, 'gold', 8), *[R(kx - 20 + k * 6, ky + 160, 4, 120, 'red', 2) for k in range(7)], R(kx - 22, ky + 160, 44, 10, 'gold', 3)]
    s.layer('chinese_knot', kt, 'drop', .55, loop='sway', origin=f'{kx} 0')
    # 绒球串
    pm = [S('M0,60 Q300,110 600,60', 'wood2', 2.5), S('M1320,60 Q1620,110 1920,60', 'wood2', 2.5)]
    for k in range(7):
        for x0 in (0, 1320):
            u = (k + .5) / 7; x = x0 + 600 * u; y = 60 + 50 * 4 * u * (1 - u) * .5 * 2 * .5 + 8
            pm.append(C(x, y + 14, 16, cols[(k + x0 // 100) % 9]))
    s.layer('pompoms', pm, 'drop', .7, loop='sway')
    fl = [R(0, 800, W, 280, s.lg([(0, 'floor1'), (1, 'floor2')]))] + [S(f'M{x},800 L{x - 100},1080', 'floor2', 3, .4) for x in range(100, W + 100, 180)]
    s.layer('floor', fl, 'rise', .1)
    # 长桌
    tb = [shadow(960, 900, 700, 16, .2), R(220, 700, 1480, 36, s.lg([(0, 'table'), (1, 'table2')]), 10, extra='filter="url(#sh)"'), R(220, 700, 1480, 6, '#FBD9AC', 4),
          R(260, 736, 26, 160, 'table2', 4), R(1634, 736, 26, 160, 'table2', 4), R(260, 840, 1400, 12, 'table2', 4, .7)]
    s.layer('table', tb, 'rise', .3)
    # 桌上：藤编篮（毛线团）、编织中的围巾、刺绣绷、剪刀、针插
    it = []
    bx = 400
    it += [shadow(bx, 704, 120, 8), yarn(bx - 50, 620, 34, 'y4', 'wood2'), yarn(bx + 20, 610, 38, 'y1', 'wood2'), yarn(bx + 70, 630, 30, 'y6', 'wood2'),
           P(f'M{bx - 110},640 L{bx + 110},640 L{bx + 90},704 L{bx - 90},704Z', 'basket')]
    for k in range(4): it.append(R(bx - 104 + k * 5, 650 + k * 14, 208 - k * 10, 5, 'basket2', 2, .7))
    it.append(R(bx - 116, 634, 232, 14, 'basket2', 6))
    # 围巾 + 棒针
    sx = 760
    sc_ = [P(f'M{sx - 120},700 L{sx + 160},700 L{sx + 150},670 L{sx - 110},676Z', 'y3')]
    for k in range(10): sc_.append(S(f'M{sx - 100 + k * 26},696 l6,-10 l6,10', 'cream', 3, .7))
    sc_ += [R(sx - 140, 662, 320, 8, 'y2', 3, .0), S(f'M{sx + 120},680 L{sx + 260},600', 'wood2', 6), S(f'M{sx + 140},690 L{sx + 290},640', 'wood2', 6), C(sx + 262, 598, 7, 'y1'), C(sx + 292, 638, 7, 'y1'),
            yarn(sx + 330, 670, 30, 'y3', 'wood2'), S(f'M{sx + 300},676 Q{sx + 250},700 {sx + 150},676', 'y3', 3)]
    it += sc_
    # 刺绣绷
    hx_, hy_ = 1300, 650
    it += [shadow(hx_, 704, 80, 7), rot([E(hx_, hy_, 80, 52, 'hoop'), E(hx_, hy_, 70, 44, 'linen'), E(hx_ + 6, hy_ - 6, 10, 6, 'leaf', extra=f'transform="rotate(-30 {hx_ + 6} {hy_ - 6})"'),
                                       *[C(hx_ - 20 + 14 * math.cos(a), hy_ + 4 + 14 * math.sin(a), 9, 'y1') for a in [q * 1.2566 for q in range(5)]], C(hx_ - 20, hy_ + 4, 6, 'y2'),
                                       S(f'M{hx_ - 20},{hy_ + 16} q10,20 30,24', 'leaf', 3), R(hx_ + 74, hy_ - 8, 16, 16, 'wood2', 3)], -12, hx_, hy_)]
    # 剪刀 + 针插
    it += [rot([ring(1480, 690, 13, 13, 'y4', 6), ring(1510, 690, 13, 13, 'y4', 6),
                poly([(1490, 680), (1560, 650), (1566, 656), (1502, 686)], '#B8C2CC'), poly([(1500, 682), (1564, 668), (1564, 676), (1506, 690)], '#9AA6B2')], -6, 1510, 680),
           shadow(1610, 704, 40, 5), R(1580, 680, 60, 22, 'wood', 6), E(1610, 672, 34, 22, 'y1'), *[S(f'M{1600 + k * 10},{660 + (k % 2) * 6} l{-4 + k * 3},-22', '#9AA6B2', 2) for k in range(3)], *[C(1600 + k * 10 - 4 + k * 3, 638 + (k % 2) * 6, 4, ['y2', 'y3', 'y4'][k]) for k in range(3)]]
    s.layer('table_items', it, 'pop', .6)
    # 落地篮（近景）
    s.layer('floor_basket', [shadow(1780, 1000, 110, 12), yarn(1740, 880, 40, 'y5', 'wood2'), yarn(1810, 870, 44, 'y7', 'wood2'), P('M1660,900 L1900,900 L1870,1000 L1690,1000Z', 'basket'),
                             *[R(1666 + k * 6, 912 + k * 20, 228 - k * 12, 6, 'basket2', 3, .7) for k in range(4)], R(1652, 892, 256, 16, 'basket2', 6)], 'rise', .75)
    s.layer('lamp', [S('M960,0 L960,30', 'wood2', 3), P('M900,70 Q960,10 1020,70Z', 'y2'), C(960, 90, 220, 'lamp', .3, 'filter="url(#b40)"')], 'drop', .9, loop='glow')
    s.layer('plant', [potted(120, 800, .9, 'y3', 'wood2', 'leaf', 'y6')], 'grow', 1.0, loop='sway', origin='120 800')
    return s


SCENES = [artroom, pottery, choirstage, woodshop, cooking, makerspace, ricefield, schoolgarden, weaving]
