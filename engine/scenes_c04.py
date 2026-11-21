from core import *
import math, random

# ---------- 本模块小工具 ----------

def star(x, y, r, col, op=None, k=.45):
    pts = [(x + (r if j % 2 == 0 else r * k) * math.cos(-math.pi / 2 + j * math.pi / 5), y + (r if j % 2 == 0 else r * k) * math.sin(-math.pi / 2 + j * math.pi / 5)) for j in range(10)]
    return poly(pts, col, op)


def arc(cx, cy, r, a0, a1, col, w=4, op=1, dash=None):
    """圆弧（角度为度，SVG 坐标系：0°向右、顺时针为正）"""
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    large = 1 if abs(a1 - a0) > 180 else 0; sweep = 1 if a1 > a0 else 0
    ex = f'stroke-dasharray="{dash}"' if dash else ''
    return S(f'M{x0:.1f},{y0:.1f} A{r},{r} 0 {large},{sweep} {x1:.1f},{y1:.1f}', col, w, op, extra=ex)


def sector(cx, cy, r, a0, a1, col, op=None, extra=''):
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    large = 1 if (a1 - a0) > 180 else 0
    return P(f'M{cx:.1f},{cy:.1f} L{x0:.1f},{y0:.1f} A{r},{r} 0 {large},1 {x1:.1f},{y1:.1f}Z', col, op, extra)


def plant(x, y, sc, pot, leaf, leaf2):
    it = [E(x, y + 2, 46 * sc, 8 * sc, '#000000', .12), P(f'M{x - 36 * sc},{y - 70 * sc} L{x + 36 * sc},{y - 70 * sc} L{x + 28 * sc},{y} L{x - 28 * sc},{y}Z', pot)]
    for k, a in enumerate([-2.8, -2.35, -1.9, -1.45, -1.0, -.55, -3.25]):
        ex, ey = x + 52 * sc * math.cos(a), y - 108 * sc + 44 * sc * math.sin(a)
        it.append(E(ex, ey, 46 * sc, 15 * sc, leaf if k % 2 else leaf2, extra=f'transform="rotate({math.degrees(a):.0f} {ex:.0f} {ey:.0f})"'))
    return G(it)


# ============ s031 数学黑板 ============
def mathboard():
    s = Scene('s031', '数学黑板', '数学', ['数学', '几何', '数轴', '通用课堂'],
              dict(wall1='#E7F4EF', wall2='#CFE8DF', board='#2C5466', board2='#244657', frame='#C99462', frame2='#A6723F', chalk='#FFFFFF', cy='#FFE08A', cb='#9FE3FF', cp='#FFB3C1', cg='#B8F0B0',
                   wains='#9CCBB9', wains2='#7FB5A2', floor1='#D8B58C', floor2='#C29A6C', tri='#F7C55E', tri2='#E9A93A', prot='#7FC4E8', bead='#E8705A', bead2='#F2B33D', wood='#B57A4A', wood2='#8A5833',
                   leaf='#6DB585', leaf2='#A6D99A', pot='#F2836B', paper='#FFFDF6'),
              desc='数学课黑板：粉笔画出直角三角形、圆与半径、面积方格和 0–10 数轴；墙上挂三角板、量角器、圆规，右侧有算盘。', stand={'ground_y': 900, 'x': [600, 1320]})
    s.layer('wall', [R(0, 0, W, 780, s.lg([(0, 'wall1'), (1, 'wall2')])), R(0, 630, W, 150, 'wains'), R(0, 624, W, 12, 'wains2'), R(0, 768, W, 12, 'wains2'),
                     *[R(x, 650, 4, 110, 'wains2', 0, .5) for x in range(40, W, 80)]], 'fade', 0)
    fl = [R(0, 780, W, 300, s.lg([(0, 'floor1'), (1, 'floor2')]))] + [S(f'M0,{y} L{W},{y}', 'floor2', 3, .4) for y in (830, 900, 990)]
    s.layer('floor', fl, 'rise', .1)
    bx0, by0, bx1, by1 = 440, 110, 1480, 560
    bd = [R(bx0 - 20, by0 - 20, bx1 - bx0 + 40, by1 - by0 + 40, 'frame', 16, extra='filter="url(#sh)"'), R(bx0, by0, bx1 - bx0, by1 - by0, s.lg([(0, 'board'), (1, 'board2')]), 6),
          R(bx0 - 30, by1 + 10, bx1 - bx0 + 60, 22, 'frame2', 8), R(500, by1 + 2, 50, 10, 'chalk', 4), R(564, by1 + 2, 36, 10, 'cy', 4), R(612, by1 + 2, 36, 10, 'cp', 4), R(1360, by1, 74, 14, '#C9CED6', 5), R(1360, by1 - 4, 74, 6, '#8A939E', 3)]
    s.layer('board', bd, 'drop', .3)
    ch = []
    # 直角三角形 + 直角标记
    ax, ay = 510, 400
    ch += [S(f'M{ax},{ay} L{ax},{ay - 210} L{ax + 160},{ay}Z', 'chalk', 5, .9), S(f'M{ax},{ay - 24} L{ax + 24},{ay - 24} L{ax + 24},{ay}', 'cy', 4, .9),
           arc(ax + 160, ay, 40, 180, 180 + math.degrees(math.atan2(210, 160)), 'cp', 4, .9)]
    # 圆 + 圆心 + 半径
    ox, oy, r = 790, 280, 120
    ch += [S(f'M{ox - r},{oy} a{r},{r} 0 1,0 {2 * r},0 a{r},{r} 0 1,0 {-2 * r},0', 'chalk', 5, .9), C(ox, oy, 6, 'cy'), S(f'M{ox},{oy} L{ox + r * math.cos(-.6):.1f},{oy + r * math.sin(-.6):.1f}', 'cy', 4, .95),
           S(f'M{ox - r},{oy} L{ox + r},{oy}', 'cb', 3, .7, extra='stroke-dasharray="10 8"')]
    # 面积方格 5×3，涂 7 格
    gx, gy, cs = 1000, 190, 44
    for i in range(5):
        for j in range(3):
            if j * 5 + i < 7: ch.append(R(gx + i * cs + 3, gy + j * cs + 3, cs - 6, cs - 6, 'cg', 3, .45))
    for i in range(6): ch.append(S(f'M{gx + i * cs},{gy} L{gx + i * cs},{gy + 3 * cs}', 'chalk', 3, .8))
    for j in range(4): ch.append(S(f'M{gx},{gy + j * cs} L{gx + 5 * cs},{gy + j * cs}', 'chalk', 3, .8))
    # 运算符号
    for k, (x, y) in enumerate([(1320, 180), (1400, 180), (1320, 260), (1400, 260)]):
        col = ['cy', 'cb', 'cp', 'cg'][k]
        if k == 0: ch.append(S(f'M{x - 18},{y} L{x + 18},{y} M{x},{y - 18} L{x},{y + 18}', col, 6))
        if k == 1: ch.append(S(f'M{x - 18},{y} L{x + 18},{y}', col, 6))
        if k == 2: ch.append(S(f'M{x - 14},{y - 14} L{x + 14},{y + 14} M{x + 14},{y - 14} L{x - 14},{y + 14}', col, 6))
        if k == 3: ch += [S(f'M{x - 18},{y} L{x + 18},{y}', col, 6), C(x, y - 14, 4.5, col), C(x, y + 14, 4.5, col)]
    # 数轴 0–10
    nx0, nx1, ny = 520, 1420, 490
    ch.append(S(f'M{nx0 - 20},{ny} L{nx1 + 30},{ny}', 'chalk', 5, .9)); ch.append(S(f'M{nx1 + 14},{ny - 12} L{nx1 + 32},{ny} L{nx1 + 14},{ny + 12}', 'chalk', 5, .9))
    step = (nx1 - nx0) / 10
    for k in range(11):
        x = nx0 + k * step
        ch += [S(f'M{x:.1f},{ny - 12} L{x:.1f},{ny + 12}', 'chalk', 4, .9), T(f'{x:.1f}', ny + 44, str(k), 26, 'chalk', 700, extra='opacity=".85"')]
    for k in range(1, 4):
        xa, xb = nx0 + (k * 2 - 1) * step, nx0 + (k * 2 + 1) * step
        ch.append(S(f'M{xa:.1f},{ny - 16} Q{(xa + xb) / 2:.1f},{ny - 70} {xb:.1f},{ny - 16}', 'cp', 3.5, .9, extra='stroke-dasharray="8 7"'))
    ch.append(C(nx0 + 7 * step, ny, 8, 'cy'))
    s.layer('chalk', ch, 'fade', .6)
    # 左墙教具：45° 三角板、30°-60° 三角板、量角器、圆规
    tl = [R(80, 150, 300, 420, 'frame', 14, .25), *[C(100 + i * 40, 170 + j * 40, 3, 'frame2', .5) for i in range(7) for j in range(10)]]
    tl += [G([poly([(110, 330), (110, 180), (260, 330)], 'tri', .92), poly([(132, 308), (132, 236), (204, 308)], 'wall1'), S('M110,330 L110,180 L260,330Z', 'tri2', 3)], 'filter="url(#shs)"')]
    h = 140; w = h * math.sqrt(3)
    tl += [G([poly([(130, 560), (130 + w * .0, 560 - h), (130 + w, 560)], 'prot', .9), poly([(150, 544), (150, 560 - h + 46), (150 + (h - 62) * math.sqrt(3), 544)], 'wall1'),
              *[S(f'M{140 + k * 14},560 L{140 + k * 14},{552 if k % 5 else 544}', '#2C5466', 2, .7) for k in range(16)]], 'filter="url(#shs)"')]
    px, py, pr = 300, 300, 66
    prot = [P(f'M{px - pr},{py} A{pr},{pr} 0 0,1 {px + pr},{py}Z', 'paper', .95, 'filter="url(#shs)"'), S(f'M{px - pr},{py} A{pr},{pr} 0 0,1 {px + pr},{py}Z', 'prot', 3)]
    for d in range(0, 181, 10):
        a = math.radians(180 + d); r0 = pr * (.78 if d % 30 == 0 else .86)
        prot.append(S(f'M{px + r0 * math.cos(a):.1f},{py + r0 * math.sin(a):.1f} L{px + pr * math.cos(a):.1f},{py + pr * math.sin(a):.1f}', 'board', 2, .8))
    prot += [C(px, py, 4, 'bead'), P(f'M{px - 26},{py} A26,26 0 0,1 {px + 26},{py}Z', 'prot', .3)]
    tl.append(G(prot, f'transform="rotate(20 {px} {py})"'))
    s.layer('tools', tl, 'slide-l', .45)
    cmp = [C(300, 400, 10, 'wood2'), S('M300,400 L262,540', 'wood', 8), S('M300,400 L338,540', 'wood', 8), S('M262,540 L258,560', '#8A939E', 3), P('M332,536 L346,536 L339,560Z', 'bead2'), R(296, 380, 8, 20, 'wood2', 3)]
    s.layer('compass', cmp, 'drop', .7, loop='swing', origin='300 400')
    # 算盘（右墙）
    abx0, aby0, abw, abh = 1560, 200, 300, 230
    ab = [R(abx0, aby0, abw, abh, 'wood2', 12, extra='filter="url(#sh)"'), R(abx0 + 14, aby0 + 14, abw - 28, abh - 28, 'paper', 6, .55), R(abx0 + 14, aby0 + 76, abw - 28, 10, 'wood2')]
    num = [3, 1, 4, 1, 5, 9, 2]
    for k in range(7):
        x = abx0 + 34 + k * 39
        ab.append(R(x - 2, aby0 + 14, 4, abh - 28, 'wood', 2))
        d = num[k]; up = d >= 5; low = d % 5
        ab += [E(x, aby0 + 30, 16, 9, 'bead2'), E(x, aby0 + 66 if up else aby0 + 50, 16, 9, 'bead2')]
        for q in range(5):
            y = (aby0 + 98 + q * 19) if q < low else (aby0 + abh - 24 - (4 - q) * 19)
            ab.append(E(x, y, 16, 9, 'bead'))
    s.layer('abacus', ab, 'pop', .55)
    # 讲台（右前）+ 绿植（左前）
    pd = [E(1690, 900, 200, 16, '#000000', .14), R(1530, 690, 320, 210, 'frame', 12, extra='filter="url(#sh)"'), R(1510, 674, 360, 26, 'frame2', 8),
          R(1560, 720, 260, 150, 'frame2', 8, .35), R(1580, 650, 120, 24, 'cb', 4), R(1590, 632, 100, 18, 'cp', 4), R(1740, 640, 70, 34, 'paper', 6), R(1748, 646, 40, 4, 'board', 2, .5)]
    s.layer('podium', pd, 'rise', .75)
    s.layer('plant', [plant(150, 900, 1.3, 'pot', 'leaf', 'leaf2')], 'grow', .85, loop='sway', origin='150 900')
    s.layer('dust', [C(x, y, r_, '#ffffff', .7) for x, y, r_ in [(700, 520, 3), (760, 470, 2), (1180, 420, 3), (980, 150, 2), (1240, 520, 2)]], 'fade', 1.2, loop='twinkle')
    s.layer('light', [E(960, 330, 560, 220, '#ffffff', .12, 'filter="url(#b40)"')], 'fade', 1.0, loop='glow')
    return s


