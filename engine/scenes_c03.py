from core import *
import math, random

# ---------- 本模块小工具 ----------

def fakechar(x, y, sz, seed, col, op=1):
    """抽象毛笔字（不可读，仅作书法装饰）：x,y 为字中心"""
    random.seed(seed)
    w = sz * .11; it = []
    h0 = sz / 2
    kinds = random.sample(['h', 'h2', 'v', 'pie', 'na', 'dot', 'dot2', 'hook'], random.randint(4, 6))
    for k in kinds:
        if k == 'h':
            yy = y - h0 * .55 + random.uniform(-4, 4) * sz / 60
            it.append(S(f'M{x - h0 * .7:.1f},{yy:.1f} q{h0 * .7:.1f},{-h0 * .1:.1f} {h0 * 1.4:.1f},{h0 * .03:.1f}', col, w, op))
        elif k == 'h2':
            yy = y + h0 * .15
            it.append(S(f'M{x - h0 * .8:.1f},{yy:.1f} q{h0 * .8:.1f},{-h0 * .12:.1f} {h0 * 1.6:.1f},0', col, w * 1.1, op))
        elif k == 'v':
            xx = x + random.uniform(-.15, .15) * sz
            it.append(S(f'M{xx:.1f},{y - h0 * .85:.1f} L{xx:.1f},{y + h0 * .8:.1f}', col, w * 1.05, op))
        elif k == 'pie':
            it.append(S(f'M{x - h0 * .05:.1f},{y - h0 * .2:.1f} q{-h0 * .2:.1f},{h0 * .6:.1f} {-h0 * .75:.1f},{h0 * .95:.1f}', col, w, op))
        elif k == 'na':
            it.append(S(f'M{x + h0 * .05:.1f},{y - h0 * .1:.1f} q{h0 * .3:.1f},{h0 * .6:.1f} {h0 * .8:.1f},{h0 * .85:.1f}', col, w, op))
        elif k == 'dot':
            it.append(E(x - h0 * .45, y - h0 * .2, w * .75, w * .5, col, op, f'transform="rotate(35 {x - h0 * .45:.1f} {y - h0 * .2:.1f})"'))
        elif k == 'dot2':
            it.append(E(x + h0 * .5, y - h0 * .7, w * .75, w * .5, col, op, f'transform="rotate(35 {x + h0 * .5:.1f} {y - h0 * .7:.1f})"'))
        else:
            it.append(S(f'M{x + h0 * .55:.1f},{y - h0 * .6:.1f} L{x + h0 * .55:.1f},{y + h0 * .55:.1f} l{-h0 * .2:.1f},{-h0 * .15:.1f}', col, w, op))
    return G(it)


def lantern(x, y, sc, body, gold, tassel=None):
    """红灯笼：x,y 为挂绳顶部"""
    tassel = tassel or gold
    return G([S(f'M{x},{y} L{x},{y + 30 * sc}', gold, 3 * sc), R(x - 20 * sc, y + 28 * sc, 40 * sc, 12 * sc, gold, 3 * sc),
              E(x, y + 80 * sc, 48 * sc, 44 * sc, body, extra='filter="url(#shs)"'),
              E(x, y + 80 * sc, 28 * sc, 44 * sc, '#ffffff', .12), E(x, y + 80 * sc, 10 * sc, 44 * sc, '#ffffff', .1),
              R(x - 20 * sc, y + 120 * sc, 40 * sc, 12 * sc, gold, 3 * sc), S(f'M{x},{y + 132 * sc} L{x},{y + 176 * sc}', tassel, 7 * sc),
              S(f'M{x - 5 * sc},{y + 140 * sc} L{x - 7 * sc},{y + 176 * sc} M{x + 5 * sc},{y + 140 * sc} L{x + 7 * sc},{y + 176 * sc}', tassel, 3 * sc)])


def eave_roof(x0, x1, y_top, y_eave, col, col2, edge, lift=26, th=26):
    """平面飞檐屋顶（正面）：屋面梯形+两端起翘"""
    w = x1 - x0; inset = w * .12
    d = (f'M{x0 + inset},{y_top} L{x1 - inset},{y_top} '
         f'Q{x1 - inset * .3},{y_eave - th * .2} {x1 + 10},{y_eave - lift} '
         f'L{x1 - 6},{y_eave + th * .4} L{x0 + 6},{y_eave + th * .4} L{x0 - 10},{y_eave - lift} '
         f'Q{x0 + inset * .3},{y_eave - th * .2} {x0 + inset},{y_top}Z')
    it = [P(d, col, extra='filter="url(#sh)"')]
    # 瓦垄
    n = int(w / 26)
    for k in range(1, n):
        xb = x0 + w * k / n; xt = x0 + inset + (w - 2 * inset) * k / n
        it.append(S(f'M{xt:.1f},{y_top + 4} L{xb:.1f},{y_eave + th * .2:.1f}', col2, 3, .45))
    it.append(P(f'M{x0 + 6},{y_eave + th * .1} L{x1 - 6},{y_eave + th * .1} L{x1 - 6},{y_eave + th * .4} L{x0 + 6},{y_eave + th * .4}Z', edge))
    it.append(R(x0 + inset - 12, y_top - 12, w - 2 * inset + 24, 16, col2, 6))
    return G(it)


# ============ s022 书法教室 ============
def calligraphy():
    s = Scene('s022', '书法教室', '语文与历史', ['语文', '书法', '传统文化', '美术'],
              dict(wall1='#F7F0E3', wall2='#ECDFC8', wood='#B98458', wood2='#8A5B3A', panel='#D9B48A', paper='#FCF8EE', silk='#E3CFA6', silk2='#C9AE80',
                   ink='#2C2A29', ink2='#6A6560', seal='#C9483B', sky1='#D9EEE6', sky2='#F6FBF4', hill='#BFD8CC', bamboo='#6FAE84', bamboo2='#A7D3A9',
                   felt='#3F5E55', plum='#E98A8F', floor1='#D7AE82', floor2='#BF915F', pot='#5F8FA0', handle='#C99B5E'),
              desc='雅致书法教室：月洞窗映竹影，两侧对联与山水、梅花挂轴，长案上摆笔架、砚台和铺开的宣纸。', stand={'ground_y': 900, 'x': [600, 1320]})
    s.layer('wall', [R(0, 0, W, 800, s.lg([(0, 'wall1'), (1, 'wall2')])), R(0, 610, W, 190, 'panel'),
                     *[R(x, 626, 3, 160, 'wood', 0, .35) for x in range(30, W, 60)], R(0, 600, W, 16, 'wood2'), R(0, 784, W, 16, 'wood2')], 'fade', 0)
    # 月洞窗
    cx, cy, r = 960, 330, 214
    cp = s.clip(f'<circle cx="{cx}" cy="{cy}" r="{r}"/>')
    inner = [R(cx - r, cy - r, 2 * r, 2 * r, s.lg([(0, 'sky1'), (1, 'sky2')])),
             P(f'M{cx - r},{cy + 120} Q{cx - 80},{cy + 20} {cx + 40},{cy + 90} Q{cx + 140},{cy + 40} {cx + r},{cy + 100} L{cx + r},{cy + r} L{cx - r},{cy + r}Z', 'hill', .8),
             C(cx + 90, cy - 90, 46, '#FFF4DC', .9)]
    s.layer('window_bg', [C(cx, cy, r + 26, 'wood2', extra='filter="url(#sh)"'), C(cx, cy, r + 12, 'wood'), G(inner, f'clip-path="{cp}"')], 'pop', .25)
    bam = []
    for bx, h, col in [(cx - 150, 520, 'bamboo'), (cx - 100, 470, 'bamboo2'), (cx + 120, 500, 'bamboo'), (cx + 170, 440, 'bamboo2')]:
        bam.append(R(bx - 7, cy + r - h, 14, h, col, 6))
        for j in range(1, 6): bam.append(R(bx - 9, cy + r - j * 90, 18, 5, 'wall1', 2, .5))
        for j in range(3):
            ly = cy + r - h + 40 + j * 70; sd = 1 if j % 2 else -1
            for q in range(3):
                a = sd * (25 + q * 18)
                bam.append(E(bx + sd * 34, ly + q * 10, 36, 9, col, extra=f'transform="rotate({a} {bx} {ly + q * 10})"'))
    s.layer('bamboo', [G(bam, f'clip-path="{cp}"')], 'fade', .5, loop='sway', origin=f'{cx} {cy + r}')
    s.layer('window_ring', [S(f'M{cx - r},{cy} a{r},{r} 0 1,0 {2 * r},0 a{r},{r} 0 1,0 {-2 * r},0', 'wood2', 6), R(cx - r - 40, cy + r + 18, 2 * r + 80, 16, 'wood2', 6)], 'fade', .3)
    # 匾额（无字，金色抽象书法）
    s.layer('plaque', [R(810, 36, 300, 64, 'wood2', 8, extra='filter="url(#shs)"'), R(820, 46, 280, 44, 'felt', 4), fakechar(890, 68, 34, 3, '#F2D28A'), fakechar(960, 68, 34, 8, '#F2D28A'), fakechar(1030, 68, 34, 12, '#F2D28A')], 'drop', .4)

    def scroll(x, y, w, h, inner_items):
        return G([R(x - w / 2 - 10, y - 10, w + 20, 14, 'wood2', 7), R(x - w / 2, y, w, h, 'silk', 2, extra='filter="url(#shs)"'),
                  R(x - w / 2 + 12, y + 30, w - 24, h - 60, 'paper'), *inner_items, R(x - w / 2 - 14, y + h - 4, w + 28, 16, 'wood2', 8),
                  C(x - w / 2 - 14, y + h + 4, 8, 'wood'), C(x + w / 2 + 14, y + h + 4, 8, 'wood'), S(f'M{x - 30},{y - 4} L{x},{y - 30} L{x + 30},{y - 4}', 'wood2', 2)])
    # 对联
    cps = []
    for x, sd in ((640, 1), (1280, 30)):
        chars = [fakechar(x, 210 + k * 76, 52, sd + k, 'ink') for k in range(5)]
        cps.append(scroll(x, 150, 84, 440, chars))
    s.layer('couplets', cps, 'drop', .55)
    # 山水挂轴（左）
    lx = 250
    land = [P(f'M{lx - 92},420 L{lx - 60},330 L{lx - 30},380 L{lx + 10},270 L{lx + 50},360 L{lx + 92},310 L{lx + 92},440 L{lx - 92},440Z', 'ink2', .45),
            P(f'M{lx - 92},470 L{lx - 40},400 L{lx},440 L{lx + 50},390 L{lx + 92},450 L{lx + 92},480 L{lx - 92},480Z', 'ink', .6),
            E(lx, 450, 90, 10, '#ffffff', .8), C(lx + 52, 236, 16, 'seal', .55), S(f'M{lx - 60},300 q8,-6 16,0 q8,-6 16,0', 'ink', 2)]
    land.append(R(lx + 60, 470, 16, 16, 'seal', 2))
    # 梅花挂轴（右）
    rx = 1670
    plum = [S(f'M{rx - 80},500 C{rx - 40},430 {rx - 50},360 {rx + 10},300 S{rx + 60},230 {rx + 70},200', 'ink', 9),
            S(f'M{rx - 30},380 C{rx + 10},380 {rx + 40},360 {rx + 70},340', 'ink', 5), S(f'M{rx},310 C{rx - 30},290 {rx - 50},260 {rx - 60},240', 'ink', 4)]
    for px, py in [(rx + 70, 200), (rx + 40, 245), (rx + 72, 338), (rx + 30, 360), (rx - 58, 240), (rx - 20, 280), (rx - 46, 420), (rx + 12, 300), (rx - 8, 395)]:
        plum += [C(px, py, 11, 'plum'), C(px, py, 4, '#FFE7A0')]
    plum.append(R(rx - 82, 210, 16, 16, 'seal', 2))
    s.layer('paintings', [scroll(lx, 150, 210, 380, land[:-1] + [R(lx + 54, 470, 16, 16, 'seal', 2)]), scroll(rx, 150, 210, 380, plum)], 'drop', .7)
    # 地板
    fl = [R(0, 800, W, 280, s.lg([(0, 'floor1'), (1, 'floor2')]))] + [S(f'M0,{y} L{W},{y}', 'floor2', 3, .45) for y in (850, 920, 1010)]
    fl += [S(f'M{x},{800 if k % 2 else 850} L{x},{850 if k % 2 else 920}', 'floor2', 3, .35) for k, x in enumerate(range(90, W, 240))]
    s.layer('floor', fl, 'rise', .1)
    s.layer('light', [beam(840, 1080, 600, 1320, 330, 1000, s, .18), E(960, 900, 380, 50, '#FFF6DE', .45, 'filter="url(#b40)"')], 'fade', .9, loop='glow')

    def desk(x0, x1):
        return G([E((x0 + x1) / 2, 900, (x1 - x0) / 2 + 30, 16, '#000000', .12), R(x0 + 30, 740, 24, 150, 'wood2', 4), R(x1 - 54, 740, 24, 150, 'wood2', 4),
                  R(x0 + 30, 840, x1 - x0 - 60, 12, 'wood2', 4), R(x0, 714, x1 - x0, 32, 'wood', 8, extra='filter="url(#shs)"'), R(x0, 740, x1 - x0, 8, 'wood2', 0, .5),
                  P(f'M{x0 - 12},{714} L{x0 + 10},{704} L{x0 + 10},{720}Z', 'wood'), P(f'M{x1 + 12},{714} L{x1 - 10},{704} L{x1 - 10},{720}Z', 'wood')])
    # 左长案：作品立架 + 砚台 + 笔架
    L = [desk(40, 540), R(60, 704, 300, 12, 'felt', 3),
         R(84, 520, 8, 190, 'wood2', 3), R(328, 520, 8, 190, 'wood2', 3), R(74, 512, 272, 12, 'wood2', 6),
         R(96, 530, 228, 170, 'paper', 3, extra='filter="url(#shs)"'), R(96, 530, 228, 8, 'silk', 0)]
    L += [fakechar(140 + k * 70, 590, 50, 40 + k, 'ink') for k in range(3)] + [fakechar(140 + k * 70, 652, 50, 60 + k, 'ink') for k in range(3)]
    L += [R(296, 676, 14, 14, 'seal', 2), R(352, 682, 80, 32, 'ink', 8), E(392, 690, 28, 7, '#4A4846'), E(384, 688, 12, 3, '#ffffff', .25)]
    bx0, bx1 = 440, 524
    rack = [R(bx0, 560, 8, 150, 'wood2', 3), R(bx1, 560, 8, 150, 'wood2', 3), P(f'M{bx0 - 14},562 Q{(bx0 + bx1) / 2},540 {bx1 + 22},562 L{bx1 + 22},572 L{bx0 - 14},572Z', 'wood2'), R(bx0 - 10, 704, 30, 10, 'wood2', 3), R(bx1 - 14, 704, 30, 10, 'wood2', 3)]
    brushes = []
    for k, sz in enumerate([1.0, .85, .72]):
        x = bx0 + 22 + k * 26
        brushes += [S(f'M{x},{570} L{x},{580}', 'wood2', 2), R(x - 5 * sz, 580, 10 * sz, 66 * sz, 'handle', 4), R(x - 6 * sz, 580 + 66 * sz, 12 * sz, 8, 'ink2', 2),
                    P(f'M{x - 7 * sz},{588 + 66 * sz} Q{x - 8 * sz},{612 + 66 * sz} {x},{626 + 70 * sz} Q{x + 8 * sz},{612 + 66 * sz} {x + 7 * sz},{588 + 66 * sz}Z', 'ink')]
    s.layer('desk_left', L, 'slide-l', .6)
    s.layer('brush_rack', [G(rack)], 'pop', .75)
    s.layer('brushes', brushes, 'drop', .9, loop='sway', origin='482 570')
    # 右长案：笔筒、镇纸、茶杯、兰花；地上画缸
    R_ = [desk(1380, 1880), R(1420, 704, 260, 10, 'paper', 2), R(1430, 694, 240, 10, 'ink', 4), C(1430, 699, 7, 'seal'), C(1670, 699, 7, 'seal')]
    R_ += [R(1710, 610, 70, 104, 'pot', 10, extra='filter="url(#shs)"'), R(1716, 640, 58, 6, '#ffffff', 2, .4), R(1716, 670, 58, 6, '#ffffff', 2, .4)]
    for k, a in enumerate([-14, -6, 2, 10, 18]):
        R_.append(G([R(1741 - 4, 520, 8, 100, 'handle', 3), P(f'M1734,520 Q1745,490 1748,470 Q1752,495 1748,520Z', 'ink')], f'transform="rotate({a} 1745 640)"'))
    R_ += [R(1560, 676, 60, 38, '#FFFFFF', 12), R(1556, 670, 68, 10, 'silk2', 4), E(1590, 671, 26, 5, 'felt', .5)]
    # 兰花
    R_ += [R(1460, 640, 70, 74, 'wall1', 14, extra='filter="url(#shs)"'), R(1460, 656, 70, 6, 'pot', 0, .7)]
    for a, ln in [(-60, 110), (-35, 140), (-10, 120), (20, 130), (50, 100)]:
        R_.append(S(f'M1495,640 q{ln * .3 * math.sin(math.radians(a)) * 2:.0f},{-ln * .6:.0f} {ln * math.sin(math.radians(a)):.0f},{-ln * math.cos(math.radians(a)):.0f}', 'bamboo', 5))
    R_ += [C(1470, 560, 9, 'plum'), C(1520, 548, 9, 'plum'), C(1500, 530, 7, '#F7C9CC')]
    s.layer('desk_right', R_, 'slide-r', .65)
    jar = [E(1850, 900, 70, 12, '#000000', .14), P('M1795,780 Q1790,900 1820,900 L1880,900 Q1910,900 1905,780Z', 'pot', extra='filter="url(#shs)"'), R(1790, 770, 120, 16, 'pot', 8)]
    for k, (x, h, col) in enumerate([(1815, 140, 'silk'), (1840, 170, 'paper'), (1865, 150, 'silk2'), (1888, 125, 'paper')]):
        jar += [R(x - 9, 780 - h + 60, 18, h, col, 9), C(x, 780 - h + 60, 9, 'wood2')]
    s.layer('scroll_jar', jar, 'rise', .85)
    s.layer('steam', [S(f'M{x},664 q-10,-16 0,-32 q10,-16 0,-32', '#ffffff', 4, .75) for x in (1580, 1600)], 'fade', 1.1, loop='flow')
    s.layer('seal', [R(1820, 40, 60, 60, 'seal', 6), fakechar(1850, 70, 34, 77, '#FBEDE0')], 'pop', 1.3)
    return s


