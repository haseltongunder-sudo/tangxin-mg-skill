"""第 1 类 · 校园 s002–s010（平面 MG）"""
from core import *
import math, random


# ---------------- 通用小工具（c01/c02 共用） ----------------
def shadow(x, y, rx, ry, op=.14):
    return E(x, y, rx, ry, '#2a1f33', op)


def star_pts(cx, cy, r, rot=-90, inner=.382):
    pts = []
    for k in range(10):
        a = math.radians(rot + k * 36)
        rr = r if k % 2 == 0 else r * inner
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts


def star(cx, cy, r, col, rot=-90, op=None, extra=''):
    return poly(star_pts(cx, cy, r, rot), col, op, extra)


def leafy(x, y, sc, pot, leaf, leaf2, n=7, potw=70, poth=80):
    """盆栽：x,y 为盆底中心"""
    it = [shadow(x, y + 4, potw * .7 * sc, 8 * sc, .12),
          P(f'M{x - potw / 2 * sc},{y - poth * sc} L{x + potw / 2 * sc},{y - poth * sc} L{x + potw * .38 * sc},{y} L{x - potw * .38 * sc},{y}Z', pot),
          R(x - potw * .56 * sc, y - poth * sc - 10 * sc, potw * 1.12 * sc, 16 * sc, pot, 5 * sc)]
    for k in range(n):
        a = -math.pi / 2 + (k - (n - 1) / 2) * .42
        lx = x + 52 * sc * math.cos(a); ly = y - poth * sc - 22 * sc + 46 * sc * math.sin(a)
        it.append(E(lx, ly, 46 * sc, 15 * sc, leaf if k % 2 else leaf2, extra=f'transform="rotate({math.degrees(a):.0f} {lx:.0f} {ly:.0f})"'))
    return G(it)