# ---------- 立体图形（平面斜二测风格） ----------
DX, DY = .5, .38  # 纵深方向偏移系数


def cuboid(x, y, w, h, d, c1, c2, c3):
    """x,y 为正面左下角；c1 正面 c2 顶面 c3 侧面"""
    dx, dy = d * DX, d * DY
    return G([poly([(x, y - h), (x + w, y - h), (x + w + dx, y - h - dy), (x + dx, y - h - dy)], c2),
              poly([(x + w, y), (x + w, y - h), (x + w + dx, y - h - dy), (x + w + dx, y - dy)], c3),
              R(x, y - h, w, h, c1), S(f'M{x},{y} L{x},{y - h} L{x + w},{y - h} L{x + w},{y}Z', '#ffffff', 2, .25)])


def cylinder(cx, y, r, h, c1, c2, c3):
    ry = r * .32
    return G([R(cx - r, y - h, 2 * r, h, c1), P(f'M{cx - r},{y} A{r},{ry} 0 0,0 {cx + r},{y}Z', c1), P(f'M{cx + r * .35},{y - h} L{cx + r},{y - h} L{cx + r},{y} A{r},{ry} 0 0,1 {cx + r * .35},{y + ry * .94}Z', c3, .55),
              E(cx, y - h, r, ry, c2)])


def cone(cx, y, r, h, c1, c3):
    ry = r * .32
    return G([P(f'M{cx - r},{y} L{cx},{y - h} L{cx + r},{y} A{r},{ry} 0 0,1 {cx - r},{y}Z', c1), P(f'M{cx},{y - h} L{cx + r},{y} A{r},{ry} 0 0,1 {cx + r * .3},{y + ry * .95}Z', c3, .55)])


def sphere(cx, cy, r, c1, c3):
    return G([C(cx, cy, r, c1), P(f'M{cx + r * .2},{cy - r * .98} A{r},{r} 0 0,1 {cx + r * .2},{cy + r * .98} A{r * .9},{r} 0 0,0 {cx + r * .2},{cy - r * .98}Z', c3, .45),
              C(cx - r * .35, cy - r * .35, r * .22, '#ffffff', .55)])


def pyramid(x, y, s_, h, c1, c3):
    dx, dy = s_ * DX, s_ * DY
    apex = (x + s_ / 2 + dx / 2, y - h)
    return G([poly([(x + s_, y), (x + s_ + dx, y - dy), apex], c3), poly([(x, y), (x + s_, y), apex], c1)])


def prism(x, y, s_, h, d, c1, c2, c3):
    dx, dy = d * DX, d * DY
    return G([poly([(x + s_ / 2, y - h), (x + s_, y), (x + s_ + dx, y - dy), (x + s_ / 2 + dx, y - h - dy)], c3), poly([(x, y), (x + s_, y), (x + s_ / 2, y - h)], c1)])


# ============ s033 积木几何台 ============
def blocks():
    s = Scene('s033', '积木几何台', '数学', ['数学', '几何', '立体图形', '空间'],
              dict(wall1='#FFF4DA', wall2='#FBE3B9', pat='#F6D9A4', shelf='#E7B479', shelf2='#C98F55', mat1='#F7B7A3', mat2='#A8DCC9', mat3='#FFE08A', mat4='#B9C8F2',
                   r1='#F27C66', r2='#F7A593', r3='#D45E4B', b1='#5FA8E0', b2='#93C8F0', b3='#3F86C2', g1='#6CC59A', g2='#A3E0C0', g3='#4BA37A', y1='#F7C44E', y2='#FFE08A', y3='#D9A12E',
                   p1='#9B85E0', p2='#C2B4F2', p3='#7A64C2', board='#FFFFFF', table='#F2C38C', table2='#D19A60', leaf='#6DB585', leaf2='#A6D99A'),
              desc='明亮的积木角：墙上平面图形挂板，书架与桌上摆着正方体、长方体、圆柱、圆锥、球、棱锥和三棱柱，还有积木城堡。', stand={'ground_y': 900, 'x': [580, 1340]})
    bg = [R(0, 0, W, 790, s.lg([(0, 'wall1'), (1, 'wall2')]))]
    random.seed(2)
    for k in range(40):
        x, y = random.uniform(0, W), random.uniform(20, 760); t = k % 3; sz = random.uniform(10, 18)
        if t == 0: bg.append(C(x, y, sz, 'pat', .55))
        elif t == 1: bg.append(R(x - sz, y - sz, 2 * sz, 2 * sz, 'pat', 4, .55, f'transform="rotate(20 {x:.0f} {y:.0f})"'))
        else: bg.append(poly([(x - sz, y + sz * .8), (x + sz, y + sz * .8), (x, y - sz)], 'pat', .55))
    s.layer('wall', bg, 'fade', 0)
    # 地垫
    fl = [R(0, 790, W, 290, 'mat2')]
    cols = ['mat1', 'mat2', 'mat3', 'mat4']
    for i, x in enumerate(range(0, W, 160)):
        for j, y in enumerate((790, 890, 990)):
            fl.append(R(x + 2, y + 2, 156, 96, cols[(i + j) % 4], 6, .9))
            fl.append(P(f'M{x + 64},{y + 2} q16,-12 32,0Z', cols[(i + j + 1) % 4], .9))
    s.layer('floor', fl, 'rise', .1)
    # 平面图形挂板
    px0, py0 = 600, 110
    pb = [R(px0, py0, 720, 340, 'board', 22, extra='filter="url(#sh)"'), R(px0, py0, 720, 46, 'y1', 22), R(px0, py0 + 24, 720, 22, 'y1')]
    for k in range(10): pb.append(C(px0 + 40 + k * 71, py0 + 23, 6, 'board', .8))
    cy_ = 290
    pb += [C(690, cy_, 60, 'r1'), R(780, cy_ - 56, 112, 112, 'b1', 6), poly([(920, cy_ + 56), (1040, cy_ + 56), (980, cy_ - 60)], 'g1'),
           poly([(1100, cy_), (1150, cy_ - 62), (1200, cy_), (1150, cy_ + 62)], 'p1')]
    hx, hy, hr = 1260, cy_, 48
    pb.append(poly([(hx + hr * math.cos(k * math.pi / 3), hy + hr * math.sin(k * math.pi / 3)) for k in range(6)], 'y3'))
    pb += [R(660, 384, 600, 40, 'wall1', 12), *[C(700 + k * 104, 404, 8, ['r1', 'b1', 'g1', 'p1', 'y3', 'r2'][k]) for k in range(6)]]
    s.layer('shape_board', pb, 'drop', .3)
    # 左：三层书架摆立体图形
    sx0, sx1 = 60, 500
    sh = [R(sx0, 300, sx1 - sx0, 560, 'shelf', 14, extra='filter="url(#sh)"')]
    for k, y in enumerate((470, 650, 830)):
        sh += [R(sx0 + 16, y - 160, sx1 - sx0 - 32, 160, 'shelf2', 6, .45), R(sx0 + 6, y, sx1 - sx0 - 12, 18, 'shelf2', 4)]
    sh += [cuboid(90, 470, 90, 90, 90, 'r1', 'r2', 'r3'), cylinder(270, 470, 46, 110, 'b1', 'b2', 'b3'), cone(400, 470, 50, 130, 'g1', 'g3'),
           sphere(130, 606, 44, 'y1', 'y3'), pyramid(210, 650, 100, 130, 'p1', 'p3'), cuboid(360, 650, 100, 60, 50, 'b1', 'b2', 'b3'),
           prism(90, 830, 120, 100, 70, 'g1', 'g2', 'g3'), cylinder(310, 830, 30, 140, 'r1', 'r2', 'r3'), cuboid(380, 830, 60, 60, 60, 'y1', 'y2', 'y3')]
    s.layer('shelf', sh, 'slide-l', .45)
    # 右：桌上积木城堡
    tx0, tx1, ty = 1420, 1880, 740
    tb = [E((tx0 + tx1) / 2, 905, 260, 16, '#000000', .14), R(tx0 + 20, ty, 26, 160, 'table2', 6), R(tx1 - 46, ty, 26, 160, 'table2', 6), R(tx0, ty - 24, tx1 - tx0, 30, 'table', 10, extra='filter="url(#shs)"')]
    base = ty - 24
    cs = [cuboid(1450, base, 340, 70, 60, 'b1', 'b2', 'b3'), cylinder(1490, base - 70, 34, 120, 'r1', 'r2', 'r3'), cylinder(1740, base - 70, 34, 120, 'r1', 'r2', 'r3'),
          cuboid(1540, base - 70, 160, 100, 50, 'y1', 'y2', 'y3'), R(1600, base - 140, 40, 70, 'y3', 20), cone(1490, base - 190, 44, 90, 'p1', 'p3'), cone(1740, base - 190, 44, 90, 'p1', 'p3'),
          prism(1540, base - 170, 160, 90, 50, 'g1', 'g2', 'g3'), sphere(1840, base - 30, 30, 'r1', 'r3')]
    s.layer('table', tb, 'rise', .55)
    s.layer('castle', cs, 'pop', .7)
    # 地上散落积木
    fb = [cuboid(560, 900, 70, 70, 70, 'r1', 'r2', 'r3'), cylinder(1360, 906, 36, 60, 'g1', 'g2', 'g3'), prism(1250, 920, 90, 70, 50, 'y1', 'y2', 'y3'), sphere(660, 886, 26, 'b1', 'b3')]
    s.layer('floor_blocks', fb, 'pop', .85)
    s.layer('plant', [plant(1860, 640, .8, 'r1', 'leaf', 'leaf2')], 'grow', .9, loop='sway', origin='1860 640')
    fl_ = [G([C(560, 220, 28, 'r2', .9)]), G([R(1360, 170, 50, 50, 'b2', 8, .9)]), G([poly([(1400, 560), (1460, 560), (1430, 508)], 'g2', .9)]), G([star(530, 520, 28, 'y1', .9)])]
    s.layer('floating', fl_, 'pop', 1.0, loop='bob')
    return s


