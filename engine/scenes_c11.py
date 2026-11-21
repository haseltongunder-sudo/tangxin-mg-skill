"""第 11 类 · 季节专题（秋季防火）：s101–s105
金秋配色：树冠一律金黄/橙红，落叶飘落（loop='fall'），火焰（loop='flicker'），浓烟（loop='smoke'）。
做其他秋季主题（秋游、秋收、重阳）也可以直接用。"""
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


def ridge(y, amp, seed, step=170):
    random.seed(seed); pts = []; x = -100; ph = random.random() * 6
    while x <= W + 100 + step:
        pts.append((x, y - amp * (.4 + .6 * (.5 + .5 * math.sin(x / 260 + ph))) - random.uniform(0, amp * .2))); x += step
    return pts


def gold_tree(x, y, s, c1, c2, c3, trunk):
    """金秋圆冠树：三色叠冠（底色 c1、亮面 c2、暗面 c3），x,y 为树根"""
    it = [P(f'M{x - 12 * s},{y} L{x - 7 * s},{y - 140 * s} L{x + 7 * s},{y - 140 * s} L{x + 12 * s},{y}Z', trunk),
          S(f'M{x},{y - 110 * s} L{x - 38 * s},{y - 160 * s}', trunk, 7 * s), S(f'M{x},{y - 125 * s} L{x + 34 * s},{y - 175 * s}', trunk, 6 * s)]
    for dx, dy, r, col in [(0, -205, 92, c1), (-70, -160, 62, c1), (72, -158, 64, c1), (-36, -250, 56, c1), (40, -246, 58, c1),
                           (60, -150, 40, c3), (-62, -148, 36, c3), (14, -175, 52, c3),
                           (-30, -262, 40, c2), (-70, -195, 30, c2), (20, -230, 34, c2)]:
        it.append(C(x + dx * s, y + dy * s, r * s, col, .55 if col == c3 else (.9 if col == c2 else None)))
    return G(it)


def ginkgo(x, y, s, c1, c2, c3, trunk):
    """银杏：高挑的卵形树冠，扇形小叶块"""
    it = [P(f'M{x - 13 * s},{y} L{x - 7 * s},{y - 300 * s} L{x + 7 * s},{y - 300 * s} L{x + 13 * s},{y}Z', trunk)]
    for k in range(7):
        yy = y - (150 + k * 52) * s; w = (60 + 60 * math.sin(math.pi * (k + .5) / 7)) * s
        it.append(E(x, yy, w, 46 * s, c1))
        it.append(E(x - w * .35, yy - 6 * s, w * .45, 26 * s, c2, .85))
        it.append(E(x + w * .4, yy + 10 * s, w * .4, 22 * s, c3, .5))
    return G(it)


def leaf(x, y, s, col, rot):
    return P(f'M0,0 Q{-9 * s},{-8 * s} {-7 * s},{-16 * s} Q0,{-12 * s} {7 * s},{-16 * s} Q{9 * s},{-8 * s} 0,0Z', col,
             extra=f'transform="translate({x:.0f},{y:.0f}) rotate({rot:.0f})"')


def leaves(seed, n, x0, x1, y0, y1, cols, s0=.8, s1=1.6):
    random.seed(seed)
    return G([leaf(random.uniform(x0, x1), random.uniform(y0, y1), random.uniform(s0, s1), random.choice(cols), random.uniform(0, 360)) for _ in range(n)])


def flame(x, y, s, c1, c2, c3):
    """火苗：x,y 为火焰底部中心"""
    return G([P(f'M{x - 40 * s},{y} Q{x - 60 * s},{y - 60 * s} {x - 20 * s},{y - 110 * s} Q{x - 10 * s},{y - 60 * s} {x + 6 * s},{y - 70 * s} Q{x - 6 * s},{y - 130 * s} {x + 30 * s},{y - 170 * s} Q{x + 30 * s},{y - 100 * s} {x + 56 * s},{y - 70 * s} Q{x + 64 * s},{y - 30 * s} {x + 40 * s},{y}Z', c1),
              P(f'M{x - 24 * s},{y} Q{x - 36 * s},{y - 46 * s} {x - 8 * s},{y - 80 * s} Q{x}, {y - 50 * s} {x + 12 * s},{y - 56 * s} Q{x + 10 * s},{y - 100 * s} {x + 26 * s},{y - 118 * s} Q{x + 30 * s},{y - 70 * s} {x + 40 * s},{y - 40 * s} Q{x + 42 * s},{y - 14 * s} {x + 26 * s},{y}Z', c2),
              P(f'M{x - 10 * s},{y} Q{x - 16 * s},{y - 30 * s} {x + 4 * s},{y - 56 * s} Q{x + 22 * s},{y - 30 * s} {x + 16 * s},{y}Z', c3)])


