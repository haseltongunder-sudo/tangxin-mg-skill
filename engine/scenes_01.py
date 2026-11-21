from core import *
import math, random


# ============ 01 教室 ============
def classroom():
    s = Scene('s001', '阳光教室', '校园', ['语文', '数学', '班会', '通用课堂'],
              dict(wall1='#FBEBD2', wall2='#F2D7B3', wains='#D49A6A', wains2='#BF8355', floor1='#E2B07A', floor2='#C98F57',
                   board='#2F6656', board2='#285848', frame='#9B6A42', sky1='#8FD3F5', sky2='#DDF3FF', leaf='#7CC48E', leaf2='#B9E3A6',
                   desk='#F0C27F', desk2='#D9A25E', metal='#5E6B7A', accent='#F2836B', paper='#FFFDF6'),
              desc='正面视角教室：黑板居中，左右两扇窗透进斜光，中央走道留给角色。', stand={'ground_y': 900, 'x': [640, 1280]})
    s.layer('wall', [R(0, 0, W, 760, s.lg([(0, 'wall1'), (1, 'wall2')])),
                     R(0, 640, W, 120, 'wains'), R(0, 640, W, 14, 'wains2'), R(0, 748, W, 12, 'wains2')], 'fade', 0)
    # 窗
    win = []
    for x0 in (90, 1490):
        win += [R(x0 - 16, 130, 372, 452, '#ffffff', 18, extra='filter="url(#shs)"'),
                R(x0, 146, 340, 420, s.lg([(0, 'sky1'), (1, 'sky2')]), 8)]
        cp = s.clip(f'<rect x="{x0}" y="146" width="340" height="420" rx="8"/>')
        win.append(G([cloud(x0 + 110, 250, .55), cloud(x0 + 260, 330, .38, op=.85),
                      C(x0 + 70, 560, 130, 'leaf'), C(x0 + 250, 590, 150, 'leaf'), C(x0 + 150, 520, 70, 'leaf2', .6)], f'clip-path="{cp}"'))
        win += [R(x0 + 166, 146, 8, 420, '#ffffff'), R(x0, 352, 340, 8, '#ffffff'), R(x0 - 26, 578, 392, 18, '#ffffff', 6)]
    s.layer('windows', win, 'pop', .25)
    # 黑板
    bd = [R(548, 138, 824, 432, 'frame', 16, extra='filter="url(#sh)"'), R(566, 156, 788, 396, s.lg([(0, 'board'), (1, 'board2')]), 8),
          R(536, 556, 848, 22, 'frame', 8),
          R(600, 548, 54, 10, '#ffffff', 4), R(672, 548, 38, 10, 'accent', 4), R(1240, 546, 70, 14, '#C9CED6', 5)]
    # 粉笔涂鸦：太阳、几何、波浪
    bd += [S('M640,250 a40,40 0 1,0 80,0 a40,40 0 1,0 -80,0', '#ffffff', 5, .85),
           *[S(f'M{680 + 58 * math.cos(a):.0f},{250 + 58 * math.sin(a):.0f} L{680 + 76 * math.cos(a):.0f},{250 + 76 * math.sin(a):.0f}', '#ffffff', 5, .85) for a in [k * math.pi / 4 for k in range(8)]],
           S('M1150,220 L1260,220 L1205,320 Z', '#FFE08A', 5, .9), S('M1110,420 q40,-40 80,0 t80,0 t80,0', '#9FE3FF', 5, .85),
           S('M840,470 L1080,470', '#ffffff', 4, .35), S('M800,420 L1020,420', '#ffffff', 4, .35)]
    s.layer('board', bd, 'drop', .45)
    # 钟
    clk = [C(960, 74, 44, '#ffffff', extra='filter="url(#shs)"'), S('M916,74 a44,44 0 1,0 88,0 a44,44 0 1,0 -88,0', 'frame', 7),
           *[C(960 + 34 * math.cos(k * math.pi / 6), 74 + 34 * math.sin(k * math.pi / 6), 3, 'metal') for k in range(12)],
           S('M960,74 L960,48', 'metal', 5), S('M960,74 L980,84', 'accent', 4), C(960, 74, 5, 'metal')]
    s.layer('clock', clk, 'pop', .6, origin='960 74')
    gl = [S('M0,20 Q240,70 480,24', 'frame', 3, .6), S('M1440,24 Q1680,70 1920,20', 'frame', 3, .6)]
    cols_ = ['accent', 'leaf', '#F7C55E', '#7FC4E8']
    for k in range(9):
        for x0, x1 in ((0, 480), (1440, 1920)):
            u = (k + .5) / 9; x = x0 + (x1 - x0) * u; y = 22 + 44 * 4 * u * (1 - u)
            gl.append(poly([(x - 20, y), (x + 20, y), (x, y + 38)], cols_[k % 4]))
    s.layer('garland', gl, 'drop', .75, loop='sway')
    # 地板（透视地板条）
    fl = [R(0, 760, W, 320, s.lg([(0, 'floor1'), (1, 'floor2')]))]
    vx, vy = 960, 380
    for k in range(-12, 13):
        xb = 960 + k * 190
        x_top = vx + (xb - vx) * (760 - vy) / (1080 - vy)
        fl.append(S(f'M{x_top:.0f},760 L{xb},1080', 'floor2', 3, .5))
    for yy in (800, 860, 950):
        fl.append(S(f'M0,{yy} L{W},{yy}', 'floor2', 2, .35))
    s.layer('floor', fl, 'rise', .1)
    # 光束与光斑
    s.layer('light', [beam(250, 430, 520, 900, 300, 1080, s, .28), beam(1530, 1700, 1180, 1540, 300, 1080, s, .22),
                      E(720, 960, 210, 40, '#FFF6D8', .45, 'filter="url(#b20)"'), E(1360, 980, 190, 36, '#FFF6D8', .4, 'filter="url(#b20)"')], 'fade', .9, loop='glow')

    # 课桌（两侧，留中间走道）
    def desk(x, y, sc):
        w, h = 300 * sc, 26 * sc
        return G([E(x, y + 160 * sc, 170 * sc, 18 * sc, '#000000', .10),
                  R(x - w / 2 + 14 * sc, y + h, 10 * sc, 150 * sc, 'metal', 3), R(x + w / 2 - 24 * sc, y + h, 10 * sc, 150 * sc, 'metal', 3),
                  R(x - w / 2 + 10 * sc, y + h, w - 20 * sc, 60 * sc, 'desk2', 6 * sc),
                  R(x - w / 2, y, w, h, 'desk', 8 * sc, extra='filter="url(#shs)"'),
                  R(x - 60 * sc, y - 8 * sc, 90 * sc, 10 * sc, 'paper', 3, extra=f'transform="rotate(-6 {x} {y})"'),
                  R(x + 50 * sc, y - 9 * sc, 50 * sc, 9 * sc, 'accent', 3)])
    s.layer('desks_back', [desk(380, 700, .62), desk(1540, 700, .62)], 'rise', .7)
    s.layer('desks_front', [desk(250, 840, .95), desk(1670, 840, .95)], 'rise', .85)
    # 绿植
    plant = [R(1820, 650, 70, 100, 'accent', 10), *[E(1855 + 40 * math.cos(a), 620 + 30 * math.sin(a), 46, 18, 'leaf', extra=f'transform="rotate({math.degrees(a):.0f} {1855 + 40 * math.cos(a):.0f} {620 + 30 * math.sin(a):.0f})"') for a in [-2.6, -1.9, -1.2, -.5, -3.2]]]
    s.layer('plant', plant, 'grow', 1.0, loop='sway', origin='1855 750')
    return s


