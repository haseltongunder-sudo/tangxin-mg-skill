"""第 5 类 科学：s042–s050（平面 MG 风格）"""
from core import *
import math, random


# ---------- 小工具 ----------
def shadow(x, y, rx, ry, op=.14):
    return E(x, y, rx, ry, '#2a1f35', op, 'filter="url(#b6)"')


def rot(items, a, cx, cy):
    return G(items if isinstance(items, list) else [items], f'transform="rotate({a:.1f} {cx:.1f} {cy:.1f})"')


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


def bez_d(p0, p1, p2, p3, t):
    u = 1 - t
    return (3 * u * u * (p1[0] - p0[0]) + 6 * u * t * (p2[0] - p1[0]) + 3 * t * t * (p3[0] - p2[0]),
            3 * u * u * (p1[1] - p0[1]) + 6 * u * t * (p2[1] - p1[1]) + 3 * t * t * (p3[1] - p2[1]))


def leafy(x, y, sc, c1, c2, n=7, spread=2.4, ln=60):
    """一丛叶子（从 x,y 向上散开）"""
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


# ============ s042 电路实验桌 ============
def circuit():
    s = Scene('s042', '电路实验桌', '科学', ['科学', '电路', '电与磁', '实验'],
              dict(wall1='#E7EEF8', wall2='#D2DDEE', stripe='#DCE5F2', peg='#F3E3C6', peg2='#E2CBA4', hole='#C7AD86', top='#EBC48D', top2='#CF9E62',
                   cab='#5C80A8', cab2='#4A6A92', knob='#F2C14E', boardw='#FFFFFF', ink='#33475E', wr='#E8584A', wb='#33475E', wy='#F2B33D',
                   batt='#2F3A46', batt2='#F2B33D', copper='#D98E4A', glass='#FFF7D6', bulb='#FFE07A', glow='#FFD25A', metal='#9AA6B2', metal2='#C9D1DA',
                   meter='#F2C14E', meter2='#E0A92E', screen='#C4ECCD', leaf='#6DBA82', leaf2='#A6DB95', pot='#F2836B', pot2='#DA6B55',
                   d1='#F2836B', d2='#5FB7B0', d3='#F7C55E', d4='#9B8CE8', d5='#7FC4E8'),
              desc='电学实验台：墙上白板画着电池-开关-灯泡的串联电路图，台面上电池盒、闸刀开关、发光小灯泡和万用表，灯泡会发光。',
              stand={'ground_y': 900, 'x': [620, 1300]})
    bg = [R(0, 0, W, 740, s.lg([(0, 'wall1'), (1, 'wall2')]))]
    for x in range(0, W, 96): bg.append(R(x, 0, 48, 740, 'stripe', 0, .45))
    s.layer('wall', bg, 'fade', 0)
    # 白板电路图（矩形回路：电池、开关、灯泡、电流表位置用电阻代替）
    bx, by, bw, bh = 660, 110, 600, 360
    bd = [R(bx - 14, by - 14, bw + 28, bh + 28, 'metal2', 18, extra='filter="url(#sh)"'), R(bx, by, bw, bh, 'boardw', 10),
          R(bx + 40, by + bh + 8, 120, 12, 'metal', 5), R(bx + 70, by + bh, 30, 10, 'wr', 3), R(bx + 110, by + bh, 30, 10, 'd2', 3)]
    L, T_, Rr, B = bx + 100, by + 80, bx + bw - 100, by + bh - 80
    ink = 'ink'
    # 上边：灯泡符号（圆 + X）
    cxb = (L + Rr) / 2
    bd += [S(f'M{L},{T_} L{cxb - 34},{T_}', ink, 6), S(f'M{cxb + 34},{T_} L{Rr},{T_}', ink, 6),
           S(f'M{cxb - 34},{T_} a34,34 0 1,0 68,0 a34,34 0 1,0 -68,0', ink, 6),
           S(f'M{cxb - 24},{T_ - 24} L{cxb + 24},{T_ + 24} M{cxb + 24},{T_ - 24} L{cxb - 24},{T_ + 24}', ink, 5)]
    # 右边：导线
    bd += [S(f'M{Rr},{T_} L{Rr},{B}', ink, 6)]
    # 下边：电池（长线正极、短粗负极）+ 开关（断开）
    bxx = L + 110
    bd += [S(f'M{Rr},{B} L{bxx + 220 + 70},{B}', ink, 6), S(f'M{bxx + 220},{B} L{bxx + 220 + 70},{B - 4}', ink, 6), C(bxx + 220, B, 7, ink), C(bxx + 290, B, 7, ink),
           S(f'M{bxx + 16},{B} L{bxx + 220},{B}', ink, 6), S(f'M{bxx + 10},{B - 40} L{bxx + 10},{B + 40}', ink, 6), S(f'M{bxx - 10},{B - 20} L{bxx - 10},{B + 20}', ink, 12, cap='butt'),
           S(f'M{L},{B} L{bxx - 16},{B}', ink, 6), S(f'M{L},{B} L{L},{T_}', ink, 6)]
    # 电流方向小箭头
    bd += [poly([(L - 12, (T_ + B) / 2 - 10), (L + 12, (T_ + B) / 2 - 10), (L, (T_ + B) / 2 + 12)], 'wr'),
           poly([(Rr - 12, (T_ + B) / 2 + 10), (Rr + 12, (T_ + B) / 2 + 10), (Rr, (T_ + B) / 2 - 12)], 'wr')]
    s.layer('board', bd, 'drop', .3)
    # 左墙：洞洞板与工具
    px, py, pw, ph = 90, 130, 400, 420
    pg = [R(px, py, pw, ph, 'peg', 14, extra='filter="url(#shs)"')]
    for yy in range(py + 24, py + ph - 10, 34):
        for xx in range(px + 24, px + pw - 10, 34): pg.append(C(xx, yy, 4, 'hole'))
    # 钳子
    pg += [rot([R(150, 200, 18, 120, 'wr', 9), R(178, 200, 18, 120, 'wr', 9), R(156, 160, 12, 50, 'metal', 4), R(178, 160, 12, 50, 'metal', 4), C(173, 206, 9, 'metal2')], -8, 173, 240)]
    # 螺丝刀
    pg += [R(236, 180, 26, 90, 'd2', 12), R(244, 270, 10, 90, 'metal', 3), R(286, 180, 26, 80, 'wy', 12), R(294, 260, 10, 80, 'metal', 3)]
    # 导线卷
    for cx_, cy_, col in [(390, 220, 'wr'), (390, 330, 'd2'), (220, 450, 'wy')]:
        pg += [C(cx_, cy_, 44, col), C(cx_, cy_, 34, col, .6), C(cx_, cy_, 14, 'peg2'), S(f'M{cx_ - 40},{cy_ + 6} q40,-12 80,0', '#ffffff', 3, .35)]
    # 小磁铁（U 形，红蓝两极）
    pg += [S('M315,420 L315,470 A35,35 0 0,0 385,470 L385,420', 'wr', 26, cap='butt'), R(302, 400, 26, 26, 'metal2', 2), R(372, 400, 26, 26, 'metal2', 2),
           S('M315,445 L315,470 A35,35 0 0,0 350,505', 'd5', 26, cap='butt')]
    s.layer('pegboard', pg, 'slide-l', .45)
    # 右墙：零件抽屉柜
    dx0, dy0 = 1440, 150
    dr = [R(dx0, dy0, 380, 400, 'cab', 16, extra='filter="url(#sh)"')]
    cols = ['d1', 'd2', 'd3', 'd4', 'd5']
    for r_ in range(5):
        for k in range(4):
            x = dx0 + 18 + k * 89; y = dy0 + 18 + r_ * 74
            dr += [R(x, y, 78, 62, '#ffffff', 8, .92), R(x + 24, y + 38, 30, 9, cols[(k + r_ * 2) % 5], 4), R(x + 10, y + 10, 58, 14, cols[(k + r_ * 2) % 5], 4, .25)]
    s.layer('drawers', dr, 'slide-r', .5)
    # 实验台
    bn = [R(0, 760, W, 320, s.lg([(0, 'cab'), (1, 'cab2')])), R(0, 724, W, 44, s.lg([(0, 'top'), (1, 'top2')]), 6), R(0, 724, W, 7, '#F8DDB2')]
    for x in range(30, W, 320):
        bn += [R(x, 800, 290, 250, 'cab', 12, extra='filter="url(#shs)"'), R(x + 120, 830, 50, 12, 'knob', 6)]
    s.layer('bench', bn, 'rise', .15)
    # 台面电路：电池盒 → 闸刀开关 → 灯泡座
    ci = [shadow(400, 724, 150, 8, .18), R(270, 664, 260, 60, 'cab2', 10)]
    for k in range(2):
        x = 288 + k * 118
        ci += [R(x, 676, 104, 38, 'batt', 12), R(x + 66, 676, 38, 38, 'batt2', 12), R(x + 104, 687, 8, 16, 'metal2', 3), R(x + 10, 682, 40, 6, '#ffffff', 3, .25)]
    # 开关（底座 + 闸刀抬起）
    sx = 640
    ci += [shadow(sx, 724, 80, 7, .18), R(sx - 70, 700, 140, 24, 'top2', 6), R(sx - 50, 690, 22, 14, 'metal', 3), R(sx + 30, 684, 22, 20, 'metal', 3),
           rot([R(sx - 44, 688, 110, 10, 'metal2', 5), R(sx + 56, 660, 14, 36, 'batt', 7)], -3, sx - 40, 694)]
    # 灯泡
    lx = 820
    ci += [shadow(lx, 724, 70, 7, .18), R(lx - 56, 700, 112, 24, 'top2', 6), R(lx - 26, 664, 52, 38, 'metal', 6)]
    for k in range(4): ci.append(R(lx - 24, 668 + k * 8, 48, 3, 'metal2'))
    ci += [P(f'M{lx - 22},{666} C{lx - 22},640 {lx - 54},620 {lx - 54},585 A54,54 0 1,1 {lx + 54},585 C{lx + 54},620 {lx + 22},640 {lx + 22},666Z', 'glass', .95),
           S(f'M{lx - 12},660 L{lx - 12},610 M{lx + 12},660 L{lx + 12},610', 'metal', 3),
           S(f'M{lx - 12},610 l6,-12 l6,12 l6,-12 l6,12', 'copper', 4), C(lx - 22, 572, 12, '#ffffff', .8)]
    # 导线（彩色弧线）
    ci += [S(f'M524,695 C560,620 590,640 {sx - 44},700', 'wr', 7), S(f'M{sx + 46},702 C{sx + 100},650 {lx - 110},650 {lx - 56},712', 'wb', 7),
           S(f'M{lx + 56},712 C{lx + 140},770 260,790 276,700', 'wy', 7, .0),
           S(f'M{lx + 54},712 C{lx + 110},790 300,780 272,700', 'wy', 7)]
    s.layer('circuit', ci, 'pop', .7)
    s.layer('bulb_glow', [C(lx, 588, 110, 'glow', .55, 'filter="url(#b20)"'), C(lx, 588, 46, '#FFFBEA', .9),
                          *[S(f'M{lx + 80 * math.cos(a):.0f},{588 + 80 * math.sin(a):.0f} L{lx + 104 * math.cos(a):.0f},{588 + 104 * math.sin(a):.0f}', 'glow', 6) for a in [-2.6, -2.1, -1.57, -1.05, -.55]]],
            'fade', 1.0, loop='glow')
    # 万用表
    mx = 1230
    mt = [shadow(mx, 724, 90, 8, .2), R(mx - 70, 560, 140, 164, 'meter', 18, extra='filter="url(#shs)"'), R(mx - 52, 576, 104, 52, 'batt', 8), R(mx - 44, 584, 88, 36, 'screen', 4),
          R(mx - 34, 594, 14, 18, 'ink', 2, .6), R(mx - 14, 594, 14, 18, 'ink', 2, .6), R(mx + 8, 594, 14, 18, 'ink', 2, .6),
          C(mx, 664, 30, 'batt'), C(mx, 664, 22, 'metal'), R(mx - 4, 640, 8, 22, '#ffffff', 3),
          C(mx - 40, 706, 7, 'wr'), C(mx, 706, 7, 'batt'), C(mx + 40, 706, 7, 'metal2'),
          S(f'M{mx - 40},706 C{mx - 120},760 {mx - 200},650 {mx - 150},620 L{mx - 140},600', 'wr', 6), S(f'M{mx},706 C{mx + 20},780 {mx + 160},720 {mx + 130},650 L{mx + 126},630', 'batt', 6),
          R(mx - 150, 580, 12, 34, 'wr', 4, extra=f'transform="rotate(15 {mx - 144} 597)"'), R(mx + 120, 600, 12, 34, 'batt', 4, extra=f'transform="rotate(-10 {mx + 126} 617)"')]
    # 导线卷轴
    mt += [shadow(1010, 724, 60, 7, .18), R(960, 640, 100, 84, 'cab2', 10), R(968, 660, 84, 44, 'wr', 6), *[R(968, 664 + k * 9, 84, 3, '#ffffff', 0, .25) for k in range(4)],
           R(954, 640, 112, 14, 'cab2', 6), R(954, 710, 112, 14, 'cab2', 6)]
    s.layer('meter', mt, 'pop', .85)
    # 台灯
    lpx = 1600
    lp = [shadow(lpx, 724, 70, 8, .2), E(lpx, 716, 60, 12, 'cab2'), S(f'M{lpx},712 L{lpx - 50},620 L{lpx - 150},580', 'cab2', 12), C(lpx - 50, 620, 12, 'knob'),
          rot([P(f'M{lpx - 200},560 L{lpx - 120},560 L{lpx - 90},620 L{lpx - 230},620Z', 'cab')], -18, lpx - 160, 590),
          P(f'M{lpx - 220},620 L{lpx - 100},606 L{lpx - 40},724 L{lpx - 300},724Z', s.lg([(0, '#FFF6D6', .7), (1, '#FFF6D6', 0)]))]
    s.layer('desk_lamp', lp, 'grow', .95, origin=f'{lpx} 724')
    # 盆栽（右端）
    s.layer('plant', [potted(1840, 724, 1.0, 'pot', 'pot2', 'leaf', 'leaf2')], 'grow', 1.05, loop='sway', origin='1840 724')
    # 电火花装饰
    sp = []
    for x, y, sc in [(560, 300, 1), (1350, 210, .8), (1110, 520, .7)]:
        sp.append(P(f'M{x},{y} l{18 * sc},{-40 * sc} l{-4 * sc},{30 * sc} l{22 * sc},{-4 * sc} l{-20 * sc},{44 * sc} l{4 * sc},{-30 * sc}Z', 'wy'))
    s.layer('sparks', sp, 'pop', 1.2, loop='twinkle')
    return s