# ============ s023 朗读角 ============
def readingcorner():
    s = Scene('s023', '朗读角', '语文与历史', ['语文', '阅读', '朗读', '图书'],
              dict(wall1='#EEE8F7', wall2='#DCD3EE', stripe='#E6DEF3', sky1='#9ED8F2', sky2='#E9F7FD', frame='#FFFFFF', shelf='#F3C58C', shelf2='#D9A060', tent='#F7D9C4', tent2='#F2B79C',
                   rug='#BFE3D2', rug2='#9ED1BC', floor1='#E8CDA8', floor2='#D2B086', b1='#F28B6E', b2='#5FB7B0', b3='#F7C55E', b4='#8E7CC3', b5='#7FB3E8', bag1='#F2A49A', bag2='#7CC4B2',
                   leaf='#6DB585', leaf2='#A8D99C', star='#FFE08A', lamp='#FFE7A8', cushion='#FFFFFF'),
              desc='温馨朗读角：拱形大窗、两侧书架、小帐篷和豆袋沙发，星星串灯闪烁，适合阅读与朗读主题。', stand={'ground_y': 910, 'x': [600, 1320]})
    bg = [R(0, 0, W, 800, s.lg([(0, 'wall1'), (1, 'wall2')]))] + [R(x, 0, 40, 800, 'stripe', 0, .6) for x in range(0, W, 110)]
    s.layer('wall', bg, 'fade', 0)
    # 拱窗
    x0, x1, yt, yb = 700, 1220, 120, 600
    rr = (x1 - x0) / 2
    arch = f'M{x0},{yb} L{x0},{yt + rr} A{rr},{rr} 0 0,1 {x1},{yt + rr} L{x1},{yb}Z'
    cp = s.clip(f'<path d="{arch}"/>')
    sky = [R(x0, yt, x1 - x0, yb - yt, s.lg([(0, 'sky1'), (1, 'sky2')])), cloud(840, 300, .55), cloud(1110, 380, .4, op=.9),
           C(760, 640, 150, 'leaf'), C(980, 680, 160, 'leaf2', .9), C(1200, 620, 140, 'leaf'), C(1080, 560, 70, 'leaf2', .6)]
    win = [P(f'M{x0 - 22},{yb + 10} L{x0 - 22},{yt + rr} A{rr + 22},{rr + 22} 0 0,1 {x1 + 22},{yt + rr} L{x1 + 22},{yb + 10}Z', 'frame', extra='filter="url(#shs)"'),
           G(sky, f'clip-path="{cp}"'), R(957, yt, 6, yb - yt, 'frame'), R(x0, 380, x1 - x0, 6, 'frame'),
           S(f'M{x0},{yt + rr} A{rr},{rr} 0 0,1 {x1},{yt + rr}', 'frame', 6), R(x0 - 50, yb, x1 - x0 + 100, 22, 'shelf', 8, extra='filter="url(#shs)"')]
    s.layer('window', win, 'pop', .25)
    # 窗台小物：书立、地球仪、小盆栽
    sill = [R(760, 540, 22, 60, 'b1', 3), R(784, 548, 18, 52, 'b3', 3), R(804, 536, 24, 64, 'b2', 3),
            C(1130, 548, 30, 'b5'), P('M1112,540 q14,-14 30,-4 q4,14 -10,22 q-14,0 -20,-18Z', 'leaf', .9), S('M1130,578 L1130,600', 'shelf2', 5), R(1110, 594, 40, 6, 'shelf2', 3),
            R(1030, 570, 36, 30, 'tent2', 6), *[E(1048 + 18 * math.cos(a), 562 + 14 * math.sin(a), 16, 6, 'leaf', extra=f'transform="rotate({math.degrees(a):.0f} {1048 + 18 * math.cos(a):.0f} {562 + 14 * math.sin(a):.0f})"') for a in (-2.6, -1.6, -.5)]]
    s.layer('sill', sill, 'pop', .5)
    # 星星串灯
    st = [S('M0,40 Q480,140 960,60 Q1440,140 1920,40', '#9C8FB8', 2.5)]
    for k in range(19):
        u = k / 18; t = (u * 2) % 1 if u < 1 else 1
        if u <= .5: y = (1 - t) ** 2 * 40 + 2 * t * (1 - t) * 140 + t ** 2 * 60
        else: y = (1 - t) ** 2 * 60 + 2 * t * (1 - t) * 140 + t ** 2 * 40
        if u == 1: y = 40
        x = u * W; r_ = 14
        pts = [(x + (r_ if j % 2 == 0 else r_ * .45) * math.cos(-math.pi / 2 + j * math.pi / 5), y + 22 + (r_ if j % 2 == 0 else r_ * .45) * math.sin(-math.pi / 2 + j * math.pi / 5)) for j in range(10)]
        st += [poly(pts, 'star'), C(x, y + 22, 26, 'star', .3, 'filter="url(#b20)"')]
    s.layer('stars', st, 'drop', 1.1, loop='twinkle')

    def bookshelf(x, y, w, h, rows, seed, arch_top=True):
        random.seed(seed)
        it = [R(x, y, w, h, 'shelf', 18, extra='filter="url(#sh)"')]
        if arch_top: it.append(P(f'M{x},{y + 40} Q{x + w / 2},{y - 50} {x + w},{y + 40}Z', 'shelf'))
        rh = (h - 40) / rows
        for r_ in range(rows):
            yy = y + 20 + r_ * rh
            it.append(R(x + 16, yy, w - 32, rh - 14, 'shelf2', 6))
            bx = x + 24
            while bx < x + w - 50:
                bw = random.randint(16, 30); bh = rh - 14 - random.randint(8, 30)
                if random.random() < .12:
                    it.append(G([R(bx, yy + rh - 14 - bh, bw, bh, random.choice(['b1', 'b2', 'b3', 'b4', 'b5']), 3)], f'transform="rotate(-14 {bx} {yy + rh - 14})"')); bx += bw + 14
                else:
                    col = random.choice(['b1', 'b2', 'b3', 'b4', 'b5'])
                    it += [R(bx, yy + rh - 14 - bh, bw, bh, col, 3), R(bx + 3, yy + rh - 14 - bh + 10, bw - 6, 4, '#ffffff', 1, .5)]
                    bx += bw + 3
            it.append(R(x + 10, yy + rh - 14, w - 20, 10, 'shelf', 3))
        return G(it)
    s.layer('shelf_left', [bookshelf(70, 230, 380, 580, 4, 2)], 'slide-l', .4)
    s.layer('shelf_right', [bookshelf(1500, 420, 360, 390, 3, 5, False), R(1530, 360, 120, 60, 'b4', 8), R(1540, 330, 100, 30, 'b2', 6), C(1780, 380, 40, 'b3'), C(1780, 380, 22, 'cushion', .7)], 'slide-r', .45)
    fl = [R(0, 800, W, 280, s.lg([(0, 'floor1'), (1, 'floor2')]))] + [S(f'M{x},800 L{x - 60},1080', 'floor2', 3, .35) for x in range(80, W + 100, 160)]
    s.layer('floor', fl, 'rise', .1)
    s.layer('rug', [E(960, 940, 560, 90, 'rug'), E(960, 940, 500, 74, 'rug2', .6), E(960, 940, 440, 60, 'rug'),
                    *[C(960 + 520 * math.cos(a), 940 + 84 * math.sin(a), 7, 'cushion', .8) for a in [k * math.pi / 14 for k in range(28)]]], 'grow', .5)
    # 小帐篷
    tx = 1230
    tent = [E(tx + 40, 905, 220, 18, '#000000', .12), poly([(tx - 150, 900), (tx + 40, 520), (tx + 230, 900)], 'tent'), poly([(tx + 40, 520), (tx + 230, 900), (tx + 110, 900)], 'tent2', .6),
            poly([(tx - 40, 900), (tx + 40, 700), (tx + 110, 900)], 'b4', .35), S(f'M{tx + 20},500 L{tx + 60},540 M{tx + 60},500 L{tx + 20},540', 'shelf2', 6),
            *[poly([(tx - 150 + k * 38 + 8, 900 - 24), (tx - 150 + k * 38 + 30, 900 - 24), (tx - 150 + k * 38 + 19, 900 - 4)], ['b1', 'b3', 'b2', 'b5'][k % 4]) for k in range(10)],
            R(tx - 10, 860, 90, 34, 'cushion', 14), R(tx + 10, 846, 50, 22, 'b3', 10)]
    s.layer('tent', tent, 'grow', .7, origin=f'{tx + 40} 900')
    # 豆袋
    bag = [E(470, 930, 170, 20, '#000000', .12), P('M330,920 Q300,780 420,760 Q520,740 580,800 Q630,860 600,925Z', 'bag1', extra='filter="url(#shs)"'), P('M360,830 Q440,800 540,840', 'none'),
           S('M380,830 Q450,800 540,840', '#ffffff', 5, .35), R(410, 850, 120, 26, 'b5', 6, extra='transform="rotate(-8 470 860)"'), R(420, 836, 100, 18, 'b3', 5, extra='transform="rotate(-8 470 860)"')]
    s.layer('beanbag', bag, 'pop', .8)
    # 落地灯 + 绿植
    lp = [R(613, 520, 8, 390, 'shelf2', 4), E(617, 908, 50, 10, 'shelf2'), P('M560,450 L674,450 L652,530 L582,530Z', 'lamp'), C(617, 520, 180, 'lamp', .3, 'filter="url(#b40)"')]
    s.layer('lamp', lp, 'grow', .6, loop='glow', origin='617 908')
    pl = [R(1840, 790, 70, 110, 'b2', 14, extra='filter="url(#shs)"')]
    for k, a in enumerate([-2.8, -2.3, -1.85, -1.4, -.95, -.5, -3.2]):
        ex, ey = 1875 + 70 * math.cos(a), 740 + 70 * math.sin(a)
        pl.append(E(ex, ey, 60, 20, 'leaf' if k % 2 else 'leaf2', extra=f'transform="rotate({math.degrees(a):.0f} {ex:.0f} {ey:.0f})"'))
    s.layer('plant', pl, 'grow', .9, loop='sway', origin='1875 900')
    # 飘浮的书
    fb = []
    for x, y, a, col in [(560, 300, -12, 'b1'), (1380, 260, 10, 'b2'), (1330, 520, -6, 'b3')]:
        fb.append(G([P(f'M{x},{y} Q{x - 30},{y - 14} {x - 60},{y - 4} L{x - 60},{y + 36} Q{x - 30},{y + 26} {x},{y + 40}Z', 'cushion'),
                     P(f'M{x},{y} Q{x + 30},{y - 14} {x + 60},{y - 4} L{x + 60},{y + 36} Q{x + 30},{y + 26} {x},{y + 40}Z', 'cushion'),
                     S(f'M{x - 60},{y + 36} Q{x - 30},{y + 26} {x},{y + 40} Q{x + 30},{y + 26} {x + 60},{y + 36}', col, 6),
                     S(f'M{x - 48},{y + 8} l34,4 M{x - 48},{y + 18} l34,4 M{x + 14},{y + 10} l34,-4', '#C9C3D8', 3)], f'transform="rotate({a} {x} {y})"'))
    s.layer('floating_books', fb, 'pop', 1.0, loop='bob')
    return s