# ============ 02 田径跑道 ============
def track():
    s = Scene('s011', '晨光田径场', '体育', ['体育', '跑步', '运动会', '健康'],
              dict(sky1='#7DC8F0', sky2='#FFE9C7', sun='#FFD36E', city='#B9CBE0', city2='#A2B6D2', stand='#E9EEF5', seat1='#F28B6E', seat2='#5BB7D6', seat3='#F7C55E',
                   grass1='#8CCB6E', grass2='#7BBE5E', track='#D8674B', track2='#C65A40', line='#FFFFFF', tree='#5FAE74', tree2='#9AD48B', trunk='#8A5A3A', hurdle='#F4F4F4'),
              desc='侧视田径直道，六条分道由近到远，背景看台与晨光城市，适合跑、跳、接力动画。', stand={'ground_y': 930, 'x': [200, 1720]})
    s.layer('sky', [R(0, 0, W, 700, s.lg([(0, 'sky1'), (1, 'sky2')])), C(1480, 300, 160, 'sun', .25, 'filter="url(#b40)"'), C(1480, 300, 78, 'sun')], 'fade', 0)
    s.layer('clouds', [cloud(380, 170, .9, op=.9), cloud(980, 120, .6, op=.8), cloud(1700, 200, .7, op=.85)], 'slide-l', .2, loop='drift')
    random.seed(3)
    city = []
    x = 0
    while x < W:
        w = random.randint(70, 150); h = random.randint(120, 300)
        city.append(R(x, 560 - h, w, h + 10, 'city' if random.random() < .5 else 'city2', 6))
        for wy in range(int(560 - h + 24), 540, 36):
            for wx in range(x + 14, x + w - 20, 30):
                if random.random() < .5: city.append(R(wx, wy, 14, 18, '#ffffff', 2, .45))
        x += w + random.randint(4, 20)
    s.layer('city', city, 'rise', .3)
    # 看台
    st = [P('M0,560 L1920,560 L1920,660 L0,660Z', 'stand')]
    for r_ in range(4):
        y = 576 + r_ * 20
        for k in range(0, W, 26):
            st.append(R(k + (r_ % 2) * 13, y, 18, 12, ['seat1', 'seat2', 'seat3'][(k // 26 + r_) % 3], 3))
    st += [R(0, 556, W, 8, '#ffffff')]
    s.layer('stands', st, 'rise', .45)
    s.layer('trees', [blob_tree(x, 690, .7 + .15 * (k % 2), 'tree', 'tree2', 'trunk') for k, x in enumerate(range(60, 1920, 210))], 'grow', .6, loop='sway')
    # 草地内场
    gr = [R(0, 660, W, 80, 'grass1')] + [R(k, 660, 120, 80, 'grass2', 0, .6) for k in range(0, W, 240)]
    s.layer('grass', gr, 'fade', .5)
    # 跑道：6 道，近大远小
    tr = [R(0, 740, W, 340, s.lg([(0, 'track2'), (1, 'track')]))]
    ys = [740]
    for k in range(6): ys.append(ys[-1] + 34 + k * 9)
    for y in ys: tr.append(R(0, y - 2, W, 4 + (y - 740) / 90, 'line'))
    for k in range(6):
        y0, y1 = ys[k], ys[k + 1]
        tr.append(T(150, (y0 + y1) / 2 + (y1 - y0) * .25, str(k + 1), int((y1 - y0) * .62), 'line', 900))
    # 起跑线与终点格
    tr.append(P(f'M210,{ys[0]} L220,{ys[0]} L232,{ys[-1]} L222,{ys[-1]}Z', 'line'))
    for k in range(6):
        y0, y1 = ys[k], ys[k + 1]; n = 2
        for j in range(n):
            for q in range(2):
                yy = y0 + (y1 - y0) * j / n; hh = (y1 - y0) / n
                tr.append(R(1720 + q * 18 + (j % 2) * 18 * (1 - 2 * q) * 0, yy, 18, hh, '#222222' if (j + q) % 2 == 0 else '#ffffff'))
    tr.append(R(0, ys[-1], W, 1080 - ys[-1], 'grass2'))
    s.layer('track', tr, 'rise', .15)

    def hurdle(x, y, sc):
        return G([R(x - 4 * sc, y - 90 * sc, 8 * sc, 90 * sc, '#C9CED6'), R(x + 76 * sc, y - 90 * sc, 8 * sc, 90 * sc, '#C9CED6'),
                  R(x - 10 * sc, y - 96 * sc, 100 * sc, 20 * sc, 'hurdle', 4, extra='filter="url(#shs)"'), R(x + 10 * sc, y - 96 * sc, 20 * sc, 20 * sc, 'seat1'), R(x + 50 * sc, y - 96 * sc, 20 * sc, 20 * sc, 'seat1'),
                  R(x - 14 * sc, y - 4 * sc, 28 * sc, 6 * sc, '#9AA3AE', 2), R(x + 66 * sc, y - 4 * sc, 28 * sc, 6 * sc, '#9AA3AE', 2)])
    s.layer('hurdles', [hurdle(1080, ys[3] - 4, .8), hurdle(1380, ys[5] - 4, 1.0)], 'pop', .9)
    bt = []
    for seg in range(4):
        x0 = seg * 480; bt.append(S(f'M{x0},546 Q{x0 + 240},590 {x0 + 480},546', '#ffffff', 3))
        for k in range(8):
            u = (k + .5) / 8; x = x0 + 480 * u; y = 547 + 44 * 4 * u * (1 - u) * .5 * 2 * .5
            bt.append(poly([(x - 16, y), (x + 16, y), (x, y + 30)], ['seat1', 'seat3', 'seat2'][k % 3]))
    s.layer('bunting', bt, 'drop', 1.0, loop='sway')
    return s


# ============ 03 古诗山水 ============
def shanshui():
    s = Scene('s021', '古诗山水', '语文与历史', ['语文', '古诗', '美术', '传统文化'],
              dict(paper1='#F6EEDC', paper2='#EADCC0', ink1='#2F3B3F', ink2='#566A6B', ink3='#8EA19B', ink4='#C3CFC3', mist='#FFFFFF', seal='#C8392F', moon='#F1C9A0', water='#A9BDB6', pine='#2F4A3F', pine2='#4E6F5C', wood='#6B4A35', roof='#3B3434'),
              desc='宣纸底色的层叠水墨远山，云雾、江面、小舟与凉亭，适合古诗意境与传统文化。', stand={'ground_y': 980, 'x': [700, 1400]})
    s.layer('paper', [R(0, 0, W, H, s.lg([(0, 'paper1'), (1, 'paper2')]))], 'fade', 0)
    s.layer('sun', [C(1460, 250, 96, 'moon', .9), C(1460, 250, 170, 'moon', .25, 'filter="url(#b40)"')], 'fade', .2, loop='glow')

    def ridge(y, amp, seed, col, step=60):
        random.seed(seed)
        pts = []; x = -40
        ph = random.random() * 6
        while x <= W + 80:
            yy = y - amp * (0.55 + 0.45 * math.sin(x / 260 + ph)) * (0.6 + 0.4 * math.sin(x / 97 + ph * 2)) - random.random() * amp * .15
            pts.append((x, yy)); x += step
        d = f'M-40,{H} ' + ' '.join(f'L{x:.0f},{y_:.0f}' for x, y_ in pts) + f' L{W + 80},{H}Z'
        g = s.lg([(0, col), (.55, col, .85), (1, 'paper1', 0)])
        return P(d, g)
    s.layer('far', [ridge(560, 320, 1, 'ink4')], 'rise', .3)
    s.layer('mist1', [E(500, 560, 700, 60, 'mist', .7, 'filter="url(#b40)"'), E(1500, 600, 600, 50, 'mist', .6, 'filter="url(#b40)"')], 'fade', .5, loop='drift')
    s.layer('mid', [ridge(700, 360, 7, 'ink3', 50)], 'rise', .45)
    # 凉亭（中景山头）
    pav = [R(1300, 470, 8, 70, 'wood'), R(1360, 470, 8, 70, 'wood'), P('M1276,476 Q1334,440 1392,476 L1384,486 Q1334,458 1284,486Z', 'roof'),
           P('M1300,452 Q1334,420 1368,452Z', 'roof'), C(1334, 418, 5, 'roof'), R(1290, 536, 88, 8, 'wood')]
    s.layer('pavilion', pav, 'pop', .8)
    s.layer('mist2', [E(900, 760, 800, 70, 'mist', .75, 'filter="url(#b40)"')], 'fade', .6, loop='drift')
    s.layer('near', [ridge(880, 300, 13, 'ink2', 40)], 'rise', .6)
    # 江面
    wv = [R(0, 900, W, 180, s.lg([(0, 'water', .0), (.3, 'water', .55), (1, 'water', .8)]))]
    for k in range(9):
        y = 930 + k * 16; x0 = (k * 173) % 900
        wv.append(S(f'M{x0},{y} q30,-8 60,0 t60,0', 'ink3', 3, .5)); wv.append(S(f'M{x0 + 900},{y + 6} q30,-8 60,0 t60,0', 'ink3', 3, .45))
    s.layer('water', wv, 'fade', .7, loop='flow')
    boat = [P('M1100,966 Q1180,996 1290,966 L1270,980 Q1180,1002 1118,980Z', 'ink1'), S('M1190,966 L1190,900', 'wood', 4), P('M1150,960 Q1190,920 1236,960Z', 'ink2'),
            S('M1100,986 q90,14 190,0', 'ink3', 3, .5)]
    s.layer('boat', boat, 'slide-r', 1.0, loop='bob')
    # 近景松
    pn = [S('M80,1080 C110,900 60,820 150,700 C180,660 230,640 260,600', 'wood', 30),
          S('M150,700 C220,700 300,690 380,650', 'wood', 16), S('M200,640 C150,600 110,580 60,590', 'wood', 12)]
    for x, y, r_ in [(260, 590, 70), (380, 640, 64), (60, 580, 56), (320, 560, 50), (180, 610, 48), (440, 620, 40)]:
        pn += [E(x, y, r_ * 1.4, r_ * .45, 'pine'), E(x + 10, y - 10, r_ * 1.0, r_ * .28, 'pine2', .8)]
    s.layer('pine', pn, 'grow', .9, loop='sway', origin='80 1080')
    birds = [S(f'M{x},{y} q14,-12 26,0 q12,-12 26,0', 'ink1', 3) for x, y in [(700, 220), (760, 250), (820, 205), (650, 260)]]
    s.layer('birds', birds, 'slide-l', 1.1, loop='drift')
    s.layer('seal', [R(1790, 900, 70, 70, 'seal', 6), T(1825, 948, '诗', 44, '#FBEDE0', 700)], 'pop', 1.3)
    return s


# ============ 04 钟表店 ============
def clockshop():
    s = Scene('s032', '钟表店', '数学', ['数学', '认识钟表', '时间', '生活'],
              dict(wall1='#2D5B63', wall2='#244A51', pat='#3B6D74', wood='#B57A4A', wood2='#8E5A34', glass='#CFEFF5', face='#FFF9EC', rim='#E3B054', rim2='#C98E3A',
                   hand='#30363C', red='#E2584A', lamp='#FFD98A', counter='#6E4426', teal='#5FB7B0', pink='#F2A49A'),
              desc='墨绿墙面挂满各式钟表（刻度与数字位置准确），落地摆钟会摆动，暖色吊灯，适合认识时间。', stand={'ground_y': 920, 'x': [560, 1360]})
    bg = [R(0, 0, W, H, s.lg([(0, 'wall1'), (1, 'wall2')]))]
    for y in range(40, 760, 80):
        for x in range(40 + (y // 80 % 2) * 40, W, 80):
            bg.append(P(f'M{x},{y - 12} L{x + 10},{y} L{x},{y + 12} L{x - 10},{y}Z', 'pat', .7))
    s.layer('wall', bg, 'fade', 0)

    def clock(cx, cy, r, hh, mm, shape='round', nums=True, col='rim'):
        it = []
        if shape == 'round':
            it += [C(cx, cy, r + r * .14, col, extra='filter="url(#sh)"'), C(cx, cy, r, 'face')]
        elif shape == 'square':
            it += [R(cx - r * 1.14, cy - r * 1.14, r * 2.28, r * 2.28, col, r * .25, extra='filter="url(#sh)"'), R(cx - r, cy - r, 2 * r, 2 * r, 'face', r * .18)]
        else:  # house
            it += [P(f'M{cx - r * 1.2},{cy - r * .6} L{cx},{cy - r * 1.7} L{cx + r * 1.2},{cy - r * .6}Z', 'wood2', extra='filter="url(#sh)"'),
                   R(cx - r * 1.1, cy - r * .7, r * 2.2, r * 2.0, 'wood', r * .12, extra='filter="url(#sh)"'), C(cx, cy + r * .1, r * .82, 'face')]
            cy = cy + r * .1; r = r * .82
        for k in range(60):
            a = k * math.pi / 30 - math.pi / 2
            big = k % 5 == 0
            if not big and r < 60: continue
            r0 = r * (.86 if big else .92); r1 = r * .97
            it.append(S(f'M{cx + r0 * math.cos(a):.1f},{cy + r0 * math.sin(a):.1f} L{cx + r1 * math.cos(a):.1f},{cy + r1 * math.sin(a):.1f}', 'hand', max(2, r * (.05 if big else .02))))
        if nums:
            for n in range(1, 13):
                a = n * math.pi / 6 - math.pi / 2
                it.append(T(f'{cx + r * .7 * math.cos(a):.1f}', f'{cy + r * .7 * math.sin(a) + r * .085:.1f}', str(n), int(r * .24), 'hand', 800))
        am = mm * math.pi / 30 - math.pi / 2; ah = (hh % 12 + mm / 60) * math.pi / 6 - math.pi / 2
        it += [S(f'M{cx},{cy} L{cx + r * .5 * math.cos(ah):.1f},{cy + r * .5 * math.sin(ah):.1f}', 'hand', r * .085),
               S(f'M{cx},{cy} L{cx + r * .78 * math.cos(am):.1f},{cy + r * .78 * math.sin(am):.1f}', 'hand', r * .05),
               C(cx, cy, r * .07, 'red')]
        return G(it)
    s.layer('clocks_big', [clock(960, 300, 190, 10, 10)], 'pop', .3, origin='960 300')
    s.layer('clocks_wall', [clock(580, 190, 80, 3, 0, 'square', col='teal'), clock(1350, 200, 84, 7, 30), clock(300, 440, 66, 12, 45, nums=False, col='pink'),
                            clock(1650, 450, 70, 9, 15, 'square', col='rim2'), clock(1230, 520, 52, 4, 20, nums=False, col='teal'), clock(660, 520, 56, 6, 0, nums=False)], 'pop', .5)
    s.layer('cuckoo', [clock(150, 230, 60, 2, 5, 'house', nums=False), clock(1790, 220, 58, 11, 55, 'house', nums=False)], 'drop', .7)
    # 落地摆钟
    # 柜台
    ct = [R(0, 820, W, 260, s.lg([(0, 'wood'), (1, 'counter')])), R(0, 800, W, 30, 'wood2'), R(0, 800, W, 8, '#E9C08E')]
    for x in range(120, W, 360): ct.append(R(x, 860, 240, 170, 'glass', 12, .25))
    ct.append(clock(380, 740, 46, 7, 0, nums=False, col='red'))
    ct += [C(350, 690, 16, 'red'), C(410, 690, 16, 'red'), R(355, 782, 10, 18, 'red'), R(395, 782, 10, 18, 'red')]
    ct.append(clock(1260, 750, 36, 5, 40, 'square', nums=False, col='teal'))
    s.layer('counter', ct, 'rise', .2)
    gx = 1720
    gf = [E(gx, 1050, 130, 18, '#000000', .25), P(f'M{gx - 90},600 Q{gx},540 {gx + 90},600Z', 'wood2'), R(gx - 95, 596, 190, 450, 'wood2', 18, extra='filter="url(#sh)"'), R(gx - 75, 616, 150, 130, 'face', 14),
          R(gx - 65, 766, 130, 240, 'glass', 10, .3), R(gx - 105, 1030, 210, 24, 'counter', 8)]
    gf.append(clock(gx, 681, 52, 1, 50, nums=False, col='wood'))
    s.layer('grandfather', gf, 'rise', .6)
    s.layer('pendulum', [S(f'M{gx},770 L{gx},940', 'rim', 6), C(gx, 952, 28, 'rim'), C(gx - 8, 944, 9, '#FFF2C8')], 'fade', 1.0, loop='swing', origin=f'{gx} 770')
    lamps = []
    for x in (340, 1580):
        lamps += [S(f'M{x},0 L{x},70', '#20262B', 4), P(f'M{x - 60},120 Q{x},40 {x + 60},120Z', 'rim2'), E(x, 122, 62, 10, 'lamp'),
                  P(f'M{x - 60},122 L{x + 60},122 L{x + 200},800 L{x - 200},800Z', s.lg([(0, 'lamp', .28), (1, 'lamp', 0)])), C(x, 130, 60, 'lamp', .5, 'filter="url(#b20)"')]
    s.layer('lamps', lamps, 'drop', .9, loop='glow')
    return s


# ============ 05 科学实验室 ============
def lab():
    s = Scene('s041', '科学实验室', '科学', ['科学', '化学', '实验', '探究'],
              dict(wall1='#E3F3F2', wall2='#CBE6E6', tile='#BFDCDC', bench='#2E3A46', bench2='#3D4C5B', cab='#F4F7F8', cab2='#D7E1E5', shelf='#9FB2BC',
                   glass='#E8FBFF', liq1='#5CC6F2', liq2='#F27BA0', liq3='#8EDC6E', liq4='#FFC94D', metal='#7C8A96', flame='#FF9F43', win1='#A6DCF7', win2='#E8F7FF', poster='#FFFFFF'),
              desc='明亮的实验室：瓷砖墙、玻璃器皿架、黑色实验台上冒泡的烧杯、显微镜和酒精灯。', stand={'ground_y': 900, 'x': [700, 1250]})
    bg = [R(0, 0, W, 700, s.lg([(0, 'wall1'), (1, 'wall2')]))]
    for x in range(0, W, 80): bg.append(R(x, 0, 2, 700, 'tile'))
    for y in range(0, 700, 80): bg.append(R(0, y, W, 2, 'tile'))
    bg.append(R(0, 700, W, 380, 'cab2'))
    s.layer('wall', bg, 'fade', 0)
    win = [R(780, 90, 360, 300, '#ffffff', 16, extra='filter="url(#shs)"'), R(796, 106, 328, 268, s.lg([(0, 'win1'), (1, 'win2')]), 8),
           cloud(900, 200, .5), R(956, 106, 8, 268, '#ffffff'), R(796, 236, 328, 8, '#ffffff')]
    s.layer('window', win, 'pop', .2)
    # 元素周期风格海报（无字色块）
    po = [R(1240, 110, 420, 270, 'poster', 14, extra='filter="url(#shs)"')]
    cols = ['liq1', 'liq2', 'liq3', 'liq4', 'shelf']
    for r_ in range(5):
        for k in range(10):
            if r_ == 0 and 0 < k < 9: continue
            if r_ in (1, 2) and 1 < k < 6: continue
            po.append(R(1262 + k * 39, 132 + r_ * 46, 33, 38, cols[(k * 3 + r_) % 5], 5, .75))
    s.layer('poster', po, 'pop', .35)

    def flask(x, y, sc, liq):
        d = f'M{x - 16 * sc},{y - 130 * sc} L{x - 16 * sc},{y - 70 * sc} L{x - 70 * sc},{y} L{x + 70 * sc},{y} L{x + 16 * sc},{y - 70 * sc} L{x + 16 * sc},{y - 130 * sc}Z'
        dl = f'M{x - 44 * sc},{y - 36 * sc} L{x - 70 * sc},{y} L{x + 70 * sc},{y} L{x + 44 * sc},{y - 36 * sc}Z'
        return G([P(d, 'glass', .7), P(dl, liq), S(d, 'metal', 3 * sc, .6), R(x - 20 * sc, y - 138 * sc, 40 * sc, 10 * sc, 'metal', 3), S(f'M{x + 30 * sc},{y - 40 * sc} L{x + 46 * sc},{y - 20 * sc}', '#ffffff', 6, .7)])

    def tube_rack(x, y):
        it = [R(x, y - 20, 220, 20, 'shelf', 4)]
        for k, cl in enumerate(['liq1', 'liq2', 'liq3', 'liq4']):
            tx = x + 30 + k * 50
            it += [R(tx - 12, y - 140, 24, 130, 'glass', 12, .8), R(tx - 12, y - 70, 24, 60, cl, 12), S(f'M{tx - 12},{y - 140} L{tx - 12},{y - 22} M{tx + 12},{y - 140} L{tx + 12},{y - 22}', 'metal', 2, .5)]
        it.append(R(x, y - 90, 220, 10, 'shelf', 4))
        return G(it)
    # 墙上搁板
    sh = [R(120, 300, 520, 16, 'shelf', 6, extra='filter="url(#shs)"'), R(120, 520, 520, 16, 'shelf', 6, extra='filter="url(#shs)"'),
          flask(200, 300, .7, 'liq2'), flask(330, 300, .55, 'liq3'), C(470, 260, 40, 'glass', .7), P('M430,262 A40,40 0 0,0 510,262Z', 'liq1'), R(458, 190, 24, 40, 'glass', 4, .7),
          R(560, 230, 50, 70, 'cab', 6), R(560, 230, 50, 18, 'liq4', 6), tube_rack(160, 520), flask(500, 520, .8, 'liq4')]
    s.layer('shelves', sh, 'slide-l', .45)
    # 实验台
    bn = [R(0, 760, W, 320, s.lg([(0, 'cab'), (1, 'cab2')])), R(0, 730, W, 40, 'bench', 6), R(0, 730, W, 8, 'bench2')]
    for x in range(40, W, 300): bn += [R(x, 800, 270, 250, 'cab', 10, extra='filter="url(#shs)"'), R(x + 115, 830, 40, 10, 'metal', 5)]
    s.layer('bench', bn, 'rise', .15)
    # 台上器材
    # 铁架台+烧杯+酒精灯
    eq = [R(1380, 380, 12, 352, 'metal', 4), R(1330, 722, 200, 12, 'metal', 4), R(1386, 556, 90, 8, 'metal', 4), S('M1421,560 a54,8 0 1,0 108,0 a54,8 0 1,0 -108,0', 'metal', 7),
          R(1425, 456, 100, 100, 'glass', 10, .75), R(1425, 494, 100, 62, 'liq1', 8), S('M1425,452 L1425,556 L1525,556 L1525,452', 'metal', 3, .6),
          P('M1446,730 L1504,730 L1496,668 L1454,668Z', 'glass', .95), R(1446, 700, 58, 30, 'liq4', 4, .5), R(1468, 652, 14, 18, 'metal'), P('M1475,654 Q1458,628 1475,596 Q1492,628 1475,654Z', 'flame'), P('M1475,650 Q1468,634 1475,616 Q1482,634 1475,650Z', '#FFE9A8')]
    s.layer('stand', eq, 'pop', .7)
    s.layer('bubbles', [C(1442 + k * 16, 520 - (k % 3) * 16, 5 + k % 3 * 2, '#ffffff', .85) for k in range(5)], 'fade', 1.1, loop='bob')
    s.layer('flame_glow', [C(1475, 630, 50, 'flame', .35, 'filter="url(#b20)"')], 'fade', 1.0, loop='glow')
    # 显微镜
    mx = 760
    mc = [E(mx, 732, 120, 10, '#000000', .15), R(mx - 100, 706, 200, 26, 'bench2', 12),
          P(f'M{mx + 60},708 C{mx + 110},640 {mx + 110},560 {mx + 40},500 L{mx + 10},526 C{mx + 70},580 {mx + 70},640 {mx + 26},708Z', '#5D6B78'),
          R(mx - 90, 628, 170, 14, 'bench2', 4), R(mx - 40, 620, 60, 8, 'glass', 2, .9), C(mx - 10, 612, 0.1, 'metal'),
          R(mx - 34, 420, 56, 150, 'metal', 14, extra=f'transform="rotate(-18 {mx} 500)"'), R(mx - 46, 392, 50, 44, '#3D4752', 10, extra=f'transform="rotate(-18 {mx} 500)"'),
          R(mx - 22, 566, 30, 40, '#3D4752', 6), C(mx + 64, 600, 18, '#3D4752'), C(mx + 64, 600, 7, 'metal'), C(mx - 20, 600, 0.1, 'metal')]
    s.layer('microscope', mc, 'pop', .85)
    s.layer('flasks_bench', [flask(1150, 730, .8, 'liq3'), flask(1660, 730, .65, 'liq2'), tube_rack(1730, 730), flask(300, 730, .7, 'liq1')], 'pop', .95)
    s.layer('light', [E(960, 260, 500, 160, '#ffffff', .4, 'filter="url(#b40)"')], 'fade', .5, loop='glow')
    return s


SCENES = [classroom, track, shanshui, clockshop, lab]