# ============ s043 显微镜下的细胞 ============
def cells():
    s = Scene('s043', '显微镜下的细胞', '科学', ['科学', '生物', '细胞', '显微镜'],
              dict(bg1='#EAF1FB', bg2='#E6DEF6', ring='#5A6678', ring2='#8D9AAB', ring3='#C3CCD8', field1='#F6FCEF', field2='#E2F2D2',
                   wall='#86C46F', wall2='#5EA552', cyto='#EDF8DF', vac='#D9F0F5', nuc='#8E6CC9', nuc2='#C8B3EE', chl='#4FA85A', chl2='#8ED67F',
                   acell='#FFE0D8', acell2='#F7B5A8', amem='#F29A8C', anuc='#B07ACB', anuc2='#DCC0EC', mito='#F2A04E', mito2='#FFD596', er='#F48FA6',
                   stage='#D0D8E2', stage2='#AEBAC8', stage3='#8C98A8', slide='#EAFBFF', clip='#6E7A8A', bokeh='#FFFFFF', light='#FFF7D2', ptr='#2F3640'),
              desc='显微镜视野：圆形视野里是排列整齐的植物细胞（细胞壁、液泡、细胞核、叶绿体），周围漂浮着动物细胞，下方是载物台与玻片。',
              stand={'ground_y': 880, 'x': [560, 1360]})
    s.layer('bg', [R(0, 0, W, H, s.lg([(0, 'bg1'), (1, 'bg2')])), C(960, 470, 560, 'light', .45, 'filter="url(#b40)"')], 'fade', 0)
    random.seed(4)
    bk = [C(random.uniform(0, W), random.uniform(0, 860), random.uniform(10, 46), 'bokeh', random.uniform(.25, .55)) for _ in range(26)]
    s.layer('bokeh', bk, 'fade', .2, loop='drift')
    cx, cy, r = 960, 450, 370
    # 视野内的植物细胞网格
    cp = s.clip(f'<circle cx="{cx}" cy="{cy}" r="{r}"/>')
    random.seed(7)
    cl = [C(cx, cy, r, s.rg([(0, 'field1'), (1, 'field2')]))]
    grid = []
    cw, ch = 176, 112
    for row in range(-1, 9):
        y = cy - r - 40 + row * ch
        off = (row % 2) * cw / 2
        for k in range(-1, 8):
            x = cx - r - 120 + k * cw + off
            w_ = cw - 4; h_ = ch - 4
            grid += [R(x, y, w_, h_, 'wall', 16), R(x + 7, y + 7, w_ - 14, h_ - 14, 'cyto', 12),
                     R(x + 20, y + 18, w_ - 40, h_ - 36, 'vac', 22, .95)]
            side = random.choice([.24, .76])
            nx, ny = x + w_ * side, y + h_ * random.uniform(.38, .62)
            grid += [C(nx, ny, 16, 'nuc'), C(nx - 3, ny - 3, 6, 'nuc2')]
            for q in range(6):
                t = random.uniform(0, 1)
                if q % 2 == 0: px_, py_ = x + 14 + t * (w_ - 28), y + 13 if q < 3 else y + h_ - 13
                else: px_, py_ = (x + 13 if q < 3 else x + w_ - 13), y + 16 + t * (h_ - 32)
                grid += [E(px_, py_, 9, 5.5, 'chl'), E(px_ - 2, py_ - 1.5, 4, 2, 'chl2')]
    cl.append(G([rot(grid, -9, cx, cy)], f'clip-path="{cp}"'))
    cl.append(C(cx, cy, r, s.rg([(.75, '#ffffff', 0), (1, '#5a4a70', .22)])))
    s.layer('cells', cl, 'zoom', .35, origin=f'{cx} {cy}')
    # 指针 + 比例尺（视野中常见）
    s.layer('pointer', [S(f'M{cx + r - 6},{cy - 10} L{cx + 90},{cy - 40}', 'ptr', 6), poly([(cx + 82, cy - 37), (cx + 108, cy - 52), (cx + 102, cy - 30)], 'ptr'),
                        R(cx - 140, cy + 280, 140, 8, 'ptr', 3, .75), R(cx - 140, cy + 272, 4, 24, 'ptr', 0, .75), R(cx - 4, cy + 272, 4, 24, 'ptr', 0, .75)], 'fade', 1.0)
    # 镜筒圆环
    rg = [C(cx, cy, r + 46, 'ring', extra='filter="url(#sh)"'), C(cx, cy, r + 34, 'ring2'), C(cx, cy, r + 14, 'ring')]
    for k in range(72):
        a = k * math.pi / 36
        r0 = r + 20 if k % 6 else r + 16
        rg.append(S(f'M{cx + r0 * math.cos(a):.1f},{cy + r0 * math.sin(a):.1f} L{cx + (r + 30) * math.cos(a):.1f},{cy + (r + 30) * math.sin(a):.1f}', 'ring3', 2.5 if k % 6 else 4, .8))
    rg.append(P(f'M{cx - r - 40},{cy} A{r + 40},{r + 40} 0 0,1 {cx - 120},{cy - r - 20}', 'none'))
    rg.append(S(f'M{cx - 250},{cy - 330} A{r + 40},{r + 40} 0 0,1 {cx + 80},{cy - r - 38}', '#ffffff', 6, .45))
    s.layer('lens_ring', [G([C(cx, cy, r, 'none')]), G(rg, f'mask="url(#{s.sid}-ringmask)"')], 'zoom', .2, origin=f'{cx} {cy}')
    s.defs.append(f'<mask id="{s.sid}-ringmask"><rect width="{W}" height="{H}" fill="#fff"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="#000"/></mask>')

    # 漂浮的动物细胞
    def acell(x, y, rr, seed):
        random.seed(seed)
        pts = []
        for k in range(14):
            a = k * 2 * math.pi / 14; rad = rr * random.uniform(.9, 1.06)
            pts.append((x + rad * math.cos(a), y + rad * .88 * math.sin(a)))
        d = 'M' + ' '.join(f'{(pts[k][0] + pts[(k + 1) % 14][0]) / 2:.1f},{(pts[k][1] + pts[(k + 1) % 14][1]) / 2:.1f} Q{pts[(k + 1) % 14][0]:.1f},{pts[(k + 1) % 14][1]:.1f}' for k in range(14)).replace(' Q', ' Q', 1)
        # 平滑闭合曲线
        seg = []
        for k in range(14):
            p1 = pts[(k + 1) % 14]; m0 = ((pts[k][0] + p1[0]) / 2, (pts[k][1] + p1[1]) / 2); m1 = ((p1[0] + pts[(k + 2) % 14][0]) / 2, (p1[1] + pts[(k + 2) % 14][1]) / 2)
            if k == 0: seg.append(f'M{m0[0]:.1f},{m0[1]:.1f}')
            seg.append(f'Q{p1[0]:.1f},{p1[1]:.1f} {m1[0]:.1f},{m1[1]:.1f}')
        d = ' '.join(seg) + 'Z'
        it = [P(d, 'amem', extra='filter="url(#shs)"'), G([P(d, 'acell')], f'transform="translate({x:.1f} {y:.1f}) scale(.94) translate({-x:.1f} {-y:.1f})"')]
        it += [S(f'M{x - rr * .2},{y + rr * .1} q{rr * .15},{-rr * .12} {rr * .3},0 t{rr * .3},0', 'er', 3, .6), S(f'M{x - rr * .25},{y + rr * .22} q{rr * .15},{-rr * .12} {rr * .3},0 t{rr * .3},0', 'er', 3, .5)]
        it += [C(x - rr * .05, y - rr * .12, rr * .3, 'anuc'), C(x - rr * .1, y - rr * .17, rr * .1, 'anuc2')]
        for k in range(4):
            a = random.uniform(0, 2 * math.pi); d_ = rr * random.uniform(.5, .68); mx_, my_ = x + d_ * math.cos(a), y + d_ * .8 * math.sin(a)
            ang = random.uniform(0, 180)
            it.append(rot([E(mx_, my_, rr * .16, rr * .075, 'mito'), S(f'M{mx_ - rr * .11},{my_} q{rr * .05},{-rr * .05} {rr * .1},0 t{rr * .1},0', 'mito2', 2)], ang, mx_, my_))
        return G(it)
    s.layer('animal_cells_far', [acell(170, 760, 70, 3), acell(1770, 760, 64, 5), acell(1560, 120, 46, 8)], 'pop', .7, loop='drift')
    s.layer('animal_cells', [acell(240, 300, 120, 1), acell(1690, 380, 132, 2)], 'pop', .55, loop='bob')
    # 载物台与玻片
    st = [R(0, 880, W, 200, s.lg([(0, 'stage'), (1, 'stage2')])), R(0, 872, W, 16, 'stage3'), R(0, 872, W, 4, '#ffffff', 0, .6),
          E(960, 900, 260, 40, 'light', .55, 'filter="url(#b20)"'),
          R(420, 846, 1080, 30, 'slide', 4, .92, 'filter="url(#shs)"'), R(420, 846, 1080, 6, '#ffffff', 2, .9), R(880, 848, 160, 26, 'field2', 3, .8),
          R(380, 820, 160, 34, 'clip', 10), R(380, 846, 100, 14, 'clip', 4), C(410, 836, 9, 'stage'),
          R(1380, 820, 160, 34, 'clip', 10), R(1440, 846, 100, 14, 'clip', 4), C(1510, 836, 9, 'stage')]
    s.layer('stage', st, 'rise', .1)
    s.layer('light', [beam(900, 1020, 880, 1040, 880, 470, s, .0), E(960, 470, 300, 300, 'light', .18, 'filter="url(#b40)"')], 'fade', .9, loop='glow')
    return s