# ============ s034 测量操场 ============
def measure():
    s = Scene('s034', '测量操场', '数学', ['数学', '测量', '长度单位', '户外'],
              dict(sky1='#86CDF2', sky2='#E6F6FF', sun='#FFD36E', school='#F6D7B8', school2='#E9BE95', roof='#E2765E', win='#A9D6F2', fence='#FFFFFF', fence2='#D9E3EA',
                   tree='#5FAE74', tree2='#9AD48B', trunk='#8A5A3A', grass1='#9FD27E', grass2='#7DBE5F', grass3='#B6E09A', tape='#F7C94A', tape2='#E2A92A', tick='#3A3A3A',
                   cone='#F2784B', cone2='#FFFFFF', wheel='#3F7FC2', metal='#8C98A4', flag1='#E85D4F', flag2='#3FA7D6', ruler='#F4E3B5', shadow='#5E8F4A'),
              desc='晴朗操场上拉开一条 0–10 米卷尺（刻度精确），旁边有测距轮、米尺、标志桶和测影子的立竿，适合长度测量课。', stand={'ground_y': 880, 'x': [300, 1600]})
    s.layer('sky', [R(0, 0, W, 760, s.lg([(0, 'sky1'), (1, 'sky2')])), C(1640, 170, 160, 'sun', .3, 'filter="url(#b40)"'), C(1640, 170, 64, 'sun')], 'fade', 0, loop=None)
    s.layer('clouds', [cloud(320, 150, .8, op=.9), cloud(980, 100, .55, op=.8), cloud(1320, 220, .5, op=.85)], 'slide-l', .2, loop='drift')
    # 教学楼
    sb = [R(500, 330, 920, 300, 'school', extra='filter="url(#shs)"'), R(480, 314, 960, 22, 'roof', 6), R(860, 250, 200, 90, 'school2', 4), P('M840,252 L960,200 L1080,252Z', 'roof'),
          C(960, 295, 26, 'fence'), S('M960,295 L960,278 M960,295 L972,302', 'tick', 3)]
    for row in range(3):
        for k in range(10):
            sb.append(R(530 + k * 90, 360 + row * 80, 56, 48, 'win', 4, .9))
    sb.append(R(900, 540, 120, 90, 'school2', 4))
    s.layer('school', [G(sb, 'opacity=".9"')], 'rise', .25)
    s.layer('trees', [blob_tree(x, 660, .75 + .12 * (k % 2), 'tree', 'tree2', 'trunk') for k, x in enumerate((80, 260, 1560, 1760, 1900))], 'grow', .4, loop='sway')
    fc = [R(0, 600, W, 8, 'fence'), R(0, 640, W, 8, 'fence')] + [R(x, 584, 10, 76, 'fence', 3) for x in range(10, W, 50)]
    s.layer('fence', fc, 'rise', .35)
    gr = [R(0, 660, W, 420, s.lg([(0, 'grass1'), (1, 'grass2')]))] + [R(x, 660, 120, 420, 'grass3', 0, .25) for x in range(0, W, 240)]
    s.layer('grass', gr, 'rise', .1)
    # 立竿测影（左）
    gx = 230
    sh = [P(f'M{gx},800 L{gx + 260},818 L{gx + 260},826 L{gx},812Z', 'shadow', .45), R(gx - 5, 620, 10, 186, 'trunk', 4), C(gx, 618, 9, 'flag1'),
          E(gx, 806, 24, 7, 'trunk')]
    s.layer('gnomon', sh, 'grow', .5, origin=f'{gx} 806')
    # 米尺倚在栅栏上
    mr = [G([R(0, 0, 24, 240, 'ruler', 3, extra='filter="url(#shs)"'), *[R(0, 240 - k * 24, 10 if k % 5 else 18, 3, 'tick') for k in range(1, 10)], R(0, 0, 24, 20, 'flag1', 3)], 'transform="translate(1180,610) rotate(-8)"')]
    s.layer('meter_stick', mr, 'pop', .6)
    # 卷尺：0–10 m
    tx0, tx1, ty = 200, 1700, 868
    unit = (tx1 - tx0) / 10
    tp = [R(tx0 - 20, ty - 4, tx1 - tx0 + 40, 40, '#000000', 6, .12), R(tx0, ty - 14, tx1 - tx0, 36, s.lg([(0, 'tape'), (1, 'tape2')]), 3)]
    for k in range(101):
        x = tx0 + k * unit / 10
        hh = 22 if k % 10 == 0 else (14 if k % 5 == 0 else 8)
        tp.append(R(x - 1, ty - 14, 2.2 if k % 10 else 3, hh, 'tick'))
    for k in range(11):
        tp.append(T(f'{tx0 + k * unit + (12 if k == 0 else 0):.1f}', ty + 18, str(k), 18, 'tick', 800))
    # 卷尺盒
    tp += [C(tx0 - 40, ty + 2, 56, 'flag1', extra='filter="url(#shs)"'), C(tx0 - 40, ty + 2, 36, '#ffffff', .9), C(tx0 - 40, ty + 2, 14, 'flag1'), R(tx0 - 24, ty - 30, 40, 60, 'flag1', 8),
           R(tx1 - 4, ty - 22, 12, 52, 'metal', 3), R(tx1 + 6, ty + 6, 20, 30, 'metal', 2)]
    s.layer('tape', tp, 'slide-r', .5)
    # 标志桶（0、5、10 米）
    cn = []
    for k in (0, 5, 10):
        x = tx0 + k * unit
        cn += [E(x, 834, 34, 8, '#000000', .15), R(x - 34, 826, 68, 10, 'cone', 3), P(f'M{x - 26},828 L{x - 8},752 L{x + 8},752 L{x + 26},828Z', 'cone'), P(f'M{x - 20},806 L{x + 20},806 L{x + 16},790 L{x - 16},790Z', 'cone2')]
    s.layer('cones', cn, 'pop', .7)
    # 测距轮（右）
    wx, wy = 1820, 820
    wh = [E(wx, wy + 52, 60, 10, '#000000', .15), C(wx, wy, 52, 'wheel', extra='filter="url(#shs)"'), C(wx, wy, 38, '#ffffff', .9), C(wx, wy, 8, 'wheel')]
    for k in range(12):
        a = k * math.pi / 6; wh.append(S(f'M{wx + 30 * math.cos(a):.1f},{wy + 30 * math.sin(a):.1f} L{wx + 38 * math.cos(a):.1f},{wy + 38 * math.sin(a):.1f}', 'tick', 2))
    wh += [S(f'M{wx},{wy} L{wx - 90},{wy - 230}', 'metal', 8), R(wx - 118, wy - 262, 60, 30, 'wheel', 8), R(wx - 108, wy - 254, 34, 14, '#C9F2D8', 3), S(f'M{wx - 110},{wy - 230} L{wx - 140},{wy - 250}', 'tick', 8)]
    s.layer('wheel', wh, 'slide-r', .8)
    # 小旗
    fg = []
    for x, col in ((tx0, 'flag1'), (tx1, 'flag2')):
        fg += [R(x - 2, 690, 4, 140, 'metal'), P(f'M{x + 2},694 L{x + 62},712 L{x + 2},732Z', col)]
    s.layer('flags', fg, 'drop', .9, loop='sway')
    return s