def no_fire_sign(x, y, s, post, board, red, fl, fl2):
    """禁火标牌：x,y 为立柱底部，圆形禁令标志里一团火"""
    by = y - 230 * s
    return G([R(x - 7 * s, by, 14 * s, 230 * s, post, 4), R(x - 80 * s, by - 150 * s, 160 * s, 170 * s, board, 14 * s, extra='filter="url(#shs)"'),
              C(x, by - 70 * s, 62 * s, '#ffffff'), flame(x - 6 * s, by - 34 * s, .48 * s, fl, fl2, '#FFE9A8'),
              ring(x, by - 70 * s, 58 * s, red, 13 * s), S(f'M{x - 41 * s},{by - 111 * s} L{x + 41 * s},{by - 29 * s}', red, 13 * s, cap='butt')])


def ring(x, y, r, col, w, op=1):
    return S(f'M{x - r},{y} a{r},{r} 0 1,0 {2 * r},0 a{r},{r} 0 1,0 {-2 * r},0', col, w, op)


def grass_tufts(seed, n, x0, x1, y, col, h=34):
    random.seed(seed); it = []
    for _ in range(n):
        gx = random.uniform(x0, x1); hh = h * random.uniform(.6, 1.2)
        it.append(S(f'M{gx - 8},{y} q2,{-hh * .6} -6,{-hh} M{gx},{y} q0,{-hh * .7} 4,{-hh * 1.1} M{gx + 8},{y} q-2,{-hh * .6} 7,{-hh * .9}', col, 3.2))
    return G(it)


AUTUMN = dict(t1='#F6B930', t2='#FFD95A', t3='#E07A22', t4='#D9542B', trunk='#7A4E33', trunk2='#5E3A26')


# ============ s101 金秋山林 · 护林防火 ============
def s101():
    s = Scene('s101', '金秋山林·护林防火', '季节专题', ['安全', '森林防火', '秋游', '秋天'],
              dict(sky1='#8CC8EC', sky2='#FFE7C2', sun='#FFF0C4', mtn='#C9B8D6', mtn2='#B49CC4', far='#F0B65A', far2='#E59B45',
                   mid='#E9A43F', ground='#E8C27A', ground2='#D8A85E', path='#F6E2B5', **AUTUMN,
                   wood='#A5683F', wood2='#7F4C2C', roof='#C4452F', board='#F9F3E3', red='#E2382F', fl='#F2622E', fl2='#FFB238', grass='#C9923F'),
              desc='层林尽染的金秋山林：远山、满山金黄橙红的树、蜿蜒山路、木制防火瞭望塔、禁火标牌、飘落的黄叶，秋季防火主题的记忆点。',
              stand={'ground_y': 880, 'x': [520, 1360]})
    s.layer('sky', [R(0, 0, W, 760, s.lg([(0, 'sky1'), (1, 'sky2')])), C(1520, 200, 70, 'sun'), C(1520, 200, 140, 'sun', .35, 'filter="url(#b40)"')], 'fade', 0, depth=0)
    s.layer('clouds', [cloud(360, 170, .9, op=.9), cloud(980, 120, .6, op=.8), cloud(1780, 300, .5, op=.7)], 'slide-l', .15, loop='drift', depth=.05)
    s.layer('mountains', [P(smooth(ridge(560, 200, 4), 800), 'mtn'), P(smooth(ridge(600, 130, 9, 150), 800), 'mtn2', .9),
                          R(0, 470, W, 200, s.lg([(0, 'sky2', 0), (1, 'sky2', .75)]))], 'rise', .25, depth=.15)
    random.seed(11); far = []
    for k in range(34):  # 远处一层层的小树冠
        x = k * 60 - 30 + random.uniform(-14, 14); y = 640 + 24 * math.sin(k * .7) + random.uniform(-8, 8)
        col = random.choice(['far', 'far2', 't1', 't3'])
        far += [C(x, y, random.uniform(34, 52), col)]
    s.layer('forest_far', [P(smooth([(-100, 660), (400, 630), (900, 650), (1400, 620), (2020, 650)], 1080), 'far2')] + far, 'rise', .35, depth=.3)
    mid = []
    for x, sc, a in [(140, 1.05, 0), (330, .85, 1), (1620, 1.1, 0), (1800, .9, 1), (1450, .75, 2)]:
        c1, c2, c3 = [('t1', 't2', 't3'), ('t3', 't1', 't4'), ('t1', 't2', 't4')][a]
        mid.append(gold_tree(x, 790, sc, c1, c2, c3, 'trunk'))
    s.layer('ground', [P(smooth([(-100, 770), (500, 740), (1000, 765), (1500, 735), (2020, 760)], 1080), s.lg([(0, 'ground'), (1, 'ground2')])),
                       P('M760,1080 Q860,930 980,860 Q1060,810 1010,760 L1090,760 Q1150,820 1080,880 Q980,960 1060,1080Z', 'path')], 'rise', .45, depth=.6)
    s.layer('trees_mid', mid, 'grow', .6, depth=.62)
    # 瞭望塔
    tx, ty = 1180, 770
    tower = [S(f'M{tx - 70},{ty} L{tx - 40},{ty - 360} M{tx + 70},{ty} L{tx + 40},{ty - 360}', 'wood2', 14),
             S(f'M{tx - 62},{ty - 70} L{tx + 52},{ty - 170} M{tx + 62},{ty - 70} L{tx - 52},{ty - 170} M{tx - 50},{ty - 190} L{tx + 46},{ty - 300} M{tx + 50},{ty - 190} L{tx - 46},{ty - 300}', 'wood', 8),
             S(f'M{tx - 66},{ty - 70} L{tx + 66},{ty - 70} M{tx - 54},{ty - 185} L{tx + 54},{ty - 185}', 'wood2', 9),
             R(tx - 78, ty - 420, 156, 70, 'wood', 6), R(tx - 64, ty - 410, 128, 40, 'sky2', 4, .9), S(f'M{tx - 22},{ty - 410} L{tx - 22},{ty - 370} M{tx + 22},{ty - 410} L{tx + 22},{ty - 370}', 'wood2', 6),
             R(tx - 86, ty - 356, 172, 12, 'wood2', 4), poly([(tx - 104, ty - 418), (tx + 104, ty - 418), (tx, ty - 486)], 'roof'),
             S(f'M{tx},{ty - 486} L{tx},{ty - 540}', 'wood2', 5), poly([(tx, ty - 540), (tx + 46, ty - 528), (tx, ty - 514)], 'red')]
    s.layer('tower', [G(tower, 'filter="url(#sh)"')], 'rise', .75, depth=.55)
    s.layer('flag', [poly([(tx, ty - 540), (tx + 46, ty - 528), (tx, ty - 514)], 'red')], 'fade', 1.1, loop='sway', origin=f'{tx} {ty - 527}', depth=.55)
    s.layer('sign', [no_fire_sign(420, 900, 1.15, 'wood2', 'board', 'red', 'fl', 'fl2'),
                     R(326, 418, 188, 44, 'red', 10, extra='filter="url(#shs)"'), T(420, 450, '护林防火', 30, '#ffffff')], 'pop', .9, depth=.8)
    s.layer('near', [gold_tree(-20, 1100, 1.6, 't3', 't1', 't4', 'trunk2'), gold_tree(1960, 1120, 1.7, 't1', 't2', 't3', 'trunk2'),
                     grass_tufts(3, 26, 160, 1760, 1000, 'grass'), leaves(5, 70, 0, W, 900, 1080, ['t1', 't3', 't4', 't2'])], 'rise', 1.0, depth=1)
    s.layer('falling', [leaves(8, 22, 0, W, 60, 700, ['t1', 't3', 't4', 't2'], 1.2, 2.0)], 'fade', 1.2, loop='fall', depth=.9)
    return s