# ============ s044 植物温室 ============
def greenhouse():
    s = Scene('s044', '植物温室', '科学', ['科学', '植物', '光合作用', '劳动'],
              dict(sky1='#BCE5F4', sky2='#F1FAF2', hill='#CDE8CF', hill2='#B4DBB8', frame='#FFFFFF', frame2='#E1EAE6', glass='#E6F6F1',
                   floor1='#E3D2B4', floor2='#CDB892', tile='#D6C3A1', bench='#8FC1A3', bench2='#6FA487', pot='#E58C5C', pot2='#CB7444', soil='#7A563C',
                   leaf='#5BAA6B', leaf2='#8ED07C', leaf3='#3E8B5A', f1='#F28BA0', f2='#F7C55E', f3='#B49AE6', f4='#FF8E5E', tomato='#EF5A45',
                   can='#5FB7D6', can2='#3E97BB', tray='#4E5A66', mist='#FFFFFF', pipe='#B8C4CC', hang='#C8A27A'),
              desc='明亮的玻璃温室：拱形白色钢架与玻璃顶，阶梯花架摆满盆栽，吊篮垂下藤蔓，育苗盘、番茄苗与喷雾管。',
              stand={'ground_y': 900, 'x': [600, 1320]})
    s.layer('sky', [R(0, 0, W, 800, s.lg([(0, 'sky1'), (1, 'sky2')])), C(1500, 200, 200, '#FFF6D0', .6, 'filter="url(#b40)"')], 'fade', 0)
    s.layer('outside', [P('M0,640 Q300,520 640,600 Q980,680 1300,560 Q1600,470 1920,580 L1920,800 L0,800Z', 'hill'),
                        P('M0,700 Q420,620 900,690 Q1400,750 1920,660 L1920,800 L0,800Z', 'hill2'),
                        *[blob_tree(x, 720, .55, 'leaf2', 'hill', 'pot2') for x in (180, 520, 1420, 1760)], cloud(400, 180, .7, op=.85), cloud(1200, 120, .5, op=.8)], 'rise', .15, loop=None)
    # 玻璃结构：拱顶 + 竖框
    fr = [P(f'M0,{H} L0,300 Q960,-120 1920,300 L1920,{H}Z', 'glass', .28)]
    for x in range(0, W + 1, 160):
        yt = 300 - (1 - ((x - 960) / 960) ** 2) * 420 * .5 - 0
        yt = 300 - 210 * (1 - ((x - 960) / 960) ** 2)
        fr.append(R(x - 6, yt, 12, 800 - yt, 'frame'))
    for yy in (520, 800):
        fr.append(R(0, yy - 6, W, 12, 'frame'))
    fr += [S('M0,300 Q960,-120 1920,300', 'frame', 16), S('M0,330 Q960,-60 1920,330', 'frame2', 6, .8)]
    for k in range(1, 6):
        u = k / 6
        fr.append(S(f'M{u * W:.0f},{300 - 210 * (1 - ((u * W - 960) / 960) ** 2):.0f} L{u * W:.0f},{300 - 210 * (1 - ((u * W - 960) / 960) ** 2) - 0:.0f}', 'frame', 4))
    # 屋顶横向肋
    fr += [S('M0,420 Q960,60 1920,420', 'frame', 5, .0)]
    s.layer('structure', fr, 'fade', .3)
    s.layer('sunbeams', [beam(1300, 1420, 900, 1180, 0, 900, s, .3), beam(1500, 1580, 1260, 1460, 0, 900, s, .25), beam(500, 580, 260, 460, 0, 900, s, .18)], 'fade', .8, loop='glow')
    # 喷雾管
    pp = [R(0, 150, W, 10, 'pipe', 5)]
    for x in range(200, W, 320): pp += [R(x - 8, 156, 16, 22, 'pipe', 4)]
    s.layer('pipe', pp, 'drop', .45)
    s.layer('mist', [P(f'M{x - 8},178 L{x + 8},178 L{x + 60},300 L{x - 60},300Z', s.lg([(0, 'mist', .55), (1, 'mist', 0)])) for x in range(200, W, 320)], 'fade', 1.1, loop='flow')
    # 地面
    fl = [R(0, 800, W, 280, s.lg([(0, 'floor1'), (1, 'floor2')])), R(0, 800, W, 6, 'frame2')]
    for x in range(0, W, 120): fl.append(S(f'M{x},806 L{x + (x - 960) * .25:.0f},1080', 'tile', 3, .7))
    for yy in (850, 920, 1010): fl.append(S(f'M0,{yy} L{W},{yy}', 'tile', 3, .6))
    s.layer('floor', fl, 'rise', .1)
    pb = [R(560, 730, 800, 70, 'pot2', 10, extra='filter="url(#shs)"'), R(548, 722, 824, 18, 'pot', 8), R(560, 760, 800, 4, 'pot', 0, .5)]
    random.seed(15)
    for k in range(22):
        x = 580 + k * 36 + random.uniform(-6, 6); h = random.uniform(40, 80)
        pb += [S(f'M{x},726 L{x + random.uniform(-6, 6):.0f},{726 - h:.0f}', 'leaf3', 4), E(x - 10, 726 - h * .45, 14, 6, 'leaf', extra=f'transform="rotate(-30 {x - 10} {726 - h * .45:.0f})"'),
               E(x + 10, 726 - h * .6, 14, 6, 'leaf2', extra=f'transform="rotate(30 {x + 10} {726 - h * .6:.0f})"')]
        col = ['f1', 'f2', 'f3', 'f4'][k % 4]
        pb += [C(x + 7 * math.cos(a), 726 - h + 7 * math.sin(a), 7, col) for a in [q * 1.2566 for q in range(5)]] + [C(x, 726 - h, 5, '#ffffff', .9)]
    s.layer('planter', pb, 'grow', .7, loop='sway', origin='960 800')

    def flowerpot(x, y, sc, fcol):
        it = [P(f'M{x - 28 * sc},{y - 48 * sc} L{x + 28 * sc},{y - 48 * sc} L{x + 21 * sc},{y} L{x - 21 * sc},{y}Z', 'pot'), R(x - 31 * sc, y - 54 * sc, 62 * sc, 12 * sc, 'pot2', 4)]
        it.insert(0, leafy(x, y - 50 * sc, sc * .9, 'leaf', 'leaf2', 6))
        if fcol:
            for k in range(3):
                fx, fy = x + (k - 1) * 22 * sc, y - (96 + (k % 2) * 16) * sc
                it += [S(f'M{x},{y - 50 * sc} L{fx},{fy}', 'leaf3', 3 * sc)] + [C(fx + 9 * sc * math.cos(a), fy + 9 * sc * math.sin(a), 7 * sc, fcol) for a in [q * 1.2566 for q in range(5)]] + [C(fx, fy, 5 * sc, 'f2' if fcol != 'f2' else 'f4')]
        return G(it)
    # 左：三层阶梯花架
    st = []
    for k, (y, x0, x1) in enumerate([(820, 40, 520), (700, 40, 400), (580, 40, 280)]):
        st += [R(x0, y, x1 - x0, 18, 'bench', 6, extra='filter="url(#shs)"'), R(x1 - 30, y + 18, 14, 860 - y, 'bench2', 4)]
    st.append(R(50, 580, 14, 280, 'bench2', 4))
    fc = ['f1', 'f3', None, 'f2', 'f4']
    for k, x in enumerate(range(90, 500, 90)): st.append(flowerpot(x, 820, 1.0, fc[k % 5]))
    for k, x in enumerate(range(90, 390, 95)): st.append(flowerpot(x, 700, .9, fc[(k + 2) % 5]))
    for k, x in enumerate(range(100, 280, 90)): st.append(flowerpot(x, 580, .8, fc[(k + 1) % 5]))
    s.layer('stand_left', st, 'slide-l', .5)
    # 右：育苗台 + 番茄苗
    rb = [R(1400, 720, 480, 24, 'bench', 6, extra='filter="url(#shs)"'), R(1420, 744, 16, 116, 'bench2', 4), R(1844, 744, 16, 116, 'bench2', 4), R(1430, 810, 420, 12, 'bench2', 4)]
    for t0 in (1420, 1650):
        rb += [R(t0, 680, 210, 40, 'tray', 6)]
        for k in range(5):
            x = t0 + 22 + k * 42; rb += [R(x - 14, 688, 28, 28, 'soil', 4), S(f'M{x},{690} L{x},{668}', 'leaf3', 3), E(x - 9, 666, 10, 5, 'leaf2', extra=f'transform="rotate(-25 {x - 9} 666)"'), E(x + 9, 662, 10, 5, 'leaf', extra=f'transform="rotate(25 {x + 9} 662)"')]
    # 番茄：大盆 + 支架 + 果实
    tx = 1760
    rb += [shadow(tx, 880, 80, 10), P(f'M{tx - 70},780 L{tx + 70},780 L{tx + 56},880 L{tx - 56},880Z', 'pot'), R(tx - 76, 770, 152, 18, 'pot2', 6),
           S(f'M{tx - 30},776 L{tx - 40},420 M{tx + 30},776 L{tx + 40},420', 'hang', 6)]
    for k in range(8):
        y = 760 - k * 44; side = 1 if k % 2 else -1
        rb += [S(f'M{tx},{y} q{side * 20},{-20} {side * 10},{-44}', 'leaf3', 5), E(tx + side * 40, y - 20, 34, 13, 'leaf', extra=f'transform="rotate({side * -25} {tx + side * 40} {y - 20})"')]
    for x, y in [(tx - 36, 640), (tx + 30, 580), (tx - 20, 520), (tx + 36, 680)]:
        rb += [C(x, y, 17, 'tomato'), C(x - 5, y - 5, 5, '#ffffff', .5), P(f'M{x - 8},{y - 16} l8,6 l8,-6 l-8,-3Z', 'leaf3')]
    s.layer('bench_right', rb, 'slide-r', .6)
    # 吊篮
    hb = []
    for x, ln in [(620, 160), (1300, 200)]:
        y = 160 + ln
        hb += [S(f'M{x},160 L{x - 40},{y} M{x},160 L{x + 40},{y}', 'hang', 3), P(f'M{x - 50},{y} L{x + 50},{y} Q{x + 44},{y + 50} {x},{y + 54} Q{x - 44},{y + 50} {x - 50},{y}Z', 'pot'),
               leafy(x, y + 4, .8, 'leaf', 'leaf2', 7)]
        for k, dx in enumerate((-40, -14, 14, 40)):
            ll = 90 + (k % 2) * 60
            hb.append(S(f'M{x + dx},{y + 20} q{dx * .4},{ll * .5} 0,{ll}', 'leaf3', 4))
            for q in range(4):
                hb.append(E(x + dx + (4 if q % 2 else -6), y + 40 + q * ll / 4.5, 12, 6, 'leaf2' if q % 2 else 'leaf'))
    s.layer('hanging', hb, 'drop', .75, loop='sway')
    # 近景：大叶植物、喷壶
    nr = [shadow(330, 1000, 110, 14), leafy(330, 900, 3.0, 'leaf3', 'leaf', 9, 2.8, 70), P('M260,900 L400,900 L384,1000 L276,1000Z', 'pot'), R(250, 888, 160, 22, 'pot2', 8),
          shadow(1560, 960, 80, 10), R(1500, 880, 110, 80, 'can', 20), S('M1610,900 L1680,850', 'can2', 14), E(1684, 846, 14, 9, 'can2'), S('M1520,890 Q1555,830 1590,890', 'can2', 10), R(1508, 900, 94, 8, '#ffffff', 4, .3)]
    s.layer('foreground', nr, 'rise', .9, loop=None)
    random.seed(12)
    s.layer('drops', [E(random.uniform(150, 1800), random.uniform(200, 340), 3, 5, 'mist', .8) for _ in range(20)], 'fade', 1.2, loop='twinkle')
    return s


