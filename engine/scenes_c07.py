from core import *
import math, random

# ================= 通用小工具（本模块与 c08 共用） =================

def shadow(x, y, rx, ry, op=.14):
    return E(x, y, rx, ry, '#2a1e30', op)


def person_run(x, y, sc, col, w=None):
    """奔跑小人图标：x,y 约为躯干中心，高约 64*sc"""
    w = w or 7 * sc
    k = lambda a, b: f'{x + a * sc:.1f},{y + b * sc:.1f}'
    return G([C(x + 8 * sc, y - 27 * sc, 6.5 * sc, col),
              S(f'M{k(5, -17)} L{k(-2, 3)}', col, w),
              S(f'M{k(5, -15)} L{k(14, -6)} L{k(22, -9)}', col, w * .72),
              S(f'M{k(4, -15)} L{k(-7, -11)} L{k(-13, -2)}', col, w * .72),
              S(f'M{k(-2, 3)} L{k(9, 12)} L{k(8, 26)}', col, w * .8),
              S(f'M{k(-2, 3)} L{k(-10, 15)} L{k(-21, 16)}', col, w * .8)])


def person_stand(x, y, sc, col):
    """站立小人：x 中心，y 脚底"""
    return G([C(x, y - 58 * sc, 8 * sc, col), R(x - 9 * sc, y - 47 * sc, 18 * sc, 26 * sc, col, 6 * sc),
              S(f'M{x - 4 * sc:.1f},{y - 22 * sc:.1f} L{x - 5 * sc:.1f},{y - 2 * sc:.1f} M{x + 4 * sc:.1f},{y - 22 * sc:.1f} L{x + 5 * sc:.1f},{y - 2 * sc:.1f}', col, 7 * sc),
              S(f'M{x - 9 * sc:.1f},{y - 42 * sc:.1f} L{x - 15 * sc:.1f},{y - 24 * sc:.1f} M{x + 9 * sc:.1f},{y - 42 * sc:.1f} L{x + 15 * sc:.1f},{y - 24 * sc:.1f}', col, 6 * sc)])


def arrow(x, y, ln, col, d=1, th=10):
    """水平箭头：从 x 开始朝 d 方向（1 右，-1 左），长 ln"""
    x2 = x + d * ln
    return G([R(min(x, x2 - d * th * 1.6), y - th / 2, abs(ln) - th * 1.6, th, col, th / 3),
              poly([(x2, y), (x2 - d * th * 2, y - th * 1.4), (x2 - d * th * 2, y + th * 1.4)], col)])


def prohibit(x, y, r, inner, red='#E5533D'):
    """禁止标志：白底 + 内图形 + 红圈斜杠"""
    a = math.radians(45)
    return G([C(x, y, r, '#ffffff', extra='filter="url(#shs)"'), *inner,
              S(f'M{x - r * .86:.1f},{y:.1f} a{r * .86:.1f},{r * .86:.1f} 0 1,0 {r * 1.72:.1f},0 a{r * .86:.1f},{r * .86:.1f} 0 1,0 {-r * 1.72:.1f},0', red, r * .22),
              S(f'M{x - r * .62:.1f},{y - r * .62:.1f} L{x + r * .62:.1f},{y + r * .62:.1f}', red, r * .2, cap='butt')])


def warn_tri(x, y, sz, inner, yel='#F7C948', blk='#2F3A48'):
    """警告三角：x 中心，y 底边"""
    h = sz * .88
    return G([P(f'M{x},{y - h} L{x + sz / 2},{y} L{x - sz / 2},{y}Z', blk, extra='filter="url(#shs)"'),
              P(f'M{x},{y - h + sz * .16} L{x + sz / 2 - sz * .11},{y - sz * .065} L{x - sz / 2 + sz * .11},{y - sz * .065}Z', yel), *inner])


def plant_pot(x, y, sc, pot, leaf, leaf2, n=6):
    """盆栽：x 中心，y 盆底"""
    it = [shadow(x, y + 2, 50 * sc, 8 * sc), P(f'M{x - 38 * sc},{y - 70 * sc} L{x + 38 * sc},{y - 70 * sc} L{x + 28 * sc},{y} L{x - 28 * sc},{y}Z', pot)]
    angs = [-2.9, -2.4, -1.9, -1.5, -1.1, -.6, -.2][:n + 1]
    for i, a in enumerate(angs):
        lx, ly = x + 46 * sc * math.cos(a), y - 70 * sc + 44 * sc * math.sin(a) - 20 * sc
        it.append(E(lx, ly, 44 * sc, 15 * sc, leaf if i % 2 else leaf2, extra=f'transform="rotate({math.degrees(a):.0f} {lx:.1f} {ly:.1f})"'))
    it.append(R(x - 42 * sc, y - 76 * sc, 84 * sc, 14 * sc, pot, 5 * sc))
    return G(it)


def skyline(s, x0, x1, base, hmin, hmax, cols, seed, win='#ffffff', wop=.45):
    random.seed(seed); it = []; x = x0
    while x < x1:
        w = random.randint(60, 130); h = random.randint(hmin, hmax)
        it.append(R(x, base - h, w, h + 4, cols[random.randint(0, len(cols) - 1)], 5))
        for wy in range(int(base - h + 18), int(base - 16), 30):
            for wx in range(x + 12, x + w - 16, 26):
                if random.random() < .5: it.append(R(wx, wy, 12, 15, win, 2, wop))
        x += w + random.randint(4, 14)
    return it


def tiles(x0, y0, x1, y1, sz, col, op=.6, th=2):
    it = []
    for x in range(int(x0), int(x1), sz): it.append(R(x, y0, th, y1 - y0, col, 0, op))
    for y in range(int(y0), int(y1), sz): it.append(R(x0, y, x1 - x0, th, col, 0, op))
    return it


def exit_sign(x, y, w, h, green, white='#ffffff', d=1):
    """安全出口标志（无字）：绿底，方向箭头 + 奔跑小人 + 门。x,y 为左上角；d=-1 镜像为朝左"""
    it = [R(x, y, w, h, green, 10, extra='filter="url(#shs)"'), R(x + 6, y + 6, w - 12, h - 12, white, 6, .12)]
    inner = [arrow(x + w * .08, y + h * .52, w * .2, white, 1, h * .1), person_run(x + w * .48, y + h * .55, h / 92, white)]
    dx = x + w * .68
    inner += [R(dx, y + h * .16, w * .2, h * .68, white, 3), R(dx + w * .03, y + h * .22, w * .14, h * .62, green, 2)]
    if d < 0:
        it.append(G(inner, f'transform="translate({2 * x + w},0) scale(-1,1)"'))
    else:
        it += inner
    return G(it)