# ============ s102 秋收田野 · 秸秆禁烧 ============
def s102():
    s = Scene('s102', '秋收田野·秸秆禁烧', '季节专题', ['安全', '秸秆禁烧', '农村', '秋收', '秋天'],
              dict(sky1='#86C3EA', sky2='#FFEBC9', sun='#FFF1C9', hill='#D9B97A', hill2='#C9A161', field='#F2C653', field2='#E3AA3A',
                   stub='#C99A48', stub2='#B07F35', straw='#F5D27A', straw2='#D9A84A', straw3='#B5822F', **AUTUMN,
                   wall='#F3E6CF', wall2='#DCC7A6', roof='#8F4A36', roof2='#6E3626', door='#9C5C3A', corn='#F7B528', corn2='#E08A1B', pers='#F07A2A',
                   post='#7F4C2C', board='#F9F3E3', red='#E2382F', fl='#F2622E', fl2='#FFB238', smoke='#B9A99A'),
              desc='秋收后的田野：金色麦田与收割后的茬地、圆柱草卷和尖顶秸秆垛、挂满玉米串的农家小院与柿子树、禁止焚烧秸秆标牌。',
              stand={'ground_y': 870, 'x': [560, 1380]})
    s.layer('sky', [R(0, 0, W, 700, s.lg([(0, 'sky1'), (1, 'sky2')])), C(360, 190, 66, 'sun'), C(360, 190, 150, 'sun', .3, 'filter="url(#b40)"')], 'fade', 0, depth=0)
    s.layer('clouds', [cloud(900, 150, .8, op=.9), cloud(1500, 110, .65, op=.85), cloud(1850, 260, .4, op=.7)], 'slide-r', .15, loop='drift', depth=.05)
    s.layer('hills', [P(smooth(ridge(600, 110, 21, 220), 800), 'hill'), P(smooth(ridge(640, 60, 23, 180), 800), 'hill2'),
                      G([C(x, 610 + 10 * math.sin(x), 26, c) for x, c in [(120, 't1'), (170, 't3'), (1640, 't1'), (1700, 't4'), (1760, 't1'), (980, 't3'), (1020, 't1')]])], 'rise', .25, depth=.15)
    rows = []
    for k in range(9):  # 透视田垄
        y = 680 + k * k * 5.2 + k * 14
        rows.append(S(f'M-50,{y:.0f} Q960,{y - 14:.0f} 1970,{y:.0f}', 'stub2' if k % 2 else 'field2', 3 + k * .8, .7))
    s.layer('field', [R(0, 660, W, 420, s.lg([(0, 'field'), (.45, 'stub'), (1, 'stub2')]))] + rows, 'rise', .35, depth=.5)
    # 农家院
    hx, hy = 1480, 730
    house = [R(hx - 210, hy - 170, 420, 170, 'wall'), R(hx - 210, hy - 30, 420, 30, 'wall2'),
             poly([(hx - 240, hy - 160), (hx + 240, hy - 160), (hx + 190, hy - 250), (hx - 190, hy - 250)], 'roof'),
             R(hx - 240, hy - 168, 480, 14, 'roof2', 4), R(hx - 40, hy - 120, 80, 120, 'door', 6), R(hx - 160, hy - 130, 80, 60, 'sky2', 6), R(hx + 90, hy - 130, 80, 60, 'sky2', 6)]
    for j, cx in enumerate([hx - 90, hx + 64, hx + 190]):  # 玉米串
        for q in range(5):
            house.append(E(cx + (q % 2) * 10 - 5, hy - 140 + q * 22, 10, 16, 'corn' if (q + j) % 2 else 'corn2'))
    s.layer('house', [G(house, 'filter="url(#sh)"')], 'rise', .5, depth=.4)
    tx0 = hx - 330
    ptree = [P(f'M{tx0 - 12},{hy + 10} L{tx0},{hy - 150} L{tx0 + 10},{hy + 10}Z', 'trunk')]
    for dx, dy, r, c in [(0, -210, 80, 't1'), (-60, -170, 52, 't3'), (60, -165, 56, 't1'), (20, -250, 50, 't2')]:
        ptree.append(C(tx0 + dx, hy + dy, r, c))
    for dx, dy in [(-40, -190), (30, -220), (60, -160), (-10, -150), (-70, -230)]:
        ptree.append(C(tx0 + dx, hy + dy, 11, 'pers'))
    s.layer('persimmon', ptree, 'grow', .65, depth=.42)
    stacks = []
    for x, y, sc in [(330, 800, 1.0), (180, 760, .7), (1880, 780, .8)]:  # 尖顶秸秆垛
        stacks.append(G([P(f'M{x - 110 * sc},{y} Q{x - 100 * sc},{y - 150 * sc} {x},{y - 230 * sc} Q{x + 100 * sc},{y - 150 * sc} {x + 110 * sc},{y}Z', 'straw'),
                         P(f'M{x},{y - 230 * sc} Q{x + 100 * sc},{y - 150 * sc} {x + 110 * sc},{y} L{x + 30 * sc},{y}Z', 'straw2', .7),
                         S(f'M{x - 96 * sc},{y - 70 * sc} Q{x},{y - 90 * sc} {x + 96 * sc},{y - 70 * sc} M{x - 70 * sc},{y - 150 * sc} Q{x},{y - 166 * sc} {x + 70 * sc},{y - 150 * sc}', 'straw3', 4 * sc, .7)]))
    for x, y, sc in [(1140, 860, 1.0), (1260, 880, .9), (700, 830, .7)]:  # 圆柱草卷
        stacks.append(G([R(x - 70 * sc, y - 110 * sc, 140 * sc, 110 * sc, 'straw2', 0), E(x - 70 * sc, y - 55 * sc, 30 * sc, 55 * sc, 'straw'),
                         ring(x - 70 * sc, y - 55 * sc, 30 * sc, 'straw3', 3), ring(x - 70 * sc, y - 55 * sc, 14 * sc, 'straw3', 3), E(x, y, 80 * sc, 10 * sc, 'stub2', .5)]))
    s.layer('straw', [G(stacks, 'filter="url(#sh)"')], 'pop', .8, depth=.62)
    s.layer('sign', [no_fire_sign(1800, 960, 1.1, 'post', 'board', 'red', 'fl', 'fl2'), R(1690, 504, 220, 44, 'red', 10, extra='filter="url(#shs)"'), T(1800, 536, '禁止焚烧秸秆', 28, '#ffffff')], 'pop', 1.0, depth=.85)
    s.layer('near', [grass_tufts(7, 40, 0, W, 1080, 'stub2', 50), leaves(9, 30, 0, W, 960, 1080, ['t1', 't3', 'corn2'])], 'rise', 1.05, depth=1)
    s.layer('falling', [leaves(12, 14, 1100, W, 300, 760, ['t1', 't3', 't4'], 1.2, 1.9)], 'fade', 1.2, loop='fall', depth=.9)
    return s