# ============ s024 戏曲舞台 ============
def opera():
    s = Scene('s024', '戏曲舞台', '语文与历史', ['语文', '戏曲', '传统文化', '音乐'],
              dict(bg1='#5A2E3C', bg2='#3E2230', red='#C8443F', red2='#A3333A', gold='#E8B858', gold2='#C9913C', back='#B23A3C', back2='#962F35', cloud='#F0C36A',
                   roof='#3C4150', roof2='#545B6E', beam='#2F6E78', beam2='#4F9AA0', floor1='#B8743F', floor2='#95592E', carpet='#D2524A', carpet2='#B8403C',
                   wood='#8E4F2E', mask1='#FFFFFF', mask2='#D8433C', mask3='#2B2B33', blue='#3F7FB5', light='#FFE9B0'),
              desc='传统戏台：飞檐屋顶、红柱金饰，正中绣有祥云的守旧幕，两侧脸谱、灯笼与堂鼓，追光照亮舞台中央。', stand={'ground_y': 880, 'x': [560, 1360]})
    s.vignette = .2
    s.layer('bg', [R(0, 0, W, H, s.lg([(0, 'bg1'), (1, 'bg2')]))], 'fade', 0)
    # 守旧幕
    bk = [R(340, 230, 1240, 600, s.lg([(0, 'back'), (1, 'back2')]))]

    def xiangyun(x, y, sc, col, op=1):
        return G([S(f'M{x - 60 * sc},{y} a{20 * sc},{20 * sc} 0 1,1 {30 * sc},{-18 * sc} a{26 * sc},{26 * sc} 0 1,1 {48 * sc},{-4 * sc} a{18 * sc},{18 * sc} 0 1,1 {14 * sc},{30 * sc}', col, 6 * sc, op),
                  S(f'M{x - 64 * sc},{y + 8 * sc} L{x + 70 * sc},{y + 8 * sc}', col, 6 * sc, op),
                  S(f'M{x - 20 * sc},{y - 6 * sc} a{10 * sc},{10 * sc} 0 1,1 {12 * sc},{-10 * sc}', col, 5 * sc, op)])
    for (x, y, sc) in [(520, 360, 1.2), (760, 300, .8), (1180, 310, .9), (1420, 380, 1.1), (460, 620, .9), (1460, 640, .9), (700, 720, .7), (1240, 720, .7)]:
        bk.append(xiangyun(x, y, sc, 'cloud', .55))
    # 正中圆形团花
    bk += [C(960, 470, 150, 'gold', .9), C(960, 470, 136, 'back2'), C(960, 470, 120, 'gold', .25)]
    for k in range(8):
        a = k * math.pi / 4
        bk.append(E(960 + 70 * math.cos(a), 470 + 70 * math.sin(a), 42, 20, 'gold', .9, f'transform="rotate({math.degrees(a):.0f} {960 + 70 * math.cos(a):.0f} {470 + 70 * math.sin(a):.0f})"'))
    bk += [C(960, 470, 34, 'gold'), C(960, 470, 16, 'back2')]
    # 上下场门
    for x in (450, 1350):
        bk += [R(x, 560, 120, 270, 'back2'), P(f'M{x},{560} Q{x + 60},{500} {x + 120},{560}Z', 'back2'), S(f'M{x},{830} L{x},{560} Q{x + 60},{500} {x + 120},{560} L{x + 120},{830}', 'gold', 5),
               *[R(x + 10 + k * 22, 580, 12, 240, 'red', 4, .6) for k in range(5)]]
    s.layer('backdrop', bk, 'fade', .2)
    # 台口：红柱 + 额枋 + 屋顶
    fr = []
    for x in (300, 1580):
        fr += [R(x, 200, 40, 680, s.lg([(0, 'red2'), (.5, 'red'), (1, 'red2')], 0, 0, 1, 0)), R(x - 10, 856, 60, 24, 'gold2', 4), R(x - 6, 200, 52, 20, 'gold2', 4)]
    fr += [R(250, 170, 1420, 60, 'beam', extra='filter="url(#sh)"'), R(250, 180, 1420, 6, 'gold'), R(250, 214, 1420, 6, 'gold')]
    for k in range(14):
        x = 290 + k * 100; fr += [P(f'M{x},200 L{x + 30},186 L{x + 60},200 L{x + 30},214Z', 'beam2'), C(x + 30, 200, 9, 'gold'), C(x + 30, 200, 4, 'red2')]
    # 雀替
    for x, sd in ((340, 1), (1580, -1)):
        fr.append(P(f'M{x},230 L{x + sd * 150},230 Q{x + sd * 90},250 {x + sd * 60},290 Q{x + sd * 30},310 {x},330Z', 'gold2'))
        fr.append(P(f'M{x},236 L{x + sd * 130},236 Q{x + sd * 80},252 {x + sd * 54},286 Q{x + sd * 28},300 {x},316Z', 'red2'))
    fr.append(eave_roof(200, 1720, 40, 160, 'roof', 'roof2', 'gold2', lift=40, th=30))
    fr += [P('M190,128 Q150,110 140,80 Q170,100 210,110Z', 'roof'), P('M1730,128 Q1770,110 1780,80 Q1750,100 1710,110Z', 'roof'),
           R(560, 18, 800, 22, 'roof2', 10), P('M548,40 q-20,-34 4,-40 q-4,18 16,30Z', 'roof'), P('M1372,40 q20,-34 -4,-40 q4,18 -16,30Z', 'roof')]
    s.layer('frame', fr, 'drop', .35)
    # 幕布（两侧束起）
    cu = []
    for x0, sd in ((340, 1), (1580, -1)):
        for k in range(4):
            x = x0 + sd * (k * 34 + 18)
            cu.append(P(f'M{x - 20},230 L{x + 20},230 Q{x + 20 + sd * 30},520 {x + sd * 10 + 14},880 L{x + sd * 10 - 14},880 Q{x - 20 + sd * 10},520 {x - 20},230Z', 'red' if k % 2 else 'red2'))
        tx = x0 + sd * 70
        cu += [E(tx, 540, 82, 14, 'gold'), E(tx, 540, 82, 5, 'gold2', .6), C(tx + sd * 70, 548, 10, 'gold'), S(f'M{tx + sd * 70},556 L{tx + sd * 70},600', 'gold', 6)]
    cu.append(R(340, 230, 1240, 50, 'red2'))
    for k in range(26): cu.append(P(f'M{340 + k * 47.7},280 q24,30 47.7,0Z', 'red2'))
    cu.append(R(340, 228, 1240, 8, 'gold'))
    s.layer('curtains', cu, 'slide-l', .5)
    # 舞台台面
    st = [R(0, 880, W, 200, s.lg([(0, 'floor1'), (1, 'floor2')])), R(200, 880, 1520, 200, s.lg([(0, 'carpet'), (1, 'carpet2')])),
          R(0, 876, W, 10, 'gold2'), R(240, 900, 1440, 3, 'gold', 0, .6), R(240, 1050, 1440, 3, 'gold', 0, .6)]
    for x in range(0, W, 120): st.append(R(x, 960, 4, 120, 'floor2', 0, .5))
    s.layer('stage', st, 'rise', .1)
    s.layer('spot', [P('M880,0 L1040,0 L1340,880 L580,880Z', s.lg([(0, 'light', .0), (.3, 'light', .14), (1, 'light', .3)])), E(960, 890, 380, 40, 'light', .5, 'filter="url(#b20)"')], 'fade', .9, loop='glow')

    def mask(x, y, sc, base, mark):
        it = [P(f'M{x - 60 * sc},{y - 40 * sc} Q{x - 64 * sc},{y + 50 * sc} {x},{y + 86 * sc} Q{x + 64 * sc},{y + 50 * sc} {x + 60 * sc},{y - 40 * sc} Q{x},{y - 90 * sc} {x - 60 * sc},{y - 40 * sc}Z', base, extra='filter="url(#shs)"')]
        it += [P(f'M{x - 50 * sc},{y - 10 * sc} Q{x - 30 * sc},{y - 34 * sc} {x - 8 * sc},{y - 6 * sc} Q{x - 30 * sc},{y + 8 * sc} {x - 50 * sc},{y - 10 * sc}Z', mark),
               P(f'M{x + 50 * sc},{y - 10 * sc} Q{x + 30 * sc},{y - 34 * sc} {x + 8 * sc},{y - 6 * sc} Q{x + 30 * sc},{y + 8 * sc} {x + 50 * sc},{y - 10 * sc}Z', mark),
               C(x - 26 * sc, y - 10 * sc, 6 * sc, '#ffffff'), C(x + 26 * sc, y - 10 * sc, 6 * sc, '#ffffff'),
               P(f'M{x - 6 * sc},{y - 70 * sc} L{x + 6 * sc},{y - 70 * sc} L{x + 4 * sc},{y + 20 * sc} L{x - 4 * sc},{y + 20 * sc}Z', mark, .8),
               P(f'M{x - 26 * sc},{y + 44 * sc} Q{x},{y + 64 * sc} {x + 26 * sc},{y + 44 * sc} Q{x},{y + 54 * sc} {x - 26 * sc},{y + 44 * sc}Z', 'mask2'),
               S(f'M{x - 44 * sc},{y - 46 * sc} Q{x - 24 * sc},{y - 56 * sc} {x - 10 * sc},{y - 40 * sc} M{x + 44 * sc},{y - 46 * sc} Q{x + 24 * sc},{y - 56 * sc} {x + 10 * sc},{y - 40 * sc}', mark, 6 * sc)]
        return G(it)
    s.layer('masks', [mask(150, 420, 1.0, 'mask2', 'mask3'), mask(1770, 420, 1.0, 'mask1', 'mask3'), mask(150, 640, .8, 'mask1', 'blue'), mask(1770, 640, .8, 'gold', 'mask2')], 'pop', .7)
    # 一桌二椅（偏左）+ 堂鼓（右）
    tb = [E(420, 880, 150, 12, '#000000', .2), R(320, 760, 200, 20, 'wood', 4), R(310, 780, 220, 100, 'red', 4), R(310, 780, 220, 14, 'gold', 0), *[R(330 + k * 40, 800, 20, 70, 'gold', 4, .35) for k in range(5)]]
    for x in (250, 590):
        tb += [R(x - 30, 690, 60, 130, 'wood', 6), R(x - 40, 800, 80, 80, 'red2', 6), R(x - 40, 800, 80, 10, 'gold', 0)]
    s.layer('table_chairs', tb, 'rise', .75)
    dx = 1500
    dr = [E(dx, 882, 120, 12, '#000000', .2), S(f'M{dx - 60},880 L{dx - 30},770 M{dx + 60},880 L{dx + 30},770 M{dx},880 L{dx},770', 'wood', 8),
          E(dx, 760, 90, 30, 'red2'), R(dx - 90, 700, 180, 60, 'red', 8), E(dx, 700, 90, 26, '#F6E3C6'), *[C(dx - 80 + k * 20, 732, 4, 'gold') for k in range(9)],
          S(f'M{dx + 30},680 L{dx + 110},630', 'wood', 6), S(f'M{dx - 30},680 L{dx - 110},640', 'wood', 6)]
    s.layer('drum', dr, 'pop', .85)
    ln = [lantern(470, 230, .8, 'red', 'gold'), lantern(1450, 230, .8, 'red', 'gold'), lantern(80, 0, 1.0, 'red', 'gold'), lantern(1840, 0, 1.0, 'red', 'gold')]
    s.layer('lanterns', ln, 'drop', 1.0, loop='sway')
    s.layer('lantern_glow', [C(x, y, 70, 'gold', .3, 'filter="url(#b20)"') for x, y in ((470, 294), (1450, 294), (80, 80), (1840, 80))], 'fade', 1.1, loop='glow')
    return s


