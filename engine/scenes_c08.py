from core import *
from scenes_c07 import shadow, plant_pot, skyline, tiles, arrow
import math, random


def window(s, x0, y0, w, h, sky1, sky2, frame, inner=(), sill=True, cross=True):
    it = [R(x0 - 16, y0 - 16, w + 32, h + 32, frame, 16, extra='filter="url(#shs)"'), R(x0, y0, w, h, s.lg([(0, sky1), (1, sky2)]), 8)]
    cp = s.clip(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="8"/>')
    if inner: it.append(G(list(inner), f'clip-path="{cp}"'))
    if cross: it += [R(x0 + w / 2 - 4, y0, 8, h, frame), R(x0, y0 + h * .45, w, 8, frame)]
    it.append(P(f'M{x0 + 30},{y0} L{x0 + 80},{y0} L{x0 + 30},{y0 + h} L{x0 + 10},{y0 + h}Z', '#ffffff', .18))
    if sill: it.append(R(x0 - 30, y0 + h + 12, w + 60, 18, frame, 6))
    return it


def books(x0, x1, ybase, cols, seed, hmin=60, hmax=90):
    random.seed(seed); it = []; x = x0
    while x < x1 - 14:
        w = random.randint(14, 24); h = random.randint(hmin, hmax)
        it.append(R(x, ybase - h, w, h, cols[random.randint(0, len(cols) - 1)], 3)); x += w + 3
    return it


def floor_planks(s, y0, c1, c2, step=180, slant=80):
    return [R(0, y0, W, H - y0, s.lg([(0, c1), (1, c2)]))] + [S(f'M{x},{y0} L{x - slant},1080', c2, 3, .4) for x in range(100, W + 200, step)]


# ================= 072 厨房 =================
def kitchen():
    s = Scene('s072', '厨房', '家庭生活', ['劳动', '家务', '饮食安全', '营养'],
              dict(wall1='#FFF6EA', wall2='#F6E6D2', tile='#D6EEE6', tile2='#B9DFD3', cab='#8CC7B5', cab2='#73B29F', knob='#F4E1C1', counter='#F4EDE3', counter2='#DCD2C4',
                   wood='#D9A06B', wood2='#B9824F', hood='#E3E8EC', hood2='#C4CCD3', steel='#B4BDC6', stove='#3A3F46', flame='#5DA9F5', pot='#E8604F', pot2='#C94E3F',
                   fridge='#F7F3EC', fridge2='#E2DBCF', sky1='#A8DCF5', sky2='#EAF8FF', leaf='#6FB57E', leaf2='#A6D99A', tomato='#E8483B', carrot='#F28C2E', fl1='#F3E7D8', fl2='#E3D3C0'),
              desc='薄荷绿橱柜的明亮厨房：窗下水槽、中央灶台上冒热气的红锅、油烟机，右侧冰箱、挂勺与切菜板。', stand={'ground_y': 940, 'x': [560, 1360]})
    s.layer('wall', [R(0, 0, W, 880, s.lg([(0, 'wall1'), (1, 'wall2')]))], 'fade', 0)
    s.layer('tiles', [R(0, 330, W, 290, 'tile'), *tiles(0, 330, W, 620, 48, 'tile2', .9, 3)], 'fade', .1)
    win = window(s, 170, 90, 400, 300, 'sky1', 'sky2', '#ffffff', [cloud(300, 170, .45), C(260, 420, 120, 'leaf'), C(470, 440, 130, 'leaf'), C(380, 400, 60, 'leaf2', .7)], sill=False)
    win += [plant_pot(240, 400, .55, 'pot', 'leaf', 'leaf2'), plant_pot(500, 400, .45, 'knob', 'leaf', 'leaf2'), R(140, 392, 460, 14, '#ffffff', 6)]
    s.layer('window', win, 'pop', .25)
    uc = []
    for x0, n in ((1220, 3),):
        for k in range(n):
            x = x0 + k * 130
            uc += [R(x, 100, 124, 210, 'cab', 10, extra='filter="url(#shs)"'), R(x + 12, 112, 100, 186, 'cab2', 8, .35), R(x + (96 if k % 2 == 0 else 18), 260, 10, 40, 'knob', 5)]
    uc += [R(640, 100, 110, 210, 'cab', 10, extra='filter="url(#shs)"'), R(652, 112, 86, 186, 'cab2', 8, .35), R(718, 260, 10, 40, 'knob', 5)]
    s.layer('upper_cabinets', uc, 'drop', .35)
    hd = [P('M790,80 L1130,80 L1130,250 L1180,330 L740,330 L790,250Z', 'hood', extra='filter="url(#shs)"'), R(880, 0, 160, 84, 'hood2'), R(740, 318, 440, 14, 'hood2', 4),
          R(780, 300, 360, 6, '#ffffff', 3, .5), C(1100, 290, 6, 'flame'), C(1080, 290, 6, 'steel')]
    s.layer('hood', hd, 'drop', .45)
    ct = [R(0, 620, W, 260, s.lg([(0, 'cab'), (1, 'cab2')])), R(0, 600, W, 30, 'counter', 6, extra='filter="url(#shs)"'), R(0, 624, W, 6, 'counter2')]
    for x in range(20, W, 240):
        ct += [R(x, 650, 220, 210, 'cab', 10, extra='filter="url(#shs)"'), R(x + 80, 670, 60, 10, 'knob', 5)]
    ct += [R(790, 640, 340, 230, 'stove', 12), R(810, 660, 300, 120, '#4A5059', 8), *[C(840 + k * 60, 820, 10, 'steel') for k in range(5)]]
    s.layer('counter', ct, 'rise', .15)
    sv = [R(790, 588, 340, 16, 'stove', 6), R(820, 580, 120, 10, 'stove', 4), R(980, 580, 120, 10, 'stove', 4),
          *[P(f'M{x - 8 + k * 9},586 q4,-14 4,-18 q4,8 4,18Z', 'flame') for x in (860, 1020) for k in range(3)],
          P('M830,520 L950,520 L944,584 L836,584Z', 'pot'), R(820, 510, 140, 16, 'pot2', 8), R(870, 496, 40, 16, 'pot2', 8), R(800, 534, 30, 10, 'pot2', 5), R(950, 534, 30, 10, 'pot2', 5),
          P('M990,560 L1110,560 L1110,580 L990,580Z', 'steel'), R(1110, 564, 90, 10, 'stove', 5), R(1000, 548, 100, 14, 'hood2', 7)]
    s.layer('stove_pot', sv, 'pop', .6)
    s.layer('steam', [S(f'M{x},490 q-14,-24 0,-48 q14,-24 0,-48', '#ffffff', 6, .75) for x in (860, 890, 920)], 'fade', 1.0, loop='flow')
    sk = [P('M250,600 L490,600 L470,640 L270,640Z', 'steel', .6), R(240, 592, 260, 12, 'steel', 6), R(356, 500, 12, 96, 'steel', 6), P('M362,506 Q362,470 400,470 L420,470 L420,486 L402,486 Q380,486 378,506Z', 'steel'),
          C(330, 580, 10, 'steel'), C(400, 580, 10, 'steel')]
    s.layer('sink', sk, 'pop', .5)
    ut = [R(1240, 380, 340, 10, 'steel', 5)]
    for x, kind in [(1280, 'ladle'), (1340, 'spat'), (1400, 'whisk'), (1480, 'pan')]:
        ut.append(R(x - 2, 386, 4, 18, 'steel'))
        if kind == 'ladle': ut += [R(x - 4, 402, 8, 90, 'wood2', 4), E(x, 500, 22, 16, 'steel')]
        if kind == 'spat': ut += [R(x - 4, 402, 8, 80, 'wood2', 4), R(x - 18, 480, 36, 40, 'steel', 6)]
        if kind == 'whisk': ut += [R(x - 4, 402, 8, 50, 'wood2', 4), S(f'M{x},450 C{x - 26},490 {x - 16},530 {x},530 C{x + 16},530 {x + 26},490 {x},450', 'steel', 4), S(f'M{x},450 L{x},528', 'steel', 3)]
        if kind == 'pan': ut += [R(x - 5, 402, 10, 70, 'stove', 5), C(x, 520, 52, 'stove'), C(x, 520, 40, '#4A5059')]
    s.layer('utensils', ut, 'drop', .7, loop='sway')
    fx = 1640
    fr = [shadow(fx + 130, 882, 160, 10, .15), R(fx, 120, 260, 760, 'fridge', 22, extra='filter="url(#sh)"'), R(fx, 400, 260, 8, 'fridge2'), R(fx + 24, 200, 12, 120, 'fridge2', 6), R(fx + 24, 440, 12, 160, 'fridge2', 6),
          R(fx + 80, 160, 60, 60, 'tile', 8), C(fx + 180, 200, 22, 'tomato'), R(fx + 150, 470, 80, 56, '#ffffff', 6, extra='transform="rotate(4 1830 500)"'), R(fx + 160, 486, 50, 6, 'tile2', 3), R(fx + 160, 500, 40, 6, 'tile2', 3)]
    s.layer('fridge', fr, 'slide-r', .55)
    bd = [R(1240, 584, 220, 20, 'wood', 8, extra='filter="url(#shs)"'), C(1300, 572, 18, 'tomato'), C(1338, 574, 16, 'tomato'), C(1296, 566, 5, '#ffffff', .5),
          P('M1380,590 L1440,578 L1446,586 L1386,598Z', 'carrot'), P('M1440,578 l14,-10 l-4,14Z', 'leaf'), E(1540, 580, 60, 22, 'wood2'), C(1520, 562, 16, '#F7D35E'), C(1550, 558, 18, 'tomato'), C(1576, 566, 14, 'leaf2')]
    s.layer('board_veg', bd, 'pop', .8)
    s.layer('floor', [R(0, 880, W, 200, 'fl1')] + [R(x, y, 80, 50, 'fl2') for y in range(880, 1080, 50) for x in range(((y - 880) // 50 % 2) * 80, W, 160)], 'rise', .1)
    s.layer('sunlight', [beam(220, 520, 600, 980, 400, 1080, s, .2), E(800, 980, 240, 30, '#FFF6D8', .35, 'filter="url(#b20)"')], 'fade', .9, loop='glow')
    return s


# ================= 073 卧室 =================
def bedroom():
    s = Scene('s073', '卧室', '家庭生活', ['作息习惯', '睡眠健康', '整理收纳', '家庭'],
              dict(wall1='#ECE6F7', wall2='#DED4F0', dot='#D2C6EA', floor1='#DDB78C', floor2='#C69E71', rug='#F6CFC8', rug2='#EDB3AA', bed='#F7F3EE', head='#B98A63', head2='#9C7050',
                   quilt='#8EC8EA', quilt2='#6FB0DA', pillow='#FFFFFF', curtain='#F4ADA4', curtain2='#E8968C', sky1='#FFD7B0', sky2='#C9ECFA', sun='#FFE7A6',
                   ward='#F4ECE1', ward2='#E1D4C3', knob='#C9A27A', lamp='#FFE3A3', lampb='#7FC4B8', star='#FFE08A', bear='#D9A06B', bear2='#B98252', clock='#7FC4B8', book1='#F28B6E', book2='#7FC4E8', book3='#F7C55E', leaf='#6FB57E', leaf2='#A6D99A', pot='#F4ECE1'),
              desc='淡紫色清晨卧室：晨光窗与粉色窗帘、蓝被子的小床、床头灯和闹钟、衣柜与小熊，星星串灯和月亮挂饰。', stand={'ground_y': 940, 'x': [800, 1400]})
    bg = [R(0, 0, W, 800, s.lg([(0, 'wall1'), (1, 'wall2')]))]
    for y in range(40, 800, 80):
        for x in range(40 + (y // 80 % 2) * 40, W, 80): bg.append(C(x, y, 4, 'dot', .8))
    s.layer('wall', bg, 'fade', 0)
    inner = [C(960, 420, 70, 'sun', .95), C(960, 420, 140, 'sun', .35, 'filter="url(#b40)"'), cloud(850, 230, .45), cloud(1100, 300, .35, op=.85),
             P('M720,520 Q820,440 920,500 Q1020,430 1200,500 L1200,540 L720,540Z', '#B7D8C0', .9)]
    s.layer('window', window(s, 720, 130, 480, 390, 'sky1', 'sky2', '#ffffff', inner), 'pop', .25)
    cu = [R(640, 92, 640, 14, 'head2', 7)]
    for side in (-1, 1):
        x = 720 if side < 0 else 1200
        cu.append(P(f'M{x - side * 70},100 L{x + side * 70},100 Q{x + side * 40},330 {x + side * 90},590 L{x - side * 40},590 Q{x - side * 60},330 {x - side * 70},100Z', 'curtain'))
        cu.append(S(f'M{x + side * 10},120 Q{x - side * 10},340 {x + side * 20},580', 'curtain2', 6, .6))
        cu.append(R(x + side * 30 - 30, 360, 60, 14, 'curtain2', 7))
    s.layer('curtains', cu, 'slide-l', .35)
    sl = [S('M40,60 Q480,140 960,70 Q1440,140 1880,60', 'head2', 2, .6)]
    for k in range(17):
        u = k / 16; x = 40 + u * 1840; y = 60 + 70 * math.sin(u * 2 * math.pi) ** 2 * .9 + 4
        pts = [(x + (14 if j % 2 == 0 else 6) * math.cos(-math.pi / 2 + j * math.pi / 5), y + 14 + (14 if j % 2 == 0 else 6) * math.sin(-math.pi / 2 + j * math.pi / 5)) for j in range(10)]
        sl += [poly(pts, 'star'), C(x, y + 14, 22, 'star', .3, 'filter="url(#b6)"')]
    s.layer('star_lights', sl, 'drop', .7, loop='twinkle')
    sh = [R(120, 300, 400, 14, 'head2', 6, extra='filter="url(#shs)"'), *books(150, 330, 300, ['book1', 'book2', 'book3'], 3), plant_pot(420, 300, .5, 'pot', 'leaf', 'leaf2'),
          R(250, 150, 140, 110, '#ffffff', 8, extra='filter="url(#shs)"'), R(262, 162, 116, 86, 'quilt', 4, .6), C(320, 205, 26, 'star')]
    s.layer('shelf', sh, 'pop', .45)
    bd = [shadow(380, 880, 330, 14, .16), R(60, 470, 70, 420, 'head', 30, extra='filter="url(#sh)"'), R(74, 486, 42, 380, 'head2', 20, .4),
          R(100, 690, 560, 110, 'bed', 20), R(110, 800, 24, 80, 'head2', 6), R(620, 800, 24, 80, 'head2', 6), R(90, 790, 580, 20, 'head', 8),
          R(140, 640, 140, 70, 'pillow', 30, extra='filter="url(#shs)"'), P('M250,690 Q260,650 330,650 L640,650 Q672,650 672,690 L672,790 L250,790Z', 'quilt', extra='filter="url(#shs)"'),
          R(250, 700, 422, 16, 'quilt2', 0, .5), *[C(320 + k * 80, 750, 8, '#ffffff', .6) for k in range(5)]]
    s.layer('bed', bd, 'rise', .5)
    ns = [shadow(735, 882, 80, 8), R(670, 720, 130, 160, 'ward', 10, extra='filter="url(#shs)"'), R(682, 760, 106, 50, 'ward2', 6), R(722, 780, 26, 8, 'knob', 4),
          R(728, 640, 14, 80, 'lampb', 4), P('M690,590 L780,590 L768,644 L702,644Z', 'lamp'), C(700, 706, 22, 'clock'), C(700, 706, 16, '#ffffff'), S('M700,706 L700,694 M700,706 L708,710', 'head2', 3),
          C(686, 688, 7, 'clock'), C(714, 688, 7, 'clock')]
    s.layer('nightstand', ns, 'pop', .6)
    s.layer('lamp_glow', [C(735, 620, 120, 'lamp', .45, 'filter="url(#b40)"')], 'fade', 1.0, loop='glow')
    wd = [shadow(1670, 882, 210, 12, .15), R(1480, 250, 380, 630, 'ward', 16, extra='filter="url(#sh)"'), R(1500, 270, 165, 590, 'ward2', 10, .45), R(1675, 270, 165, 590, 'ward2', 10, .45),
          R(1648, 520, 10, 60, 'knob', 5), R(1682, 520, 10, 60, 'knob', 5), R(1470, 236, 400, 20, 'head2', 8), R(1500, 210, 90, 26, 'book2', 6), R(1600, 200, 70, 36, 'book3', 8)]
    s.layer('wardrobe', wd, 'slide-r', .55)
    s.layer('floor', floor_planks(s, 800, 'floor1', 'floor2'), 'rise', .1)
    s.layer('rug', [E(1060, 960, 420, 70, 'rug'), E(1060, 960, 360, 54, 'rug2', .5), E(1060, 960, 300, 42, 'rug')], 'grow', .65)
    mb = [S('M1340,0 L1340,120', 'head2', 2), R(1270, 118, 140, 6, 'head2', 3), S('M1280,124 L1280,200 M1400,124 L1400,180 M1340,124 L1340,230', 'head2', 2),
          P('M1268,190 a20,20 0 1,0 26,26 a16,16 0 1,1 -26,-26Z', 'star'), poly([(1400 + 16 * math.cos(-math.pi / 2 + j * math.pi / 5) * (1 if j % 2 == 0 else .45), 196 + 16 * math.sin(-math.pi / 2 + j * math.pi / 5) * (1 if j % 2 == 0 else .45)) for j in range(10)], 'curtain'),
          C(1340, 246, 16, 'quilt')]
    s.layer('mobile', mb, 'drop', .8, loop='sway', origin='1340 0')
    tb = [shadow(1400, 882, 60, 8), C(1400, 836, 40, 'bear'), C(1400, 790, 30, 'bear'), C(1378, 766, 11, 'bear'), C(1422, 766, 11, 'bear'), C(1378, 766, 5, 'bear2'), C(1422, 766, 5, 'bear2'),
          E(1400, 798, 12, 9, '#F6E2CC'), C(1390, 786, 3, '#3A2A2A'), C(1410, 786, 3, '#3A2A2A'), C(1372, 864, 14, 'bear'), C(1428, 864, 14, 'bear'), R(1386, 812, 28, 8, 'curtain', 4)]
    s.layer('teddy', tb, 'pop', .9)
    return s


# ================= 074 晚餐餐桌 =================
def dinner():
    s = Scene('s074', '晚餐餐桌', '家庭生活', ['营养', '饮食习惯', '家庭', '餐桌礼仪'],
              dict(wall1='#E7EEDD', wall2='#D5E1C8', wains='#A9805F', wains2='#8E6849', floor1='#BC875D', floor2='#9E6D47', table='#C99260', table2='#A6733F',
                   cloth='#FFF8EE', runner='#F2B9A6', plate='#FFFFFF', plate2='#E8ECEF', fish='#F2A35E', fish2='#E08A45', veg='#6DB46F', veg2='#9AD18E', egg='#F7D35E', tom='#E8604F',
                   rice='#FFFDF6', bowl='#7FB8D8', bowl2='#5E9CC0', soup='#F4C56A', lamp='#FFD98A', shade='#E8835E', chair='#8E5B36', chair2='#744828', side='#B98A63', side2='#9A6E4A',
                   sky1='#3E4F82', sky2='#E9A48A', star='#FFF1C2', fruit1='#F28C2E', fruit2='#E8483B', fruit3='#F7D35E', frame='#FFFFFF', leaf='#5FA873', leaf2='#93CC8E', pot='#E9DFD0'),
              desc='傍晚的家庭餐桌：暖黄吊灯下摆着鱼、青菜、番茄炒蛋、米饭和冒热气的汤，窗外晚霞，右侧餐边柜。', stand={'ground_y': 960, 'x': [420, 1500]})
    s.layer('wall', [R(0, 0, W, 800, s.lg([(0, 'wall1'), (1, 'wall2')])), R(0, 580, W, 220, 'wains'), R(0, 580, W, 12, 'wains2'), *[R(x, 600, 4, 200, 'wains2', 0, .5) for x in range(60, W, 120)]], 'fade', 0)
    inner = [C(270, 400, 50, '#FFD9A0'), *[C(x, y, 3, 'star') for x, y in [(160, 190), (250, 160), (360, 210), (310, 250), (180, 260)]],
             *skyline(s, 110, 430, 520, 40, 140, ['#7A6D8E', '#8E7C9E'], 2, '#FFE3A3', .8)]
    s.layer('window', window(s, 110, 140, 320, 380, 'sky1', 'sky2', '#ffffff', inner), 'pop', .25)
    fr = [R(1480, 200, 160, 200, 'frame', 8, extra='filter="url(#shs)"'), R(1494, 214, 132, 172, 'egg', 4, .7), C(1560, 290, 34, 'tom', .8),
          R(1670, 240, 140, 120, 'frame', 8, extra='filter="url(#shs)"'), R(1682, 252, 116, 96, 'bowl', 4, .6), P('M1682,348 L1730,300 L1760,330 L1798,290 L1798,348Z', 'veg')]
    s.layer('frames', fr, 'pop', .4)
    sb = [shadow(1690, 862, 200, 10), R(1500, 600, 380, 260, 'side', 12, extra='filter="url(#sh)"'), R(1490, 590, 400, 22, 'side2', 8),
          R(1520, 640, 160, 200, 'side2', 8, .45), R(1700, 640, 160, 200, 'side2', 8, .45), C(1660, 740, 6, 'lamp'), C(1720, 740, 6, 'lamp'),
          E(1600, 580, 70, 14, 'bowl2'), C(1570, 566, 20, 'fruit1'), C(1606, 560, 22, 'fruit2'), C(1636, 568, 18, 'fruit3'), plant_pot(1800, 590, .7, 'pot', 'leaf', 'leaf2')]
    s.layer('sideboard', sb, 'slide-r', .5)
    s.layer('floor', floor_planks(s, 800, 'floor1', 'floor2'), 'rise', .1)
    ch = []
    for x in (700, 960, 1220):
        ch += [R(x - 70, 500, 140, 160, 'chair', 30, extra='filter="url(#shs)"'), R(x - 52, 518, 104, 110, 'chair2', 20, .5), *[R(x - 40 + k * 30, 530, 14, 100, 'chair', 7) for k in range(3)]]
    s.layer('chairs', ch, 'rise', .4)
    tb = [shadow(960, 910, 520, 18, .2), R(540, 760, 24, 150, 'table2', 6), R(1356, 760, 24, 150, 'table2', 6), R(500, 640, 920, 30, 'table', 10, extra='filter="url(#sh)"'),
          P('M500,660 L1420,660 L1420,770 Q1380,790 1340,770 Q1300,790 1260,770 Q1220,790 1180,770 Q1140,790 1100,770 Q1060,790 1020,770 Q980,790 940,770 Q900,790 860,770 Q820,790 780,770 Q740,790 700,770 Q660,790 620,770 Q580,790 540,770 Q520,780 500,770Z', 'cloth'),
          R(820, 660, 280, 120, 'runner', 0, .7), R(500, 650, 920, 14, 'cloth')]
    s.layer('table', tb, 'rise', .55)
    dz = []
    # 鱼
    dz += [E(960, 640, 120, 26, 'plate2'), E(960, 636, 112, 22, 'plate'), E(950, 630, 70, 20, 'fish'), poly([(1010, 630), (1040, 612), (1040, 648)], 'fish2'), C(905, 626, 3.5, '#3A2A2A'),
           S('M930,624 q8,8 0,14 M950,622 q8,8 0,16 M970,624 q8,8 0,14', 'fish2', 3), *[E(930 + k * 22, 616, 6, 2, 'veg') for k in range(3)]]
    # 青菜
    dz += [E(720, 640, 90, 22, 'plate2'), E(720, 636, 84, 18, 'plate')] + [E(690 + k * 20, 626 - (k % 2) * 6, 22, 9, 'veg' if k % 2 else 'veg2', extra=f'transform="rotate({(k - 1.5) * 18} {690 + k * 20} 626)"') for k in range(4)]
    # 番茄炒蛋
    dz += [E(1200, 640, 90, 22, 'plate2'), E(1200, 636, 84, 18, 'plate')] + [C(1170 + k * 16, 626 - (k % 2) * 6, 13, 'egg' if k % 2 == 0 else 'tom') for k in range(5)]
    # 米饭碗
    for x in (600, 830, 1090, 1320):
        dz += [P(f'M{x - 34},648 Q{x},700 {x + 34},648Z', 'bowl'), P(f'M{x - 30},650 Q{x},620 {x + 30},650Z', 'rice'), R(x - 36, 646, 72, 6, 'bowl2', 3),
               R(x + 40, 646, 40, 4, 'chair', 2, extra=f'transform="rotate(-10 {x + 40} 648)"'), R(x + 40, 654, 40, 4, 'chair', 2, extra=f'transform="rotate(-6 {x + 40} 656)"')]
    # 汤
    dz += [P('M1060,600 Q1060,650 1110,650 Q1160,650 1160,600Z', 'bowl2'), E(1110, 600, 50, 9, 'soup'), R(1050, 594, 120, 8, 'bowl2', 4, .0)]
    s.layer('dishes', dz, 'pop', .75)
    s.layer('steam', [S(f'M{x},588 q-12,-20 0,-40 q12,-20 0,-40', '#ffffff', 5, .7) for x in (1094, 1124, 940)], 'fade', 1.0, loop='flow')
    lp = [R(958, 0, 4, 250, 'chair2'), P('M880,330 Q880,250 960,250 Q1040,250 1040,330Z', 'shade', extra='filter="url(#shs)"'), E(960, 330, 80, 10, 'lamp'), C(960, 336, 16, '#FFF6D8')]
    s.layer('pendant', lp, 'drop', .6)
    s.layer('lamp_glow', [P('M884,334 L1036,334 L1300,660 L620,660Z', s.lg([(0, 'lamp', .45), (1, 'lamp', 0)])), C(960, 340, 110, 'lamp', .5, 'filter="url(#b40)"')], 'fade', 1.0, loop='glow')
    s.layer('plant', [plant_pot(240, 860, 1.4, 'pot', 'leaf', 'leaf2')], 'grow', .9, loop='sway', origin='240 860')
    return s


# ================= 075 洗漱台 =================
def bathroom():
    s = Scene('s075', '洗漱台', '家庭生活', ['卫生习惯', '刷牙洗手', '健康', '生活自理'],
              dict(wall1='#EEF8FB', tile='#D6EDF3', tile2='#BEE0EA', vanity='#F6F0E8', vanity2='#E3D9CC', counter='#FFFFFF', counter2='#E2E8EC', basin='#F8FBFC', mirror='#DDF1F7', mirror2='#BFE3EE',
                   frame='#E6B67A', frame2='#CF9D60', steel='#B8C2CB', towel='#F4A69C', towel2='#7FC8BA', cup1='#7FC4E8', cup2='#F7C55E', brush1='#F2836B', brush2='#5FB7B0', bubble='#FFFFFF',
                   leaf='#6FB57E', leaf2='#A6D99A', pot='#FFFFFF', floor1='#EDE6DC', floor2='#DDD3C6', stool='#7FC8BA', stool2='#62B0A2', light='#FFF5D6', water='#9ED8F0', soap='#F7B7C8', poster='#FFFFFF'),
              desc='清爽的洗漱台：圆镜与镜前灯、白色台盆和水龙头、两只牙刷杯和泡泡香皂，墙上毛巾架与洗手步骤图示，旁边儿童踏凳。', stand={'ground_y': 940, 'x': [560, 1360]})
    s.layer('wall', [R(0, 0, W, 860, 'wall1'), R(0, 440, W, 420, 'tile'), *tiles(0, 440, W, 860, 60, 'tile2', .9, 3), R(0, 432, W, 12, 'tile2')], 'fade', 0)
    s.layer('floor', [R(0, 860, W, 220, s.lg([(0, 'floor1'), (1, 'floor2')]))] + [R(x, 860, 3, 220, '#ffffff', 0, .5) for x in range(0, W, 120)] + [R(0, 960, W, 3, '#ffffff', 0, .5)], 'rise', .1)
    mr = [C(960, 300, 214, 'frame', extra='filter="url(#sh)"'), C(960, 300, 196, s.lg([(0, 'mirror'), (1, 'mirror2')])), P('M850,170 L900,140 L790,330 L770,290Z', '#ffffff', .5), P('M920,130 L940,124 L820,380 L810,350Z', '#ffffff', .35),
          C(960, 300, 204, 'frame2', .0)]
    s.layer('mirror', mr, 'pop', .3)
    s.layer('mirror_glint', [C(1060, 200, 8, '#ffffff', .9), C(1080, 230, 4, '#ffffff', .8), C(860, 400, 5, '#ffffff', .7)], 'fade', 1.2, loop='twinkle')
    lt = [R(800, 50, 320, 26, 'steel', 13), *[E(x, 80, 26, 10, 'light') for x in (860, 960, 1060)], E(960, 110, 260, 60, 'light', .5, 'filter="url(#b20)"')]
    s.layer('vanity_lights', lt, 'drop', .45, loop='glow')
    vn = [shadow(960, 864, 400, 12, .15), R(600, 620, 720, 240, 'vanity', 14, extra='filter="url(#sh)"'), R(620, 650, 330, 190, 'vanity2', 10, .5), R(970, 650, 330, 190, 'vanity2', 10, .5),
          R(920, 700, 12, 60, 'frame', 6), R(988, 700, 12, 60, 'frame', 6), R(580, 590, 760, 36, 'counter', 10, extra='filter="url(#shs)"'), R(580, 618, 760, 8, 'counter2')]
    s.layer('vanity', vn, 'rise', .2)
    bs = [E(960, 596, 150, 20, 'counter2'), E(960, 592, 140, 14, 'basin'), E(960, 594, 18, 5, 'steel'),
          R(952, 510, 16, 80, 'steel', 8), P('M960,516 Q960,490 990,490 L1040,490 L1040,506 L990,506 Q976,506 976,520Z', 'steel'), R(944, 520, 32, 12, 'steel', 6), R(944, 500, 10, 26, 'steel', 4)]
    bs += [P('M1032,520 Q1024,534 1032,540 Q1040,534 1032,520Z', 'water'), E(1032, 588, 16, 4, 'water', .6)]
    s.layer('basin', bs, 'pop', .5)
    cp = []
    for x, col, bcol in ((700, 'cup1', 'brush1'), (780, 'cup2', 'brush2')):
        cp += [R(x - 6, 470, 10, 90, bcol, 5, extra=f'transform="rotate(-8 {x} 560)"'), R(x - 10, 462, 18, 26, '#ffffff', 6, extra=f'transform="rotate(-8 {x} 560)"'),
               P(f'M{x - 30},520 L{x + 30},520 L{x + 24},592 L{x - 24},592Z', col, extra='filter="url(#shs)"'), R(x - 24, 540, 48, 6, '#ffffff', 3, .4)]
    cp += [R(830, 566, 70, 22, '#ffffff', 10, extra='filter="url(#shs)"'), R(830, 566, 24, 22, 'brush1', 8), R(896, 572, 10, 10, 'brush1', 3)]
    s.layer('cups', cp, 'pop', .6)
    sp = [R(1100, 480, 56, 110, 'towel2', 16, extra='filter="url(#shs)"'), R(1114, 452, 28, 30, 'steel', 6), R(1140, 456, 30, 10, 'steel', 4), R(1110, 520, 36, 30, '#ffffff', 6, .6),
          E(1230, 586, 60, 12, 'counter2'), R(1190, 556, 80, 30, 'soap', 14)]
    s.layer('soap', sp, 'pop', .7)
    s.layer('bubbles', [C(x, y, r_, 'bubble', .85, 'style="stroke:#BFE3EE;stroke-width:2"') for x, y, r_ in [(1200, 540, 12), (1226, 520, 9), (1250, 536, 14), (1240, 500, 7), (1270, 510, 10)]], 'fade', 1.1, loop='bob')
    tw = [R(170, 340, 360, 14, 'steel', 7, extra='filter="url(#shs)"'), C(170, 347, 12, 'steel'), C(530, 347, 12, 'steel'),
          R(200, 350, 140, 260, 'towel', 10, extra='filter="url(#shs)"'), R(200, 560, 140, 18, '#ffffff', 0, .5), R(200, 584, 140, 8, '#ffffff', 0, .4),
          R(360, 350, 140, 200, 'towel2', 10, extra='filter="url(#shs)"'), R(360, 500, 140, 16, '#ffffff', 0, .5)]
    s.layer('towels', tw, 'drop', .55, loop='sway', origin='350 347')
    sh = [R(1460, 260, 320, 14, 'frame2', 6, extra='filter="url(#shs)"'), plant_pot(1520, 260, .55, 'pot', 'leaf', 'leaf2'),
          R(1600, 190, 40, 70, 'cup1', 10), R(1610, 176, 20, 18, 'steel', 4), R(1660, 200, 44, 60, 'soap', 12), R(1720, 214, 36, 46, 'cup2', 10)]
    s.layer('shelf', sh, 'pop', .65)
    # 洗手步骤图示（3 格）
    po = [R(1460, 380, 320, 200, 'poster', 14, extra='filter="url(#shs)"')]
    for k in range(3):
        cx = 1520 + k * 100
        po += [R(cx - 42, 400, 84, 120, 'tile', 10, .7), C(cx - 46 + 92, 530, 0.1, 'tile')]
        if k == 0: po += [P(f'M{cx - 4},{420} Q{cx - 10},{436} {cx - 4},{442} Q{cx + 2},{436} {cx - 4},{420}Z', 'water'), P(f'M{cx + 10},{428} Q{cx + 4},{444} {cx + 10},{450} Q{cx + 16},{444} {cx + 10},{428}Z', 'water')]
        po += [P(f'M{cx - 26},{500} Q{cx - 30},{466} {cx - 8},{460} L{cx + 2},{460} L{cx + 2},{500}Z', 'towel'), P(f'M{cx + 26},{500} Q{cx + 30},{466} {cx + 8},{460} L{cx - 2},{460} L{cx - 2},{500}Z', 'frame')]
        if k == 1: po += [C(cx - 20, 452, 8, 'bubble', .9, 'style="stroke:#BFE3EE;stroke-width:2"'), C(cx + 22, 446, 6, 'bubble', .9, 'style="stroke:#BFE3EE;stroke-width:2"')]
        if k == 2: po += [P(f'M{cx - 12},{436} l8,8 l16,-18', 'none'), S(f'M{cx - 14},{440} L{cx - 4},{450} L{cx + 16},{428}', 'brush2', 6)]
        po.append(C(cx, 548, 12, ['cup1', 'cup2', 'brush2'][k]))
    po += [arrow(1562, 460, 14, 'frame2', 1, 4), arrow(1662, 460, 14, 'frame2', 1, 4)]
    s.layer('wash_steps', po, 'pop', .8)
    st = [shadow(1460, 864, 100, 8), R(1370, 770, 180, 30, 'stool', 10, extra='filter="url(#shs)"'), R(1380, 800, 20, 64, 'stool2', 4), R(1520, 800, 20, 64, 'stool2', 4), R(1390, 820, 140, 12, 'stool2', 4),
          C(1460, 785, 8, '#ffffff', .6)]
    s.layer('step_stool', st, 'rise', .85)
    return s


# ================= 076 阳台晾衣 =================
def balcony():
    s = Scene('s076', '阳台晾衣', '家庭生活', ['劳动', '家务', '阳光与健康', '家庭'],
              dict(sky1='#8FD0F2', sky2='#FFF0D6', sun='#FFD36E', city1='#C9DAEA', city2='#B5CADF', city3='#D9E3EE', tree='#8CCB8E', tree2='#B8E0A8', trunk='#8A5A3A',
                   wall='#F4E3D0', wall2='#E6CFB6', ceil='#FBF2E7', rail='#FFFFFF', rail2='#D7DEE4', floor1='#E8CBA6', floor2='#D5B48C', pole='#AEB7C0',
                   shirt1='#F28B6E', shirt2='#7FC4E8', shirt3='#F7D35E', towel='#8ED0B0', sock='#C9A6E8', dress='#F4A9C0', basket='#D9A86B', basket2='#BD8C52', pot='#E8835E', pot2='#D06C49',
                   leaf='#5FA873', leaf2='#9AD18E', flower='#F28BA0', flower2='#FFFFFF', can='#7FC4B8'),
              desc='阳光明媚的阳台：晾衣杆上挂着衬衫、裙子、毛巾和袜子随风轻摆，白色栏杆外是城市与树，花箱、脏衣篮和喷壶。', stand={'ground_y': 940, 'x': [560, 1360]})
    s.layer('sky', [R(0, 0, W, 860, s.lg([(0, 'sky1'), (1, 'sky2')])), C(1500, 250, 170, 'sun', .3, 'filter="url(#b40)"'), C(1500, 250, 70, 'sun')], 'fade', 0)
    s.layer('clouds', [cloud(500, 260, .7, op=.9), cloud(1200, 200, .5, op=.8), cloud(1760, 330, .45, op=.85)], 'slide-l', .2, loop='drift')
    ct = skyline(s, 120, 1800, 680, 120, 300, ['city1', 'city2', 'city3'], 9)
    s.layer('city', ct, 'rise', .3)
    s.layer('trees', [blob_tree(x, 700, .7 + .12 * (k % 2), 'tree', 'tree2', 'trunk') for k, x in enumerate(range(200, 1800, 170))], 'grow', .4)
    fr = [R(0, 0, W, 70, 'ceil'), R(0, 64, W, 10, 'wall2'), R(0, 0, 130, 860, s.lg([(0, 'wall2'), (1, 'wall')], 0, 0, 1, 0)), R(1790, 0, 130, 860, s.lg([(0, 'wall'), (1, 'wall2')], 0, 0, 1, 0)),
          R(124, 70, 8, 790, 'wall2'), R(1788, 70, 8, 790, 'wall2')]
    s.layer('frame', fr, 'fade', .15)
    pl = [R(300, 74, 8, 70, 'pole'), R(1612, 74, 8, 70, 'pole'), R(260, 140, 1400, 12, 'pole', 6), R(260, 140, 1400, 4, '#ffffff', 2, .5)]
    s.layer('poles', pl, 'drop', .35)

    def hanger(x):
        return G([S(f'M{x},{146} q0,-10 8,-10', 'pole', 3), S(f'M{x - 60},{184} L{x},{156} L{x + 60},{184}', 'pole', 4)])

    def shirt(x, col, sc=1):
        return G([hanger(x), P(f'M{x - 60 * sc},{180} L{x - 22 * sc},{170} Q{x},{190} {x + 22 * sc},{170} L{x + 60 * sc},{180} L{x + 92 * sc},{240} L{x + 62 * sc},{258} L{x + 50 * sc},{232} L{x + 50 * sc},{180 + 200 * sc} L{x - 50 * sc},{180 + 200 * sc} L{x - 50 * sc},{232} L{x - 62 * sc},{258} L{x - 92 * sc},{240}Z', col, extra='filter="url(#shs)"'),
                  P(f'M{x - 22 * sc},{170} Q{x},{204} {x + 22 * sc},{170} Q{x},{190} {x - 22 * sc},{170}Z', '#ffffff', .5), *[C(x, 220 + k * 40 * sc, 4, '#ffffff', .8) for k in range(3)]])

    def dress(x, col):
        return G([hanger(x), P(f'M{x - 40},{180} L{x + 40},{180} L{x + 34},{260} L{x + 90},{420} L{x - 90},{420} L{x - 34},{260}Z', col, extra='filter="url(#shs)"'), R(x - 36, 254, 72, 12, '#ffffff', 6, .6),
                  S(f'M{x - 80},{400} Q{x},{420} {x + 80},{400}', '#ffffff', 4, .5)])

    def towel(x, col):
        return G([R(x - 70, 146, 140, 260, col, 8, extra='filter="url(#shs)"'), R(x - 70, 350, 140, 14, '#ffffff', 0, .5), R(x - 70, 372, 140, 6, '#ffffff', 0, .4), R(x - 70, 146, 140, 30, col, 8)])

    def sock(x, col):
        return G([R(x - 6, 142, 12, 22, 'basket2', 3), P(f'M{x - 14},{160} L{x + 14},{160} L{x + 14},{230} Q{x + 14},{250} {x + 34},{250} L{x + 40},{250} Q{x + 50},{262} {x + 38},{272} L{x + 6},{272} Q{x - 14},{272} {x - 14},{250}Z', col), R(x - 14, 160, 28, 14, '#ffffff', 3, .6)])
    cl = [shirt(420, 'shirt1'), dress(640, 'dress'), towel(840, 'towel'), sock(980, 'sock'), sock(1040, 'shirt3'), shirt(1220, 'shirt2', .8), towel(1420, 'shirt3'), shirt(1580, 'sock', .65)]
    s.layer('clothes', cl, 'drop', .5, loop='sway')
    rl = [R(130, 640, 1660, 26, 'rail', 10, extra='filter="url(#shs)"'), R(130, 820, 1660, 14, 'rail2', 6)]
    for x in range(160, 1790, 46): rl.append(R(x - 5, 666, 10, 160, 'rail', 4))
    rl += [R(130, 834, 1660, 26, 'wall2', 0)]
    s.layer('railing', rl, 'rise', .45)
    fb = []
    for x0 in (180, 1500):
        fb += [R(x0, 598, 240, 50, 'pot', 10, extra='filter="url(#shs)"'), R(x0, 598, 240, 12, 'pot2', 6)]
        for k in range(8):
            x = x0 + 20 + k * 28
            fb += [S(f'M{x},598 L{x + (k % 3 - 1) * 6},{560 - (k % 2) * 14}', 'leaf', 4), C(x + (k % 3 - 1) * 6, 556 - (k % 2) * 14, 11, 'flower' if k % 2 else 'shirt3'), C(x + (k % 3 - 1) * 6, 556 - (k % 2) * 14, 4, 'flower2')]
        fb += [E(x0 + 120, 594, 120, 14, 'leaf2', .8)]
    s.layer('flower_boxes', fb, 'grow', .7, loop='sway')
    s.layer('floor', [R(0, 860, W, 220, s.lg([(0, 'floor1'), (1, 'floor2')]))] + [R(x, 860, 3, 220, '#ffffff', 0, .4) for x in range(0, W, 160)] + [R(0, 940, W, 3, '#ffffff', 0, .35), R(0, 1030, W, 3, '#ffffff', 0, .3)], 'rise', .1)
    bk = [shadow(1600, 942, 130, 10), P('M1480,820 L1720,820 L1700,940 L1500,940Z', 'basket', extra='filter="url(#shs)"'), R(1470, 806, 260, 22, 'basket2', 10)]
    for k in range(5): bk.append(R(1500 + k * 44, 840, 8, 90, 'basket2', 4, .5))
    bk += [P('M1520,810 Q1560,770 1600,808Z', 'shirt2'), P('M1590,808 Q1630,760 1680,806Z', 'towel'), R(1530, 790, 60, 22, 'dress', 10, extra='transform="rotate(-12 1560 800)"')]
    s.layer('basket', bk, 'pop', .8)
    wc = [shadow(320, 942, 80, 8), R(260, 860, 120, 80, 'can', 18, extra='filter="url(#shs)"'), P('M376,880 L450,830 L458,840 L384,900Z', 'can'), E(456, 832, 12, 8, 'can'),
          S('M280,860 Q320,800 360,860', 'can', 8), plant_pot(150, 940, 1.1, 'pot', 'leaf', 'leaf2'), plant_pot(1790, 940, 1.0, 'pot2', 'leaf', 'leaf2')]
    s.layer('props', wc, 'pop', .9)
    s.layer('sun_patch', [E(960, 980, 520, 50, '#FFF6D8', .4, 'filter="url(#b40)"')], 'fade', 1.0, loop='glow')
    return s


# ================= 077 书房写作业 =================
def study():
    s = Scene('s077', '书房写作业', '家庭生活', ['学习习惯', '用眼卫生', '时间管理', '家庭'],
              dict(wall1='#F6EBDC', wall2='#EAD8C0', sky1='#2F416F', sky2='#6C7DB4', moon='#FFF1C2', star='#FFF6D6', desk='#CF9A64', desk2='#AC7645', lamp='#F2836B', lamp2='#D8664F',
                   glow='#FFE3A3', book1='#F28B6E', book2='#7FC4E8', book3='#F7C55E', book4='#8ED081', book5='#B9A2E8', cork='#DDB47E', cork2='#C99A60', note1='#FFF2A8', note2='#BDE6F5', note3='#F9C7C0', note4='#C9EBC0',
                   globe='#7FC4E8', globe2='#8ED081', chair='#5FB7B0', chair2='#4A9C95', floor1='#C9965F', floor2='#AC7A47', rug='#E9D1B0', rug2='#D9BB92', shelf='#B98A63', shelf2='#97693F', leaf='#5FA873', leaf2='#93CC8E', pot='#FFFFFF', paper='#FFFDF6'),
              desc='夜晚的书房：窗外月亮和星星，书桌上台灯洒下暖光，摊开的作业本、笔筒和地球仪，墙上软木板与计划表，右侧书架。', stand={'ground_y': 940, 'x': [900, 1400]})
    s.layer('wall', [R(0, 0, W, 800, s.lg([(0, 'wall1'), (1, 'wall2')])), *[R(x, 0, 2, 800, 'wall2', 0, .8) for x in range(0, W, 90)]], 'fade', 0)
    inner = [C(560, 230, 46, 'moon'), C(578, 220, 40, s.pal['sky1'] and 'sky1', .0), C(560, 230, 110, 'moon', .2, 'filter="url(#b40)"'),
             *skyline(s, 280, 740, 480, 40, 120, ['#3F5185', '#4A5D93'], 5, '#FFE3A3', .8)]
    s.layer('window', window(s, 300, 130, 420, 330, 'sky1', 'sky2', '#ffffff', inner, sill=True), 'pop', .25)
    s.layer('stars', [C(x, y, r_, 'star') for x, y, r_ in [(350, 180, 3), (420, 160, 2.5), (470, 210, 3.5), (650, 300, 2.5), (380, 270, 2.5), (680, 170, 3), (620, 360, 2)]], 'fade', .9, loop='twinkle')
    ck = [R(900, 150, 440, 300, 'cork2', 14, extra='filter="url(#sh)"'), R(914, 164, 412, 272, 'cork', 8)]
    for x, y, col, rot in [(940, 190, 'note1', -4), (1050, 184, 'note2', 3), (940, 320, 'note3', 2), (1060, 310, 'note4', -3)]:
        ck += [R(x, y, 90, 90, col, 4, extra=f'transform="rotate({rot} {x + 45} {y + 45})" filter="url(#shs)"'), C(x + 45, y + 8, 6, 'lamp'), R(x + 14, y + 36, 60, 5, '#000000', 2, .12), R(x + 14, y + 52, 46, 5, '#000000', 2, .12)]
    # 计划表：方格 + 勾
    ck += [R(1170, 184, 136, 236, 'paper', 6, extra='filter="url(#shs)"')]
    for r_ in range(5):
        for c_ in range(3):
            ck.append(R(1184 + c_ * 40, 210 + r_ * 40, 30, 30, ['book2', 'book3', 'book4'][c_], 5, .35))
            if (r_ + c_) % 2 == 0: ck.append(S(f'M{1190 + c_ * 40},{225 + r_ * 40} l6,7 l12,-14', 'lamp2', 4))
    s.layer('corkboard', ck, 'pop', .4)
    bs = [shadow(1640, 882, 210, 12, .15), R(1460, 200, 360, 680, 'shelf', 12, extra='filter="url(#sh)"')]
    for k in range(4):
        y = 220 + k * 160
        bs += [R(1476, y, 328, 144, 'shelf2', 6)] + books(1486, 1700 if k % 2 else 1790, y + 140, ['book1', 'book2', 'book3', 'book4', 'book5'], 20 + k, 90, 128)
    bs += [C(1750, 420, 30, 'globe'), R(1740, 680, 50, 40, 'book3', 6), plant_pot(1750, 524, .5, 'pot', 'leaf', 'leaf2')]
    s.layer('bookshelf', bs, 'slide-r', .5)
    s.layer('floor', floor_planks(s, 800, 'floor1', 'floor2'), 'rise', .1)
    s.layer('rug', [E(620, 970, 480, 70, 'rug'), E(620, 970, 420, 54, 'rug2', .5)], 'grow', .45)
    dk = [shadow(560, 884, 380, 14, .18), R(200, 620, 720, 34, 'desk', 10, extra='filter="url(#sh)"'), R(220, 654, 24, 226, 'desk2', 6), R(876, 654, 24, 226, 'desk2', 6),
          R(660, 654, 216, 150, 'desk2', 8), R(676, 670, 184, 56, 'desk', 6), R(676, 738, 184, 56, 'desk', 6), R(748, 692, 40, 10, 'shelf2', 5), R(748, 760, 40, 10, 'shelf2', 5)]
    s.layer('desk', dk, 'rise', .35)
    it = [P('M420,616 L520,600 L620,616 L620,622 L420,622Z', 'paper', extra='filter="url(#shs)"'), S('M520,602 L520,620', '#D9CDB8', 2),
          *[R(440 + k * 0, 606 + 0, 0, 0, 'paper') for k in range(0)], *[S(f'M{440},{608 + k * 3} L{510},{604 + k * 3}', '#9FB4C8', 1.2, .0) for k in range(1)],
          R(640, 600, 110, 22, 'book2', 4), R(646, 582, 100, 18, 'book1', 4), R(652, 566, 90, 16, 'book3', 4),
          P('M800,560 L840,560 L836,620 L804,620Z', 'chair'), R(806, 520, 6, 50, 'lamp2', 3, extra='transform="rotate(-8 809 545)"'), R(818, 516, 6, 56, 'book3', 3), R(828, 524, 6, 46, 'book2', 3, extra='transform="rotate(8 831 547)"'),
          R(560, 612, 70, 6, 'lamp2', 3, extra='transform="rotate(-12 595 615)"'),
          R(250, 600, 120, 18, 'cork2', 6), C(300, 560, 40, 'globe'), P('M282,540 Q300,530 316,548 Q306,566 288,560Z', 'globe2'), P('M300,584 Q320,574 330,590 Q314,600 300,594Z', 'globe2'), S('M300,518 a42,42 0 0,1 0,84', 'shelf2', 4), R(296, 598, 8, 8, 'shelf2')]
    s.layer('desk_items', it, 'pop', .6)
    lp = [E(420, 616, 50, 8, 'lamp2'), S('M420,612 L380,500 L470,430', 'lamp', 10), C(380, 500, 9, 'lamp2'), P('M450,410 L520,440 L500,480 L430,452Z', 'lamp', extra='filter="url(#shs)"'), E(480, 470, 30, 10, 'glow')]
    s.layer('desk_lamp', lp, 'drop', .7)
    s.layer('lamp_glow', [P('M466,462 L506,476 L640,620 L380,620Z', s.lg([(0, 'glow', .55), (1, 'glow', .1)])), C(480, 500, 160, 'glow', .3, 'filter="url(#b40)"')], 'fade', 1.0, loop='glow')
    chx = 520
    chs = [shadow(chx, 892, 120, 10, .2), R(chx - 110, 640, 220, 150, 'chair', 40, extra='filter="url(#shs)"'), R(chx - 90, 656, 180, 110, 'chair2', 30, .4), R(chx - 100, 780, 200, 30, 'chair2', 14),
           R(chx - 8, 810, 16, 50, '#7A8794'), R(chx - 70, 856, 140, 10, '#7A8794', 5), C(chx - 66, 872, 10, '#3A4552'), C(chx + 66, 872, 10, '#3A4552')]
    s.layer('chair', chs, 'rise', .8)
    s.layer('clock_plant', [plant_pot(1080, 880, 1.2, 'pot', 'leaf', 'leaf2')], 'grow', .9, loop='sway', origin='1080 880')
    return s


# ================= 078 玄关出门 =================
def entryway():
    s = Scene('s078', '玄关出门', '家庭生活', ['生活自理', '出门安全', '整理习惯', '家庭'],
              dict(wall1='#E7EFE9', wall2='#D6E3DA', door='#2F7480', door2='#25606B', knob='#E8B84A', frame='#F7F2EA', frame2='#E3D9CA', light='#FFF3CC', sky='#CDEBF7',
                   floor1='#C9A27A', floor2='#AF8760', tile='#EFE5D6', tile2='#DDD0BC', cab='#F4ECDF', cab2='#DED0BB', wood='#B98A63', wood2='#966843', bag='#F2836B', bag2='#D9654E',
                   coat='#F7C948', coat2='#E0AF2E', hat='#7FC4E8', umb1='#7FC4E8', umb2='#F28BA0', mat='#D98E5E', mat2='#C27648', shoe1='#5FB7B0', shoe2='#F28B6E', mirror='#DDEFF4', leaf='#5FA873', leaf2='#93CC8E', pot='#E9DFD0', board='#FFFFFF'),
              desc='玄关：墨绿色大门与侧窗透进晨光，鞋柜上放着钥匙盘，墙上挂书包、雨衣和帽子，伞桶、换鞋凳与“出门检查”图示板。', stand={'ground_y': 940, 'x': [560, 1360]})
    s.layer('wall', [R(0, 0, W, 860, s.lg([(0, 'wall1'), (1, 'wall2')])), R(0, 620, W, 240, 'wall2', 0, .5), R(0, 616, W, 8, 'frame2'), *[R(x, 624, 4, 236, 'frame2', 0, .6) for x in range(40, W, 80)]], 'fade', 0)
    fl = [R(0, 860, W, 220, s.lg([(0, 'floor1'), (1, 'floor2')])), *[S(f'M{x},860 L{x - 60},1080', 'floor2', 3, .4) for x in range(100, W + 100, 180)],
          R(700, 860, 520, 220, 'tile'), *[R(700 + k * 104, 860, 3, 220, 'tile2') for k in range(6)], R(700, 960, 520, 3, 'tile2'), R(700, 856, 520, 8, 'tile2')]
    s.layer('floor', fl, 'rise', .1)
    dr = [R(760, 200, 400, 666, 'frame', 10, extra='filter="url(#sh)"'), R(790, 230, 260, 636, 'door', 6), R(810, 260, 220, 260, 'door2', 8), R(810, 550, 220, 290, 'door2', 8),
          R(826, 276, 188, 228, 'door', 6), R(826, 566, 188, 258, 'door', 6), C(1020, 560, 14, 'knob'), R(1000, 554, 46, 12, 'knob', 6), C(920, 330, 8, '#1E3F45'), C(920, 330, 4, 'knob'),
          R(1070, 230, 70, 636, s.lg([(0, 'sky'), (1, '#F4FBFE')]), 4), R(1101, 230, 8, 636, 'frame'), *[R(1070, 330 + k * 150, 70, 6, 'frame') for k in range(4)]]
    s.layer('door', dr, 'rise', .3)
    s.layer('door_light', [P('M1070,866 L1140,866 L1320,1080 L1100,1080Z', 'light', .45), R(1060, 220, 90, 660, 'light', 20, .3, 'filter="url(#b20)"')], 'fade', .9, loop='glow')
    mr = [R(220, 200, 300, 340, 'wood', 150, extra='filter="url(#shs)"'), R(236, 216, 268, 308, 'mirror', 136), P('M300,250 L340,236 L260,420 L250,380Z', '#ffffff', .5), P('M360,240 L374,236 L290,460 L282,440Z', '#ffffff', .35)]
    s.layer('mirror', mr, 'pop', .4)
    sc = [shadow(370, 862, 260, 12, .16), R(130, 620, 480, 240, 'cab', 12, extra='filter="url(#sh)"'), R(120, 606, 500, 22, 'wood', 8)]
    for k in range(3): sc += [R(148 + k * 152, 646, 140, 196, 'cab2', 8, .55)] + [R(160 + k * 152, 660 + j * 22, 116, 4, 'cab2') for j in range(8)] + [R(210 + k * 152, 740, 20, 8, 'wood2', 4)]
    sc += [E(250, 600, 50, 12, 'umb1'), R(238, 586, 30, 8, 'knob', 3), C(268, 590, 7, 'knob'), plant_pot(540, 606, .6, 'pot', 'leaf', 'leaf2'),
           R(370, 546, 80, 60, '#ffffff', 6, extra='filter="url(#shs)"'), R(378, 554, 64, 44, 'coat', 3, .6), C(410, 576, 12, 'bag')]
    s.layer('shoe_cabinet', sc, 'slide-l', .45)
    hk = [R(1300, 300, 480, 30, 'wood', 10, extra='filter="url(#shs)"'), *[C(x, 330, 8, 'wood2') for x in (1360, 1480, 1620, 1730)]]
    hk += [R(1310, 330, 100, 220, 'coat', 30, extra='filter="url(#shs)"'), P('M1330,330 Q1360,300 1390,330 L1390,370 L1330,370Z', 'coat2'), R(1356, 360, 8, 180, 'coat2', 4, .6), *[C(1340, 400 + k * 40, 5, '#ffffff', .8) for k in range(3)]]
    hk += [S('M1450,330 Q1480,300 1510,330', 'bag2', 6), R(1420, 340, 120, 160, 'bag', 26, extra='filter="url(#shs)"'), R(1436, 410, 88, 70, 'bag2', 14), R(1460, 360, 40, 12, 'board', 6, .7),
           R(1436, 410, 88, 10, 'knob', 4)]
    hk += [P('M1580,350 Q1620,290 1660,350Z', 'hat'), E(1620, 352, 60, 10, 'hat'), R(1590, 340, 60, 8, 'umb2', 4)]
    hk += [S('M1730,330 L1730,400', 'wood2', 3), C(1730, 420, 22, 'shoe1'), R(1724, 440, 12, 30, 'shoe1', 4)]
    s.layer('hooks', hk, 'drop', .55, loop='sway')
    um = [shadow(1300, 864, 50, 8), R(1260, 740, 80, 124, 'umb1', 12, extra='filter="url(#shs)"'), R(1260, 740, 80, 14, '#5AA6CC', 6),
          P('M1272,740 L1286,600 L1300,740Z', 'umb2'), R(1284, 584, 4, 24, 'wood2', 2), P('M1300,740 L1316,620 L1332,740Z', 'coat'), S('M1316,620 q0,-16 10,-16', 'wood2', 4)]
    s.layer('umbrellas', um, 'pop', .7)
    bn = [shadow(1640, 864, 170, 10), R(1480, 740, 320, 30, 'wood', 10, extra='filter="url(#shs)"'), R(1500, 770, 20, 94, 'wood2', 4), R(1760, 770, 20, 94, 'wood2', 4), R(1500, 812, 280, 10, 'wood2', 4),
          R(1540, 700, 90, 44, 'umb2', 18), R(1550, 708, 70, 10, '#ffffff', 5, .5),
          P('M1530,864 L1600,864 Q1610,840 1590,836 L1550,836 Q1530,840 1530,864Z', 'shoe1'), P('M1610,864 L1680,864 Q1690,840 1670,836 L1630,836 Q1610,840 1610,864Z', 'shoe1'),
          P('M1700,808 L1750,808 Q1756,792 1742,790 L1712,790 Q1700,794 1700,808Z', 'shoe2'), P('M1752,808 L1790,808 Q1794,792 1784,790 L1760,790 Q1752,794 1752,808Z', 'shoe2')]
    s.layer('bench_shoes', bn, 'rise', .65)
    s.layer('doormat', [R(820, 870, 300, 50, 'mat', 14, extra='filter="url(#shs)"'), R(836, 880, 268, 30, 'mat2', 10, .6), *[R(850 + k * 24, 884, 10, 22, 'mat', 4, .7) for k in range(11)]], 'grow', .75)
    # 出门检查：钥匙 / 书包 / 水杯
    ck = [R(1180, 380, 100, 300, 'board', 12, extra='filter="url(#shs)"')]
    for k, y in enumerate((430, 520, 610)):
        ck += [R(1196, y - 34, 68, 68, 'wall1', 10)]
        if k == 0: ck += [C(1218, y, 12, 'knob'), C(1218, y, 5, 'wall1'), R(1228, y - 4, 26, 8, 'knob', 3), R(1246, y + 2, 6, 10, 'knob', 2)]
        if k == 1: ck += [R(1212, y - 18, 36, 40, 'bag', 10), R(1220, y, 20, 14, 'bag2', 4)]
        if k == 2: ck += [R(1220, y - 22, 20, 44, 'hat', 6), R(1222, y - 30, 16, 10, 'shoe1', 3)]
        ck += [C(1268, y - 26, 10, 'shoe1'), S(f'M{1262},{y - 26} l4,5 l8,-9', '#ffffff', 3)]
    s.layer('checklist', ck, 'pop', .85)
    s.layer('ceiling_lamp', [R(940, 0, 40, 30, 'frame2', 8), E(960, 40, 90, 22, 'board', extra='filter="url(#shs)"'), E(960, 60, 280, 60, 'light', .5, 'filter="url(#b40)"')], 'drop', .5)
    return s


# ================= 079 爷爷奶奶的小院 =================
def courtyard():
    s = Scene('s079', '爷爷奶奶的小院', '家庭生活', ['家庭', '孝亲敬老', '传统文化', '劳动'],
              dict(sky1='#9FD6F0', sky2='#FFF1D6', hill='#C3DEB9', hill2='#A9D0A0', wall='#F3EBDD', wall2='#DFD2BC', tile='#5F6A75', tile2='#7C8692', wood='#A8693E', wood2='#7E4A2A',
                   door='#BF4A34', door2='#9E3B28', lantern='#E5483C', gold='#F2C14E', persim='#F28C2E', leaf='#6FAE5E', leaf2='#9ACB7C', trunk='#7A5238', ground='#ECDAB8', ground2='#DCC59C',
                   stone='#CFC8BB', stone2='#B9B1A2', corn='#F7C948', chili='#D9413A', veg='#7DBE6A', veg2='#A8D88E', soil='#B98B5E', hen='#FFFFFF', comb='#E5483C', beak='#F2A33A', bamboo='#D9B676', bamboo2='#BF9858'),
              desc='爷爷奶奶的农家小院：灰瓦白墙、红木门和一对红灯笼，墙上挂玉米和辣椒，柿子树结满果，菜畦、竹摇椅和小鸡。', stand={'ground_y': 930, 'x': [560, 1360]})
    s.layer('sky', [R(0, 0, W, 720, s.lg([(0, 'sky1'), (1, 'sky2')]))], 'fade', 0)
    s.layer('clouds', [cloud(420, 120, .7, op=.9), cloud(1150, 80, .5, op=.85), cloud(1700, 150, .55, op=.8)], 'slide-l', .2, loop='drift')
    s.layer('hills', [P('M-20,420 Q300,260 620,380 Q900,280 1240,380 Q1560,270 1940,390 L1940,720 L-20,720Z', 'hill'),
                      P('M-20,470 Q400,380 800,450 Q1200,390 1940,460 L1940,720 L-20,720Z', 'hill2')], 'rise', .25)
    hs = [R(240, 360, 1300, 360, 'wall', 0, extra='filter="url(#sh)"'), R(240, 660, 1300, 60, 'wall2'), R(240, 360, 1300, 20, 'wall2', 0, .6)]
    hs += [P('M180,372 Q200,350 260,330 L1520,330 Q1580,350 1600,372 L1600,384 L180,384Z', 'tile'), P('M220,330 L300,250 L1480,250 L1560,330Z', 'tile2')]
    for x in range(310, 1480, 34): hs.append(R(x, 254, 10, 76, 'tile', 4, .55))
    hs += [R(280, 240, 1220, 18, 'tile', 8), P('M260,246 Q240,226 250,212 Q264,232 290,240Z', 'tile'), P('M1520,246 Q1540,226 1530,212 Q1516,232 1490,240Z', 'tile')]
    for x0 in (380, 1200):
        hs += [R(x0, 440, 200, 160, 'wood', 6), R(x0 + 10, 450, 180, 140, '#FBEFD6', 4)]
        for k in range(1, 4): hs += [R(x0 + 10 + k * 45 - 3, 450, 6, 140, 'wood'), R(x0 + 10, 450 + k * 35 - 3, 180, 6, 'wood')]
    s.layer('house', hs, 'rise', .3)
    dr = [R(800, 420, 280, 300, 'wood2', 6), R(814, 434, 124, 286, 'door', 4), R(942, 434, 124, 286, 'door', 4), C(924, 590, 8, 'gold'), C(956, 590, 8, 'gold'),
          *[C(840 + c_ * 36, 470 + r_ * 40, 5, 'gold', .9) for r_ in range(3) for c_ in range(3)], *[C(968 + c_ * 36, 470 + r_ * 40, 5, 'gold', .9) for r_ in range(3) for c_ in range(3)],
          R(760, 430, 30, 250, 'door', 4), R(1090, 430, 30, 250, 'door', 4), R(800, 400, 280, 26, 'door', 4), R(780, 716, 320, 16, 'stone2', 4)]
    s.layer('door', dr, 'rise', .4)
    ln = []
    for x in (720, 1160):
        ln += [S(f'M{x},384 L{x},420', 'wood2', 3), R(x - 16, 418, 32, 10, 'gold', 3), E(x, 460, 40, 36, 'lantern', extra='filter="url(#shs)"'), R(x - 16, 492, 32, 10, 'gold', 3),
               S(f'M{x},460 m-20,-30 q-10,30 0,60 M{x},430 L{x},490 M{x + 20},430 q10,30 0,60', 'door2', 2, .6), *[S(f'M{x - 8 + k * 8},502 L{x - 8 + k * 8},530', 'gold', 2) for k in range(3)]]
    s.layer('lanterns', ln, 'drop', .6, loop='sway')
    hg = []
    for k in range(4): hg += [E(640, 420 + k * 34, 18, 26, 'corn'), *[S(f'M{640 + j * 6 - 6},{404 + k * 34} L{640 + j * 6 - 6},{436 + k * 34}', '#E0AE2E', 1.5) for j in range(3)]]
    hg += [S('M640,390 L640,410', 'bamboo2', 3), P('M626,404 L640,392 L654,404Z', 'veg')]
    hg += [S('M1240,390 L1240,600', 'bamboo2', 2)]
    for k in range(10): hg.append(P(f'M{1240 + (8 if k % 2 else -8)},{400 + k * 20} q{(14 if k % 2 else -14)},10 {(4 if k % 2 else -4)},26Z', 'chili'))
    s.layer('hangings', hg, 'pop', .7)
    gd = [P('M0,720 L1920,720 L1920,1080 L0,1080Z', s.lg([(0, 'ground'), (1, 'ground2')]))]
    for k, (x, y) in enumerate([(940, 760), (900, 820), (960, 890), (920, 970), (980, 1050)]): gd += [E(x, y, 70 + k * 6, 20 + k * 2, 'stone'), E(x - 6, y - 4, 54 + k * 5, 12 + k, '#ffffff', .25)]
    s.layer('ground', gd, 'rise', .1)
    vp = [R(60, 780, 440, 130, 'soil', 20, extra='filter="url(#shs)"')]
    for r_ in range(3):
        for k in range(7):
            x = 100 + k * 58 + (r_ % 2) * 20; y = 812 + r_ * 36
            vp += [E(x - 10, y, 14, 7, 'veg', extra=f'transform="rotate(-30 {x - 10} {y})"'), E(x + 10, y, 14, 7, 'veg2', extra=f'transform="rotate(30 {x + 10} {y})"'), C(x, y - 6, 6, 'veg')]
    for x in range(50, 520, 30): vp += [R(x, 740, 10, 70, 'bamboo', 3)]
    vp += [R(40, 756, 480, 8, 'bamboo2', 3), R(40, 784, 480, 8, 'bamboo2', 3)]
    s.layer('veg_patch', vp, 'grow', .55)
    tr = [P('M1700,1000 C1720,860 1690,760 1740,620 L1790,630 C1750,760 1780,880 1770,1000Z', 'trunk'), S('M1745,700 C1690,640 1640,620 1600,560', 'trunk', 18), S('M1770,660 C1820,600 1850,560 1880,520', 'trunk', 14),
          C(1700, 430, 170, 'leaf'), C(1560, 500, 110, 'leaf'), C(1860, 470, 130, 'leaf'), C(1640, 360, 100, 'leaf2', .6), C(1800, 380, 90, 'leaf2', .5)]
    random.seed(21)
    for _ in range(18):
        a = random.uniform(0, 2 * math.pi); rr = random.uniform(40, 200); x = 1700 + rr * math.cos(a) * 1.1; y = 450 + rr * math.sin(a) * .7
        tr += [C(x, y, 16, 'persim'), R(x - 6, y - 18, 12, 6, 'leaf', 3), C(x - 5, y - 4, 4, '#ffffff', .4)]
    s.layer('persimmon_tree', tr, 'grow', .5, origin='1740 1000')
    rc = [shadow(1430, 880, 110, 10), S('M1350,880 Q1430,910 1510,880', 'bamboo2', 10), R(1360, 780, 140, 20, 'bamboo', 8), P('M1372,780 L1350,640 L1374,636 L1396,780Z', 'bamboo'),
          *[R(1356 + k * 7, 650 + k * 30, 30, 6, 'bamboo2', 3) for k in range(4)], R(1370, 800, 10, 76, 'bamboo2', 3), R(1480, 800, 10, 76, 'bamboo2', 3), R(1376, 760, 110, 22, 'lantern', 10, .8)]
    rc += [R(1540, 800, 100, 14, 'wood', 6), R(1584, 814, 12, 66, 'wood2'), R(1556, 872, 68, 8, 'wood2', 4), P('M1560,800 Q1560,770 1580,770 L1592,770 Q1600,800 1600,800Z', '#ffffff'), R(1606, 784, 22, 16, '#ffffff', 4)]
    s.layer('rocking_chair', rc, 'pop', .75)
    def hen(x, y, d=1, sc=1):
        return G([shadow(x, y + 30 * sc, 36 * sc, 6 * sc), E(x, y, 34 * sc, 26 * sc, 'hen'), P(f'M{x - d * 30 * sc},{y - 6 * sc} L{x - d * 50 * sc},{y - 26 * sc} L{x - d * 40 * sc},{y + 4 * sc}Z', 'hen'),
                  C(x + d * 26 * sc, y - 22 * sc, 14 * sc, 'hen'), P(f'M{x + d * 20 * sc},{y - 36 * sc} q{d * 4 * sc},{-10 * sc} {d * 8 * sc},0 q{d * 4 * sc},{-10 * sc} {d * 8 * sc},2Z', 'comb'),
                  poly([(x + d * 38 * sc, y - 24 * sc), (x + d * 48 * sc, y - 20 * sc), (x + d * 38 * sc, y - 16 * sc)], 'beak'), C(x + d * 30 * sc, y - 25 * sc, 2.4 * sc, '#3A2A2A'),
                  E(x - d * 4 * sc, y + 2 * sc, 16 * sc, 10 * sc, 'stone', .6), S(f'M{x - 6 * sc},{y + 24 * sc} L{x - 6 * sc},{y + 30 * sc} M{x + 6 * sc},{y + 24 * sc} L{x + 6 * sc},{y + 30 * sc}', 'beak', 3)])
    s.layer('chickens', [hen(1220, 860, -1), hen(1300, 900, 1, .7), C(1260, 920, 4, 'corn'), C(1240, 928, 4, 'corn'), C(1280, 930, 4, 'corn')], 'pop', .9, loop='bob')
    s.layer('well', [shadow(640, 860, 90, 10), R(570, 760, 140, 100, 'stone2', 14, extra='filter="url(#shs)"'), R(560, 750, 160, 20, 'stone', 8), *[R(580 + k * 34, 780, 26, 18, 'stone', 4, .7) for k in range(4)],
                     R(570, 650, 10, 104, 'wood2'), R(700, 650, 10, 104, 'wood2'), P('M552,660 L640,610 L728,660Z', 'tile'), R(600, 690, 80, 12, 'wood', 6), S('M640,702 L640,740', 'wood2', 2), R(628, 740, 24, 20, 'wood', 4)], 'rise', .65)
    return s


# ================= 080 生日派对 =================
def birthday():
    s = Scene('s080', '生日派对', '家庭生活', ['家庭', '感恩', '心理健康', '分享'],
              dict(wall1='#FFEAF0', wall2='#FAD5E0', stripe='#FFF4F7', floor1='#EBD0A9', floor2='#D9B98D', cloth='#FFFFFF', cloth2='#F7B7C8', cake1='#FFF2DE', cake2='#F7A8B8', cake3='#9ED6EC',
                   cream='#FFFFFF', berry='#E8483B', flame='#FFB547', b1='#F28BA0', b2='#7FC4E8', b3='#F7D35E', b4='#9ED89A', b5='#B9A2E8', gift1='#7FC4E8', gift2='#F7D35E', gift3='#B9A2E8', gift4='#9ED89A',
                   ribbon='#F2836B', fan1='#FFD6A5', fan2='#C9E7F5', fan3='#E5D8FA', string='#C9A6B4', plate='#FFFFFF', cup='#F7C55E'),
              desc='粉色生日派对：中央三层蛋糕点着蜡烛，墙上纸扇花与三角彩旗，两侧彩色气球束轻轻飘动，礼物盒、纸杯蛋糕和彩纸屑。', stand={'ground_y': 950, 'x': [520, 1400]})
    bg = [R(0, 0, W, 820, s.lg([(0, 'wall1'), (1, 'wall2')]))] + [R(x, 0, 40, 820, 'stripe', 0, .45) for x in range(0, W, 100)]
    s.layer('wall', bg, 'fade', 0)
    fn = []
    for x, y, r_, col, col2 in [(760, 260, 110, 'fan1', 'b3'), (1160, 260, 110, 'fan2', 'b2'), (960, 190, 80, 'fan3', 'b5'), (560, 350, 70, 'fan2', 'b2'), (1360, 350, 70, 'fan1', 'b3')]:
        fn.append(C(x, y, r_, col, extra='filter="url(#shs)"'))
        for k in range(24):
            a = k * math.pi / 12
            fn.append(S(f'M{x},{y} L{x + r_ * math.cos(a):.1f},{y + r_ * math.sin(a):.1f}', col2, 2, .35))
        fn.append(C(x, y, r_ * .22, col2))
    s.layer('paper_fans', fn, 'pop', .3)
    bt = [S('M0,40 Q480,140 960,50 Q1440,140 1920,40', 'string', 3)]
    cols = ['b1', 'b3', 'b2', 'b4', 'b5']
    for seg, (x0, x1, y0, y1) in enumerate([(0, 960, 40, 50), (960, 1920, 50, 40)]):
        for k in range(10):
            t = (k + .5) / 10; x = x0 + (x1 - x0) * t; y = (1 - t) ** 2 * y0 + 2 * t * (1 - t) * 140 + t ** 2 * y1 - 2
            bt.append(poly([(x - 24, y), (x + 24, y), (x, y + 48)], cols[(k + seg) % 5]))
    s.layer('bunting', bt, 'drop', .45, loop='sway')
    s.layer('floor', [R(0, 820, W, 260, s.lg([(0, 'floor1'), (1, 'floor2')]))] + [S(f'M{x},820 L{x - 70},1080', 'floor2', 3, .4) for x in range(100, W + 100, 180)], 'rise', .1)
    tb = [shadow(960, 884, 420, 14, .18), R(600, 640, 720, 24, 'cloth', 8, extra='filter="url(#sh)"')]
    d = 'M600,656 L1320,656 L1320,840 '
    for k in range(12): d += f'Q{1320 - k * 60 - 30},870 {1320 - (k + 1) * 60},840 '
    d += 'Z'
    tb += [P(d, 'cloth'), R(600, 656, 720, 40, 'cloth2', 0, .7)]
    for k in range(12): tb.append(P(f'M{600 + k * 60},696 Q{630 + k * 60},726 {660 + k * 60},696Z', 'cloth2', .7))
    s.layer('table', tb, 'rise', .4)
    ck = [E(960, 640, 210, 20, 'plate'), R(780, 540, 360, 100, 'cake2', 24, extra='filter="url(#shs)"'), R(830, 450, 260, 96, 'cake1', 22, extra='filter="url(#shs)"'), R(880, 380, 160, 76, 'cake3', 20, extra='filter="url(#shs)"')]
    for x0, x1, y in ((780, 1140, 540), (830, 1090, 450), (880, 1040, 380)):
        n = int((x1 - x0) / 40)
        dd = f'M{x0},{y + 12} '
        for k in range(n): dd += f'Q{x0 + k * 40 + 20},{y + 40} {x0 + (k + 1) * 40},{y + 12} '
        dd += f'L{x1},{y} L{x0},{y}Z'
        ck += [R(x0, y, x1 - x0, 18, 'cream', 9), P(dd, 'cream')]
    ck += [*[C(800 + k * 40, 600, 7, 'berry') for k in range(9)], *[C(860 + k * 50, 505, 8, 'b5') for k in range(5)]]
    for k, x in enumerate((910, 960, 1010)):
        ck += [R(x - 7, 320, 14, 60, ['b2', 'b3', 'b1'][k], 4), *[R(x - 7, 330 + j * 16, 14, 5, '#ffffff', 1, .7) for j in range(3)], S(f'M{x},320 L{x},312', '#5A4A3A', 2)]
    s.layer('cake', ck, 'pop', .6)
    s.layer('candle_glow', [*[P(f'M{x},282 Q{x - 12},302 {x},314 Q{x + 12},302 {x},282Z', 'flame') for x in (910, 960, 1010)], *[C(x, 300, 34, 'flame', .45, 'filter="url(#b20)"') for x in (910, 960, 1010)],
                            C(960, 320, 160, 'flame', .15, 'filter="url(#b40)"')], 'fade', 1.0, loop='glow')
    sd = []
    for x, col in ((680, 'b1'), (1240, 'b2')):
        sd += [P(f'M{x - 34},600 L{x + 34},600 L{x + 26},640 L{x - 26},640Z', col), C(x, 590, 30, 'cream'), C(x - 16, 596, 18, 'cream'), C(x + 16, 596, 18, 'cream'), C(x, 566, 7, 'berry')]
    for x, col in ((1170, 'b5'), (750, 'b4')):
        sd += [P(f'M{x - 30},636 L{x + 30},636 L{x},560Z', col), C(x, 556, 8, 'b3'), *[C(x - 14 + k * 14, 616 - k * 0, 4, '#ffffff') for k in range(3)]]
    s.layer('party_items', sd, 'pop', .75)

    def balloon(x, y, r_, col, sx, sy):
        return G([S(f'M{x},{y + r_ * 1.2} Q{(x + sx) / 2 + 20},{(y + sy) / 2} {sx},{sy}', 'string', 2), E(x, y, r_, r_ * 1.2, col, extra='filter="url(#shs)"'), poly([(x - 8, y + r_ * 1.2 + 10), (x + 8, y + r_ * 1.2 + 10), (x, y + r_ * 1.2 - 2)], col),
                  E(x - r_ * .35, y - r_ * .45, r_ * .2, r_ * .3, '#ffffff', .5)])
    bl = [balloon(180, 260, 70, 'b1', 290, 760), balloon(300, 200, 64, 'b2', 290, 760), balloon(240, 380, 60, 'b3', 290, 760), balloon(380, 330, 56, 'b5', 290, 760),
          balloon(1560, 220, 66, 'b4', 1640, 760), balloon(1700, 280, 72, 'b1', 1640, 760), balloon(1620, 380, 58, 'b2', 1640, 760), balloon(1780, 170, 54, 'b3', 1640, 760)]
    s.layer('balloons', bl, 'rise', .7, loop='bob')

    def gift(x, y, w, h, col, rib):
        return G([shadow(x + w / 2, y + h, w * .6, 8), R(x, y, w, h, col, 8, extra='filter="url(#shs)"'), R(x - 6, y - 4, w + 12, 26, col, 6), R(x - 6, y - 4, w + 12, 26, '#ffffff', 6, .25),
                  R(x + w / 2 - 9, y - 4, 18, h + 4, rib), R(x - 6, y + h * .5, w + 12, 0, rib),
                  P(f'M{x + w / 2},{y - 4} Q{x + w / 2 - 40},{y - 40} {x + w / 2 - 10},{y - 30}Z', rib), P(f'M{x + w / 2},{y - 4} Q{x + w / 2 + 40},{y - 40} {x + w / 2 + 10},{y - 30}Z', rib), C(x + w / 2, y - 6, 9, rib)])
    gf = [R(270, 760, 40, 0, 'b1'), gift(180, 760, 150, 120, 'gift1', 'ribbon'), gift(330, 800, 110, 80, 'gift2', 'b5'), gift(220, 680, 90, 80, 'gift3', 'b3'),
          gift(1500, 770, 160, 110, 'gift4', 'ribbon'), gift(1660, 790, 120, 90, 'gift3', 'b3'), gift(1560, 700, 80, 70, 'gift2', 'b1')]
    s.layer('gifts', gf, 'pop', .85)
    random.seed(30)
    cf = []
    for _ in range(46):
        x = random.uniform(40, 1880); y = random.uniform(120, 1060)
        if 560 < x < 1360 and y > 700: continue
        col = random.choice(cols)
        cf.append(R(x, y, 14, 7, col, 2, .9, f'transform="rotate({random.randint(0, 180)} {x:.0f} {y:.0f})"') if random.random() < .6 else C(x, y, 5, col, .9))
    s.layer('confetti', cf, 'fade', 1.1, loop='twinkle')
    return s


SCENES = [kitchen, bedroom, dinner, bathroom, balcony, study, entryway, courtyard, birthday]
