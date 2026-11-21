from core import *
import math, random


# ============ 06 音乐教室 ============
def musicroom():
    s = Scene('s051', '音乐教室', '艺术与劳动', ['音乐', '艺术', '合唱', '节奏'],
              dict(wall1='#FFE7D6', wall2='#F8D2BF', curtain='#C8455A', curtain2='#A3354A', gold='#F2C14E', floor1='#B9744A', floor2='#9C5D38',
                   piano='#2B2A33', piano2='#3E3C48', key='#FFFFFF', board='#FFFFFF', staff='#C9B6E4', note='#7A5CC4', drum='#4FA3D9', drum2='#2F7FB5', skin='#FFF6EA', metal='#C9CED6',
                   xylo1='#F2836B', xylo2='#F7C55E', xylo3='#8ED081', xylo4='#5FB7E0', xylo5='#9B8CE8'),
              desc='暖色音乐教室：两侧丝绒幕布、五线谱白板、立式钢琴、架子鼓和彩色木琴，音符会飘动。', stand={'ground_y': 900, 'x': [640, 1280]})
    s.layer('wall', [R(0, 0, W, 780, s.lg([(0, 'wall1'), (1, 'wall2')])), *[R(x, 0, 4, 780, 'wall2', 0, .6) for x in range(60, W, 120)]], 'fade', 0)
    st = [R(560, 110, 800, 380, 'board', 22, extra='filter="url(#sh)"')]
    for k in range(5):
        y = 190 + k * 26; st.append(R(620, y, 680, 4, 'staff'))
        y2 = 340 + k * 26; st.append(R(620, y2, 680, 4, 'staff'))
    # 音符（四分、八分）
    for x, y in [(700, 268), (790, 242), (880, 255), (970, 216), (1060, 229), (1150, 203)]:
        st += [E(x, y, 15, 11, 'note', extra=f'transform="rotate(-20 {x} {y})"'), R(x + 11, y - 70, 5, 70, 'note')]
    st += [P('M1230,190 L1260,190 L1260,210 L1230,210Z', 'note', .0)]
    for x, y in [(720, 398), (820, 372), (920, 411), (1010, 385)]:
        st += [E(x, y, 15, 11, 'note', extra=f'transform="rotate(-20 {x} {y})"'), R(x + 11, y - 66, 5, 66, 'note')]
    st += [P('M831,306 L1021,319 L1021,331 L831,318Z', 'note')]  # 横梁连接 820/1010? 示意
    s.layer('staffboard', st[:-1] if False else st, 'drop', .3)
    fl = [R(0, 760, W, 320, s.lg([(0, 'floor1'), (1, 'floor2')]))] + [S(f'M0,{y} L{W},{y}', 'floor2', 3, .5) for y in (800, 850, 920, 1000)]
    s.layer('floor', fl, 'rise', .1)

    def curtain(x0, side):
        it = []
        for k in range(6):
            x = x0 + side * k * 46
            it.append(P(f'M{x - 30},0 L{x + 30},0 Q{x + 34 - side * 40},500 {x + 26 + side * 24},790 L{x - 26 + side * 24},790 Q{x - 30 - side * 30},500 {x - 30},0Z', 'curtain' if k % 2 else 'curtain2'))
        it.append(R(min(x0, x0 + side * 260) - 40, 0, 360, 60, 'curtain2'))
        for k in range(7): it.append(C(min(x0, x0 + side * 260) - 30 + k * 52, 62, 22, 'curtain2'))
        it.append(R(min(x0, x0 + side * 260) - 40, 44, 360, 10, 'gold'))
        return G(it)
    s.layer('curtains', [curtain(30, 1), curtain(1890, -1)], 'slide-l', .2)
    # 钢琴（左）
    pn = [E(420, 905, 230, 22, '#000000', .18), R(220, 560, 400, 330, 'piano', 16, extra='filter="url(#sh)"'), R(240, 580, 360, 120, 'piano2', 10),
          R(204, 700, 432, 30, 'piano', 6), R(214, 726, 412, 44, 'key', 4)]
    for k in range(20): pn.append(R(214 + k * 20.6, 726, 2, 44, '#C9CED6'))
    for k in range(20):
        if k % 7 in (2, 6): continue
        pn.append(R(228 + k * 20.6, 726, 12, 26, 'piano'))
    pn += [R(240, 770, 30, 120, 'piano'), R(570, 770, 30, 120, 'piano'), R(330, 600, 180, 70, 'board', 6, .95)]
    for k in range(3): pn.append(R(345, 615 + k * 18, 150, 3, 'staff'))
    s.layer('piano', pn, 'rise', .45)
    # 架子鼓（右）
    dx = 1560
    dr = [E(dx, 905, 250, 22, '#000000', .18), C(dx, 800, 110, 'drum', extra='filter="url(#sh)"'), C(dx, 800, 86, 'skin'), C(dx, 800, 30, 'drum2', .4),
          R(dx - 210, 700, 110, 60, 'drum2', 12), E(dx - 155, 700, 55, 14, 'skin'), R(dx + 110, 690, 110, 70, 'drum2', 12), E(dx + 165, 690, 55, 14, 'skin'),
          S(f'M{dx - 155},760 L{dx - 175},900 M{dx - 155},760 L{dx - 135},900', 'metal', 6), S(f'M{dx + 165},760 L{dx + 145},900 M{dx + 165},760 L{dx + 185},900', 'metal', 6),
          S(f'M{dx + 230},520 L{dx + 230},900', 'metal', 6), E(dx + 230, 520, 90, 14, 'gold'), S(f'M{dx - 250},560 L{dx - 250},900', 'metal', 6), E(dx - 250, 560, 80, 12, 'gold')]
    s.layer('drums', dr, 'rise', .55)
    s.layer('cymbal_glint', [C(dx + 200, 515, 10, '#ffffff', .9), C(dx - 270, 556, 8, '#ffffff', .9)], 'fade', 1.2, loop='twinkle')
    # 木琴（前）
    xy = [E(960, 1040, 260, 18, '#000000', .15), R(720, 980, 480, 16, 'floor2', 6)]
    for k in range(8):
        h = 120 - k * 9; xy.append(R(735 + k * 58, 980 - h / 2 - 10, 46, h, ['xylo1', 'xylo2', 'xylo3', 'xylo4', 'xylo5'][k % 5], 8, extra='filter="url(#shs)"'))
    xy += [R(740, 1000, 12, 60, 'floor2'), R(1168, 1000, 12, 60, 'floor2')]
    s.layer('xylophone', xy, 'pop', .8)
    nts = []
    for x, y, sc, col in [(560, 470, 1, 'note'), (1150, 470, .8, 'xylo1'), (900, 620, .7, 'xylo4'), (1080, 545, .9, 'xylo3')]:
        nts += [E(x, y, 18 * sc, 13 * sc, col, extra=f'transform="rotate(-20 {x} {y})"'), R(x + 13 * sc, y - 70 * sc, 6 * sc, 70 * sc, col), P(f'M{x + 13 * sc},{y - 70 * sc} q30,10 26,40 q-6,-20 -26,-24Z', col)]
    s.layer('notes', nts, 'pop', 1.0, loop='bob')
    s.layer('spot', [E(960, 860, 420, 60, '#FFF3C4', .35, 'filter="url(#b40)"')], 'fade', .9, loop='glow')
    return s