# ============ s025 竹林书院 ============
def academy():
    s = Scene('s025', '竹林书院', '语文与历史', ['语文', '历史', '传统文化', '古诗'],
              dict(sky1='#D7EFE6', sky2='#F7F5E8', hill='#C4DFD2', hill2='#A9CDBB', wallw='#F8F5EE', wallw2='#E6E1D6', tile='#4A5560', tile2='#6B7682', wood='#8A5A3E', wood2='#6B4330',
                   door='#7A4632', plaque='#2F3A44', gold='#E2B860', bam1='#CFE6D2', bam2='#9CCBA6', bam3='#5FA77A', bam4='#3E8A60', stone='#D9D4C7', stone2='#BDB6A6',
                   path='#E6DFCE', grass='#9ACB8A', grass2='#7FB873', lamp='#FFE1A0'),
              desc='青瓦白墙的书院掩映在层层竹林中，马头墙、匾额与石板路，竹叶随风飘落，适合古诗文与历史课。', stand={'ground_y': 900, 'x': [600, 1320]})
    s.layer('sky', [R(0, 0, W, H, s.lg([(0, 'sky1'), (1, 'sky2')])), C(1450, 200, 70, '#FFF6DA'), C(1450, 200, 150, '#FFF3D0', .5, 'filter="url(#b40)"')], 'fade', 0)
    s.layer('hills', [P('M0,560 Q300,380 620,520 Q900,420 1180,500 Q1500,360 1920,520 L1920,700 L0,700Z', 'hill', .9),
                      P('M0,620 Q400,500 760,600 Q1100,520 1400,590 Q1700,540 1920,600 L1920,720 L0,720Z', 'hill2', .7)], 'rise', .15)

    def bamboo(x, y0, h, w, col, leafcol, seed, leaves=True):
        random.seed(seed)
        it = [R(x - w / 2, y0 - h, w, h, col, w / 2)]
        for j in range(1, int(h / 110) + 1): it.append(R(x - w / 2 - 2, y0 - j * 110, w + 4, 4, '#ffffff', 2, .35))
        if leaves:
            for j in range(4):
                ly = y0 - h + 30 + j * random.uniform(60, 110); sd = random.choice((-1, 1))
                for q in range(3):
                    a = sd * (20 + q * 16)
                    it.append(E(x + sd * w * 2.4, ly + q * 8, w * 2.6, w * .65, leafcol, extra=f'transform="rotate({a} {x} {ly + q * 8:.0f})"'))
        return G(it)
    s.layer('bamboo_far', [bamboo(x, 760, random.Random(x).uniform(420, 620), 12, 'bam1', 'bam1', x) for x in range(20, W, 46)], 'rise', .25)
    s.layer('mist', [R(0, 560, W, 220, s.lg([(0, 'sky2', 0), (.6, 'sky2', .85), (1, 'sky2', .2)]))], 'fade', .35, loop='drift')
    # 书院建筑
    b = []
    # 两侧马头墙院墙
    for x0, x1, sd in ((330, 700, -1), (1220, 1590, 1)):
        b += [R(x0, 520, x1 - x0, 260, 'wallw', extra='filter="url(#shs)"'), R(x0, 740, x1 - x0, 40, 'wallw2')]
        # 阶梯状马头墙
        steps = [(x0, 470), (x0 + (x1 - x0) / 3, 430), (x0 + 2 * (x1 - x0) / 3, 470)] if sd < 0 else [(x0, 470), (x0 + (x1 - x0) / 3, 430), (x0 + 2 * (x1 - x0) / 3, 470)]
        widths = (x1 - x0) / 3
        for k, (xx, yy) in enumerate([(x0, 480), (x0 + widths, 440), (x0 + 2 * widths, 480)]):
            b += [R(xx, yy, widths + 1, 520 - yy + 4, 'wallw'), R(xx - 12, yy - 18, widths + 24, 22, 'tile', 4), P(f'M{xx - 18},{yy - 10} l14,-14 l2,14Z', 'tile'), P(f'M{xx + widths + 18},{yy - 10} l-14,-14 l-2,14Z', 'tile')]
        # 漏窗
        for wx in (x0 + 80, x1 - 140):
            b += [R(wx, 580, 60, 60, 'tile2', 6), *[R(wx + 8 + i * 12, 588, 4, 44, 'wallw', 0) for i in range(4)], *[R(wx + 8, 588 + i * 12, 44, 4, 'wallw') for i in range(4)]]
    # 主楼
    b += [R(640, 430, 640, 350, 'wallw', extra='filter="url(#sh)"'), R(640, 740, 640, 40, 'wallw2')]
    b.append(eave_roof(600, 1320, 300, 420, 'tile', 'tile2', 'tile2', lift=34, th=28))
    b += [R(700, 290, 520, 14, 'tile', 6), P('M690,300 q-24,-30 6,-40 q-2,18 14,30Z', 'tile'), P('M1230,300 q24,-30 -6,-40 q2,18 -14,30Z', 'tile')]
    # 檐下木构
    b += [R(660, 444, 600, 18, 'wood2'), *[R(680 + k * 100, 462, 20, 318, 'wood') for k in range(6)]]
    # 大门
    b += [R(850, 560, 220, 220, 'door', 6), R(850, 560, 220, 12, 'wood2'), R(958, 572, 4, 208, 'wood2'), C(940, 680, 8, 'gold'), C(980, 680, 8, 'gold'),
          *[C(870 + i * 30, 600 + j * 40, 4, 'gold', .8) for i in (0, 1, 2) for j in range(4)], *[C(990 + i * 30, 600 + j * 40, 4, 'gold', .8) for i in (0, 1, 2) for j in range(4)]]
    # 匾额
    b += [R(860, 480, 200, 60, 'plaque', 6, extra='filter="url(#shs)"'), R(868, 488, 184, 44, 'none'), S('M868,488 L1052,488 L1052,532 L868,532Z', 'gold', 3),
          fakechar(912, 510, 32, 21, 'gold'), fakechar(960, 510, 32, 25, 'gold'), fakechar(1008, 510, 32, 29, 'gold')]
    # 窗格（门两侧）
    for wx in (720, 1100):
        b += [R(wx, 580, 100, 140, 'wood', 6)] + [R(wx + 10 + i * 22, 590, 12, 120, 'wallw2', 3, .9) for i in range(4)] + [R(wx + 6, 640, 88, 6, 'wood')]
    # 台阶
    b += [R(820, 780, 280, 22, 'stone2', 4), R(800, 800, 320, 22, 'stone', 4)]
    s.layer('academy', b, 'rise', .45)
    s.layer('lanterns', [lantern(720, 470, .55, '#E86F55', 'gold'), lantern(1200, 470, .55, '#E86F55', 'gold')], 'drop', .9, loop='sway')
    s.layer('lantern_glow', [C(720, 515, 46, 'lamp', .5, 'filter="url(#b20)"'), C(1200, 515, 46, 'lamp', .5, 'filter="url(#b20)"')], 'fade', 1.0, loop='glow')
    gd = [R(0, 780, W, 300, s.lg([(0, 'grass'), (1, 'grass2')])), P('M800,820 L1120,820 L1360,1080 L560,1080Z', 'path')]
    for k, (y0, y1) in enumerate([(820, 860), (866, 912), (918, 974), (980, 1040)]):
        t0 = (y0 - 820) / 260; t1 = (y1 - 820) / 260
        xl0, xr0 = 800 - 240 * t0, 1120 + 240 * t0; xl1, xr1 = 800 - 240 * t1, 1120 + 240 * t1
        mid0 = (xl0 + xr0) / 2 + (20 if k % 2 else -20); mid1 = (xl1 + xr1) / 2 + (20 if k % 2 else -20)
        gd += [poly([(xl0 + 10, y0), (mid0 - 5, y0), (mid1 - 5, y1), (xl1 + 10, y1)], 'stone', .9), poly([(mid0 + 5, y0), (xr0 - 10, y0), (xr1 - 10, y1), (mid1 + 5, y1)], 'stone', .9)]
    s.layer('ground', gd, 'rise', .1)
    # 石灯笼 + 石头
    sl = []
    for x in (480, 1440):
        sl += [E(x, 900, 70, 10, '#000000', .12), R(x - 40, 880, 80, 20, 'stone2', 4), R(x - 14, 790, 28, 90, 'stone', 4), R(x - 40, 770, 80, 20, 'stone2', 4),
               R(x - 30, 720, 60, 50, 'stone', 6), R(x - 16, 732, 32, 26, 'lamp', 4), P(f'M{x - 56},{722} L{x},{680} L{x + 56},{722}Z', 'stone2'), C(x, 674, 8, 'stone2')]
    sl += [E(300, 880, 80, 30, 'stone2'), E(290, 870, 50, 16, 'stone', .8), E(1640, 900, 60, 22, 'stone2')]
    s.layer('stone_lamps', sl, 'pop', .7)
    s.layer('near_bamboo_l', [bamboo(40, 1080, 1100, 34, 'bam3', 'bam3', 2), bamboo(130, 1080, 1000, 26, 'bam4', 'bam4', 3), bamboo(210, 1080, 820, 20, 'bam3', 'bam3', 4)], 'slide-l', .6, loop='sway', origin='120 1080')
    s.layer('near_bamboo_r', [bamboo(1880, 1080, 1100, 34, 'bam3', 'bam3', 5), bamboo(1790, 1080, 980, 26, 'bam4', 'bam4', 6), bamboo(1710, 1080, 760, 20, 'bam3', 'bam3', 7)], 'slide-r', .65, loop='sway', origin='1800 1080')
    random.seed(13)
    lv = [E(random.uniform(250, 1700), random.uniform(120, 700), 16, 4, 'bam3', .8, f'transform="rotate({random.uniform(-40, 40):.0f} 0 0)"') for _ in range(0)]
    for _ in range(12):
        x, y, a = random.uniform(260, 1680), random.uniform(100, 720), random.uniform(-50, 50)
        lv.append(E(x, y, 18, 4.5, 'bam3', .85, f'transform="rotate({a:.0f} {x:.0f} {y:.0f})"'))
    s.layer('falling_leaves', lv, 'fade', 1.2, loop='drift')
    return s


