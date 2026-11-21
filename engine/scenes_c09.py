"""第 9 类 · 社会日常：s082–s090（平面 MG）"""
from core import *
import math, random


# ---------- 本模块小工具 ----------
def smooth(pts, close_to=None):
    """二次曲线平滑折线；close_to=底边 y 时闭合成填充形状"""
    d = f'M{pts[0][0]:.1f},{pts[0][1]:.1f}'
    for i in range(1, len(pts) - 1):
        mx, my = (pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2
        d += f' Q{pts[i][0]:.1f},{pts[i][1]:.1f} {mx:.1f},{my:.1f}'
    d += f' L{pts[-1][0]:.1f},{pts[-1][1]:.1f}'
    if close_to is not None:
        d += f' L{pts[-1][0]:.1f},{close_to} L{pts[0][0]:.1f},{close_to}Z'
    return d


def hills(y, amp, seed, step=160, x0=-60, x1=W + 60):
    random.seed(seed); pts = []; x = x0
    while x <= x1 + step:
        pts.append((x, y - random.uniform(.25, 1) * amp)); x += step
    return pts


def shadow(x, y, rx, ry=None, op=.14):
    return E(x, y, rx, ry or rx * .09, '#2a1e30', op, 'filter="url(#b6)"')


def leafy(x, y, s, c1, c2, pot, n=7):
    """盆栽：x,y 为盆底中心"""
    it = [shadow(x, y, 50 * s), P(f'M{x - 40 * s},{y - 80 * s} L{x + 40 * s},{y - 80 * s} L{x + 30 * s},{y} L{x - 30 * s},{y}Z', pot), R(x - 44 * s, y - 88 * s, 88 * s, 14 * s, pot, 6 * s)]
    for k in range(n):
        a = -math.pi / 2 + (k - (n - 1) / 2) * .42
        lx, ly = x + 70 * s * math.cos(a), y - 90 * s + 70 * s * math.sin(a)
        it.append(E(lx, ly, 46 * s, 15 * s, c1 if k % 2 else c2, extra=f'transform="rotate({math.degrees(a):.0f} {lx:.0f} {ly:.0f})"'))
    return G(it)


def flowerbed(x0, x1, y, seed, cols, leaf, h=40):
    random.seed(seed); it = []
    for k in range(int((x1 - x0) / 26)):
        x = x0 + k * 26 + random.uniform(-6, 6); hh = h * random.uniform(.7, 1.2)
        it += [S(f'M{x:.0f},{y} L{x:.0f},{y - hh:.0f}', leaf, 3), E(x - 8, y - hh * .5, 9, 4, leaf, extra=f'transform="rotate(-30 {x - 8:.0f} {y - hh * .5:.0f})"')]
        col = cols[k % len(cols)]
        for q in range(5):
            a = q * math.pi * 2 / 5
            it.append(C(x + 7 * math.cos(a), y - hh + 7 * math.sin(a), 6, col))
        it.append(C(x, y - hh, 4, '#FFF3C4'))
    return G(it)


def ring(x, y, r, col, w, op=1):
    return S(f'M{x - r},{y} a{r},{r} 0 1,0 {2 * r},0 a{r},{r} 0 1,0 {-2 * r},0', col, w, op)


def lights_strip(y, xs, col, glow):
    it = []
    for x in xs:
        it += [R(x - 90, y, 180, 16, col, 8), C(x, y + 30, 70, glow, .35, 'filter="url(#b20)"')]
    return it


# ============ s082 超市收银台 ============
def supermarket():
    s = Scene('s082', '超市收银台', '社会日常', ['数学', '认识人民币', '购物', '社会生活'],
              dict(wall1='#EAF6F2', wall2='#D3ECE5', ceil='#FFFFFF', panel='#FFF8E6', glow='#FFF3C4', shelf='#FFFFFF', shelf2='#CFE3DE', head='#3E9A8F',
                   floor1='#F3EADB', floor2='#E2D3BC', counter='#3E9A8F', counter2='#2E7A71', top='#F4F6F7', belt='#3A4048', belt2='#59616C', metal='#AEB8C3',
                   screen='#22303A', screen2='#7FE0C8', g1='#F2836B', g2='#F7C55E', g3='#6FB6E0', g4='#8ED081', g5='#B39DDB', g6='#F5A3B5', cart='#E8665A', white='#FFFFFF'),
              desc='明亮超市：背景货架摆满彩色商品，右侧收银台有传送带、收银机和扫码器，左侧购物车，适合认识人民币与购物计算。',
              stand={'ground_y': 910, 'x': [560, 1240]})
    s.layer('wall', [R(0, 0, W, 800, s.lg([(0, 'wall1'), (1, 'wall2')])), R(0, 0, W, 64, 'ceil'), R(0, 62, W, 6, 'shelf2')], 'fade', 0)
    s.layer('ceiling_lights', [*lights_strip(22, (240, 720, 1200, 1680), 'panel', 'glow')], 'fade', .15, loop='glow')
    # 背景货架
    random.seed(21)

    def gondola(x0, w, top, hc):
        it = [R(x0 - 12, top - 46, w + 24, 46, hc, 12, extra='filter="url(#shs)"'), R(x0, top, w, 800 - top, 'shelf2', 6)]
        levels = 4; lh = (800 - top - 40) / levels
        for lv in range(levels):
            yb = top + (lv + 1) * lh
            x = x0 + 12
            while x < x0 + w - 40:
                kind = random.random(); col = random.choice(['g1', 'g2', 'g3', 'g4', 'g5', 'g6'])
                if kind < .4:   # 盒子
                    bw, bh = random.randint(34, 52), random.randint(int(lh * .5), int(lh * .78))
                    if x + bw > x0 + w - 12: break
                    for q in range(random.randint(1, 3)):
                        if x + bw > x0 + w - 12: break
                        it += [R(x, yb - bh, bw, bh, col, 4), R(x, yb - bh * .62, bw, bh * .22, 'white', 0, .55)]; x += bw + 3
                elif kind < .7:  # 瓶子
                    bh = random.randint(int(lh * .55), int(lh * .8))
                    for q in range(random.randint(2, 4)):
                        if x + 24 > x0 + w - 12: break
                        it += [R(x, yb - bh * .72, 24, bh * .72, col, 8), R(x + 7, yb - bh, 10, bh * .32, col, 3), R(x, yb - bh * .45, 24, bh * .16, 'white', 0, .6)]; x += 28
                else:  # 罐头
                    for q in range(random.randint(2, 4)):
                        if x + 30 > x0 + w - 12: break
                        it += [R(x, yb - 40, 30, 40, col, 5), R(x, yb - 30, 30, 14, 'white', 0, .5), E(x + 15, yb - 40, 15, 4, 'metal')]; x += 33
                x += 8
            it += [R(x0 - 4, yb, w + 8, 12, 'shelf', 3, extra='filter="url(#shs)"'), R(x0 - 4, yb + 3, w + 8, 4, 'g2', 0, .0)]
            for px in range(int(x0 + 40), int(x0 + w - 30), 150):
                it.append(R(px, yb + 2, 26, 9, 'g2', 2))
        return G(it)
    s.layer('shelves', [gondola(40, 520, 330, 'head'), gondola(680, 560, 300, 'g1'), gondola(1360, 520, 330, 'head')], 'rise', .25)
    # 悬挂分类牌（图形）
    hs = []
    for x, col, ic in [(300, 'g1', 'apple'), (960, 'g3', 'bottle'), (1620, 'g2', 'bread')]:
        hs += [S(f'M{x - 50},68 L{x - 50},130 M{x + 50},68 L{x + 50},130', 'metal', 3), R(x - 90, 128, 180, 86, col, 20, extra='filter="url(#shs)"'), C(x, 171, 30, 'white')]
        if ic == 'apple':
            hs += [C(x - 7, 174, 14, col), C(x + 7, 174, 14, col), P(f'M{x},160 q6,-14 16,-12 q-4,12 -16,12Z', 'g4')]
        elif ic == 'bottle':
            hs += [R(x - 9, 160, 18, 28, col, 5), R(x - 4, 150, 8, 12, col, 2)]
        else:
            hs += [P(f'M{x - 18},186 L{x - 18},170 Q{x - 18},154 {x},154 Q{x + 18},154 {x + 18},170 L{x + 18},186Z', col)]
    s.layer('hanging_signs', hs, 'drop', .5, loop='sway')
    # 地面
    fl = [R(0, 800, W, 280, s.lg([(0, 'floor1'), (1, 'floor2')]))]
    for y in (840, 900, 980): fl.append(R(0, y, W, 2, 'floor2', 0, .8))
    for x in range(0, W, 160): fl.append(R(x, 800, 2, 280, 'floor2', 0, .6))
    fl.append(E(960, 860, 700, 40, 'white', .35, 'filter="url(#b20)"'))
    s.layer('floor', fl, 'rise', .1)
    # 收银台（右）
    cx0 = 1290
    ck = [shadow(1580, 905, 330), R(cx0, 700, 560, 200, 'counter', 14, extra='filter="url(#sh)"'), R(cx0, 700, 560, 18, 'counter2', 8),
          R(cx0 + 20, 740, 520, 8, 'white', 4, .25), R(cx0 - 10, 682, 360, 28, 'belt', 10), R(cx0, 686, 340, 8, 'belt2', 4)]
    for k in range(8): ck.append(R(cx0 + 14 + k * 42, 694, 3, 12, 'belt2'))
    ck += [R(cx0 + 340, 680, 210, 24, 'top', 8), R(cx0 + 360, 672, 90, 14, 'screen', 4), R(cx0 + 372, 675, 60, 6, 'g3', 3, .8)]
    # 收银机
    rx = 1720
    ck += [R(rx - 70, 640, 140, 42, 'top', 10, extra='filter="url(#shs)"'), R(rx - 54, 652, 108, 8, 'metal', 3), R(rx - 54, 666, 108, 6, 'metal', 3),
           R(rx - 6, 560, 12, 84, 'metal', 4), R(rx - 70, 470, 140, 96, 'screen', 12, extra='filter="url(#shs)"'), R(rx - 58, 482, 116, 72, 'screen2', 6, .9),
           R(rx - 46, 494, 60, 8, 'white', 3, .8), R(rx - 46, 510, 90, 6, 'white', 3, .5), R(rx - 46, 524, 74, 6, 'white', 3, .5),
           R(1580, 620, 46, 62, 'belt', 8), R(1586, 628, 34, 22, 'screen2', 3, .8)]
    for k in range(9): ck.append(R(1588 + (k % 3) * 11, 656 + (k // 3) * 7, 8, 5, 'metal', 1))
    s.layer('checkout', ck, 'slide-r', .45)
    # 收银灯柱（号码 1）
    lp = [R(1858, 420, 14, 300, 'metal', 5), C(1865, 400, 40, 'g1', extra='filter="url(#shs)"'), C(1865, 400, 30, 'white'), T(1865, 414, '1', 40, 'g1', 900)]
    s.layer('lane_light', lp, 'pop', .7)
    s.layer('lane_glow', [C(1865, 400, 80, 'g1', .3, 'filter="url(#b20)"')], 'fade', 1.0, loop='glow')
    # 传送带上的商品
    gd = [R(1310, 610, 56, 74, 'white', 6, extra='filter="url(#shs)"'), P('M1310,612 L1338,588 L1366,612Z', 'g3'), R(1310, 632, 56, 22, 'g3', 0),
          C(1410, 664, 20, 'g1'), C(1402, 656, 6, 'white', .6), P('M1410,646 q4,-12 14,-10 q-3,10 -14,10Z', 'g4'),
          E(1490, 668, 50, 18, 'g2'), E(1490, 660, 46, 12, '#FBDD8A'), *[S(f'M{1462 + k * 18},656 l8,10', '#D9A23E', 3) for k in range(3)],
          R(1460, 590, 10, 0.1, 'g2')]
    s.layer('goods', gd, 'pop', .85)
    # 购物车（左）
    cx, cy = 300, 905
    ct = [shadow(cx + 20, cy, 190), P(f'M{cx - 160},700 L{cx + 160},700 L{cx + 130},830 L{cx - 120},830Z', 'cart', .18),
          S(f'M{cx - 160},700 L{cx + 160},700 L{cx + 130},830 L{cx - 120},830Z', 'cart', 8)]
    for k in range(1, 7): ct.append(S(f'M{cx - 160 + k * 46},700 L{cx - 120 + k * 36},830', 'cart', 4, .7))
    ct += [S(f'M{cx - 150},745 L{cx + 148},745 M{cx - 136},790 L{cx + 140},790', 'cart', 4, .7), S(f'M{cx + 160},700 L{cx + 200},640 L{cx + 250},640', 'metal', 10),
           R(cx + 236, 630, 46, 20, 'g2', 10), S(f'M{cx - 120},830 L{cx - 140},880 L{cx + 150},880', 'metal', 8),
           C(cx - 120, cy - 10, 16, 'belt'), C(cx + 130, cy - 10, 16, 'belt'), C(cx - 120, cy - 10, 6, 'metal'), C(cx + 130, cy - 10, 6, 'metal')]
    # 车里的东西
    ct = ct[:1] + [R(cx - 120, 610, 60, 96, 'g4', 6), R(cx - 120, 640, 60, 26, 'white', 0, .6), R(cx - 50, 640, 40, 66, 'g6', 10), R(cx - 40, 624, 20, 20, 'g6', 3),
                   E(cx + 40, 676, 64, 30, 'g2'), C(cx + 110, 676, 28, 'g1'), P(f'M{cx - 80},700 Q{cx - 30},560 {cx + 10},700Z', 'g4', .0)] + ct[1:]
    s.layer('cart', ct, 'slide-l', .6)
    # 购物篮堆
    bk = [shadow(560, 905, 80)]
    for k in range(3):
        y = 860 - k * 22
        bk += [P(f'M{500},{y - 50} L{620},{y - 50} L{610},{y} L{510},{y}Z', 'g1' if k < 2 else 'cart'), R(498, y - 54, 124, 10, 'counter2', 4)]
    bk += [S('M520,786 Q560,740 600,786', 'belt', 6)]
    for k in range(5): bk.append(R(516 + k * 20, 830, 10, 22, 'white', 3, .5))
    s.layer('baskets', bk, 'pop', .8)
    s.layer('sparkle', [C(x, y, 5, 'white', .9) for x, y in [(1340, 600), (1730, 488), (1500, 640), (980, 330)]], 'fade', 1.2, loop='twinkle')
    return s


# ============ s083 社区公园 ============
def park():
    s = Scene('s083', '社区公园', '社会日常', ['体育', '健康', '社区生活', '户外活动'],
              dict(sky1='#A6DCF6', sky2='#EEF9FF', sun='#FFE7A3', b1='#F3D9C6', b2='#DCE6F3', b3='#F6E9BE', win='#FFFFFF', far='#BFE2B2', tree='#5FAE74', tree2='#A1D893', trunk='#8A5A3A',
                   grass1='#A6D884', grass2='#86C569', path='#F4E6CB', path2='#E3CFA8', bench='#E0905C', bench2='#B56A3C', iron='#4F5D6B', fit1='#F2B33D', fit2='#3FA0D6', fit3='#E8665A',
                   pav='#C8463E', pav2='#F0E6D2', col='#B83A33', f1='#F2836B', f2='#FFFFFF', f3='#F7C55E', f4='#C6A4E8', kite='#F2836B', kite2='#FFD36E', lamp='#FFF3C4'),
              desc='阳光社区公园：远处住宅楼，草坪中的弯曲步道，凉亭、长椅、路灯、健身器材与花坛，天上飘着风筝。',
              stand={'ground_y': 900, 'x': [560, 1360]})
    s.layer('sky', [R(0, 0, W, 760, s.lg([(0, 'sky1'), (1, 'sky2')])), C(1560, 190, 170, 'sun', .4, 'filter="url(#b40)"'), C(1560, 190, 70, 'sun')], 'fade', 0)
    s.layer('clouds', [cloud(330, 160, .8, op=.95), cloud(980, 110, .55, op=.85), cloud(1250, 230, .45, op=.8)], 'slide-l', .2, loop='drift')
    # 远处住宅楼
    bl = []
    for x, w, h, col in [(40, 220, 330, 'b2'), (300, 180, 260, 'b1'), (1240, 200, 300, 'b3'), (1480, 230, 360, 'b2'), (1750, 170, 280, 'b1'), (720, 170, 220, 'b3'), (930, 200, 190, 'b2')]:
        top = 640 - h
        bl += [R(x, top, w, h + 20, col, 10), R(x, top, w, 14, 'win', 6, .5)]
        for wy in range(top + 34, 610, 46):
            for wx in range(x + 22, x + w - 30, 46):
                bl += [R(wx, wy, 26, 28, 'win', 4, .75), R(wx, wy + 22, 26, 6, col, 0, .5)]
    s.layer('buildings', bl, 'rise', .25)
    s.layer('haze', [R(0, 460, W, 220, s.lg([(0, 'sky2', 0), (1, 'sky2', .85)]))], 'fade', .3)
    # 远树篱
    ft = [P(smooth(hills(680, 50, 4, 90), 760), 'far')]
    for k, x in enumerate(range(-20, W + 60, 150)):
        ft.append(blob_tree(x, 700, .62 + .12 * ((k * 7) % 3), 'tree' if k % 2 else '#79BE84', 'tree2', 'trunk'))
    s.layer('trees_far', ft, 'grow', .4)
    # 草地与步道
    gd = [P(smooth([(-40, 720), (400, 700), (960, 715), (1500, 698), (1960, 712)], 1080), s.lg([(0, 'grass1'), (1, 'grass2')]))]
    gd += [P('M820,712 Q760,760 720,810 Q640,900 380,1080 L1540,1080 Q1280,900 1200,810 Q1160,760 1100,712Z', 'path'),
           S('M820,712 Q760,760 720,810 Q640,900 380,1080', 'path2', 8), S('M1100,712 Q1160,760 1200,810 Q1280,900 1540,1080', 'path2', 8)]
    for k, (x, y) in enumerate([(900, 760), (1000, 800), (880, 850), (1060, 900), (920, 960), (1150, 1010), (760, 1020)]):
        gd.append(E(x, y, 34 + k * 3, 10 + k, 'path2', .7))
    s.layer('ground', gd, 'rise', .1)
    # 凉亭（左后）
    px = 330
    pv = [shadow(px, 745, 170), R(px - 140, 728, 280, 18, 'pav2', 6), R(px - 120, 610, 16, 122, 'col', 4), R(px + 104, 610, 16, 122, 'col', 4), R(px - 8, 610, 16, 122, 'col', 4, .5),
          R(px - 130, 690, 260, 10, 'pav2', 4), P(f'M{px - 180},620 Q{px},600 {px + 180},620 Q{px + 120},560 {px},500 Q{px - 120},560 {px - 180},620Z', 'pav'),
          P(f'M{px - 180},620 Q{px - 200},606 {px - 196},596 Q{px - 170},614 {px - 150},612Z', 'pav'), P(f'M{px + 180},620 Q{px + 200},606 {px + 196},596 Q{px + 170},614 {px + 150},612Z', 'pav'),
          R(px - 160, 614, 320, 12, 'col', 6), C(px, 494, 9, 'fit1'), P(f'M{px},500 Q{px - 60},560 {px - 120},600', 'none'), S(f'M{px},504 Q{px - 50},560 {px - 130},604', 'col', 3, .5), S(f'M{px},504 Q{px + 50},560 {px + 130},604', 'col', 3, .5)]
    s.layer('pavilion', pv, 'drop', .5)
    # 健身器材（右）
    fx = 1560
    fe = [shadow(fx + 60, 900, 230), S(f'M{fx - 100},900 L{fx - 100},700 Q{fx - 100},680 {fx - 80},680 L{fx + 40},680 Q{fx + 60},680 {fx + 60},700 L{fx + 60},900', 'fit2', 18),
          S(f'M{fx - 100},760 L{fx + 60},760', 'fit1', 12), R(fx - 112, 890, 24, 14, 'iron', 4), R(fx + 48, 890, 24, 14, 'iron', 4),
          # 太极推手转盘
          S(f'M{fx + 200},900 L{fx + 200},740', 'fit3', 16), C(fx + 200, 740, 46, 'fit1', extra='filter="url(#shs)"'), C(fx + 200, 740, 30, 'fit3'), C(fx + 200, 740, 8, 'fit1'),
          *[S(f'M{fx + 200 + 30 * math.cos(a):.0f},{740 + 30 * math.sin(a):.0f} L{fx + 200 + 50 * math.cos(a):.0f},{740 + 50 * math.sin(a):.0f}', 'iron', 6) for a in (0, 2.1, 4.2)],
          R(fx + 186, 890, 28, 14, 'iron', 4)]
    s.layer('fitness', fe, 'rise', .65)
    # 长椅 + 路灯（左前）
    bx = 330
    bc = [shadow(bx, 912, 190), R(bx - 170, 800, 340, 22, 'bench', 8), R(bx - 170, 830, 340, 22, 'bench', 8), R(bx - 176, 860, 352, 22, 'bench2', 8, extra='filter="url(#shs)"'),
          S(f'M{bx - 140},790 L{bx - 140},906 M{bx + 140},790 L{bx + 140},906', 'iron', 10), S(f'M{bx - 160},882 L{bx - 160},906 M{bx + 160},882 L{bx + 160},906', 'iron', 10)]
    lx = 640
    bc += [shadow(lx, 908, 40), R(lx - 8, 560, 16, 344, 'iron', 6), R(lx - 22, 890, 44, 18, 'iron', 6), P(f'M{lx - 34},560 L{lx + 34},560 L{lx + 24},520 L{lx - 24},520Z', 'iron'),
           R(lx - 26, 562, 52, 34, 'lamp', 6), P(f'M{lx - 30},520 Q{lx},494 {lx + 30},520Z', 'iron')]
    s.layer('bench_lamp', bc, 'slide-l', .75)
    s.layer('lamp_glow', [C(lx, 580, 60, 'lamp', .45, 'filter="url(#b20)"')], 'fade', 1.1, loop='glow')
    # 花坛（前景两角）
    fb = [P('M0,960 Q140,900 300,950 L300,1080 L0,1080Z', 'grass2'), flowerbed(10, 280, 960, 3, ['f1', 'f3', 'f2'], 'tree', 46),
          P('M1640,950 Q1780,905 1920,950 L1920,1080 L1640,1080Z', 'grass2'), flowerbed(1650, 1910, 960, 5, ['f4', 'f2', 'f1'], 'tree', 46)]
    s.layer('flowers', fb, 'grow', .9, loop='sway')
    # 风筝
    kt = [P('M1180,170 L1230,120 L1280,170 L1230,250Z', 'kite', extra='filter="url(#shs)"'), P('M1180,170 L1230,120 L1230,250Z', 'kite2'), S('M1230,250 q-20,30 0,60 q20,30 0,60', 'kite', 3),
          *[poly([(1230 + dx - 10, y), (1230 + dx + 10, y), (1230 + dx, y + 14)], 'kite2') for dx, y in [(-8, 270), (8, 300), (-6, 330)]], S('M1230,250 Q1100,500 940,720', '#ffffff', 2, .7)]
    s.layer('kite', kt, 'pop', 1.1, loop='bob')
    s.layer('birds', [S(f'M{x},{y} q12,-10 22,0 q10,-10 22,0', 'iron', 3, .7) for x, y in [(620, 220), (670, 250), (720, 210)]], 'slide-l', 1.2)
    return s


# ============ s084 游乐场 ============
def playground():
    s = Scene('s084', '游乐场', '社会日常', ['体育', '游戏安全', '课间活动', '户外'],
              dict(sky1='#86CDF2', sky2='#FFF0D8', sun='#FFE08A', hill='#B8E09C', hill2='#9ACF80', fw='#F7B7C8', fw2='#FFFFFF', fw3='#9DD5F0',
                   floor='#7FC4A8', floor2='#6DB394', tile1='#F2B33D', tile2='#5FB7E0', tile3='#F2836B', sand='#F6DFA8', sand2='#E8C987',
                   post='#3FA0D6', post2='#2F80B8', slide='#F7C55E', slide2='#E8A93A', roof='#E8574A', roof2='#C8453A', deck='#FFFFFF', swing='#F2836B', chain='#7C8A96',
                   seesaw='#8ED081', seesaw2='#5FAE6A', fence='#FFFFFF', bal1='#F2836B', bal2='#F7C55E', bal3='#5FB7E0', bal4='#B39DDB', tree='#5FAE74', tree2='#A1D893', trunk='#8A5A3A'),
              desc='彩色儿童游乐场：带红顶塔楼的滑梯、秋千架、跷跷板和沙池，彩色安全地垫，远处摩天轮与气球。',
              stand={'ground_y': 910, 'x': [600, 1300]})
    s.layer('sky', [R(0, 0, W, 760, s.lg([(0, 'sky1'), (1, 'sky2')])), C(300, 170, 150, 'sun', .4, 'filter="url(#b40)"'), C(300, 170, 64, 'sun')], 'fade', 0)
    s.layer('clouds', [cloud(700, 140, .7, op=.95), cloud(1500, 110, .6, op=.85), cloud(1100, 230, .4, op=.75)], 'slide-l', .2, loop='drift')
    # 远处摩天轮
    fx, fy, fr = 1180, 420, 210
    fw = [S(f'M{fx},{fy} L{fx - 110},700 M{fx},{fy} L{fx + 110},700', 'fw3', 10), ring(fx, fy, fr, 'fw', 10), ring(fx, fy, fr - 30, 'fw2', 4, .8)]
    for k in range(12):
        a = k * math.pi / 6
        fw.append(S(f'M{fx},{fy} L{fx + fr * math.cos(a):.0f},{fy + fr * math.sin(a):.0f}', 'fw2', 3, .8))
        cx, cy = fx + fr * math.cos(a), fy + fr * math.sin(a)
        fw += [R(cx - 18, cy, 36, 30, ['bal1', 'bal2', 'bal3', 'bal4'][k % 4], 9, .85), R(cx - 2, cy - 6, 4, 8, 'fw2')]
    fw.append(C(fx, fy, 18, 'fw'))
    s.layer('ferris', [G(fw, 'opacity=".7"')], 'zoom', .3, loop=None)
    s.layer('hills', [P(smooth(hills(700, 70, 8, 220), 800), 'hill'), P(smooth(hills(740, 40, 9, 180), 820), 'hill2')], 'rise', .25)
    s.layer('trees', [blob_tree(x, 760, sc, 'tree', 'tree2', 'trunk') for x, sc in [(80, .9), (240, .7), (1720, .8), (1870, 1)]], 'grow', .4, loop='sway')
    # 围栏
    fc = [R(0, 724, W, 10, 'fence', 4), R(0, 756, W, 10, 'fence', 4)]
    for x in range(10, W, 40): fc.append(R(x, 700, 14, 90, 'fence', 7))
    s.layer('fence', fc, 'fade', .35)
    # 安全地垫
    fl = [R(0, 780, W, 300, s.lg([(0, 'floor'), (1, 'floor2')]))]
    for x in range(-80, W, 320):
        fl += [R(x, 1000, 300, 80, 'floor2', 0, .45)]
    fl += [R(0, 780, W, 6, 'floor2', 0, .6), R(0, 940, W, 3, 'floor2', 0, .4)]
    s.layer('floor', fl, 'rise', .1)
    # 滑梯塔（右）
    tx = 1500
    sl = [shadow(tx + 60, 905, 300), R(tx - 120, 470, 22, 436, 'post', 8), R(tx + 98, 470, 22, 436, 'post', 8),
          R(tx - 130, 620, 260, 26, 'deck', 8, extra='filter="url(#shs)"'), R(tx - 120, 646, 240, 10, 'post2', 0, .5),
          P(f'M{tx - 150},480 L{tx},370 L{tx + 150},480Z', 'roof', extra='filter="url(#shs)"'), P(f'M{tx},370 L{tx + 150},480 L{tx},480Z', 'roof2', .6), C(tx, 368, 10, 'slide'),
          R(tx - 100, 560, 200, 60, 'none')]
    for k in range(5): sl.append(R(tx - 100 + k * 46, 560, 10, 60, 'post', 5))
    sl.append(R(tx - 110, 554, 220, 12, 'post2', 6))
    # 滑道
    sl += [P(f'M{tx - 120},640 Q{tx - 260},660 {tx - 330},800 Q{tx - 360},870 {tx - 450},880 L{tx - 450},900 Q{tx - 330},900 {tx - 300},810 Q{tx - 250},690 {tx - 120},676Z', 'slide', extra='filter="url(#shs)"'),
           S(f'M{tx - 122},646 Q{tx - 258},664 {tx - 326},804 Q{tx - 356},874 {tx - 450},884', 'slide2', 8)]
    # 爬梯
    sl += [S(f'M{tx + 140},640 L{tx + 230},900 M{tx + 190},640 L{tx + 280},900', 'post2', 10)]
    for k in range(1, 6):
        u = k / 6; sl.append(S(f'M{tx + 140 + 90 * u:.0f},{640 + 260 * u:.0f} L{tx + 190 + 90 * u:.0f},{640 + 260 * u:.0f}', 'slide2', 8))
    s.layer('slide', sl, 'rise', .5)
    # 秋千（左）
    sx = 380
    sw = [shadow(sx, 905, 260), S(f'M{sx - 250},905 L{sx - 190},520 L{sx - 130},905 M{sx + 250},905 L{sx + 190},520 L{sx + 130},905', 'post', 16), R(sx - 214, 506, 428, 26, 'post2', 12)]
    s.layer('swing_frame', sw, 'rise', .55)
    s.layer('swing1', [S(f'M{sx - 110},530 L{sx - 110},800 M{sx - 30},530 L{sx - 30},800', 'chain', 4), R(sx - 126, 796, 112, 18, 'swing', 8, extra='filter="url(#shs)"')], 'fade', .8, loop='swing', origin=f'{sx - 70} 530')
    s.layer('swing2', [S(f'M{sx + 30},530 L{sx + 30},780 M{sx + 110},530 L{sx + 110},780', 'chain', 4), R(sx + 14, 776, 112, 18, 'tile1', 8, extra='filter="url(#shs)"')], 'fade', .9)
    # 跷跷板 + 沙池（前）
    ss = [shadow(250, 1000, 200), P('M220,1000 L280,1000 L250,950Z', 'seesaw2'), R(60, 942, 380, 18, 'seesaw', 9, extra='transform="rotate(-9 250 951)"'),
          R(80, 900, 12, 40, 'chain', 4, extra='transform="rotate(-9 250 951)"'), R(408, 900, 12, 40, 'chain', 4, extra='transform="rotate(-9 250 951)"'),
          shadow(1720, 960, 190), E(1720, 940, 200, 50, 'sand2'), E(1720, 934, 180, 40, 'sand'), P('M1660,930 L1720,880 L1780,930Z', 'sand2'), R(1710, 870, 3, 20, 'chain'), poly([(1713, 870), (1735, 876), (1713, 882)], 'tile3'),
          P('M1800,920 L1820,920 L1826,940 L1794,940Z', 'tile2'), S('M1802,922 Q1810,906 1820,922', 'tile2', 3), E(1640, 944, 20, 6, 'tile1')]
    s.layer('seesaw_sand', ss, 'pop', .95)
    # 气球
    bb = []
    for x, y, col in [(860, 300, 'bal1'), (920, 260, 'bal3'), (980, 310, 'bal2'), (1040, 270, 'bal4')]:
        bb += [S(f'M{x},{y + 46} Q{x + 10},{y + 120} {x - 6 + (960 - x) * .6:.0f},{y + 200}', 'chain', 2, .7), E(x, y, 34, 42, col), E(x - 10, y - 14, 8, 12, '#ffffff', .5), poly([(x - 6, y + 46), (x + 6, y + 46), (x, y + 38)], col)]
    s.layer('balloons', bb, 'rise', 1.1, loop='bob')
    return s


# ============ s085 医院候诊厅 ============
def hospital():
    s = Scene('s085', '医院候诊厅', '社会日常', ['健康', '就医常识', '生活技能', '卫生'],
              dict(wall1='#EEF6FB', wall2='#DCEAF4', band='#8CCFCB', band2='#6DBDB8', ceil='#FFFFFF', panel='#F7FBFF', glow='#FFFFFF', floor1='#E9EFF3', floor2='#CFDAE2',
                   desk='#FFFFFF', desk2='#5BB5B0', desk3='#3E9A95', cross='#E8574A', chair='#6FA8DC', chair2='#4F8BC4', metal='#9AA8B6',
                   screen='#1F2A36', led='#FF6B5A', led2='#7CF2C8', leaf='#5FAE74', leaf2='#8FD39A', pot='#F2C9A0', glass='#CFEFF5', poster='#FFFFFF', p1='#F7C55E', p2='#F28B8B', water='#9AD7F5'),
              desc='干净明亮的医院候诊厅：红十字标识、叫号屏、白色导诊台，左侧蓝色候诊椅，右侧取药窗口与饮水机。',
              stand={'ground_y': 910, 'x': [600, 1300]})
    s.layer('wall', [R(0, 0, W, 800, s.lg([(0, 'wall1'), (1, 'wall2')])), R(0, 0, W, 56, 'ceil'), R(0, 560, W, 240, 'band', 0, .35), R(0, 556, W, 8, 'band2', 0, .6)], 'fade', 0)
    s.layer('ceiling_lights', lights_strip(18, (260, 720, 1200, 1660), 'panel', 'glow'), 'fade', .15, loop='glow')
    fl = [R(0, 800, W, 280, s.lg([(0, 'floor1'), (1, 'floor2')]))]
    for x in range(0, W, 120): fl.append(R(x, 800, 2, 280, 'floor2', 0, .8))
    for y in (850, 920, 1000): fl.append(R(0, y, W, 2, 'floor2', 0, .8))
    fl += [E(960, 860, 600, 30, '#ffffff', .5, 'filter="url(#b20)"'), R(0, 800, W, 12, 'band2', 0, .5)]
    s.layer('floor', fl, 'rise', .1)
    # 红十字 + 叫号屏
    lg = [C(960, 150, 64, '#ffffff', extra='filter="url(#sh)"'), R(938, 108, 44, 84, 'cross', 8), R(918, 128, 84, 44, 'cross', 8)]
    s.layer('cross_logo', lg, 'pop', .3)
    sc = [R(700, 240, 520, 150, 'screen', 18, extra='filter="url(#sh)"'), R(716, 256, 488, 118, '#2A3A4A', 10)]
    sc += [T(820, 344, 'A', 78, 'led', 900), T(960, 344, '026', 78, 'led', 900), R(1090, 280, 90, 20, 'led2', 6, .8), R(1090, 312, 70, 16, 'led2', 6, .5), R(1090, 338, 80, 16, 'led2', 6, .5)]
    s.layer('queue_screen', sc, 'drop', .45)
    s.layer('screen_glow', [R(720, 260, 480, 110, 'led', 0, .14, 'filter="url(#b20)"')], 'fade', 1.0, loop='glow')
    # 导诊台
    dk = [shadow(960, 800, 380), R(600, 600, 720, 200, 'desk', 30, extra='filter="url(#sh)"'), R(600, 600, 720, 26, 'desk2', 13), R(640, 680, 640, 10, 'band', 5, .6),
          R(660, 560, 120, 40, 'screen', 6), R(706, 600, 28, 8, 'metal', 3), R(1120, 572, 110, 30, 'poster', 6), R(1130, 562, 90, 12, 'p1', 4)]
    dk += [C(960, 730, 34, 'desk2'), R(952, 712, 16, 36, '#ffffff', 3), R(942, 722, 36, 16, '#ffffff', 3)]
    s.layer('desk', dk, 'rise', .3)
    # 候诊椅（左）
    ch = [shadow(300, 905, 270)]
    for k in range(4):
        x = 90 + k * 110
        ch += [R(x, 720, 96, 110, 'chair', 22, extra='filter="url(#shs)"'), R(x - 4, 812, 104, 34, 'chair2', 14)]
    ch += [R(70, 846, 460, 12, 'metal', 6), R(100, 856, 12, 50, 'metal', 4), R(490, 856, 12, 50, 'metal', 4)]
    for k in range(3):
        x = 140 + k * 140
        ch.append(R(x, 300, 0.1, 0.1, 'metal'))
    s.layer('chairs', ch, 'slide-l', .55)
    # 墙上海报（健康图形，无字）
    po = [R(110, 210, 180, 240, 'poster', 10, extra='filter="url(#shs)"'), C(200, 290, 52, 'p2', .35), P('M200,320 C160,290 160,250 200,268 C240,250 240,290 200,320Z', 'p2'),
          R(140, 370, 120, 10, 'band', 5), R(140, 392, 90, 10, 'metal', 5, .6), R(140, 414, 104, 10, 'metal', 5, .6),
          R(330, 250, 160, 200, 'poster', 10, extra='filter="url(#shs)"'), C(410, 320, 40, 'p1', .4), R(380, 300, 60, 40, 'p1', 12), R(404, 340, 12, 30, 'p1'),
          R(360, 390, 100, 10, 'band', 5), R(360, 412, 70, 10, 'metal', 5, .6)]
    s.layer('posters', po, 'pop', .5)
    # 取药窗口 + 饮水机（右）
    ph = [R(1430, 300, 420, 320, 'desk', 16, extra='filter="url(#sh)"'), R(1450, 320, 380, 230, 'glass', 10, .9), R(1636, 320, 8, 230, 'desk'),
          R(1470, 340, 150, 14, '#ffffff', 7, .7), R(1660, 340, 150, 14, '#ffffff', 7, .7), R(1420, 560, 440, 40, 'desk2', 10), R(1430, 600, 420, 180, 'desk', 0),
          R(1440, 790, 400, 10, 'band2', 0, .4)]
    # 药架剪影
    for k in range(3):
        y = 420 + k * 44; ph.append(R(1470, y + 30, 340, 6, 'band2', 3, .5))
        for j in range(8): ph.append(R(1480 + j * 42, y + (j % 2) * 6, 28, 30 - (j % 2) * 6, ['p1', 'p2', 'band', 'chair'][(j + k) % 4], 5, .6))
    ph += [C(1640, 650, 34, 'cross', .9), R(1633, 632, 14, 36, '#ffffff', 3), R(1622, 643, 36, 14, '#ffffff', 3)]
    s.layer('pharmacy', ph, 'slide-r', .6)
    wd = [shadow(1350, 905, 60), R(1300, 720, 100, 186, 'desk', 14, extra='filter="url(#shs)"'), R(1312, 600, 76, 124, 'water', 30, .85), R(1320, 616, 60, 10, '#ffffff', 5, .6),
          R(1316, 760, 30, 22, 'cross', 6), R(1354, 760, 30, 22, 'chair', 6), R(1318, 800, 64, 8, 'metal', 4)]
    s.layer('water', wd, 'pop', .8)
    s.layer('plant', [leafy(1830, 905, 1.2, 'leaf', 'leaf2', 'pot', 9), leafy(560, 905, .8, 'leaf', 'leaf2', 'pot')], 'grow', .9, loop='sway')
    return s


# ============ s086 快递驿站 ============
def parcel():
    s = Scene('s086', '快递驿站', '社会日常', ['劳动', '社会生活', '数学', '分类整理'],
              dict(wall1='#FFF2E0', wall2='#F7DEBE', ceil='#F28B3E', ceil2='#D9702A', floor1='#E7DCCB', floor2='#CDBDA6', box1='#E3B47E', box2='#C98F55', box3='#F0CC9A', tape='#F6E6C8',
                   label='#FFFFFF', code='#3A3F47', rack='#5E6B7A', rack2='#7C8A96', locker='#3D8FD1', locker2='#2F74B0', door='#62ABE6', door2='#86C2EF', screen='#1F2A36', screen2='#8EEAD0',
                   counter='#F28B3E', counter2='#D9702A', top='#FFF7EC', green='#5FB37A', white='#FFFFFF', lamp='#FFF3C4'),
              desc='社区快递驿站：左侧货架堆满大小包裹，中间取件柜台与扫码枪，右侧蓝色智能快递柜，前景手推车。',
              stand={'ground_y': 920, 'x': [600, 1300]})
    s.layer('wall', [R(0, 0, W, 800, s.lg([(0, 'wall1'), (1, 'wall2')])), R(0, 0, W, 70, 'ceil'), R(0, 66, W, 10, 'ceil2')] +
            [R(x, 76, 3, 724, 'wall2', 0, .7) for x in range(80, W, 160)], 'fade', 0)
    fl = [R(0, 800, W, 280, s.lg([(0, 'floor1'), (1, 'floor2')]))]
    for x in range(0, W, 200): fl.append(R(x, 800, 2, 280, 'floor2', 0, .6))
    fl += [R(0, 900, W, 3, 'floor2', 0, .6), R(560, 1000, 800, 14, 'counter', 7, .0)]
    s.layer('floor', fl, 'rise', .1)
    # 顶部招牌：包裹图标
    sg = [R(760, 110, 400, 110, 'counter', 26, extra='filter="url(#sh)"'), R(776, 126, 368, 78, 'counter2', 18, .4), C(960, 165, 44, 'white')]
    sg += [P('M932,152 L960,138 L988,152 L960,166Z', 'box3'), P('M932,152 L960,166 L960,196 L932,182Z', 'box1'), P('M988,152 L960,166 L960,196 L988,182Z', 'box2'), P('M946,145 L974,159 L974,166 L946,152Z', 'tape')]
    for k in range(3): sg += [R(820 + k * 30, 150 + k * 0, 18, 30, 'white', 4, .0)]
    sg += [C(830, 165, 8, 'white', .7), C(1090, 165, 8, 'white', .7)]
    s.layer('sign', sg, 'drop', .3)

    def box(x, y, w, h, col='box1', lab=True, tilt=0):
        it = [R(x, y - h, w, h, col, 4), R(x, y - h, w, h * .16, 'box2', 3, .5), R(x + w * .42, y - h, w * .16, h * .5, 'tape', 0, .9)]
        if lab and w > 46:
            it += [R(x + w * .12, y - h * .55, w * .34, h * .3, 'label', 3)]
            for q in range(5): it.append(R(x + w * .15 + q * w * .055, y - h * .5, max(2, w * .025), h * .14, 'code'))
        return G(it, f'transform="rotate({tilt} {x + w / 2} {y})"' if tilt else '')
    # 货架（左）
    rk = [shadow(300, 905, 270)]
    for x in (60, 290, 520): rk.append(R(x, 280, 16, 626, 'rack', 4))
    random.seed(31)
    for lv, y in enumerate((420, 580, 740, 890)):
        rk.append(R(48, y, 500, 14, 'rack2', 4, extra='filter="url(#shs)"'))
        x = 82
        while x < 520:
            w = random.randint(56, 110); h = random.randint(60, 120 if lv < 3 else 110)
            if x + w > 530: break
            if lv == 0: h = min(h, 128)
            rk.append(box(x, y, w, h, random.choice(['box1', 'box3', 'box1', 'box2'])))
            if random.random() < .35 and w > 70: rk.append(box(x + 10, y - h, w - 24, random.randint(30, 50), 'box3', False))
            x += w + 6
            if x < 300 and x > 270: x = 310
    s.layer('rack', rk, 'slide-l', .45)
    # 取件柜台（中）
    ct = [shadow(960, 905, 330), R(660, 680, 600, 224, 'counter', 18, extra='filter="url(#sh)"'), R(640, 664, 640, 30, 'top', 12, extra='filter="url(#shs)"'),
          R(700, 740, 520, 12, 'white', 6, .3), R(700, 860, 520, 12, 'counter2', 6, .5)]
    ct += [R(1080, 560, 150, 104, 'screen', 12), R(1092, 572, 126, 80, 'screen2', 6, .85), R(1146, 664, 20, 4, 'rack'), R(1100, 586, 70, 8, 'white', 4, .8), R(1100, 602, 100, 6, 'white', 3, .6), R(1100, 616, 80, 6, 'white', 3, .6)]
    # 扫码枪
    ct += [P('M760,640 L820,620 L830,640 L790,656Z', 'code'), R(770, 640, 22, 30, 'code', 6, extra='transform="rotate(-12 780 655)"'), P('M820,620 L840,610 L846,632 L830,640Z', 'screen2', .9)]
    ct += [box(860, 664, 120, 70, 'box3'), box(990, 664, 70, 46, 'box1', False)]
    s.layer('counter', ct, 'rise', .3)
    s.layer('scan_beam', [P('M846,620 L940,600 L940,640Z', '#FF5B4A', .35), S('M846,622 L938,618', '#FF5B4A', 2, .8)], 'fade', 1.0, loop='glow')
    # 智能快递柜（右）
    lx0, ly0, lw, lh = 1360, 300, 500, 606
    lk = [shadow(1610, 905, 270), R(lx0, ly0, lw, lh, 'locker', 16, extra='filter="url(#sh)"'), R(lx0, ly0, lw, 26, 'locker2', 12)]
    cols = [(lx0 + 16, 140), (lx0 + 164, 160), (lx0 + 332, 152)]
    for ci, (x, w) in enumerate(cols):
        y = ly0 + 40
        sizes = [[90, 90, 130, 90, 190], [60, 60, 60, 60, 80, 120, 120], [120, 70, 70, 120, 160]][ci]
        for k, h in enumerate(sizes):
            if ci == 1 and 2 <= k <= 3:
                if k == 2:
                    lk += [R(x, y, w, 128, 'screen', 8), R(x + 12, y + 12, w - 24, 72, 'screen2', 4, .85), R(x + 20, y + 96, w - 40, 22, 'rack2', 4)]
                y += 64; continue
            lk += [R(x, y, w, h - 8, 'door', 6), R(x, y, w, (h - 8) * .4, 'door2', 6, .35), R(x + w - 26, y + (h - 8) / 2 - 10, 8, 20, 'locker2', 3), C(x + 18, y + 16, 4, 'green' if (k + ci) % 3 else '#F2C14E')]
            y += h
    lk += [R(lx0 + 8, ly0 + lh - 20, lw - 16, 14, 'locker2', 4)]
    s.layer('lockers', lk, 'slide-r', .55)
    s.layer('locker_lights', [C(lx0 + 34, ly0 + 56, 10, 'green', .5, 'filter="url(#b6)"'), C(lx0 + 182, ly0 + 56, 10, 'green', .5, 'filter="url(#b6)"'), C(lx0 + 350, ly0 + 56, 10, 'green', .5, 'filter="url(#b6)"')], 'fade', 1.1, loop='twinkle')
    # 手推车（前景）
    hx = 1420
    ht = [shadow(hx + 20, 1000, 120), S(f'M{hx - 70},700 L{hx - 70},986 L{hx + 120},986', 'rack', 12), S(f'M{hx - 90},700 L{hx - 50},700', 'counter2', 14),
          C(hx - 40, 994, 22, 'code'), C(hx + 90, 994, 22, 'code'), C(hx - 40, 994, 8, 'rack2'), C(hx + 90, 994, 8, 'rack2'),
          box(hx - 60, 980, 170, 110, 'box1'), box(hx - 46, 870, 140, 84, 'box3'), box(hx - 30, 786, 100, 62, 'box1', False)]
    s.layer('trolley', ht, 'slide-r', .8)
    # 吊灯
    lp = []
    for x in (520, 1400):
        lp += [S(f'M{x},76 L{x},150', 'rack', 3), P(f'M{x - 46},190 Q{x},120 {x + 46},190Z', 'counter2'), E(x, 192, 46, 8, 'lamp'), C(x, 200, 60, 'lamp', .45, 'filter="url(#b20)"')]
    s.layer('lamps', lp, 'drop', .9, loop='glow')
    # 地上小包裹堆（左前）
    s.layer('floor_boxes', [shadow(640, 912, 90), box(560, 910, 120, 90, 'box3'), box(690, 910, 70, 56, 'box2', False), box(585, 820, 80, 50, 'box1', False)], 'pop', .95)
    return s


# ============ s087 银行柜台 ============
def bank():
    s = Scene('s087', '银行柜台', '社会日常', ['数学', '认识人民币', '理财', '社会生活'],
              dict(wall1='#F5F0E8', wall2='#E8DFD0', navy='#26496E', navy2='#1B3754', gold='#D9AE5F', gold2='#B98C3E', glass='#D6EAF4', marble1='#F6F3EE', marble2='#DDD5C8', vein='#CFC6B8',
                   counter='#FFFFFF', counter2='#EDE7DD', wood='#B88457', wood2='#94643C', screen='#16263A', led='#FFC765', led2='#8FD8F2', leaf='#4E9E6A', leaf2='#86C79A', pot='#F2EEE6',
                   belt='#26496E', post='#C9A25A', atm='#E9EDF1', atm2='#C9D2DA', lamp='#FFF0C8', sofa='#7FA7C9'),
              desc='沉稳雅致的银行大厅：藏青与金色的墙面，三个带玻璃隔板的编号柜台窗口，左侧 ATM 机与排队隔离带，右侧取号机与绿植。',
              stand={'ground_y': 920, 'x': [560, 1360]})
    s.layer('wall', [R(0, 0, W, 800, s.lg([(0, 'wall1'), (1, 'wall2')])), R(0, 0, W, 240, s.lg([(0, 'navy'), (1, 'navy2')])), R(0, 236, W, 10, 'gold')] +
            [R(x, 246, 4, 554, 'wall2', 0, .9) for x in range(100, W, 200)], 'fade', 0)
    # 金色徽标（古钱币造型，无字）
    lg = [C(960, 120, 70, 'gold', extra='filter="url(#sh)"'), C(960, 120, 56, 'gold2'), C(960, 120, 48, 'gold'), R(940, 100, 40, 40, 'navy', 4)]
    for k in range(8):
        a = k * math.pi / 4; lg.append(C(960 + 62 * math.cos(a), 120 + 62 * math.sin(a), 3, 'navy2', .6))
    lg += [R(620, 116, 240, 6, 'gold', 3, .7), R(1060, 116, 240, 6, 'gold', 3, .7)]
    s.layer('logo', lg, 'pop', .3)
    s.layer('logo_glint', [C(930, 90, 8, '#ffffff', .9), C(990, 150, 5, '#ffffff', .8)], 'fade', 1.2, loop='twinkle')
    # 汇率屏（左上，色块）
    rs = [R(90, 280, 330, 180, 'screen', 14, extra='filter="url(#sh)"')]
    for k in range(5):
        y = 300 + k * 30; rs += [R(112, y, 56, 16, 'led2', 4, .8), R(196, y, 90, 16, 'led', 4, .9), R(306, y, 92, 16, 'led', 4, .6)]
    s.layer('rate_board', rs, 'drop', .4, loop='glow')
    # 柜台窗口 ×3
    ct = [shadow(960, 800, 480), R(520, 640, 880, 160, 'counter', 0, extra='filter="url(#sh)"'), R(500, 620, 920, 30, 'counter2', 10, extra='filter="url(#shs)"'),
          R(520, 700, 880, 8, 'gold', 0, .8), R(520, 790, 880, 10, 'wood2', 0, .4)]
    for k in range(3):
        x = 540 + k * 290
        ct += [R(x, 330, 260, 290, 'glass', 8, .85), R(x, 330, 260, 290, 'none'), R(x + 20, 350, 50, 260, '#ffffff', 6, .35), R(x + 90, 350, 20, 260, '#ffffff', 6, .25),
               R(x + 80, 590, 100, 30, 'counter', 6), R(x + 90, 596, 80, 12, 'atm2', 4), R(x - 2, 316, 264, 16, 'navy', 6),
               C(x + 130, 290, 26, 'navy', extra='filter="url(#shs)"'), C(x + 130, 290, 22, 'gold'), T(x + 130, 301, str(k + 1), 30, 'navy2', 900),
               R(x + 40, 740, 180, 40, 'wood', 6, .25)]
    for x in (530, 820, 1110, 1400): ct.append(R(x - 10, 316, 20, 310, 'wood', 6))
    s.layer('counters', ct, 'rise', .35)
    s.layer('glass_shine', [P(f'M{x + 150},330 L{x + 200},330 L{x + 120},620 L{x + 70},620Z', '#ffffff', .25) for x in (540, 830, 1120)], 'fade', 1.0, loop='glow')
    # 地面（大理石）
    fl = [R(0, 800, W, 280, s.lg([(0, 'marble1'), (1, 'marble2')]))]
    for x in range(-200, W, 240): fl.append(P(f'M{x},800 L{x + 2},800 L{x - 120},1080 L{x - 122},1080Z', 'vein', .7))
    fl += [S('M120,880 q80,20 160,-10 t180,20', 'vein', 2, .8), S('M1400,960 q60,-20 140,10 t160,-10', 'vein', 2, .8), R(0, 800, W, 10, 'gold', 0, .5),
           E(960, 880, 560, 40, '#ffffff', .5, 'filter="url(#b20)"')]
    s.layer('floor', fl, 'rise', .1)
    # ATM（左）
    ax = 250
    at = [shadow(ax, 905, 130), R(ax - 110, 500, 220, 406, 'atm', 18, extra='filter="url(#sh)"'), R(ax - 110, 500, 220, 50, 'navy', 18), R(ax - 110, 530, 220, 20, 'navy'),
          R(ax - 80, 560, 160, 110, 'screen', 10), R(ax - 68, 572, 136, 86, 'led2', 6, .8), R(ax - 56, 586, 80, 10, '#ffffff', 5, .8), R(ax - 56, 606, 110, 8, '#ffffff', 4, .5),
          R(ax - 120, 690, 240, 26, 'atm2', 8), R(ax + 40, 724, 50, 8, 'screen', 4), R(ax - 60, 760, 120, 10, 'screen', 5)]
    for k in range(12): at.append(R(ax - 84 + (k % 3) * 28, 726 + (k // 3) * 0 + (k // 3) * 0, 0.1, 0.1, 'atm2'))
    for r_ in range(4):
        for q in range(3): at.append(R(ax - 86 + q * 30, 724 + r_ * 0 - 20 + 0, 0.1, 0.1, 'atm2'))
    at += [R(ax - 90, 726, 100, 0.1, 'atm2')]
    kp = []
    for r_ in range(3):
        for q in range(3): kp.append(R(ax - 86 + q * 28, 700 + r_ * 0 - 6, 22, 0.1, 'atm2'))
    at += [R(ax - 70, 790, 140, 100, 'atm2', 8, .5)]
    s.layer('atm', at, 'slide-l', .5)
    # 排队隔离带
    qb = []
    for x in (430, 620):
        qb += [shadow(x, 905, 34), R(x - 6, 790, 12, 114, 'post', 5), C(x, 788, 12, 'post'), E(x, 902, 30, 8, 'post')]
    qb += [P('M436,800 Q525,822 614,800 L614,818 Q525,840 436,818Z', 'belt')]
    s.layer('queue_belt', qb, 'rise', .7)
    # 取号机 + 绿植（右）
    kx = 1600
    kk = [shadow(kx, 905, 70), R(kx - 60, 560, 120, 346, 'atm', 22, extra='filter="url(#sh)"'), R(kx - 46, 586, 92, 120, 'screen', 8), R(kx - 38, 594, 76, 104, 'led2', 6, .75),
          R(kx - 24, 610, 48, 30, '#ffffff', 6, .85), R(kx - 24, 652, 48, 30, '#ffffff', 6, .6), R(kx - 30, 730, 60, 8, 'screen', 4), R(kx - 22, 736, 44, 30, '#ffffff', 2)]
    kk += [leafy(1800, 905, 1.25, 'leaf', 'leaf2', 'pot', 9)]
    s.layer('kiosk_plant', kk, 'slide-r', .6)
    # 吊灯
    lp = []
    for x in (380, 960, 1540):
        lp += [S(f'M{x},246 L{x},260', 'gold2', 2)]
    for x in (1640,):
        lp += [S(f'M{x},246 L{x},330', 'gold2', 3), E(x, 340, 60, 16, 'gold'), E(x, 350, 50, 8, 'lamp'), C(x, 360, 80, 'lamp', .4, 'filter="url(#b20)"')]
    s.layer('lamps', lp, 'drop', .85, loop='glow')
    return s


# ============ s088 垃圾分类站 ============
def sorting():
    s = Scene('s088', '垃圾分类站', '社会日常', ['道德与法治', '环保', '劳动', '科学'],
              dict(sky1='#A8DCF2', sky2='#F2FAF2', b1='#F1E2CF', b2='#D8E7F0', win='#FFFFFF', far='#B7DDB0', tree='#5FAE74', tree2='#A1D893', trunk='#8A5A3A',
                   pave1='#ECE5D8', pave2='#D9CFBE', grass='#9ED37E', canopy='#5FA36A', canopy2='#4B8A56', wall='#E6F2E2', post='#6E7F74',
                   blue='#2F7BC8', blue2='#2466A8', red='#E2483C', red2='#BF3A30', green='#3FA65A', green2='#318A49', gray='#5D6670', gray2='#4A525B', icon='#FFFFFF',
                   sink='#E9EEF2', sink2='#BFC9D2', water='#8FD3F5', leaf='#4E9E5A', sun='#FFE7A3', bag='#F7C55E'),
              desc='小区垃圾分类亭：绿色顶棚下蓝、红、绿、灰四色分类桶（可回收物、有害垃圾、厨余垃圾、其他垃圾）带图标，旁边洗手池和绿树。',
              stand={'ground_y': 910, 'x': [480, 1440]})
    s.layer('sky', [R(0, 0, W, 760, s.lg([(0, 'sky1'), (1, 'sky2')])), C(1700, 140, 150, 'sun', .45, 'filter="url(#b40)"'), C(1700, 140, 58, 'sun')], 'fade', 0)
    s.layer('clouds', [cloud(260, 150, .7, op=.95), cloud(1200, 120, .55, op=.85)], 'slide-l', .2, loop='drift')
    bl = []
    for x, w, h, col in [(0, 260, 420, 'b2'), (280, 220, 340, 'b1'), (1400, 240, 380, 'b1'), (1660, 260, 440, 'b2')]:
        top = 680 - h; bl += [R(x, top, w, h, col, 10)]
        for wy in range(top + 30, 640, 52):
            for wx in range(x + 24, x + w - 40, 54): bl += [R(wx, wy, 30, 32, 'win', 4, .8), R(wx - 4, wy + 30, 38, 6, col, 2, .0)]
    s.layer('buildings', [G(bl, 'opacity=".9"'), R(0, 520, W, 180, s.lg([(0, 'sky2', 0), (1, 'sky2', .8)]))], 'rise', .25)
    s.layer('trees', [P(smooth(hills(700, 40, 2, 120), 760), 'far')] + [blob_tree(x, 730, sc, 'tree', 'tree2', 'trunk') for x, sc in [(120, .8), (520, .75), (1380, .7), (1560, .9), (1820, .85)]], 'grow', .4, loop='sway')
    gd = [R(0, 730, W, 350, s.lg([(0, 'pave1'), (1, 'pave2')])), R(0, 726, W, 10, 'grass')]
    for y in (790, 860, 950):
        off = (y // 10) % 2 * 60
        gd.append(R(0, y, W, 2, 'pave2'))
        for x in range(-off, W, 120): gd.append(R(x, y - (70 if y > 790 else 60), 2, 70 if y > 790 else 60, 'pave2', 0, .8))
    s.layer('ground', gd, 'rise', .1)
    # 分类亭
    k0, k1 = 520, 1400
    kb = [shadow(960, 830, 470), R(k0 + 10, 360, 860, 460, 'wall', 14), R(k0 + 10, 360, 860, 460, s.lg([(0, '#ffffff', .4), (1, '#ffffff', 0)])),
          R(k0, 330, 18, 500, 'post', 6), R(k1 - 18, 330, 18, 500, 'post', 6),
          P(f'M{k0 - 70},350 L{k0 + 40},260 L{k1 - 40},260 L{k1 + 70},350Z', 'canopy', extra='filter="url(#sh)"'), R(k0 - 70, 344, k1 - k0 + 140, 26, 'canopy2', 8)]
    for k in range(10):
        x = k0 - 60 + k * (k1 - k0 + 120) / 10; kb.append(P(f'M{x},370 L{x + (k1 - k0 + 120) / 10},370 Q{x + (k1 - k0 + 120) / 20},392 {x},370Z', 'canopy2'))
    # 顶棚中央循环标志
    kb += [C(960, 304, 32, '#ffffff', .95)]
    for k in range(3):
        a = k * 2 * math.pi / 3 - math.pi / 2
        x1, y1 = 960 + 18 * math.cos(a), 304 + 18 * math.sin(a); x2, y2 = 960 + 18 * math.cos(a + 1.6), 304 + 18 * math.sin(a + 1.6)
        kb += [S(f'M{x1:.1f},{y1:.1f} A18,18 0 0,1 {x2:.1f},{y2:.1f}', 'green', 6, cap='butt')]
        ax_, ay_ = 960 + 18 * math.cos(a + 1.75), 304 + 18 * math.sin(a + 1.75); tx, ty = -math.sin(a + 1.75), math.cos(a + 1.75)
        kb.append(poly([(ax_ + tx * 9, ay_ + ty * 9), (ax_ - 9 * math.cos(a + 1.75) - tx * 2, ay_ - 9 * math.sin(a + 1.75) - ty * 2), (ax_ + 9 * math.cos(a + 1.75) - tx * 2, ay_ + 9 * math.sin(a + 1.75) - ty * 2)], 'green'))
    s.layer('kiosk', kb, 'drop', .35)

    # 四个分类桶
    def bin_(x, col, col2, icon):
        y = 820; w = 170; h = 260
        it = [shadow(x, y, 100), P(f'M{x - w / 2 + 8},{y - h} L{x + w / 2 - 8},{y - h} L{x + w / 2 - 18},{y} L{x - w / 2 + 18},{y}Z', col, extra='filter="url(#shs)"'),
              R(x - w / 2, y - h - 34, w, 40, col2, 12), R(x - 30, y - h - 46, 60, 16, col2, 6), R(x - w / 2 + 20, y - h + 20, 12, h - 50, '#ffffff', 6, .2),
              C(x, y - h * .52, 48, 'icon'), C(x - 46, y + 2, 14, 'gray2'), C(x + 46, y + 2, 14, 'gray2')]
        cy = y - h * .52
        if icon == 'recycle':
            for k in range(3):
                a = k * 2 * math.pi / 3 - math.pi / 2
                x1, y1 = x + 26 * math.cos(a), cy + 26 * math.sin(a); x2, y2 = x + 26 * math.cos(a + 1.55), cy + 26 * math.sin(a + 1.55)
                it.append(S(f'M{x1:.1f},{y1:.1f} A26,26 0 0,1 {x2:.1f},{y2:.1f}', col, 8, cap='butt'))
                b = a + 1.7; px, py = x + 26 * math.cos(b), cy + 26 * math.sin(b); tx, ty = -math.sin(b), math.cos(b)
                it.append(poly([(px + tx * 12, py + ty * 12), (px - 11 * math.cos(b), py - 11 * math.sin(b)), (px + 11 * math.cos(b), py + 11 * math.sin(b))], col))
        elif icon == 'battery':
            it += [R(x - 15, cy - 26, 30, 52, col, 6), R(x - 7, cy - 32, 14, 8, col, 2), R(x - 9, cy - 18, 18, 12, 'icon', 2, .9), P(f'M{x + 3},{cy - 4} L{x - 7},{cy + 10} L{x + 1},{cy + 10} L{x - 4},{cy + 22} L{x + 9},{cy + 4} L{x + 1},{cy + 4}Z', 'icon')]
        elif icon == 'food':
            it += [P(f'M{x - 30},{cy} L{x + 8},{cy - 16} L{x + 8},{cy + 16}Z', col), E(x - 6, cy, 18, 12, col), poly([(x + 6, cy), (x + 26, cy - 14), (x + 26, cy + 14)], col),
                   C(x - 16, cy - 2, 3, 'icon'), S(f'M{x - 4},{cy - 8} L{x - 4},{cy + 8} M{x + 4},{cy - 8} L{x + 4},{cy + 8}', 'icon', 2, .8)]
        else:
            it += [P(f'M{x - 18},{cy - 18} L{x + 18},{cy - 18} L{x + 14},{cy + 24} L{x - 14},{cy + 24}Z', col), R(x - 22, cy - 26, 44, 8, col, 3), S(f'M{x - 6},{cy - 10} L{x - 5},{cy + 16} M{x + 6},{cy - 10} L{x + 5},{cy + 16}', 'icon', 3)]
        return G(it)
    s.layer('bins', [bin_(640, 'blue', 'blue2', 'recycle'), bin_(853, 'red', 'red2', 'battery'), bin_(1066, 'green', 'green2', 'food'), bin_(1279, 'gray', 'gray2', 'other')], 'pop', .55)
    # 洗手池（左）
    sx = 270
    sk = [shadow(sx, 905, 140), R(sx - 120, 700, 240, 206, 'sink', 14, extra='filter="url(#sh)"'), R(sx - 130, 680, 260, 30, 'sink2', 10), E(sx, 690, 90, 10, 'water', .8),
          S(f'M{sx},680 L{sx},610 Q{sx},590 {sx + 30},590 L{sx + 40},600', 'sink2', 12), R(sx - 90, 740, 180, 140, 'sink2', 10, .4),
          R(sx + 140, 590, 60, 100, 'green', 10, extra='filter="url(#shs)"'), R(sx + 156, 570, 28, 24, 'green2', 4), C(sx + 170, 630, 14, '#ffffff', .8)]
    s.layer('sink', sk, 'slide-l', .7)
    s.layer('drip', [E(sx + 40, 620, 6, 9, 'water'), E(sx + 40, 650, 4, 6, 'water', .7)], 'fade', 1.1, loop='flow')
    # 右侧：扎好的可回收纸箱和瓶子
    rc = [shadow(1640, 905, 160), R(1540, 780, 150, 120, '#E3B47E', 6), R(1540, 780, 150, 20, '#C98F55', 4), S('M1615,780 L1615,900 M1540,840 L1690,840', '#F6E6C8', 6),
          R(1700, 760, 50, 140, 'water', 14, .8), R(1714, 740, 22, 24, 'blue', 4), R(1760, 790, 44, 110, 'green', 12, .7), R(1772, 772, 20, 22, 'green2', 4),
          P('M1560,780 Q1600,720 1650,780Z', 'bag', .0)]
    s.layer('recyclables', rc, 'pop', .85)
    s.layer('butterflies', [G([E(1460, 560, 14, 9, 'bag', extra='transform="rotate(-30 1460 560)"'), E(1474, 560, 14, 9, 'bag', extra='transform="rotate(30 1474 560)"')]),
                            G([E(430, 520, 12, 8, 'red', .8, extra='transform="rotate(-30 430 520)"'), E(442, 520, 12, 8, 'red', .8, extra='transform="rotate(30 442 520)"')])], 'fade', 1.2, loop='bob')
    return s


# ============ s089 志愿服务站 ============
def volunteer():
    s = Scene('s089', '志愿服务站', '社会日常', ['道德与法治', '志愿服务', '社区', '品德'],
              dict(sky1='#9ED6F4', sky2='#FFF3E2', sun='#FFE08A', far='#C4E3B4', tree='#5FAE74', tree2='#A1D893', trunk='#8A5A3A', b1='#F5DCCB', win='#FFFFFF',
                   plaza1='#F1E5D2', plaza2='#DDCBB0', tent='#E8574A', tent2='#FFFFFF', tent3='#C8453A', pole='#B9C2CC', table='#3FA0D6', table2='#2F80B8', cloth='#FFFFFF',
                   heart='#E8574A', heart2='#FF8A80', box='#F7C55E', box2='#E0A93A', kit='#FFFFFF', water='#8FD3F5', water2='#4FB0E0', paper='#FFFDF6',
                   bal1='#F2836B', bal2='#F7C55E', bal3='#5FB7E0', bal4='#8ED081', chair='#F2B33D', board='#FFFFFF', board2='#D9A86A'),
              desc='社区广场上的志愿服务站：红白条纹帐篷挂着爱心标志，桌上有饮用水、医药箱和爱心捐赠箱，旁边留言板与彩色气球。',
              stand={'ground_y': 910, 'x': [560, 1360]})
    s.layer('sky', [R(0, 0, W, 760, s.lg([(0, 'sky1'), (1, 'sky2')])), C(260, 160, 160, 'sun', .4, 'filter="url(#b40)"'), C(260, 160, 62, 'sun')], 'fade', 0)
    s.layer('clouds', [cloud(800, 130, .7, op=.95), cloud(1600, 170, .6, op=.85)], 'slide-l', .2, loop='drift')
    bl = []
    for x, w, h in [(0, 300, 260), (1580, 340, 300), (320, 180, 200), (1400, 180, 220)]:
        top = 660 - h; bl.append(R(x, top, w, h, 'b1', 10))
        for wy in range(top + 28, 640, 48):
            for wx in range(x + 22, x + w - 30, 50): bl.append(R(wx, wy, 28, 30, 'win', 4, .8))
    s.layer('buildings', [G(bl, 'opacity=".85"'), R(0, 480, W, 220, s.lg([(0, 'sky2', 0), (1, 'sky2', .85)]))], 'rise', .25)
    s.layer('trees', [P(smooth(hills(690, 40, 6, 120), 760), 'far')] + [blob_tree(x, 720, sc, 'tree', 'tree2', 'trunk') for x, sc in [(60, .85), (230, .7), (1700, .75), (1870, .9)]], 'grow', .35, loop='sway')
    gd = [R(0, 720, W, 360, s.lg([(0, 'plaza1'), (1, 'plaza2')]))]
    for k in range(-6, 7): gd.append(S(f'M{960 + k * 110},720 L{960 + k * 260},1080', 'plaza2', 2, .8))
    for y in (770, 840, 940): gd.append(R(0, y, W, 2, 'plaza2'))
    s.layer('ground', gd, 'rise', .1)
    # 帐篷
    t0, t1, ty = 560, 1360, 360
    tn = [shadow(960, 830, 460), R(t0 + 10, ty, 12, 470, 'pole', 4), R(t1 - 22, ty, 12, 470, 'pole', 4),
          P(f'M{t0 - 40},{ty + 20} L{t0 + 120},{ty - 120} L{t1 - 120},{ty - 120} L{t1 + 40},{ty + 20}Z', 'tent', extra='filter="url(#sh)"')]
    for k in range(8):
        xa = t0 + 120 + k * (t1 - t0 - 240) / 8; xb = t0 - 40 + k * (t1 - t0 + 80) / 8
        if k % 2: tn.append(poly([(xa, ty - 120), (xa + (t1 - t0 - 240) / 8, ty - 120), (xb + (t1 - t0 + 80) / 8, ty + 20), (xb, ty + 20)], 'tent2'))
    tn += [R(t0 - 40, ty + 14, t1 - t0 + 80, 56, 'tent', 6)]
    for k in range(12):
        x = t0 - 40 + k * (t1 - t0 + 80) / 12; w = (t1 - t0 + 80) / 12
        tn.append(P(f'M{x},{ty + 68} L{x + w},{ty + 68} Q{x + w / 2},{ty + 100} {x},{ty + 68}Z', 'tent2' if k % 2 else 'tent'))
    # 帐篷上的爱心徽章
    tn += [C(960, ty + 42, 46, 'tent2', extra='filter="url(#shs)"'), P(f'M960,{ty + 66} C920,{ty + 40} 922,{ty + 12} 946,{ty + 18} C954,{ty + 20} 958,{ty + 26} 960,{ty + 30} C962,{ty + 26} 966,{ty + 20} 974,{ty + 18} C998,{ty + 12} 1000,{ty + 40} 960,{ty + 66}Z', 'heart')]
    tn += [R(t0 + 20, ty + 100, t1 - t0 - 40, 360, 'tent2', 0, .25)]
    s.layer('tent', tn, 'drop', .35)
    # 桌子与物资
    tb = [R(600, 690, 720, 30, 'table', 8, extra='filter="url(#shs)"'), R(610, 716, 700, 120, 'cloth', 6), R(610, 716, 700, 120, 'table', 6, .15),
          P('M930,760 C900,740 902,718 920,722 C926,724 929,728 930,732 C931,728 934,724 940,722 C958,718 960,740 930,760Z', 'heart', .9), R(630, 820, 660, 10, 'table2', 4, .4)]
    for k in range(6):
        x = 640 + k * 30; tb += [R(x, 630, 22, 60, 'water', 6, .9), R(x + 5, 618, 12, 14, 'water2', 3), R(x, 650, 22, 16, '#ffffff', 0, .7)]
    tb += [R(850, 620, 120, 70, 'kit', 10, extra='filter="url(#shs)"'), R(890, 608, 40, 14, 'pole', 6), R(904, 634, 12, 40, 'heart'), R(890, 648, 40, 12, 'heart'),
           R(1010, 600, 130, 90, 'box', 10, extra='filter="url(#shs)"'), R(1010, 600, 130, 18, 'box2', 8), R(1050, 604, 50, 8, 'box2', 4),
           P('M1075,672 C1048,654 1050,632 1066,636 C1070,637 1073,641 1075,645 C1077,641 1080,637 1084,636 C1100,632 1102,654 1075,672Z', 'heart'),
           R(1170, 664, 80, 26, 'paper', 4, extra='transform="rotate(-6 1210 677)"'), R(1180, 650, 80, 26, 'heart2', 4, .7, extra='transform="rotate(4 1220 663)"')]
    s.layer('table', tb, 'rise', .55)
    # 留言板（左）
    bx = 300
    bd = [shadow(bx, 905, 150), R(bx - 8, 640, 16, 266, 'board2', 4), R(bx - 140, 860, 16, 46, 'board2', 4), R(bx + 124, 860, 16, 46, 'board2', 4),
          R(bx - 160, 440, 320, 240, 'board2', 14, extra='filter="url(#sh)"'), R(bx - 144, 456, 288, 208, 'board', 8)]
    for k, (x, y, col, rot) in enumerate([(bx - 110, 480, 'bal2', -6), (bx - 20, 476, 'bal3', 4), (bx + 70, 486, 'heart2', -3), (bx - 100, 570, 'bal4', 5), (bx - 4, 566, 'heart2', -5), (bx + 80, 578, 'bal2', 3)]):
        bd += [R(x - 34, y, 68, 64, col, 4, .85, extra=f'transform="rotate({rot} {x} {y + 32})"'), C(x, y + 6, 5, 'heart')]
        bd.append(P(f'M{x},{y + 48} C{x - 14},{y + 38} {x - 12},{y + 26} {x - 5},{y + 28} C{x - 2},{y + 29} {x},{y + 32} {x},{y + 33} C{x},{y + 32} {x + 2},{y + 29} {x + 5},{y + 28} C{x + 12},{y + 26} {x + 14},{y + 38} {x},{y + 48}Z', 'tent2', .9))
    s.layer('board', bd, 'slide-l', .65)
    # 椅子 + 物资箱（右前）
    rt = [shadow(1580, 905, 160)]
    for x in (1500, 1640):
        rt += [R(x - 46, 740, 92, 60, 'chair', 14), R(x - 50, 800, 100, 22, 'chair', 8, extra='filter="url(#shs)"'), S(f'M{x - 40},822 L{x - 44},904 M{x + 40},822 L{x + 44},904', 'pole', 6)]
    rt += [shadow(1800, 905, 90), R(1720, 800, 160, 104, '#E3B47E', 8), R(1720, 800, 160, 22, '#C98F55', 6), R(1784, 800, 32, 52, '#F6E6C8'),
           R(1740, 740, 120, 62, '#E3B47E', 8), R(1740, 740, 120, 16, '#C98F55', 6)]
    s.layer('chairs_boxes', rt, 'rise', .75)
    # 气球（系在帐篷柱上）
    bb = []
    for x0_, xs in ((t0 + 16, [(-60, 230, 'bal1'), (-10, 196, 'bal2'), (36, 236, 'bal3')]), (t1 - 16, [(-36, 226, 'bal4'), (10, 190, 'bal1'), (60, 232, 'bal2')])):
        for dx, y, col in xs:
            x = x0_ + dx; bb += [S(f'M{x},{y + 44} Q{x + (x0_ - x) * .5},{y + 120} {x0_},{ty + 60}', 'pole', 2), E(x, y, 34, 42, col), E(x - 10, y - 14, 8, 12, '#ffffff', .5), poly([(x - 6, y + 46), (x + 6, y + 46), (x, y + 38)], col)]
    s.layer('balloons', bb, 'rise', 1.0, loop='bob')
    # 彩旗
    bt = [S('M0,40 Q480,110 960,50 Q1440,110 1920,40', 'pole', 3)]
    for k in range(24):
        u = (k + .5) / 24; x = u * 1920; lu = (u * 2) % 1; y = (1 - lu) ** 2 * (40 if u < .5 else 50) + 2 * lu * (1 - lu) * 110 + lu ** 2 * (50 if u < .5 else 40)
        bt.append(poly([(x - 16, y), (x + 16, y), (x, y + 32)], ['bal1', 'bal2', 'bal3', 'bal4'][k % 4]))
    s.layer('bunting', bt, 'drop', 1.1, loop='sway')
    return s


# ============ s090 宠物医院 ============
def vet():
    s = Scene('s090', '宠物医院', '社会日常', ['科学', '生命教育', '爱护动物', '社会生活'],
              dict(wall1='#F1ECFB', wall2='#E2D9F4', paw='#CDBFEE', wains='#8FD3C8', wains2='#6FBFB2', floor1='#F5EDE0', floor2='#E3D4BE',
                   metal='#C9D2DA', metal2='#9AA8B6', cab='#FFFFFF', cab2='#E4E9EE', teal='#4FB3A9', xray='#2B3542', xray2='#BFE9FF', bone='#FFFFFF',
                   carrier='#F2A65A', carrier2='#D9883E', bed='#F28B9A', bed2='#E06A7E', toy='#F7C55E', jar1='#F28B9A', jar2='#7FC4E8', jar3='#F7C55E', jar4='#8ED081',
                   lamp='#FFF3C4', leaf='#5FAE74', leaf2='#8FD39A', pot='#FFFFFF', win1='#A6DCF7', win2='#E8F7FF'),
              desc='温馨的宠物医院诊室：淡紫墙面点缀爪印，墙上看片灯显示小狗骨骼，不锈钢诊疗台与无影灯，药品柜、宠物航空箱和狗窝。',
              stand={'ground_y': 910, 'x': [620, 1300]})

    def pawprint(x, y, sc, col, op=1):
        return G([E(x, y, 16 * sc, 13 * sc, col, op), C(x - 15 * sc, y - 16 * sc, 6 * sc, col, op), C(x - 5 * sc, y - 24 * sc, 6 * sc, col, op), C(x + 6 * sc, y - 24 * sc, 6 * sc, col, op), C(x + 16 * sc, y - 16 * sc, 6 * sc, col, op)])
    bg = [R(0, 0, W, 800, s.lg([(0, 'wall1'), (1, 'wall2')]))]
    random.seed(41)
    for y in range(80, 560, 120):
        for x in range(60 + (y // 120 % 2) * 90, W, 180): bg.append(G([pawprint(x, y, 1, 'paw', .45)], f'transform="rotate({random.randint(-25, 25)} {x} {y})"'))
    bg += [R(0, 580, W, 220, 'wains', 0, .55), R(0, 576, W, 8, 'wains2')]
    s.layer('wall', bg, 'fade', 0)
    fl = [R(0, 800, W, 280, s.lg([(0, 'floor1'), (1, 'floor2')]))]
    for x in range(0, W, 140): fl.append(R(x, 800, 2, 280, 'floor2', 0, .7))
    for y in (860, 940): fl.append(R(0, y, W, 2, 'floor2', 0, .7))
    s.layer('floor', fl, 'rise', .1)
    # 诊所徽标：十字 + 爪印
    lg = [C(960, 120, 62, 'cab', extra='filter="url(#sh)"'), R(938, 76, 44, 88, 'teal', 10), R(916, 98, 88, 44, 'teal', 10), pawprint(960, 132, .9, 'cab')]
    s.layer('logo', lg, 'pop', .3)
    # 窗
    win = [R(1070, 230, 300, 250, 'cab', 14, extra='filter="url(#shs)"'), R(1084, 244, 272, 222, s.lg([(0, 'win1'), (1, 'win2')]), 8)]
    cp = s.clip('<rect x="1084" y="244" width="272" height="222" rx="8"/>')
    win += [G([cloud(1180, 320, .4), C(1140, 500, 90, 'leaf2', .8), C(1300, 520, 100, 'leaf', .7)], f'clip-path="{cp}"'), R(1216, 244, 8, 222, 'cab'), R(1060, 476, 320, 16, 'cab', 6)]
    s.layer('window', win, 'pop', .35)
    # 看片灯（小狗骨骼）
    xr = [R(560, 220, 400, 270, 'metal2', 16, extra='filter="url(#sh)"'), R(576, 236, 368, 238, 'xray', 8), R(576, 236, 368, 238, s.rg([(0, 'xray2', .35), (1, 'xray2', 0)]))]
    bx_, by_ = 760, 360
    xr += [S(f'M{bx_ - 110},{by_} Q{bx_},{by_ - 26} {bx_ + 90},{by_ - 6}', 'bone', 8, .85)]
    for k in range(9):
        x = bx_ - 100 + k * 22; xr.append(S(f'M{x},{by_ - 12 + abs(k - 4) * 1.5} q-6,26 -2,44', 'bone', 5, .65))
    xr += [E(bx_ + 120, by_ - 30, 46, 32, 'bone', .8), E(bx_ + 158, by_ - 16, 26, 14, 'bone', .8), P(f'M{bx_ + 92},{by_ - 54} L{bx_ + 104},{by_ - 90} L{bx_ + 122},{by_ - 56}Z', 'bone', .8),
           C(bx_ + 126, by_ - 36, 7, 'xray'), S(f'M{bx_ - 110},{by_} Q{bx_ - 150},{by_ - 20} {bx_ - 170},{by_ - 60}', 'bone', 5, .7)]
    for lx_ in (bx_ - 80, bx_ - 50, bx_ + 50, bx_ + 80):
        xr.append(S(f'M{lx_},{by_ + 20} L{lx_ + (8 if lx_ < bx_ else -6)},{by_ + 70} L{lx_ + 4},{by_ + 98}', 'bone', 7, .8))
    s.layer('xray', xr, 'drop', .4)
    s.layer('xray_glow', [R(590, 250, 340, 210, 'xray2', 0, .16, 'filter="url(#b20)"')], 'fade', 1.0, loop='glow')
    # 药品柜（右）
    cx = 1480
    cb = [shadow(1660, 905, 220), R(cx, 300, 380, 280, 'cab', 14, extra='filter="url(#sh)"'), R(cx + 14, 314, 352, 252, 'xray2', 8, .35)]
    for lv, y in enumerate((420, 560)):
        cb.append(R(cx + 14, y - 6, 352, 8, 'cab2', 3))
        for j in range(6):
            x = cx + 34 + j * 56; h = 60 + (j * 13 + lv * 7) % 30
            col = ['jar1', 'jar2', 'jar3', 'jar4'][(j + lv) % 4]
            cb += [R(x, y - 6 - h, 38, h, col, 8, .9), R(x + 4, y - 14 - h, 30, 12, 'cab2', 3), R(x + 6, y - 6 - h * .6, 26, h * .26, '#ffffff', 2, .7)]
    cb += [R(cx + 188, 314, 4, 252, 'cab'), R(cx, 600, 380, 306, 'cab', 14, extra='filter="url(#sh)"'), R(cx + 20, 620, 165, 270, 'cab2', 8), R(cx + 195, 620, 165, 270, 'cab2', 8),
           R(cx + 160, 740, 12, 40, 'metal2', 5), R(cx + 208, 740, 12, 40, 'metal2', 5)]
    s.layer('cabinet', cb, 'slide-r', .5)
    # 诊疗台 + 无影灯（左）
    tx = 300
    tb = [shadow(tx, 905, 200), R(tx - 200, 660, 400, 30, 'metal', 10, extra='filter="url(#shs)"'), R(tx - 190, 686, 380, 10, 'metal2', 4),
          R(tx - 20, 694, 40, 180, 'metal2', 8), E(tx, 890, 120, 18, 'metal2'), R(tx - 160, 640, 320, 24, 'teal', 10, .9), R(tx - 150, 640, 300, 6, '#ffffff', 3, .4)]
    tb += [S(f'M{tx},0 L{tx},140 Q{tx},180 {tx + 40},200', 'metal2', 10), P(f'M{tx - 60},250 Q{tx + 40},170 {tx + 140},250Z', 'metal', extra='filter="url(#shs)"'), E(tx + 40, 250, 100, 14, 'lamp')]
    s.layer('exam_table', tb, 'rise', .6)
    s.layer('lamp_glow', [P(f'M{tx - 50},252 L{tx + 130},252 L{tx + 220},660 L{tx - 140},660Z', s.lg([(0, 'lamp', .35), (1, 'lamp', 0)])), C(tx + 40, 260, 70, 'lamp', .5, 'filter="url(#b20)"')], 'fade', .9, loop='glow')
    # 体重秤
    sc = [shadow(760, 910, 80), R(680, 880, 160, 26, 'cab2', 10, extra='filter="url(#shs)"'), R(690, 874, 140, 10, 'teal', 5), R(736, 888, 48, 12, 'xray', 3), R(742, 891, 26, 6, 'xray2', 2)]
    s.layer('scale', sc, 'pop', .8)
    # 航空箱 + 狗窝（右前）
    ca = [shadow(1360, 912, 130), R(1240, 790, 240, 120, 'carrier', 26, extra='filter="url(#sh)"'), R(1240, 838, 240, 10, 'carrier2'), R(1318, 760, 84, 22, 'carrier2', 10),
          R(1250, 806, 60, 84, 'cab', 10, .85)]
    for k in range(4): ca.append(R(1258 + k * 13, 812, 5, 72, 'metal2', 2))
    for k in range(3): ca.append(R(1340 + k * 40, 806, 24, 22, 'carrier2', 8, .6))
    ca += [shadow(1700, 995, 190), E(1700, 980, 190, 60, 'bed2'), E(1700, 966, 150, 38, 'bed'), E(1700, 962, 120, 26, 'wall1', .9),
           G([C(1640, 952, 12, 'toy'), C(1640, 970, 12, 'toy'), C(1700, 952, 12, 'toy'), C(1700, 970, 12, 'toy'), R(1640, 950, 60, 22, 'toy', 6)], 'transform="rotate(-10 1670 960)"')]
    s.layer('carrier_bed', ca, 'rise', .75)
    s.layer('plant', [leafy(580, 905, 1.0, 'leaf', 'leaf2', 'teal', 8)], 'grow', .9, loop='sway', origin='580 905')
    s.layer('paw_trail', [pawprint(x, y, .7, 'paw', .9) for x, y in [(160, 1010), (230, 980), (300, 1012), (370, 984)]], 'fade', 1.2, loop=None)
    return s


SCENES = [supermarket, park, playground, hospital, parcel, bank, sorting, volunteer, vet]