# ============ s045 气象站 ============
def weather():
    s = Scene('s045', '气象站', '科学', ['科学', '天气', '气象观测', '地理'],
              dict(sky1='#86CCF0', sky2='#E9F7FF', sun='#FFD36E', hill='#B3DCA2', hill2='#97CD86', grass1='#A3D486', grass2='#83C26A', plot='#C3E6A8',
                   white='#FFFFFF', white2='#E1E7EE', white3='#C7D0DA', metal='#7D8A98', metal2='#A9B4C0', red='#F2735E', orange='#F7A64A',
                   fence='#FFFFFF', path='#EBDDBE', panel='#3D5B8C', panel2='#6C90C6', blue='#5FB7D6', tree='#5FAE74', tree2='#9AD48B', trunk='#8A5A3A', rainbow1='#F7A6A0', rainbow2='#FFE08A', rainbow3='#A8E0B5', rainbow4='#9FD3F5'),
              desc='户外气象观测场：白色百叶箱、风速风向杆（风杯与风向标）、雨量筒、日照计、风向袋与升空的探空气球。',
              stand={'ground_y': 880, 'x': [600, 1300]})
    s.layer('sky', [R(0, 0, W, 800, s.lg([(0, 'sky1'), (1, 'sky2')])), C(380, 170, 170, 'sun', .3, 'filter="url(#b40)"'), C(380, 170, 72, 'sun')], 'fade', 0)
    rb = []
    for k, col in enumerate(['rainbow1', 'rainbow2', 'rainbow3', 'rainbow4']):
        rr = 620 - k * 26
        rb.append(S(f'M{1360 - rr},700 A{rr},{rr} 0 0,1 {1360 + rr},700', col, 26, .45, cap='butt'))
    s.layer('rainbow', rb, 'fade', .3)
    s.layer('clouds', [cloud(760, 150, .8, op=.95), cloud(1300, 230, .6, op=.9), cloud(1780, 120, .7, op=.9)], 'slide-l', .25, loop='drift')
    s.layer('hills', [P('M0,640 Q360,540 760,610 Q1180,690 1540,580 Q1760,520 1920,560 L1920,800 L0,800Z', 'hill'),
                      *[blob_tree(x, 680, .5 + .1 * (k % 2), 'tree', 'tree2', 'trunk') for k, x in enumerate((90, 640, 1120, 1480))],
                      P('M0,720 Q500,650 1000,700 Q1500,750 1920,690 L1920,800 L0,800Z', 'hill2')], 'rise', .2)
    gd = [R(0, 760, W, 320, s.lg([(0, 'grass1'), (1, 'grass2')])), P('M120,780 L1800,780 L1880,1080 L40,1080Z', 'plot', .6),
          P('M860,780 L1060,780 L1160,1080 L760,1080Z', 'path')]
    for k in range(8): gd.append(S(f'M{120 + k * 240},790 l-8,-16 m8,16 l8,-18 m-8,18 l0,-20', 'grass2', 3, .8))
    s.layer('ground', gd, 'rise', .1)
    # 白色矮栅栏
    fn = [R(0, 724, W, 10, 'fence'), R(0, 752, W, 10, 'fence')]
    for x in range(10, W, 46): fn += [P(f'M{x},780 L{x},716 L{x + 12},700 L{x + 24},716 L{x + 24},780Z', 'fence'), R(x + 20, 716, 4, 64, 'white3', 0, .5)]
    s.layer('fence', fn, 'rise', .3)
    # 百叶箱（左）
    hx = 330
    hv = [shadow(hx, 880, 150, 14, .2)]
    for dx in (-90, 90): hv.append(R(hx + dx - 8, 600, 16, 280, 'white2', 4))
    hv += [S(f'M{hx - 90},800 L{hx + 90},700 M{hx + 90},800 L{hx - 90},700', 'white3', 6), R(hx - 120, 360, 240, 250, 'white', 8, extra='filter="url(#sh)"'),
           poly([(hx - 140, 368), (hx + 140, 368), (hx + 112, 320), (hx - 112, 320)], 'white2'), R(hx - 146, 360, 292, 14, 'white', 4)]
    for side in (-1, 1):
        x0 = hx - 108 if side < 0 else hx + 4
        for k in range(10):
            y = 384 + k * 21
            hv += [R(x0, y, 104, 14, 'white2', 3), R(x0, y + 10, 104, 4, 'white3', 0, .8)]
    hv += [R(hx - 4, 376, 8, 226, 'white3'), C(hx + 12, 490, 6, 'metal'), R(hx - 160, 604, 320, 14, 'white2', 4)]
    hv += [R(hx - 60, 820, 120, 14, 'white2', 3), R(hx - 50, 760, 100, 12, 'white2', 3)]  # 台阶
    s.layer('screen_box', hv, 'rise', .5)
    # 风杆（右）：风杯 + 风向标
    mx = 1560
    ms = [shadow(mx, 880, 60, 8), R(mx - 30, 860, 60, 24, 'metal', 4), R(mx - 7, 150, 14, 720, s.lg([(0, 'metal2'), (1, 'metal')], 0, 0, 1, 0)),
          ]
    for k in range(0, 720, 120): ms.append(R(mx - 7, 220 + k, 14, 60, 'red', 0, .9))
    # 风杯（三个半球，正视看见两侧+中间）
    ms += [R(mx - 4, 120, 8, 40, 'metal'), R(mx - 90, 116, 180, 6, 'metal', 3), R(mx - 4, 98, 8, 22, 'metal'),
           P(f'M{mx - 110},104 a22,22 0 0,0 0,44Z', 'white', extra='filter="url(#shs)"'), E(mx - 110, 126, 6, 22, 'white3'),
           P(f'M{mx + 110},104 a22,22 0 0,1 0,44Z', 'white', extra='filter="url(#shs)"'), E(mx + 110, 126, 6, 22, 'white3'),
           C(mx, 92, 20, 'white'), E(mx, 92, 20, 7, 'white3', .7), C(mx, 128, 8, 'metal2')]
    s.layer('mast', ms, 'grow', .6, origin=f'{mx} 880')
    # 风向标（箭头 + 尾翼）
    s.layer('vane', [R(mx - 100, 211, 200, 6, 'metal', 3), poly([(mx - 150, 214), (mx - 104, 191), (mx - 104, 237)], 'red'),
                     poly([(mx + 90, 214), (mx + 160, 177), (mx + 170, 177), (mx + 130, 214), (mx + 170, 251), (mx + 160, 251)], 'orange'),
                     C(mx, 214, 10, 'metal2')], 'pop', .9, loop='sway', origin=f'{mx} 214')
    # 雨量筒 + 日照计 + 太阳能板
    eq = [shadow(1260, 880, 52, 8), R(1226, 700, 68, 170, 'white', 8, extra='filter="url(#shs)"'), E(1260, 700, 34, 8, 'white3'), R(1226, 760, 68, 6, 'white3'), R(1232, 860, 56, 20, 'metal', 4),
          R(1230, 714, 6, 140, '#ffffff', 2, .6)]
    eq += [shadow(1810, 880, 40, 6), R(1806, 690, 8, 190, 'metal'), R(1776, 676, 68, 14, 'metal', 4), C(1810, 646, 30, 'blue', .55), C(1800, 636, 9, '#ffffff', .9), S('M1780,646 a30,30 0 0,0 60,0', 'white3', 4)]
    eq += [shadow(1380, 880, 70, 8), R(1374, 770, 12, 110, 'metal'), rot([R(1300, 700, 160, 100, 'panel', 6, extra='filter="url(#shs)"')] + [R(1306 + k * 38, 706, 34, 88, 'panel2', 2, .7) for k in range(4)] + [R(1300, 748, 160, 3, 'panel')], -14, 1380, 770)]
    s.layer('instruments', eq, 'pop', .75)
    # 风向袋
    ws = [R(1700, 400, 8, 480, 'metal')]
    ws2 = [P('M1708,404 L1850,424 L1850,466 L1708,486Z', 'red'), P('M1755,410 L1802,417 L1802,473 L1755,480Z', 'white'), P('M1850,424 L1880,430 L1880,460 L1850,466Z', 'white')]
    s.layer('windsock_pole', ws, 'grow', .8, origin='1704 880')
    s.layer('windsock', ws2, 'pop', 1.0, loop='sway', origin='1708 445')
    # 探空气球
    bl = [S('M1070,330 Q1050,420 1080,520', 'metal', 2.5), R(1068, 520, 26, 22, 'orange', 4), C(1060, 250, 82, 'white', extra='filter="url(#sh)"'), C(1030, 220, 26, '#ffffff', .9),
          P('M1046,328 L1074,328 L1066,340 L1054,340Z', 'white3')]
    s.layer('balloon', bl, 'rise', 1.1, loop='bob')
    return s