# ============ s026 长城 ============
def greatwall():
    s = Scene('s026', '长城', '语文与历史', ['历史', '语文', '地理', '传统文化'],
              dict(sky1='#8FCBEB', sky2='#FBE6CF', sun='#FFD99A', m1='#C8D3E6', m2='#A9BCD6', m3='#8FB79A', m4='#6FA27F', m5='#5A8E6A',
                   wall='#D9B98E', wall2='#BF9A6C', wall3='#A67F55', brick='#C9A574', top='#E8CFA6', autumn1='#E9824F', autumn2='#F2B24C', autumn3='#D9604A',
                   pine='#3F7A5A', pine2='#5E9A72', trunk='#7A5238', walk1='#D7BE98', walk2='#C2A47A', flag='#D9483B'),
              desc='秋日群山之上，长城沿山脊蜿蜒，烽火台点缀峰顶；近景是城墙步道与垛口、敌楼，适合历史与语文课。', stand={'ground_y': 950, 'x': [520, 1300]})
    s.layer('sky', [R(0, 0, W, H, s.lg([(0, 'sky1'), (.75, 'sky2')])), C(1420, 230, 200, 'sun', .35, 'filter="url(#b40)"'), C(1420, 230, 70, 'sun')], 'fade', 0)
    s.layer('clouds', [cloud(300, 150, .8, op=.85), cloud(950, 110, .55, op=.75), cloud(1720, 170, .6, op=.8)], 'slide-l', .2, loop='drift')

    def ridge_fn(base, amp, ph, f1=1 / 230, f2=1 / 97):
        return lambda x: base - amp * (.55 + .45 * math.sin(x * f1 + ph)) * (.7 + .3 * math.sin(x * f2 + ph * 1.7))

    def mountain(fn, col, step=12):
        pts = [(x, fn(x)) for x in range(-20, W + 40, step)]
        return P('M-20,1080 ' + ' '.join(f'L{x},{y:.1f}' for x, y in pts) + f' L{W + 40},1080Z', col)
    f1 = ridge_fn(520, 260, .4, 1 / 260, 1 / 120)
    f2 = ridge_fn(600, 230, 2.2, 1 / 210, 1 / 90)
    f3 = ridge_fn(700, 150, 4.1, 1 / 180, 1 / 77)
    s.layer('far_mtn', [mountain(f1, 'm1'), R(0, 420, W, 200, s.lg([(0, 'sky2', 0), (1, 'sky2', .5)]))], 'rise', .2)

    def greatwall_on(fn, x0, x1, th, mh, col, col2, tops, step=None, towers=()):
        """沿山脊 fn 画城墙：th 墙体厚，mh 垛口高"""
        step = step or max(6, int(mh * 1.6))
        xs = list(range(int(x0), int(x1) + 1, 4))
        top = [(x, fn(x) - th * .4) for x in xs]
        bot = [(x, fn(x) + th * .7) for x in reversed(xs)]
        it = [poly(top + bot, col)]
        it.append(S('M' + ' L'.join(f'{x},{y:.1f}' for x, y in top), tops, max(2, th * .25)))
        for x in range(int(x0), int(x1), step):
            y = fn(x) - th * .4
            it.append(R(x, y - mh, step * .55, mh + 1, col2))
        for tx in towers:
            ty = fn(tx) - th * .4; tw = th * 3.2;thh = th * 3.4
            it += [R(tx - tw / 2, ty - thh, tw, thh + th, col2), R(tx - tw / 2 - 2, ty - thh - 2, tw + 4, th * .3, tops)]
            for k in range(4): it.append(R(tx - tw / 2 + k * tw / 3.5, ty - thh - mh, tw / 7, mh, col2))
            it.append(P(f'M{tx - tw * .14},{ty - thh * .2} L{tx - tw * .14},{ty - thh * .5} A{tw * .14},{tw * .14} 0 0,1 {tx + tw * .14},{ty - thh * .5} L{tx + tw * .14},{ty - thh * .2}Z', '#5A4634', .6))
        return G(it)
    s.layer('far_wall', [greatwall_on(f1, 0, W, 8, 5, 'm2', 'm2', 'm1', 9, towers=(300, 980, 1640))], 'fade', .35)
    s.layer('mid_mtn', [mountain(f2, 'm3')], 'rise', .35)
    s.layer('mid_wall', [greatwall_on(f2, -20, W + 20, 22, 12, 'wall2', 'wall3', 'top', 18, towers=(170, 620, 1110, 1550))], 'fade', .5)
    s.layer('mist', [E(600, 700, 700, 50, '#ffffff', .55, 'filter="url(#b40)"'), E(1500, 740, 600, 50, '#ffffff', .5, 'filter="url(#b40)"')], 'fade', .55, loop='drift')
    near_m = mountain(f3, 'm4')
    # 秋树点缀
    random.seed(17); trees = []
    for k in range(34):
        x = random.uniform(0, W); y = f3(x) + random.uniform(6, 40); r_ = random.uniform(12, 20)
        col = random.choice(['autumn1', 'autumn2', 'autumn3', 'm5', 'autumn1', 'autumn2'])
        trees += [R(x - 2, y - 4, 4, 18, 'trunk', 1), E(x, y - r_ * .6, r_ * .8, r_, col), E(x - r_ * .25, y - r_ * .9, r_ * .3, r_ * .4, '#ffffff', .18)]
    s.layer('near_mtn', [near_m, *trees], 'rise', .45)
    # 近景城墙：垛口墙 + 步道
    nw = [R(0, 790, W, 96, s.lg([(0, 'wall'), (1, 'wall2')]))]
    for y in range(800, 884, 26):
        off = 0 if (y // 26) % 2 else 40
        for x in range(-off, W, 80): nw.append(R(x + 2, y, 76, 22, 'brick', 3, .55))
    for x in range(-20, W, 150):
        nw += [R(x, 728, 100, 64, 'wall', 4), R(x, 722, 100, 12, 'top', 4), R(x + 40, 750, 20, 20, 'wall3', 3, .8)]
        nw += [R(x + 4, 740, 30, 16, 'brick', 2, .5), R(x + 66, 740, 30, 16, 'brick', 2, .5), R(x + 4, 766, 30, 16, 'brick', 2, .5), R(x + 66, 766, 30, 16, 'brick', 2, .5)]
        nw += [P(f'M{x + 104},790 q4,-16 8,0 q4,-12 8,0Z', 'm4', .9)]
    nw += [R(0, 786, W, 10, 'top'), R(0, 880, W, 8, 'wall3', 0, .5)]
    s.layer('parapet', nw, 'rise', .6)
    wk = [R(0, 886, W, 194, s.lg([(0, 'walk1'), (1, 'walk2')])), R(0, 886, W, 26, 'wall3', .18)]
    rows = [886, 924, 968, 1020, 1080]
    for k in range(4):
        y0, y1 = rows[k], rows[k + 1]; bw = 110 + k * 30
        wk.append(R(0, y1 - 2, W, 3, 'wall2', 0, .7))
        for x in range(-(k % 2) * bw // 2, W, bw): wk.append(R(x, y0, 3, y1 - y0, 'wall2', 0, .55))
    for x in range(-20, W, 150): wk.append(R(x - 10, 886, 120, 10, 'wall3', 3, .12))
    s.layer('walkway', wk, 'rise', .1)
    # 近景敌楼（右）
    tx0, tx1 = 1560, 1920
    tw = [R(tx0, 380, tx1 - tx0, 500, s.lg([(0, 'wall'), (1, 'wall2')]), extra='filter="url(#sh)"')]
    for y in range(400, 880, 30):
        off = 0 if (y // 30) % 2 else 36
        for x in range(tx0 - off, tx1, 72): tw.append(R(max(x + 2, tx0), y, min(68, tx1 - max(x + 2, tx0)), 26, 'brick', 3, .5))
    for x in range(tx0, tx1, 72):
        tw += [R(x + 6, 330, 46, 52, 'wall', 3), R(x + 6, 326, 46, 10, 'top', 3)]
    tw += [R(tx0 - 10, 376, tx1 - tx0 + 20, 14, 'top', 3)]
    for ax in (1640, 1780):
        tw.append(P(f'M{ax - 34},{620} L{ax - 34},{540} A34,34 0 0,1 {ax + 34},{540} L{ax + 34},{620}Z', 'wall3'))
        tw.append(P(f'M{ax - 26},{620} L{ax - 26},{544} A26,26 0 0,1 {ax + 26},{544} L{ax + 26},{620}Z', '#5E4632', .8))
    tw += [P(f'M{tx0 + 80},880 L{tx0 + 80},760 A70,70 0 0,1 {tx0 + 220},760 L{tx0 + 220},880Z', '#5E4632', .85), S(f'M{tx0 + 80},880 L{tx0 + 80},760 A70,70 0 0,1 {tx0 + 220},760 L{tx0 + 220},880', 'top', 8)]
    tw += [R(1880, 150, 8, 190, 'trunk', 3)]
    s.layer('tower', tw, 'slide-r', .7)
    s.layer('flag', [P('M1888,156 Q1840,170 1800,160 Q1830,190 1790,214 Q1840,220 1888,206Z', 'flag')], 'pop', 1.0, loop='sway', origin='1888 180')
    # 近景左：松树枝 + 秋叶
    pn = [S('M-20,560 C80,520 160,470 260,450', 'trunk', 18), S('M120,500 C160,450 200,420 240,380', 'trunk', 10)]
    for x, y, r_ in [(250, 440, 60), (200, 390, 48), (90, 500, 54), (320, 460, 40), (150, 450, 44)]:
        pn += [E(x, y, r_ * 1.5, r_ * .45, 'pine'), E(x + 8, y - 8, r_ * 1.0, r_ * .26, 'pine2', .9)]
    s.layer('pine', pn, 'slide-l', .8, loop='sway', origin='-20 560')
    s.layer('birds', [S(f'M{x},{y} q12,-10 22,0 q10,-10 22,0', '#4A5A6A', 3) for x, y in [(700, 260), (750, 290), (800, 250), (660, 300)]], 'slide-l', 1.1, loop='drift')
    return s


# ============ s027 故宫宫门 ============
def palacegate():
    s = Scene('s027', '故宫宫门', '语文与历史', ['历史', '语文', '传统文化', '建筑'],
              dict(sky1='#7EC3EA', sky2='#E3F3FB', red='#C4433A', red2='#A9362F', red3='#D9584B', yel='#F2BE45', yel2='#D99A2B', yel3='#FFE08A', green='#2F8A7E', blue='#2F6496',
                   marble='#F4F0E6', marble2='#DCD5C6', marble3='#C7BFAE', door='#B5382F', nail='#F2C14E', ground1='#E9E2D2', ground2='#D5CBB6', bronze='#7A6A4E', cloudw='#FFFFFF', lan='#E14B3B'),
              desc='正面平视的故宫宫门：金黄琉璃重檐屋顶、红墙城台与三个拱门（九路门钉），汉白玉栏杆，两侧华表，适合历史与传统文化。', stand={'ground_y': 930, 'x': [600, 1320]})
    s.layer('sky', [R(0, 0, W, 900, s.lg([(0, 'sky1'), (1, 'sky2')]))], 'fade', 0)
    s.layer('clouds', [cloud(260, 170, .9, op=.9), cloud(1700, 130, .7, op=.85), cloud(1100, 80, .45, op=.7)], 'slide-l', .15, loop='drift')
    # 远处两侧角楼影
    side = []
    for x, sd in ((90, 1), (1830, -1)):
        side += [R(x - 70, 470, 140, 160, 'red2', 0, .55), eave_roof(x - 100, x + 100, 400, 460, 'yel2', 'yel', 'yel2', lift=18, th=18)]
    # 城台
    ct = [R(200, 470, 1520, 420, s.lg([(0, 'red3'), (1, 'red')]), extra='filter="url(#sh)"'), R(200, 470, 1520, 18, 'marble'), R(200, 860, 1520, 30, 'marble2')]
    for y in range(500, 860, 40): ct.append(R(200, y, 1520, 2, 'red2', 0, .25))

    def archdoor(cx, w, top, bottom):
        rr = w / 2
        it = [P(f'M{cx - rr - 14},{bottom} L{cx - rr - 14},{top + rr} A{rr + 14},{rr + 14} 0 0,1 {cx + rr + 14},{top + rr} L{cx + rr + 14},{bottom}Z', 'marble2'),
              P(f'M{cx - rr},{bottom} L{cx - rr},{top + rr} A{rr},{rr} 0 0,1 {cx + rr},{top + rr} L{cx + rr},{bottom}Z', 'door')]
        # 九路门钉（每扇 9×9）
        for sd in (-1, 1):
            x0 = cx + (0 if sd > 0 else -rr) + rr * .1; x1 = x0 + rr * .8
            y0 = top + rr * .55; y1 = bottom - rr * .25
            for i in range(9):
                for j in range(9):
                    px = x0 + (x1 - x0) * (j + .5) / 9; py = y0 + (y1 - y0) * (i + .5) / 9
                    it.append(C(px, py, max(2.5, rr * .028), 'nail'))
            it.append(C(cx + sd * rr * .14, (y0 + y1) / 2, rr * .05, 'nail'))
        it += [R(cx - 2, top + rr * .2, 4, bottom - top - rr * .2, 'red2'), R(cx - rr, bottom - 10, 2 * rr, 10, 'red2', 0, .5)]
        return G(it)
    ct += [archdoor(960, 220, 600, 860), archdoor(560, 160, 670, 860), archdoor(1360, 160, 670, 860)]
    s.layer('platform', ct, 'rise', .3)
    # 汉白玉栏杆（城台顶）
    bal = [R(200, 440, 1520, 34, 'marble'), R(200, 466, 1520, 8, 'marble2')]
    for x in range(210, 1720, 54): bal += [R(x, 424, 14, 46, 'marble'), C(x + 7, 422, 9, 'marble')]
    for x in range(224, 1700, 54): bal.append(R(x + 6, 448, 30, 14, 'marble2', 6))
    s.layer('balustrade', bal, 'fade', .45)
    # 主殿
    hall = [R(420, 300, 1080, 145, 'red'), R(420, 300, 1080, 22, 'green'), R(420, 322, 1080, 14, 'blue')]
    for k in range(12):
        x = 420 + k * 90
        hall += [R(x, 336, 16, 109, 'red2'), R(x + 16, 344, 74, 92, 'red3', 2, .9)]
        hall += [R(x + 24, 350, 58, 80, 'yel', 2, .18)] + [R(x + 30 + q * 12, 354, 4, 72, 'yel2', 0, .5) for q in range(4)]
    for k in range(18): hall.append(R(420 + k * 60, 302, 30, 16, 'yel3', 3, .6))
    # 下檐
    hall.append(eave_roof(340, 1580, 250, 300, 'yel', 'yel2', 'yel2', lift=28, th=26))
    # 上层
    hall += [R(520, 170, 880, 80, 'red'), R(520, 170, 880, 16, 'green'), R(520, 186, 880, 10, 'blue')]
    for k in range(11): hall += [R(520 + k * 88, 196, 12, 54, 'red2')]
    # 上檐（庑殿）
    hall.append(eave_roof(400, 1520, 70, 175, 'yel', 'yel2', 'yel2', lift=34, th=30))
    hall += [R(560, 54, 800, 22, 'yel2', 8), P('M548,70 q-30,-36 6,-56 q-6,24 20,40Z', 'yel2'), P('M1372,70 q30,-36 -6,-56 q6,24 -20,40Z', 'yel2')]
    # 脊兽
    for k in range(5):
        hall += [C(388 + k * 10, 162 - k * 9, 6, 'yel2'), C(1532 - k * 10, 162 - k * 9, 6, 'yel2')]
    s.layer('hall', hall, 'drop', .5)
    s.layer('roof_glint', [P('M600,90 L1320,90 L1360,120 L560,120Z', '#ffffff', .18), P('M480,262 L1440,262 L1470,280 L450,280Z', '#ffffff', .15)], 'fade', 1.0, loop='glow')
    s.layer('lanterns', [lantern(x, 445, .6, 'lan', 'nail') for x in (700, 1220)], 'drop', .9, loop='sway')
    gd = [R(0, 880, W, 200, s.lg([(0, 'ground1'), (1, 'ground2')]))]
    for y in (920, 970, 1030): gd.append(R(0, y, W, 3, 'marble3', 0, .5))
    for k, x in enumerate(range(0, W, 160)): gd.append(R(x + (80 if k % 2 else 0), 880, 3, 200, 'marble3', 0, .35))
    gd.append(P('M820,880 L1100,880 L1180,1080 L740,1080Z', 'marble', .7))
    s.layer('ground', gd, 'rise', .1)

    def huabiao(x):
        return G([E(x, 935, 110, 14, '#000000', .14), R(x - 90, 880, 180, 50, 'marble2', 4), R(x - 76, 860, 152, 26, 'marble', 4),
                  *[R(x - 86 + k * 24, 836, 10, 30, 'marble', 3) for k in range(8)], R(x - 22, 330, 44, 540, s.lg([(0, 'marble2'), (.5, 'marble'), (1, 'marble2')], 0, 0, 1, 0)),
                  S(f'M{x - 20},800 C{x + 30},740 {x - 30},680 {x + 20},620 C{x + 40},580 {x - 30},520 {x + 10},460', 'marble3', 8, .8),
                  P(f'M{x - 110},400 Q{x - 60},370 {x - 20},390 L{x + 20},390 Q{x + 60},370 {x + 110},400 Q{x + 60},410 {x + 20},404 L{x - 20},404 Q{x - 60},410 {x - 110},400Z', 'marble', extra='filter="url(#shs)"'),
                  E(x, 330, 46, 12, 'marble2'), R(x - 34, 296, 68, 34, 'marble', 10), C(x, 286, 18, 'marble')])
    s.layer('huabiao', [huabiao(100), huabiao(1820)], 'rise', .7)

    def lion(x, sd):
        return G([E(x, 935, 90, 12, '#000000', .16), R(x - 80, 830, 160, 100, 'marble2', 6), R(x - 70, 820, 140, 20, 'marble', 4),
                  P(f'M{x - 50},820 L{x - 46},740 Q{x - 40},700 {x},690 Q{x + 40},700 {x + 46},740 L{x + 50},820Z', 'bronze'),
                  C(x, 660, 50, 'bronze'), *[C(x + 46 * math.cos(a), 660 + 46 * math.sin(a), 14, 'bronze') for a in [k * math.pi / 6 for k in range(12)]],
                  C(x - 16, 652, 6, 'yel3'), C(x + 16, 652, 6, 'yel3'), E(x, 676, 16, 8, '#5E5038'),
                  C(x + sd * 34, 790, 22, 'bronze'), C(x + sd * 34, 790, 10, '#5E5038', .6)])
    s.layer('lions', [lion(330, 1), lion(1590, -1)], 'pop', .85)
    s.layer('doves', [S(f'M{x},{y} q12,-10 22,0 q10,-10 22,0', '#5B6B7B', 3) for x, y in [(1040, 120), (1090, 150), (1140, 110)]], 'slide-r', 1.2, loop='drift')
    return s


# ============ s028 古代集市 ============
def ancientmarket():
    s = Scene('s028', '古代集市', '语文与历史', ['历史', '语文', '传统文化', '数学'],
              dict(sky1='#F7D8B0', sky2='#FCEFD9', far='#E4C9A8', wood='#A8693F', wood2='#7F4C2D', wood3='#C98B57', wallp='#F3E3C6', tile='#4E4A52', tile2='#6E6872',
                   red='#C9473B', red2='#E06A4E', gold='#E9B85A', cloth1='#5E9E95', cloth2='#E9A04B', cloth3='#9B6FB0', cloth4='#D9574B', jar='#B7774A', jar2='#8F5A36',
                   street1='#E2CFAE', street2='#CDB58E', umb='#E3584A', umb2='#F2C14E', paper='#FFF5E0', leaf='#7FB077'),
              desc='古风街市：两层木楼商铺、飞檐与酒旗、红灯笼，中央远处是牌坊，摊位上摆陶罐、布匹和油纸伞。', stand={'ground_y': 920, 'x': [560, 1360]})
    s.layer('sky', [R(0, 0, W, 900, s.lg([(0, 'sky1'), (1, 'sky2')])), C(960, 300, 260, '#FFF3D8', .6, 'filter="url(#b40)"')], 'fade', 0)
    # 远景：塔 + 城墙
    fz = [R(0, 600, W, 120, 'far', .8)]
    for x in range(0, W, 60): fz.append(R(x, 588, 36, 14, 'far', .8))
    px = 1500
    for k in range(6):
        w = 90 - k * 10; y = 600 - k * 52
        fz += [R(px - w * .55, y - 40, w * 1.1, 40, 'far'), P(f'M{px - w},{y - 34} L{px + w},{y - 34} L{px + w * .6},{y - 54} L{px - w * .6},{y - 54}Z', 'far')]
    fz += [R(px - 3, 260, 6, 30, 'far')]
    s.layer('far', [G(fz, 'opacity=".85"')], 'rise', .2)
    # 牌坊（中央远处）
    pf = []
    for x in (760, 880, 1040, 1160):
        pf += [R(x - 16, 470, 32, 300, 'wood2'), R(x - 26, 740, 52, 30, 'far', 1), R(x - 26, 736, 52, 8, 'wood', .6)]
    pf += [R(740, 500, 440, 26, 'red'), R(740, 506, 440, 6, 'gold', 0, .8), R(740, 570, 440, 18, 'red'),
           R(770, 528, 100, 40, 'cloth1', 2), R(1050, 528, 100, 40, 'cloth1', 2), R(890, 528, 140, 40, 'cloth1', 2),
           R(870, 436, 180, 64, 'gold', 4), R(878, 444, 164, 48, 'red2'), C(960, 468, 14, 'gold'), R(954, 462, 12, 12, 'red2'),
           *[R(746 + k * 22, 488, 14, 12, 'gold', 2, .7) for k in range(20)],
           eave_roof(840, 1080, 380, 432, 'tile', 'tile2', 'tile2', lift=20, th=16), eave_roof(720, 900, 446, 484, 'tile', 'tile2', 'tile2', lift=14, th=12),
           eave_roof(1020, 1200, 446, 484, 'tile', 'tile2', 'tile2', lift=14, th=12)]
    s.layer('paifang', [G(pf, 'opacity=".9"')], 'rise', .3)
    s.layer('haze', [R(0, 560, W, 260, s.lg([(0, 'sky2', 0), (.7, 'sky2', .6), (1, 'sky2', 0)]))], 'fade', .35)

    def shop(x0, w, flagcol, seed):
        random.seed(seed)
        it = [R(x0, 360, w, 440, 'wallp', extra='filter="url(#sh)"')]
        # 二层
        it += [R(x0, 360, w, 30, 'wood2'), R(x0 + 20, 400, w - 40, 140, 'wood3', 4)]
        for k in range(int((w - 40) / 40)): it.append(R(x0 + 28 + k * 40, 408, 30, 124, 'paper', 3, .85))
        for k in range(int((w - 40) / 40)): it += [R(x0 + 28 + k * 40, 440, 30, 3, 'wood', 0, .6), R(x0 + 28 + k * 40, 480, 30, 3, 'wood', 0, .6)]
        it += [R(x0 - 10, 540, w + 20, 18, 'wood2'), *[R(x0 + k * 30, 558, 14, 36, 'wood3', 2) for k in range(int(w / 30) + 1) if x0 + k * 30 + 14 <= x0 + w]]
        it.append(eave_roof(x0 - 40, x0 + w + 40, 270, 360, 'tile', 'tile2', 'tile2', lift=26, th=22))
        it.append(eave_roof(x0 - 30, x0 + w + 30, 590, 630, 'tile', 'tile2', 'tile2', lift=16, th=14))
        # 一层店面
        it += [R(x0 + 20, 640, w - 40, 160, 'wood2', 2), R(x0 + 40, 650, w - 80, 150, '#5C3A26', 2)]
        for k in range(int((w - 80) / 50)): it.append(R(x0 + 46 + k * 50, 656, 40, 144, 'wood', 2, .9))
        it += [R(x0, 360, 18, 440, 'wood2'), R(x0 + w - 18, 360, 18, 440, 'wood2')]
        return G(it)
    s.layer('shops_left', [shop(-20, 440, 'cloth1', 1)], 'slide-l', .45)
    s.layer('shops_right', [shop(1500, 440, 'cloth2', 2)], 'slide-r', .5)
    # 酒旗（三角旗+长幡）
    def coin(x, y, col):
        return G([C(x, y, 34, 'gold'), C(x, y, 26, col), C(x, y, 22, 'gold', .9), R(x - 9, y - 9, 18, 18, col)])
    fl = [S('M470,250 L470,640', 'wood2', 8), P('M474,270 L600,270 L600,520 L560,490 L520,520 L474,500Z', 'cloth1'), R(474, 270, 126, 18, 'gold'), R(474, 286, 126, 4, 'gold2' if False else 'gold', .5),
          coin(537, 390, 'cloth1'), S('M484,300 L484,490 M590,300 L590,500', 'gold', 3, .7),
          S('M1450,250 L1450,640', 'wood2', 8), P('M1446,270 L1320,270 L1320,520 L1360,490 L1400,520 L1446,500Z', 'red'), R(1320, 270, 126, 18, 'gold'),
          coin(1383, 390, 'red'), S('M1330,300 L1330,500 M1436,300 L1436,490', 'gold', 3, .7)]
    # 横跨街道的灯笼串
    ls = [S('M380,150 Q960,300 1540,150', 'wood2', 3)]
    for k in range(1, 12):
        u = k / 12; x = 380 + 1160 * u; y = (1 - u) ** 2 * 150 + 2 * u * (1 - u) * 300 + u ** 2 * 150
        ls.append(lantern(x, y, .36, 'red' if k % 2 else 'red2', 'gold'))
    s.layer('lantern_string', ls, 'drop', 1.0, loop='sway')
    s.layer('banners', fl, 'drop', .7, loop='sway', origin='470 260')
    # 灯笼串
    s.layer('lanterns', [lantern(x, 360, .5, 'red', 'gold') for x in (80, 220, 360, 1580, 1720, 1860)], 'drop', .85, loop='sway')
    s.layer('street', [R(0, 800, W, 280, s.lg([(0, 'street1'), (1, 'street2')])),
                       *[R(x + (40 if (y // 50) % 2 else 0), y, 76, 44, 'street2', 6, .5) for y in range(808, 1080, 50) for x in range(-40, W, 84)]], 'rise', .1)
    # 摊位：左陶罐摊，右布匹+伞
    def jar(x, y, sc, col):
        return G([P(f'M{x - 26 * sc},{y - 70 * sc} Q{x - 60 * sc},{y - 40 * sc} {x - 36 * sc},{y} L{x + 36 * sc},{y} Q{x + 60 * sc},{y - 40 * sc} {x + 26 * sc},{y - 70 * sc}Z', col, extra='filter="url(#shs)"'),
                  R(x - 22 * sc, y - 84 * sc, 44 * sc, 16 * sc, col, 4), R(x - 40 * sc, y - 46 * sc, 80 * sc, 6 * sc, 'paper', 2, .5)])
    lt = [E(330, 920, 220, 16, '#000000', .14), R(140, 780, 380, 26, 'wood', 6), R(160, 806, 18, 110, 'wood2'), R(482, 806, 18, 110, 'wood2'), R(160, 856, 340, 10, 'wood2'),
          jar(210, 780, 1.0, 'jar'), jar(300, 780, .8, 'jar2'), jar(380, 780, 1.1, 'jar'), jar(460, 780, .7, 'red2'),
          jar(90, 910, 1.2, 'jar2'), jar(560, 910, .9, 'jar')]
    s.layer('pottery_stall', lt, 'pop', .75)
    rt = [E(1600, 920, 230, 16, '#000000', .14), R(1410, 780, 380, 26, 'wood', 6), R(1430, 806, 18, 110, 'wood2'), R(1752, 806, 18, 110, 'wood2'),
          *[R(1430 + k * 66, 730, 56, 50, c_, 10, extra='filter="url(#shs)"') for k, c_ in enumerate(['cloth1', 'cloth2', 'cloth3', 'cloth4', 'cloth1'])],
          *[R(1440 + k * 66, 690, 50, 40, c_, 10) for k, c_ in enumerate(['cloth3', 'cloth4', 'cloth2', 'cloth1'])]]
    # 油纸伞
    ux, uy = 1640, 520
    umb = [S(f'M{ux},{uy} L{ux},{780}', 'wood2', 6)]
    for k in range(10):
        a0 = math.pi + k * math.pi / 10; a1 = a0 + math.pi / 10
        umb.append(P(f'M{ux},{uy} L{ux + 220 * math.cos(a0):.1f},{uy + 70 * math.sin(a0) + 70:.1f} L{ux + 220 * math.cos(a1):.1f},{uy + 70 * math.sin(a1) + 70:.1f}Z', 'umb' if k % 2 else 'umb2'))
    umb = [umb[0]] + [P(f'M{ux - 230},{uy + 70} Q{ux},{uy - 90} {ux + 230},{uy + 70}Z', 'umb')] + [S(f'M{ux},{uy - 10} L{ux + 230 * math.cos(math.pi + k * math.pi / 8):.0f},{uy + 70 + 80 * math.sin(math.pi + k * math.pi / 8):.0f}', 'umb2', 3, .7) for k in range(9)] + [C(ux, uy - 12, 10, 'gold')]
    s.layer('cloth_stall', rt + umb, 'pop', .8)
    # 箩筐、小板凳
    misc = [P('M620,900 L700,900 L690,850 L630,850Z', 'gold', extra='filter="url(#shs)"'), *[C(640 + k * 14, 846, 9, 'red2') for k in range(4)],
            P('M1240,900 L1320,900 L1312,850 L1248,850Z', 'gold'), *[C(1258 + k * 14, 846, 9, 'leaf') for k in range(4)]]
    s.layer('baskets', misc, 'pop', .95)
    s.layer('lantern_glow', [C(x, 400, 40, 'gold', .35, 'filter="url(#b20)"') for x in (80, 220, 360, 1580, 1720, 1860)], 'fade', 1.1, loop='glow')
    return s


# ============ s029 博物馆展厅 ============
def museum():
    s = Scene('s029', '博物馆展厅', '语文与历史', ['历史', '语文', '传统文化', '美术'],
              dict(wall1='#E9E3DA', wall2='#D8CFC2', panel='#3C4A57', panel2='#2E3A45', floor1='#C9BBA8', floor2='#A99A86', plinth='#F7F4EE', plinth2='#DCD5C9',
                   glass='#E6F4F7', bronze='#4F8A7A', bronze2='#3A6E62', bronze3='#7FB3A0', blue='#2E5C9E', porc='#F8F7F2', clay='#C9774A', clay2='#9E5634',
                   jade='#9FCFB4', gold='#E2B860', light='#FFF2D0', rope='#B8433C', scroll='#F3E8D0', ink='#5E6A6A', ink2='#8FA3A0'),
              desc='安静的博物馆展厅：中央墙上长卷山水，两侧玻璃展柜中陈列青铜鼎、青花瓷瓶、彩陶罐和玉璧，顶灯投下光束。', stand={'ground_y': 910, 'x': [600, 1320]})
    s.layer('wall', [R(0, 0, W, 800, s.lg([(0, 'wall1'), (1, 'wall2')])), R(0, 0, W, 70, 'panel2'), R(0, 70, W, 8, 'gold', 0, .7),
                     R(560, 120, 800, 420, 'panel', 6)], 'fade', 0)
    # 长卷山水
    sx0, sx1, sy = 600, 1320, 200
    sc = [R(sx0 - 16, sy - 10, sx1 - sx0 + 32, 240, 'gold', 4, .9), R(sx0, sy, sx1 - sx0, 220, 'scroll', extra='filter="url(#shs)"')]
    cp = s.clip(f'<rect x="{sx0}" y="{sy}" width="{sx1 - sx0}" height="220"/>')
    random.seed(4); m = []
    for layer_, (base, amp, col, op) in enumerate([(360, 110, 'ink2', .5), (400, 90, 'ink', .55)]):
        pts = [(x, base - amp * (.5 + .5 * math.sin(x / 70 + layer_ * 2)) * (.6 + .4 * math.sin(x / 31 + layer_))) for x in range(sx0 - 20, sx1 + 40, 20)]
        m.append(P(f'M{sx0 - 20},{sy + 220} ' + ' '.join(f'L{x},{y:.0f}' for x, y in pts) + f' L{sx1 + 40},{sy + 220}Z', col, op))
    m += [E(960, 400, 400, 16, '#ffffff', .7, 'filter="url(#b6)"'), P('M1100,404 Q1140,414 1190,404 L1180,412 Q1140,420 1110,412Z', 'ink'), S('M1146,404 L1146,380', 'ink', 2)]
    sc.append(G(m, f'clip-path="{cp}"'))
    sc += [R(sx0 - 30, sy - 14, 18, 248, 'panel2', 6), R(sx1 + 12, sy - 14, 18, 248, 'panel2', 6), R(1270, 380, 22, 22, '#C9483B', 2)]
    s.layer('scroll', sc, 'zoom', .3)
    # 说明牌
    s.layer('labels', [R(900, 470, 120, 40, 'plinth', 4, .9), R(912, 482, 70, 5, 'panel', 2, .6), R(912, 494, 90, 5, 'panel', 2, .4)], 'fade', .6)
    fl = [R(0, 800, W, 280, s.lg([(0, 'floor1'), (1, 'floor2')]))] + [R(x, 800, 3, 280, 'floor2', 0, .45) for x in range(0, W, 200)] + [R(0, y, W, 3, 'floor2', 0, .4) for y in (860, 940, 1030)]
    fl += [E(330, 880, 160, 20, '#ffffff', .25, 'filter="url(#b6)"'), E(1590, 880, 160, 20, '#ffffff', .25, 'filter="url(#b6)"')]
    s.layer('floor', fl, 'rise', .1)
    # 轨道射灯 + 光束
    lt = [R(0, 86, W, 10, 'panel2')]
    for x in (330, 760, 1160, 1590):
        lt += [R(x - 10, 92, 20, 24, 'panel2', 4), R(x - 20, 112, 40, 36, 'panel', 8, extra=f'transform="rotate(0 {x} 120)"'), E(x, 148, 16, 5, 'light')]
    s.layer('track_lights', lt, 'drop', .4)
    s.layer('beams', [beam(310, 350, 170, 490, 150, 860, s, .28), beam(1570, 1610, 1430, 1750, 150, 860, s, .28), beam(745, 775, 680, 860, 150, 560, s, .12), beam(1145, 1175, 1060, 1240, 150, 560, s, .12)], 'fade', .8, loop='glow')

    def case(x, w, h, plinth_h=260):
        base_y = 880
        return G([E(x, base_y + 6, w * .6, 12, '#000000', .14), R(x - w / 2, base_y - plinth_h, w, plinth_h, s.lg([(0, 'plinth'), (1, 'plinth2')]), 4, extra='filter="url(#sh)"'),
                  R(x - w / 2 - 6, base_y - plinth_h - 10, w + 12, 14, 'plinth2', 3),
                  R(x - w / 2 + 6, base_y - plinth_h - 10 - h, w - 12, h, 'glass', 6, .35), S(f'M{x - w / 2 + 6},{base_y - plinth_h - 10} L{x - w / 2 + 6},{base_y - plinth_h - 10 - h} L{x + w / 2 - 6},{base_y - plinth_h - 10 - h} L{x + w / 2 - 6},{base_y - plinth_h - 10}', '#ffffff', 4, .9),
                  P(f'M{x - w / 2 + 30},{base_y - plinth_h - 20 - h * .1} L{x - w / 2 + 70},{base_y - plinth_h - 10 - h * .95} L{x - w / 2 + 90},{base_y - plinth_h - 10 - h * .95} L{x - w / 2 + 50},{base_y - plinth_h - 20 - h * .1}Z', '#ffffff', .35),
                  R(x - 40, base_y - plinth_h + 40, 80, 30, 'panel', 3, .8), R(x - 28, base_y - plinth_h + 50, 40, 4, 'plinth', 2, .8)])
    # 青铜鼎（左）
    dx, dy = 330, 610
    ding = [case(dx, 300, 300),
            S(f'M{dx - 70},{dy - 150} L{dx - 70},{dy - 190} L{dx - 40},{dy - 190} L{dx - 40},{dy - 150}', 'bronze2', 12, 1, 'butt'),
            S(f'M{dx + 70},{dy - 150} L{dx + 70},{dy - 190} L{dx + 40},{dy - 190} L{dx + 40},{dy - 150}', 'bronze2', 12, 1, 'butt'),
            P(f'M{dx - 100},{dy - 150} L{dx + 100},{dy - 150} Q{dx + 104},{dy - 40} {dx},{dy - 40} Q{dx - 104},{dy - 40} {dx - 100},{dy - 150}Z', 'bronze'),
            R(dx - 108, dy - 160, 216, 16, 'bronze2', 4), R(dx - 96, dy - 132, 192, 26, 'bronze2', 2, .7)]
    for k in range(6): ding.append(S(f'M{dx - 86 + k * 32},{dy - 112} q8,-12 16,0 q8,12 16,0', 'bronze3', 3, .9))
    ding += [P(f'M{dx - 70},{dy - 56} L{dx - 80},{dy} L{dx - 62},{dy} L{dx - 52},{dy - 50}Z', 'bronze2'), P(f'M{dx + 70},{dy - 56} L{dx + 80},{dy} L{dx + 62},{dy} L{dx + 52},{dy - 50}Z', 'bronze2'),
             P(f'M{dx - 8},{dy - 44} L{dx - 8},{dy} L{dx + 8},{dy} L{dx + 8},{dy - 44}Z', 'bronze2'), E(dx - 40, dy - 120, 30, 8, '#ffffff', .2)]
    s.layer('ding', ding, 'rise', .5)
    # 青花瓷瓶（右）
    vx, vy = 1590, 610
    vase = [case(vx, 260, 330),
            P(f'M{vx - 24},{vy - 300} L{vx + 24},{vy - 300} L{vx + 20},{vy - 250} Q{vx + 100},{vy - 200} {vx + 70},{vy - 70} Q{vx + 50},{vy} {vx + 36},{vy} L{vx - 36},{vy} Q{vx - 50},{vy} {vx - 70},{vy - 70} Q{vx - 100},{vy - 200} {vx - 20},{vy - 250}Z', 'porc', extra='filter="url(#shs)"'),
            R(vx - 30, vy - 306, 60, 12, 'porc', 4), S(f'M{vx - 26},{vy - 300} L{vx + 26},{vy - 300}', 'blue', 4), S(f'M{vx - 52},{vy - 220} Q{vx},{vy - 236} {vx + 52},{vy - 220}', 'blue', 5),
            S(f'M{vx - 78},{vy - 90} Q{vx},{vy - 80} {vx + 78},{vy - 90}', 'blue', 5), S(f'M{vx - 40},{vy - 20} L{vx + 40},{vy - 20}', 'blue', 4)]
    for k in range(5):
        a = k * 1.25
        vase.append(S(f'M{vx - 50 + k * 22},{vy - 150 + 14 * math.sin(a)} q10,-18 20,0 q-10,18 -20,0', 'blue', 4, .9))
    vase += [S(f'M{vx - 60},{vy - 130} C{vx - 20},{vy - 190} {vx + 20},{vy - 110} {vx + 60},{vy - 160}', 'blue', 4, .8), C(vx - 20, vy - 160, 12, 'blue', .8), C(vx + 30, vy - 130, 10, 'blue', .8),
             *[S(f'M{vx - 26 + k * 13},{vy - 280} L{vx - 26 + k * 13},{vy - 256}', 'blue', 3, .7) for k in range(5)], E(vx - 36, vy - 170, 10, 40, '#ffffff', .45)]
    s.layer('vase', vase, 'rise', .6)
    # 小展台：彩陶罐 + 玉璧（中间两侧靠墙）
    sm = [R(450, 760, 120, 120, 'plinth', 4, extra='filter="url(#shs)"'), R(444, 752, 132, 12, 'plinth2', 3),
          P('M480,752 Q456,712 474,682 L486,668 L534,668 L546,682 Q564,712 540,752Z', 'clay', extra='filter="url(#shs)"'), R(484, 660, 52, 12, 'clay2', 3),
          *[S(f'M{464 + k * 18},712 q9,-14 18,0', 'clay2', 4) for k in range(4)], S('M468,694 L552,694', 'clay2', 3), S('M468,730 L552,730', 'clay2', 3),
          R(1350, 760, 120, 120, 'plinth', 4, extra='filter="url(#shs)"'), R(1344, 752, 132, 12, 'plinth2', 3), R(1404, 712, 12, 42, 'panel', 3),
          C(1410, 674, 46, 'jade', extra='filter="url(#shs)"'), C(1410, 674, 16, 'wall1'), S('M1374,674 a36,36 0 0,1 72,0', '#ffffff', 3, .4),
          *[C(1410 + 31 * math.cos(a), 674 + 31 * math.sin(a), 3, '#7FB399') for a in [k * math.pi / 6 for k in range(12)]]]
    s.layer('small_plinths', sm, 'pop', .75)
    # 隔离栏
    rp = []
    for x in (640, 1280):
        rp += [E(x, 910, 30, 8, '#000000', .15), R(x - 22, 900, 44, 10, 'gold', 4), R(x - 5, 790, 10, 112, 'gold', 4), C(x, 786, 10, 'gold')]
    rp.append(S('M640,792 Q960,860 1280,792', 'rope', 10))
    s.layer('stanchions', rp, 'rise', .9)
    s.layer('glints', [C(330, 470, 4, '#ffffff', .9), C(1520, 400, 5, '#ffffff', .9), C(1410, 640, 3, '#ffffff', .9)], 'fade', 1.2, loop='twinkle')
    return s


# ============ s030 汉字演变长廊 ============
def hanzi():
    s = Scene('s030', '汉字演变长廊', '语文与历史', ['语文', '汉字', '历史', '书法'],
              dict(wall1='#F7EFE0', wall2='#EADBC1', pillar='#C24A3E', pillar2='#9E3A31', beam='#2F7A78', beam2='#5BA6A0', beam3='#E8B95A', floor1='#D9CBB0', floor2='#BFAE8E',
                   bone='#EDE1C6', bone2='#CDB98F', bronze='#5E9483', bronze2='#3F7466', bamboo='#D8B66E', bamboo2='#B8924E', paper='#FFFBF0', ink='#2F2C2A', red='#C8473A',
                   type='#C9A26C', type2='#A7804C', lan='#E0533F', gold='#F2C766', sky='#CDE9E6', leaf='#77B58C'),
              desc='古色长廊：红柱彩梁间依次陈列甲骨、青铜铭文、竹简、宣纸与活字，中央展板展示象形字到楷书的演变。', stand={'ground_y': 910, 'x': [600, 1320]})
    hw = [R(0, 0, W, 800, s.lg([(0, 'wall1'), (1, 'wall2')])), R(0, 690, W, 110, 'wall2'), R(0, 690, W, 6, 'pillar2', 0, .5), R(0, 794, W, 6, 'pillar2', 0, .5)]
    for x in range(0, W, 48): hw.append(S(f'M{x + 6},770 L{x + 6},716 L{x + 40},716 L{x + 40},760 L{x + 18},760 L{x + 18},730 L{x + 30},730', 'bone2', 4, .8))
    s.layer('wall', hw, 'fade', 0)
    fl = [R(0, 800, W, 280, s.lg([(0, 'floor1'), (1, 'floor2')]))]
    for y in range(800, 1080, 56):
        for x in range(-(y // 56 % 2) * 60, W, 120): fl.append(R(x + 2, y + 2, 116, 52, 'floor2', 3, .3))
    s.layer('floor', fl, 'rise', .1)
    # 展板位置（柱间）：x 中心
    bays = [(170, 260), (520, 300), (960, 440), (1400, 300), (1750, 260)]

    def frame(cx, w, y0=220, h=380):
        return G([R(cx - w / 2 - 10, y0 - 10, w + 20, h + 20, 'pillar2', 8, extra='filter="url(#sh)"'), R(cx - w / 2, y0, w, h, 'paper', 4)])
    # 1 甲骨
    x = bays[0][0]
    p1 = [frame(x, 220), P(f'M{x - 70},300 Q{x - 80},250 {x - 30},236 L{x + 30},236 Q{x + 80},250 {x + 70},300 L{x + 76},420 Q{x + 70},520 {x},540 Q{x - 70},520 {x - 76},420Z', 'bone', extra='filter="url(#shs)"'),
          S(f'M{x},250 L{x},530', 'bone2', 3), S(f'M{x - 70},330 L{x + 70},330 M{x - 74},430 L{x + 74},430', 'bone2', 3)]
    # 象形刻画：日、月、山、人、水
    p1 += [S(f'M{x - 40},285 a16,16 0 1,0 0.1,0', 'bone2', 4), C(x - 40, 301, 3, 'bone2'),
           S(f'M{x + 26},282 q22,18 0,40 q10,-20 0,-40', 'bone2', 4), S(f'M{x - 56},400 l14,-30 l14,30 l14,-44 l14,44 l14,-30 l14,30', 'bone2', 4),
           S(f'M{x + 28},360 l-14,44 M{x + 28},376 l14,28', 'bone2', 4), S(f'M{x - 30},470 q8,14 0,28 M{x - 44},470 q-8,14 0,28 M{x - 16},470 q8,14 0,28', 'bone2', 3),
           S(f'M{x + 20},460 l8,8 l-8,8 l8,8 M{x + 40},462 l0,40', 'bone2', 3)]
    # 2 青铜铭文（鼎）
    x = bays[1][0]
    p2 = [frame(x, 260), R(x - 90, 260, 180, 200, 'bronze', 10, extra='filter="url(#shs)"'), R(x - 80, 270, 160, 180, 'bronze2', 6, .5)]
    random.seed(31)
    for i in range(3):
        for j in range(4):
            cx_, cy_ = x - 50 + i * 50, 300 + j * 44
            p2.append(fakechar(cx_, cy_, 32, 200 + i * 5 + j, '#A9D2C2'))
    p2 += [P(f'M{x - 70},470 L{x + 70},470 Q{x + 74},540 {x},556 Q{x - 74},540 {x - 70},470Z', 'bronze'), R(x - 76, 462, 152, 12, 'bronze2', 4)]
    # 3 中央：象形 → 楷书
    x = bays[2][0]
    p3 = [frame(x, 560, 200, 420), R(x - 280, 200, 560, 50, 'beam', 4), *[C(x - 240 + k * 60, 225, 8, 'beam3') for k in range(9)]]
    glyph_x = [x - 195, x - 65, x + 65, x + 195]
    pict = [
        [S('M{0},330 a34,34 0 1,0 0.1,0', 'ink', 6), C(0, 364, 6, 'ink')],
        [S('M{0},330 q46,34 0,70 q20,-34 0,-70', 'ink', 6)],
        [S('M{0},400 l-44,0 l0,-30 M{0},400 l44,0 l0,-30 M{0},400 l0,-70', 'ink', 6)],
        [S('M{0},326 l0,80 M{0},360 l-28,-28 M{0},360 l28,-28 M{0},392 l-26,18 M{0},392 l26,18', 'ink', 6)],
    ]
    for k, gx in enumerate(glyph_x):
        for item in pict[k]:
            p3.append(item.replace('M{0}', f'M{gx}').replace('cx="0.0"', f'cx="{gx}.0"'))
    p3[-1:] = p3[-1:]
    # 修正：日中点
    p3 = [it if 'cx="0.0"' not in it else it.replace('cx="0.0"', f'cx="{glyph_x[0]:.1f}"') for it in p3]
    for gx in glyph_x:
        p3 += [P(f'M{gx - 10},430 L{gx + 10},430 L{gx + 10},446 L{gx + 18},446 L{gx},466 L{gx - 18},446 L{gx - 10},446Z', 'red', .8)]
    for gx, ch in zip(glyph_x, '日月山木'):
        p3 += [R(gx - 50, 480, 100, 100, 'wall1', 10), T(gx, 556, ch, 72, 'ink', 800)]
    s.layer('panels_side', [G(p1), G(p2)], 'pop', .4)
    # 4 竹简
    x = bays[3][0]
    p4 = [frame(x, 260)]
    for k in range(9):
        bx = x - 104 + k * 26
        p4 += [R(bx, 250, 22, 300, 'bamboo', 4, extra='filter="url(#shs)"' if k == 0 else ''), R(bx + 15, 250, 4, 300, 'bamboo2', 2, .6)]
        for j in range(5): p4.append(fakechar(bx + 10, 280 + j * 56, 18, 300 + k * 9 + j, 'ink'))
    p4 += [R(x - 108, 300, 238, 4, 'bamboo2'), R(x - 108, 500, 238, 4, 'bamboo2')]
    # 5 活字
    x = bays[4][0]
    p5 = [frame(x, 220), R(x - 90, 260, 180, 240, 'type2', 8, extra='filter="url(#shs)"')]
    for i in range(4):
        for j in range(5):
            p5 += [R(x - 82 + i * 42, 268 + j * 46, 38, 42, 'type', 4), fakechar(x - 63 + i * 42, 289 + j * 46, 26, 400 + i * 11 + j, 'type2')]
    p5 += [R(x - 60, 520, 120, 56, 'paper', 4, extra='filter="url(#shs)"'), *[fakechar(x - 36 + k * 36, 548, 22, 500 + k, 'ink') for k in range(3)]]
    s.layer('panels_right', [G(p4), G(p5)], 'pop', .55)
    s.layer('panel_center', p3, 'zoom', .7)
    # 长廊结构：柱 + 彩梁 + 挂落
    st = [R(0, 0, W, 130, 'beam', extra='filter="url(#sh)"'), R(0, 26, W, 8, 'beam3'), R(0, 112, W, 8, 'beam3')]
    for k in range(13):
        x = 75 + k * 150
        st += [P(f'M{x - 44},73 L{x},48 L{x + 44},73 L{x},98Z', 'beam2'), C(x, 73, 18, 'beam3'), C(x, 73, 9, 'pillar'),
               *[C(x + 24 * math.cos(a), 73 + 15 * math.sin(a), 6, 'wall1', .9) for a in [j * math.pi / 3 for j in range(6)]],
               S(f'M{x + 60},40 L{x + 60},106 M{x + 90},40 L{x + 90},106', 'beam3', 3, .6)]
    for x in (0, 345, 1575, 1920 - 1):
        pass
    for x in (345, 1575):
        st += [R(x - 26, 120, 52, 690, s.lg([(0, 'pillar2'), (.5, 'pillar'), (1, 'pillar2')], 0, 0, 1, 0)), R(x - 36, 790, 72, 20, 'bone2', 4)]
    for x in (0, 1920):
        st += [R(x - 26, 120, 52, 690, s.lg([(0, 'pillar2'), (.5, 'pillar'), (1, 'pillar2')], 0, 0, 1, 0))]
    # 挂落（花格）
    for x0, x1 in ((26, 319), (371, 1549), (1601, 1894)):
        st.append(R(x0, 130, x1 - x0, 10, 'pillar2'))
        for xx in range(int(x0) + 10, int(x1) - 20, 34):
            st.append(S(f'M{xx},140 l0,18 l24,0 l0,-18', 'pillar2', 4, .9))
    s.layer('corridor', st, 'drop', .2)
    s.layer('lanterns', [lantern(x, 140, .55, 'lan', 'gold') for x in (345, 1575)], 'drop', .9, loop='sway')
    s.layer('glow', [C(x, 184, 50, 'gold', .4, 'filter="url(#b20)"') for x in (345, 1575)] + [E(960, 880, 420, 50, '#FFF6DE', .4, 'filter="url(#b40)"')], 'fade', 1.0, loop='glow')
    # 前景：毛笔墨迹装饰 + 绿植
    pl = []
    for px, sd in ((80, 1), (1840, -1)):
        pl += [E(px, 912, 80, 12, '#000000', .14), R(px - 46, 820, 92, 90, 'bronze', 14, extra='filter="url(#shs)"'), R(px - 46, 840, 92, 8, 'bronze2', 0, .6)]
        for k, a in enumerate([-2.7, -2.1, -1.57, -1.0, -.45]):
            ex, ey = px + 60 * math.cos(a), 790 + 50 * math.sin(a)
            pl.append(E(ex, ey, 56, 16, 'leaf', extra=f'transform="rotate({math.degrees(a):.0f} {ex:.0f} {ey:.0f})"'))
    s.layer('plants', pl, 'grow', 1.0, loop='sway')
    return s


SCENES = [calligraphy, readingcorner, opera, academy, greatwall, palacegate, ancientmarket, museum, hanzi]