# ============ s035 统计展板 ============
def stats():
    s = Scene('s035', '统计展板', '数学', ['数学', '统计', '图表', '数据'],
              dict(wall1='#E6F0FA', wall2='#D2E2F3', board='#FFFFFF', frame='#5C7FA8', cork='#E3BE8C', cork2='#D1A774', grid='#DCE6F0', axis='#3D4B5C',
                   c1='#F27C66', c2='#F7C44E', c3='#6CC59A', c4='#5FA8E0', c5='#9B85E0', pin='#E8574A', note1='#FFF0A0', note2='#FFD1DC', note3='#C9F2D8',
                   floor1='#C8D2DE', floor2='#B0BCCB', easel='#B57A4A', paper='#FFFDF6', leaf='#6DB585', leaf2='#A6D99A', pot='#5FA8E0'),
              desc='数据统计展示墙：中央条形统计图、左侧扇形图与便利贴、右侧折线图和计数符号，前方画架上是象形统计图。', stand={'ground_y': 900, 'x': [600, 1320]})
    s.layer('wall', [R(0, 0, W, 790, s.lg([(0, 'wall1'), (1, 'wall2')])), *[R(0, y, W, 2, 'wall2', 0, .6) for y in range(60, 790, 60)], R(0, 760, W, 30, 'frame', 0, .25)], 'fade', 0)
    s.layer('floor', [R(0, 790, W, 290, s.lg([(0, 'floor1'), (1, 'floor2')])), *[R(x, 790, 3, 290, 'floor2', 0, .5) for x in range(0, W, 160)]], 'rise', .1)
    # 中央条形图
    bx0, by0, bw, bh = 600, 110, 720, 460
    cb = [R(bx0 - 14, by0 - 14, bw + 28, bh + 28, 'frame', 18, extra='filter="url(#sh)"'), R(bx0, by0, bw, bh, 'board', 10)]
    ox, oy, top = bx0 + 90, by0 + bh - 60, by0 + 60
    unit = (oy - top) / 8
    for k in range(9):
        y = oy - k * unit
        cb.append(R(ox, y - 1, bw - 140, 2, 'grid')); cb.append(T(ox - 22, y + 8, str(k), 22, 'axis', 700, 'end'))
    cb += [R(ox - 2, top - 20, 4, oy - top + 22, 'axis'), R(ox - 2, oy - 2, bw - 130, 4, 'axis'), P(f'M{ox - 10},{top - 16} L{ox},{top - 34} L{ox + 10},{top - 16}Z', 'axis'),
           P(f'M{ox + bw - 132},{oy - 10} L{ox + bw - 114},{oy} L{ox + bw - 132},{oy + 10}Z', 'axis')]
    s.layer('bar_board', cb, 'drop', .3)
    vals = [3, 5, 4, 7, 6]; cols = ['c1', 'c2', 'c3', 'c4', 'c5']
    bars = []
    for k, (v, c_) in enumerate(zip(vals, cols)):
        x = ox + 40 + k * 108
        bars += [R(x, oy - v * unit, 64, v * unit, c_, 6), R(x, oy - v * unit, 64, 10, '#ffffff', 4, .3), T(x + 32, oy - v * unit - 12, str(v), 24, c_, 800),
                 C(x + 32, oy + 30, 12, c_)]
    s.layer('bars', bars, 'grow', .6, origin=f'{ox} {oy}')
    # 左：软木板 + 扇形图 + 便利贴
    lx0 = 90
    lb = [R(lx0 - 12, 150, 404, 420, 'cork2', 16, extra='filter="url(#sh)"'), R(lx0, 162, 380, 396, 'cork', 10)]
    lb += [R(lx0 + 30, 190, 220, 230, 'board', 8, extra='filter="url(#shs)"'), C(lx0 + 140, 186, 8, 'pin')]
    pcx, pcy, pr = lx0 + 140, 310, 86
    a = -90
    for pct, c_ in zip([35, 25, 20, 20], ['c4', 'c2', 'c1', 'c3']):
        a1 = a + pct * 3.6; lb.append(sector(pcx, pcy, pr, a, a1, c_)); a = a1
    for a in (-90, 36, 126, 198): lb.append(S(f'M{pcx},{pcy} L{pcx + pr * math.cos(math.radians(a)):.1f},{pcy + pr * math.sin(math.radians(a)):.1f}', '#ffffff', 3))
    for k, (c_, ny) in enumerate(zip(['c4', 'c2', 'c1', 'c3'], range(445, 530, 22))):
        pass
    notes = [(lx0 + 280, 200, 'note1', -6), (lx0 + 280, 320, 'note2', 5), (lx0 + 60, 450, 'note3', -4), (lx0 + 200, 450, 'note1', 6)]
    for x, y, c_, rot in notes:
        lb.append(G([R(x, y, 90, 84, c_, 4, extra='filter="url(#shs)"'), R(x + 14, y + 26, 60, 5, 'axis', 2, .3), R(x + 14, y + 40, 46, 5, 'axis', 2, .3), R(x + 14, y + 54, 54, 5, 'axis', 2, .3), C(x + 45, y + 6, 6, 'pin')], f'transform="rotate({rot} {x + 45} {y + 42})"'))
    s.layer('left_board', lb, 'slide-l', .45)
    # 右：折线图 + 计数
    rx0 = 1440
    rb = [R(rx0 - 12, 150, 404, 420, 'frame', 16, extra='filter="url(#sh)"'), R(rx0, 162, 380, 396, 'board', 10)]
    gx0, gy0, gw, gh = rx0 + 40, 190, 300, 200
    for i in range(7): rb.append(R(gx0 + i * 50, gy0, 2, gh, 'grid'))
    for j in range(5): rb.append(R(gx0, gy0 + j * 50, gw, 2, 'grid'))
    rb += [R(gx0 - 2, gy0 - 6, 4, gh + 8, 'axis'), R(gx0 - 2, gy0 + gh - 2, gw + 10, 4, 'axis')]
    data = [1, 2, 1.5, 3, 2.5, 3.5, 4]
    pts = [(gx0 + i * 50, gy0 + gh - v * 50) for i, v in enumerate(data)]
    rb.append(S('M' + ' L'.join(f'{x},{y}' for x, y in pts), 'c1', 5))
    # 计数符号（每组 5）
    tx, ty = rx0 + 40, 440
    for row, n in enumerate([7, 12]):
        x = tx
        for g in range(math.ceil(n / 5)):
            m = min(5, n - g * 5)
            for q in range(min(m, 4)): rb.append(S(f'M{x + q * 14},{ty + row * 56} L{x + q * 14},{ty + row * 56 + 40}', 'axis', 4))
            if m == 5: rb.append(S(f'M{x - 8},{ty + row * 56 + 34} L{x + 50},{ty + row * 56 + 6}', 'c1', 4))
            x += 74
    s.layer('right_board', rb, 'slide-r', .5)
    s.layer('line_points', [C(x, y, 9, 'c1') for x, y in pts] + [C(x, y, 4, '#ffffff') for x, y in pts], 'pop', .9, loop='twinkle')
    # 画架：象形统计图
    ex, ey = 1640, 640
    ea = [S(f'M{ex - 90},{ey + 260} L{ex - 30},{ey - 40} M{ex + 90},{ey + 260} L{ex + 30},{ey - 40} M{ex},{ey + 260} L{ex},{ey}', 'easel', 10),
          R(ex - 130, ey - 20, 260, 200, 'paper', 6, extra='filter="url(#sh)"'), R(ex - 140, ey + 176, 280, 14, 'easel', 5)]
    for row, (n, c_) in enumerate([(4, 'c1'), (6, 'c2'), (3, 'c3')]):
        y = ey + 20 + row * 56
        ea.append(R(ex - 116, y - 14, 24, 28, c_, 6, .35))
        for k in range(n):
            x = ex - 74 + k * 32
            ea += [C(x, y + 2, 12, c_), R(x - 1.5, y - 16, 3, 8, 'easel'), E(x + 5, y - 13, 6, 3, 'leaf')]
    s.layer('easel', ea, 'rise', .7)
    s.layer('plant', [plant(240, 900, 1.25, 'pot', 'leaf', 'leaf2')], 'grow', .8, loop='sway', origin='240 900')
    s.layer('light', [E(960, 330, 560, 200, '#ffffff', .25, 'filter="url(#b40)"')], 'fade', 1.0, loop='glow')
    return s