# ============ s046 火山地质剖面 ============
def volcano():
    s = Scene('s046', '火山地质剖面', '科学', ['科学', '地球', '火山', '地理'],
              dict(sky1='#F9CFB0', sky2='#FFF1DE', far='#EBC9B1', far2='#E2B9A0', smoke='#A79AAE', smoke2='#D6CCD8', ash='#8E8296',
                   cone1='#8C6858', cone2='#A6826E', cone3='#735447', lava='#FF7A3D', lava2='#FFC04D', magma='#E5432C', magma2='#FF9A3D',
                   grass='#9ACB7A', grass2='#7DB463', soil='#9D7152', l1='#E2BB8C', l2='#CB9763', l3='#EFD3A6', l4='#B5835E', l5='#93694F', l6='#7A584A',
                   peb='#F3E2C6', fossil='#FFF2DC', tree='#5FA36E', tree2='#8CCB80', trunk='#7A5238', house='#FFFFFF', roof='#E2584A', glow='#FFB347'),
              desc='火山地质剖面：上方是喷发的层状火山与灰云，地面以下切开可见彩色沉积岩层、化石、岩浆房与火山通道，左侧平地可站人讲解。',
              stand={'ground_y': 640, 'x': [180, 880]})
    s.layer('sky', [R(0, 0, W, 700, s.lg([(0, 'sky1'), (1, 'sky2')]))], 'fade', 0)
    s.layer('far', [P('M0,520 L180,400 L320,470 L480,360 L640,480 L760,430 L980,520 L1180,440 L1700,470 L1920,380 L1920,700 L0,700Z', 'far'),
                    P('M0,580 L220,500 L400,560 L600,490 L900,600 L1100,540 L1300,620 L1300,700 L0,700Z', 'far2')], 'rise', .2)
    # 火山锥外形
    sx0, sy0 = 960, 640
    cone_d = 'M960,640 C1150,600 1300,420 1394,238 L1420,254 L1484,254 L1508,236 C1600,420 1760,560 1920,600 L1920,640Z'
    # 层状火山：内部平行层（层状剖面）
    co = [P(cone_d, 'cone1')]
    cpc = s.clip(f'<path d="{cone_d}"/>')
    lay = []
    for k in range(7):
        off = 30 + k * 34
        lay.append(S(f'M{960 + off * 2.2:.0f},640 C{1150 + off},{600 - off * .2:.0f} {1300 + off * .3:.0f},{420 + off * .7:.0f} {1450},{254 + off * 1.25:.0f} C{1600 - off * .3:.0f},{420 + off * .7:.0f} {1760 - off},{560 - off * .1:.0f} {1920},{600 + off * .4:.0f}', 'cone2' if k % 2 == 0 else 'cone3', 16, .7))
    co.append(G(lay, f'clip-path="{cpc}"'))
    s.layer('cone', co, 'rise', .3)
    # 地表草皮与左侧小村
    gs = [R(0, 626, 980, 20, 'grass', 6), P('M960,640 C1150,600 1300,420 1394,238 L1400,250 C1310,430 1160,616 970,652Z', 'grass2', .55)]
    vil = []
    for x, sc in [(120, .5), (300, .62), (780, .55)]:
        vil.append(blob_tree(x, 630, sc, 'tree', 'tree2', 'trunk'))
    for x in (430, 560):
        vil += [R(x, 572, 80, 60, 'house', 4, extra='filter="url(#shs)"'), poly([(x - 10, 576), (x + 90, 576), (x + 40, 536)], 'roof'), R(x + 30, 600, 20, 32, 'l2', 3), R(x + 58, 590, 14, 14, 'sky1', 2)]
    s.layer('village', gs + vil, 'grow', .5, origin='500 640')
    # 地下岩层（剖面）
    bands = [(640, 'soil'), (690, 'l3'), (760, 'l1'), (840, 'l2'), (915, 'l4'), (990, 'l5'), (1050, 'l6')]
    st = []
    for k, (y0, col) in enumerate(bands):
        d = f'M0,{y0} ' + ' '.join(f'L{x},{y0 + 10 * math.sin(x / 300 + k * .8) + (x - 960) * .02 * (k % 2):.0f}' for x in range(0, W + 1, 60)) + f' L{W},{H} L0,{H}Z'
        st.append(P(d, col))
    random.seed(21)
    for _ in range(70):
        x = random.uniform(0, W); y = random.uniform(1000, 1076); st.append(E(x, y, random.uniform(6, 14), random.uniform(4, 8), 'peb', .55))
    for _ in range(40):
        x = random.uniform(0, W); y = random.uniform(700, 750); st.append(C(x, y, random.uniform(2, 4), 'l2', .6))
    # 化石：菊石、三叶虫
    for fx, fy, sc in [(260, 800, 1), (700, 880, .8)]:
        sp = ' '.join(f'L{fx + (4 + t * 3.2) * sc * math.cos(t):.1f},{fy + (4 + t * 3.2) * sc * math.sin(t):.1f}' for t in [q * .25 for q in range(1, 48)])
        st += [C(fx, fy, 42 * sc, 'fossil', .85), S(f'M{fx},{fy} {sp}', 'l4', 4 * sc)]
    st += [E(420, 960, 30, 20, 'fossil', .85), S('M392,960 L448,960 M400,950 L440,950 M400,970 L440,970', 'l5', 3), C(420, 942, 8, 'fossil', .85)]
    s.layer('strata', st, 'rise', .1)
    # 岩浆房 + 通道 + 支脉
    mg = [E(1450, 880, 270, 92, s.rg([(0, 'lava2'), (.55, 'magma2'), (1, 'magma')])),
          P('M1430,800 C1426,600 1436,420 1428,254 L1472,254 C1466,420 1478,600 1474,800Z', s.lg([(0, 'lava2'), (1, 'magma2')])),
          P('M1458,560 C1520,520 1600,470 1650,420 L1664,436 C1610,486 1530,540 1462,590Z', 'magma2'),
          E(1250, 920, 70, 22, 'magma', .8), P('M1300,900 C1340,880 1380,870 1400,860 L1400,880 C1360,890 1330,905 1300,915Z', 'magma', .8)]
    s.layer('magma', mg, 'grow', .6, origin='1450 880')
    s.layer('magma_glow', [E(1450, 880, 340, 140, 'glow', .45, 'filter="url(#b40)"'), C(1450, 250, 90, 'glow', .6, 'filter="url(#b20)"'), C(1656, 428, 40, 'glow', .6, 'filter="url(#b20)"')], 'fade', .9, loop='glow')
    # 地表熔岩流
    lv = [P('M1484,250 C1520,300 1540,380 1580,420 C1610,460 1640,520 1700,560 C1680,570 1650,560 1630,530 C1590,470 1560,430 1530,390 C1500,340 1490,300 1470,256Z', 'lava'),
          P('M1490,262 C1515,320 1530,370 1556,410 C1540,380 1510,330 1490,262Z', 'lava2'),
          P('M1650,420 C1690,460 1720,520 1780,560 C1750,566 1720,540 1700,510 C1680,480 1660,450 1646,430Z', 'lava')]
    s.layer('lava', lv, 'fade', .8)
    # 火山灰云
    sm = []
    for x, y, r in [(1450, 190, 60), (1400, 140, 70), (1500, 120, 76), (1440, 70, 84), (1340, 80, 64), (1560, 60, 70), (1260, 50, 50), (1640, 30, 56)]:
        sm += [C(x, y, r, 'smoke'), C(x - r * .2, y - r * .22, r * .78, 'smoke2', .85)]
    s.layer('ash_cloud', sm, 'grow', 1.0, loop='drift', origin='1450 240')
    random.seed(5)
    s.layer('lava_bombs', [C(1450 + random.uniform(-160, 160), random.uniform(150, 230), random.uniform(6, 11), 'lava' if k % 2 else 'lava2') for k in range(10)], 'pop', 1.2, loop='twinkle')
    return s


# ============ s047 海底世界 ============
def ocean():
    s = Scene('s047', '海底世界', '科学', ['科学', '海洋生物', '生态', '自然'],
              dict(w1='#9BE2EE', w2='#47A9CF', w3='#2C80B4', far='#6FC3DC', far2='#5AB2D2', sand='#F4E0B3', sand2='#E4C892',
                   c1='#F2836B', c2='#F9A9BD', c3='#F7C55E', c4='#B892E6', c5='#FF9E7A', weed='#3FAE86', weed2='#7CD6A2',
                   fish1='#FFB547', fish2='#FF7A5E', fish3='#7FE0EA', fish4='#FFE07A', white='#FFFFFF', ink='#25384A',
                   turtle='#7FC46B', turtle2='#5C9E57', turtle3='#B9E08E', jelly='#F7C2E8', jelly2='#E79AD3', rock='#4F7C9E', rock2='#6E98B8', star='#F28B4E', shell='#FBE3D2', shell2='#F2B9A0', bubble='#FFFFFF'),
              desc='明亮的浅海海底：光束从水面洒下，两侧珊瑚礁与海葵、摇曳海草，小丑鱼、鱼群、海龟、水母，沙地上有海星和贝壳。',
              stand={'ground_y': 900, 'x': [560, 1360]})
    s.layer('water', [R(0, 0, W, H, s.lg([(0, 'w1'), (.55, 'w2'), (1, 'w3')])), R(0, 0, W, 40, '#ffffff', 0, .25)], 'fade', 0)
    s.layer('rays', [beam(300, 420, 160, 520, 0, 900, s, .28), beam(820, 900, 760, 1000, 0, 900, s, .25), beam(1300, 1420, 1260, 1600, 0, 900, s, .22)], 'fade', .5, loop='glow')
    far = [P('M0,760 Q160,600 320,700 Q440,560 600,690 Q760,620 900,740 L900,860 L0,860Z', 'far', .9),
           P('M1020,740 Q1180,600 1320,690 Q1500,560 1640,680 Q1780,620 1920,700 L1920,860 L1020,860Z', 'far', .9),
           P('M0,820 Q480,760 960,800 Q1440,840 1920,790 L1920,880 L0,880Z', 'far2', .8)]
    s.layer('far_reef', far, 'rise', .15)
    random.seed(31)
    # 远处鱼群
    sch = []
    for k in range(22):
        x = 980 + random.uniform(-260, 260); y = 330 + random.uniform(-90, 90)
        sch += [E(x, y, 15, 6, 'far2', .9), poly([(x + 13, y), (x + 24, y - 7), (x + 24, y + 7)], 'far2', .9)]
    s.layer('school', sch, 'slide-r', .4, loop='drift')
    sd = [P('M0,850 Q480,800 960,840 Q1440,880 1920,830 L1920,1080 L0,1080Z', s.lg([(0, 'sand'), (1, 'sand2')]))]
    for k in range(12): sd.append(S(f'M{80 + k * 160},{900 + (k % 3) * 50} q30,-10 60,0 t60,0', 'sand2', 4, .9))
    s.layer('sand', sd, 'rise', .1)
    s.layer('caustics', [S(f'M{x},{y} q20,-8 40,0 t40,0', '#ffffff', 3, .45) for x, y in [(600, 880), (900, 920), (1200, 900), (760, 990), (1100, 1010)]], 'fade', 1.0, loop='flow')

    def coral_branch(x, y, h, col, seed):
        random.seed(seed); it = []

        def br(x0, y0, a, ln, w, d):
            x1, y1 = x0 + ln * math.cos(a), y0 + ln * math.sin(a)
            it.append(S(f'M{x0:.0f},{y0:.0f} L{x1:.0f},{y1:.0f}', col, w))
            if d > 0:
                br(x1, y1, a - random.uniform(.3, .55), ln * .72, w * .78, d - 1)
                br(x1, y1, a + random.uniform(.3, .55), ln * .72, w * .78, d - 1)
            else:
                it.append(C(x1, y1, w * .62, col))
        br(x, y, -math.pi / 2, h, 26, 3)
        return G(it)

    def fan(x, y, r, col):
        """柳珊瑚（海扇）：扇形分叉网"""
        it = []
        random.seed(int(x))
        def br(x0, y0, a, ln, w, d):
            x1, y1 = x0 + ln * math.cos(a), y0 + ln * math.sin(a)
            it.append(S(f'M{x0:.0f},{y0:.0f} Q{(x0 + x1) / 2 + random.uniform(-8, 8):.0f},{(y0 + y1) / 2:.0f} {x1:.0f},{y1:.0f}', col, w))
            if d > 0:
                br(x1, y1, a - .32, ln * .78, w * .75, d - 1); br(x1, y1, a + .32, ln * .78, w * .75, d - 1)
        for a in (-2.2, -1.57, -.94):
            br(x, y, a, r * .42, 9, 3)
        it.append(P(f'M{x},{y} L{x - r * .95},{y - r * .7} A{r},{r} 0 0,1 {x + r * .95},{y - r * .7}Z', col, .18))
        return G(it)

    def brain(x, y, r, col):
        return G([E(x, y, r, r * .7, col), *[S(f'M{x - r * .8},{y - r * .4 + k * r * .25} q{r * .2},-{r * .15} {r * .4},0 t{r * .4},0 t{r * .4},0 t{r * .4},0', 'white', 3, .35) for k in range(4)]])

    def anemone(x, y, sc, col):
        it = [E(x, y, 50 * sc, 20 * sc, 'c5')]
        for k in range(11):
            a = -math.pi / 2 + (k - 5) * .22
            it.append(S(f'M{x + (k - 5) * 8 * sc},{y - 8 * sc} q{20 * sc * math.cos(a) * 0},{-40 * sc} {70 * sc * math.cos(a)},{70 * sc * math.sin(a)}', col, 9 * sc))
        return G(it)
    lr = [E(240, 860, 280, 110, 'rock'), E(160, 800, 160, 90, 'rock2'), E(420, 840, 140, 70, 'rock2'),
          coral_branch(150, 760, 120, 'c1', 1), fan(380, 790, 120, 'c4'), brain(480, 830, 70, 'c3'), coral_branch(60, 840, 90, 'c2', 4)]
    rr_ = [E(1700, 860, 300, 110, 'rock'), E(1780, 800, 170, 90, 'rock2'), E(1500, 850, 130, 60, 'rock2'),
           coral_branch(1800, 760, 130, 'c2', 2), fan(1580, 800, 110, 'c3'), brain(1460, 840, 60, 'c4'), coral_branch(1880, 860, 90, 'c1', 6)]
    s.layer('reef_left', lr, 'slide-l', .35)
    s.layer('reef_right', rr_, 'slide-r', .4)
    s.layer('anemone', [anemone(300, 860, 1.0, 'c2'), anemone(1680, 870, .9, 'c3')], 'grow', .6, loop='sway')
    wd = []
    for x, h, col in [(560, 260, 'weed'), (600, 200, 'weed2'), (1320, 240, 'weed'), (1370, 300, 'weed2'), (40, 340, 'weed'), (1880, 320, 'weed2')]:
        y0 = 880
        wd.append(P(f'M{x - 8},{y0} C{x - 40},{y0 - h * .3} {x + 30},{y0 - h * .6} {x},{y0 - h} C{x + 50},{y0 - h * .6} {x - 10},{y0 - h * .3} {x + 10},{y0}Z', col))
    s.layer('seaweed', wd, 'grow', .55, loop='sway')

    def fish(x, y, sc, body, flip=False, stripes=False):
        f = -1 if flip else 1
        it = [P(f'M{x + f * 50 * sc},{y} Q{x},{y - 34 * sc} {x - f * 46 * sc},{y} Q{x},{y + 34 * sc} {x + f * 50 * sc},{y}Z', body, extra='filter="url(#shs)"'),
              poly([(x - f * 40 * sc, y), (x - f * 76 * sc, y - 26 * sc), (x - f * 70 * sc, y), (x - f * 76 * sc, y + 26 * sc)], body),
              P(f'M{x - f * 4 * sc},{y - 26 * sc} q{-f * 18 * sc},{-20 * sc} {-f * 34 * sc},{-8 * sc} q{f * 10 * sc},{6 * sc} {f * 14 * sc},{12 * sc}Z', body)]
        if stripes:
            cpi = s.clip(f'<path d="M{x + f * 50 * sc},{y} Q{x},{y - 34 * sc} {x - f * 46 * sc},{y} Q{x},{y + 34 * sc} {x + f * 50 * sc},{y}Z"/>')
            it.append(G([R(x + f * 18 * sc - 7 * sc, y - 40 * sc, 14 * sc, 80 * sc, 'white'), R(x - f * 16 * sc - 7 * sc, y - 40 * sc, 14 * sc, 80 * sc, 'white')], f'clip-path="{cpi}"'))
        it += [C(x + f * 30 * sc, y - 6 * sc, 7 * sc, 'white'), C(x + f * 32 * sc, y - 6 * sc, 4 * sc, 'ink')]
        return G(it)
    s.layer('fish', [fish(330, 770, 1.0, 'fish2', stripes=True), fish(440, 720, .8, 'fish2', True, True), fish(1250, 560, 1.0, 'fish1', True),
                     fish(1500, 470, .7, 'fish3'), fish(660, 520, .8, 'fish4', True), fish(1660, 640, .6, 'fish1')], 'slide-r', .75, loop='bob')
    # 海龟
    tx, ty = 480, 330
    tt = [rot([E(tx - 70, ty + 30, 40, 14, 'turtle2'), E(tx + 70, ty - 40, 50, 16, 'turtle2'), E(tx - 60, ty - 40, 34, 12, 'turtle2'), E(tx + 50, ty + 46, 34, 12, 'turtle2'),
               E(tx + 110, ty, 32, 24, 'turtle'), C(tx + 124, ty - 6, 5, 'ink'),
               E(tx, ty, 100, 66, 'turtle2', extra='filter="url(#shs)"'), E(tx, ty - 4, 88, 56, 'turtle'),
               poly([(tx - 20, ty - 30), (tx + 20, ty - 30), (tx + 34, ty), (tx + 20, ty + 30), (tx - 20, ty + 30), (tx - 34, ty)], 'turtle3', .55),
               poly([(tx - 70, ty - 20), (tx - 40, ty - 34), (tx - 34, ty), (tx - 40, ty + 30), (tx - 72, ty + 16)], 'turtle3', .45),
               poly([(tx + 70, ty - 20), (tx + 40, ty - 34), (tx + 34, ty), (tx + 40, ty + 30), (tx + 72, ty + 16)], 'turtle3', .45)], -12, tx, ty)]
    s.layer('turtle', tt, 'slide-r', .9, loop='bob')
    # 水母
    jl = []
    for x, y, sc in [(1580, 220, 1.0), (1760, 340, .7)]:
        jl += [P(f'M{x - 60 * sc},{y} A{60 * sc},{56 * sc} 0 0,1 {x + 60 * sc},{y} Q{x + 40 * sc},{y + 10 * sc} {x + 20 * sc},{y + 4 * sc} Q{x},{y + 14 * sc} {x - 20 * sc},{y + 4 * sc} Q{x - 40 * sc},{y + 10 * sc} {x - 60 * sc},{y}Z', 'jelly', .92),
               E(x - 18 * sc, y - 28 * sc, 18 * sc, 10 * sc, '#ffffff', .5)]
        for k in range(5):
            xx = x + (k - 2) * 22 * sc
            jl.append(S(f'M{xx},{y + 6 * sc} q{12 * sc},{30 * sc} 0,{60 * sc} t0,{60 * sc}', 'jelly2', 4 * sc, .8))
    s.layer('jellyfish', jl, 'fade', 1.0, loop='bob')
    # 沙地小物
    sm = []
    for x, y, sc, a in [(720, 960, 1, 10), (1460, 990, .8, -20)]:
        pts = []
        for k in range(10):
            rr = (38 if k % 2 == 0 else 16) * sc; aa = -math.pi / 2 + k * math.pi / 5
            pts.append((x + rr * math.cos(aa), y + rr * math.sin(aa)))
        sm.append(rot([poly(pts, 'star'), C(x, y, 8 * sc, 'c3', .6)], a, x, y))
    for x, y in [(880, 1000), (1240, 970)]:
        sm += [P(f'M{x - 30},{y} A30,30 0 0,1 {x + 30},{y}Z', 'shell'), *[S(f'M{x},{y} L{x + 28 * math.cos(-math.pi + k * math.pi / 5):.0f},{y + 28 * math.sin(-math.pi + k * math.pi / 5):.0f}', 'shell2', 3) for k in range(1, 5)], R(x - 10, y, 20, 8, 'shell2', 3)]
    s.layer('seabed_items', sm, 'pop', 1.1)
    random.seed(8)
    bb = []
    for k in range(18):
        x = random.choice([random.uniform(100, 500), random.uniform(1400, 1850), random.uniform(600, 1300)]); y = random.uniform(120, 760); r = random.uniform(5, 14)
        bb += [C(x, y, r, 'bubble', .35), S(f'M{x - r * .5},{y - r * .2} a{r * .55},{r * .55} 0 0,1 {r * .5},{-r * .45}', 'bubble', 2, .9)]
    s.layer('bubbles', bb, 'fade', 1.2, loop='bob')
    return s