# ============ s103 银杏校园 ============
def s103():
    s = Scene('s103', '银杏校园', '季节专题', ['校园', '秋天', '消防', '安全'],
              dict(sky1='#8DCBF0', sky2='#E8F5FF', bld='#F4E9DC', bld2='#E2D0BC', bld3='#C9B39B', win='#9CCBE6', win2='#D5EDFA', roofb='#C7553D',
                   ground='#E9D6B4', ground2='#D9C09A', mat='#F7C844', **AUTUMN, pole='#C9CED6', flag='#E2382F', star='#FFD84A',
                   cab='#E2382F', cab2='#B9271F', glass='#DFF1FA', ext='#D42C24', hyd='#E2382F', hyd2='#B9271F'),
              desc='秋日校园：教学楼前两排金黄银杏、满地黄叶铺成的金色地毯、国旗、红色消防栓和消防器材箱，适合开场与校园防火。',
              stand={'ground_y': 860, 'x': [540, 1380]})
    s.layer('sky', [R(0, 0, W, 760, s.lg([(0, 'sky1'), (1, 'sky2')]))], 'fade', 0, depth=0)
    s.layer('clouds', [cloud(420, 150, .8, op=.95), cloud(1400, 110, .6, op=.85)], 'slide-l', .1, loop='drift', depth=.05)
    b = [R(360, 260, 1200, 470, 'bld'), R(360, 260, 1200, 34, 'bld2'), R(840, 200, 240, 530, 'bld2'), R(870, 230, 180, 90, 'bld', 10), C(960, 275, 34, '#ffffff'),
         S('M960,275 L960,253 M960,275 L978,282', 'bld3', 5), R(900, 590, 120, 140, 'bld3', 6), R(912, 600, 96, 130, 'win', 4)]
    for r in range(3):
        for cidx in range(6):
            for side in (0, 1):
                x = 400 + cidx * 70 + side * 760; y = 340 + r * 110
                b += [R(x, y, 52, 70, 'win', 4), R(x + 4, y + 4, 20, 62, 'win2', 2, .7)]
    b += [R(360, 720, 1200, 12, 'bld3')]
    s.layer('building', [G(b, 'filter="url(#sh)"')], 'rise', .25, depth=.3)
    s.layer('flagpole', [R(1700, 330, 10, 430, 'pole', 4), C(1705, 326, 9, 'pole')], 'grow', .4, depth=.35)
    s.layer('flag', [P('M1710,340 Q1760,330 1800,345 Q1840,360 1880,350 L1880,440 Q1840,450 1800,435 Q1760,420 1710,430Z', 'flag'), C(1740, 368, 12, 'star')], 'fade', .9, loop='sway', origin='1710 385', depth=.35)
    s.layer('ground', [R(0, 730, W, 350, s.lg([(0, 'ground'), (1, 'ground2')])),
                       P('M700,1080 L880,732 L1040,732 L1220,1080Z', 'mat', .55), leaves(31, 220, 0, W, 740, 1080, ['t1', 't2', 'mat', 't3'], .7, 1.4)], 'rise', .35, depth=.6)
    trees = []
    for x, sc in [(150, 1.05), (420, .8), (1500, .8), (1780, 1.05)]:
        trees.append(ginkgo(x, 800 + (sc - .8) * 140, sc * 1.3, 't1', 't2', 't3', 'trunk'))
    s.layer('ginkgo', trees, 'grow', .5, depth=.65)
    fx = [R(560, 690, 110, 170, 'cab', 10), R(572, 704, 86, 120, 'glass', 6), R(596, 730, 38, 86, 'ext', 12), R(606, 716, 18, 18, 'cab2', 4), R(560, 836, 110, 24, 'cab2', 4),
          R(1330, 790, 46, 70, 'hyd', 10), R(1318, 776, 70, 22, 'hyd2', 8), C(1353, 772, 18, 'hyd'), R(1312, 812, 18, 22, 'hyd2', 4), R(1376, 812, 18, 22, 'hyd2', 4), E(1353, 862, 50, 9, 'ground2', .7)]
    s.layer('fire_gear', [G(fx, 'filter="url(#shs)"')], 'pop', .8, depth=.7)
    s.layer('near', [ginkgo(-60, 1200, 1.9, 't1', 't2', 't3', 'trunk2'), leaves(33, 50, 0, W, 980, 1080, ['t1', 't2', 't3'], 1.4, 2.4)], 'rise', 1.0, depth=1)
    s.layer('falling', [leaves(35, 26, 0, W, 40, 720, ['t1', 't2', 'mat'], 1.2, 2.0)], 'fade', 1.1, loop='fall', depth=.9)
    return s