def sky_window(s, x, y, w, h, sky1, sky2, frame, deco=None, mull='cross', rx=10, border=14):
    it = [R(x - border, y - border, w + 2 * border, h + 2 * border, frame, rx + 6, extra='filter="url(#shs)"'),
          R(x, y, w, h, s.lg([(0, sky1), (1, sky2)]), rx)]
    if deco:
        cp = s.clip(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/>')
        it.append(G(deco, f'clip-path="{cp}"'))
    if mull in ('cross', 'v'):
        it.append(R(x + w / 2 - 4, y, 8, h, frame))
    if mull == 'cross':
        it.append(R(x, y + h * .42 - 4, w, 8, frame))
    it.append(P(f'M{x + w * .12},{y + h} L{x + w * .3},{y} L{x + w * .38},{y} L{x + w * .2},{y + h}Z', '#ffffff', .18))
    return G(it)


def floor_lines(y0, y1, col, vx=960, vy=380, step=180, op=.45, w=3, rows=(), rowop=.3):
    it = []
    for k in range(-14, 15):
        xb = vx + k * step
        xt = vx + (xb - vx) * (y0 - vy) / (y1 - vy)
        it.append(S(f'M{xt:.0f},{y0} L{xb},{y1}', col, w, op))
    for yy in rows:
        it.append(S(f'M0,{yy} L{W},{yy}', col, 2, rowop))
    return it


# ============ s002 走廊宣传栏 ============
def corridor():
    s = Scene('s002', '走廊宣传栏', '校园', ['班会', '德育', '通用课堂', '校园生活'],
              dict(wall1='#F7FAF6', wall2='#E8F1EB', dado='#8FCFB6', dado2='#6DB89C', floor1='#EEE7DB', floor2='#D9CEBD', speck='#C9BCA6',
                   frame='#C98F5A', frame2='#A8703F', cork='#EBC99B', cork2='#DDB582', paper='#FFFDF6', p1='#FF9E80', p2='#8CCBF0', p3='#FFD66B', p4='#B9A6EE', p5='#9ADBA3',
                   pin='#E8574A', door='#F3A65E', door2='#DB8C45', glass='#CFEAF6', plate='#FFFFFF', ink='#3B4A5A', fire='#E24B3E', fire2='#B8352B', light='#FFF6D6',
                   leaf='#5FAE74', leaf2='#8FCB8E', pot='#F0F2F4'),
              desc='教学楼走廊：中央软木宣传栏贴满作品与红花榜，两侧教室门、消防栓箱与绿植，地面水磨石。', stand={'ground_y': 900, 'x': [560, 1360]})
    s.layer('wall', [R(0, 0, W, 800, s.lg([(0, 'wall1'), (1, 'wall2')])), R(0, 0, W, 36, 'wall2'),
                     R(0, 600, W, 200, s.lg([(0, 'dado'), (1, 'dado2')])), R(0, 596, W, 10, 'dado2'), R(0, 788, W, 14, 'dado2')], 'fade', 0)
    # 顶灯
    s.layer('ceiling_light', [G([R(x - 120, 8, 240, 18, 'plate', 9), E(x, 40, 220, 40, 'light', .55, 'filter="url(#b20)"')]) for x in (480, 1440)], 'fade', .15, loop='glow')
    # 地面（水磨石）
    random.seed(21)
    fl = [R(0, 800, W, 280, s.lg([(0, 'floor1'), (1, 'floor2')]))]
    for _ in range(140):
        fl.append(C(random.uniform(0, W), random.uniform(810, 1075), random.uniform(1.5, 3.5), random.choice(['speck', 'dado', 'p1']), .35))
    fl += floor_lines(800, 1080, 'floor2', step=300, op=.5, rows=(860, 960))
    fl.append(R(560, 812, 800, 70, 'cork', 0, .18, 'filter="url(#b20)"'))
    s.layer('floor', fl, 'rise', .1)

    # 教室门（左右）
    def door(x, num):
        it = [R(x - 18, 236, 276, 568, 'plate', 10, extra='filter="url(#shs)"'), R(x, 252, 240, 548, s.lg([(0, 'door'), (1, 'door2')]), 6),
              R(x + 40, 300, 160, 150, 'glass', 6), R(x + 116, 300, 8, 150, 'plate'), P(f'M{x + 56},450 L{x + 96},300 L{x + 112},300 L{x + 72},450Z', '#ffffff', .4),
              R(x + 24, 500, 192, 260, 'door2', 8, .45), R(x + 196, 530, 14, 54, 'ink', 6), R(x + 186, 548, 30, 12, 'ink', 6),
              R(x + 50, 176, 140, 46, 'plate', 10, extra='filter="url(#shs)"'), R(x + 50, 176, 22, 46, 'dado2', 8), T(x + 132, 210, num, 30, 'ink', 800)]
        return G(it)
    s.layer('doors', [door(80, '301'), door(1600, '302')], 'rise', .25)
    # 宣传栏
    bx, by, bw, bh = 470, 150, 980, 420
    bd = [R(bx - 22, by - 22, bw + 44, bh + 44, 'frame', 18, extra='filter="url(#sh)"'), R(bx, by, bw, bh, s.lg([(0, 'cork'), (1, 'cork2')]), 8)]
    random.seed(4)
    for _ in range(90):
        bd.append(C(random.uniform(bx + 6, bx + bw - 6), random.uniform(by + 6, by + bh - 6), random.uniform(1.5, 3), 'frame2', .25))
    # 顶部波浪彩边
    for k in range(20):
        x0 = bx + k * bw / 20
        bd.append(P(f'M{x0},{by} L{x0 + bw / 20},{by} L{x0 + bw / 20},{by + 14} Q{x0 + bw / 40},{by + 34} {x0},{by + 14}Z', ['p1', 'p3', 'p2', 'p5'][k % 4]))
    s.layer('board', bd, 'drop', .35)

    def card(x, y, w, h, rot, inner):
        return G([R(x, y, w, h, 'paper', 6, extra='filter="url(#shs)"')] + inner + [C(x + w / 2, y + 10, 8, 'pin'), C(x + w / 2 - 2, y + 8, 3, '#ffffff', .8)],
                 f'transform="rotate({rot} {x + w / 2} {y + h / 2})"')
    # 1 红花榜（星星格）
    grid = []
    for r_ in range(5):
        grid.append(R(522, 262 + r_ * 38, 40, 26, 'p2', 4, .7))
        for k in range(r_ % 3 + 2):
            grid.append(star(588 + k * 34, 275 + r_ * 38, 13, 'p1' if (r_ + k) % 2 else 'p3'))
    c1 = card(506, 214, 240, 236, -2, [R(506, 214, 240, 36, 'p1', 6), R(506, 238, 240, 12, 'p1')] + grid)
    # 2 儿童画：房子与太阳
    c2 = card(782, 200, 250, 190, 2, [R(796, 216, 222, 158, s.lg([(0, 'p2'), (1, 'paper')]), 4), C(980, 252, 22, 'p3'), R(796, 330, 222, 44, 'p5', 0, .9),
                                       poly([(840, 300), (900, 252), (960, 300)], 'p1'), R(852, 298, 96, 50, 'paper'), R(890, 316, 22, 32, 'p4')])
    # 3 照片墙
    ph = []
    for r_ in range(2):
        for k in range(3):
            x = 1078 + k * 108; y = 214 + r_ * 104
            ph += [R(x, y, 96, 90, 'paper', 4, extra='filter="url(#shs)"'), R(x + 6, y + 6, 84, 64, ['p2', 'p5', 'p3', 'p4', 'p1', 'p2'][r_ * 3 + k], 3, .85),
                   C(x + 30, y + 30, 10, 'paper', .8), P(f'M{x + 6},{y + 70} L{x + 40},{y + 40} L{x + 64},{y + 58} L{x + 90},{y + 44} L{x + 90},{y + 70}Z', 'paper', .55), C(x + 48, y + 4, 6, ['pin', 'p2', 'p3'][k])]
    # 4 下排：横幅与小卡片
    c4 = card(800, 420, 200, 120, -3, [R(816, 444, 120, 10, 'ink', 4, .25), R(816, 466, 160, 8, 'ink', 4, .18), R(816, 484, 140, 8, 'ink', 4, .18), R(816, 502, 100, 8, 'ink', 4, .18)])
    c5 = card(1040, 436, 160, 110, 3, [C(1120, 490, 34, 'p3'), *[S(f'M{1120 + 40 * math.cos(a):.0f},{490 + 40 * math.sin(a):.0f} L{1120 + 50 * math.cos(a):.0f},{490 + 50 * math.sin(a):.0f}', 'p3', 4) for a in [k * math.pi / 4 for k in range(8)]]])
    c6 = card(1236, 432, 180, 112, -2, [R(1252, 452, 148, 78, 'p4', 4, .35), *[R(1264 + k * 34, 510 - h, 22, h, ['p1', 'p2', 'p3', 'p5'][k], 3) for k, h in enumerate([28, 50, 38, 60])]])
    c7 = card(520, 470, 230, 76, 1, [R(536, 490, 198, 12, 'p5', 6), R(536, 512, 150, 10, 'ink', 5, .18)])
    s.layer('posters', [c1, c2, G(ph), c4, c5, c6, c7], 'pop', .55)
    s.layer('stickers', [star(760, 196, 18, 'p3'), star(1060, 548, 14, 'p1'), star(1430, 196, 16, 'p2'), star(482, 556, 12, 'p5')], 'pop', 1.1, loop='twinkle')
    # 消防栓箱 + 绿植
    fb = [R(1446, 620, 104, 160, s.lg([(0, 'fire'), (1, 'fire2')]), 8, extra='filter="url(#shs)"'), R(1458, 634, 80, 100, 'glass', 4, .5),
          S('M1498,690 a22,22 0 1,0 0.1,0', 'fire2', 6), R(1462, 748, 72, 16, 'plate', 4, .7)]
    s.layer('fire_box', fb, 'pop', .8)
    s.layer('plant', [leafy(400, 830, 1.15, 'pot', 'leaf', 'leaf2', 9)], 'grow', .9, loop='sway', origin='400 830')
    # 彩旗挂饰
    gl = [S(f'M{bx - 10},{by - 40} Q960,{by + 10} {bx + bw + 10},{by - 40}', 'frame2', 3, .7)]
    for k in range(13):
        u = (k + .5) / 13; x = bx - 10 + (bw + 20) * u; y = by - 40 + 50 * 4 * u * (1 - u) * .5 + 2
        gl.append(poly([(x - 18, y), (x + 18, y), (x, y + 32)], ['p1', 'p3', 'p2', 'p5', 'p4'][k % 5]))
    s.layer('garland', gl, 'drop', 1.0, loop='sway')
    return s


# ============ s003 食堂 ============
def canteen():
    s = Scene('s003', '食堂', '校园', ['营养', '健康饮食', '劳动', '校园生活'],
              dict(wall1='#FFF4DE', wall2='#FBE4BE', tile='#E6F4EF', tile2='#CFE6DE', steel='#D6DEE4', steel2='#AFBCC6', steel3='#8C9BA7', front='#F58E6E', front2='#E27657',
                   glass='#E6F6FF', rice='#FFFDF4', egg='#FFD24F', tomato='#EE5A3F', green='#62B861', green2='#93D57E', meat='#C77C47', corn='#F8C93A', carrot='#F3963A',
                   board='#3E6B5C', board2='#335A4D', lamp='#FFE29A', lampc='#4F8F87', floor1='#F2E8DA', floor2='#DCCDB6', table='#FFFFFF', tabletop='#8FD1C7', stool='#F7B84B',
                   tray='#7FC4E8', tray2='#5FA9D2', bowl='#FFFFFF', soup='#F5B85A'),
              desc='明亮食堂：不锈钢打菜窗口里有米饭、番茄炒蛋、青菜和红烧肉，上方菜单牌，两侧餐桌摆着餐盘。', stand={'ground_y': 900, 'x': [560, 1360]})
    bg = [R(0, 0, W, 800, s.lg([(0, 'wall1'), (1, 'wall2')]))]
    s.layer('wall', bg, 'fade', 0)
    # 后厨瓷砖区
    kt = [R(220, 280, 1480, 330, 'tile')]
    for x in range(220, 1701, 60): kt.append(R(x, 280, 2, 330, 'tile2'))
    for y in range(280, 611, 60): kt.append(R(220, y, 1480, 2, 'tile2'))
    kt += [R(200, 262, 1520, 22, 'steel2', 6), R(200, 262, 24, 360, 'steel2'), R(1696, 262, 24, 360, 'steel2')]
    kt += [R(300, 380, 1320, 12, 'steel2', 4, extra='filter="url(#shs)"')]
    for k, x in enumerate(range(360, 1600, 170)):
        if k % 3 == 0:
            kt += [R(x, 316, 110, 64, 'steel', 10), R(x - 10, 310, 130, 12, 'steel3', 6), R(x + 40, 298, 30, 14, 'steel3', 6)]
        elif k % 3 == 1:
            kt += [E(x + 55, 352, 62, 28, 'steel'), R(x - 16, 346, 30, 8, 'steel3', 4), R(x + 110, 346, 40, 8, 'steel3', 4)]
        else:
            kt += [S(f'M{x + 20},300 L{x + 20},360', 'steel3', 5), E(x + 20, 366, 16, 10, 'steel3'), S(f'M{x + 70},300 L{x + 70},350', 'steel3', 5), R(x + 56, 348, 28, 26, 'steel3', 4)]
    s.layer('kitchen', kt, 'fade', .1)
    # 菜单牌（无字，图示）
    mb = []
    for k, x in enumerate((330, 760, 1190)):
        mb += [S(f'M{x + 60},60 L{x + 60},100 M{x + 340},60 L{x + 340},100', 'steel3', 3), R(x, 96, 400, 150, 'board', 14, extra='filter="url(#sh)"'), R(x + 10, 106, 380, 130, 'board2', 10)]
        for j in range(3):
            cx = x + 70 + j * 130
            col = [['tomato', 'green', 'meat'], ['corn', 'egg', 'green2'], ['carrot', 'tomato', 'soup']][k][j]
            mb += [E(cx, 172, 46, 30, 'bowl'), E(cx, 162, 38, 16, col), C(cx - 10, 158, 6, '#ffffff', .5), R(cx - 30, 212, 60, 8, 'lamp', 4, .8)]
    s.layer('menu', mb, 'drop', .3)
    # 打菜台
    ct = [R(150, 590, 1620, 34, s.lg([(0, 'steel'), (1, 'steel2')]), 8, extra='filter="url(#shs)"'), R(150, 620, 1620, 190, s.lg([(0, 'front'), (1, 'front2')]), 6)]
    for x in range(190, 1740, 200): ct.append(R(x, 650, 160, 130, 'front2', 10, .45))
    ct.append(R(150, 620, 1620, 8, 'front2'))
    s.layer('counter', ct, 'rise', .2)

    def pan(x, y, w, kind):
        it = [R(x, y, w, 46, 'steel3', 6), R(x + 6, y + 4, w - 12, 18, 'steel', 4)]
        cx = x + w / 2
        random.seed(int(x))
        if kind == 'rice':
            it += [P(f'M{x + 8},{y + 14} Q{cx},{y - 52} {x + w - 8},{y + 14}Z', 'rice')] + [E(random.uniform(x + 30, x + w - 30), random.uniform(y - 4, y + 10), 5, 2.5, 'tile2') for _ in range(18)]
        elif kind == 'eggtom':
            it += [P(f'M{x + 8},{y + 14} Q{cx},{y - 40} {x + w - 8},{y + 14}Z', 'egg')]
            it += [P(f'M{random.uniform(x + 24, x + w - 44):.0f},{random.uniform(y - 2, y + 8):.0f} l18,-4 l6,14 l-20,4Z', 'tomato') for _ in range(9)]
        elif kind == 'greens':
            it += [P(f'M{x + 8},{y + 14} Q{cx},{y - 40} {x + w - 8},{y + 14}Z', 'green')]
            it += [E(random.uniform(x + 26, x + w - 26), random.uniform(y - 2, y + 10), 16, 6, 'green2', extra=f'transform="rotate({random.randint(-30, 30)} {cx} {y})"') for _ in range(12)]
        elif kind == 'meat':
            it += [P(f'M{x + 8},{y + 14} Q{cx},{y - 12} {x + w - 8},{y + 14}Z', 'meat', .6)]
            for k in range(7): it += [R(x + 22 + k * (w - 60) / 6, y - 6 + (k % 2) * 8, 30, 24, 'meat', 6), R(x + 22 + k * (w - 60) / 6, y - 6 + (k % 2) * 8, 30, 8, '#F2D3B0', 4, .8)]
        elif kind == 'corn':
            it += [P(f'M{x + 8},{y + 14} Q{cx},{y - 40} {x + w - 8},{y + 14}Z', 'corn')]
            it += [C(random.uniform(x + 20, x + w - 20), random.uniform(y - 2, y + 10), 5, random.choice(['carrot', 'green', 'egg'])) for _ in range(30)]
        return G(it)
    fd = [R(230, 548, 1460, 14, 'steel2', 4)]
    kinds = ['rice', 'eggtom', 'greens', 'meat', 'corn']
    for k, kd in enumerate(kinds):
        fd.append(pan(250 + k * 290, 548, 260, kd))
    s.layer('food', fd, 'pop', .5)
    # 防护玻璃
    gl = [R(230, 430, 1460, 16, 'steel2', 6), R(230, 446, 1460, 100, 'glass', 0, .35)]
    for x in (230, 520, 810, 1100, 1390, 1680): gl.append(R(x, 430, 10, 132, 'steel3', 4))
    gl.append(P('M300,446 L360,446 L330,546 L270,546Z', '#ffffff', .35))
    s.layer('sneeze_guard', gl, 'fade', .65)
    # 汤桶 + 餐盘堆
    sp = [R(1620, 470, 120, 120, s.lg([(0, 'steel'), (1, 'steel3')]), 12, extra='filter="url(#shs)"'), E(1680, 470, 60, 12, 'soup'), R(1606, 462, 148, 14, 'steel2', 6)]
    for k in range(8): sp.append(R(60, 576 - k * 9, 150, 10, 'tray' if k % 2 else 'tray2', 4))
    sp += [R(40, 586, 190, 14, 'steel2', 6)]
    s.layer('soup_trays', sp, 'pop', .75)
    s.layer('steam', [S(f'M{x},450 q-14,-24 0,-48 q14,-24 0,-48', '#ffffff', 6, .75) for x in (1660, 1700)] + [S(f'M{x},540 q-10,-18 0,-36 q10,-18 0,-36', '#ffffff', 5, .6) for x in (400, 1000)], 'fade', 1.1, loop='flow')
    # 吊灯
    lp = []
    for x in (560, 960, 1360):
        lp += [S(f'M{x},0 L{x},40', 'steel3', 3), P(f'M{x - 54},84 Q{x},18 {x + 54},84Z', 'lampc'), E(x, 84, 54, 8, 'lamp'), E(x, 110, 120, 40, 'lamp', .4, 'filter="url(#b20)"')]
    s.layer('lamps', lp, 'drop', .9, loop='glow')
    # 地面
    fl = [R(0, 810, W, 270, s.lg([(0, 'floor1'), (1, 'floor2')]))] + floor_lines(810, 1080, 'floor2', step=220, op=.6, rows=(870, 960))
    s.layer('floor', fl, 'rise', .1)

    # 餐桌（两侧）
    def table(cx, flip):
        it = [shadow(cx, 1010, 250, 18), R(cx - 220, 880, 440, 26, 'tabletop', 10, extra='filter="url(#shs)"'), R(cx - 200, 904, 400, 12, 'table', 4),
              R(cx - 190, 914, 16, 96, 'steel3', 4), R(cx + 174, 914, 16, 96, 'steel3', 4)]
        for dx in (-130, 130):
            it += [R(cx + dx - 46, 950, 92, 22, 'stool', 11), R(cx + dx - 6, 970, 12, 44, 'steel3', 4), E(cx + dx, 1014, 34, 6, 'steel3')]
        tx = cx - 120 if flip else cx - 20
        it += [R(tx, 852, 150, 30, 'tray', 8), C(tx + 36, 862, 18, 'rice'), E(tx + 84, 864, 22, 10, 'green'), E(tx + 122, 864, 16, 9, 'egg'),
               R(tx + 170 if flip else tx - 70, 846, 44, 36, 'bowl', 10), E(tx + 192 if flip else tx - 48, 848, 20, 5, 'soup'),
               C(cx + (150 if not flip else -170), 860, 18, 'tomato'), C(cx + (150 if not flip else -170), 862, 6, 'tomato')]
        return G(it)
    s.layer('tables', [table(270, False), table(1650, True)], 'rise', .85)
    fb = [E(1560, 586, 70, 14, 'steel2'), P('M1490,560 Q1560,620 1630,560Z', 'bowl')]
    for dx, dy, col in [(-34, 552, 'tomato'), (0, 546, 'egg'), (34, 552, 'green2'), (-16, 532, 'carrot'), (18, 532, 'tomato')]:
        fb += [C(1560 + dx, dy, 18, col), C(1554 + dx, dy - 6, 5, '#ffffff', .5)]
    s.layer('fruit', fb, 'pop', 1.0)
    return s


# ============ s004 校门口 ============
def schoolgate():
    s = Scene('s004', '校门口', '校园', ['安全教育', '入学', '道德与法治', '校园生活'],
              dict(sky1='#8FD3F5', sky2='#E8F7FF', bld='#FBE3C7', bld2='#F2CDA4', roof='#E07A5F', win='#BFE3F5', win2='#FFFFFF', pillar='#F4EFE6', pillar2='#DCD3C4',
                   gold='#F2C14E', red='#E5533D', wallc='#E7DDD0', rail='#5B6F82', gate='#C9D2DB', gate2='#97A6B4', booth='#FFFFFF', boothr='#4FA3C7', walk='#E9DDCB', walk2='#D9C9B2',
                   road='#596273', stripe='#F5F5F0', grass='#8CCB6E', grass2='#6DB35A', tree='#5FAE74', tree2='#9ED38C', trunk='#8A5A3A', flower1='#FF8FA3', flower2='#FFD15C', sign='#2F7FC9'),
              desc='晴天校门口：门柱横梁与校徽、半开的伸缩门、保安亭、花坛与行道树，身后是教学楼。', stand={'ground_y': 900, 'x': [600, 1320]})
    s.layer('sky', [R(0, 0, W, 760, s.lg([(0, 'sky1'), (1, 'sky2')])), C(1640, 150, 60, '#FFF3C0'), C(1640, 150, 130, '#FFF3C0', .35, 'filter="url(#b40)"')], 'fade', 0)
    s.layer('clouds', [cloud(300, 160, .8, op=.95), cloud(1100, 110, .55, op=.85), cloud(1500, 250, .45, op=.8)], 'slide-l', .2, loop='drift')
    # 教学楼
    bl = [R(420, 330, 1080, 380, s.lg([(0, 'bld'), (1, 'bld2')]), 6, extra='filter="url(#shs)"'), R(400, 316, 1120, 24, 'roof', 6), R(860, 250, 200, 90, 'bld', 6), poly([(840, 256), (1080, 256), (960, 196)], 'roof'),
          C(960, 296, 30, 'win2'), S('M960,296 L960,276 M960,296 L974,304', 'rail', 4)]
    for r_ in range(4):
        for k in range(12):
            x = 456 + k * 86
            if 870 < x < 1010 and r_ == 3: continue
            bl += [R(x, 364 + r_ * 84, 56, 52, 'win', 4), R(x, 364 + r_ * 84, 56, 12, 'win2', 3, .8)]
    bl += [R(890, 610, 140, 100, 'win', 4), R(956, 610, 8, 100, 'win2')]
    bl += [S('M1440,316 L1440,200', 'rail', 4), P('M1442,200 L1510,212 L1442,236Z', 'red')]
    s.layer('building', bl, 'rise', .25)
    s.layer('trees_back', [blob_tree(x, 720, .8, 'tree', 'tree2', 'trunk') for x in (120, 300, 1620, 1800)], 'grow', .4, loop='sway')
    # 围墙栏杆
    fw = [R(0, 690, W, 80, 'wallc')]
    for x in range(0, W, 26): fw.append(R(x, 560, 7, 132, 'rail', 3))
    fw += [R(0, 580, W, 8, 'rail'), R(0, 650, W, 8, 'rail')]
    for x in range(0, W, 150): fw.append(R(x, 540, 40, 230, 'pillar2', 4))
    s.layer('fence', [G(fw, 'clip-path="' + s.clip('<path d="M0,0 H600 V1080 H0Z M1320,0 H1920 V1080 H1320Z"/>') + '"')], 'rise', .35)
    # 地面
    gd = [R(0, 770, W, 310, s.lg([(0, 'walk'), (1, 'walk2')]))]
    gd += floor_lines(770, 1080, 'walk2', step=160, op=.5, rows=(830, 920, 1020))
    gd.append(P('M640,770 L1280,770 L1500,1080 L420,1080Z', 'pillar', .45))
    s.layer('ground', gd, 'rise', .1)
    # 门柱与横梁
    gp = [R(500, 400, 130, 380, s.lg([(0, 'pillar'), (1, 'pillar2')]), 8, extra='filter="url(#sh)"'), R(1290, 400, 130, 380, s.lg([(0, 'pillar'), (1, 'pillar2')]), 8, extra='filter="url(#sh)"'),
          R(486, 386, 158, 28, 'pillar2', 6), R(1276, 386, 158, 28, 'pillar2', 6), R(480, 300, 960, 100, 'red', 14, extra='filter="url(#sh)"'), R(492, 312, 936, 76, 'red', 10),
          R(492, 312, 936, 10, '#ffffff', 4, .18), C(960, 350, 52, 'gold'), C(960, 350, 42, 'red'), star(960, 350, 24, 'gold'),
          R(620, 342, 220, 16, 'gold', 8, .7), R(1080, 342, 220, 16, 'gold', 8, .7), R(500, 760, 130, 20, 'pillar2'), R(1290, 760, 130, 20, 'pillar2')]
    s.layer('gate_posts', gp, 'rise', .45)
    # 伸缩门（半开）
    sg = [R(630, 676, 220, 14, 'gate2', 6)]
    for k in range(10):
        x = 640 + k * 21
        sg.append(S(f'M{x},690 L{x + 21},760 M{x + 21},690 L{x},760', 'gate', 5))
    sg += [R(630, 756, 230, 10, 'gate2', 4), R(842, 666, 28, 110, 'gate2', 6), C(850, 784, 9, 'rail'), R(842, 690, 28, 20, 'red', 4)]
    s.layer('sliding_gate', sg, 'slide-l', .7)
    # 保安亭
    bx = 1500
    bo = [shadow(bx + 120, 800, 150, 14), R(bx, 520, 240, 270, 'booth', 14, extra='filter="url(#sh)"'), R(bx - 16, 500, 272, 36, 'boothr', 12),
          R(bx + 24, 570, 190, 110, 'win', 6), R(bx + 116, 570, 6, 110, 'booth'), R(bx + 24, 700, 190, 12, 'boothr', 4, .6), R(bx + 70, 470, 100, 32, 'boothr', 8), C(bx + 120, 486, 8, 'flower2')]
    s.layer('guard_booth', bo, 'pop', .8)

    # 花坛
    def bed(x, w):
        it = [R(x, 770, w, 50, 'pillar2', 10, extra='filter="url(#shs)"'), E(x + w / 2, 770, w / 2 - 6, 30, 'grass2')]
        for k in range(int(w // 34)):
            fx = x + 20 + k * 34; it += [C(fx, 754 - (k % 2) * 10, 10, 'flower1' if k % 2 else 'flower2'), C(fx, 754 - (k % 2) * 10, 4, '#ffffff')]
        return G(it)
    s.layer('flower_beds', [bed(140, 300), bed(1520, 280)], 'grow', .95, loop='sway')
    # 近景行道树与路标
    s.layer('trees_front', [blob_tree(70, 1000, 1.25, 'tree', 'tree2', 'trunk'), blob_tree(1870, 1000, 1.2, 'tree', 'tree2', 'trunk')], 'grow', 1.05, loop='sway')
    sn = [R(1736, 640, 10, 360, 'rail', 4), poly([(1741, 560), (1801, 664), (1681, 664)], '#ffffff'), poly([(1741, 576), (1789, 656), (1693, 656)], 'flower2'),
          C(1726, 610, 7, 'rail'), P('M1720,620 L1732,620 L1736,648 L1716,648Z', 'rail'), C(1756, 616, 6, 'rail'), P('M1750,624 L1762,624 L1766,648 L1746,648Z', 'rail')]
    s.layer('sign', sn, 'pop', 1.15)
    return s


# ============ s005 升旗广场 ============
def flagsquare():
    s = Scene('s005', '升旗广场', '校园', ['德育', '爱国主义', '班会', '升旗仪式'],
              dict(sky1='#7EC8F2', sky2='#EAF7FF', bld='#FFF3E4', bld2='#F3DDC3', band='#F08A6C', win='#B9DDF2', win2='#FFFFFF', red='#E83A2F', red2='#C92D24', star='#FFDE00',
                   pole='#D9DEE3', pole2='#AEB6BF', plat='#E9E1D6', plat2='#D4C8B8', plaza='#F1E9DC', plaza2='#E2D5C2', grass='#8CCB6E', tree='#62B07A', tree2='#A2D88E', trunk='#8A5A3A',
                   bush='#5FA873', flower='#FF8F7A', flower2='#FFD15C', dove='#FFFFFF'),
              desc='晴空下的升旗广场：三级旗台上的旗杆与飘扬的五星红旗，身后教学楼，广场方砖与花坛。', stand={'ground_y': 910, 'x': [380, 1150]})
    s.layer('sky', [R(0, 0, W, 760, s.lg([(0, 'sky1'), (1, 'sky2')]))], 'fade', 0)
    s.layer('clouds', [cloud(260, 180, .75, op=.95), cloud(820, 110, .5, op=.85), cloud(1220, 230, .4, op=.8)], 'slide-l', .2, loop='drift')
    # 教学楼（长楼，横向彩带）
    bl = [R(0, 380, W, 340, s.lg([(0, 'bld'), (1, 'bld2')]))]
    for r_ in range(3):
        y = 410 + r_ * 96
        bl.append(R(0, y + 74, W, 12, 'band', 0, .55))
        for x in range(30, W, 110): bl += [R(x, y, 76, 58, 'win', 4), R(x, y, 76, 12, 'win2', 3, .8), R(x + 36, y, 4, 58, 'win2', 0, .7)]
    bl += [R(0, 366, W, 20, 'band'), R(780, 300, 360, 90, 'bld', 6), R(770, 290, 380, 16, 'band', 6), C(960, 346, 30, 'win2'), C(960, 346, 22, 'red')]
    s.layer('building', bl, 'rise', .25)
    s.layer('trees', [blob_tree(x, 740, .75 + .1 * (k % 2), 'tree', 'tree2', 'trunk') for k, x in enumerate((90, 330, 570, 1790))], 'grow', .4, loop='sway')
    s.layer('hedge', [R(0, 700, W, 60, 'bush', 30)] + [C(x, 706, 34, 'bush') for x in range(0, W + 40, 60)] + [C(x + 20, 694, 8, 'flower' if (x // 60) % 2 else 'flower2') for x in range(0, W, 90)], 'rise', .35)
    # 广场
    pz = [R(0, 760, W, 320, s.lg([(0, 'plaza'), (1, 'plaza2')]))] + floor_lines(760, 1080, 'plaza2', vx=1450, vy=420, step=150, op=.7, rows=(800, 860, 940, 1040), rowop=.5)
    pz.append(E(1450, 930, 520, 70, 'plaza2', .35))
    s.layer('plaza', pz, 'rise', .1)
    # 旗台（三级台阶）
    px = 1450
    pl = [shadow(px, 900, 330, 20, .16)]
    for k, (w, y) in enumerate([(640, 852), (520, 812), (400, 772)]):
        pl += [R(px - w / 2, y, w, 46, 'plat2', 6), R(px - w / 2, y, w, 14, 'plat', 6)]
    pl += [R(px - 200, 758, 400, 16, 'red2', 6, .85)]
    s.layer('platform', pl, 'rise', .45)
    # 旗杆
    pole = [R(px - 9, 140, 18, 634, s.lg([(0, 'pole'), (.5, '#ffffff'), (1, 'pole2')], 0, 0, 1, 0), 9), C(px, 132, 16, 'star'), R(px - 30, 760, 60, 16, 'pole2', 6)]
    s.layer('pole', pole, 'grow', .6, origin=f'{px} 774')
    # 国旗：3:2，五星位置按标准（30x20 网格）
    fx, fy, u = px + 9, 152, 10.8   # 旗宽 324，高 216
    fw_, fh_ = 30 * u, 20 * u
    flag = [P(f'M{fx},{fy} Q{fx + fw_ * .3},{fy - 16} {fx + fw_ * .55},{fy + 4} T{fx + fw_},{fy + 2} L{fx + fw_},{fy + fh_ + 2} Q{fx + fw_ * .78},{fy + fh_ + 16} {fx + fw_ * .55},{fy + fh_ + 4} T{fx},{fy + fh_}Z', 'red', extra='filter="url(#shs)"'),
            P(f'M{fx + fw_ * .42},{fy - 2} Q{fx + fw_ * .55},{fy + fh_ * .5} {fx + fw_ * .5},{fy + fh_ + 6} L{fx + fw_ * .62},{fy + fh_ + 6} Q{fx + fw_ * .66},{fy + fh_ * .5} {fx + fw_ * .56},{fy}Z', 'red2', .35)]
    bx_, by_ = fx + 5 * u, fy + 5 * u
    flag.append(star(bx_, by_, 3 * u, 'star'))
    for gx, gy in [(10, 2), (12, 4), (12, 7), (10, 9)]:
        cx, cy = fx + gx * u, fy + gy * u
        ang = math.degrees(math.atan2(by_ - cy, bx_ - cx))
        flag.append(star(cx, cy, u, 'star', rot=ang))
    flag += [R(fx - 6, fy - 4, 8, 10, 'pole2', 2), R(fx - 6, fy + fh_ - 6, 8, 10, 'pole2', 2), S(f'M{px - 5},{fy} L{px - 5},770', 'pole2', 2, .8)]
    s.layer('flag', flag, 'fade', .85, loop='sway', origin=f'{fx} {fy + fh_ / 2}')
    # 花盆（旗台两侧）与鸽子
    pots = []
    for x in (1170, 1730):
        pots += [shadow(x, 900, 60, 8), R(x - 46, 830, 92, 70, 'plat2', 10), C(x, 812, 46, 'bush'), *[C(x + dx, 796 + dy, 10, 'flower' if (dx // 10) % 2 else 'flower2') for dx, dy in [(-24, 6), (0, -14), (22, 4), (-8, 18), (14, 20)]]]
    s.layer('pots', pots, 'pop', 1.0)
    dv = []
    for x, y, sc in [(560, 260, 1), (660, 220, .8), (500, 200, .7)]:
        dv += [E(x, y, 22 * sc, 11 * sc, 'dove'), P(f'M{x - 6 * sc},{y - 4 * sc} Q{x - 20 * sc},{y - 34 * sc} {x - 40 * sc},{y - 30 * sc} Q{x - 20 * sc},{y - 10 * sc} {x + 4 * sc},{y}Z', 'dove'),
               C(x + 20 * sc, y - 6 * sc, 7 * sc, 'dove'), poly([(x + 26 * sc, y - 7 * sc), (x + 34 * sc, y - 4 * sc), (x + 26 * sc, y - 2 * sc)], 'flower2')]
    s.layer('doves', dv, 'slide-l', 1.15, loop='bob')
    return s


# ============ s006 医务室 ============
def clinic():
    s = Scene('s006', '医务室', '校园', ['健康', '卫生', '视力保护', '急救'],
              dict(wall1='#F2FAF9', wall2='#DDF0EE', dado='#A9DCD6', dado2='#8CCBC4', floor1='#E3EEF0', floor2='#C9DADF', white='#FFFFFF', line='#D6E2E6', ink='#2F3A44',
                   cross='#EF5B5B', curtain='#9CD8D2', curtain2='#7CC4BD', rail='#9AA8B3', bed='#E9F3FF', bed2='#C7DCF0', metal='#8C9BA7', glass='#D9F1FA', bottle1='#7FC4E8',
                   bottle2='#F7C55E', bottle3='#9ADBA3', bottle4='#F2A49A', sky1='#A8DDF5', sky2='#EAF8FF', leaf='#5FAE74', leaf2='#9ED38C', wood='#E7C9A4', ruler='#F7D774'),
              desc='干净的校医务室：视力表、身高体重秤、带百叶的窗、药品柜、急救箱与拉帘病床。', stand={'ground_y': 900, 'x': [600, 1300]})
    s.layer('wall', [R(0, 0, W, 800, s.lg([(0, 'wall1'), (1, 'wall2')])), R(0, 620, W, 180, s.lg([(0, 'dado'), (1, 'dado2')])), R(0, 614, W, 10, 'white', 0, .8)], 'fade', 0)
    fl = [R(0, 800, W, 280, s.lg([(0, 'floor1'), (1, 'floor2')]))] + floor_lines(800, 1080, 'floor2', step=200, op=.7, rows=(860, 950))
    s.layer('floor', fl, 'rise', .1)
    # 视力表（E 字，逐行变小，四个方向）
    ex, ey = 110, 120
    ec = [R(ex, ey, 230, 470, 'white', 10, extra='filter="url(#sh)"'), R(ex, ey, 230, 30, 'cross', 10), R(ex, ey + 20, 230, 10, 'cross')]

    def E_opt(cx, cy, sz, d):
        u = sz / 5
        d_ = f'M0,0 h{5 * u} v{u} h{-4 * u} v{u} h{4 * u} v{u} h{-4 * u} v{u} h{4 * u} v{u} h{-5 * u}Z'
        rot = {'r': 0, 'l': 180, 'u': -90, 'd': 90}[d]
        return P(d_, 'ink', extra=f'transform="translate({cx},{cy}) rotate({rot}) translate({-2.5 * u},{-2.5 * u})"')
    random.seed(6)
    rows = [(1, 64), (2, 44), (3, 30), (4, 22), (5, 16), (6, 12), (7, 9), (8, 7)]
    y = ey + 80
    for n, sz in rows:
        for k in range(n):
            cx = ex + 115 + (k - (n - 1) / 2) * (sz * 1.9)
            ec.append(E_opt(cx, y, sz, random.choice('rlud')))
        y += sz * 1.15 + 22
    s.layer('eye_chart', ec, 'drop', .3)
    # 身高体重秤
    hx = 450
    hs = [shadow(hx, 892, 80, 10), R(hx - 70, 850, 140, 40, 'white', 10, extra='filter="url(#shs)"'), R(hx - 56, 862, 112, 16, 'line', 6), R(hx - 14, 260, 28, 600, 'white', 8, extra='filter="url(#shs)"'),
          R(hx - 6, 280, 16, 570, 'ruler', 3)]
    for k in range(29):
        hs.append(R(hx - 6, 290 + k * 19.5, 9 if k % 5 else 16, 2, 'ink', 1, .7))
    hs += [R(hx - 70, 420, 110, 14, 'metal', 6), R(hx - 20, 410, 34, 34, 'metal', 6), C(hx + 60, 820, 26, 'white'), C(hx + 60, 820, 20, 'glass'), S(f'M{hx + 60},820 L{hx + 72},808', 'cross', 3)]
    s.layer('height_scale', hs, 'rise', .5)
    # 窗（百叶）
    blinds = [R(700 + 0, 150 + k * 22, 520, 12, 'white', 3, .85) for k in range(7)]
    s.layer('window', [sky_window(s, 700, 150, 520, 330, 'sky1', 'sky2', 'white', [cloud(820, 300, .5), C(1000, 520, 140, 'leaf2'), C(1160, 500, 110, 'leaf2', .8)] + blinds, mull='v'),
                       R(686, 486, 548, 18, 'white', 6), leafy(800, 486, .55, 'cross', 'leaf', 'leaf2', 6), leafy(1120, 486, .5, 'curtain2', 'leaf', 'leaf2', 6)], 'pop', .25)
    # 急救箱（墙挂）
    fa = [R(890, 540, 140, 100, 'white', 12, extra='filter="url(#shs)"'), R(890, 540, 140, 18, 'cross', 10), R(948, 568, 24, 60, 'cross', 4), R(930, 586, 60, 24, 'cross', 4), R(948, 530, 24, 12, 'metal', 4)]
    s.layer('first_aid', fa, 'pop', .7)
    # 药品柜
    cx0 = 1260
    cb = [shadow(cx0 + 130, 802, 150, 12), R(cx0, 220, 260, 580, 'white', 12, extra='filter="url(#sh)"'), R(cx0 + 16, 236, 228, 330, 'glass', 6, .7), R(cx0 + 128, 236, 4, 330, 'white')]
    for k, y in enumerate((340, 450, 560)): cb.append(R(cx0 + 16, y, 228, 8, 'line'))
    random.seed(12)
    for k, y in enumerate((340, 450, 560)):
        x = cx0 + 26
        while x < cx0 + 230:
            w = random.choice([22, 28, 34]); h = random.randint(44, 76); col = random.choice(['bottle1', 'bottle2', 'bottle3', 'bottle4', 'white'])
            if x + w > cx0 + 240: break
            cb += [R(x, y - h, w, h, col, 6), R(x + 3, y - h - 8, w - 6, 10, 'metal', 3), R(x + 3, y - h * .6, w - 6, h * .25, 'white', 2, .7)]
            x += w + 8
    cb += [R(cx0 + 16, 590, 228, 190, 'line', 6, .5), R(cx0 + 128, 590, 4, 190, 'white'), R(cx0 + 108, 670, 8, 30, 'metal', 4), R(cx0 + 144, 670, 8, 30, 'metal', 4),
           P(f'M{cx0 + 40},566 L{cx0 + 90},236 L{cx0 + 110},236 L{cx0 + 60},566Z', 'white', .4)]
    s.layer('cabinet', cb, 'slide-r', .55)
    ct = [R(1560, 76, 360, 10, 'rail', 5)] + [C(1580 + k * 50, 82, 7, 'rail') for k in range(6)]
    for k in range(4):
        x = 1836 + k * 20
        ct.append(P(f'M{x},86 L{x + 30},86 Q{x + 36},500 {x + 26},780 L{x - 4},780 Q{x + 4},500 {x},86Z', 'curtain' if k % 2 else 'curtain2'))
    s.layer('curtain', ct, 'slide-r', .85, loop='sway', origin='1880 86')
    # 病床 + 拉帘
    bx = 1550
    bd = [shadow(bx + 150, 880, 190, 14), R(bx, 700, 320, 40, 'bed2', 12), R(bx, 676, 320, 34, 'bed', 14, extra='filter="url(#shs)"'), R(bx + 10, 650, 100, 34, 'white', 16), R(bx + 150, 672, 170, 40, 'curtain', 12, .55), R(bx + 150, 672, 170, 10, 'white', 5, .6),
          R(bx + 20, 740, 12, 130, 'metal', 4), R(bx + 290, 740, 12, 130, 'metal', 4), R(bx - 6, 600, 14, 270, 'metal', 6), C(bx + 26, 872, 10, 'ink'), C(bx + 296, 872, 10, 'ink')]
    s.layer('bed', bd, 'rise', .75)
    # 洗手池 + 听诊器
    sk = [R(160, 700, 220, 30, 'white', 10, extra='filter="url(#shs)"'), P('M180,730 L360,730 L340,800 L200,800Z', 'white'), R(260, 640, 12, 60, 'metal', 4), R(260, 640, 56, 12, 'metal', 6),
          R(176, 600, 36, 80, 'bottle3', 8), R(186, 586, 16, 16, 'metal', 4)]
    s.layer('sink', sk, 'pop', .9)
    s.layer('sunlight', [beam(760, 900, 640, 900, 480, 1080, s, .22), beam(1000, 1140, 1000, 1240, 480, 1080, s, .18)], 'fade', 1.0, loop='glow')
    return s


# ============ s007 图书馆 ============
def library():
    s = Scene('s007', '图书馆', '校园', ['语文', '阅读', '英语', '通用课堂'],
              dict(wall1='#F5EBDA', wall2='#E9D8BE', wood='#B98458', wood2='#8D5E3A', wood3='#6E472B', sky1='#A6D9F2', sky2='#F3FBFF', frame='#FFFFFF',
                   b1='#E8806B', b2='#5FA8B5', b3='#F2C55C', b4='#8C7BC4', b5='#7DBB86', b6='#F2A7B8', b7='#4E6E9E', rug='#86AE91', rug2='#A9C9AE', floor1='#D7A877', floor2='#BE8C5D',
                   table='#C8925E', lamp='#3F8C6E', lampg='#FFE6A3', leaf='#5FAE74', leaf2='#9ED38C', pot='#F3EEE6', globe='#7CC4E8', globe2='#9BD07E', gold='#D8A94B'),
              desc='安静的图书馆：中央高大拱窗洒下光束，两侧顶天书架与梯子，绿罩台灯阅读桌、地球仪与地毯。', stand={'ground_y': 910, 'x': [600, 1320]})
    s.layer('wall', [R(0, 0, W, 800, s.lg([(0, 'wall1'), (1, 'wall2')])), *[R(x, 0, 3, 800, 'wall2', 0, .8) for x in range(700, 1240, 60)]], 'fade', 0)
    # 拱窗
    ax, ay, aw, ah = 720, 110, 480, 560
    arch = f'M{ax},{ay + ah} L{ax},{ay + aw / 2} A{aw / 2},{aw / 2} 0 0,1 {ax + aw},{ay + aw / 2} L{ax + aw},{ay + ah}Z'
    cp = s.clip(f'<path d="{arch}"/>')
    win = [P(f'M{ax - 22},{ay + ah + 10} L{ax - 22},{ay + aw / 2} A{aw / 2 + 22},{aw / 2 + 22} 0 0,1 {ax + aw + 22},{ay + aw / 2} L{ax + aw + 22},{ay + ah + 10}Z', 'wood', extra='filter="url(#sh)"'),
           P(arch, s.lg([(0, 'sky1'), (1, 'sky2')])),
           G([cloud(860, 300, .55), cloud(1100, 420, .4, op=.9), C(820, 700, 130, 'leaf2'), C(1100, 720, 160, 'leaf2', .85), C(960, 690, 90, 'leaf', .5)], f'clip-path="{cp}"'),
           G([R(ax + aw / 2 - 5, ay, 10, ah, 'frame'), R(ax, ay + 300, aw, 10, 'frame'), R(ax, ay + 450, aw, 10, 'frame'), S(f'M{ax + aw / 2},{ay + aw / 2} L{ax + 40},{ay + 140} M{ax + aw / 2},{ay + aw / 2} L{ax + aw - 40},{ay + 140}', 'frame', 8, 1)], f'clip-path="{cp}"'),
           S(f'M{ax},{ay + aw / 2} A{aw / 2},{aw / 2} 0 0,1 {ax + aw},{ay + aw / 2}', 'frame', 10),
           R(ax - 40, ay + ah, aw + 80, 26, 'wood2', 8)]
    s.layer('window', win, 'pop', .25)
    s.layer('beams', [beam(800, 980, 700, 1040, 300, 1080, s, .3), beam(1000, 1150, 1000, 1300, 300, 1080, s, .22)], 'fade', 1.0, loop='glow')
    # 地面与地毯
    fl = [R(0, 800, W, 280, s.lg([(0, 'floor1'), (1, 'floor2')]))]
    for k, y in enumerate((800, 850, 910, 980, 1060)):
        fl.append(R(0, y, W, 3, 'wood2', 0, .45))
        for x in range(-100 + (k % 2) * 120, W, 240): fl.append(R(x, y, 3, ([850, 910, 980, 1060, 1080][k] - y), 'wood2', 0, .35))
    s.layer('floor', fl, 'rise', .1)
    s.layer('rug', [E(960, 960, 560, 82, 'rug'), E(960, 960, 500, 64, 'rug2', .6), E(960, 960, 430, 50, 'rug')], 'grow', .5)

    # 书架
    def shelf(x0, w, seed):
        it = [R(x0, 80, w, 720, s.lg([(0, 'wood'), (1, 'wood2')]), 10, extra='filter="url(#sh)"'), R(x0 - 14, 66, w + 28, 26, 'wood3', 8)]
        random.seed(seed)
        for k in range(5):
            y0 = 110 + k * 136
            it.append(R(x0 + 16, y0, w - 32, 116, 'wood3', 4, .55))
            x = x0 + 22
            while x < x0 + w - 40:
                bw = random.randint(16, 30); bh = random.randint(78, 108); col = random.choice(['b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7'])
                if random.random() < .08 and x < x0 + w - 80:
                    it.append(R(x + 6, y0 + 116 - bh + 6, bw, bh - 6, col, 3, extra=f'transform="rotate(14 {x} {y0 + 116})"'))
                    x += bw + 24; continue
                it += [R(x, y0 + 116 - bh, bw, bh, col, 3), R(x + 3, y0 + 116 - bh + 14, bw - 6, 5, 'gold', 2, .55), R(x + 3, y0 + 116 - 22, bw - 6, 4, 'gold', 2, .45)]
                x += bw + 2
            it.append(R(x0 + 10, y0 + 116, w - 20, 12, 'wood', 3))
        return G(it)
    s.layer('shelf_left', [shelf(40, 560, 3)], 'slide-l', .35)
    s.layer('shelf_right', [shelf(1320, 560, 8)], 'slide-r', .4)
    # 梯子
    ld = [S('M1460,40 L1500,900', 'wood3', 14), S('M1580,40 L1620,900', 'wood3', 14)]
    for k in range(10):
        t = (k + .5) / 10; ld.append(S(f'M{1460 + 40 * t:.0f},{40 + 860 * t:.0f} L{1580 + 40 * t:.0f},{40 + 860 * t:.0f}', 'wood3', 10))
    ld += [R(1420, 30, 240, 10, 'gold', 5), C(1500, 904, 10, 'gold'), C(1620, 904, 10, 'gold')]
    s.layer('ladder', ld, 'drop', .6)

    # 阅读桌 + 台灯 + 书
    def rtable(cx):
        return G([shadow(cx, 1000, 210, 14), R(cx - 200, 860, 400, 24, 'table', 10, extra='filter="url(#shs)"'), R(cx - 180, 882, 16, 116, 'wood3', 4), R(cx + 164, 882, 16, 116, 'wood3', 4),
                  R(cx - 150, 884, 300, 30, 'wood2', 4, .6),
                  R(cx + 70, 852, 70, 10, 'gold', 4), R(cx + 102, 770, 6, 84, 'gold', 3), P(f'M{cx + 60},780 Q{cx + 105},746 {cx + 150},780Z', 'lamp'), E(cx + 105, 780, 45, 7, 'lampg'),
                  R(cx - 130, 838, 120, 22, 'b2', 4), R(cx - 124, 818, 108, 22, 'b1', 4), P(f'M{cx - 20},858 L{cx + 50},852 L{cx + 50},860 L{cx - 20},864Z', 'frame')])
    s.layer('tables', [rtable(330), rtable(1600)], 'rise', .7)
    s.layer('lamp_glow', [E(435, 820, 90, 50, 'lampg', .5, 'filter="url(#b20)"'), E(1705, 820, 90, 50, 'lampg', .5, 'filter="url(#b20)"')], 'fade', 1.1, loop='glow')
    # 地球仪
    gx = 640
    gb = [shadow(gx, 902, 50, 8), R(gx - 40, 888, 80, 14, 'wood3', 6), R(gx - 5, 830, 10, 60, 'wood3'), C(gx, 770, 56, 'globe'),
          P(f'M{gx - 40},{740} q20,-14 36,4 q8,22 -12,30 q-18,0 -24,-34Z', 'globe2'), P(f'M{gx + 6},{780} q28,-10 34,10 q-6,26 -22,26 q-16,-14 -12,-36Z', 'globe2'),
          S(f'M{gx - 64},{770} A64,64 0 0,1 {gx + 30},{712}', 'gold', 6), C(gx - 20, 750, 12, '#ffffff', .35)]
    s.layer('globe', gb, 'pop', .9)
    s.layer('plant', [leafy(1250, 910, 1.1, 'pot', 'leaf', 'leaf2', 9)], 'grow', 1.0, loop='sway', origin='1250 910')
    random.seed(30)
    s.layer('dust', [C(random.uniform(780, 1250), random.uniform(350, 850), random.uniform(2, 4), '#ffffff', .8) for _ in range(20)], 'fade', 1.2, loop='twinkle')
    return s


# ============ s008 计算机房 ============
def computerlab():
    s = Scene('s008', '计算机房', '校园', ['信息科技', '编程', '数学', '科学'],
              dict(wall1='#EEF1FB', wall2='#DCE3F5', dado='#B9C6EA', floor1='#C9D2E6', floor2='#AEB9D3', screen='#FFFFFF', case='#3B4256', case2='#2C3243', desk='#F7F8FC', desk2='#DCE1EE',
                   mon='#2E3448', mon2='#4A5370', scr1='#5EA8F5', scr2='#8E7CF0', key='#FFFFFF', key2='#C7CEDD', kb='#E4E8F2', chair='#5B8DEF', chair2='#4672CF',
                   blk1='#8E6CF0', blk2='#FFAB3D', blk3='#59C0E8', blk4='#5CCB7A', blk5='#F06C9B', light='#FFFFFF', leaf='#5FAE74', leaf2='#9ED38C', pot='#FFFFFF', cable='#6A7390'),
              desc='整洁的计算机房：前方投影幕布展示积木编程，两侧电脑桌上显示器、精确键盘与鼠标，蓝色转椅。', stand={'ground_y': 910, 'x': [600, 1320]})
    s.layer('wall', [R(0, 0, W, 800, s.lg([(0, 'wall1'), (1, 'wall2')])), R(0, 660, W, 140, 'dado', 0, .45), R(0, 656, W, 8, 'dado')], 'fade', 0)
    s.layer('ceiling', [G([R(x - 140, 0, 280, 22, 'light', 6), E(x, 30, 260, 40, 'light', .6, 'filter="url(#b20)"')]) for x in (360, 960, 1560)], 'fade', .1, loop='glow')
    fl = [R(0, 800, W, 280, s.lg([(0, 'floor1'), (1, 'floor2')]))]
    for y in range(800, 1080, 70):
        for x in range(-((y // 70) % 2) * 70, W, 140): fl.append(R(x, y, 140, 70, 'floor2', 0, .18))
    s.layer('floor', fl, 'rise', .1)
    # 投影幕
    sx, sy, sw, sh = 600, 120, 720, 430
    sc = [R(sx - 30, 92, sw + 60, 30, 'case', 15, extra='filter="url(#shs)"'), R(sx, 120, sw, sh, 'screen', 4, extra='filter="url(#sh)"'), R(sx, sh + 120 - 10, sw, 14, 'case2', 4),
          R(sx + 20, 140, sw - 40, sh - 50, s.lg([(0, '#F5F7FF'), (1, '#E9EDFB')]), 6), R(sx + 20, 140, 160, sh - 50, 'desk2', 6, .7)]
    for k, col in enumerate(['blk1', 'blk2', 'blk3', 'blk4', 'blk5', 'blk1']):
        sc.append(C(sx + 50, 176 + k * 52, 12, col)); sc.append(R(sx + 72, 168 + k * 52, 90, 16, col, 8, .55))

    def block(x, y, w, col, hat=False):
        d = (f'M{x},{y} ' + (f'Q{x + 40},{y - 26} {x + 80},{y} ' if hat else f'L{x + 18},{y} L{x + 24},{y + 7} L{x + 42},{y + 7} L{x + 48},{y} ')
             + f'L{x + w},{y} L{x + w},{y + 40} L{x + 48},{y + 40} L{x + 42},{y + 47} L{x + 24},{y + 47} L{x + 18},{y + 40} L{x},{y + 40}Z')
        return G([P(d, col), R(x + 14, y + 15, w * .45, 10, '#ffffff', 5, .55), C(x + w * .7, y + 20, 8, '#ffffff', .7)])
    bx, by = sx + 230, 190
    sc += [block(bx, by, 220, 'blk2', True), block(bx, by + 40, 260, 'blk3'), block(bx, by + 80, 200, 'blk1')]
    sc += [P(f'M{bx},{by + 120} L{bx + 240},{by + 120} L{bx + 240},{by + 160} L{bx + 40},{by + 160} L{bx + 40},{by + 210} L{bx + 240},{by + 210} L{bx + 240},{by + 236} L{bx},{by + 236}Z', 'blk2'),
           block(bx + 40, by + 160, 190, 'blk4'), R(bx + 14, by + 134, 100, 10, '#ffffff', 5, .55)]
    # 舞台上的星星角色
    sc += [R(sx + 520, 170, 170, 130, 'desk', 8), star(sx + 605, 240, 40, 'blk2'), C(sx + 592, 232, 5, 'case'), C(sx + 618, 232, 5, 'case')]
    s.layer('screen', sc, 'drop', .3)
    s.layer('sparkle', [star(sx + 660, 186, 9, 'blk3'), star(sx + 548, 278, 7, 'blk5'), star(sx + 680, 280, 6, 'blk4')], 'pop', 1.2, loop='twinkle')

    # 电脑桌一组
    def station(x0, n, gap):
        it = [shadow(x0 + n * gap / 2, 912, n * gap / 2 + 40, 12), R(x0 - 20, 640, n * gap + 40, 26, 'desk', 8, extra='filter="url(#shs)"'), R(x0 - 10, 664, n * gap + 20, 160, 'desk2', 6)]
        for k in range(n + 1): it.append(R(x0 - 10 + k * gap, 664, 14, 240, 'desk2', 4))
        for k in range(n):
            cx = x0 + gap / 2 + k * gap
            # 显示器 16:9
            mw, mh = 200, 116
            it += [R(cx - 12, 584, 24, 58, 'mon2', 4), R(cx - 44, 630, 88, 12, 'mon2', 5), R(cx - mw / 2 - 8, 460, mw + 16, mh + 16, 'mon', 10, extra='filter="url(#shs)"'),
                   R(cx - mw / 2, 468, mw, mh, s.lg([(0, ['scr1', 'scr2', 'blk4'][k % 3]), (1, 'scr2' if k % 3 == 0 else 'scr1')]), 4)]
            # 屏幕内容：积木
            it += [R(cx - 84, 480, 56, 12, 'blk2', 6), R(cx - 84, 496, 70, 12, 'blk3', 6), R(cx - 74, 512, 60, 12, 'blk1', 6), R(cx + 6, 484, 76, 60, '#ffffff', 6, .85), star(cx + 44, 514, 16, 'blk2'),
                   P(f'M{cx - mw / 2 + 20},{468} L{cx - mw / 2 + 60},{468} L{cx - mw / 2 + 20},{468 + mh}Z', '#ffffff', .12)]
            # 键盘（按键网格）与鼠标
            kx, ky, kw = cx - 90, 618, 150
            it.append(R(kx, ky, kw, 20, 'kb', 4))
            for r_ in range(3):
                for c_ in range(12):
                    it.append(R(kx + 4 + c_ * 12, ky + 2 + r_ * 5.6, 10, 4, 'key2', 1))
            it += [R(kx + 40, ky + 16, 70, 3.5, 'key2', 1), E(cx + 92, 628, 10, 7, 'key'), R(cx + 91, 621, 2, 6, 'key2')]
            # 椅背（面向桌子）
            it += [R(cx - 60, 700, 120, 120, 'chair', 30, extra='filter="url(#shs)"'), R(cx - 48, 712, 96, 96, 'chair2', 24, .5), R(cx - 8, 820, 16, 60, 'case', 4),
                   S(f'M{cx - 56},{896} L{cx + 56},{896}', 'case', 10), C(cx - 56, 900, 9, 'case'), C(cx + 56, 900, 9, 'case'), C(cx, 902, 9, 'case')]
        return G(it)
    s.layer('desks_left', [station(40, 2, 250)], 'rise', .55)
    s.layer('desks_right', [station(1380, 2, 250)], 'rise', .65)
    s.layer('screen_glow', [E(x, 526, 130, 80, 'scr1', .25, 'filter="url(#b20)"') for x in (165, 415, 1505, 1755)], 'fade', 1.0, loop='glow')
    # 主机箱、绿植、挂钟
    s.layer('extras', [leafy(560, 905, .9, 'pot', 'leaf', 'leaf2', 7), leafy(1360, 905, .9, 'pot', 'leaf', 'leaf2', 7),
                       C(1520, 200, 54, 'screen', extra='filter="url(#shs)"'), S('M1466,200 a54,54 0 1,0 108,0 a54,54 0 1,0 -108,0', 'case', 8),
                       *[R(1517, 154, 6, 12, 'case', 2, extra=f'transform="rotate({k * 30} 1520 200)"') for k in range(12)], S('M1520,200 L1520,166', 'case', 6), S('M1520,200 L1546,212', 'blk5', 5), C(1520, 200, 6, 'case'),
                       R(300, 150, 200, 280, 'desk', 10, extra='filter="url(#shs)"'), *[R(322, 176 + k * 44, 156, 30, ['blk1', 'blk2', 'blk3', 'blk4', 'blk5', 'blk1'][k], 15, .8) for k in range(5)], C(340, 191, 0.1, 'case')],
            'pop', .85)
    return s


# ============ s009 校车站 ============
def busstop():
    s = Scene('s009', '校车站', '校园', ['交通安全', '安全教育', '上学放学', '生活'],
              dict(sky1='#9FD8F3', sky2='#FFF0D9', hill='#C4E4B4', hill2='#A9D69A', house1='#F7C9A8', house2='#BFD8EE', house3='#F6E0A6', roof1='#E07A5F', roof2='#5FA8B5',
                   road='#5A6170', road2='#4C5361', stripe='#F5F5F0', curb='#CFC6B8', walk='#EDE3D3', walk2='#DDCFBA', bus='#F8C535', bus2='#E4A91C', trim='#2E3440', win='#BFE6F7', win2='#E8F7FF',
                   lightc='#FF6A4D', tire='#2A2E36', hub='#C9CED6', shelter='#5FB7B0', shelter2='#4A9C95', glass='#DDF4F2', bench='#F28B6E', pole='#6A7684', signb='#2F7FC9',
                   tree='#62B07A', tree2='#A2D88E', trunk='#8A5A3A', sun='#FFE08A'),
              desc='清晨校车站：黄色校车停靠路边，候车亭与站牌、长椅，远处小山与房屋，人行道上留出候车空间。', stand={'ground_y': 930, 'x': [480, 1280]})
    s.layer('sky', [R(0, 0, W, 700, s.lg([(0, 'sky1'), (1, 'sky2')])), C(380, 220, 70, 'sun'), C(380, 220, 150, 'sun', .3, 'filter="url(#b40)"')], 'fade', 0)
    s.layer('clouds', [cloud(700, 140, .7, op=.9), cloud(1400, 180, .8, op=.85), cloud(1800, 110, .45, op=.8)], 'slide-l', .2, loop='drift')
    s.layer('hills', [P('M0,560 Q300,430 640,520 Q980,600 1300,480 Q1620,380 1920,500 L1920,640 L0,640Z', 'hill'), P('M0,600 Q400,520 800,580 Q1200,640 1600,560 Q1800,520 1920,560 L1920,660 L0,660Z', 'hill2')], 'rise', .25)

    def house(x, w, h, body, roof):
        return G([R(x, 640 - h, w, h, body, 4), poly([(x - 14, 640 - h), (x + w + 14, 640 - h), (x + w / 2, 640 - h - w * .4)], roof), R(x + w * .2, 640 - h + 20, w * .22, w * .2, 'win2', 3), R(x + w * .58, 640 - h + 20, w * .22, w * .2, 'win2', 3)])
    s.layer('houses', [house(560, 120, 90, 'house1', 'roof1'), house(720, 100, 70, 'house2', 'roof2'), house(1080, 130, 100, 'house3', 'roof1'), house(1260, 96, 74, 'house1', 'roof2'), house(1620, 120, 86, 'house2', 'roof1')], 'rise', .3)
    s.layer('trees', [blob_tree(x, 650, .7 + .12 * (k % 2), 'tree', 'tree2', 'trunk') for k, x in enumerate((60, 260, 900, 1480, 1860))], 'grow', .4, loop='sway')
    # 道路与人行道
    rd = [R(0, 640, W, 150, s.lg([(0, 'road2'), (1, 'road')]))] + [R(x, 708, 90, 8, 'stripe', 3, .9) for x in range(20, W, 180)]
    rd += [R(0, 784, W, 22, 'curb'), R(0, 800, W, 280, s.lg([(0, 'walk'), (1, 'walk2')]))] + floor_lines(806, 1080, 'walk2', step=170, op=.6, rows=(870, 960, 1050))
    s.layer('road', rd, 'rise', .1)
    # 校车（侧面，车头朝右，靠近我方一侧为车门侧）
    bx0, bx1, top, bot = 120, 1010, 430, 750
    bus = [shadow((bx0 + bx1) / 2, 784, 470, 14, .2),
           P(f'M{bx0},{bot - 20} L{bx0},{top + 30} Q{bx0},{top} {bx0 + 30},{top} L{bx1 - 150},{top} Q{bx1 - 110},{top} {bx1 - 100},{top + 40} L{bx1 - 90},{top + 120} L{bx1 - 20},{top + 140} Q{bx1},{top + 146} {bx1},{top + 170} L{bx1},{bot - 20} Q{bx1},{bot} {bx1 - 20},{bot} L{bx0 + 20},{bot} Q{bx0},{bot} {bx0},{bot - 20}Z',
             s.lg([(0, 'bus'), (1, 'bus2')]), extra='filter="url(#sh)"'),
           R(bx0, top + 190, bx1 - bx0, 16, 'trim'), R(bx0, top + 236, bx1 - bx0, 8, 'trim', 0, .8), R(bx0, bot - 44, bx1 - bx0, 22, 'trim', 4)]
    for k in range(6):
        x = bx0 + 30 + k * 100
        bus += [R(x, top + 40, 84, 110, 'win', 8), R(x, top + 40, 84, 26, 'win2', 6, .8), R(x, top + 96, 84, 6, 'trim', 0, .5)]
    # 车门（前门在右侧前轮后）
    dx = bx1 - 250
    bus += [R(dx, top + 40, 110, 240, 'trim', 10), R(dx + 8, top + 48, 44, 224, 'win', 6), R(dx + 58, top + 48, 44, 224, 'win', 6), R(dx + 53, top + 48, 4, 224, 'trim')]
    # 驾驶窗/挡风
    bus += [P(f'M{bx1 - 120},{top + 40} L{bx1 - 104},{top + 40} L{bx1 - 94},{top + 120} L{bx1 - 120},{top + 120}Z', 'win'),
            R(bx1 - 22, top + 200, 24, 30, 'sun', 6), R(bx1 - 12, bot - 70, 16, 30, 'lightc', 4), R(bx0 - 4, bot - 70, 14, 34, 'lightc', 4), R(bx0 + 4, top + 200, 12, 30, 'lightc', 4),
            R(bx1 - 60, bot - 30, 66, 20, 'trim', 6), R(bx0 - 8, bot - 30, 50, 20, 'trim', 6)]
    # 停车标志伸出臂（收起）
    bus += [R(bx0 + 640, top + 262, 70, 10, 'trim', 4, .5), R(bx0 + 20, top + 262, 200, 10, 'trim', 4, .35)]
    for wx in (bx0 + 200, bx1 - 70):
        bus += [C(wx, bot, 64, 'trim'), C(wx, bot, 50, 'tire'), C(wx, bot, 26, 'hub'), C(wx, bot, 8, 'trim')]
    s.layer('bus', bus, 'slide-l', .5, loop='bob')
    # 候车亭
    sx0 = 1320
    sh = [shadow(sx0 + 250, 926, 280, 14), R(sx0, 470, 16, 450, 'shelter2', 6), R(sx0 + 484, 470, 16, 450, 'shelter2', 6), R(sx0 - 30, 450, 560, 36, 'shelter', 12, extra='filter="url(#shs)"'),
          R(sx0 - 30, 478, 560, 10, 'shelter2', 4), R(sx0 + 16, 500, 468, 330, 'glass', 6, .55), R(sx0 + 260, 520, 200, 280, 'house3', 8), R(sx0 + 276, 540, 168, 160, 'sky1', 4),
          C(sx0 + 330, 590, 26, 'sun'), P(f'M{sx0 + 276},700 L{sx0 + 340},630 L{sx0 + 390},670 L{sx0 + 444},610 L{sx0 + 444},700Z', 'tree'), R(sx0 + 276, 720, 168, 14, 'pole', 6, .5), R(sx0 + 276, 744, 120, 12, 'pole', 6, .35),
          R(sx0 + 40, 820, 400, 22, 'bench', 10), R(sx0 + 40, 780, 400, 18, 'bench', 9, .85), R(sx0 + 70, 842, 14, 76, 'pole', 4), R(sx0 + 396, 842, 14, 76, 'pole', 4),
          P(f'M{sx0 + 30},500 L{sx0 + 90},500 L{sx0 + 30},830Z', '#ffffff', .25)]
    s.layer('shelter', sh, 'rise', .7)
    # 站牌
    sn = [R(1236, 520, 14, 410, 'pole', 6), C(1243, 520, 56, '#ffffff', extra='filter="url(#shs)"'), C(1243, 520, 48, 'signb'),
          R(1213, 494, 60, 44, '#ffffff', 8), R(1219, 500, 48, 18, 'signb', 3), C(1225, 542, 7, '#ffffff'), C(1261, 542, 7, '#ffffff'), R(1205, 600, 76, 120, '#ffffff', 8, extra='filter="url(#shs)"'),
          *[R(1215, 616 + k * 20, 56, 8, 'pole', 4, .4) for k in range(5)]]
    s.layer('stop_sign', sn, 'drop', .9)
    s.layer('bushes', [C(x, 800, r_, 'tree') for x, r_ in ((1850, 46), (1900, 38))] + [C(1868, 784, 22, 'tree2', .6)], 'grow', 1.0, loop='sway')
    return s


# ============ s010 礼堂 ============
def auditorium():
    s = Scene('s010', '礼堂', '校园', ['班会', '演讲', '文艺表演', '开学典礼'],
              dict(back1='#FBE3D2', back2='#F5CDB6', fold='#EDB89E', curtain='#D9485F', curtain2='#B5334C', gold='#F3C969', gold2='#D9A441', arch='#FFF6EC', arch2='#F1DDC6',
                   stage1='#D49A64', stage2='#B67A47', apron='#8E5A35', hall='#6E5A8E', hall2='#57476F', seat='#E1546A', seat2='#B93E54', spot='#FFF4CF', podium='#8E5A35', podium2='#B67A47',
                   flower1='#FF8FA3', flower2='#FFD15C', flower3='#FFFFFF', leaf='#5FAE74', mic='#2E3440', star='#FFE38A'),
              desc='学校礼堂舞台：拱形台口、红丝绒大幕与金色流苏、聚光灯光柱、讲台与鲜花，台下前排座椅。', stand={'ground_y': 830, 'x': [560, 1360]})
    s.layer('hall', [R(0, 0, W, H, s.lg([(0, 'hall'), (1, 'hall2')]))], 'fade', 0)
    # 舞台后幕
    bk = [R(180, 100, 1560, 680, s.lg([(0, 'back1'), (1, 'back2')]))]
    for x in range(200, 1740, 70): bk.append(R(x, 100, 26, 680, 'fold', 0, .35))
    bk.append(E(960, 420, 420, 260, '#ffffff', .35, 'filter="url(#b40)"'))
    # 背景板装饰：星星与彩带
    for x, y, r_ in [(700, 260, 26), (1220, 240, 32), (960, 200, 40), (820, 360, 16), (1110, 350, 18)]:
        bk.append(star(x, y, r_, 'star'))
    bk += [S('M560,470 Q960,560 1360,470', 'gold', 10, .8), S('M600,500 Q960,590 1320,500', 'curtain', 6, .5)]
    s.layer('backdrop', bk, 'fade', .15)
    s.layer('stars_twinkle', [star(x, y, 9, '#ffffff', op=.9) for x, y in [(640, 330), (1290, 320), (1020, 280), (900, 250)]], 'pop', 1.2, loop='twinkle')
    # 舞台地板
    st = [R(150, 760, 1620, 80, s.lg([(0, 'stage1'), (1, 'stage2')]))]
    for x in range(150, 1770, 90): st.append(R(x, 760, 2, 80, 'stage2', 0, .5))
    st += [R(130, 836, 1660, 24, 'gold2', 6), R(130, 856, 1660, 70, 'apron', 4)]
    for x in range(180, 1760, 160): st.append(R(x, 870, 120, 40, 'stage2', 8, .5))
    s.layer('stage', st, 'rise', .1)
    # 侧幕（收拢）
    def side(x0, sd):
        it = []
        for k in range(7):
            x = x0 + sd * k * 34
            w = 44
            it.append(P(f'M{x - w / 2},90 L{x + w / 2},90 Q{x + w / 2 - sd * 30},420 {x + w / 2 + sd * 70},600 Q{x + sd * 60},760 {x + w / 2 + sd * 40},840 L{x - w / 2 + sd * 40},840 Q{x - w / 2 + sd * 50},700 {x - w / 2 + sd * 50},600 Q{x - w / 2 - sd * 20},420 {x - w / 2},90Z',
                        'curtain' if k % 2 else 'curtain2'))
        tx = x0 + sd * 150
        it += [S(f'M{x0 - sd * 20},590 Q{tx},630 {x0 + sd * 260},584', 'gold', 10), E(tx, 606, 18, 14, 'gold'), S(f'M{tx},612 L{tx},680', 'gold', 8), P(f'M{tx - 16},676 L{tx + 16},676 L{tx + 22},720 L{tx - 22},720Z', 'gold2')]
        return G(it)
    s.layer('side_curtains', [side(200, 1), side(1720, -1)], 'slide-l', .3)
    # 上方帷幔（扇形垂幔）
    vl = [R(150, 70, 1620, 60, 'curtain2')]
    for k in range(9):
        x0 = 150 + k * 180
        vl += [P(f'M{x0},120 Q{x0 + 90},250 {x0 + 180},120Z', 'curtain'), P(f'M{x0 + 20},120 Q{x0 + 90},210 {x0 + 160},120Z', 'curtain2', .35), C(x0, 128, 14, 'gold')]
    vl += [C(1770, 128, 14, 'gold'), R(150, 124, 1620, 8, 'gold')]
    s.layer('valance', vl, 'drop', .45, loop='sway', origin='960 70')
    # 台口拱框
    fr = P('M0,0 H1920 V1080 H1790 V200 Q1790,40 1600,40 H320 Q130,40 130,200 V1080 H0Z', s.lg([(0, 'arch'), (1, 'arch2')]))
    s.layer('proscenium', [fr, S('M130,1080 V200 Q130,40 320,40 H1600 Q1790,40 1790,200 V1080', 'gold', 12), S('M100,1080 V190 Q100,10 310,10 H1610 Q1820,10 1820,190 V1080', 'gold2', 4, .7),
                           C(960, 26, 22, 'gold'), C(960, 26, 12, 'curtain')], 'zoom', .05)
    # 聚光灯
    s.layer('spotlights', [beam(560, 640, 680, 1020, 0, 860, s, .3), beam(1280, 1360, 900, 1240, 0, 860, s, .3), E(960, 820, 360, 40, 'spot', .55, 'filter="url(#b20)"')], 'fade', .9, loop='glow')
    # 讲台 + 话筒 + 花
    px = 1380
    pd = [shadow(px, 840, 110, 10), P(f'M{px - 90},640 L{px + 90},640 L{px + 76},836 L{px - 76},836Z', s.lg([(0, 'podium2'), (1, 'podium')]), extra='filter="url(#sh)"'), R(px - 104, 624, 208, 24, 'podium', 8),
          C(px, 720, 34, 'gold'), C(px, 720, 26, 'curtain'), star(px, 720, 14, 'gold'), S(f'M{px - 30},624 Q{px - 40},570 {px - 10},540', 'mic', 5), E(px - 6, 536, 10, 14, 'mic')]
    for k, (dx, dy, col) in enumerate([(70, 590, 'flower1'), (90, 570, 'flower2'), (52, 566, 'flower3'), (80, 548, 'flower1'), (104, 596, 'flower3')]):
        pd += [C(px + dx, dy, 14, col), C(px + dx, dy, 5, 'flower2' if col != 'flower2' else 'flower3')]
    pd += [E(px + 66, 604, 30, 10, 'leaf')]
    s.layer('podium', pd, 'rise', .7)
    # 台口花盆
    pt = []
    for x in (300, 540, 1560, 1700):
        pt += [R(x - 40, 800, 80, 40, 'gold2', 8), C(x, 790, 34, 'leaf')] + [C(x + dx, 776 + dy, 9, 'flower1' if (dx + 40) % 3 else 'flower2') for dx, dy in [(-18, 8), (0, -8), (18, 6), (6, 14)]]
    s.layer('flowers', pt, 'pop', .85)
    # 前排座椅（仅两侧，避开字幕区）
    se = []
    for x0, x1 in ((0, 520), (1400, 1920)):
        for k in range(4):
            x = x0 + 20 + k * 128
            if x + 110 > x1: continue
            se += [R(x, 930, 112, 150, 'seat2', 28, extra='filter="url(#sh)"'), R(x + 10, 940, 92, 110, 'seat', 22)]
    s.layer('seats', se, 'rise', .95)
    return s


SCENES = [corridor, canteen, schoolgate, flagsquare, clinic, library, computerlab, busstop, auditorium]