# ============ s048 恐龙化石馆 ============
def dinomuseum():
    s = Scene('s048', '恐龙化石馆', '科学', ['科学', '古生物', '恐龙', '博物馆'],
              dict(wall1='#D6E3EC', wall2='#BCCFDD', arch='#F4F8FB', win1='#CDE8F5', win2='#F7FCFF', trim='#A9BDCC',
                   floor1='#D6AE82', floor2='#B98D66', plinth='#C27C5C', plinth2='#A3624A', top='#D99878',
                   bone='#FFF5E2', bone2='#EAD7B4', bone3='#D2BA92', rod='#7E8792', case='#FFFFFF', glass='#D9F1F4',
                   stone='#BCA68C', stone2='#9E876F', egg='#F0E2C8', egg2='#DCC7A2', rope='#C8455A', post='#D2A957', ban1='#5FA38E', ban2='#F2A65A', ban3='#E57766', foot='#B68E68'),
              desc='恐龙化石展厅：拱窗下的展台上是一副完整的长颈蜥脚类恐龙骨架，两侧展柜陈列菊石和恐龙蛋，红绳围栏与地面脚印。',
              stand={'ground_y': 930, 'x': [560, 1360]})
    bg = [R(0, 0, W, 800, s.lg([(0, 'wall1'), (1, 'wall2')])), R(0, 760, W, 40, 'trim')]
    for x in range(0, W, 240): bg.append(R(x, 0, 6, 760, 'trim', 0, .35))
    s.layer('wall', bg, 'fade', 0)
    wn = []
    for x in (330, 960, 1590):
        wn += [P(f'M{x - 150},620 L{x - 150},200 A150,150 0 0,1 {x + 150},200 L{x + 150},620Z', 'arch', extra='filter="url(#shs)"'),
               P(f'M{x - 126},600 L{x - 126},204 A126,126 0 0,1 {x + 126},204 L{x + 126},600Z', s.lg([(0, 'win1'), (1, 'win2')])),
               R(x - 4, 80, 8, 520, 'arch'), R(x - 126, 330, 252, 8, 'arch'), R(x - 126, 470, 252, 8, 'arch'), R(x - 166, 612, 332, 18, 'trim', 6)]
    s.layer('windows', wn, 'fade', .2)
    s.layer('light', [beam(840, 1080, 600, 1160, 200, 1000, s, .25), beam(220, 440, 100, 520, 200, 1000, s, .18), beam(1480, 1700, 1400, 1820, 200, 1000, s, .18)], 'fade', .7, loop='glow')
    bn = []
    for x, col in [(110, 'ban1'), (1810, 'ban2')]:
        bn += [R(x - 60, 110, 120, 8, 'rod', 4), P(f'M{x - 50},118 L{x + 50},118 L{x + 50},420 L{x},380 L{x - 50},420Z', col), C(x, 220, 30, '#ffffff', .85),
               P(f'M{x - 16},234 Q{x - 6},200 {x + 8},206 Q{x + 22},210 {x + 18},228 Z', col, .8)]
    s.layer('banners', bn, 'drop', .5, loop='sway')
    fl = [R(0, 800, W, 280, s.lg([(0, 'floor1'), (1, 'floor2')]))]
    for x in range(-200, W + 200, 160): fl.append(S(f'M{x},800 L{x + (x - 960) * .3:.0f},1080', 'floor2', 3, .45))
    for yy in (850, 930, 1030): fl.append(S(f'M0,{yy} L{W},{yy}', 'floor2', 2, .4))
    for k, (x, y) in enumerate([(240, 1000), (360, 960), (1560, 990), (1690, 950)]):
        fl.append(G([E(x, y, 22, 14, 'foot', .7), *[E(x + dx, y - 22, 7, 16, 'foot', .7, f'transform="rotate({dx} {x + dx} {y - 22})"') for dx in (-18, 0, 18)]]))
    s.layer('floor', fl, 'rise', .1)
    # 展台
    pl = [shadow(990, 812, 620, 16, .2), R(380, 730, 1220, 72, 'plinth', 10), R(380, 724, 1220, 18, 'top', 8), R(380, 790, 1220, 12, 'plinth2', 4)]
    s.layer('plinth', pl, 'rise', .3)
    # 骨架：脊柱（颈—背—尾）
    sk = []
    neck = ((800, 470), (690, 440), (620, 300), (520, 230))
    back = ((1220, 470), (1100, 420), (920, 420), (800, 470))
    tail = ((1220, 470), (1370, 500), (1500, 560), (1600, 700))
    # 支撑杆
    for x, y in [(700, 400), (1010, 432), (1400, 520), (1540, 610)]:
        sk.append(R(x - 3, y, 6, 726 - y, 'rod'))
    # 腿（后腿在后，颜色稍深）
    def leg(x, y, ln, dark, back_leg):
        col = 'bone2' if dark else 'bone'
        kx = x + (14 if back_leg else -10)
        return G([R(x - 22, y, 44, ln * .52, col, 20), C(kx, y + ln * .52, 22, col), R(kx - 17, y + ln * .52, 34, ln * .48 - 10, col, 16),
                  P(f'M{kx - 26},{y + ln - 4} L{kx + 34},{y + ln - 4} Q{kx + 30},{y + ln - 26} {kx},{y + ln - 26}Z', col)])
    sk += [leg(860, 490, 236, True, False), leg(1170, 500, 226, True, True)]
    # 肋骨
    for k in range(9):
        t = .1 + k * .1
        x, y = bez(*back[::-1], t) if False else bez(back[3], back[2], back[1], back[0], t)
        ln = 120 - abs(k - 4) * 12
        sk.append(S(f'M{x:.0f},{y + 6:.0f} q{-24:.0f},{ln * .55:.0f} {6:.0f},{ln:.0f}', 'bone2', 11))
    # 脊椎
    def vert(p0, p1, p2, p3, n, s0, s1, spine=True):
        it = []
        for k in range(n):
            t = k / (n - 1)
            x, y = bez(p0, p1, p2, p3, t); dx, dy = bez_d(p0, p1, p2, p3, t)
            a = math.degrees(math.atan2(dy, dx)); sz = s0 + (s1 - s0) * t
            seg = [R(x - sz * .55, y - sz * .45, sz * 1.1, sz * .9, 'bone', sz * .3)]
            if spine: seg.append(R(x - sz * .18, y - sz * 1.05, sz * .36, sz * .7, 'bone', sz * .15))
            it.append(rot(seg, a, x, y))
        return it
    sk += vert(*back, 12, 34, 34)
    sk += vert(*neck, 16, 32, 15, spine=False)
    sk += vert(*tail, 24, 32, 7)
    # 头骨
    hx, hy = 500, 222
    sk += [rot([P(f'M{hx - 70},{hy} Q{hx - 64},{hy - 30} {hx - 20},{hy - 32} Q{hx + 30},{hy - 36} {hx + 34},{hy - 6} Q{hx + 30},{hy + 20} {hx},{hy + 16} L{hx - 66},{hy + 14}Z', 'bone'),
                C(hx + 2, hy - 12, 10, 'bone3'), E(hx - 34, hy - 6, 14, 7, 'bone3'), S(f'M{hx - 66},{hy + 6} L{hx - 10},{hy + 8}', 'bone3', 3)], 12, hx, hy)]
    # 前腿（前景层）
    sk += [leg(830, 480, 248, False, False), leg(1200, 490, 236, False, True)]
    # 肩胛与盆骨
    sk += [E(840, 470, 50, 32, 'bone', extra='transform="rotate(-30 840 470)"'), E(1200, 470, 62, 42, 'bone'), C(1200, 470, 16, 'bone3')]
    s.layer('skeleton', [G(sk, 'filter="url(#shs)"')], 'rise', .55)

    # 展柜
    def case(x, content):
        return G([shadow(x, 900, 130, 12, .2), R(x - 100, 760, 200, 140, 'plinth2', 10), R(x - 110, 748, 220, 20, 'plinth', 6),
                  R(x - 100, 560, 200, 190, 'glass', 8, .6, 'filter="url(#shs)"'), *content,
                  S(f'M{x - 100},560 L{x + 100},560 L{x + 100},748 L{x - 100},748Z', 'case', 6), S(f'M{x - 70},580 L{x - 30},620', 'case', 6, .8)])
    sp = ' '.join(f'L{200 + (3 + t * 3.6) * math.cos(t):.1f},{676 + (3 + t * 3.6) * math.sin(t):.1f}' for t in [q * .25 for q in range(1, 50)])
    am = [E(200, 680, 64, 62, 'stone'), C(200, 676, 54, 'stone2'), S(f'M200,676 {sp}', 'bone', 5)]
    eg = [E(1740, 720, 86, 26, 'stone2'), E(1700, 690, 26, 34, 'egg'), E(1744, 682, 28, 36, 'egg2'), E(1786, 694, 26, 32, 'egg'), E(1692, 680, 8, 12, '#ffffff', .6)]
    s.layer('cases', [case(200, am), case(1740, eg)], 'pop', .8)
    # 红绳围栏
    rp = []
    posts = [420, 640, 1340, 1560]
    for x in posts: rp += [E(x, 900, 30, 8, 'post'), R(x - 6, 820, 12, 80, 'post', 4), C(x, 816, 12, 'post')]
    for a, b in [(420, 640), (1340, 1560)]: rp.append(S(f'M{a},{826} Q{(a + b) / 2},{870} {b},{826}', 'rope', 8))
    s.layer('rope', rp, 'rise', .95)
    # 悬挂翼龙骨架
    px, py = 1380, 170
    pt = [S(f'M{px},0 L{px},{py - 10}', 'rod', 2), S(f'M{px - 240},0 L{px - 180},{py}', 'rod', 2, .6), S(f'M{px + 240},0 L{px + 180},{py}', 'rod', 2, .6),
          S(f'M{px - 30},{py} L{px - 120},{py - 20} L{px - 260},{py + 20}', 'bone', 8), S(f'M{px + 30},{py} L{px + 120},{py - 20} L{px + 260},{py + 20}', 'bone', 8),
          P(f'M{px - 120},{py - 16} L{px - 260},{py + 20} L{px - 40},{py + 20}Z', 'bone', .35), P(f'M{px + 120},{py - 16} L{px + 260},{py + 20} L{px + 40},{py + 20}Z', 'bone', .35),
          E(px, py + 6, 40, 16, 'bone'), P(f'M{px - 34},{py - 4} L{px - 110},{py + 12} L{px - 36},{py + 14}Z', 'bone'), P(f'M{px - 30},{py - 4} L{px - 4},{py - 40} L{px - 18},{py - 2}Z', 'bone'), S(f'M{px + 36},{py + 8} L{px + 80},{py + 20}', 'bone', 6)]
    s.layer('pterosaur', [G(pt, 'filter="url(#shs)"')], 'drop', 1.1, loop='bob')
    return s