# ============ s104 秋冬客厅 · 取暖用电 ============
def s104():
    s = Scene('s104', '秋冬客厅·取暖用电', '季节专题', ['家庭', '用电安全', '取暖', '秋天'],
              dict(wall='#F5E3CC', wall2='#EBCFAF', floor='#C98F5E', floor2='#B47A4C', rug='#E9765A', rug2='#F4A27C', win='#9ED3F0', win2='#FFE6B0', frame='#FFFFFF',
                   sofa='#5E8FB8', sofa2='#4A7AA3', pillow='#F7C85A', blanket='#E4574B', **AUTUMN,
                   heater='#ECEFF2', heater2='#B9C2CC', coil='#FF7A2E', glow='#FFB24A', strip='#FFFFFF', strip2='#C9CED6', plug='#3E4A5A', wire='#3E4A5A',
                   rack='#9AA5B1', cloth1='#7FC8A9', cloth2='#F4A6B8', lamp='#FFD98A', shelf='#A4693F'),
              desc='秋冬傍晚的客厅：窗外金黄秋树，电暖器亮着橙光、旁边晾着衣服，一个插线板插满插头、电线乱拉，是家庭用电防火的教学场景。',
              stand={'ground_y': 870, 'x': [620, 1300]})
    s.layer('wall', [R(0, 0, W, 860, s.lg([(0, 'wall'), (1, 'wall2')])), R(0, 820, W, 40, 'wall2')], 'fade', 0, depth=.4)
    win = [R(1180, 150, 560, 420, 'frame', 12), R(1200, 170, 520, 380, s.lg([(0, 'win'), (1, 'win2')]), 6),
           gold_tree(1330, 600, 1.1, 't1', 't2', 't3', 'trunk'), gold_tree(1600, 640, 1.3, 't3', 't1', 't4', 'trunk'),
           R(1450, 170, 20, 380, 'frame'), R(1200, 350, 520, 16, 'frame')]
    cp1 = s.clip('<rect x="1180" y="150" width="560" height="420" rx="12"/>'); cp2 = s.clip('<rect x="1200" y="170" width="520" height="380"/>')
    s.layer('window', [G(win, f'clip-path="{cp1}"'), R(1160, 560, 600, 22, 'frame', 8)], 'fade', .15, depth=.2)
    s.layer('window_leaves', [G([leaves(41, 10, 1210, 1700, 190, 520, ['t1', 't3'], 1.2, 1.8)], f'clip-path="{cp2}"')], 'fade', .5, loop='fall', depth=.2)
    s.layer('shelf', [R(160, 260, 360, 18, 'shelf', 6), R(190, 210, 40, 50, 't3', 4), R(240, 190, 30, 70, 'sofa', 4), R(280, 220, 60, 40, 't1', 4), C(430, 230, 28, 'cloth1'),
                      R(160, 400, 360, 18, 'shelf', 6), R(200, 340, 90, 60, 'pillow', 6), R(330, 350, 26, 50, 'rug', 4)], 'slide-l', .3, depth=.4)
    s.layer('floor', [R(0, 860, W, 220, s.lg([(0, 'floor'), (1, 'floor2')])), E(960, 960, 560, 70, 'rug'), E(960, 960, 470, 52, 'rug2', .6)], 'rise', .2, depth=.6)
    s.layer('sofa', [G([R(140, 600, 520, 200, 'sofa', 40), R(110, 690, 580, 140, 'sofa2', 30), R(110, 820, 30, 50, 'shelf'), R(660, 820, 30, 50, 'shelf'),
                        R(190, 630, 140, 100, 'pillow', 24), P('M380,700 L620,690 L640,820 L400,830Z', 'blanket')], 'filter="url(#sh)"')], 'rise', .4, depth=.62)
    # 电暖器 + 晾衣架（隐患）
    hx = 1380
    heat = [R(hx, 640, 200, 240, 'heater', 18), R(hx + 18, 664, 164, 170, 'heater2', 10)]
    for k in range(5): heat.append(R(hx + 30, 680 + k * 30, 140, 12, 'coil', 6))
    heat += [R(hx + 20, 870, 40, 14, 'heater2', 5), R(hx + 140, 870, 40, 14, 'heater2', 5)]
    s.layer('heater', [G(heat, 'filter="url(#sh)"')], 'pop', .6, depth=.7)
    s.layer('heat_glow', [E(hx + 100, 760, 200, 160, 'glow', .45, 'filter="url(#b40)"'), E(hx + 100, 900, 260, 40, 'glow', .35, 'filter="url(#b20)"')], 'fade', 1.0, loop='glow', depth=.7)
    rack = [S(f'M{hx + 250},880 L{hx + 290},560 L{hx + 330},880 M{hx + 410},880 L{hx + 450},560 L{hx + 490},880', 'rack', 7), S(f'M{hx + 280},590 L{hx + 460},590', 'rack', 8),
            P(f'M{hx + 296},592 L{hx + 360},592 L{hx + 352},740 L{hx + 300},740Z', 'cloth1'), P(f'M{hx + 372},592 L{hx + 446},592 L{hx + 440},700 L{hx + 380},700Z', 'cloth2')]
    s.layer('rack', [G(rack)], 'drop', .7, depth=.72)
    # 插线板：插满插头 + 乱线
    px, py = 880, 1000
    strip = [R(px, py, 300, 48, 'strip', 14, extra='filter="url(#shs)"'), R(px + 262, py + 14, 22, 20, 'coil', 6)]
    for k in range(4):
        x = px + 22 + k * 58
        strip += [R(x, py - 20, 40, 34, 'plug', 6), S(f'M{x + 20},{py - 20} Q{x + 20 - 60 + k * 30},{py - 160 - k * 20} {x - 300 + k * 260},{py - 120 - k * 30}', 'wire', 7)]
    strip.append(S(f'M{px},{py + 24} Q{px - 200},{py + 40} {px - 420},{py - 10} Q{px - 560},{py - 60} {px - 620},{py - 20}', 'wire', 8))
    strip.append(S(f'M{px + 150},{py - 160} Q{px + 380},{py - 120} {hx + 30},{py - 130}', 'wire', 8))
    s.layer('power_strip', [G(strip)], 'rise', .85, depth=.9)
    s.layer('lamp', [R(1900 - 120, 360, 14, 500, 'shelf'), P('M1720,370 L1850,370 L1820,280 L1750,280Z', 'lamp'), E(1785, 380, 120, 60, 'lamp', .3, 'filter="url(#b20)"')], 'fade', .9, depth=.5)
    return s