# ============ s036 分数披萨店 ============
def pizzashop():
    s = Scene('s036', '分数披萨店', '数学', ['数学', '分数', '平均分', '生活'],
              dict(wall1='#FFF1E2', wall2='#F8DEC4', tile='#F1D2B4', awn1='#E3584A', awn2='#FFFFFF', board='#34433F', board2='#2A3734', frame='#B9804E', chalk='#FFFFFF', chalky='#FFE08A',
                   counter='#3F7F6E', counter2='#326656', top='#F4EDE2', crust='#E9A55A', crust2='#C9823D', sauce='#D9483B', cheese='#FFD66B', cheese2='#FFE79A', pep='#C2392F', basil='#4E9E5A',
                   brick='#C8674A', brick2='#A9533B', fire='#FF9F43', fire2='#FFD36E', plate='#FFFFFF', wood='#C58A55', wood2='#9C6537', floor1='#F2E6D6', floor2='#3F4A55', lamp='#FFE3A3', leaf='#6DB585', leaf2='#A6D99A'),
              desc='温暖的披萨店：柜台上的披萨被精确切成 2、4、8 等份（拿走一块），黑板菜单画着分数饼图，右侧砖砌烤炉火光闪烁。', stand={'ground_y': 920, 'x': [560, 1360]})
    bg = [R(0, 0, W, 860, s.lg([(0, 'wall1'), (1, 'wall2')]))]
    for y in range(300, 700, 36):
        off = 0 if (y // 36) % 2 else 40
        for x in range(-off, W, 80): bg.append(R(x + 2, y + 2, 76, 32, 'tile', 6, .55))
    s.layer('wall', bg, 'fade', 0)
    # 顶部条纹布幔
    aw = [R(0, 0, W, 50, 'awn1')]
    for k in range(24):
        x = k * 80
        aw.append(P(f'M{x},40 L{x + 80},40 L{x + 80},110 Q{x + 40},140 {x},110Z', 'awn1' if k % 2 == 0 else 'awn2'))
    s.layer('awning', aw, 'drop', .2, loop=None)
    # 黑板菜单（分数饼图）
    mx0, my0 = 120, 190
    mb = [R(mx0 - 16, my0 - 16, 432, 372, 'frame', 14, extra='filter="url(#sh)"'), R(mx0, my0, 400, 340, s.lg([(0, 'board'), (1, 'board2')]), 6)]
    for k, (n, fill_) in enumerate([(2, 1), (3, 2), (4, 3), (8, 5)]):
        cx = mx0 + 100 + (k % 2) * 200; cy = my0 + 90 + (k // 2) * 160; r = 52
        for q in range(n):
            a0 = -90 + q * 360 / n; a1 = a0 + 360 / n
            if q < fill_: mb.append(sector(cx, cy, r, a0, a1, 'chalky', .55))
        mb.append(S(f'M{cx - r},{cy} a{r},{r} 0 1,0 {2 * r},0 a{r},{r} 0 1,0 {-2 * r},0', 'chalk', 4, .9))
        for q in range(n):
            a = math.radians(-90 + q * 360 / n); mb.append(S(f'M{cx},{cy} L{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}', 'chalk', 3, .9))
        # 分数
        fx = cx + 74
        mb += [T(fx, cy - 8, str(fill_), 26, 'chalk', 800), R(fx - 13, cy, 26, 3, 'chalk'), T(fx, cy + 30, str(n), 26, 'chalk', 800)]
    s.layer('menu', mb, 'drop', .35)
    # 披萨铲挂墙
    s.layer('peel', [G([R(-12, 0, 24, 160, 'wood2', 8), P('M-70,150 L70,150 L60,300 Q0,320 -60,300Z', 'wood')], 'transform="translate(1340,180) rotate(12)"'),
                     G([R(-10, 0, 20, 120, 'wood2', 8), C(0, 170, 60, 'wood')], 'transform="translate(1250,190) rotate(-8)"')], 'pop', .5)
    # 烤炉（右）
    ox, oy = 1660, 760
    ov = [R(ox - 220, oy - 300, 440, 300, 'brick', 0), P(f'M{ox - 220},{oy - 300} Q{ox},{oy - 500} {ox + 220},{oy - 300}Z', 'brick'), R(ox - 50, 120, 100, 200, 'brick2', 4), R(ox - 64, 110, 128, 20, 'brick2', 6)]
    for y in range(oy - 290, oy, 34):
        off = 0 if (y // 34) % 2 else 30
        for x in range(ox - 220 - off, ox + 220, 60): ov.append(R(max(x + 2, ox - 218), y, min(56, ox + 218 - max(x + 2, ox - 218)), 30, 'brick2', 3, .45))
    ov += [P(f'M{ox - 120},{oy - 40} L{ox - 120},{oy - 170} A120,120 0 0,1 {ox + 120},{oy - 170} L{ox + 120},{oy - 40}Z', '#3A2420'),
           S(f'M{ox - 120},{oy - 40} L{ox - 120},{oy - 170} A120,120 0 0,1 {ox + 120},{oy - 170} L{ox + 120},{oy - 40}', 'brick2', 14)]
    s.layer('oven', ov, 'rise', .4)
    fire = [P(f'M{ox - 80},{oy - 44} Q{ox - 90},{oy - 110} {ox - 50},{oy - 150} Q{ox - 40},{oy - 100} {ox - 20},{oy - 120} Q{ox},{oy - 190} {ox + 30},{oy - 130} Q{ox + 50},{oy - 100} {ox + 60},{oy - 140} Q{ox + 100},{oy - 90} {ox + 80},{oy - 44}Z', 'fire'),
            P(f'M{ox - 50},{oy - 44} Q{ox - 50},{oy - 90} {ox - 20},{oy - 100} Q{ox},{oy - 140} {ox + 24},{oy - 96} Q{ox + 54},{oy - 80} {ox + 50},{oy - 44}Z', 'fire2'),
            C(ox, oy - 100, 150, 'fire', .3, 'filter="url(#b40)"')]
    s.layer('fire', fire, 'fade', .9, loop='glow')
    # 柜台
    ct = [R(0, 700, W, 160, s.lg([(0, 'counter'), (1, 'counter2')])), R(0, 682, W, 26, 'top', 6, extra='filter="url(#shs)"')]
    for x in range(30, W, 120): ct.append(R(x, 724, 90, 112, 'counter2', 8, .6))
    s.layer('counter', ct, 'rise', .2)
    s.layer('floor', [R(0, 860, W, 220, 'floor1'), *[R(x, y, 60, 60, 'floor2', 0, .9) for y in range(860, 1080, 60) for x in range(((y - 860) // 60 % 2) * 60, W, 120)]], 'rise', .1)

    def pizza(cx, cy, r, n, missing=(), pulled=None):
        it = [E(cx, cy + r + 8, r * .8, 10, '#000000', .14), R(cx - 8, cy + r * .6, 16, r * .5 + 40, 'wood2', 4), E(cx, cy + r * 1.1 + 40, r * .55, 12, 'wood2'),
              C(cx, cy, r + 14, 'plate', extra='filter="url(#shs)"')]
        random.seed(n * 7 + int(cx))
        for q in range(n):
            if q in missing: continue
            a0 = -90 + q * 360 / n; a1 = a0 + 360 / n; am = math.radians((a0 + a1) / 2)
            off = (r * .22 if q == pulled else 2.5)
            dx, dy = off * math.cos(am), off * math.sin(am)
            g = [sector(cx, cy, r, a0, a1, 'crust'), sector(cx, cy, r * .86, a0, a1, 'sauce'), sector(cx, cy, r * .82, a0, a1, 'cheese')]
            for t, (rr, da) in enumerate([(.55, -.25), (.6, .25), (.32, 0)]):
                if n >= 8 and t == 2: continue
                span = math.radians(360 / n) / 2
                aa = am + da * span * 1.2
                g.append(C(cx + r * rr * math.cos(aa), cy + r * rr * math.sin(aa), r * .1, 'pep'))
            g.append(E(cx + r * .7 * math.cos(am), cy + r * .7 * math.sin(am), r * .07, r * .035, 'basil', extra=f'transform="rotate({math.degrees(am):.0f} {cx + r * .7 * math.cos(am):.1f} {cy + r * .7 * math.sin(am):.1f})"'))
            g.append(C(cx + r * .42 * math.cos(am + .3), cy + r * .42 * math.sin(am + .3), r * .05, 'cheese2'))
            it.append(G(g, f'transform="translate({dx:.1f},{dy:.1f})"'))
        return G(it)
    pz = [pizza(250, 520, 110, 4, missing=(1,)), pizza(560, 540, 90, 2, missing=()), pizza(1370, 520, 110, 8, missing=(), pulled=2)]
    s.layer('pizzas', pz, 'pop', .6)
    # 柜台小物：油瓶、罗勒盆栽、盘子
    sm = [R(820, 610, 34, 76, 'basil', 10, .85), R(830, 594, 14, 20, 'wood2', 3), R(870, 630, 30, 56, 'awn1', 8), R(876, 618, 18, 14, 'wood2', 3),
          plant(1080, 684, .55, 'awn2', 'leaf', 'leaf2'), E(1180, 678, 60, 8, 'plate'), E(1180, 672, 56, 8, 'plate')]
    s.layer('counter_props', sm, 'pop', .75)
    lm = []
    for x in (420, 960, 1500):
        lm += [S(f'M{x},110 L{x},200', '#333333', 3), P(f'M{x - 50},250 Q{x},170 {x + 50},250Z', 'counter'), E(x, 251, 50, 7, 'lamp'), C(x, 260, 70, 'lamp', .4, 'filter="url(#b20)"')]
    s.layer('lamps', lm, 'drop', .85, loop='glow')
    s.layer('steam', [S(f'M{x},{y} q-12,-20 0,-40 q12,-20 0,-40', '#ffffff', 5, .6) for x, y in ((1350, 400), (1390, 390), (260, 400))], 'fade', 1.1, loop='flow')
    return s


# ============ s037 尺规作图桌 ============
def construction():
    s = Scene('s037', '尺规作图桌', '数学', ['数学', '几何', '尺规作图', '图形'],
              dict(wall1='#ECEFF8', wall2='#DADFF0', grid='#D3D9EC', board='#FFFFFF', bgrid='#E3EAF5', frame='#8D6A9F', frame2='#6F5082', ink='#2E3A59', arc='#5FA8E0', tri='#F27C66', hex='#6CC59A',
                   desk='#E7B98A', desk2='#C9925E', wood='#B57A4A', wood2='#8A5833', metal='#9AA6B2', metal2='#6C7884', lamp='#FFE3A3', lampb='#F2C14E', ruler='#FFE7A8', rtick='#3D4B5C',
                   floor1='#C9B8D6', floor2='#B19EC2', book1='#F27C66', book2='#5FA8E0', book3='#F7C44E', book4='#6CC59A', leaf='#6DB585', leaf2='#A6D99A', win1='#A6DCF7', win2='#E8F7FF'),
              desc='几何作图角：画板上用圆规交弧作出等边三角形、圆内接正六边形，桌上有大圆规、直尺、量角器和台灯。', stand={'ground_y': 900, 'x': [600, 1320]})
    bg = [R(0, 0, W, 790, s.lg([(0, 'wall1'), (1, 'wall2')]))] + [R(x, 0, 2, 790, 'grid', 0, .6) for x in range(0, W, 48)] + [R(0, y, W, 2, 'grid', 0, .6) for y in range(0, 790, 48)]
    s.layer('wall', bg, 'fade', 0)
    s.layer('floor', [R(0, 790, W, 290, s.lg([(0, 'floor1'), (1, 'floor2')])), *[S(f'M0,{y} L{W},{y}', 'floor2', 3, .5) for y in (840, 910, 1000)]], 'rise', .1)
    # 窗（左上）
    win = [R(90, 110, 340, 300, '#ffffff', 16, extra='filter="url(#shs)"'), R(106, 126, 308, 268, s.lg([(0, 'win1'), (1, 'win2')]), 8), cloud(220, 230, .45),
           R(256, 126, 8, 268, '#ffffff'), R(106, 256, 308, 8, '#ffffff'), R(80, 404, 360, 16, '#ffffff', 6)]
    s.layer('window', win, 'pop', .25)
    # 画架 + 画板
    bx0, by0, bx1, by1 = 560, 100, 1360, 560
    ea = [S(f'M760,{by1} L700,890 M1160,{by1} L1220,890 M960,{by1} L960,880', 'wood2', 14), R(700, 760, 520, 12, 'wood2', 5)]
    s.layer('easel', ea, 'rise', .3)
    bd = [R(bx0 - 18, by0 - 18, bx1 - bx0 + 36, by1 - by0 + 36, 'frame', 14, extra='filter="url(#sh)"'), R(bx0, by0, bx1 - bx0, by1 - by0, 'board', 6)]
    for x in range(bx0 + 40, bx1, 40): bd.append(R(x, by0, 1.5, by1 - by0, 'bgrid'))
    for y in range(by0 + 40, by1, 40): bd.append(R(bx0, y, bx1 - bx0, 1.5, 'bgrid'))
    bd.append(R(bx0 - 30, by1 + 12, bx1 - bx0 + 60, 20, 'frame2', 8))
    s.layer('board', bd, 'drop', .4)
    # 作图：等边三角形（以 AB 为半径作弧交于 C）
    Ax, Ay = 660, 470; Bx, By = 900, 470; L = Bx - Ax
    Cx, Cy = (Ax + Bx) / 2, Ay - L * math.sqrt(3) / 2
    con = [arc(Ax, Ay, L, -80, -40, 'arc', 3, .9), arc(Bx, By, L, -140, -100, 'arc', 3, .9), arc(Ax, Ay, L, 20, 35, 'arc', 3, .5), arc(Bx, By, L, 145, 160, 'arc', 3, .5),
           S(f'M{Ax},{Ay} L{Bx},{By}', 'ink', 4), S(f'M{Ax},{Ay} L{Cx:.1f},{Cy:.1f} L{Bx},{By}', 'tri', 5), C(Ax, Ay, 6, 'ink'), C(Bx, By, 6, 'ink'), C(Cx, Cy, 6, 'tri'),
           T(Ax - 16, Ay + 30, 'A', 26, 'ink', 700), T(Bx + 16, By + 30, 'B', 26, 'ink', 700), T(Cx, Cy - 20, 'C', 26, 'tri', 700),
           S(f'M{(Ax + Cx) / 2 - 6:.1f},{(Ay + Cy) / 2 - 4:.1f} l12,7', 'tri', 3), S(f'M{(Bx + Cx) / 2 - 6:.1f},{(By + Cy) / 2 + 4:.1f} l12,-7', 'tri', 3), S(f'M{(Ax + Bx) / 2:.1f},{Ay - 7} l0,14', 'tri', 3)]
    # 圆内接正六边形（半径等分圆周）
    Ox, Oy, Rr = 1150, 320, 150
    hexp = [(Ox + Rr * math.cos(math.radians(-90 + k * 60)), Oy + Rr * math.sin(math.radians(-90 + k * 60))) for k in range(6)]
    con += [S(f'M{Ox - Rr},{Oy} a{Rr},{Rr} 0 1,0 {2 * Rr},0 a{Rr},{Rr} 0 1,0 {-2 * Rr},0', 'ink', 3, .8), poly(hexp, 'hex', .2), S('M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in hexp) + 'Z', 'hex', 4),
            C(Ox, Oy, 5, 'ink'), S(f'M{Ox},{Oy} L{hexp[1][0]:.1f},{hexp[1][1]:.1f}', 'ink', 3, .8, extra='stroke-dasharray="8 6"'), T(Ox - 4, Oy + 30, 'O', 24, 'ink', 700)]
    for x, y in hexp:
        a = math.degrees(math.atan2(y - Oy, x - Ox))
        con += [C(x, y, 5, 'hex'), arc(x, y, Rr, a + 180 - 66, a + 180 - 54, 'arc', 2.5, .7), arc(x, y, Rr, a + 180 + 54, a + 180 + 66, 'arc', 2.5, .7)]
    s.layer('construction', con, 'fade', .7)
    # 画板上的圆规（针尖在 A，笔尖在 C）
    Mx, My = (Ax + Cx) / 2, (Ay + Cy) / 2
    lg = 170; hh = math.sqrt(lg ** 2 - (L / 2) ** 2)
    ux, uy = (Cx - Ax) / L, (Cy - Ay) / L
    Hx, Hy = Mx - uy * hh * -1 * -1 + uy * 0, My
    Hx, Hy = Mx + uy * hh, My - ux * hh
    cp = [S(f'M{Ax},{Ay} L{Hx:.1f},{Hy:.1f}', 'metal2', 9), S(f'M{Hx:.1f},{Hy:.1f} L{Cx:.1f},{Cy:.1f}', 'metal', 9), C(Hx, Hy, 13, 'metal2'), R(Hx - 5, Hy - 40, 10, 30, 'wood2', 4),
          C(Cx, Cy, 6, 'lampb'), C(Ax, Ay, 4, 'ink')]
    s.layer('compass_on_board', cp, 'pop', .9, loop='swing', origin=f'{Ax} {Ay}')
    # 左桌：大圆规立着、直尺、笔筒
    dk = [E(300, 900, 240, 16, '#000000', .14), R(80, 720, 26, 180, 'desk2', 6), R(494, 720, 26, 180, 'desk2', 6), R(60, 696, 480, 30, 'desk', 10, extra='filter="url(#shs)"')]
    dk += [R(90, 664, 330, 32, 'ruler', 4, extra='filter="url(#shs)"')]
    for k in range(31): dk.append(R(96 + k * 10.6, 664, 2, 16 if k % 5 == 0 else 9, 'rtick'))
    dk += [R(440, 600, 64, 96, 'book2', 12), *[R(448 + k * 14, 520 + (k % 2) * 16, 8, 90, ['book1', 'book3', 'book4', 'rtick'][k], 3) for k in range(4)]]
    s.layer('desk_left', dk, 'slide-l', .5)
    bc = [C(250, 470, 16, 'metal2'), S('M250,470 L190,660', 'metal', 12), S('M250,470 L310,660', 'metal', 12), S('M190,660 L186,684', 'rtick', 4), P('M302,654 L320,654 L311,690Z', 'tri'),
          R(244, 430, 12, 40, 'wood2', 5), S('M218,560 L282,560', 'metal2', 4)]
    s.layer('big_compass', bc, 'drop', .65)
    # 右桌：台灯、量角器、三角板
    rd = [E(1640, 900, 240, 16, '#000000', .14), R(1420, 720, 26, 180, 'desk2', 6), R(1834, 720, 26, 180, 'desk2', 6), R(1400, 696, 480, 30, 'desk', 10, extra='filter="url(#shs)"')]
    ppx, ppy, ppr = 1560, 690, 100
    rd += [P(f'M{ppx - ppr},{ppy} A{ppr},{ppr} 0 0,1 {ppx + ppr},{ppy}Z', 'ruler', .95, 'filter="url(#shs)"'), P(f'M{ppx - 40},{ppy} A40,40 0 0,1 {ppx + 40},{ppy}Z', 'desk', .9)]
    for d in range(0, 181, 5):
        a = math.radians(180 + d); r0 = ppr * (.8 if d % 30 == 0 else (.87 if d % 10 == 0 else .92))
        rd.append(S(f'M{ppx + r0 * math.cos(a):.1f},{ppy + r0 * math.sin(a):.1f} L{ppx + ppr * math.cos(a):.1f},{ppy + ppr * math.sin(a):.1f}', 'rtick', 1.6 if d % 10 else 2.4))
    rd += [C(ppx, ppy - 2, 4, 'tri'), poly([(1680, 696), (1680, 560), (1760, 696)], 'hex', .85), poly([(1694, 682), (1694, 616), (1730, 682)], 'desk')]
    lp = [R(1800, 680, 80, 16, 'frame2', 6), S('M1840,680 L1800,560 L1740,500', 'frame2', 10), P('M1700,470 L1780,470 L1770,530 L1710,530Z', 'lampb', extra='transform="rotate(-25 1740 500)"')]
    s.layer('desk_right', rd + lp, 'slide-r', .55)
    s.layer('lamp_glow', [P('M1700,520 L1770,500 L1820,700 L1580,700Z', s.lg([(0, 'lamp', .45), (1, 'lamp', 0)])), C(1735, 520, 60, 'lamp', .5, 'filter="url(#b20)"')], 'fade', 1.0, loop='glow')
    # 右墙书架
    shf = [R(1460, 200, 380, 16, 'wood2', 6, extra='filter="url(#shs)"')]
    x = 1480
    for k, (w, h, c_) in enumerate([(26, 110, 'book1'), (22, 96, 'book2'), (30, 120, 'book3'), (24, 100, 'book4'), (28, 112, 'book1'), (22, 90, 'book2')]):
        shf.append(R(x, 200 - h, w, h, c_, 3)); x += w + 4
    shf += [C(1720, 160, 40, 'book2'), S('M1680,160 a40,14 0 1,0 80,0', '#ffffff', 3, .7), S('M1720,120 a14,40 0 1,0 0,80', '#ffffff', 3, .7), R(1716, 200, 8, 0, 'wood')]
    shf += [R(1460, 380, 380, 16, 'wood2', 6, extra='filter="url(#shs)"'), cuboid(1490, 380, 70, 70, 50, 'book1', '#F7A593', '#D45E4B'), cone(1640, 380, 40, 100, 'book3', '#D9A12E'), C(1760, 340, 40, 'book4'), C(1748, 328, 9, '#ffffff', .5)]
    s.layer('shelf', shf, 'pop', .6)
    s.layer('plant', [plant(470, 908, 1.0, 'book2', 'leaf', 'leaf2')], 'grow', .8, loop='sway', origin='470 908')
    return s


# ============ s038 数字迷宫 ============
def numbermaze():
    s = Scene('s038', '数字迷宫', '数学', ['数学', '数数', '思维训练', '游戏'],
              dict(sky1='#8FD3F5', sky2='#EAF8FF', sun='#FFD36E', far='#A8D9B5', hedge='#4FA36B', hedge2='#3E8A57', hedge3='#7CC48E', hedge4='#2F7347', path='#F3E2C0', path2='#E2CB9C',
                   stone='#FFFFFF', n1='#F27C66', n2='#F7C44E', n3='#5FA8E0', n4='#9B85E0', n5='#6CC59A', wood='#B57A4A', wood2='#8A5833', board='#FFFDF4', wall='#3E8A57',
                   bal1='#F27C66', bal2='#F7C44E', bal3='#5FA8E0', bal4='#9B85E0', flower='#FF9FB0', grass='#93CF7B', grass2='#7DBE68'),
              desc='户外树篱迷宫：中央拱形树篱入口，数字踏步石一路通向迷宫，左侧立着迷宫地图牌（程序生成、可走通），右侧路标和气球。', stand={'ground_y': 910, 'x': [600, 1320]})
    s.layer('sky', [R(0, 0, W, 800, s.lg([(0, 'sky1'), (1, 'sky2')])), C(300, 160, 150, 'sun', .3, 'filter="url(#b40)"'), C(300, 160, 60, 'sun')], 'fade', 0)
    s.layer('clouds', [cloud(700, 150, .6, op=.9), cloud(1300, 110, .8, op=.9), cloud(1750, 220, .5, op=.85)], 'slide-l', .2, loop='drift')
    s.layer('far', [P('M0,560 Q200,470 420,530 Q640,450 900,520 Q1150,440 1400,520 Q1650,460 1920,530 L1920,640 L0,640Z', 'far')], 'rise', .2)

    def hedge(x0, x1, y_top, y_bot, col, col2, bumps=True):
        it = [R(x0, y_top, x1 - x0, y_bot - y_top, col, 14)]
        if bumps:
            for x in range(int(x0) + 20, int(x1) - 10, 40): it.append(C(x, y_top + 6, 22, col))
        it.append(R(x0, y_bot - 18, x1 - x0, 18, col2, 0, .6))
        for x in range(int(x0) + 30, int(x1) - 20, 70): it.append(C(x, y_top + 40 + (x % 3) * 12, 6, col2, .5))
        return G(it)
    # 远层树篱（有缺口）
    s.layer('hedge_far', [hedge(0, 520, 600, 680, 'hedge3', 'hedge'), hedge(620, 1300, 600, 680, 'hedge3', 'hedge'), hedge(1400, 1920, 600, 680, 'hedge3', 'hedge')], 'rise', .3)
    # 中层树篱 + 拱门
    ax0, ax1 = 840, 1080
    mid = [hedge(-20, ax0, 640, 790, 'hedge', 'hedge2'), hedge(ax1, 1940, 640, 790, 'hedge', 'hedge2'),
           P(f'M{ax0 - 40},790 L{ax0 - 40},560 A{(ax1 - ax0) / 2 + 40},{(ax1 - ax0) / 2 + 40} 0 0,1 {ax1 + 40},560 L{ax1 + 40},790 L{ax1},790 L{ax1},560 A{(ax1 - ax0) / 2},{(ax1 - ax0) / 2} 0 0,0 {ax0},560 L{ax0},790Z', 'hedge2'),
           *[C(ax0 - 20 + 300 * k / 8, 560 - math.sqrt(max(0, 160 ** 2 - (300 * k / 8 - 140) ** 2)) * .98 + 6, 18, 'hedge2') for k in range(9)]]
    mid += [R(ax0, 600, ax1 - ax0, 190, 'path2', 0, .35)]
    s.layer('hedge_mid', mid, 'rise', .4)
    # 拱门顶小旗
    s.layer('arch_flags', [S(f'M{960},{400} L{960},{450}', 'wood2', 4), P('M962,402 L1010,414 L962,428Z', 'n1'), C(960, 398, 6, 'n2')], 'pop', .9, loop='sway', origin='960 450')
    gd = [R(0, 790, W, 290, s.lg([(0, 'grass'), (1, 'grass2')])), P(f'M{ax0},790 L{ax1},790 Q{1180},900 {1300},1080 L{620},1080 Q{760},900 {ax0},790Z', 'path')]
    s.layer('ground', gd, 'rise', .1)
    # 数字踏步石
    st = []
    for k, (x, y, r_) in enumerate([(880, 928, 40), (1030, 880, 34), (920, 842, 28), (1010, 814, 23), (955, 796, 18)]):
        col = ['n1', 'n2', 'n3', 'n4', 'n5'][k]
        st += [E(x, y + r_ * .25, r_ * 1.15, r_ * .5, '#000000', .1), E(x, y, r_ * 1.15, r_ * .55, 'stone'), E(x, y - 2, r_ * .95, r_ * .42, col, .9),
               T(x, y + r_ * .17, str(k + 1), int(r_ * .55), 'stone', 900)]
    s.layer('stepping_stones', st, 'pop', .6)
    # 迷宫地图牌（左）
    N = 7; cs = 40; mx0, my0 = 120, 330
    random.seed(8)
    walls = {(i, j): [True, True, True, True] for i in range(N) for j in range(N)}  # 上右下左
    seen = {(0, 0)}; stack = [(0, 0)]
    while stack:
        i, j = stack[-1]
        nb = [(d, i + di, j + dj) for d, (di, dj) in enumerate([(0, -1), (1, 0), (0, 1), (-1, 0)]) if 0 <= i + di < N and 0 <= j + dj < N and (i + di, j + dj) not in seen]
        if not nb: stack.pop(); continue
        d, ni, nj = random.choice(nb)
        walls[(i, j)][d] = False; walls[(ni, nj)][(d + 2) % 4] = False
        seen.add((ni, nj)); stack.append((ni, nj))
    # 求解路径
    from collections import deque
    prev = {(0, 0): None}; q = deque([(0, 0)])
    while q:
        c_ = q.popleft()
        for d, (di, dj) in enumerate([(0, -1), (1, 0), (0, 1), (-1, 0)]):
            n_ = (c_[0] + di, c_[1] + dj)
            if not walls[c_][d] and n_ not in prev: prev[n_] = c_; q.append(n_)
    path = []; c_ = (N - 1, N - 1)
    while c_: path.append(c_); c_ = prev[c_]
    path.reverse()
    mp = [S(f'M{mx0 + N * cs / 2},{my0 + N * cs + 30} L{mx0 + N * cs / 2},{900}', 'wood2', 14), E(mx0 + N * cs / 2, 902, 60, 10, '#000000', .14),
          R(mx0 - 24, my0 - 24, N * cs + 48, N * cs + 48, 'wood', 14, extra='filter="url(#sh)"'), R(mx0 - 10, my0 - 10, N * cs + 20, N * cs + 20, 'board', 8)]
    mp.append(S('M' + ' L'.join(f'{mx0 + i * cs + cs / 2},{my0 + j * cs + cs / 2}' for i, j in path), 'n2', 10, .55))
    for (i, j), wl in walls.items():
        x, y = mx0 + i * cs, my0 + j * cs
        if wl[0] and not (i == 0 and j == 0): mp.append(S(f'M{x},{y} L{x + cs},{y}', 'wall', 5))
        if wl[1] and not (i == N - 1 and j == N - 1): mp.append(S(f'M{x + cs},{y} L{x + cs},{y + cs}', 'wall', 5))
        if j == N - 1 and wl[2]: mp.append(S(f'M{x},{y + cs} L{x + cs},{y + cs}', 'wall', 5))
        if i == 0 and wl[3]: mp.append(S(f'M{x},{y} L{x},{y + cs}', 'wall', 5))
    for k in range(0, len(path), max(1, len(path) // 6)):
        i, j = path[k]
        if k == 0: continue
        mp.append(T(f'{mx0 + i * cs + cs / 2}', my0 + j * cs + cs / 2 + 8, str(min(9, k // max(1, len(path) // 6))), 22, 'n1', 900))
    mp += [C(mx0 + cs / 2, my0 + cs / 2, 11, 'n5'), star(mx0 + (N - .5) * cs, my0 + (N - .5) * cs, 15, 'n1')]
    s.layer('map_board', mp, 'slide-l', .5)
    # 近景树篱（左右框景）+ 修剪球
    nh = [hedge(-20, 80, 520, 1000, 'hedge2', 'hedge4'), hedge(1840, 1940, 520, 1000, 'hedge2', 'hedge4')]
    for x in (600, 1320):
        nh += [E(x, 912, 70, 12, '#000000', .14), R(x - 40, 860, 80, 50, 'wood', 10), C(x, 810, 58, 'hedge'), C(x - 16, 792, 18, 'hedge3', .7)]
    s.layer('topiary', nh, 'grow', .7)
    # 路标（右）
    sp = [R(1586, 520, 14, 390, 'wood2', 5), E(1593, 910, 50, 10, '#000000', .14)]
    for k, (y, d, c_) in enumerate([(540, 1, 'n3'), (600, -1, 'n1'), (660, 1, 'n5')]):
        x0 = 1593 if d > 0 else 1593 - 170
        sp.append(P(f'M{x0},{y} L{x0 + 150},{y} L{x0 + 170},{y + 22} L{x0 + 150},{y + 44} L{x0},{y + 44}Z' if d > 0 else f'M{x0 + 170},{y} L{x0 + 20},{y} L{x0},{y + 22} L{x0 + 20},{y + 44} L{x0 + 170},{y + 44}Z', c_, extra='filter="url(#shs)"'))
        sp.append(T(f'{x0 + 85}', y + 32, ['+1', '−2', '×3'][k], 26, 'stone', 900))
    s.layer('signpost', sp, 'drop', .8)
    bl = [S('M1760,700 Q1750,600 1720,480 M1760,700 Q1770,600 1800,440 M1760,700 Q1760,620 1760,500', '#ffffff', 2, .9)]
    for x, y, c_ in ((1720, 460, 'bal1'), (1800, 420, 'bal3'), (1760, 480, 'bal2'), (1830, 500, 'bal4')):
        bl += [E(x, y, 34, 42, c_), E(x - 10, y - 14, 8, 12, '#ffffff', .5), P(f'M{x - 5},{y + 42} L{x + 5},{y + 42} L{x},{y + 50}Z', c_)]
    s.layer('balloons', bl, 'pop', 1.0, loop='bob')
    random.seed(3)
    fw = []
    for k in range(16):
        x = random.choice([random.uniform(150, 560), random.uniform(1360, 1800)]); y = random.uniform(820, 940)
        fw += [S(f'M{x:.0f},{y:.0f} L{x:.0f},{y - 20:.0f}', 'hedge2', 3), C(x, y - 24, 7, random.choice(['flower', 'n2', 'stone'])), C(x, y - 24, 2.5, 'n2')]
    s.layer('flowers', fw, 'grow', 1.1, loop='sway')
    return s


# ============ s039 天平称重台 ============
def balance():
    s = Scene('s039', '天平称重台', '数学', ['数学', '质量', '克与千克', '等式'],
              dict(wall1='#FDEBDD', wall2='#F6D6C0', wains='#E9B79A', wains2='#D99E7E', counter='#7A5C9E', counter2='#634A84', top='#F4EEF8', brass='#E6B54E', brass2='#C7922E', brass3='#FFE29A',
                   metal='#8E9AA8', metal2='#6B7785', pan='#D7DEE6', scale='#FFFFFF', tick='#3D4B5C', apple='#E8483B', apple2='#FF8A7A', pear='#B7D65A', leaf='#4E9E5A',
                   jar='#E6F4F7', bean1='#C9773F', bean2='#F2C14E', bean3='#6CC59A', shelf='#C08A5E', shelf2='#9C6A42', lamp='#FFE3A3', box='#B9804E', box2='#8E5A33', velvet='#C8455A', floor1='#D7C3B2', floor2='#BEA592'),
              desc='称重台：等臂托盘天平横梁水平、指针归零，左盘苹果右盘砝码；旁有砝码盒、弹簧秤与装豆子的量罐，适合质量与等式课。', stand={'ground_y': 910, 'x': [1080, 1640]})
    s.layer('wall', [R(0, 0, W, 800, s.lg([(0, 'wall1'), (1, 'wall2')])), R(0, 520, W, 180, 'wains', 0, .45), R(0, 514, W, 10, 'wains2')], 'fade', 0)
    s.layer('floor', [R(0, 860, W, 220, s.lg([(0, 'floor1'), (1, 'floor2')])), *[R(x, 860, 3, 220, 'floor2', 0, .5) for x in range(0, W, 140)]], 'rise', .1)
    # 柜台
    ct = [R(0, 720, W, 150, s.lg([(0, 'counter'), (1, 'counter2')])), R(0, 702, W, 26, 'top', 6, extra='filter="url(#shs)"')]
    for x in range(40, W, 160): ct.append(R(x, 746, 120, 104, 'counter2', 10, .55))
    s.layer('counter', ct, 'rise', .2)
    # 墙架：量罐
    shf = [R(1300, 300, 560, 18, 'shelf', 6, extra='filter="url(#shs)"'), R(1320, 318, 14, 30, 'shelf2'), R(1826, 318, 14, 30, 'shelf2')]
    for k, (c_, lvl) in enumerate([('bean1', .7), ('bean2', .5), ('bean3', .85), ('bean1', .35), ('bean2', .9)]):
        x = 1340 + k * 102; h = 140
        shf += [R(x, 300 - h, 76, h, 'jar', 14, .9), R(x + 4, 300 - h * lvl, 68, h * lvl - 4, c_, 10, .9), R(x - 4, 300 - h - 14, 84, 18, 'shelf2', 6)]
        for q in range(1, 5): shf.append(R(x + 60, 300 - q * 28, 12, 2, 'tick', 0, .6))
    s.layer('jars', shf, 'slide-r', .4)
    # 弹簧秤（挂在左上）
    sx = 300
    sp = [R(sx - 40, 90, 80, 14, 'shelf2', 5), S(f'M{sx},104 L{sx},140', 'metal2', 4), R(sx - 30, 140, 60, 210, 'scale', 12, extra='filter="url(#shs)"'), S(f'M{sx - 30},140 L{sx + 30},140', 'metal2', 3)]
    for k in range(11):
        y = 170 + k * 16; sp.append(R(sx - 18 if k % 5 == 0 else sx - 10, y, 18 if k % 5 == 0 else 10, 2.5, 'tick'))
    sp += [S(f'M{sx + 4},{150} L{sx + 4},{170 + 6 * 16}', 'metal', 4), P(f'M{sx - 6},{170 + 6 * 16} L{sx + 14},{170 + 6 * 16 - 7} L{sx + 14},{170 + 6 * 16 + 7}Z', 'apple'),
           S(f'M{sx},{350} L{sx},{396} q0,16 -12,16 q-12,0 -12,-12', 'metal2', 4), C(sx - 26, 440, 30, 'pear'), P(f'M{sx - 26},408 q4,-14 14,-16', 'leaf'), C(sx - 34, 430, 8, '#ffffff', .4)]
    s.layer('spring_scale', sp, 'drop', .5, loop='swing', origin=f'{sx} 97')
    # 天平：支点 (bx, by)
    bx, by, arm = 760, 330, 260
    bal = [E(bx, 704, 190, 12, '#000000', .14), R(bx - 170, 670, 340, 34, 'brass2', 12, extra='filter="url(#shs)"'), R(bx - 150, 656, 300, 20, 'brass', 8),
           R(bx - 14, by + 10, 28, 650 - by, s.lg([(0, 'brass2'), (.5, 'brass'), (1, 'brass2')], 0, 0, 1, 0)), P(f'M{bx - 40},{656} L{bx + 40},{656} L{bx + 20},{620} L{bx - 20},{620}Z', 'brass2')]
    # 刻度盘
    dx_, dy_ = bx, 560
    bal += [P(f'M{dx_ - 70},{dy_} A70,70 0 0,1 {dx_ + 70},{dy_}Z', 'scale', 1, 'filter="url(#shs)"')]
    for d in range(-40, 41, 10):
        a = math.radians(-90 + d)
        bal.append(S(f'M{dx_ + 52 * math.cos(a):.1f},{dy_ + 52 * math.sin(a):.1f} L{dx_ + 66 * math.cos(a):.1f},{dy_ + 66 * math.sin(a):.1f}', 'tick' if d else 'apple', 3 if d else 4))
    s.layer('balance_stand', bal, 'rise', .45)
    beam_ = [R(bx - arm - 10, by - 9, 2 * arm + 20, 18, 'brass', 9, extra='filter="url(#shs)"'), R(bx - arm, by - 4, 2 * arm, 4, 'brass3', 2, .7), C(bx, by, 22, 'brass2'), C(bx, by, 9, 'brass3'),
             C(bx - arm, by, 10, 'brass2'), C(bx + arm, by, 10, 'brass2')]
    # 托盘（链）
    pan_y = 560
    for sd in (-1, 1):
        px = bx + sd * arm
        beam_ += [S(f'M{px},{by + 6} L{px - 90},{pan_y - 6} M{px},{by + 6} L{px + 90},{pan_y - 6} M{px},{by + 6} L{px},{pan_y - 10}', 'metal', 3),
                  P(f'M{px - 110},{pan_y - 8} L{px + 110},{pan_y - 8} Q{px + 100},{pan_y + 34} {px},{pan_y + 34} Q{px - 100},{pan_y + 34} {px - 110},{pan_y - 8}Z', 'pan', extra='filter="url(#shs)"'),
                  E(px, pan_y - 8, 110, 12, 'metal'), E(px, pan_y - 10, 104, 9, 'pan')]
    # 左盘苹果（3 个）
    for x, yy in ((bx - arm - 46, pan_y - 40), (bx - arm + 46, pan_y - 40), (bx - arm, pan_y - 84)):
        beam_ += [C(x, yy, 36, 'apple'), C(x - 12, yy - 12, 10, 'apple2', .7), S(f'M{x},{yy - 34} q2,-14 8,-18', 'shelf2', 4), E(x + 14, yy - 46, 12, 6, 'leaf', extra=f'transform="rotate(-25 {x + 14} {yy - 46})"')]
    # 右盘砝码
    def weight(x, y, r_, h):
        return G([R(x - r_, y - h, 2 * r_, h, 'brass', 6), E(x, y - h, r_, r_ * .3, 'brass3'), R(x - r_ * .3, y - h - r_ * .7, r_ * .6, r_ * .6, 'brass2', 3), C(x, y - h - r_ * .8, r_ * .38, 'brass'),
                  R(x - r_ + 6, y - h + 8, 6, h - 14, '#ffffff', 3, .4)])
    beam_ += [weight(bx + arm - 40, pan_y - 12, 40, 56), weight(bx + arm + 50, pan_y - 12, 30, 44), weight(bx + arm + 4, pan_y - 70, 24, 34)]
    s.layer('beam_pans', beam_, 'drop', .6)
    s.layer('pointer', [S(f'M{bx},{by} L{bx},{dy_ - 8}', 'apple', 5), C(bx, by, 6, 'brass3')], 'fade', .9, loop='swing', origin=f'{bx} {by}')
    # 砝码盒（左前）
    wb = [R(80, 618, 300, 90, 'box', 10, extra='filter="url(#shs)"'), R(92, 630, 276, 66, 'velvet', 6)]
    for k, (r_, h) in enumerate([(26, 36), (22, 30), (18, 26), (14, 22), (12, 18), (10, 14)]):
        x = 122 + k * 44
        wb.append(weight(x, 684, r_ * .8, h))
    wb += [R(80, 560, 300, 60, 'box2', 10, extra=f'transform="rotate(-24 80 620)"'), R(96, 572, 268, 8, 'velvet', 3, .5, f'transform="rotate(-24 80 620)"')]
    wb += [S('M410,690 L470,640 M414,694 L478,648', 'metal2', 5)]
    s.layer('weight_box', wb, 'pop', .75)
    # 电子秤（右侧小）+ 绿植
    es = [R(1640, 660, 160, 44, 'scale', 10, extra='filter="url(#shs)"'), R(1650, 650, 140, 14, 'metal', 6), R(1680, 674, 80, 22, '#2E3A45', 4), R(1690, 678, 50, 14, '#8EF0B0', 2),
          C(1700, 620, 30, 'pear'), C(1740, 624, 26, 'apple'), C(1690, 610, 8, '#ffffff', .4)]
    s.layer('digital_scale', es, 'pop', .85)
    s.layer('plant', [plant(1880, 704, .8, 'velvet', 'leaf', 'pear')], 'grow', .9, loop='sway', origin='1880 704')
    lm = [S('M760,0 L760,90', '#333333', 3), P('M690,150 Q760,70 830,150Z', 'counter'), E(760, 151, 70, 9, 'lamp'), C(760, 170, 120, 'lamp', .4, 'filter="url(#b40)"')]
    s.layer('lamp', lm, 'drop', 1.0, loop='glow')
    s.layer('glints', [C(bx + arm - 60, pan_y - 50, 4, '#ffffff', .9), C(bx - 100, by - 6, 4, '#ffffff', .9), C(140, 650, 3, '#ffffff', .9)], 'fade', 1.2, loop='twinkle')
    return s


# ============ s040 数轴跳格步道 ============
def numberline():
    s = Scene('s040', '数轴跳格步道', '数学', ['数学', '数轴', '加减法', '户外'],
              dict(sky1='#9AD8F5', sky2='#FFF3DC', sun='#FFD36E', hill='#BFE3B0', hill2='#A2D492', tree='#5FAE74', tree2='#9AD48B', trunk='#8A5A3A', grass1='#9CD27C', grass2='#80C062',
                   path='#F6ECDD', path2='#E3D3BB', line='#3D4B5C', c0='#F27C66', c1='#F7A541', c2='#F7C44E', c3='#8FD06F', c4='#5CC3A8', c5='#5FA8E0', c6='#8C8EE6', c7='#C285D9',
                   hop='#F2556A', bench='#C58A55', bench2='#9C6537', kite1='#F27C66', kite2='#5FA8E0', kite3='#F7C44E', flower='#FF9FB0', white='#FFFFFF'),
              desc='公园步道上画着 0–10 的数轴（等距刻度、箭头），每个刻度有彩色跳格圆点，虚线弧表示“+2”跳跃，背景是树林与风筝。', stand={'ground_y': 900, 'x': [200, 1720]})
    s.layer('sky', [R(0, 0, W, 760, s.lg([(0, 'sky1'), (1, 'sky2')])), C(1560, 200, 170, 'sun', .3, 'filter="url(#b40)"'), C(1560, 200, 66, 'sun')], 'fade', 0)
    s.layer('clouds', [cloud(300, 170, .8, op=.9), cloud(880, 110, .55, op=.85), cloud(1250, 240, .45, op=.8)], 'slide-l', .2, loop='drift')
    s.layer('hills', [P('M0,580 Q300,470 640,560 Q980,470 1300,550 Q1620,480 1920,560 L1920,700 L0,700Z', 'hill'), P('M0,640 Q480,570 960,630 Q1440,580 1920,640 L1920,720 L0,720Z', 'hill2')], 'rise', .25)
    s.layer('trees', [blob_tree(x, 690, .62 + .14 * (k % 3) / 2, 'tree', 'tree2', 'trunk') for k, x in enumerate((60, 230, 420, 1500, 1690, 1870))] +
            [pine(x, 690, .5, 'tree', 'tree2', 'trunk') for x in (330, 1600)], 'grow', .4, loop='sway')
    s.layer('grass', [R(0, 690, W, 390, s.lg([(0, 'grass1'), (1, 'grass2')]))], 'rise', .1)
    # 长椅
    bc = []
    for x in (640, 1280):
        bc += [R(x - 90, 660, 180, 14, 'bench', 5), R(x - 90, 640, 180, 12, 'bench', 5), R(x - 90, 688, 180, 14, 'bench', 6), R(x - 80, 700, 10, 34, 'bench2'), R(x + 70, 700, 10, 34, 'bench2'),
               R(x - 84, 640, 8, 60, 'bench2'), R(x + 76, 640, 8, 60, 'bench2')]
    s.layer('benches', bc, 'rise', .5)
    # 步道
    pth = [R(0, 760, W, 190, 'path2', 0), R(0, 770, W, 170, 'path'), R(0, 940, W, 10, 'grass2', 0, .5)]
    for x in range(0, W, 120): pth.append(R(x, 770, 2, 170, 'path2', 0, .6))
    s.layer('path', pth, 'rise', .15)
    # 数轴 0–10
    x0, step, ly = 180, 150, 870
    nl = [R(100, ly - 4, 1640, 8, 'line', 4), P(f'M{1736},{ly - 22} L{1790},{ly} L{1736},{ly + 22}Z', 'line')]
    cols = ['c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c0', 'c1', 'c2']
    for k in range(11):
        x = x0 + k * step
        nl += [R(x - 3, ly - 20, 6, 40, 'line', 3), C(x, ly - 64, 30, cols[k], extra='filter="url(#shs)"'), C(x, ly - 64, 22, 'white', .25), T(x, ly - 53, str(k), 30, 'white', 900)]
        if k < 10: nl.append(R(x + step / 2 - 1.5, ly - 10, 3, 20, 'line', 1, .6))
    s.layer('numberline', nl, 'slide-l', .5)
    # 跳跃弧（+2）
    hp = []
    for a in (1, 3, 5):
        xa, xb = x0 + a * step, x0 + (a + 2) * step
        hp.append(S(f'M{xa},{ly - 100} Q{(xa + xb) / 2},{ly - 250} {xb},{ly - 100}', 'hop', 5, .9, extra='stroke-dasharray="14 10"'))
        hp.append(P(f'M{xb - 16},{ly - 122} L{xb + 2},{ly - 98} L{xb + 12},{ly - 128}Z', 'hop'))
        hp.append(T((xa + xb) / 2, ly - 190, '+2', 32, 'hop', 900))
    s.layer('hops', hp, 'fade', .9, loop='glow')
    # 风筝
    def kite(x, y, c1, c2, rot):
        return G([poly([(x, y - 60), (x + 44, y), (x, y + 70), (x - 44, y)], c1), poly([(x, y - 60), (x + 44, y), (x, y)], c2, .7), poly([(x, y), (x - 44, y), (x, y + 70)], c2, .45),
                  S(f'M{x},{y + 70} q-20,30 0,60 q20,30 0,60', c1, 3), *[P(f'M{x - 10},{y + 100 + k * 30} l10,-8 l10,8 l-10,8Z', c2) for k in range(2)]], f'transform="rotate({rot} {x} {y})"')
    s.layer('kites', [kite(560, 220, 'kite1', 'kite3', -12), kite(1340, 160, 'kite2', 'kite1', 10), kite(1820, 330, 'kite3', 'kite2', -6)], 'pop', .8, loop='bob')
    random.seed(5)
    fw = []
    for k in range(20):
        x = random.uniform(30, 1890); y = random.uniform(714, 752)
        fw += [S(f'M{x:.0f},{y:.0f} L{x:.0f},{y - 16:.0f}', 'tree', 3), C(x, y - 19, 6, random.choice(['flower', 'c2', 'white']))]
    for k in range(10):
        x = random.uniform(30, 1890); y = random.uniform(960, 1060)
        fw += [P(f'M{x - 14:.0f},{y:.0f} q6,-26 10,-4 q4,-28 8,0 q6,-22 10,4Z', 'grass1')]
    s.layer('flowers', fw, 'grow', 1.0, loop='sway')
    return s


SCENES = [mathboard, blocks, measure, stats, pizzashop, construction, numbermaze, balance, numberline]