# ============ s049 天文台星空 ============
def observatory():
    s = Scene('s049', '天文台星空', '科学', ['科学', '天文', '星座', '夜晚'],
              dict(sky1='#1D2453', sky2='#353B82', sky3='#7B66B4', horizon='#F4A8A6', star='#FFFFFF', star2='#FFE9A8', milky='#C9C3FF', moon='#FFF0C4',
                   hill1='#56689E', hill2='#3F5389', hill3='#2E4272', dome='#E8EEF6', dome2='#C3CEDD', wall='#D3DCE8', slit='#262B57', scope='#5C6A8C', scope2='#A1ADC8',
                   glow='#FFD98A', line='#C8D0FF', tree='#1E2C50', meteor='#FFFFFF'),
              desc='晴朗星空下的天文台：银河斜贯夜空，北斗七星与北极星连线，弯月、流星，山丘上圆顶天文台开着观测缝，近处一架望远镜。',
              stand={'ground_y': 900, 'x': [520, 1300]})
    s.layer('sky', [R(0, 0, W, H, s.lg([(0, 'sky1'), (.55, 'sky2'), (.85, 'sky3'), (1, 'horizon')]))], 'fade', 0)
    mw = [rot([E(960, 360, 1100, 120, 'milky', .22, 'filter="url(#b40)"'), E(900, 360, 800, 60, 'milky', .25, 'filter="url(#b20)"'), E(1100, 350, 400, 40, '#ffffff', .18, 'filter="url(#b20)"')], -22, 960, 360)]
    random.seed(17)
    for _ in range(160):
        t = random.uniform(-1, 1); x = 960 + t * 1000; y = 360 - math.tan(math.radians(22)) * t * 1000 + random.gauss(0, 50)
        mw.append(C(x, y, random.uniform(.8, 2.2), 'star', random.uniform(.4, .9)))
    s.layer('milkyway', mw, 'fade', .2)
    random.seed(3)
    st = []
    for _ in range(110):
        x, y = random.uniform(0, W), random.uniform(0, 640); r = random.uniform(1.2, 3)
        st.append(C(x, y, r, 'star' if random.random() < .8 else 'star2', random.uniform(.5, 1)))
    s.layer('stars', st, 'fade', .3, loop='twinkle')

    def spark(x, y, r, col):
        return G([P(f'M{x},{y - r} Q{x + r * .18},{y - r * .18} {x + r},{y} Q{x + r * .18},{y + r * .18} {x},{y + r} Q{x - r * .18},{y + r * .18} {x - r},{y} Q{x - r * .18},{y - r * .18} {x},{y - r}Z', col),
                  C(x, y, r * 1.2, col, .25, 'filter="url(#b6)"')])
    # 北斗七星（勺形）+ 北极星
    dip = [(1180, 230), (1216, 278), (1306, 268), (1294, 216), (1366, 202), (1430, 210), (1494, 248)]  # 天枢 天璇 天玑 天权 玉衡 开阳 摇光
    cs = [S('M' + ' L'.join(f'{x},{y}' for x, y in [dip[0], dip[1], dip[2], dip[3], dip[0]]), 'line', 2.5, .55),
          S('M' + ' L'.join(f'{x},{y}' for x, y in dip[3:]), 'line', 2.5, .55)]
    pol = (dip[0][0] + (dip[0][0] - dip[1][0]) * 4.6, dip[0][1] + (dip[0][1] - dip[1][1]) * 1.1)
    pol = (1180 - 36 * 4.3, 230 - 48 * 4.3)
    cs.append(S(f'M{dip[0][0]},{dip[0][1]} L{pol[0] + 8:.0f},{pol[1] + 10:.0f}', 'line', 2, .3, extra='stroke-dasharray="6 10"'))
    for x, y in dip: cs.append(spark(x, y, 12, 'star2'))
    cs.append(spark(pol[0], pol[1], 16, 'star'))
    s.layer('big_dipper', cs, 'fade', .6, loop='glow')
    # 弯月（亮面朝右下）
    cm = s.clip('<circle cx="330" cy="170" r="70"/>')
    s.layer('moon', [C(330, 170, 140, 'moon', .2, 'filter="url(#b40)"'), G([C(330, 170, 70, 'moon'), C(296, 150, 66, 'sky1')], f'clip-path="{cm}"')], 'fade', .4)
    s.layer('meteor', [P('M560,360 L820,280 L824,286 Z', s.lg([(0, 'meteor', 0), (1, 'meteor', .9)], 560, 0, 820, 0, units=True)), C(822, 282, 5, 'meteor')], 'slide-r', 1.2, loop='twinkle')
    # 山丘
    s.layer('hills_far', [P('M0,700 Q300,600 640,660 Q1000,720 1300,620 Q1600,540 1920,620 L1920,1080 L0,1080Z', 'hill1')], 'rise', .15)
    s.layer('hills_near', [P('M0,820 Q400,760 800,800 Q1200,840 1400,700 Q1560,620 1920,640 L1920,1080 L0,1080Z', 'hill2'),
                           P('M0,900 Q500,860 960,890 Q1400,920 1920,880 L1920,1080 L0,1080Z', 'hill3'),
                           *[pine(x, y, sc, 'tree', 'hill2', 'tree') for x, y, sc in [(60, 830, .6), (150, 840, .45), (1860, 660, .55), (1240, 770, .4)]]], 'rise', .25)
    # 天文台
    ox, oy = 1590, 660
    ob = [shadow(ox, oy + 6, 220, 14, .3), R(ox - 170, oy - 220, 340, 226, 'wall', 8, extra='filter="url(#sh)"'), R(ox - 170, oy - 230, 340, 18, 'dome2', 6),
          P(f'M{ox - 180},{oy - 228} A180,180 0 0,1 {ox + 180},{oy - 228}Z', 'dome'),
          P(f'M{ox - 180},{oy - 228} A180,180 0 0,1 {ox},{oy - 408} L{ox},{oy - 228}Z', 'dome2', .35)]
    # 观测缝（打开）+ 望远镜
    ob += [P(f'M{ox - 30},{oy - 228} L{ox - 30},{oy - 400} Q{ox},{oy - 412} {ox + 30},{oy - 400} L{ox + 30},{oy - 228}Z', 'slit'),
           rot([R(ox - 18, oy - 400, 36, 150, 'scope', 8), R(ox - 22, oy - 404, 44, 22, 'scope2', 6)], -28, ox, oy - 260)]
    for k in range(1, 6): ob.append(S(f'M{ox - 180 + k * 60},{oy - 228} Q{ox - 180 + k * 60},{oy - 300} {ox},{oy - 408}', 'dome2', 2, .5))
    ob += [R(ox - 40, oy - 120, 80, 126, 'scope', 6), R(ox - 32, oy - 112, 64, 118, 'glow', 4, .9), R(ox + 80, oy - 170, 50, 50, 'glow', 6, .85), R(ox - 130, oy - 170, 50, 50, 'glow', 6, .85),
           R(ox - 60, oy - 6, 120, 12, 'dome2', 4)]
    s.layer('observatory', ob, 'rise', .5)
    s.layer('window_glow', [C(ox, oy - 60, 120, 'glow', .3, 'filter="url(#b40)"'), C(ox + 105, oy - 145, 50, 'glow', .35, 'filter="url(#b20)"'), C(ox - 105, oy - 145, 50, 'glow', .35, 'filter="url(#b20)"')], 'fade', 1.0, loop='glow')
    # 近景望远镜（三脚架）
    tx, ty = 360, 900
    tp = [shadow(tx, ty, 140, 12, .3), S(f'M{tx},{ty - 190} L{tx - 110},{ty} M{tx},{ty - 190} L{tx + 110},{ty} M{tx},{ty - 190} L{tx + 10},{ty + 6}', 'scope2', 10),
          S(f'M{tx - 60},{ty - 90} L{tx + 60},{ty - 90}', 'scope', 5), C(tx, ty - 196, 18, 'scope'),
          rot([R(tx - 150, ty - 236, 300, 56, 'dome', 26, extra='filter="url(#shs)"'), R(tx + 130, ty - 244, 48, 72, 'scope', 14), R(tx - 170, ty - 222, 40, 28, 'scope', 8), R(tx - 40, ty - 236, 26, 56, 'scope2', 4),
                 R(tx - 70, ty - 270, 90, 26, 'scope', 10)], -24, tx, ty - 208)]
    s.layer('telescope', tp, 'slide-l', .7)
    random.seed(44)
    s.layer('fireflies', [C(random.uniform(500, 1300), random.uniform(820, 940), random.uniform(3, 5), 'glow', .8) for _ in range(10)], 'fade', 1.2, loop='twinkle')
    s.vignette = .18
    return s