# ============ s105 金秋消防站 ============
def s105():
    s = Scene('s105', '金秋消防站', '季节专题', ['安全', '消防', '119', '秋天'],
              dict(sky1='#86C6EE', sky2='#FFEFD4', bld='#E04A3B', bld2='#B9342A', bld3='#F5E6D4', door='#F2F2F2', door2='#C9CED6', win='#A9D6F0',
                   truck='#E2382F', truck2='#B42820', truck3='#F2F2F2', tire='#2F3640', ladder='#C9CED6', light='#3FA1F2', light2='#FF4A3D',
                   ground='#D9D2C6', ground2='#BDB4A6', line='#FFFFFF', **AUTUMN, hose='#F2C14A'),
              desc='金秋的消防站：红色消防站、敞开的车库门里停着消防车、训练塔，门前两棵金黄大树和落叶，适合讲 119 报警与消防员叔叔。',
              stand={'ground_y': 900, 'x': [520, 1400]})
    s.layer('sky', [R(0, 0, W, 760, s.lg([(0, 'sky1'), (1, 'sky2')]))], 'fade', 0, depth=0)
    s.layer('clouds', [cloud(300, 140, .7, op=.9), cloud(1100, 100, .55, op=.85)], 'slide-r', .1, loop='drift', depth=.05)
    b = [R(1460, 120, 200, 620, 'bld2'), R(1490, 150, 140, 60, 'win', 6), R(1490, 260, 140, 60, 'win', 6), R(1490, 370, 140, 60, 'win', 6), R(1440, 100, 240, 30, 'bld3', 6),
         R(300, 300, 1180, 440, 'bld'), R(300, 300, 1180, 50, 'bld2'), R(300, 350, 1180, 90, 'bld3')]
    for k in range(3):
        x = 360 + k * 370
        b += [R(x, 470, 320, 270, 'door2', 10), R(x + 10, 480, 300, 64, 'door', 4)]
    b += [C(890, 395, 36, '#ffffff'), T(890, 410, '119', 34, 'bld'), R(300, 730, 1180, 14, 'bld2')]
    s.layer('station', [G(b, 'filter="url(#sh)"')], 'rise', .25, depth=.3)
    tr = [R(760, 560, 420, 160, 'truck'), R(1100, 590, 130, 130, 'truck', 14), R(1130, 605, 80, 56, 'win', 6), R(760, 690, 470, 40, 'truck2'),
          S('M780,560 L1080,520', 'ladder', 10), S('M780,544 L1080,504', 'ladder', 6), R(800, 600, 260, 20, 'truck3', 6), R(1150, 575, 40, 16, 'light', 6)]
    for x in (840, 1140): tr += [C(x, 740, 44, 'tire'), C(x, 740, 18, 'door2')]
    s.layer('truck', [G(tr, 'filter="url(#sh)"')], 'slide-r', .55, depth=.45)
    s.layer('siren', [R(1150, 575, 20, 16, 'light2', 4), E(1170, 580, 60, 30, 'light', .5, 'filter="url(#b20)"')], 'fade', 1.0, loop='twinkle', depth=.45)
    s.layer('ground', [R(0, 740, W, 340, s.lg([(0, 'ground'), (1, 'ground2')])), S('M0,900 L1920,900', 'line', 6, .6),
                       leaves(51, 90, 0, W, 760, 1080, ['t1', 't3', 't2'], .7, 1.3)], 'rise', .35, depth=.6)
    s.layer('trees', [gold_tree(150, 860, 1.5, 't1', 't2', 't3', 'trunk'), gold_tree(1790, 860, 1.4, 't3', 't1', 't4', 'trunk')], 'grow', .5, depth=.65)
    s.layer('hose', [G([C(1560, 840, 46, 'hose'), C(1560, 840, 30, 'bld2'), C(1560, 840, 14, 'hose')], 'filter="url(#shs)"')], 'pop', .9, depth=.75)
    s.layer('falling', [leaves(55, 20, 0, W, 60, 720, ['t1', 't3', 't2'], 1.2, 2.0)], 'fade', 1.1, loop='fall', depth=.9)
    return s