# ================= 062 公交车内 =================
def bus():
    s = Scene('s062', '公交车内', '安全与法治', ['道德与法治', '乘车安全', '文明礼让', '安全教育'],
              dict(ceil='#F4F7F9', wall1='#EAF1F5', wall2='#DCE7EE', panel='#CBDCE5', panel2='#B8CDD9', frame='#62788A', sky1='#9FD9F4', sky2='#EAF8FF',
                   city1='#F6C8A8', city2='#BFD8EE', city3='#F7E3A4', tree='#7CC48E', tree2='#B2DFA0', seat='#4A93D4', seat2='#3577B5', prio='#F2A33A', prio2='#D9862A',
                   pole='#F4C542', pole2='#D9A82E', floor='#C3C9CF', floor2='#AEB5BD', line='#F4C542', red='#E5533D', door='#D5E0E7', glass='#C3E6F4', handle='#FAFBFC',
                   disp='#2E3640', led='#FFB547', ledg='#4CD08A', lamp='#FFFBEA'),
              desc='公交车车厢侧视：车窗外城市掠过，中央后门、黄色扶杆与吊环、蓝色座椅和橙色爱心座，配安全锤与下车按钮。', stand={'ground_y': 900, 'x': [560, 1360]})
    P_ = s.pal
    s.layer('cabin', [R(0, 0, W, 130, 'ceil'), R(0, 118, W, 12, 'panel2'), R(0, 130, W, 740, s.lg([(0, 'wall1'), (1, 'wall2')])),
                      R(0, 540, W, 330, 'panel'), R(0, 540, W, 10, 'panel2'), *[R(x, 34, 300, 30, 'lamp', 15) for x in (120, 1500)],
                      R(760, 30, 400, 40, 'lamp', 20, .9)], 'fade', 0)
    # 窗外风景（裁切在窗内）
    wins = [(40, 190, 620, 320), (1260, 190, 620, 320)]
    out = []
    for x0, y0, w, h in wins:
        cp = s.clip(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="22"/>')
        inner = [R(x0, y0, w, h, s.lg([(0, 'sky1'), (1, 'sky2')])), cloud(x0 + 160, y0 + 80, .5, op=.9), cloud(x0 + 470, y0 + 60, .35, op=.8)]
        inner += skyline(s, x0 - 20, x0 + w + 20, y0 + h - 40, 60, 180, ['city1', 'city2', 'city3'], x0)
        for k in range(5): inner.append(blob_tree(x0 + 40 + k * 140, y0 + h, .55, 'tree', 'tree2', '#8A5A3A'))
        out.append(G(inner, f'clip-path="{cp}"'))
    s.layer('outside', out, 'fade', .1, loop='drift')
    wf = []
    for x0, y0, w, h in wins:
        wf += [S(f'M{x0 + 22},{y0} L{x0 + w - 22},{y0} Q{x0 + w},{y0} {x0 + w},{y0 + 22} L{x0 + w},{y0 + h - 22} Q{x0 + w},{y0 + h} {x0 + w - 22},{y0 + h} L{x0 + 22},{y0 + h} Q{x0},{y0 + h} {x0},{y0 + h - 22} L{x0},{y0 + 22} Q{x0},{y0} {x0 + 22},{y0}Z', 'frame', 14),
               R(x0 + w / 2 - 7, y0, 14, h, 'frame'), R(x0 + 20, y0 + 70, w - 40, 6, '#ffffff', 3, .0),
               P(f'M{x0 + 60},{y0 + 20} L{x0 + 120},{y0 + 20} L{x0 + 40},{y0 + h - 20} L{x0 + 20},{y0 + h - 20}Z', '#ffffff', .18),
               P(f'M{x0 + w / 2 + 50},{y0 + 20} L{x0 + w / 2 + 80},{y0 + 20} L{x0 + w / 2 + 30},{y0 + h - 20} L{x0 + w / 2 + 16},{y0 + h - 20}Z', '#ffffff', .15),
               R(x0 - 10, y0 + h + 6, w + 20, 16, 'panel2', 8)]
    s.layer('window_frames', wf, 'pop', .25)
    # 后门
    dr = [R(740, 150, 440, 730, 'frame', 18, extra='filter="url(#sh)"')]
    for x0 in (762, 964):
        dr += [R(x0, 172, 194, 700, 'door', 10), R(x0 + 22, 196, 150, 470, s.lg([(0, 'glass'), (1, '#E6F6FC')]), 10),
               P(f'M{x0 + 40},{196} L{x0 + 80},{196} L{x0 + 44},{666} L{x0 + 22},{666}Z', '#ffffff', .35),
               R(x0 + 22, 700, 150, 150, 'panel2', 10, .6), R(x0 + (170 if x0 < 900 else 14), 380, 10, 170, 'pole', 5)]
    dr += [R(956, 172, 8, 700, '#4A5866'), R(760, 140, 400, 14, 'pole', 6)]
    s.layer('door', dr, 'rise', .3)
    # 地板
    fl = [R(0, 870, W, 210, s.lg([(0, 'floor'), (1, 'floor2')])), R(0, 870, W, 8, '#6B7480')]
    for y in range(910, 1080, 34):
        for x in range((y // 34 % 2) * 23, W, 46): fl.append(R(x, y, 22, 5, '#ffffff', 2, .22))
    fl.append(E(960, 940, 700, 60, '#ffffff', .25, 'filter="url(#b40)"'))
    fl += [R(740, 878, 440, 18, 'line', 4), *[R(760 + k * 40, 884, 20, 6, '#ffffff', 2, .5) for k in range(10)]]
    s.layer('floor', fl, 'rise', .1)

    # 座椅（侧视，面朝右）
    def seat(x, col, col2, prio=False):
        it = [shadow(x + 70, 868, 90, 8, .12), R(x + 110, 800, 16, 70, '#5E6B7A', 4), R(x + 30, 790, 140, 18, '#5E6B7A', 6),
              P(f'M{x},{600} Q{x - 6},{560} {x + 30},{556} L{x + 46},{556} Q{x + 64},{560} {x + 60},{600} L{x + 54},{760} L{x + 6},{760}Z', col),
              R(x + 4, 720, 172, 56, col, 22, extra='filter="url(#shs)"'), R(x + 20, 724, 140, 14, col2, 7, .55), R(x + 10, 576, 30, 120, col2, 12, .35),
              R(x + 2, 545, 70, 18, 'pole', 9)]
        if prio: it += [C(x + 34, 640, 16, '#ffffff', .9), P(f'M{x + 34},{650} l-9,-9 a5,5 0 0,1 9,-6 a5,5 0 0,1 9,6Z', 'red')]
        return G(it)
    s.layer('seats', [seat(70, 'seat', 'seat2'), seat(290, 'seat', 'seat2'), seat(510, 'prio', 'prio2', True),
                      seat(1250, 'prio', 'prio2', True), seat(1470, 'seat', 'seat2'), seat(1690, 'seat', 'seat2')], 'rise', .5)
    # 扶杆与横杆
    pl = [R(0, 148, W, 14, 'pole', 7), R(0, 148, W, 4, '#FFE7A0', 2)]
    for x in (700, 1210): pl += [R(x, 140, 18, 740, 'pole', 9), R(x + 3, 140, 5, 740, '#FFE7A0', 2), R(x - 10, 862, 38, 14, 'pole2', 6), R(x - 6, 470, 30, 40, 'red', 8), C(x + 9, 490, 8, '#ffffff', .9)]
    s.layer('poles', pl, 'drop', .45)
    hd = []
    for x in list(range(90, 660, 110)) + list(range(1290, 1880, 110)):
        hd += [R(x - 5, 160, 10, 64, '#5E6B7A', 4), R(x - 18, 222, 36, 14, '#5E6B7A', 6),
               S(f'M{x - 22},{262} a22,22 0 1,0 44,0 a22,22 0 1,0 -44,0', 'handle', 9), S(f'M{x - 22},{262} a22,22 0 1,0 44,0 a22,22 0 1,0 -44,0', 'panel2', 2, .7)]
    s.layer('handles', hd, 'drop', .6, loop='sway')
    # 安全锤、爱心座图标、下车按钮
    def hammer(x, y):
        return G([R(x - 30, y - 12, 60, 110, '#ffffff', 10, extra='filter="url(#shs)"'), R(x - 6, y + 10, 12, 70, 'red', 4), P(f'M{x - 22},{y + 2} L{x + 22},{y + 2} L{x + 26},{y + 14} L{x - 26},{y + 14}Z', 'red'),
                  C(x - 26, y + 8, 6, '#C9D2DA'), C(x + 26, y + 8, 6, '#C9D2DA')])
    sf = [G([hammer(350, 380)], 'transform="translate(350,380) scale(.7) translate(-350,-380)"'), G([hammer(1570, 380)], 'transform="translate(1570,380) scale(.7) translate(-1570,-380)"'),
          R(600, 420, 100, 100, '#ffffff', 16, extra='filter="url(#shs)"'), R(608, 428, 84, 84, 'prio', 12, .9), person_stand(636, 500, .95, '#ffffff'),
          S('M662,450 L668,500', '#ffffff', 5), C(670, 446, 5, '#ffffff'),
          R(1220, 420, 100, 100, '#ffffff', 16, extra='filter="url(#shs)"'), R(1228, 428, 84, 84, 'prio', 12, .9),
          P('M1270,494 l-20,-20 a11,11 0 0,1 20,-14 a11,11 0 0,1 20,14Z', '#ffffff')]
    s.layer('safety_items', sf, 'pop', .8)
    # 顶部线路屏
    ds = [R(800, 74, 320, 56, 'disp', 14, extra='filter="url(#shs)"'), R(830, 101, 260, 4, '#5E6B7A', 2)]
    s.layer('route_display', ds, 'pop', .9)
    s.layer('route_leds', [C(840 + k * 40, 103, 7, 'ledg' if k < 4 else 'led', 1 if k != 3 else 1) for k in range(7)] + [C(960, 103, 12, 'ledg', .4, 'filter="url(#b6)"')], 'fade', 1.1, loop='twinkle')
    s.layer('sunlight', [P('M120,510 L560,510 L700,870 L260,870Z', '#FFF6D8', .22), P('M1340,510 L1780,510 L1660,870 L1220,870Z', '#FFF6D8', .18),
                         E(500, 900, 220, 26, '#FFF6D8', .35, 'filter="url(#b20)"'), E(1450, 900, 220, 26, '#FFF6D8', .3, 'filter="url(#b20)"')], 'fade', 1.0, loop='glow')
    return s


# ================= 063 地铁站台 =================
def metro():
    s = Scene('s063', '地铁站台', '安全与法治', ['道德与法治', '乘车安全', '排队候车', '安全教育'],
              dict(ceil='#E9EEF3', ceil2='#D3DCE5', wall1='#EEF3F7', wall2='#DDE6EE', tile='#CFDBE5', m1='#8FD0C4', m2='#F6B89C', m3='#9FC4EC', m4='#F7D88A',
                   train='#F5F7F9', train2='#DCE3EA', stripe='#38A8D8', stripe2='#F2836B', twin='#34465A', psd='#9AAAB9', psd2='#7D8E9F', glass='#D7EEF7',
                   floor='#DDE2E8', floor2='#C9D0D8', tact='#F4C542', tact2='#E2AE2A', col='#C4D1DD', col2='#AFBFCD', sign='#2E3A48', green='#2DB36F', led='#4CD08A', red='#E5533D',
                   bench='#6FA8D8', bench2='#5288BC', lamp='#FFFFFF'),
              desc='地铁站台：彩色壁画墙、驶入的列车与全高屏蔽门，地面黄色盲道安全线和排队箭头，顶部悬挂导向牌。', stand={'ground_y': 930, 'x': [560, 1360]})
    s.layer('wall', [R(0, 0, W, 110, s.lg([(0, 'ceil'), (1, 'ceil2')])), R(0, 110, W, 760, s.lg([(0, 'wall1'), (1, 'wall2')])), *tiles(0, 110, W, 760, 60, 'tile', .55)], 'fade', 0)
    # 壁画带：抽象山丘与圆
    mu = [R(0, 150, W, 160, '#ffffff', 0, .5)]
    for k, (x, r_, col) in enumerate([(120, 120, 'm1'), (420, 160, 'm3'), (760, 110, 'm2'), (1060, 150, 'm4'), (1380, 120, 'm1'), (1700, 170, 'm3')]):
        mu.append(P(f'M{x - r_ * 1.6},310 Q{x},{310 - r_ * 1.1} {x + r_ * 1.6},310Z', col, .7))
    for x, y, r_, col in [(280, 200, 26, 'm4'), (980, 190, 22, 'm2'), (1560, 205, 28, 'm4'), (640, 210, 16, 'm1')]: mu.append(C(x, y, r_, col, .85))
    s.layer('mural', mu, 'fade', .2)
    s.layer('ceiling_lights', [*[R(x, 40, 260, 22, 'lamp', 11) for x in (80, 560, 1100, 1580)], *[E(x + 130, 64, 200, 40, '#ffffff', .5, 'filter="url(#b20)"') for x in (80, 560, 1100, 1580)]], 'fade', .3, loop='glow')
    # 列车（屏蔽门后）
    tr = [R(-40, 360, 2000, 470, s.lg([(0, 'train'), (1, 'train2')]), 40), R(-40, 700, 2000, 26, 'stripe'), R(-40, 730, 2000, 10, 'stripe2')]
    for cx in (0, 240, 720, 1200, 1680, 1920):
        tr += [R(cx - 120 + (20 if cx in (0, 1920) else 0), 420, 240 - (40 if cx in (0, 1920) else 0), 170, 'twin', 22), R(cx - 100, 432, 60, 146, '#ffffff', 16, .08)]
    for cx in (480, 960, 1440): tr += [R(cx - 100, 396, 200, 340, 'train2', 14), R(cx - 2, 396, 4, 340, '#B8C4CF'), R(cx - 84, 420, 70, 150, 'twin', 12), R(cx + 14, 420, 70, 150, 'twin', 12)]
    s.layer('train', tr, 'slide-r', .35)
    # 屏蔽门
    pd = [R(0, 300, W, 50, 'psd2'), R(0, 340, W, 10, 'psd')]
    for cx in (480, 960, 1440):
        pd += [R(cx - 140, 352, 280, 28, 'sign', 6), R(cx - 30, 358, 60, 16, '#000000', 4, .3)]
    pd += [R(0, 350, W, 480, 'glass', 0, .38)]
    for x in range(0, W + 1, 240): pd.append(R(x - 9, 350, 18, 480, 'psd', 4))
    for cx in (480, 960, 1440):
        pd += [R(cx - 3, 380, 6, 450, 'psd2'), S(f'M{cx - 120},{380} L{cx - 120},{830} M{cx + 120},{380} L{cx + 120},{830}', 'psd2', 6)]
    for x in range(40, W, 240): pd.append(P(f'M{x + 30},360 L{x + 70},360 L{x + 20},820 L{x},820Z', '#ffffff', .25))
    pd += [R(0, 760, W, 80, 'psd', 0, .75), R(0, 760, W, 6, '#ffffff', 0, .5)]
    s.layer('screen_doors', pd, 'fade', .5)
    s.layer('door_leds', [C(cx + dx, 366, 5, 'led') for cx in (480, 960, 1440) for dx in (-18, 0, 18)] + [C(cx, 366, 26, 'led', .35, 'filter="url(#b6)"') for cx in (480, 960, 1440)], 'fade', 1.1, loop='twinkle')
    # 门上提示：禁止倚靠
    st = []
    for cx in (480, 960, 1440):
        for d in (-1, 1):
            hx = cx + d * 64
            st.append(prohibit(hx, 560, 26, [R(hx - 8, 548, 16, 26, '#3A4552', 6), C(hx, 540, 7, '#3A4552')]))
    s.layer('door_stickers', st, 'pop', .8)
    # 地面：盲道安全线 + 排队箭头
    fl = [R(0, 830, W, 250, s.lg([(0, 'floor'), (1, 'floor2')])), R(0, 830, W, 6, '#B8C1CB')]
    fl += [R(0, 852, W, 34, 'tact'), *[C(x, 869, 4, 'tact2') for x in range(14, W, 22)]]
    for x in range(0, W, 120): fl.append(R(x, 900, 2, 180, '#ffffff', 0, .35))
    s.layer('floor', fl, 'rise', .1)
    qa = []
    def chev(x, y, col, up=True, sz=22):
        d = -1 if up else 1
        return S(f'M{x - sz},{y - d * sz * .5} L{x},{y + d * sz * .5} L{x + sz},{y - d * sz * .5}', col, 9)
    for cx in (480, 960, 1440):
        for dx in (-190, 190):
            qa += [chev(cx + dx, 920, 'green'), chev(cx + dx, 952, 'green', sz=26)]
        qa += [chev(cx, 920, 'stripe2', False), chev(cx, 950, 'stripe2', False, 26), R(cx - 120, 902, 4, 70, 'stripe2', 2, .0)]
    s.layer('queue_marks', qa, 'pop', .9)
    # 柱子与座椅
    cl = []
    for x in (120, 1800):
        cl += [R(x - 50, 110, 100, 760, s.lg([(0, 'col2'), (.5, 'col'), (1, 'col2')], 0, 0, 1, 0)), R(x - 60, 860, 120, 20, 'col2', 6)]
    s.layer('columns', cl, 'rise', .6)
    # 悬挂导向牌
    sg = [R(758, 0, 6, 70, '#7A8794'), R(1156, 0, 6, 70, '#7A8794'), R(720, 66, 480, 92, 'sign', 16, extra='filter="url(#sh)"')]
    sg += [R(746, 82, 100, 60, '#ffffff', 10), R(760, 92, 72, 34, 'stripe', 8), R(770, 98, 20, 14, '#ffffff', 3), R(800, 98, 20, 14, '#ffffff', 3), C(776, 132, 5, 'sign'), C(816, 132, 5, 'sign'),
           R(880, 84, 4, 56, '#ffffff', 2, .3), arrow(930, 112, 230, '#ffffff', 1, 16)]
    s.layer('hanging_sign', sg, 'drop', .7)
    return s


# ================= 064 消防站 =================
def firestation():
    s = Scene('s064', '消防站', '安全与法治', ['道德与法治', '消防安全', '职业认知', '安全教育'],
              dict(sky1='#9ED7F4', sky2='#FFF0DC', brick='#E9775F', brick2='#D2634D', trim='#FBF3E8', trim2='#E6D8C6', roof='#4E5966', door='#ECF0F3', door2='#CBD3DB',
                   truck='#E5483C', truck2='#BE3A30', chrome='#DCE2E7', glass='#BFE4F4', tire='#2F343A', apron='#DCD6CB', apron2='#C9C1B3', hatch='#F4C542',
                   tree='#69B97C', tree2='#A6DB95', trunk='#8A5A3A', hydrant='#E5483C', cone='#F28C2E', light='#FFD36E', blue='#4FA3E0', gold='#F2C14E'),
              desc='红砖消防站：中间车库门敞开露出消防车正面，左侧瞭望塔，门前消防栓、雪糕筒，车顶警灯闪烁。', stand={'ground_y': 930, 'x': [560, 1360]})
    s.layer('sky', [R(0, 0, W, 760, s.lg([(0, 'sky1'), (1, 'sky2')])), C(1700, 160, 120, 'light', .25, 'filter="url(#b40)"'), C(1700, 160, 56, 'light', .9)], 'fade', 0)
    s.layer('clouds', [cloud(560, 150, .7, op=.9), cloud(1250, 100, .55, op=.85), cloud(160, 260, .45, op=.8)], 'slide-l', .2, loop='drift')
    s.layer('trees', [blob_tree(80, 760, 1.05, 'tree', 'tree2', 'trunk'), blob_tree(1840, 760, 1.1, 'tree', 'tree2', 'trunk'), blob_tree(1720, 760, .8, 'tree2', 'tree', 'trunk')], 'grow', .5, loop='sway')
    # 主楼
    b = [R(330, 250, 1300, 520, 'brick', 0, extra='filter="url(#sh)"')]
    for y in range(262, 760, 26):
        off = 0 if (y // 26) % 2 else 40
        for x in range(330 + off, 1630, 80): b.append(R(x, y, 2, 24, 'brick2', 0, .35))
        b.append(R(330, y + 24, 1300, 2, 'brick2', 0, .3))
    b += [R(310, 226, 1340, 36, 'trim', 6), R(310, 256, 1340, 8, 'trim2'), R(330, 440, 1300, 22, 'trim', 0)]
    for x in range(400, 1600, 150):
        if 820 < x < 1080: continue
        b += [R(x, 300, 100, 110, 'trim', 10), R(x + 8, 308, 84, 94, 'glass', 6), R(x + 48, 308, 4, 94, 'trim'), P(f'M{x + 16},308 L{x + 36},308 L{x + 14},402 L{x + 8},402Z', '#ffffff', .4)]
    s.layer('building', b, 'rise', .3)
    # 徽章：圆形火焰
    em = [C(980, 345, 62, 'trim', extra='filter="url(#shs)"'), C(980, 345, 52, 'truck'), P('M980,385 Q950,372 952,345 Q956,322 975,305 Q972,330 990,338 Q996,318 990,300 Q1018,322 1010,356 Q1004,380 980,385Z', 'gold'),
          P('M980,382 Q966,372 968,356 Q972,344 980,336 Q984,352 994,356 Q996,374 980,382Z', '#ffffff', .85)]
    s.layer('emblem', em, 'pop', .7)
    # 瞭望塔
    tw = [R(150, 170, 180, 600, 'brick2', 0, extra='filter="url(#sh)"'), P('M130,175 L240,90 L350,175Z', 'roof'), R(130, 170, 220, 14, 'trim', 4),
          R(178, 210, 124, 90, 'trim', 10), R(186, 218, 108, 74, 'glass', 6), R(196, 440, 88, 120, 'trim', 10), R(204, 448, 72, 104, 'glass', 6),
          R(170, 330, 140, 12, 'trim', 4), C(240, 260, 22, 'gold'), R(237, 70, 6, 24, 'roof')]
    s.layer('tower', tw, 'rise', .4)
    # 车库门
    bays = []
    for x0, open_ in ((420, False), (800, True), (1180, False)):
        bays += [R(x0 - 14, 490, 388, 290, 'trim', 12)]
        if open_:
            bays.append(R(x0, 504, 360, 266, '#3B3F46', 4))
            bays.append(R(x0, 504, 360, 34, 'door2', 0))
        else:
            bays.append(R(x0, 504, 360, 266, 'door', 4))
            for k in range(8): bays.append(R(x0, 520 + k * 32, 360, 3, 'door2'))
            for k in range(3): bays.append(R(x0 + 30 + k * 110, 530, 80, 50, 'glass', 6, .9))
    s.layer('bays', bays, 'rise', .45)
    # 消防车正面
    tx = 980
    tk = [shadow(tx, 775, 200, 12, .3), R(tx - 170, 560, 340, 200, 'truck', 24), R(tx - 150, 576, 300, 96, 'glass', 14), P(f'M{tx - 120},576 L{tx - 80},576 L{tx - 120},672 L{tx - 146},672Z', '#ffffff', .4),
          R(tx - 6, 576, 12, 96, 'truck2'), R(tx - 170, 688, 340, 50, 'truck2', 10), R(tx - 80, 694, 160, 38, 'chrome', 8), *[R(tx - 72 + k * 22, 700, 12, 26, '#9AA4AE', 3) for k in range(7)],
          C(tx - 130, 712, 18, 'light'), C(tx + 130, 712, 18, 'light'), R(tx - 180, 736, 360, 22, 'chrome', 8), R(tx - 160, 750, 50, 26, 'tire', 6), R(tx + 110, 750, 50, 26, 'tire', 6),
          R(tx - 150, 538, 300, 22, 'chrome', 6), S(f'M{tx - 140},{532} L{tx + 140},{532}', '#C9D0D6', 6), R(tx - 186, 600, 16, 40, 'chrome', 4), R(tx + 170, 600, 16, 40, 'chrome', 4)]
    s.layer('truck', tk, 'rise', .6)
    s.layer('siren', [R(tx - 70, 546, 60, 18, 'truck', 6), R(tx + 10, 546, 60, 18, 'blue', 6), C(tx - 40, 552, 34, 'truck', .55, 'filter="url(#b20)"'), C(tx + 40, 552, 34, 'blue', .55, 'filter="url(#b20)"')], 'fade', 1.0, loop='glow')
    # 地坪
    ap = [R(0, 770, W, 310, s.lg([(0, 'apron'), (1, 'apron2')])), R(0, 770, W, 8, 'apron2')]
    for k in range(0, W, 200): ap.append(R(k, 780, 3, 300, '#ffffff', 0, .3))
    for k in range(14): ap.append(P(f'M{800 + k * 28},790 L{816 + k * 28},790 L{806 + k * 28},812 L{790 + k * 28},812Z', 'hatch', .9))
    ap.append(R(800, 812, 360, 4, 'hatch', 0, .9))
    s.layer('apron', ap, 'rise', .1)

    def hydrant(x, y):
        return G([shadow(x, y, 46, 8), R(x - 26, y - 90, 52, 90, 'hydrant', 10), P(f'M{x - 30},{y - 88} Q{x},{y - 128} {x + 30},{y - 88}Z', 'hydrant'), R(x - 34, y - 96, 68, 12, 'truck2', 5),
                  R(x - 44, y - 66, 18, 22, 'truck2', 5), R(x + 26, y - 66, 18, 22, 'truck2', 5), C(x, y - 50, 12, 'truck2'), R(x - 34, y - 10, 68, 12, 'truck2', 4), C(x - 8, y - 110, 5, '#ffffff', .5)])

    def cone(x, y, sc=1):
        return G([shadow(x, y, 40 * sc, 6 * sc), R(x - 38 * sc, y - 10 * sc, 76 * sc, 10 * sc, 'cone', 3), P(f'M{x - 26 * sc},{y - 10 * sc} L{x - 7 * sc},{y - 92 * sc} L{x + 7 * sc},{y - 92 * sc} L{x + 26 * sc},{y - 10 * sc}Z', 'cone'),
                  P(f'M{x - 18 * sc},{y - 40 * sc} L{x - 13 * sc},{y - 60 * sc} L{x + 13 * sc},{y - 60 * sc} L{x + 18 * sc},{y - 40 * sc}Z', '#ffffff')])
    s.layer('props', [hydrant(380, 900), cone(1460, 900), cone(1560, 912, .9), cone(1660, 900)], 'pop', .85)
    # 墙上水带卷盘
    hr = [C(1560, 620, 64, 'truck2', extra='filter="url(#shs)"'), C(1560, 620, 50, 'gold'), *[S(f'M{1560 - r_},620 a{r_},{r_} 0 1,0 {2 * r_},0 a{r_},{r_} 0 1,0 {-2 * r_},0', 'gold', 4) for r_ in ()],
          S('M1520,620 a40,40 0 1,0 80,0 a40,40 0 1,0 -80,0', '#E3A93A', 5), S('M1532,620 a28,28 0 1,0 56,0 a28,28 0 1,0 -56,0', '#E3A93A', 5), C(1560, 620, 12, 'truck2'),
          R(1500, 700, 120, 10, 'truck2', 4)]
    s.layer('hose_reel', hr, 'pop', .95)
    return s


# ================= 065 楼道安全出口 =================
def corridor():
    s = Scene('s065', '楼道安全出口', '安全与法治', ['消防安全', '疏散逃生', '安全教育', '道德与法治'],
              dict(wall1='#EFF6F0', wall2='#DDEBE0', dado='#BCD6C5', dado2='#A6C7B2', ceil='#F7FAF7', floor1='#D3D9D2', floor2='#BCC4BC', speck='#9AA49A',
                   door='#86A6B6', door2='#6F8FA0', bar='#D7DEE3', exitg='#1FA463', exitg2='#178A52', red='#E5483C', red2='#BE3A30', metal='#AAB4BD', glass='#CFEAF2',
                   stair='#E3E7E1', stair2='#C7CEC6', rail='#6F7C86', light='#FFF5CC', hose='#F2C14E'),
              desc='教学楼楼道：中央防火门上方亮着绿色安全出口标志，左侧消火栓箱与报警按钮，右侧楼梯，墙脚疏散指示灯。', stand={'ground_y': 930, 'x': [560, 1340]})
    s.layer('wall', [R(0, 0, W, 60, 'ceil'), R(0, 56, W, 6, 'dado2', 0, .5), R(0, 62, W, 738, s.lg([(0, 'wall1'), (1, 'wall2')])),
                     R(0, 640, W, 160, 'dado'), R(0, 640, W, 10, 'dado2')], 'fade', 0)
    fl = [R(0, 800, W, 280, s.lg([(0, 'floor1'), (1, 'floor2')])), R(0, 800, W, 10, 'dado2')]
    random.seed(4)
    for _ in range(260): fl.append(C(random.uniform(0, W), random.uniform(815, 1075), random.uniform(1.5, 3.5), 'speck', .35))
    for x in range(0, W, 240): fl.append(R(x, 810, 3, 270, '#ffffff', 0, .4))
    s.layer('floor', fl, 'rise', .1)
    # 防火门
    dr = [R(790, 330, 340, 476, 'door2', 10, extra='filter="url(#sh)"')]
    for x0 in (806, 966):
        dr += [R(x0, 346, 148, 456, 'door', 6), R(x0 + 44, 380, 60, 110, 'glass', 6), P(f'M{x0 + 54},380 L{x0 + 74},380 L{x0 + 58},490 L{x0 + 48},490Z', '#ffffff', .4),
               R(x0 + 14, 590, 120, 22, 'bar', 10), R(x0 + 14, 590, 120, 6, '#ffffff', 3, .6)]
    dr += [R(956, 346, 8, 456, 'door2')]
    s.layer('fire_door', dr, 'rise', .3)
    s.layer('exit_sign', [R(958, 238, 4, 40, 'metal'), exit_sign(830, 196, 260, 104, 'exitg')], 'drop', .55)
    s.layer('exit_glow', [R(810, 176, 300, 144, 'exitg', 20, .25, 'filter="url(#b20)"'), E(960, 340, 260, 40, 'exitg', .15, 'filter="url(#b20)"')], 'fade', .9, loop='glow')
    # 消火栓箱 + 报警按钮
    hx, hy = 150, 400
    hc = [R(hx, hy, 300, 380, 'red2', 14, extra='filter="url(#sh)"'), R(hx + 14, hy + 14, 272, 352, 'red', 10), R(hx + 30, hy + 30, 240, 230, 'glass', 8, .9),
          S(f'M{hx + 80},{hy + 145} a70,70 0 1,0 140,0 a70,70 0 1,0 -140,0', 'hose', 16), S(f'M{hx + 104},{hy + 145} a46,46 0 1,0 92,0 a46,46 0 1,0 -92,0', 'hose', 14),
          C(hx + 150, hy + 145, 22, 'red2'), R(hx + 200, hy + 200, 50, 16, 'metal', 6, extra=f'transform="rotate(-30 {hx + 225} {hy + 208})"'),
          P(f'M{hx + 60},{hy + 40} L{hx + 110},{hy + 40} L{hx + 50},{hy + 250} L{hx + 40},{hy + 250}Z', '#ffffff', .35),
          R(hx + 30, hy + 280, 240, 70, 'red2', 8, .6), R(hx + 50, hy + 300, 90, 30, 'metal', 6), C(hx + 220, hy + 315, 18, 'metal')]
    hc += [R(468, 470, 84, 84, 'red', 12, extra='filter="url(#shs)"'), R(478, 480, 64, 64, '#ffffff', 8, .9), C(510, 512, 20, 'red'), C(504, 506, 6, '#ffffff', .6)]
    s.layer('hydrant_box', hc, 'slide-l', .45)
    # 灭火器（落地）
    def ext(x, y):
        return G([shadow(x, y, 34, 6), R(x - 22, y - 120, 44, 120, 'red', 18), R(x - 22, y - 80, 44, 30, '#ffffff', 2, .85), R(x - 8, y - 140, 16, 24, '#3A4552', 4),
                  P(f'M{x - 8},{y - 140} L{x - 34},{y - 150} L{x - 34},{y - 140} L{x - 8},{y - 132}Z', '#3A4552'), S(f'M{x + 8},{y - 130} q30,10 26,60', '#3A4552', 6), R(x - 14, y - 112, 6, 30, '#ffffff', 3, .4)])
    s.layer('extinguishers', [shadow(560, 802, 70, 8), R(490, 760, 140, 42, 'red2', 8), ext(530, 770), ext(590, 770)], 'pop', .7)
    # 楼梯（右，平面立面）
    st = []
    x0, y0 = 1420, 800; sw, sh_ = 64, 40
    pts = [(x0, y0)]
    for k in range(10): pts += [(x0 + k * sw, y0 - (k + 1) * sh_), (x0 + (k + 1) * sw, y0 - (k + 1) * sh_)]
    pts += [(W + 10, y0 - 10 * sh_), (W + 10, y0)]
    st.append(poly(pts, 'stair', extra='filter="url(#shs)"'))
    for k in range(10): st.append(R(x0 + k * sw, y0 - (k + 1) * sh_, sw, 8, 'stair2'))
    st.append(poly([(x0, y0)] + [(x0 + (k + 1) * sw, y0 - (k + 1) * sh_) for k in range(10)] + [(W + 10, y0 - 10 * sh_), (W + 10, y0)], 'stair2', .45))
    for k in range(0, 10, 2):
        bx = x0 + k * sw + 30; by = y0 - (k + 1) * sh_
        st.append(R(bx - 3, by - 150, 6, 150, 'rail'))
    st.append(S(f'M{x0 + 10},{y0 - 190} L{x0 + 10 * sw + 40},{y0 - 10 * sh_ - 190}', 'rail', 12))
    st.append(S(f'M{x0 + 10},{y0 - 190} L{x0 + 10 * sw + 40},{y0 - 10 * sh_ - 190}', '#ffffff', 3, .35))
    s.layer('stairs', st, 'slide-r', .5)
    # 应急照明灯
    el = [R(1200, 150, 140, 54, '#ffffff', 12, extra='filter="url(#shs)"'), C(1225, 208, 22, 'light'), C(1315, 208, 22, 'light'), C(1270, 177, 6, 'exitg'),
          R(1205, 196, 40, 16, 'metal', 6), R(1295, 196, 40, 16, 'metal', 6)]
    s.layer('emergency_light', el, 'pop', .8)
    # 墙脚疏散指示灯（指向出口）
    gl = []
    for x in (150, 360, 1560, 1760):
        d = 1 if x < 960 else -1
        if x > 1400: y = 600 - (x - 1420) / 64 * 40 * 0 
        gl += [R(x - 50, 690, 100, 44, '#ffffff', 8, extra='filter="url(#shs)"'), R(x - 44, 696, 88, 32, 'exitg', 5), arrow(x - d * 30, 712, 60, '#ffffff', d, 8)]
    gl += [R(x - 50, 690, 100, 44, 'exitg', 20, .25, 'filter="url(#b6)"') for x in (150, 360)]
    s.layer('guide_lights', gl, 'fade', 1.0, loop='twinkle')
    # 天花：烟感与喷淋
    cd = []
    for x in (300, 700, 1220, 1640):
        cd += [E(x, 64, 30, 9, '#ffffff', extra='filter="url(#shs)"'), C(x, 70, 4, 'red')]
    for x in (500, 1440): cd += [R(x - 4, 60, 8, 16, 'metal', 2), E(x, 80, 16, 5, 'metal')]
    s.layer('ceiling_devices', cd, 'drop', .65)
    s.layer('soft_light', [E(960, 120, 600, 120, '#ffffff', .35, 'filter="url(#b40)"')], 'fade', .4)
    return s


# ================= 066 电梯厅 =================
def elevator():
    s = Scene('s066', '电梯厅', '安全与法治', ['安全教育', '乘梯安全', '消防安全', '生活'],
              dict(wall1='#F4EFE9', wall2='#E7DED3', panel='#D9C7B2', panel2='#C9B49C', steel1='#E1E6EB', steel2='#B4BDC6', frame='#8E99A4', frame2='#77838F',
                   floor='#EFE9E1', floor2='#DDD3C6', disp='#2C3138', led='#FFB547', ledg='#3CC27A', red='#E5483C', plant='#5FA873', plant2='#9AD18E', pot='#E5D8C8',
                   light='#FFF4D6', art1='#9ED0C7', art2='#F4B49A', art3='#F7D88A', bench='#7AA6B4'),
              desc='明亮电梯厅：两部不锈钢电梯门、楼层显示与上下呼梯按钮，中间“火灾时禁用电梯”图示，地面映出倒影。', stand={'ground_y': 930, 'x': [560, 1360]})
    bg = [R(0, 0, W, 820, s.lg([(0, 'wall1'), (1, 'wall2')]))]
    for x in range(0, W, 160): bg += [R(x, 0, 156, 820, 'panel', 0, .22), R(x + 156, 0, 4, 820, 'panel2', 0, .4)]
    bg += [R(0, 0, W, 70, '#FBF8F4'), R(0, 66, W, 6, 'panel2', 0, .6), R(0, 800, W, 20, 'panel2')]
    s.layer('wall', bg, 'fade', 0)
    fl = [R(0, 820, W, 260, s.lg([(0, 'floor'), (1, 'floor2')]))]
    for x in range(-200, W + 200, 320): fl.append(S(f'M{x},820 L{x - 160},1080', '#ffffff', 3, .45))
    fl += [R(0, 900, W, 2, '#ffffff', 0, .4), R(0, 990, W, 2, '#ffffff', 0, .35)]
    s.layer('floor', fl, 'rise', .1)
    # 倒影
    rf = []
    for x0 in (450, 1110):
        rf += [R(x0, 822, 360, 160, s.lg([(0, 'steel2', .35), (1, 'steel2', 0)]))]
    rf.append(R(930, 822, 60, 50, s.lg([(0, 'frame', .25), (1, 'frame', 0)])))
    s.layer('reflection', rf, 'fade', .8)
    # 门框与门
    fr = []
    for x0 in (450, 1110):
        fr += [R(x0 - 26, 250, 412, 572, 'frame', 10, extra='filter="url(#sh)"'), R(x0 - 12, 264, 384, 558, 'frame2', 6)]
    s.layer('door_frames', fr, 'rise', .25)
    dd = []
    for x0 in (450, 1110):
        for k in range(2):
            xx = x0 + k * 181
            dd += [R(xx, 276, 179, 544, s.lg([(0, 'steel1'), (.5, '#F7F9FB'), (1, 'steel2')], 0, 0, 1, 0)),
                   P(f'M{xx + 40},276 L{xx + 90},276 L{xx + 40},820 L{xx + 10},820Z', '#ffffff', .35)]
        dd.append(R(x0 + 178, 276, 4, 544, 'frame2'))
    s.layer('doors', dd, 'slide-l', .4)
    # 楼层显示
    ds = []
    for x0 in (450, 1110):
        cx = x0 + 180
        ds += [R(cx - 90, 170, 180, 60, 'disp', 14, extra='filter="url(#shs)"')]
    s.layer('displays', ds, 'drop', .5)
    lt = []
    for x0 in (450, 1110):
        cx = x0 + 180
        lt += [poly([(cx - 48, 214), (cx - 28, 186), (cx - 8, 214)], 'ledg'), *[R(cx + 10 + k * 18, 188, 10, 26, 'led', 3) for k in range(3)]]
    s.layer('display_leds', lt, 'fade', 1.0, loop='twinkle')
    # 呼梯面板
    cp = [R(918, 560, 84, 150, 'steel1', 12, extra='filter="url(#shs)"'), R(918, 560, 84, 150, 'frame', 12, .15),
          C(960, 605, 22, '#ffffff'), S('M938,605 a22,22 0 1,0 44,0 a22,22 0 1,0 -44,0', 'frame', 3), poly([(950, 612), (970, 612), (960, 596)], 'ledg'),
          C(960, 665, 22, '#ffffff'), S('M938,665 a22,22 0 1,0 44,0 a22,22 0 1,0 -44,0', 'frame', 3), poly([(950, 658), (970, 658), (960, 674)], 'frame2')]
    s.layer('call_panel', cp, 'pop', .7)
    # 火灾禁用电梯
    fx, fy = 960, 400
    inner = [R(fx - 26, fy - 34, 52, 66, '#5E6B78', 6), R(fx - 22, fy - 30, 21, 58, '#C9D2DA', 2), R(fx + 1, fy - 30, 21, 58, '#C9D2DA', 2),
             P(f'M{fx + 32},{fy + 34} Q{fx + 18},{fy + 26} {fx + 22},{fy + 10} Q{fx + 26},{fy} {fx + 34},{fy - 8} Q{fx + 34},{fy + 6} {fx + 42},{fy + 10} Q{fx + 46},{fy + 28} {fx + 32},{fy + 34}Z', '#F28C2E')]
    s.layer('no_elevator_fire', [R(fx - 80, fy - 80, 160, 160, '#ffffff', 20, extra='filter="url(#shs)"'), prohibit(fx, fy, 66, inner)], 'pop', .85)
    # 绿植与长椅
    pl = [plant_pot(200, 820, 1.6, 'pot', 'plant', 'plant2', 6), R(186, 640, 28, 60, '#8A5A3A', 6, .0)]
    s.layer('plant', pl, 'grow', .9, loop='sway', origin='200 820')
    ar = [R(1590, 230, 240, 300, '#ffffff', 10, extra='filter="url(#shs)"'), R(1606, 246, 208, 268, 'art1', 4), C(1730, 330, 48, 'art3'), P('M1606,514 L1680,420 L1740,470 L1780,440 L1814,514Z', 'art2'),
          shadow(1710, 822, 150, 10), R(1580, 720, 260, 30, 'bench', 12, extra='filter="url(#shs)"'), R(1600, 750, 16, 70, 'frame2', 4), R(1804, 750, 16, 70, 'frame2', 4)]
    s.layer('art_bench', ar, 'slide-r', .6)
    lg = []
    for x in (330, 960, 1590):
        lg += [E(x, 70, 50, 10, 'light'), P(f'M{x - 46},72 L{x + 46},72 L{x + 160},700 L{x - 160},700Z', s.lg([(0, 'light', .35), (1, 'light', 0)]))]
    s.layer('downlights', lg, 'fade', .9, loop='glow')
    return s


# ================= 067 河边防溺水警示 =================
def riverside():
    s = Scene('s067', '河边防溺水警示', '安全与法治', ['防溺水', '安全教育', '道德与法治', '户外'],
              dict(sky1='#A6DBF4', sky2='#FFF3DE', sun='#FFD98A', hill1='#C3E2CB', hill2='#A2D0B0', far='#86C29A', water1='#86CDE6', water2='#BDE9F5',
                   bank='#A5D48E', bank2='#88C273', path='#EEDFC0', path2='#DECBA4', fence='#F6F1E8', fence2='#CDBFA9', willow='#7DBE84', willow2='#A9D99B', trunk='#8A5A3A',
                   signy='#F7C948', signk='#2F3A48', red='#E5533D', buoy='#F28C2E', post='#7A6A5A', reed='#8FB86A', reed2='#C7A86A', duck='#FFFFFF', bill='#F2A33A', blue='#3D8FD6'),
              desc='温和的河畔：远山、平静河面、木栏杆与草地小路，警示牌（当心落水、禁止游泳）和救生圈架，柳枝轻摆。', stand={'ground_y': 930, 'x': [560, 1360]})
    s.layer('sky', [R(0, 0, W, 620, s.lg([(0, 'sky1'), (1, 'sky2')])), C(1460, 210, 160, 'sun', .3, 'filter="url(#b40)"'), C(1460, 210, 64, 'sun')], 'fade', 0)
    s.layer('clouds', [cloud(380, 150, .75, op=.9), cloud(1000, 110, .5, op=.8), cloud(1750, 190, .6, op=.85)], 'slide-l', .2, loop='drift')
    hl = [P('M-20,560 Q200,380 460,470 Q700,330 1000,460 Q1240,360 1500,450 Q1720,380 1940,470 L1940,580 L-20,580Z', 'hill1'),
          P('M-20,580 Q300,470 620,540 Q900,470 1220,545 Q1560,480 1940,540 L1940,600 L-20,600Z', 'hill2')]
    for k, x in enumerate(range(40, 1920, 95)): hl += [C(x, 590 - (k % 3) * 6, 26 + (k % 2) * 8, 'far'), R(x - 3, 590, 6, 16, 'trunk', 2)]
    s.layer('hills', hl, 'rise', .3)
    rv = [R(0, 600, W, 200, s.lg([(0, 'water2'), (1, 'water1')])), R(0, 598, W, 8, 'bank2', 0, .7)]
    rv += [R(1380, 610, 160, 6, '#ffffff', 3, .5), R(1420, 626, 100, 5, '#ffffff', 3, .4), R(1440, 640, 60, 4, '#ffffff', 2, .35)]
    s.layer('river', rv, 'fade', .35)
    rp = []
    for k in range(10):
        x = (k * 211) % 1800 + 60; y = 650 + (k % 4) * 30
        rp.append(S(f'M{x},{y} q24,-8 48,0 t48,0', '#ffffff', 3, .6))
    s.layer('ripples', rp, 'fade', .8, loop='flow')
    # 鸭子
    def duck(x, y, sc, d=1):
        return G([E(x, y, 34 * sc, 16 * sc, 'duck'), C(x + d * 24 * sc, y - 16 * sc, 12 * sc, 'duck'), poly([(x + d * 34 * sc, y - 18 * sc), (x + d * 46 * sc, y - 14 * sc), (x + d * 34 * sc, y - 11 * sc)], 'bill'),
                  C(x + d * 27 * sc, y - 19 * sc, 2.2 * sc, 'signk'), P(f'M{x - d * 34 * sc},{y - 4 * sc} l{-d * 10 * sc},{-10 * sc} l{d * 14 * sc},{4 * sc}Z', 'duck'), E(x, y + 12 * sc, 34 * sc, 4 * sc, 'water1', .6)])
    s.layer('ducks', [duck(1100, 690, 1.1), duck(1190, 712, .8)], 'slide-r', .9, loop='bob')
    # 近岸草地与小路
    bk = [P(f'M0,780 Q480,760 960,778 Q1440,796 1920,772 L1920,1080 L0,1080Z', s.lg([(0, 'bank'), (1, 'bank2')]))]
    bk.append(P('M0,900 Q500,860 960,880 Q1420,900 1920,866 L1920,990 Q1420,1020 960,1000 Q500,980 0,1010Z', 'path'))
    bk.append(P('M0,900 Q500,860 960,880 Q1420,900 1920,866 L1920,876 Q1420,910 960,890 Q500,870 0,910Z', 'path2', .7))
    for x, y in [(300, 940), (720, 950), (1200, 948), (1600, 930)]: bk += [E(x, y, 26, 8, 'path2', .7), E(x + 50, y + 16, 18, 6, 'path2', .6)]
    random.seed(12)
    for k in range(40):
        x = random.uniform(20, 1900); y = random.choice([random.uniform(800, 860), random.uniform(1010, 1070)])
        if 560 < x < 1360 and y > 1000: continue
        bk += [S(f'M{x:.0f},{y:.0f} L{x:.0f},{y - 18:.0f}', 'bank2', 3), C(x, y - 20, 6, ['#ffffff', 'signy', '#F4A0B0'][k % 3]), C(x, y - 20, 2.4, 'bill')]
    s.layer('bank', bk, 'rise', .15)
    # 木栏杆
    fc = []
    for x in range(30, W, 140):
        fc += [R(x - 9, 712, 18, 104, 'fence2', 4), R(x - 8, 710, 16, 100, 'fence', 4)]
    fc += [R(0, 724, W, 16, 'fence', 6, extra='filter="url(#shs)"'), R(0, 762, W, 12, 'fence', 5), R(0, 736, W, 4, 'fence2', 0, .6)]
    s.layer('fence', fc, 'rise', .45)
    # 柳树（左侧框景）
    wl = [P('M60,1000 C90,820 40,640 130,420 L170,430 C110,640 160,820 140,1000Z', 'trunk'), E(100, 290, 230, 160, 'willow'), E(200, 350, 150, 100, 'willow2', .7)]
    random.seed(6)
    for k in range(14):
        x = -60 + k * 28 + random.uniform(-8, 8); ln = random.uniform(230, 420)
        wl.append(S(f'M{x},{330} Q{x + 18},{330 + ln * .5} {x + 4},{330 + ln}', 'willow' if k % 2 else 'willow2', 9))
    s.layer('willow', wl, 'grow', .55, loop='sway', origin='120 1000')
    # 芦苇
    rd = []
    for x0 in (1700, 1780, 1860, 600, 330):
        for k in range(4):
            x = x0 + k * 12; h = 120 + (k % 3) * 30
            rd += [S(f'M{x},{800} Q{x + 6},{800 - h * .5} {x + (k - 1.5) * 8},{800 - h}', 'reed', 4), E(x + (k - 1.5) * 8, 800 - h, 5, 18, 'reed2')]
    s.layer('reeds', rd, 'grow', .7)
    # 警示牌
    sx = 470
    drown = [C(sx, 330, 11, 'signk'), S(f'M{sx - 4},{318} L{sx - 18},{290}', 'signk', 7), S(f'M{sx - 30},{352} q10,-8 20,0 t20,0 t20,0 t20,0', 'signk', 6), S(f'M{sx - 30},{366} q10,-8 20,0 t20,0 t20,0 t20,0', 'blue', 5)]
    swim = [C(sx - 14, 456, 9, 'signk'), S(f'M{sx - 4},{460} L{sx + 22},{452}', 'signk', 7), S(f'M{sx - 26},{474} q8,-6 16,0 t16,0 t16,0 t16,0', 'blue', 5)]
    sg = [R(sx - 7, 270, 14, 560, 'post', 4), shadow(sx, 830, 50, 8), warn_tri(sx, 390, 160, drown, 'signy', 'signk'), prohibit(sx, 465, 54, swim, 'red')]
    s.layer('warning_signs', [G(sg, f'transform="translate({sx},830) scale(1.2) translate({-sx},-830)"')], 'pop', .85)
    # 救生圈架
    bx = 1560
    lb = [shadow(bx, 832, 70, 8), R(bx - 8, 520, 16, 312, 'post', 4), R(bx - 70, 520, 140, 18, 'post', 6), R(bx - 60, 538, 120, 160, '#ffffff', 10, .0),
          C(bx, 610, 62, 'buoy', extra='filter="url(#shs)"'), C(bx, 610, 30, '#ffffff', .0)]
    for k in range(4):
        a0 = k * math.pi / 2 + math.pi / 4
        x1, y1 = bx + 62 * math.cos(a0 - .3), 610 + 62 * math.sin(a0 - .3); x2, y2 = bx + 62 * math.cos(a0 + .3), 610 + 62 * math.sin(a0 + .3)
        x3, y3 = bx + 30 * math.cos(a0 + .3), 610 + 30 * math.sin(a0 + .3); x4, y4 = bx + 30 * math.cos(a0 - .3), 610 + 30 * math.sin(a0 - .3)
        lb.append(P(f'M{x1:.1f},{y1:.1f} A62,62 0 0,1 {x2:.1f},{y2:.1f} L{x3:.1f},{y3:.1f} A30,30 0 0,0 {x4:.1f},{y4:.1f}Z', '#ffffff'))
    lb.append(C(bx, 610, 30, 'water2'))
    lb.append(S(f'M{bx - 46},{570} q46,-20 92,0', '#ffffff', 3, .5))
    lb.append(S(f'M{bx - 40},{650} Q{bx},{720} {bx + 40},{650}', 'reed2', 4))
    s.layer('life_buoy', lb, 'pop', 1.0)
    return s


# ================= 068 模拟法庭 =================
def court():
    s = Scene('s068', '模拟法庭', '安全与法治', ['道德与法治', '法治教育', '规则意识', '班会'],
              dict(wall1='#F3E9DA', wall2='#E6D6BF', panel='#A06F48', panel2='#835735', groove='#6E4729', bench='#8E5D38', bench2='#704527', top='#C08A58',
                   carpet='#6F96C4', carpet2='#5A7FAE', runner='#8CB0D8', gold='#EBBB4F', gold2='#C99A34', blue='#2F5D8C', chair='#3C4B5E', chair2='#2C3847',
                   paper='#FFFDF6', mic='#4A4F55', plant='#5FA873', plant2='#93CC8E', pot='#E7DCCB', lamp='#FFE3A3'),
              desc='庄重而明亮的模拟法庭：木质背墙中央的天平徽章、抬高的审判席与法槌、左右两张席位桌，蓝色地毯。', stand={'ground_y': 940, 'x': [560, 1360]})
    s.layer('wall', [R(0, 0, W, 800, s.lg([(0, 'wall1'), (1, 'wall2')])), R(0, 0, W, 40, 'panel2', 0, .25), *[R(x, 40, 2, 760, 'wall2', 0, .9) for x in range(0, W, 96)]], 'fade', 0)
    pi = []
    for x in (300, 1620):
        pi += [R(x - 50, 60, 100, 740, 'panel', 0, extra='filter="url(#shs)"'), R(x - 64, 40, 128, 34, 'panel2', 4), R(x - 64, 760, 128, 40, 'panel2', 4), R(x - 22, 90, 10, 660, 'groove', 3, .45), R(x + 12, 90, 10, 660, 'groove', 3, .45)]
    s.layer('pilasters', pi, 'rise', .2)
    bp = [R(520, 70, 880, 560, 'panel', 14, extra='filter="url(#sh)"'), R(540, 90, 840, 520, 'panel2', 8)]
    for x in range(570, 1380, 70): bp.append(R(x, 110, 40, 480, 'panel', 6, .55))
    bp += [R(500, 56, 920, 26, 'top', 8)]
    s.layer('back_panel', bp, 'rise', .3)
    # 天平徽章
    ex, ey = 960, 250
    em = [C(ex, ey, 118, 'gold', extra='filter="url(#sh)"'), C(ex, ey, 104, 'blue'), S(f'M{ex - 92},{ey} a92,92 0 1,0 184,0 a92,92 0 1,0 -184,0', 'gold2', 3)]
    for k in range(24):
        a = k * math.pi / 12; em.append(C(ex + 92 * math.cos(a), ey + 92 * math.sin(a), 3, 'gold', .8))
    em += [R(ex - 4, ey - 60, 8, 112, 'gold'), C(ex, ey - 64, 9, 'gold'), R(ex - 70, ey - 44, 140, 8, 'gold', 4), P(f'M{ex - 34},{ey + 56} L{ex + 34},{ey + 56} L{ex + 22},{ey + 44} L{ex - 22},{ey + 44}Z', 'gold'),
           S(f'M{ex - 64},{ey - 40} L{ex - 82},{ey + 6} M{ex - 64},{ey - 40} L{ex - 46},{ey + 6} M{ex + 64},{ey - 40} L{ex + 46},{ey + 6} M{ex + 64},{ey - 40} L{ex + 82},{ey + 6}', 'gold', 3),
           P(f'M{ex - 90},{ey + 6} L{ex - 38},{ey + 6} Q{ex - 64},{ey + 30} {ex - 90},{ey + 6}Z', 'gold'), P(f'M{ex + 38},{ey + 6} L{ex + 90},{ey + 6} Q{ex + 64},{ey + 30} {ex + 38},{ey + 6}Z', 'gold')]
    s.layer('emblem', em, 'pop', .5, origin=f'{ex} {ey}')
    s.layer('emblem_shine', [C(ex - 50, ey - 60, 10, '#ffffff', .9), C(ex + 70, ey + 40, 6, '#ffffff', .8), C(ex, ey, 160, 'gold', .18, 'filter="url(#b40)"')], 'fade', 1.2, loop='twinkle')
    # 高背椅
    ch = []
    for x in (760, 960, 1160):
        ch += [R(x - 56, 400, 112, 170, 'chair', 30, extra='filter="url(#shs)"'), R(x - 42, 414, 84, 130, 'chair2', 22, .6), R(x - 46, 400, 92, 10, 'gold', 4, .8)]
    s.layer('chairs', ch, 'rise', .55)
    # 审判席
    da = [shadow(960, 800, 460, 14, .2), R(560, 520, 800, 260, 'bench', 10, extra='filter="url(#sh)"'), R(540, 500, 840, 34, 'top', 10), R(540, 528, 840, 8, 'bench2', 0, .6)]
    for x in (620, 860, 1100): da += [R(x, 570, 200, 170, 'bench2', 10, .55), R(x + 14, 584, 172, 142, 'bench', 8)]
    da += [R(520, 770, 880, 30, 'bench2', 6), R(892, 600, 136, 60, 'gold', 10, .0)]
    s.layer('judge_bench', da, 'rise', .4)
    gv = [E(1150, 500, 46, 9, 'bench2'), R(1110, 486, 80, 14, 'bench2', 7), R(1080, 452, 90, 30, 'bench2', 13, extra='transform="rotate(-18 1125 467)"'), R(1120, 466, 110, 10, 'top', 5, extra='transform="rotate(-18 1125 467)"'),
          R(740, 484, 120, 16, 'paper', 3, extra='transform="rotate(-4 800 492)"'), R(760, 478, 90, 12, 'paper', 3, .9), R(940, 470, 8, 34, 'mic'), E(944, 466, 12, 8, 'mic')]
    s.layer('gavel', gv, 'pop', .75)

    def table(x0, d):
        it = [shadow(x0 + 170, 858, 210, 10, .18)]
        cx = x0 + 170
        for k in (-1, 1): it += [R(cx + k * 90 - 40, 620, 80, 140, 'chair', 24), R(cx + k * 90 - 30, 632, 60, 100, 'chair2', 18, .6)]
        it += [R(x0, 700, 340, 160, 'bench', 10, extra='filter="url(#shs)"'), R(x0 - 14, 686, 368, 26, 'top', 8), R(x0 + 20, 730, 300, 110, 'bench2', 8, .45),
               R(cx - 60, 650, 120, 36, 'paper', 6, extra='filter="url(#shs)"'), R(cx - 50, 658, 100, 20, 'runner' if d < 0 else 'gold', 4, .7),
               R(cx + d * 110, 640, 6, 48, 'mic'), E(cx + d * 110 + 3, 636, 10, 7, 'mic'), R(cx - d * 120 - 40, 674, 80, 12, 'paper', 2, extra=f'transform="rotate({d * 5} {cx - d * 120} 680)"')]
        return G(it)
    s.layer('table_left', [table(120, 1)], 'slide-l', .6)
    s.layer('table_right', [table(1460, -1)], 'slide-r', .65)
    fl = [R(0, 800, W, 280, s.lg([(0, 'carpet'), (1, 'carpet2')])), R(0, 800, W, 8, 'panel2'), P('M760,808 L1160,808 L1260,1080 L660,1080Z', 'runner', .45),
          S('M760,808 L660,1080 M1160,808 L1260,1080', 'gold', 4, .5)]
    for y in range(840, 1080, 60):
        for x in range(((y // 60) % 2) * 60, W, 120): fl.append(poly([(x, y - 12), (x + 12, y), (x, y + 12), (x - 12, y)], '#ffffff', .12))
    s.layer('floor', fl, 'rise', .1)
    pl = [plant_pot(70, 800, 1.2, 'pot', 'plant', 'plant2'), plant_pot(1850, 800, 1.2, 'pot', 'plant', 'plant2')]
    s.layer('plants', pl, 'grow', .9)
    lp = []
    for x in (300, 1620):
        lp += [R(x - 30, 170, 60, 16, 'gold2', 6), P(f'M{x - 34},120 L{x + 34},120 L{x + 26},170 L{x - 26},170Z', 'lamp'), C(x, 150, 90, 'lamp', .4, 'filter="url(#b20)"')]
    s.layer('sconces', lp, 'fade', .95, loop='glow')
    return s


# ================= 069 警务站 =================
def policebox():
    s = Scene('s069', '警务站', '安全与法治', ['道德与法治', '求助报警', '安全教育', '职业认知'],
              dict(sky1='#9FD6F3', sky2='#EEF8FF', b1='#F4D8C2', b2='#CFE0EE', b3='#E8ECCB', b4='#F2CBD3', win='#FFFFFF', win2='#A9CBE6',
                   booth='#F7F9FB', booth2='#DCE4EB', blue='#2E6EC4', blue2='#20549C', red='#E5483E', glass='#BFE4F4', walk='#EAE3D8', walk2='#D8CFC2',
                   tree='#69B97C', tree2='#A6DB95', trunk='#8A5A3A', cone='#F28C2E', gold='#F2C14E', flower='#F28BA0', scooter='#2E6EC4', tire='#2F343A'),
              desc='街角警务站：蓝白岗亭、顶部红蓝警灯、盾形徽章与报警电话图示，旁边一键报警柱和巡逻电动车。', stand={'ground_y': 930, 'x': [240, 800]})
    s.layer('sky', [R(0, 0, W, 700, s.lg([(0, 'sky1'), (1, 'sky2')]))], 'fade', 0)
    s.layer('clouds', [cloud(320, 140, .7, op=.9), cloud(1100, 90, .55, op=.85), cloud(1700, 170, .6, op=.85)], 'slide-l', .2, loop='drift')
    bl = []
    for x, w, h, col in [(0, 260, 340, 'b1'), (270, 220, 260, 'b2'), (500, 260, 400, 'b3'), (770, 220, 300, 'b4'), (1000, 280, 360, 'b2'), (1290, 240, 280, 'b1'), (1540, 380, 420, 'b3')]:
        top = 660 - h
        bl.append(R(x, top, w, h, col, 8))
        for wy in range(top + 30, 620, 60):
            for wx in range(x + 24, x + w - 40, 60): bl += [R(wx, wy, 34, 38, 'win2', 4, .75), R(wx, wy, 34, 9, 'win', 3, .7)]
    s.layer('buildings', bl, 'rise', .25)
    s.layer('trees', [blob_tree(x, 690, .85 + .1 * (k % 2), 'tree', 'tree2', 'trunk') for k, x in enumerate((90, 460, 860, 1880))], 'grow', .45, loop='sway')
    pz = [R(0, 680, W, 400, s.lg([(0, 'walk'), (1, 'walk2')])), R(0, 680, W, 12, 'walk2')]
    for x in range(-200, W + 200, 160): pz.append(S(f'M{x},692 L{x - 60},1080', '#ffffff', 3, .45))
    for y in (760, 860, 980): pz.append(R(0, y, W, 2, '#ffffff', 0, .45))
    s.layer('plaza', pz, 'rise', .1)
    # 岗亭
    bx0, bx1 = 1000, 1580
    bt = [shadow((bx0 + bx1) / 2, 846, 330, 14, .2), R(bx0, 330, bx1 - bx0, 510, 'booth', 16, extra='filter="url(#sh)"'), R(bx0, 760, bx1 - bx0, 80, 'blue', 0), R(bx0, 760, bx1 - bx0, 10, 'blue2'),
          R(bx0 - 30, 280, bx1 - bx0 + 60, 60, 'blue', 14, extra='filter="url(#shs)"'), R(bx0 - 30, 330, bx1 - bx0 + 60, 10, 'blue2'), R(bx0, 340, bx1 - bx0, 26, 'booth2')]
    s.layer('booth', bt, 'rise', .35)
    bw = [R(1030, 400, 330, 260, 'blue2', 12), R(1042, 412, 306, 236, 'glass', 8), P('M1080,412 L1140,412 L1070,648 L1042,648Z', '#ffffff', .4), R(1193, 412, 4, 236, 'blue2'),
          R(1020, 650, 350, 24, 'booth2', 6, extra='filter="url(#shs)"'), R(1020, 674, 350, 8, 'blue', 0, .3),
          R(1400, 420, 150, 340, 'blue2', 10), R(1410, 430, 130, 330, 'booth2', 6), R(1428, 450, 94, 120, 'glass', 6), C(1520, 620, 8, 'gold')]
    # 盾形徽章 + 电话图示
    bw += [P('M1300,300 L1340,292 L1380,300 L1380,316 Q1380,338 1340,350 Q1300,338 1300,316Z', 'gold', extra='filter="url(#shs)"'),
           P('M1308,304 L1340,298 L1372,304 L1372,316 Q1372,334 1340,342 Q1308,334 1308,316Z', 'blue2'),
           poly([(1340 + 12 * math.cos(a), 318 + 12 * math.sin(a)) if k % 2 == 0 else (1340 + 5 * math.cos(a), 318 + 5 * math.sin(a)) for k, a in enumerate([-math.pi / 2 + k * math.pi / 5 for k in range(10)])], 'gold')]
    bw += [R(1060, 293, 170, 34, '#ffffff', 10, .95), P('M1078,300 q-6,10 4,20 q10,8 16,4 l4,-6 l-8,-6 l-4,4 q-6,-2 -8,-8 l4,-4 l-6,-8Z', 'blue'), T(1160, 321, '110', 26, 'blue', 900)]
    s.layer('booth_details', bw, 'pop', .55)
    lb = [R(1180, 236, 220, 44, 'booth2', 14), R(1190, 244, 90, 28, 'red', 10), R(1300, 244, 90, 28, 'blue', 10), C(1215, 252, 6, '#ffffff', .7), C(1325, 252, 6, '#ffffff', .7)]
    s.layer('light_bar', lb, 'drop', .7)
    s.layer('siren_glow', [C(1235, 258, 60, 'red', .5, 'filter="url(#b20)"'), C(1345, 258, 60, 'blue', .5, 'filter="url(#b20)"')], 'fade', 1.0, loop='glow')
    # 一键报警柱
    px = 1740
    pl = [shadow(px, 846, 60, 8), R(px - 34, 420, 68, 426, 'blue', 20, extra='filter="url(#shs)"'), R(px - 34, 420, 68, 50, 'blue2', 20), C(px, 444, 12, 'red'),
          R(px - 24, 500, 48, 70, '#ffffff', 8), C(px, 535, 18, 'red'), C(px - 5, 530, 5, '#ffffff', .6),
          R(px - 24, 590, 48, 48, '#ffffff', 8), P(f'M{px - 10},{600} q-5,9 3,17 q8,7 13,3 l3,-5 l-6,-5 l-3,3 q-5,-2 -7,-7 l3,-3 l-5,-6Z', 'blue'), R(px - 24, 660, 48, 6, '#ffffff', 3, .5)]
    s.layer('sos_pillar', pl, 'rise', .8)
    # 巡逻电动车
    sx = 860
    sc = [shadow(sx, 846, 120, 8), C(sx - 80, 806, 36, 'tire'), C(sx - 80, 806, 14, 'booth2'), C(sx + 82, 806, 36, 'tire'), C(sx + 82, 806, 14, 'booth2'),
          P(f'M{sx - 110},{780} L{sx + 30},{780} L{sx + 70},{690} L{sx + 92},{690} L{sx + 60},{800} L{sx - 120},{800}Z', 'scooter'), R(sx - 120, 740, 120, 46, 'scooter', 20),
          R(sx - 120, 736, 110, 16, '#ffffff', 8), R(sx + 60, 660, 14, 50, 'booth2', 4), R(sx + 44, 654, 60, 12, '#3A4552', 6), C(sx + 100, 706, 9, 'gold'), R(sx - 100, 756, 60, 10, '#ffffff', 4, .8),
          R(sx - 70, 708, 40, 24, 'red', 6), R(sx - 70, 708, 20, 24, 'blue', 6)]
    s.layer('scooter', sc, 'slide-l', .75)
    def cone(x, y, sc=1):
        return G([shadow(x, y, 36 * sc, 6 * sc), R(x - 34 * sc, y - 9 * sc, 68 * sc, 9 * sc, 'cone', 3), P(f'M{x - 24 * sc},{y - 9 * sc} L{x - 6 * sc},{y - 84 * sc} L{x + 6 * sc},{y - 84 * sc} L{x + 24 * sc},{y - 9 * sc}Z', 'cone'),
                  P(f'M{x - 16 * sc},{y - 36 * sc} L{x - 12 * sc},{y - 54 * sc} L{x + 12 * sc},{y - 54 * sc} L{x + 16 * sc},{y - 36 * sc}Z', '#ffffff')])
    fb = [R(30, 760, 200, 70, 'walk2', 14, extra='filter="url(#shs)"'), R(40, 740, 180, 30, 'tree', 15)]
    for k in range(7): fb += [C(52 + k * 26, 744 - (k % 2) * 8, 10, 'flower' if k % 2 else 'gold'), C(52 + k * 26, 744 - (k % 2) * 8, 4, '#ffffff', .8)]
    fb += [cone(1660, 900, .9), cone(1830, 920)]
    s.layer('props', fb, 'pop', .9)
    return s


# ================= 070 防震演练教室 =================
def quakedrill():
    s = Scene('s070', '防震演练教室', '安全与法治', ['防震减灾', '安全教育', '应急演练', '班会'],
              dict(wall1='#E6F1F8', wall2='#D3E5F0', wains='#93BBD2', wains2='#7EA6BF', floor1='#DDBE93', floor2='#C7A57A', board='#FFFFFF', bframe='#B5C2CC',
                   marker='#3D7FC4', marker2='#E5533D', desk='#F3C98B', desk2='#D9A863', metal='#6C7A88', helmet='#F7C53A', helmet2='#DDA92A', red='#E5533D',
                   green='#2DB36F', paper='#FFFDF6', bag='#E86F4F', bag2='#C9573B', sky1='#9ED7F4', sky2='#E8F7FF', leaf='#7CC48E', leaf2='#B9E3A6', cab='#F7F9FA', cab2='#DCE5EA', door='#C9DCE7'),
              desc='防震演练教室：白板上画着“蹲下-护头-撤离”三步图示，课桌下留出躲避空间，墙边安全帽、应急包和亮着的安全出口。', stand={'ground_y': 920, 'x': [600, 1300]})
    s.layer('wall', [R(0, 0, W, 780, s.lg([(0, 'wall1'), (1, 'wall2')])), R(0, 650, W, 130, 'wains'), R(0, 650, W, 12, 'wains2'), R(0, 768, W, 12, 'wains2')], 'fade', 0)
    # 窗
    x0 = 90
    win = [R(x0 - 16, 130, 352, 400, '#ffffff', 16, extra='filter="url(#shs)"'), R(x0, 146, 320, 368, s.lg([(0, 'sky1'), (1, 'sky2')]), 8)]
    cp = s.clip(f'<rect x="{x0}" y="146" width="320" height="368" rx="8"/>')
    win.append(G([cloud(x0 + 110, 240, .5), C(x0 + 60, 520, 120, 'leaf'), C(x0 + 250, 540, 140, 'leaf'), C(x0 + 160, 480, 60, 'leaf2', .6)], f'clip-path="{cp}"'))
    win += [R(x0 + 156, 146, 8, 368, '#ffffff'), R(x0, 326, 320, 8, '#ffffff'), R(x0 - 26, 526, 372, 18, '#ffffff', 6)]
    s.layer('window', win, 'pop', .25)
    # 白板 + 三步图示
    bd = [R(560, 130, 800, 400, 'bframe', 16, extra='filter="url(#sh)"'), R(574, 144, 772, 372, 'board', 8), R(550, 516, 820, 18, 'bframe', 8),
          R(620, 506, 50, 10, 'marker', 4), R(690, 506, 50, 10, 'marker2', 4)]
    s.layer('whiteboard', bd, 'drop', .4)
    ic = []
    # 1 蹲在桌下
    cx = 700
    ic += [R(cx - 90, 230, 180, 120, 'marker', 16, .1), R(cx - 70, 290, 140, 12, 'marker', 4), R(cx - 62, 302, 8, 50, 'marker'), R(cx + 54, 302, 8, 50, 'marker'),
           C(cx - 6, 316, 10, 'marker2'), P(f'M{cx - 4},{326} Q{cx + 30},{318} {cx + 30},{344} L{cx - 14},{346}Z', 'marker2')]
    # 2 双手护头
    cx = 960
    ic += [R(cx - 90, 230, 180, 120, 'marker', 16, .1), C(cx, 280, 16, 'marker2'), P(f'M{cx - 22},{268} Q{cx},{248} {cx + 22},{268}', 'none'),
           S(f'M{cx - 20},{290} L{cx - 26},{272} Q{cx - 16},{258} {cx},{262}', 'marker2', 6), S(f'M{cx + 20},{290} L{cx + 26},{272} Q{cx + 16},{258} {cx},{262}', 'marker2', 6),
           P(f'M{cx - 18},{298} Q{cx},{292} {cx + 18},{298} L{cx + 24},{340} L{cx - 24},{340}Z', 'marker2')]
    # 3 撤离到空地
    cx = 1220
    ic += [R(cx - 90, 230, 180, 120, 'marker', 16, .1), person_run(cx - 30, 296, .9, 'green'), arrow(cx + 4, 296, 70, 'green', 1, 9)]
    # 步骤间箭头与编号圆点
    ic += [arrow(800, 290, 50, 'marker', 1, 6), arrow(1060, 290, 50, 'marker', 1, 6)]
    for k, cx in enumerate((700, 960, 1220)):
        ic += [C(cx - 74, 214, 18, 'marker'), *[C(cx - 80 + j * 12, 214, 3.4, '#ffffff') for j in range(k + 1)]]
    ic += [S('M640,420 L1280,420', 'marker', 4, .25), S('M680,460 L1080,460', 'marker', 4, .25)]
    s.layer('drill_steps', ic, 'pop', .6)
    clk = [C(960, 72, 40, '#ffffff', extra='filter="url(#shs)"'), S('M920,72 a40,40 0 1,0 80,0 a40,40 0 1,0 -80,0', 'wains2', 7),
           *[C(960 + 30 * math.cos(k * math.pi / 6), 72 + 30 * math.sin(k * math.pi / 6), 2.6, 'metal') for k in range(12)],
           S('M960,72 L960,50', 'metal', 5), S('M960,72 L978,62', 'red', 4), C(960, 72, 5, 'metal')]
    s.layer('clock', clk, 'pop', .7)
    # 门 + 出口标志
    dr = [R(1560, 290, 270, 490, '#ffffff', 10, extra='filter="url(#shs)"'), R(1576, 306, 238, 474, '#FBF4E6', 4), R(1576, 306, 238, 474, s.lg([(0, '#FFF6DE'), (1, '#F4E3C2')]), 4),
          P('M1576,306 L1660,330 L1660,800 L1576,780Z', 'door'), C(1645, 560, 7, 'metal'), R(1600, 360, 40, 100, '#ffffff', 4, .5)]
    dr += [exit_sign(1610, 196, 170, 70, 'green')]
    s.layer('door_exit', dr, 'slide-r', .5)
    s.layer('exit_glow', [R(1590, 180, 210, 100, 'green', 20, .25, 'filter="url(#b20)"'), P('M1660,330 L1814,306 L1814,780 L1660,800Z', '#FFF3C4', .35)], 'fade', 1.0, loop='glow')
    # 安全帽挂架
    hm = [R(1390, 300, 120, 12, 'metal', 6)]
    for k, y in enumerate((320, 450)):
        hx = 1450
        hm += [R(hx - 4, y - 8, 8, 30, 'metal', 3), P(f'M{hx - 54},{y + 70} Q{hx - 54},{y + 10} {hx},{y + 10} Q{hx + 54},{y + 10} {hx + 54},{y + 70}Z', 'helmet', extra='filter="url(#shs)"'),
               R(hx - 66, y + 64, 132, 14, 'helmet2', 7), R(hx - 8, y + 12, 16, 56, 'helmet2', 6, .7), P(f'M{hx - 36},{y + 40} Q{hx - 30},{y + 20} {hx - 10},{y + 18}', 'none'),
               S(f'M{hx - 38},{y + 50} Q{hx - 34},{y + 26} {hx - 16},{y + 22}', '#ffffff', 5, .55)]
    s.layer('helmets', hm, 'drop', .75)
    # 应急柜：应急包 + 急救箱 + 手电
    kc = [R(60, 600, 420, 180, 'cab', 12, extra='filter="url(#shs)"'), R(76, 640, 186, 126, 'cab2', 8), R(278, 640, 186, 126, 'cab2', 8), R(150, 700, 40, 8, 'metal', 4), R(350, 700, 40, 8, 'metal', 4),
          R(60, 596, 420, 16, 'cab2', 6)]
    kc += [R(110, 500, 120, 100, 'bag', 26, extra='filter="url(#shs)"'), R(124, 530, 92, 50, 'bag2', 14), R(150, 484, 40, 26, 'bag2', 10, .0), S('M140,500 Q170,466 200,500', 'bag2', 8),
           R(156, 540, 28, 8, '#ffffff', 3), R(166, 530, 8, 28, '#ffffff', 3),
           R(270, 530, 110, 70, '#ffffff', 10, extra='filter="url(#shs)"'), R(270, 530, 110, 16, 'red', 8), R(317, 552, 16, 40, 'red', 3), R(305, 564, 40, 16, 'red', 3),
           R(400, 566, 60, 26, 'metal', 8), R(452, 560, 18, 38, 'helmet2', 6), C(470, 579, 14, '#FFF3C4', .7, 'filter="url(#b6)"')]
    s.layer('emergency_kit', kc, 'slide-l', .55)
    fl = [R(0, 780, W, 300, s.lg([(0, 'floor1'), (1, 'floor2')]))]
    for k in range(-12, 13):
        xb = 960 + k * 190; xt = 960 + (xb - 960) * (780 - 380) / (1080 - 380)
        fl.append(S(f'M{xt:.0f},780 L{xb},1080', 'floor2', 3, .45))
    for yy in (820, 880, 965): fl.append(S(f'M0,{yy} L{W},{yy}', 'floor2', 2, .3))
    s.layer('floor', fl, 'rise', .1)

    def desk(x, y, sc, cushion=None):
        w, h = 300 * sc, 26 * sc
        it = [shadow(x, y + 162 * sc, 170 * sc, 16 * sc, .1), R(x - w / 2 + 14 * sc, y + h, 12 * sc, 150 * sc, 'metal', 3), R(x + w / 2 - 26 * sc, y + h, 12 * sc, 150 * sc, 'metal', 3),
              R(x - w / 2 + 10 * sc, y + h, w - 20 * sc, 44 * sc, 'desk2', 6 * sc), R(x - w / 2, y, w, h, 'desk', 8 * sc, extra='filter="url(#shs)"')]
        if cushion: it += [R(x - 70 * sc, y + 128 * sc, 140 * sc, 30 * sc, cushion, 12 * sc), R(x - 60 * sc, y + 132 * sc, 120 * sc, 8 * sc, '#ffffff', 4, .4)]
        it += [R(x - 50 * sc, y - 9 * sc, 80 * sc, 10 * sc, 'paper', 3, extra=f'transform="rotate(-5 {x} {y})"'), R(x + 60 * sc, y - 9 * sc, 40 * sc, 9 * sc, 'marker', 3)]
        return G(it)
    s.layer('desks_back', [desk(420, 690, .6), desk(1500, 690, .6)], 'rise', .7)
    s.layer('desks_front', [desk(270, 830, .95), desk(1650, 830, .95)], 'rise', .85)
    s.layer('light', [beam(240, 400, 480, 860, 300, 1080, s, .24), E(960, 960, 360, 46, '#FFF6D8', .35, 'filter="url(#b20)"')], 'fade', .9, loop='glow')
    return s


SCENES = [bus, metro, firestation, corridor, elevator, riverside, court, policebox, quakedrill]