# ============ s050 太空站 ============
def spacestation():
    s = Scene('s050', '太空站', '科学', ['科学', '航天', '天宫课堂', '宇宙'],
              dict(sp1='#141A3C', sp2='#28306E', sp3='#4C3F88', star='#FFFFFF', star2='#FFE9B0', earth1='#5BB3E6', earth2='#2F7FC2', earth3='#1F5E9C',
                   land='#7CC48E', land2='#B3DC8C', land3='#E9D49A', cloudE='#FFFFFF', atm='#9FE6FF', mod='#F1F4F8', mod2='#CED7E2', mod3='#A6B3C3',
                   gold='#EDBB5C', gold2='#C9973E', panel='#28468A', panel2='#3E68B8', grid='#93B2EA', truss='#8B96A8', red='#EE5A4A', sun='#FFF3C4', moon='#ECE7F4', moon2='#CFC6E0'),
              desc='近地轨道上的空间站：T 字形舱段、巨大的太阳能帆板、对接的飞船与机械臂，下方是蓝色地球与大气光边，远处有月亮和闪烁的星星。',
              stand={'ground_y': 900, 'x': [560, 1360]})
    s.layer('space', [R(0, 0, W, H, s.lg([(0, 'sp1'), (.7, 'sp2'), (1, 'sp3')])), C(120, 110, 300, s.rg([(0, 'sun', .55), (.35, 'sun', .18), (1, 'sun', 0)])), C(120, 110, 36, '#ffffff', .95, 'filter="url(#b6)"')], 'fade', 0, loop=None)
    random.seed(9)
    st = [C(random.uniform(0, W), random.uniform(0, 760), random.uniform(1, 2.8), 'star' if random.random() < .8 else 'star2', random.uniform(.4, 1)) for _ in range(150)]
    s.layer('stars', st, 'fade', .15, loop='twinkle')
    cm = s.clip('<circle cx="1720" cy="150" r="56"/>')
    s.layer('moon', [C(1720, 150, 56, 'moon'), G([C(1700, 140, 12, 'moon2'), C(1745, 170, 9, 'moon2'), C(1730, 120, 7, 'moon2'), C(1760, 160, 60, 'sp1', .35)], f'clip-path="{cm}"')], 'fade', .3)
    # 地球
    ex, ey, er = 960, 2150, 1380
    cpe = s.clip(f'<circle cx="{ex}" cy="{ey}" r="{er}"/>')
    random.seed(2)
    lands = [P('M300,900 C380,820 520,800 640,830 C720,850 760,900 700,940 C640,980 520,960 460,1000 C400,1040 320,1020 300,980Z', 'land'),
             P('M1100,840 C1200,800 1320,810 1400,860 C1480,900 1460,960 1380,980 C1300,1000 1240,960 1180,970 C1110,980 1060,900 1100,840Z', 'land'),
             P('M1650,900 C1720,860 1820,880 1880,930 L1900,1080 L1640,1080 C1610,1000 1620,940 1650,900Z', 'land'),
             P('M1180,880 C1230,860 1300,870 1320,900 C1300,930 1230,930 1190,915Z', 'land3', .8), P('M420,900 C470,880 560,870 600,900 C560,920 470,930 420,915Z', 'land2', .8)]
    clouds_e = [E(820, 860, 160, 22, 'cloudE', .85), E(980, 900, 120, 18, 'cloudE', .75), E(1500, 870, 140, 20, 'cloudE', .8), E(560, 1000, 200, 24, 'cloudE', .7),
                E(1300, 1040, 180, 22, 'cloudE', .7), S('M200,960 q60,-30 120,0 t120,0', 'cloudE', 10, .6)]
    s.layer('earth', [C(ex, ey, er + 60, 'atm', .35, 'filter="url(#b20)"'), C(ex, ey, er, s.lg([(0, 'earth1'), (.25, 'earth2'), (1, 'earth3')])), G(lands, f'clip-path="{cpe}"'),
                      C(ex, ey, er, s.rg([(.9, '#ffffff', 0), (1, 'atm', .55)]))], 'rise', .2)
    s.layer('earth_clouds', [G(clouds_e, f'clip-path="{cpe}"')], 'fade', .6, loop='drift')
    s.layer('atmosphere', [S(f'M{ex - er},{ey} A{er},{er} 0 0,1 {ex + er},{ey}', 'atm', 10, .8), S(f'M{ex - er - 14},{ey} A{er + 14},{er + 14} 0 0,1 {ex + er + 14},{ey}', 'atm', 14, .25)], 'fade', .5, loop='glow')

    # 太阳能帆板
    def wing(x, y, w, h):
        it = [R(x, y, w, h, 'panel', 4, extra='filter="url(#shs)"')]
        for k in range(1, 6): it.append(R(x + k * w / 6 - 1.5, y, 3, h, 'grid', 0, .5))
        for k in range(1, 12): it.append(R(x, y + k * h / 12 - 1, w, 2, 'grid', 0, .35))
        it += [R(x + 3, y + 3, w * .45, h - 6, 'panel2', 3, .45)]
        return G(it)
    cx_, cy_ = 960, 380
    wg = [R(250, cy_ - 4, 1420, 8, 'truss')]
    for x0 in (220, 1500):
        wg += [wing(x0, cy_ - 250, 200, 220), wing(x0, cy_ + 30, 200, 220), R(x0 + 96, cy_ - 30, 8, 60, 'truss')]
    wg += [wing(cx_ - 210, cy_ - 330, 150, 120), wing(cx_ + 60, cy_ - 330, 150, 120), R(cx_ - 60, cy_ - 274, 120, 8, 'truss')]
    s.layer('solar_wings', wg, 'grow', .55, origin=f'{cx_} {cy_}')

    def module(x, y, w, h, gold=False):
        it = [R(x, y, w, h, 'mod', h / 2.6, extra='filter="url(#sh)"'), R(x, y + h * .62, w, h * .38, 'mod2', h / 3, .9)]
        for k in range(1, int(w // 70)):
            it.append(R(x + k * 70 - 2, y + 4, 4, h - 8, 'mod3', 2, .6))
        if gold: it += [R(x + w * .3, y + 2, w * .4, h - 4, 'gold', 6, .9), R(x + w * .3, y + h * .6, w * .4, h * .38, 'gold2', 4, .6)]
        it.append(R(x + 10, y + h * .18, w - 20, h * .12, '#ffffff', 6, .55))
        return G(it)
    md = [module(520, cy_ - 40, 340, 80, True), module(1060, cy_ - 40, 340, 80, True),
          C(cx_, cy_, 66, 'mod', extra='filter="url(#sh)"'), C(cx_, cy_, 50, 'mod2'), C(cx_, cy_, 26, 'mod3'), C(cx_ - 14, cy_ - 16, 12, '#ffffff', .7),
          R(cx_ - 46, cy_ - 270, 92, 220, 'mod', 30, extra='filter="url(#sh)"'), R(cx_ + 12, cy_ - 270, 34, 220, 'mod2', 16, .8), R(cx_ - 46, cy_ - 160, 92, 40, 'gold', 8, .9),
          R(cx_ - 28, cy_ - 286, 56, 24, 'mod3', 8), R(cx_ - 4, cy_ - 300, 8, 18, 'red', 3)]
    for x in (520, 1400): md += [E(x, cy_, 14, 40, 'mod3')]
    s.layer('modules', md, 'zoom', .35, origin=f'{cx_} {cy_}', loop=None)
    # 对接飞船（下方）
    sh = [R(cx_ - 34, cy_ + 60, 68, 34, 'mod3', 8), R(cx_ - 46, cy_ + 90, 92, 70, 'mod', 30, extra='filter="url(#shs)"'), P(f'M{cx_ - 56},{cy_ + 156} L{cx_ + 56},{cy_ + 156} L{cx_ + 44},{cy_ + 236} L{cx_ - 44},{cy_ + 236}Z', 'mod2'),
          R(cx_ - 44, cy_ + 236, 88, 40, 'mod3', 8), C(cx_ - 12, cy_ + 196, 10, 'sp2'),
          wing(cx_ - 210, cy_ + 230, 150, 34), wing(cx_ + 60, cy_ + 230, 150, 34), R(cx_ - 60, cy_ + 243, 120, 6, 'truss')]
    s.layer('spacecraft', sh, 'rise', .8)
    # 机械臂
    s.layer('robot_arm', [S(f'M{cx_ + 46},{cy_ - 200} L{cx_ + 170},{cy_ - 250} L{cx_ + 280},{cy_ - 170}', 'mod', 16), C(cx_ + 170, cy_ - 250, 14, 'mod3'), C(cx_ + 46, cy_ - 200, 12, 'mod3'),
                          R(cx_ + 270, cy_ - 176, 30, 26, 'gold', 6)], 'grow', 1.0, origin=f'{cx_ + 46} {cy_ - 200}')
    # 信号灯 + 远处卫星
    s.layer('beacons', [C(520, cy_, 7, 'red'), C(1400, cy_, 7, 'red'), C(cx_, cy_ - 300, 6, 'red'), C(520, cy_, 20, 'red', .35, 'filter="url(#b6)"'), C(1400, cy_, 20, 'red', .35, 'filter="url(#b6)"')], 'fade', 1.1, loop='twinkle')
    sat = [R(1780, 700, 40, 30, 'gold', 4), R(1710, 708, 64, 14, 'panel2', 2), R(1826, 708, 64, 14, 'panel2', 2), S('M1800,700 L1800,680', 'mod2', 2), C(1800, 678, 4, 'mod')]
    s.layer('satellite', sat, 'slide-l', 1.2, loop='drift')
    s.vignette = .2
    return s


SCENES = [circuit, cells, greenhouse, weather, volcano, ocean, dinomuseum, observatory, spacestation]