# ============ s106 秋山枫林·石径人家（古诗《山行》等秋景） ============
def s106():
    s = Scene('s106', '秋山枫林·石径人家', '季节专题', ['语文', '古诗', '秋天', '秋游', '山水'],
              dict(sky1='#9CCBEA', sky2='#FFE3C4', sun='#FFF0C4', mtn='#C7B5D3', mtn2='#AF97C1', far='#E8743A', far2='#D9542B',
                   ground='#E3B07A', ground2='#C98F5A', path='#EADFCB', path2='#BFAF96', **AUTUMN,
                   wall='#F6EEE0', wall2='#DCCDB6', roof='#5B5F6E', roof2='#454856', door='#8A5536', grass='#B9743A'),
              desc='层林尽染的秋山：远处青紫群山、白云缭绕的半山腰有几户白墙灰瓦人家，一条石阶小路弯弯曲曲伸向山上，满山枫红，落叶飘飞。无任何标牌，适合古诗《山行》与秋游。',
              stand={'ground_y': 930, 'x': [460, 1460]})
    s.layer('sky', [R(0, 0, W, 760, s.lg([(0, 'sky1'), (1, 'sky2')])), C(1560, 190, 66, 'sun'), C(1560, 190, 140, 'sun', .35, 'filter="url(#b40)"')], 'fade', 0, depth=0)
    s.layer('mountains', [P(smooth(ridge(560, 230, 31), 800), 'mtn'), P(smooth(ridge(610, 150, 37, 150), 800), 'mtn2', .9),
                          R(0, 470, W, 200, s.lg([(0, 'sky2', 0), (1, 'sky2', .7)]))], 'rise', .15, depth=.15)
    # 半山腰人家
    hs = []
    for hx, hy, sc in [(1240, 430, .55), (1340, 445, .45), (1150, 452, .4)]:
        hs.append(G([R(hx - 60 * sc, hy - 70 * sc, 120 * sc, 70 * sc, 'wall'), R(hx - 60 * sc, hy - 12 * sc, 120 * sc, 12 * sc, 'wall2'),
                     poly([(hx - 78 * sc, hy - 64 * sc), (hx + 78 * sc, hy - 64 * sc), (hx + 56 * sc, hy - 104 * sc), (hx - 56 * sc, hy - 104 * sc)], 'roof'),
                     R(hx - 80 * sc, hy - 68 * sc, 160 * sc, 8 * sc, 'roof2', 2), R(hx - 12 * sc, hy - 44 * sc, 24 * sc, 44 * sc, 'door', 3)]))
    s.layer('houses', hs, 'fade', .3, depth=.2)
    s.layer('clouds', [cloud(1180, 470, .75, op=.9), cloud(1460, 420, .55, op=.85), cloud(360, 180, .8, op=.9), cloud(860, 120, .55, op=.8)], 'slide-l', .35, loop='drift', depth=.08)
    random.seed(41); far = []
    for k in range(36):
        x = k * 58 - 30 + random.uniform(-14, 14); y = 650 + 26 * math.sin(k * .6) + random.uniform(-8, 8)
        far.append(C(x, y, random.uniform(32, 50), random.choice(['far', 'far2', 't3', 't4', 't1'])))
    s.layer('forest_far', [P(smooth([(-100, 670), (400, 640), (900, 660), (1400, 630), (2020, 660)], 1080), 'far2')] + far, 'rise', .4, depth=.3)
    # 石径：从画面下方弯弯曲曲伸向远山（S 形，越远越窄），带石阶横纹
    L_ = [(820, 1080), (900, 960), (1060, 880), (1000, 800), (900, 745), (980, 690), (1080, 660)]
    Rr = [(1180, 1080), (1120, 960), (1200, 880), (1080, 800), (960, 745), (1010, 690), (1094, 660)]
    pd = f'M{L_[0][0]},{L_[0][1]}' + ''.join(f' L{x},{y}' for x, y in L_[1:]) + ''.join(f' L{x},{y}' for x, y in reversed(Rr)) + 'Z'
    steps = [S(f'M{a[0]},{a[1]} L{b[0]},{b[1]}', 'path2', max(2, (a[1] - 640) / 70), .8) for a, b in zip(L_, Rr)]
    for a1, a2, b1, b2 in zip(L_, L_[1:], Rr, Rr[1:]):
        for q in (.33, .66):
            xa = a1[0] + (a2[0] - a1[0]) * q; ya = a1[1] + (a2[1] - a1[1]) * q; xb = b1[0] + (b2[0] - b1[0]) * q; yb = b1[1] + (b2[1] - b1[1]) * q
            steps.append(S(f'M{xa:.0f},{ya:.0f} L{xb:.0f},{yb:.0f}', 'path2', max(2, (ya - 640) / 80), .7))
    s.layer('ground', [P(smooth([(-100, 780), (500, 750), (1000, 775), (1500, 745), (2020, 770)], 1080), s.lg([(0, 'ground'), (1, 'ground2')])),
                       P(pd, 'path')] + steps, 'rise', .5, depth=.6)
    mid = []
    for x, sc, a in [(150, 1.0, 0), (330, .8, 1), (640, .62, 2), (1360, .6, 1), (1620, 1.05, 0), (1820, .85, 2)]:
        c1, c2, c3 = [('t4', 't3', 'trunk2'), ('t3', 't1', 't4'), ('t4', 't2', 't3')][a]
        mid.append(gold_tree(x, 800, sc, c1, c2, c3 if c3 != 'trunk2' else 't3', 'trunk'))
    s.layer('trees_mid', mid, 'grow', .65, depth=.62)
    s.layer('near', [gold_tree(-40, 1110, 1.5, 't4', 't3', 't1', 'trunk2'), gold_tree(1980, 1120, 1.6, 't3', 't4', 't1', 'trunk2'),
                     grass_tufts(13, 18, 120, 700, 1010, 'grass'), grass_tufts(14, 18, 1260, 1800, 1010, 'grass'),
                     leaves(15, 60, 0, W, 940, 1080, ['t1', 't3', 't4'])], 'rise', .9, depth=1)
    s.layer('falling', [leaves(18, 22, 0, W, 60, 700, ['t3', 't4', 't1'], 1.2, 2.0)], 'fade', 1.1, loop='fall', depth=.9)
    return s


SCENES = [s101, s102, s103, s104, s105, s106]