# ============ 07 十字路口 ============
def crossing():
    s = Scene('s061', '十字路口斑马线', '安全与法治', ['道德与法治', '交通安全', '安全教育', '生活'],
              dict(sky1='#9FD9F5', sky2='#F3FBFF', b1='#F6C8A8', b2='#BFD8EE', b3='#F7E3A4', b4='#C9E5C3', win='#FFFFFF', win2='#9CC6E6', awn1='#F2836B', awn2='#5FB7B0',
                   walk='#E7E1D7', curb='#C9C2B6', road='#4A5260', road2='#3C434F', stripe='#F5F5F0', yline='#F2C14E', pole='#5C6672', tl='#2F353D', red='#FF4B3E', amber='#5A4A22', green='#24422E',
                   tree='#69B97C', tree2='#A6DB95', trunk='#8A5A3A'),
              desc='街景十字路口：斑马线由近及远，红绿灯（当前红灯）与人行信号灯，两侧商铺和行道树。', stand={'ground_y': 820, 'x': [200, 640]})
    s.layer('sky', [R(0, 0, W, 600, s.lg([(0, 'sky1'), (1, 'sky2')])), cloud(300, 140, .8, op=.9), cloud(1400, 100, .6, op=.85)], 'fade', 0, loop=None)
    bl = []
    xs = [(0, 300, 380, 'b1'), (300, 260, 300, 'b2'), (560, 220, 440, 'b3'), (1140, 260, 360, 'b4'), (1400, 240, 460, 'b1'), (1640, 280, 330, 'b2')]
    for x, w, h, col in xs:
        top = 600 - h
        bl.append(R(x, top, w, h + 20, col, 8, extra='filter="url(#shs)"'))
        for wy in range(top + 30, 520, 64):
            for wx in range(x + 26, x + w - 50, 70): bl.append(R(wx, wy, 40, 44, 'win2', 4, .8)); bl.append(R(wx, wy, 40, 10, 'win', 3, .7))
        bl.append(R(x + 10, 520, w - 20, 80, 'win2', 4, .5))
        for k in range(int((w - 20) / 40)):
            bl.append(P(f'M{x + 10 + k * 40},500 L{x + 50 + k * 40},500 L{x + 50 + k * 40},530 Q{x + 30 + k * 40},548 {x + 10 + k * 40},530Z', 'awn1' if (k + x // 100) % 2 else 'win'))
    s.layer('buildings', bl, 'rise', .2)
    s.layer('trees', [blob_tree(x, 640, .9, 'tree', 'tree2', 'trunk') for x in (120, 520, 1200, 1700)], 'grow', .5, loop='sway')
    # 人行道与道路（透视）
    rd = [R(0, 600, W, 70, 'walk'), R(0, 664, W, 14, 'curb'), R(0, 678, W, 402, s.lg([(0, 'road2'), (1, 'road')]))]
    # 斑马线：路面从 y678 到 1080 由远到近
    vx = 960; vy = 300
    for k in range(-4, 5):
        xb0, xb1 = 960 + k * 130 - 45, 960 + k * 130 + 45
        def top(xb): return vx + (xb - vx) * (700 - vy) / (1080 - vy)
        rd.append(poly([(top(xb0), 700), (top(xb1), 700), (xb1, 1080), (xb0, 1080)], 'stripe', .95))
    rd += [R(0, 682, W, 6, 'yline', 0, .0)]
    s.layer('road', rd, 'rise', .1)
    # 停止线（近景两侧）
    # 红绿灯
    tl = [R(1500, 200, 22, 470, 'pole', 6), R(1500, 220, 300, 18, 'pole', 6), R(1730, 170, 90, 250, 'tl', 18, extra='filter="url(#sh)"'),
          C(1775, 220, 30, 'red'), C(1775, 295, 30, 'amber'), C(1775, 370, 30, 'green'), R(1430, 400, 70, 130, 'tl', 12), C(1465, 434, 20, 'red'), C(1465, 494, 20, 'green')]
    # 行人信号图形（站立小人、行走小人）
    tl += [C(1465, 424, 5, '#ffffff'), R(1461, 430, 8, 18, '#ffffff', 3), C(1465, 484, 5, '#6F8F78'), R(1461, 490, 8, 16, '#6F8F78', 3)]
    s.layer('traffic_light', tl, 'drop', .6)
    s.layer('red_glow', [C(1775, 220, 70, 'red', .45, 'filter="url(#b20)"'), C(1465, 434, 40, 'red', .4, 'filter="url(#b20)"')], 'fade', 1.0, loop='glow')
    lamp = [R(300, 260, 14, 410, 'pole', 5), P('M300,262 Q300,230 350,230 L380,230', 'none', extra=''), S('M307,262 Q307,230 350,230 L380,232', 'pole', 10), E(390, 240, 40, 14, 'tl'), E(390, 250, 26, 6, '#FFF3C4')]
    s.layer('street_lamp', lamp[:1] + lamp[2:], 'grow', .7)
    sign = [R(140, 380, 10, 290, 'pole', 4), C(145, 360, 46, '#ffffff'), C(145, 360, 40, '#2F7FC9'), poly([(118, 390), (172, 390), (145, 330)], '#ffffff', .0),
            R(124, 372, 42, 6, '#ffffff'), R(124, 352, 42, 6, '#ffffff'), R(124, 332, 42, 6, '#ffffff', 0, .0)]
    return s


# ============ 08 客厅 ============
def livingroom():
    s = Scene('s071', '温馨客厅', '家庭生活', ['家庭', '亲子', '心理健康', '生活习惯'],
              dict(wall1='#F4E2CF', wall2='#E9CDB0', pat='#EBD3B8', floor1='#C98D5B', floor2='#A96F42', rug='#E8B4A0', rug2='#D99A86', sofa='#5E8F96', sofa2='#4C7980',
                   wood='#B47A4E', wood2='#8E5B36', sky1='#F7B48A', sky2='#FBD9A8', city='#C28F86', lamp='#FFE3A3', leaf='#5FA873', leaf2='#8FCB8E', pot='#E9ECEF',
                   frame='#FFFFFF', art1='#F2C14E', art2='#7FC4E8', art3='#F28B6E', book1='#F28B6E', book2='#5FB7B0', book3='#F2C14E', book4='#8E7CC3', tv='#2C3038'),
              desc='傍晚的客厅：大窗外是晚霞城市，沙发、茶几、地毯、落地灯与书架，暖光氛围。', stand={'ground_y': 930, 'x': [560, 1360]})
    bg = [R(0, 0, W, 800, s.lg([(0, 'wall1'), (1, 'wall2')]))]
    for x in range(0, W, 64): bg.append(R(x, 0, 30, 800, 'pat', 0, .35))
    bg.append(R(0, 770, W, 30, 'wood2'))
    s.layer('wall', bg, 'fade', 0)
    win = [R(620, 90, 680, 420, 'frame', 14, extra='filter="url(#shs)"'), R(640, 110, 640, 380, s.lg([(0, 'sky1'), (1, 'sky2')]), 6)]
    cp = s.clip('<rect x="640" y="110" width="640" height="380"/>')
    random.seed(5); cty = [C(1080, 330, 60, '#FFF0C8', .9)]
    x = 640
    while x < 1280:
        w = random.randint(50, 90); h = random.randint(80, 210); cty.append(R(x, 490 - h, w, h, 'city', 3, .85))
        for wy in range(490 - h + 14, 480, 26):
            if random.random() < .6: cty.append(R(x + 12, wy, 10, 12, '#FFE3A3', 1, .9))
        x += w + 6
    win.append(G(cty, f'clip-path="{cp}"'))
    win += [R(955, 110, 10, 380, 'frame'), R(600, 500, 720, 22, 'frame', 6),
            P('M560,70 L700,70 Q690,300 720,560 L600,560 Q590,300 560,70Z', 'art3', .85), P('M1360,70 L1220,70 Q1230,300 1200,560 L1320,560 Q1330,300 1360,70Z', 'art3', .85), R(540, 58, 840, 14, 'wood2', 6)]
    s.layer('window', win, 'pop', .25)
    # 画框
    fr = [R(240, 180, 200, 150, 'frame', 8, extra='filter="url(#shs)"'), R(256, 196, 168, 118, 'art2', 4), P('M256,314 L320,240 L370,290 L400,262 L424,314Z', 'leaf'), C(390, 226, 16, 'art1'),
          R(1490, 170, 150, 190, 'frame', 8, extra='filter="url(#shs)"'), R(1504, 184, 122, 162, 'art1', 4), C(1565, 265, 40, 'art3'),
          R(1660, 230, 110, 110, 'frame', 8, extra='filter="url(#shs)"'), R(1672, 242, 86, 86, 'art2', 4, .7)]
    s.layer('frames', fr, 'pop', .4)
    fl = [R(0, 800, W, 280, s.lg([(0, 'floor1'), (1, 'floor2')]))] + [S(f'M{x},800 L{x - 80},1080', 'floor2', 3, .4) for x in range(100, W + 100, 180)]
    s.layer('floor', fl, 'rise', .1)
    s.layer('rug', [E(960, 960, 620, 90, 'rug'), E(960, 960, 560, 72, 'rug2', .5), E(960, 960, 480, 56, 'rug', 1)], 'grow', .5)
    # 沙发
    sf = [E(960, 840, 430, 26, '#000000', .18), R(560, 560, 800, 200, 'sofa2', 60, extra='filter="url(#sh)"'), R(600, 680, 720, 120, 'sofa', 30),
          R(520, 640, 120, 190, 'sofa', 50), R(1280, 640, 120, 190, 'sofa', 50), R(610, 600, 340, 110, 'sofa', 36, .6), R(970, 600, 340, 110, 'sofa', 36, .6),
          R(660, 620, 120, 90, 'art1', 24, extra='transform="rotate(-8 720 665)"'), R(1150, 620, 120, 90, 'art3', 24, extra='transform="rotate(8 1210 665)"'),
          R(580, 820, 22, 30, 'wood2', 4), R(1320, 820, 22, 30, 'wood2', 4)]
    s.layer('sofa', sf, 'rise', .45)
    # 落地灯
    lp = [R(1490, 480, 10, 400, 'wood2', 4), E(1495, 882, 60, 12, 'wood2'), P('M1430,400 L1560,400 L1530,490 L1460,490Z', 'lamp'), C(1495, 470, 260, 'lamp', .35, 'filter="url(#b40)"')]
    s.layer('floor_lamp', lp, 'grow', .6, loop='glow', origin='1495 882')
    # 书架
    bs = [R(1620, 380, 260, 440, 'wood', 10, extra='filter="url(#sh)"')]
    for k in range(3): bs.append(R(1636, 400 + k * 140, 228, 118, 'wood2', 4))
    random.seed(8)
    for k in range(3):
        x = 1644
        while x < 1840:
            w = random.randint(16, 28); h = random.randint(80, 108); bs.append(R(x, 518 + k * 140 - h, w, h, ['book1', 'book2', 'book3', 'book4'][random.randint(0, 3)], 3)); x += w + 3
    s.layer('bookshelf', bs, 'slide-r', .55)
    # 电视柜与绿植（左）
    tv = [R(60, 640, 380, 170, 'wood', 12, extra='filter="url(#sh)"'), R(80, 670, 160, 110, 'wood2', 6), R(260, 670, 160, 110, 'wood2', 6),
          R(150, 520, 120, 120, 'pot', 50), *[E(210 + 80 * math.cos(a), 450 + 60 * math.sin(a), 70, 24, 'leaf' if k % 2 else 'leaf2', extra=f'transform="rotate({math.degrees(a):.0f} {210 + 80 * math.cos(a):.0f} {450 + 60 * math.sin(a):.0f})"') for k, a in enumerate([-2.8, -2.2, -1.6, -1.0, -.4, -3.4])],
          R(320, 600, 60, 40, 'art2', 8), C(350, 590, 22, 'art1')]
    s.layer('cabinet', tv, 'rise', .65)
    tb = [E(960, 945, 260, 20, '#000000', .15), R(740, 870, 440, 30, 'wood', 14, extra='filter="url(#shs)"'), R(770, 898, 18, 50, 'wood2'), R(1132, 898, 18, 50, 'wood2'),
          R(860, 838, 70, 34, '#ffffff', 10), R(905, 845, 20, 18, '#ffffff', 8), R(1000, 846, 110, 24, 'book2', 4), R(1010, 830, 90, 18, 'book1', 4)]
    s.layer('table', tb, 'pop', .8)
    s.layer('steam', [S(f'M{x},826 q-12,-20 0,-40 q12,-20 0,-40', '#ffffff', 5, .7) for x in (880, 905)], 'fade', 1.1, loop='flow')
    return s


# ============ 09 菜市场 ============
def market():
    s = Scene('s081', '热闹菜市场', '社会日常', ['数学', '劳动', '营养', '社会生活'],
              dict(wall1='#F3D9B5', wall2='#E7C394', brick='#E2B88A', awn1='#E85D4F', awn2='#FFFFFF', awn3='#3FA67A', awn4='#F2B33D', wood='#C58A55', wood2='#9C6537',
                   tomato='#E8483B', cabbage='#8CCB6E', cabbage2='#C3E59C', carrot='#F28C2E', eggplant='#7B4A9C', orange='#F7A02E', apple='#E2483C', banana='#F7D54A', leaf='#4E9E5A',
                   bulb='#FFE7A0', wire='#4A3B32', crate='#D7A26A', tag='#FFFFFF'),
              desc='三个彩色条纹遮阳棚摊位，摆满蔬菜水果的木箱、电子秤，串灯点亮，适合认识人民币、营养搭配。', stand={'ground_y': 950, 'x': [300, 1620]})
    bg = [R(0, 0, W, 800, s.lg([(0, 'wall1'), (1, 'wall2')]))]
    for y in range(0, 800, 40):
        for x in range(-((y // 40) % 2) * 50, W, 100): bg.append(R(x + 3, y + 3, 94, 34, 'brick', 4, .45))
    s.layer('wall', bg, 'fade', 0)
    fl = [R(0, 800, W, 280, s.lg([(0, '#D6C3A8'), (1, '#BFA888')]))] + [R(x, 800, 2, 280, '#ffffff', 0, .25) for x in range(0, W, 160)]
    s.layer('floor', fl, 'rise', .1)

    def stall(x0, w, c1, c2, delay_key):
        it = [R(x0 + 10, 330, 14, 470, 'wood2', 4), R(x0 + w - 24, 330, 14, 470, 'wood2', 4)]
        n = 8; sw = (w + 40) / n
        for k in range(n):
            xx = x0 - 20 + k * sw
            it.append(P(f'M{xx},250 L{xx + sw},250 L{xx + sw},340 Q{xx + sw / 2},372 {xx},340Z', c1 if k % 2 == 0 else c2))
        it.append(R(x0 - 30, 236, w + 60, 22, c1, 8))
        # 货台
        it += [R(x0 - 10, 640, w + 20, 160, 'wood', 10, extra='filter="url(#sh)"'), R(x0 - 10, 640, w + 20, 18, 'wood2', 6)]
        for k in range(int(w // 120)): it.append(R(x0 + 10 + k * 120, 680, 100, 100, 'crate', 8, .55))
        return G(it)
    s.layer('stalls', [stall(80, 520, 'awn1', 'awn2', 0), stall(700, 520, 'awn3', 'awn2', 1), stall(1320, 520, 'awn4', 'awn2', 2)], 'rise', .3)

    def heap(cx, cy, n, r, col, hl, seed):
        random.seed(seed); it = []
        rows = [(n, 0), (n - 1, -1), (n - 2, -2)]
        for cnt, row in rows:
            for k in range(cnt):
                x = cx + (k - (cnt - 1) / 2) * r * 1.8; y = cy + row * r * 1.5
                it += [C(x, y, r, col), C(x - r * .35, y - r * .35, r * .3, hl, .5)]
        return G(it)

    def crate_box(x, y, w):
        return G([R(x, y, w, 70, 'crate', 6, extra='filter="url(#shs)"'), R(x, y + 30, w, 6, 'wood2', 0, .5), R(x, y, w, 8, 'wood2', 3, .6)])
    veg = [crate_box(110, 590, 220), heap(220, 590, 5, 20, 'tomato', '#ffffff', 1), crate_box(360, 590, 210)]
    for k in range(3):
        x = 400 + k * 66
        veg += [C(x, 572, 38, 'cabbage'), C(x - 8, 562, 22, 'cabbage2', .8), S(f'M{x - 20},580 Q{x},540 {x + 20},580', 'leaf', 3, .6)]
    s.layer('veg', veg, 'pop', .6)
    v2 = [crate_box(730, 590, 220)]
    for k in range(6):
        x = 750 + k * 34; v2 += [P(f'M{x},590 L{x + 22},590 L{x + 11},500Z', 'carrot', extra=f'transform="rotate({(k - 2.5) * 5} {x + 11} 590)"'), P(f'M{x + 11},500 l-10,-24 l10,10 l10,-12Z', 'leaf')]
    v2.append(crate_box(980, 590, 210))
    for k in range(4):
        x = 1010 + k * 46; v2 += [E(x, 560, 22, 46, 'eggplant', extra=f'transform="rotate({(k - 1.5) * 12} {x} 560)"'), P(f'M{x - 12},516 L{x + 12},516 L{x},500Z', 'leaf')]
    s.layer('veg2', v2, 'pop', .75)
    fr = [crate_box(1350, 590, 220), heap(1460, 590, 5, 20, 'orange', '#FFE0A0', 2), crate_box(1600, 590, 210), heap(1705, 590, 5, 20, 'apple', '#ffffff', 3)]
    s.layer('fruit', fr, 'pop', .9)
    # 秤与价签
    sc = [R(560, 600, 120, 40, '#E9ECEF', 8, extra='filter="url(#shs)"'), R(570, 584, 100, 16, '#C9CED6', 6), R(590, 610, 60, 20, '#3D4752', 4), R(598, 614, 30, 12, '#8EF0B0', 2)]
    for x in (230, 470, 840, 1080, 1460, 1700): sc += [R(x - 30, 650, 60, 40, 'tag', 6, extra='filter="url(#shs)"'), R(x - 20, 662, 40, 6, '#C9CED6', 3), R(x - 20, 674, 26, 6, '#E85D4F', 3)]
    s.layer('scale_tags', sc, 'pop', 1.0)
    # 串灯
    bl = [S('M0,90 Q480,190 960,100 Q1440,190 1920,90', 'wire', 3)]
    for k in range(17):
        u = k / 16; x = u * 1920
        local = (u * 2) % 1
        t_ = local; y0_, y2_ = (90, 100) if u <= .5 else (100, 90)
        y = (1 - t_) ** 2 * y0_ + 2 * t_ * (1 - t_) * 190 + t_ ** 2 * y2_ - 4
        bl += [R(x - 5, y, 10, 14, 'wire', 2), E(x, y + 26, 13, 17, 'bulb'), C(x, y + 26, 34, 'bulb', .35, 'filter="url(#b20)"')]
    s.layer('string_lights', bl, 'drop', 1.1, loop='twinkle')
    return s


# ============ 10 森林 ============
def forest():
    s = Scene('s091', '晨雾森林', '自然与地理', ['科学', '自然', '生态', '户外'],
              dict(sky1='#CFEBDF', sky2='#FFF6DD', far='#A9D3BE', mid='#6FB28C', mid2='#5A9E7A', near='#3F7F5F', near2='#2F6A4E', trunk='#7A5238', trunk2='#5E3D29',
                   ground1='#7FBF6A', ground2='#5FA552', water='#8FD3E8', water2='#C9F0FA', rock='#9AA5A8', rock2='#C3CBCC', mush='#E8574A', dot='#FFFFFF', flower='#F7C55E', fly='#FFF2A0'),
              desc='层层远近的森林、穿林光束、弯曲小溪、蘑菇和萤火，适合自然科学与生态主题。', stand={'ground_y': 920, 'x': [300, 900]})
    s.layer('sky', [R(0, 0, W, H, s.lg([(0, 'sky1'), (1, 'sky2')])), C(1350, 220, 220, '#FFF6D0', .7, 'filter="url(#b40)"')], 'fade', 0)

    def trees_row(y, n, h, col, col2, seed, wmin=40, wmax=80):
        random.seed(seed); it = []
        for k in range(n):
            x = k * W / (n - 1) + random.uniform(-30, 30); hh = h * random.uniform(.8, 1.15); w = random.uniform(wmin, wmax)
            if random.random() < .55:
                for q in range(4):
                    ww = w * (1.6 - q * .3); yy = y - q * hh * .22
                    it.append(poly([(x - ww, yy), (x + ww, yy), (x, yy - hh * .42)], col))
                    it.append(poly([(x, yy), (x + ww, yy), (x, yy - hh * .42)], col2, .5))
            else:
                it += [R(x - w * .12, y - hh * .5, w * .24, hh * .5, 'trunk'), E(x, y - hh * .65, w * 1.1, hh * .45, col), E(x + w * .3, y - hh * .55, w * .6, hh * .3, col2, .5)]
        return G(it)
    s.layer('far', [trees_row(560, 22, 260, 'far', 'sky2', 1), R(0, 540, W, 60, 'far')], 'rise', .2)
    s.layer('fog1', [R(0, 430, W, 200, s.lg([(0, 'sky2', 0), (.6, 'sky2', .8), (1, 'sky2', 0)]))], 'fade', .35, loop='drift')
    s.layer('mid', [trees_row(700, 14, 380, 'mid', 'mid2', 4, 60, 100), R(0, 680, W, 60, 'mid')], 'rise', .35)
    s.layer('fog2', [R(0, 590, W, 160, s.lg([(0, 'sky2', 0), (.5, 'sky2', .6), (1, 'sky2', 0)]))], 'fade', .5, loop='drift')
    s.layer('rays', [beam(1180, 1280, 900, 1120, 0, 1000, s, .3), beam(1380, 1440, 1240, 1400, 0, 1000, s, .25), beam(1560, 1640, 1520, 1720, 0, 1000, s, .2)], 'fade', .8, loop='glow')
    # 地面与小溪
    gd = [P(f'M0,760 Q480,720 960,750 Q1440,780 1920,740 L1920,1080 L0,1080Z', s.lg([(0, 'ground1'), (1, 'ground2')]))]
    gd.append(P('M1100,750 Q1180,800 1080,860 Q960,940 1150,1080 L1560,1080 Q1300,960 1400,880 Q1480,810 1230,752Z', s.lg([(0, 'water2'), (1, 'water')])))
    gd += [S('M1180,900 q30,-6 60,0', '#ffffff', 4, .7), S('M1260,990 q40,-8 80,0', '#ffffff', 4, .7), S('M1150,820 q24,-5 48,0', '#ffffff', 3, .6)]
    s.layer('ground', gd, 'rise', .15)
    s.layer('stream_shine', [S('M1300,1040 q40,-8 80,0', '#ffffff', 4, .8), S('M1120,950 q30,-6 60,0', '#ffffff', 4, .8)], 'fade', 1.0, loop='flow')
    # 近景大树（左右框住画面）
    nt = [R(40, 0, 90, 860, s.lg([(0, 'trunk2'), (.5, 'trunk'), (1, 'trunk2')], 0, 0, 1, 0)), P('M30,860 Q85,800 140,860Z', 'trunk2'), E(80, 60, 260, 200, 'near'), E(220, 120, 150, 110, 'near2'),
          R(1780, 0, 80, 880, s.lg([(0, 'trunk2'), (.5, 'trunk'), (1, 'trunk2')], 0, 0, 1, 0)), E(1830, 40, 240, 180, 'near'), E(1680, 100, 150, 100, 'near2')]
    s.layer('near_trees', nt, 'slide-l', .55)
    # 石头、蘑菇、花
    rk = [E(1000, 900, 90, 50, 'rock'), E(980, 885, 60, 28, 'rock2', .7), E(1600, 870, 70, 40, 'rock'), E(1590, 860, 44, 20, 'rock2', .7)]
    s.layer('rocks', rk, 'pop', .7)
    ms = []
    for x, y, sc in [(330, 930, 1), (400, 950, .7), (700, 880, .8)]:
        ms += [R(x - 10 * sc, y - 40 * sc, 20 * sc, 40 * sc, '#FFF4E4', 6), P(f'M{x - 44 * sc},{y - 36 * sc} Q{x},{y - 100 * sc} {x + 44 * sc},{y - 36 * sc}Z', 'mush'),
               C(x - 14 * sc, y - 60 * sc, 7 * sc, 'dot'), C(x + 16 * sc, y - 54 * sc, 5 * sc, 'dot'), C(x + 2 * sc, y - 74 * sc, 5 * sc, 'dot')]
    s.layer('mushrooms', ms, 'pop', .85)
    fw = []
    random.seed(9)
    for k in range(18):
        x = random.uniform(200, 1000) if k % 2 else random.uniform(1450, 1760); y = random.uniform(820, 1060)
        fw += [S(f'M{x},{y} L{x},{y - 30}', 'near', 3), C(x, y - 34, 8, 'flower' if k % 3 else 'mush'), C(x, y - 34, 3, '#ffffff')]
    s.layer('flowers', fw, 'grow', 1.0, loop='sway')
    random.seed(11)
    s.layer('fireflies', [C(random.uniform(200, 1700), random.uniform(500, 900), random.uniform(4, 7), 'fly', .9) for _ in range(16)], 'fade', 1.2, loop='twinkle')
    return s


SCENES = [musicroom, crossing, livingroom, market, forest]
