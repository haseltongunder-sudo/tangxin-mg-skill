"""第 2 类 · 体育 s012–s020（平面 MG）
场地线按真实尺寸程序绘制：地面采用「正投影压扁」平面（横向 sx 像素/米，纵深 sy 像素/米，不汇聚），
立面物体（篮架、球门、球网）用与横向相同的 sx 作为真实高度比例。"""
from core import *
from scenes_c01 import shadow, star, leafy, sky_window, floor_lines
import math, random


def ER(cx, cy, rx, ry, col, w=4, op=1, dash=None):
    """椭圆描边（避免重复 style 属性）"""
    ex = f'stroke-dasharray="{dash}"' if dash else ''
    return S(f'M{cx - rx:.1f},{cy:.1f} a{rx:.1f},{ry:.1f} 0 1,0 {2 * rx:.1f},0 a{rx:.1f},{ry:.1f} 0 1,0 {-2 * rx:.1f},0Z', col, w, op, extra=ex)


def RR(x, y, w, h, col, sw=4, op=1):
    return S(f'M{x},{y} h{w} v{h} h{-w}Z', col, sw, op)


class Court:
    """地面平面坐标（米）→ 屏幕：u 横向（以 cx 为 0），v 纵深（v=0 在 y0，向观众增大）"""
    def __init__(self, cx, y0, sx, sy):
        self.cx, self.y0, self.sx, self.sy = cx, y0, sx, sy

    def p(self, u, v, h=0):
        return (self.cx + u * self.sx, self.y0 + v * self.sy - h * self.sx)

    def line(self, pts, col, w=5, op=1):
        q = [self.p(u, v) for u, v in pts]
        return S('M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in q), col, w, op, cap='butt')

    def arc(self, uc, vc, r, a0, a1, col, w=5, op=1, n=48, extra_pts_before=(), extra_pts_after=()):
        pts = list(extra_pts_before) + [(uc + r * math.cos(a0 + (a1 - a0) * k / n), vc + r * math.sin(a0 + (a1 - a0) * k / n)) for k in range(n + 1)] + list(extra_pts_after)
        return self.line(pts, col, w, op)

    def rect(self, u0, v0, u1, v1, col, w=5, op=1):
        return self.line([(u0, v0), (u1, v0), (u1, v1), (u0, v1), (u0, v0)], col, w, op)

    def fillrect(self, u0, v0, u1, v1, col, op=None):
        (x0, y0), (x1, y1) = self.p(u0, v0), self.p(u1, v1)
        return R(min(x0, x1), min(y0, y1), abs(x1 - x0), abs(y1 - y0), col, 0, op)

    def ell(self, uc, vc, r, col, op=None):
        x, y = self.p(uc, vc)
        return E(x, y, r * self.sx, r * self.sy, col, op)


def pennants(x0, x1, y, sag, n, cols, size=18):
    it = [S(f'M{x0},{y} Q{(x0 + x1) / 2},{y + sag * 2} {x1},{y}', '#ffffff', 3, .9)]
    for k in range(n):
        u = (k + .5) / n; x = x0 + (x1 - x0) * u; yy = y + sag * 4 * u * (1 - u)
        it.append(poly([(x - size, yy), (x + size, yy), (x, yy + size * 1.7)], cols[k % len(cols)]))
    return it


def high_lamp(x, y, s, col='lamp', body='metal'):
    return G([S(f'M{x},0 L{x},{y - 30 * s}', body, 3), P(f'M{x - 60 * s},{y} Q{x},{y - 60 * s} {x + 60 * s},{y}Z', body), E(x, y, 60 * s, 9 * s, col), E(x, y + 40 * s, 150 * s, 60 * s, col, .35, 'filter="url(#b20)"')])


# ============ s012 篮球馆 ============
def basketball():
    s = Scene('s012', '篮球馆', '体育', ['体育', '篮球', '运动会', '团队合作'],
              dict(wall1='#EAF1FA', wall2='#D5E2F2', band='#3F6FB5', band2='#F28B4B', truss='#B9C7D8', win1='#A8DDF7', win2='#EAF8FF', floor1='#E9B97F', floor2='#D9A266', plank='#C98F55',
                   paint='#4F86C9', paint2='#F0A35E', line='#FFFFFF', oob='#3F6FB5', board='#FFFFFF', boardline='#E8573E', rim='#F26A2E', net='#FFFFFF', post='#3B4656', pad='#F28B4B',
                   seat1='#F28B4B', seat2='#4F86C9', seat3='#F7C55E', stand='#C9D6E6', score='#2C3445', digit='#FFC94D', digit2='#FF6A5A', ball='#E9772E', ball2='#B9531C', metal='#8C9BA7', lamp='#FFF4CF'),
              desc='室内篮球馆端线视角：篮板、篮圈与篮网按标准高度，地面三分线、罚球区与罚球圈按 FIBA 尺寸绘制，两侧看台与记分牌。', stand={'ground_y': 900, 'x': [560, 1360]})
    s.layer('wall', [R(0, 0, W, 620, s.lg([(0, 'wall1'), (1, 'wall2')])), R(0, 540, W, 80, 'band', 0, .55), R(0, 532, W, 8, 'band2')], 'fade', 0)
    # 屋架与高窗
    tr = []
    for x in range(0, W + 1, 240):
        tr += [S(f'M{x},0 L{x + 120},70 L{x + 240},0', 'truss', 6, .8)]
    tr += [R(0, 66, W, 10, 'truss', 0, .8)]
    for x in range(40, W, 240):
        tr.append(sky_window(s, x + 20, 110, 160, 110, 'win1', 'win2', 'line', None, mull='v', rx=6, border=8))
    s.layer('roof_windows', tr, 'fade', .1)
    s.layer('lamps', [high_lamp(x, 92, .7) for x in (240, 720, 1200, 1680)], 'drop', .2, loop='glow')
    # 两侧看台
    st = []
    for x0, x1 in ((0, 520), (1400, 1920)):
        for r_ in range(4):
            y = 300 + r_ * 50
            st.append(R(x0, y + 34, x1 - x0, 16, 'stand'))
            for k in range(int((x1 - x0) / 34)):
                st += [R(x0 + 6 + k * 34, y + 8, 26, 30, ['seat1', 'seat2', 'seat3'][(k + r_) % 3], 6), R(x0 + 6 + k * 34, y + 30, 26, 8, ['seat1', 'seat2', 'seat3'][(k + r_) % 3], 3, .7)]
        st.append(R(x0, 296, x1 - x0, 8, 'post', 0, .5))
    s.layer('bleachers', st, 'rise', .3)
    # 记分牌
    sb = [S('M820,0 L820,40 M1100,0 L1100,40', 'metal', 4), R(780, 36, 360, 130, 'score', 16, extra='filter="url(#sh)"'), R(800, 56, 120, 70, '#1E2433', 8), R(1000, 56, 120, 70, '#1E2433', 8),
          T(860, 112, '36', 56, 'digit', 900), T(1060, 112, '28', 56, 'digit2', 900), C(960, 76, 6, 'digit'), C(960, 104, 6, 'digit'), R(820, 136, 80, 10, 'seat2', 5), R(1020, 136, 80, 10, 'seat1', 5)]
    s.layer('scoreboard', sb, 'drop', .45)
    s.layer('pennants', pennants(560, 1360, 250, 14, 12, ['seat1', 'seat3', 'seat2', 'line'], 15), 'drop', .9, loop='sway')
    # 地面：球场 15 m 宽，横向 113 px/m；纵深 31 px/m；端线 y=640
    ct = Court(960, 640, 113.3, 30.5)
    fl = [R(0, 600, W, 480, s.lg([(0, 'floor1'), (1, 'floor2')]))]
    for y in range(612, 1080, 22): fl.append(R(0, y, W, 2, 'plank', 0, .35))
    random.seed(2)
    for y in range(612, 1080, 22):
        x = random.randint(-200, 0)
        while x < W: x += random.randint(220, 420); fl.append(R(x, y, 2, 22, 'plank', 0, .35))
    fl.append(R(0, 600, W, 40, 'oob', 0, .4))   # 端线外缓冲区
    x0, _ = ct.p(-7.5, 0); x1, _ = ct.p(7.5, 0)
    fl += [R(0, 600, x0, 480, 'oob', 0, .4), R(x1, 600, W - x1, 480, 'oob', 0, .4)]
    # 罚球区上色
    fl.append(ct.fillrect(-2.45, 0, 2.45, 5.8, 'paint', .9))
    fl.append(ct.ell(0, 5.8, 1.8, 'paint', .9))
    fl.append(ct.ell(0, 14, 1.8, 'paint2', .9))
    # 线（5 cm 线宽夸张为 5 px）
    L = 'line'
    fl.append(ct.rect(-7.5, 0, 7.5, 14.5, L, 6))
    fl.append(ct.line([(-7.5, 14), (7.5, 14)], L, 6))
    fl.append(ct.rect(-2.45, 0, 2.45, 5.8, L, 5))
    fl.append(ct.arc(0, 5.8, 1.8, 0, math.pi, L, 5))                       # 罚球圈外半
    for k in range(8):                                                        # 罚球圈内半（虚线）
        a0 = math.pi + k * math.pi / 8; fl.append(ct.arc(0, 5.8, 1.8, a0, a0 + math.pi / 16, L, 5, n=4))
    fl.append(ct.arc(0, 1.575, 1.25, 0, math.pi, L, 4))                     # 无撞人半圆
    a = math.acos(6.6 / 6.75)                                                 # 三分线：底角直线 + 半径 6.75 圆弧
    vt = 1.575 + 6.75 * math.sin(a)
    fl.append(ct.arc(0, 1.575, 6.75, a, math.pi - a, L, 6, extra_pts_before=[(6.6, 0)], extra_pts_after=[(-6.6, 0)]))
    fl.append(ct.arc(0, 14, 1.8, math.pi, 2 * math.pi, L, 5))                # 中圈（只见上半）
    for v in (1.75, 2.6, 3.45, 4.3):                                          # 分位线
        fl += [ct.line([(-2.45, v), (-2.6, v)], L, 4), ct.line([(2.45, v), (2.6, v)], L, 4)]
    fl.append(R(0, 600, W, 120, 'line', 0, .0))
    s.layer('court', fl, 'rise', .1)
    # 篮架（篮板 1.8×1.05 m，下沿 2.9 m，篮圈 3.05 m，篮圈中心距端线 1.575 m）
    bx, by_board = ct.p(0, 1.2)
    _, rim_y = ct.p(0, 1.575, 3.05)
    bw = 1.8 * ct.sx; bh = 1.05 * ct.sx; btop = by_board - 3.95 * ct.sx
    hp = [R(bx - 70, btop - 46, 140, 50, 'post', 8), R(bx - 120, btop - 56, 240, 14, 'post', 6), R(bx - 60, btop + bh, 120, 60, 'post', 8, .8),
          R(bx - bw / 2 - 10, btop - 10, bw + 20, bh + 20, 'post', 12, extra='filter="url(#sh)"'), R(bx - bw / 2, btop, bw, bh, 'board', 6),
          R(bx - bw / 2, btop, bw, bh * .32, '#ffffff', 6, .0),
          S(f'M{bx - .295 * ct.sx},{btop + bh - .15 * ct.sx} L{bx - .295 * ct.sx},{btop + bh - .6 * ct.sx} L{bx + .295 * ct.sx},{btop + bh - .6 * ct.sx} L{bx + .295 * ct.sx},{btop + bh - .15 * ct.sx}', 'boardline', 6, cap='butt'),
          S(f'M{bx - bw / 2 + 4},{btop + 4} L{bx + bw / 2 - 4},{btop + 4} L{bx + bw / 2 - 4},{btop + bh - 4} L{bx - bw / 2 + 4},{btop + bh - 4}Z', 'boardline', 7),
          R(bx - bw / 2 - 10, btop + bh + 4, bw + 20, 14, 'pad', 6)]
    # 篮网
    rr = .225 * ct.sx; nh = .45 * ct.sx
    net = [P(f'M{bx - rr},{rim_y} L{bx + rr},{rim_y} L{bx + rr * .55},{rim_y + nh} L{bx - rr * .55},{rim_y + nh}Z', 'net', .25)]
    for k in range(7):
        t = k / 6; xa = bx - rr + 2 * rr * t; xb = bx - rr * .55 + 2 * rr * .55 * (1 - t)
        net.append(S(f'M{xa:.1f},{rim_y} L{xb:.1f},{rim_y + nh}', 'net', 2.5, .95))
    for k in range(1, 4):
        yy = rim_y + nh * k / 4; w_ = rr * (1 - .45 * k / 4)
        net.append(S(f'M{bx - w_:.1f},{yy:.1f} L{bx + w_:.1f},{yy:.1f}', 'net', 2, .8))
    hp += [R(bx - 8, rim_y - 12, 16, 12, 'rim', 2)] + net + [ER(bx, rim_y, rr, 7, 'rim', 6), S(f'M{bx - rr},{rim_y} L{bx + rr},{rim_y}', 'rim', 6)]
    s.layer('hoop', hp, 'drop', .5)
    # 球车与篮球
    def ball(x, y, r):
        return G([C(x, y, r, 'ball'), S(f'M{x - r},{y} L{x + r},{y} M{x},{y - r} L{x},{y + r}', 'ball2', 3), S(f'M{x - r * .7},{y - r * .7} Q{x - r * .25},{y} {x - r * .7},{y + r * .7} M{x + r * .7},{y - r * .7} Q{x + r * .25},{y} {x + r * .7},{y + r * .7}', 'ball2', 3), C(x - r * .35, y - r * .4, r * .25, '#ffffff', .25)])
    cart = [shadow(1720, 950, 150, 12), R(1590, 820, 260, 14, 'metal', 6), R(1590, 900, 260, 14, 'metal', 6), R(1590, 820, 12, 120, 'metal', 4), R(1838, 820, 12, 120, 'metal', 4),
            C(1600, 946, 10, 'post'), C(1840, 946, 10, 'post')]
    for k in range(4): cart.append(ball(1630 + k * 60, 790, 30))
    for k in range(3): cart.append(ball(1660 + k * 60, 742, 30))
    for k in range(4): cart.append(ball(1630 + k * 60, 872, 28))
    s.layer('ball_cart', cart, 'rise', .8)
    s.layer('ball', [shadow(330, 960, 44, 8, .18), ball(330, 924, 36)], 'pop', 1.0, loop='bob')
    # 计时器/水瓶小道具
    s.layer('bench', [shadow(200, 830, 170, 10), R(40, 770, 330, 20, 'seat2', 10), R(60, 790, 14, 40, 'post', 4), R(336, 790, 14, 40, 'post', 4),
                      R(90, 730, 28, 42, 'paint', 8), R(96, 720, 16, 12, 'line', 4), R(140, 740, 26, 32, 'seat1', 8), R(220, 744, 90, 28, 'line', 8), R(228, 750, 74, 6, 'seat3', 3)], 'rise', .9)
    return s


# ============ s013 足球场 ============
def football():
    s = Scene('s013', '足球场', '体育', ['体育', '足球', '运动会', '团队合作'],
              dict(sky1='#7CC7F0', sky2='#E3F6FF', bowl='#E6EDF3', bowl2='#C9D5E0', roof='#F4F7FA', roof2='#AFC0D0', seat1='#3E8ED0', seat2='#FFFFFF', seat3='#67B7E8',
                   ad1='#3E8ED0', ad2='#F2B33D', ad3='#E8574A', ad4='#34A86B', g1='#78C25B', g2='#69B44F', line='#FFFFFF', post='#FFFFFF', net='#FFFFFF', tower='#8C9BA7', lampc='#FFF6CC',
                   ball='#FFFFFF', ball2='#2E3440', cone='#FF8A3D', flag1='#F2B33D', flag2='#E8574A', tree='#5FAE74', tree2='#9ED38C', trunk='#8A5A3A'),
              desc='足球场球门正面视角：7.32×2.44 m 球门与球网、球门区、点球点与罚球弧按标准尺寸，背后广告板、看台与灯塔。', stand={'ground_y': 930, 'x': [480, 1440]})
    s.layer('sky', [R(0, 0, W, 700, s.lg([(0, 'sky1'), (1, 'sky2')]))], 'fade', 0)
    s.layer('clouds', [cloud(320, 120, .7, op=.9), cloud(1000, 80, .5, op=.85), cloud(1650, 150, .65, op=.85)], 'slide-l', .2, loop='drift')
    # 看台碗
    bw = [P('M-20,700 L-20,330 Q960,250 1940,330 L1940,700Z', s.lg([(0, 'bowl'), (1, 'bowl2')]))]
    for r_ in range(6):
        y = 372 + r_ * 50
        bw.append(P(f'M-20,{y + 34} Q960,{y + 34 - 140 * (1 - r_ / 9)} 1940,{y + 34} L1940,{y + 42} Q960,{y + 42 - 140 * (1 - r_ / 9)} -20,{y + 42}Z', 'bowl2', .8))
        for k in range(0, 1960, 40):
            yy = y + 34 - 70 * (1 - ((k + 15 - 960) / 980) ** 2) * (1 - r_ / 9) * 2 * .5 - 30
            col = 'seat3' if (k // 40 + r_) % 5 == 0 else 'seat1'
            if abs(k + 15 - 960) < 220 and 0 < r_ < 5: col = 'seat2'
            bw.append(R(k, yy, 30, 26, col, 7))
    bw += [P('M-20,330 Q960,250 1940,330 L1940,300 Q960,214 -20,300Z', 'roof2'), P('M-20,300 Q960,214 1940,300 L1940,250 Q960,170 -20,250Z', 'roof')]
    s.layer('stadium', [G(bw)], 'rise', .25)
    # 旗帜
    fg = []
    for x in (200, 560, 1360, 1720):
        yb = 300 - 90 * (1 - ((x - 960) / 1000) ** 2) + 10
        fg += [S(f'M{x},{yb} L{x},{yb - 90}', 'tower', 3), P(f'M{x},{yb - 90} Q{x + 30},{yb - 100} {x + 56},{yb - 84} L{x + 56},{yb - 56} Q{x + 30},{yb - 72} {x},{yb - 62}Z', 'flag1' if x < 960 else 'flag2')]
    s.layer('flags', fg, 'drop', .5, loop='sway')
    # 灯塔
    tw = []
    for x in (110, 1810):
        tw += [P(f'M{x - 18},700 L{x + 18},700 L{x + 8},150 L{x - 8},150Z', 'tower'), R(x - 90, 70, 180, 90, 'tower', 10, extra='filter="url(#shs)"')]
        for r_ in range(2):
            for k in range(4): tw.append(C(x - 60 + k * 40, 98 + r_ * 36, 14, 'lampc'))
        tw.append(C(x, 115, 150, 'lampc', .35, 'filter="url(#b40)"'))
    s.layer('towers', tw, 'grow', .4, loop='glow')
    # 广告板（无字色块）
    ad = [R(0, 640, W, 64, 'ad1')]
    for k, x in enumerate(range(0, W, 240)):
        ad += [R(x + 4, 646, 232, 52, ['ad1', 'ad2', 'ad3', 'ad4'][k % 4], 6), R(x + 30, 664, 120, 14, 'line', 7, .85), C(x + 190, 671, 16, 'line', .85)]
    s.layer('ad_boards', ad, 'rise', .45)
    # 草坪：横向 88 px/m，纵深 14 px/m；球门线 y=760
    ct = Court(960, 760, 88, 16)
    gr = [R(0, 700, W, 380, 'g1')]
    for k in range(12):
        y = 700 + k * 32
        if k % 2: gr.append(R(0, y, W, 32, 'g2'))
    L = 'line'
    gr += [S(f'M0,{760} L{W},{760}', L, 6, cap='butt'),
           ct.line([(-9.16, 0), (-9.16, 5.5), (9.16, 5.5), (9.16, 0)], L, 5),          # 球门区 18.32×5.5
           ct.line([(-20.16, 16.5), (20.16, 16.5)], L, 5),                               # 罚球区 40.32×16.5
           ct.line([(-20.16, 0), (-20.16, 16.5)], L, 5), ct.line([(20.16, 0), (20.16, 16.5)], L, 5)]
    a = math.acos(5.5 / 9.15)                                                                 # 罚球弧：以点球点为圆心 r=9.15
    gr.append(ct.arc(0, 11, 9.15, a, math.pi - a, L, 5))
    px_, py_ = ct.p(0, 11)
    gr.append(E(px_, py_, 9, 4, L))                                                           # 点球点
    s.layer('pitch', gr, 'rise', .1)
    # 球门 7.32×2.44 m，网深约 2 m
    gx0, gy = ct.p(-3.66, 0); gx1, _ = ct.p(3.66, 0); gh = 2.44 * ct.sx; pw = .12 * ct.sx
    bx0, byb = ct.p(-3.66, -2.0); bx1, _ = ct.p(3.66, -2.0)
    top_back = byb - 1.6 * ct.sx
    cp = s.clip(f'<path d="M{gx0},{gy - gh} L{gx1},{gy - gh} L{gx1},{gy} L{gx0},{gy}Z"/>')
    mesh = [R(gx0, gy - gh, gx1 - gx0, gh, 'net', .05)]
    for x in range(int(gx0) + 12, int(gx1), 24): mesh.append(S(f'M{x},{gy - gh} L{x},{byb}', 'net', 1.6, .45))
    for y in range(int(gy - gh) + 12, int(byb), 24): mesh.append(S(f'M{gx0},{y} L{gx1},{y}', 'net', 1.6, .45))
    goal = [R(gx0 - 20, byb - 4, gx1 - gx0 + 40, gy - byb + 10, '#000000', .06, 'filter="url(#b6)"'), G(mesh, f'clip-path="{cp}"'),
            S(f'M{bx0},{byb} L{bx1},{byb}', 'net', 3, .7),
            S(f'M{gx0},{gy - gh} L{bx0 + 20},{top_back} L{bx1 - 20},{top_back} L{gx1},{gy - gh}', 'post', 4, .8),
            S(f'M{bx0 + 20},{top_back} L{bx0 + 30},{byb} M{bx1 - 20},{top_back} L{bx1 - 30},{byb}', 'post', 4, .8),
            R(gx0 - pw, gy - gh - pw, pw, gh + pw, 'post', 3, extra='filter="url(#shs)"'), R(gx1, gy - gh - pw, pw, gh + pw, 'post', 3, extra='filter="url(#shs)"'),
            R(gx0 - pw, gy - gh - pw, gx1 - gx0 + 2 * pw, pw, 'post', 3, extra='filter="url(#shs)"')]
    s.layer('goal', goal, 'rise', .55)
    s.layer('trees', [blob_tree(x, 640, .6, 'tree', 'tree2', 'trunk') for x in (30, 1890)], 'grow', .35, loop='sway')

    def fball(x, y, r):
        it = [C(x, y, r, 'ball'), poly([(x + r * .38 * math.cos(math.radians(-90 + k * 72)), y + r * .38 * math.sin(math.radians(-90 + k * 72))) for k in range(5)], 'ball2')]
        for k in range(5):
            ang = math.radians(-90 + 36 + k * 72)
            cx_, cy_ = x + r * .92 * math.cos(ang), y + r * .92 * math.sin(ang)
            it.append(C(cx_, cy_, r * .22, 'ball2'))
            a2 = math.radians(-90 + k * 72); it.append(S(f'M{x + r * .38 * math.cos(a2):.1f},{y + r * .38 * math.sin(a2):.1f} L{x + r * .78 * math.cos(a2):.1f},{y + r * .78 * math.sin(a2):.1f}', 'ball2', 2))
        it.append(C(x - r * .35, y - r * .4, r * .22, '#ffffff', .5))
        return G([P(f'M{x - r},{y} a{r},{r} 0 1,0 {2 * r},0 a{r},{r} 0 1,0 {-2 * r},0', 'ball')] + it)
    s.layer('ball', [shadow(1500, 1000, 46, 9, .2), fball(1500, 960, 40)], 'pop', .9, loop='bob')
    cones = []
    for k, x in enumerate((200, 320, 440)):
        y = 890 + (k % 2) * 30
        cones += [shadow(x, y + 4, 34, 6), R(x - 32, y - 6, 64, 10, 'cone', 4), P(f'M{x - 20},{y - 4} L{x + 20},{y - 4} L{x + 6},{y - 70} L{x - 6},{y - 70}Z', 'cone'), R(x - 15, y - 40, 30, 10, 'line', 3, .9)]
    s.layer('cones', cones, 'pop', 1.0)
    return s


# ============ s014 排球场 ============
def volleyball():
    s = Scene('s014', '排球场', '体育', ['体育', '排球', '团队合作', '运动会'],
              dict(sky1='#8ED2F4', sky2='#FFF3DC', bld='#F8E1C4', bld2='#EDC9A0', win='#BFE3F5', win2='#FFFFFF', roof='#E07A5F', fence='#7E9AAE', tree='#5FAE74', tree2='#9ED38C', trunk='#8A5A3A',
                   free='#4DAF7C', free2='#3F9A6C', court='#F08A5D', court2='#E47A4D', line='#FFFFFF', post='#3B4656', postpad='#2F7FC9', net='#2E3440', tape='#FFFFFF', ant1='#E8473B', ant2='#FFFFFF',
                   ball1='#FFD447', ball2='#3E8ED0', ball3='#FFFFFF', bench='#F2B33D', metal='#8C9BA7'),
              desc='户外排球场端线视角：球网高 2.24 m、宽 9.5 m，标志杆与进攻线、端线按标准比例，背后围网、树与教学楼。', stand={'ground_y': 900, 'x': [520, 1400]})
    s.layer('sky', [R(0, 0, W, 520, s.lg([(0, 'sky1'), (1, 'sky2')])), C(1600, 140, 60, '#FFF1B8'), C(1600, 140, 140, '#FFF1B8', .35, 'filter="url(#b40)"')], 'fade', 0)
    s.layer('clouds', [cloud(300, 120, .7, op=.9), cloud(1000, 90, .5, op=.85)], 'slide-l', .2, loop='drift')
    bl = [R(260, 180, 1400, 300, s.lg([(0, 'bld'), (1, 'bld2')]), 6), R(240, 166, 1440, 22, 'roof', 6)]
    for r_ in range(3):
        for k in range(16):
            bl += [R(296 + k * 84, 214 + r_ * 84, 52, 50, 'win', 4), R(296 + k * 84, 214 + r_ * 84, 52, 12, 'win2', 3, .8)]
    s.layer('building', bl, 'rise', .25)
    s.layer('trees', [blob_tree(x, 470, .8 + .12 * (k % 2), 'tree', 'tree2', 'trunk') for k, x in enumerate((80, 260, 520, 1380, 1640, 1850))], 'grow', .35, loop='sway')
    # 围网
    fn = [R(0, 300, W, 6, 'fence'), R(0, 456, W, 6, 'fence')]
    for x in range(0, W, 240): fn.append(R(x, 290, 10, 172, 'fence', 4))
    mesh = []
    for x in range(-200, W + 200, 22):
        mesh.append(S(f'M{x},306 L{x + 150},456', 'fence', 1.5, .5)); mesh.append(S(f'M{x + 150},306 L{x},456', 'fence', 1.5, .5))
    fn.append(G(mesh))
    s.layer('fence', fn, 'fade', .4)
    # 场地：横向 130 px/m；纵深 24 px/m；中线 y=700
    ct = Court(960, 700, 130, 24)
    gd = [R(0, 460, W, 620, s.lg([(0, 'free'), (1, 'free2')])), ct.fillrect(-4.5, -9, 4.5, 9, 'court')]
    gd.append(ct.fillrect(-4.5, -3, 4.5, 3, 'court2', .55))
    L = 'line'
    gd += [ct.rect(-4.5, -9, 4.5, 9, L, 6), ct.line([(-4.5, 0), (4.5, 0)], L, 6), ct.line([(-4.5, 3), (4.5, 3)], L, 5), ct.line([(-4.5, -3), (4.5, -3)], L, 5)]
    for k in range(5):  # 进攻线延长虚线（每段 15 cm，间隔 20 cm）
        for sd in (-1, 1):
            u0 = sd * (4.5 + .2 + k * .35); gd.append(ct.line([(u0, 3), (u0 + sd * .15, 3)], L, 5)); gd.append(ct.line([(u0, -3), (u0 + sd * .15, -3)], L, 5))
    s.layer('court', gd, 'rise', .1)
    # 球网：宽 9.5 m（中心 1 m 高），网上沿 2.24 m，标志杆高出网 0.8 m，立柱距边线 1 m
    netw = 9.5; ytop = 700 - 2.24 * ct.sx; ybot = ytop + 1.0 * ct.sx
    xl, xr = ct.p(-netw / 2, 0)[0], ct.p(netw / 2, 0)[0]
    pl, pr = ct.p(-5.5, 0)[0], ct.p(5.5, 0)[0]
    nt = [shadow(pl, 704, 40, 6), shadow(pr, 704, 40, 6), R(pl - 9, ytop - 40, 18, 740 - ytop, 'post', 6), R(pr - 9, ytop - 40, 18, 740 - ytop, 'post', 6),
          R(pl - 20, 520, 40, 180, 'postpad', 12), R(pr - 20, 520, 40, 180, 'postpad', 12),
          S(f'M{pl},{ytop + 4} L{xl},{ytop + 4} M{xr},{ytop + 4} L{pr},{ytop + 4} M{pl},{ybot - 4} L{xl},{ybot - 4} M{xr},{ybot - 4} L{pr},{ybot - 4}', 'net', 3)]
    msh = [R(xl, ytop, xr - xl, ybot - ytop, 'net', .04)]
    step = .1 * ct.sx
    k = 0
    x = xl
    while x <= xr + .1:
        msh.append(S(f'M{x:.1f},{ytop} L{x:.1f},{ybot}', 'net', 1.1, .32)); x += step
    y = ytop
    while y <= ybot + .1:
        msh.append(S(f'M{xl},{y:.1f} L{xr},{y:.1f}', 'net', 1.1, .32)); y += step
    nt += msh + [R(xl, ytop, xr - xl, .07 * ct.sx, 'tape', 2), R(xl, ybot - .05 * ct.sx, xr - xl, .05 * ct.sx, 'tape', 2)]
    for u in (-4.5, 4.5):  # 侧标志带 5 cm + 标志杆（红白相间 10 cm）
        x, _ = ct.p(u, 0)
        nt.append(R(x - .025 * ct.sx, ytop, .05 * ct.sx, ybot - ytop, 'tape'))
        for j in range(18):
            yy = ytop - .8 * ct.sx + j * .1 * ct.sx
            nt.append(R(x - 4, yy, 8, .1 * ct.sx, 'ant1' if j % 2 == 0 else 'ant2'))
    s.layer('net', nt, 'drop', .5)

    def vball(x, y, r):
        cp = s.clip(f'<circle cx="{x}" cy="{y}" r="{r}"/>')
        bands = [S(f'M{x - r * 1.2},{y - r * .2} Q{x},{y - r * 1.1} {x + r * 1.2},{y - r * .5}', 'ball1', r * .42),
                 S(f'M{x - r * 1.1},{y + r * .6} Q{x - r * .1},{y - r * .1} {x + r * .7},{y + r * 1.2}', 'ball2', r * .42)]
        return G([C(x, y, r, 'ball3'), G(bands, f'clip-path="{cp}"'), ER(x, y, r, r, 'net', 1.5, .35), C(x - r * .35, y - r * .4, r * .22, '#ffffff', .6)])
    s.layer('ball_air', [vball(1240, 320, 34)], 'pop', .9, loop='bob')
    bn = [shadow(1720, 900, 170, 10), R(1560, 840, 320, 22, 'bench', 10), R(1580, 860, 14, 40, 'post', 4), R(1846, 860, 14, 40, 'post', 4),
          R(1600, 800, 28, 42, 'postpad', 8), R(1606, 790, 16, 12, 'line', 4), R(1650, 812, 90, 30, 'line', 8), R(1658, 818, 74, 6, 'court', 3)]
    cart = [shadow(240, 930, 120, 10), R(130, 830, 220, 90, 'metal', 14, .35), S('M130,830 L130,920 L350,920 L350,830', 'metal', 6), C(150, 930, 10, 'post'), C(330, 930, 10, 'post')]
    for k in range(4): cart.append(vball(160 + k * 54, 816, 26))
    for k in range(3): cart.append(vball(188 + k * 54, 776, 26))
    s.layer('props', bn + cart, 'rise', .8)
    s.layer('ball_floor', [shadow(1300, 1004, 36, 7), vball(1300, 976, 30)], 'pop', 1.0)
    return s


# ============ s015 乒乓球室 ============
def tabletennis():
    s = Scene('s015', '乒乓球室', '体育', ['体育', '乒乓球', '国球', '协调性'],
              dict(wall1='#EAF4F8', wall2='#D3E7EF', band='#2F6FB0', win1='#A8DDF7', win2='#EAF8FF', frame='#FFFFFF', floor1='#C9584B', floor2='#B04A3F', top='#2C6FB5', top2='#245C98',
                   edge='#1E4E80', line='#FFFFFF', legs='#3B4656', net='#2E3440', netw='#FFFFFF', barrier='#2F4E8A', barrier2='#3E64A8', ball='#FFFFFF', ball2='#FF9F43',
                   paddle='#E8473B', paddle2='#2E3440', handle='#D9A066', robot='#5B6B7C', basket='#F2B33D', score='#2C3445', digit='#FFFFFF', lamp='#FFF4CF', metal='#9AA8B3', leaf='#5FAE74', leaf2='#9ED38C'),
              desc='乒乓球训练室：标准 2.74×1.525 m 球台（高 76 cm、网高 15.25 cm），挡板、翻分牌、发球机和球筐，红色运动地胶。', stand={'ground_y': 900, 'x': [480, 1060]})
    s.layer('wall', [R(0, 0, W, 640, s.lg([(0, 'wall1'), (1, 'wall2')])), R(0, 600, W, 40, 'band')], 'fade', 0)
    s.layer('windows', [sky_window(s, x, 150, 280, 300, 'win1', 'win2', 'frame', [cloud(x + 100, 250, .4), C(x + 60, 470, 110, 'leaf2', .8), C(x + 230, 480, 90, 'leaf', .5)], mull='cross') for x in (130, 590, 1050, 1510)], 'pop', .15)
    s.layer('lamps', [high_lamp(x, 70, .55) for x in (380, 840, 1300, 1760)], 'drop', .2, loop='glow')
    s.layer('pennants', pennants(0, W, 30, 10, 24, ['band', 'paddle', 'basket', 'netw'], 13), 'drop', .7, loop='sway')
    fl = [R(0, 640, W, 440, s.lg([(0, 'floor1'), (1, 'floor2')]))] + [R(0, y, W, 2, 'floor2', 0, .5) for y in (700, 790, 900, 1020)]
    s.layer('floor', fl, 'rise', .1)
    # 挡板（远处一排）
    br = []
    for x in range(0, W, 230):
        br += [R(x + 6, 540, 218, 100, 'barrier', 8, extra='filter="url(#shs)"'), R(x + 16, 552, 198, 56, 'barrier2', 4), R(x + 30, 570, 80, 10, 'netw', 5, .6), C(x + 180, 575, 12, 'netw', .6)]
    s.layer('barriers', br, 'rise', .3)

    # 球台：斜二测（台面纵深向右上偏移），尺寸 2.74 × 1.525 × 0.76 m
    def table(x0, yn, k, d_ratio=(.26, .34)):
        Lx = 2.74 * k; Dx, Dy = 1.525 * k * d_ratio[0], -1.525 * k * d_ratio[1]; Hh = .76 * k; th = .03 * k + 4
        def q(u, d, h=0):  # u 沿长度(米), d 沿纵深(米), h 高度(米)
            return (x0 + u * k + d / 1.525 * Dx, yn + d / 1.525 * Dy - (h - .76) * k)
        it = [E(x0 + Lx / 2 + Dx / 2, yn + Hh + Dy / 2 + 6, Lx / 2 + 40, 22, '#2a1f33', .16)]
        # 后腿
        for u in (.3, 2.44):
            a = q(u, 1.3); it.append(R(a[0] - 5, a[1], 10, Hh - th, 'legs', 3))
        # 台面
        c = [q(0, 0), q(2.74, 0), q(2.74, 1.525), q(0, 1.525)]
        it += [poly(c, 'top'), poly([q(1.37, 0), q(2.74, 0), q(2.74, 1.525), q(1.37, 1.525)], 'top2', .35)]
        b = .02 * 3
        it += [S('M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in [q(b / 2, b / 2), q(2.74 - b / 2, b / 2), q(2.74 - b / 2, 1.525 - b / 2), q(b / 2, 1.525 - b / 2)]) + 'Z', 'line', max(3, .02 * k)),
               S(f'M{q(0, .7625)[0]:.1f},{q(0, .7625)[1]:.1f} L{q(2.74, .7625)[0]:.1f},{q(2.74, .7625)[1]:.1f}', 'line', 2.2, .95)]
        # 台面厚度（正面与右侧）
        it += [poly([q(0, 0), q(2.74, 0), (q(2.74, 0)[0], q(2.74, 0)[1] + th), (q(0, 0)[0], q(0, 0)[1] + th)], 'edge'),
               poly([q(2.74, 0), q(2.74, 1.525), (q(2.74, 1.525)[0], q(2.74, 1.525)[1] + th), (q(2.74, 0)[0], q(2.74, 0)[1] + th)], 'edge', .8)]
        # 前腿 + 底架
        for u in (.3, 2.44):
            a = q(u, .2); it += [R(a[0] - 6, a[1] + th, 12, Hh - th, 'legs', 3), R(a[0] - 18, a[1] + Hh - 6, 36, 8, 'legs', 3)]
        a1 = q(.3, .2); a2 = q(2.44, .2)
        it.append(R(a1[0], a1[1] + Hh * .55, a2[0] - a1[0], 8, 'legs', 3, .8))
        # 球网（高 15.25 cm，两侧各伸出 15.25 cm）
        n0 = q(1.37, -.1525, .76); n1 = q(1.37, 1.525 + .1525, .76); nh = .1525 * k
        it += [poly([n0, n1, (n1[0], n1[1] - nh), (n0[0], n0[1] - nh)], 'net', .8)]
        for j in range(1, 10):
            t = j / 10; xx = n0[0] + (n1[0] - n0[0]) * t; yy = n0[1] + (n1[1] - n0[1]) * t
            it.append(S(f'M{xx:.1f},{yy:.1f} L{xx:.1f},{yy - nh:.1f}', 'netw', 1, .3))
        it += [S(f'M{n0[0]:.1f},{n0[1] - nh:.1f} L{n1[0]:.1f},{n1[1] - nh:.1f}', 'netw', max(3, .015 * k * 2)),
               R(n0[0] - 4, n0[1] - nh - 2, 8, nh + 10, 'metal', 2), R(n1[0] - 4, n1[1] - nh - 2, 8, nh + 10, 'metal', 2)]
        return G(it)
    s.layer('table_back', [table(110, 600, 150)], 'rise', .45)
    s.layer('table_front', [table(1130, 740, 236)], 'rise', .6)

    def paddle(x, y, r, rot, rubber):
        return G([R(x - 7, y + r * .7, 14, r * 1.0, 'handle', 5), E(x, y, r * .92, r, rubber), ER(x, y, r * .92, r, 'paddle2', 3), R(x - 7, y + r * .7, 14, 14, 'paddle2', 3)],
                 f'transform="rotate({rot} {x} {y + r})"')
    s.layer('paddles', [paddle(1290, 690, 34, -70, 'paddle'), paddle(1600, 666, 34, 60, 'paddle2'), C(1460, 682, 8, 'ball'), C(1458, 680, 3, '#ffffff')], 'pop', .85)
    # 翻分牌
    sc = [shadow(960, 912, 110, 8), S('M880,900 L920,760 M1040,900 L1000,760', 'legs', 6), R(870, 690, 180, 120, 'score', 10, extra='filter="url(#shs)"'), R(884, 706, 70, 90, 'frame', 6), R(966, 706, 70, 90, 'frame', 6),
          T(919, 776, '7', 64, 'top', 900), T(1001, 776, '5', 64, 'paddle', 900), R(884, 748, 70, 3, 'score', 0, .4), R(966, 748, 70, 3, 'score', 0, .4), C(960, 690, 8, 'metal')]
    s.layer('scoreboard', sc, 'pop', .8)
    # 发球机 + 球筐
    rb = [shadow(130, 1000, 110, 10), R(60, 900, 140, 90, 'robot', 16), C(80, 996, 10, 'legs'), C(180, 996, 10, 'legs'), P('M70,900 L190,900 L170,800 L90,800Z', 'metal', .55),
          *[C(102 + (k % 4) * 18, 846 - (k // 4) * 16, 8, 'ball2' if k % 3 else 'ball') for k in range(12)], R(124, 740, 14, 70, 'robot', 4), R(100, 720, 66, 34, 'robot', 10), C(170, 737, 8, 'legs')]
    bk = [shadow(400, 1000, 70, 9), P('M340,900 L460,900 L446,996 L354,996Z', 'basket', .9)]
    for k in range(6): bk.append(S(f'M{344 + k * 22},902 L{356 + k * 18},996', 'leg' if False else 'legs', 1.5, .3))
    for k in range(9): bk.append(C(356 + (k % 5) * 22 + (k // 5) * 11, 892 - (k // 5) * 16, 11, 'ball2' if k % 2 else 'ball'))
    s.layer('robot_basket', rb + bk, 'rise', .95)
    s.layer('ball_fly', [C(1060, 520, 9, 'ball2'), C(1035, 532, 6, 'ball2', .35), C(1015, 542, 4, 'ball2', .2)], 'pop', 1.15, loop='bob')
    s.layer('plant', [leafy(1840, 640, .9, 'frame', 'leaf', 'leaf2', 7)], 'grow', 1.05, loop='sway', origin='1840 640')
    return s


# ============ s016 羽毛球馆 ============
def badminton():
    s = Scene('s016', '羽毛球馆', '体育', ['体育', '羽毛球', '协调性', '运动会'],
              dict(wall1='#F6F1E7', wall2='#E9E0CF', panel='#7FB7A4', panel2='#5E9E89', truss='#C8C0B0', win1='#A8DDF7', win2='#EAF8FF', frame='#FFFFFF', wood1='#E2B482', wood2='#CF9C66',
                   mat='#2F8F6A', mat2='#287D5C', line='#FFFFFF', post='#2E3440', net='#2E3440', tape='#FFFFFF', chair='#F2B33D', chair2='#3B4656', cork='#F4E7D3', feather='#FFFFFF', band='#E8574A',
                   racket='#3E8ED0', string='#E8EEF4', lamp='#FFF4CF', metal='#9AA8B3', bag='#E8574A', bottle='#7FC4E8'),
              desc='室内羽毛球馆端线视角：绿色场地胶上双打/单打边线、前发球线、双打后发球线按标准，球网中高 1.524 m，裁判椅与球拍。', stand={'ground_y': 900, 'x': [520, 1400]})
    s.layer('wall', [R(0, 0, W, 560, s.lg([(0, 'wall1'), (1, 'wall2')])), R(0, 380, W, 180, s.lg([(0, 'panel'), (1, 'panel2')])), R(0, 374, W, 8, 'frame', 0, .8)], 'fade', 0)
    tr = [R(0, 0, W, 50, 'truss', 0, .45)]
    for x in range(0, W + 1, 160): tr.append(S(f'M{x},50 L{x + 80},0 L{x + 160},50', 'truss', 5, .8))
    for x in range(60, W, 300): tr.append(sky_window(s, x, 120, 200, 160, 'win1', 'win2', 'frame', [cloud(x + 80, 190, .3)], mull='cross', rx=6, border=10))
    s.layer('roof_windows', tr, 'fade', .1)
    s.layer('lamps', [high_lamp(x, 80, .6) for x in (300, 760, 1160, 1620)], 'drop', .2, loop='glow')
    # 地面：横向 220 px/m；纵深 26 px/m；网下中线 y=720
    ct = Court(960, 720, 220, 26)
    fl = [R(0, 540, W, 540, s.lg([(0, 'wood1'), (1, 'wood2')]))]
    for y in range(556, 1080, 26): fl.append(R(0, y, W, 2, 'wood2', 0, .55))
    fl.append(ct.fillrect(-3.05 - .4, -6.7 - .6, 3.05 + .4, 6.7 + 1.5, 'mat'))
    fl.append(ct.fillrect(-3.05, -6.7, 3.05, 6.7, 'mat2', .35))
    L = 'line'; w = 4
    fl += [ct.rect(-3.05, -6.7, 3.05, 6.7, L, w),                                     # 双打边线 / 端线
           ct.line([(-2.59, -6.7), (-2.59, 6.7)], L, w), ct.line([(2.59, -6.7), (2.59, 6.7)], L, w),   # 单打边线（内收 0.46 m）
           ct.line([(-3.05, 1.98), (3.05, 1.98)], L, w), ct.line([(-3.05, -1.98), (3.05, -1.98)], L, w),   # 前发球线 1.98 m
           ct.line([(-3.05, 5.94), (3.05, 5.94)], L, w), ct.line([(-3.05, -5.94), (3.05, -5.94)], L, w),   # 双打后发球线（距端线 0.76 m）
           ct.line([(0, 1.98), (0, 6.7)], L, w), ct.line([(0, -1.98), (0, -6.7)], L, w)]                   # 中线
    s.layer('court', fl, 'rise', .1)
    # 球网：网柱高 1.55 m，网中央高 1.524 m，网高 0.76 m
    pl = ct.p(-3.05, 0); pr = ct.p(3.05, 0)
    yp = 720 - 1.55 * ct.sx; yc = 720 - 1.524 * ct.sx; nh = .76 * ct.sx
    nt = [shadow(pl[0], 724, 40, 6), shadow(pr[0], 724, 40, 6), R(pl[0] - 22, 712, 44, 14, 'post', 5), R(pr[0] - 22, 712, 44, 14, 'post', 5),
          R(pl[0] - 7, yp - 6, 14, 720 - yp + 6, 'post', 4), R(pr[0] - 7, yp - 6, 14, 720 - yp + 6, 'post', 4)]
    top_d = f'M{pl[0]},{yp} Q960,{2 * yc - yp} {pr[0]},{yp}'
    cp = s.clip(f'<path d="M{pl[0]},{yp} Q960,{2 * yc - yp} {pr[0]},{yp} L{pr[0]},{yp + nh} Q960,{2 * yc - yp + nh} {pl[0]},{yp + nh}Z"/>')
    mesh = [R(pl[0], yp - 10, pr[0] - pl[0], nh + 20, 'net', .05)]
    x = pl[0]
    while x < pr[0]:
        mesh.append(S(f'M{x:.1f},{yp - 10} L{x:.1f},{yp + nh + 10}', 'net', 1.1, .35)); x += 19
    for k in range(1, 40):
        yy = yp - 10 + k * 19
        if yy > yp + nh + 10: break
        mesh.append(S(f'M{pl[0]},{yy} Q960,{yy + 2 * (yc - yp)} {pr[0]},{yy}', 'net', 1.1, .35))
    nt.append(G(mesh, f'clip-path="{cp}"'))
    nt += [S(top_d, 'tape', 16, cap='butt'), S(f'M{pl[0]},{yp + nh} Q960,{2 * yc - yp + nh} {pr[0]},{yp + nh}', 'net', 4)]
    s.layer('net', nt, 'drop', .5)
    # 裁判椅（网柱外侧）
    jx = pr[0] + 130
    jc = [shadow(jx, 724, 70, 8), S(f'M{jx - 50},720 L{jx - 30},460 M{jx + 50},720 L{jx + 30},460', 'chair2', 10), S(f'M{jx - 44},640 L{jx + 44},640 M{jx - 38},560 L{jx + 38},560', 'chair2', 7),
          R(jx - 60, 440, 120, 24, 'chair', 8), R(jx - 54, 360, 108, 84, 'chair', 14), R(jx - 70, 430, 20, 40, 'chair2', 6), R(jx + 50, 430, 20, 40, 'chair2', 6)]
    s.layer('umpire_chair', jc, 'rise', .7)

    def racket(x, y, rot, sc=1):
        it = [E(x, y, 46 * sc, 58 * sc, 'racket'), E(x, y, 40 * sc, 52 * sc, 'string', .55)]
        for k in range(-3, 4): it.append(S(f'M{x + k * 10 * sc},{y - 50 * sc} L{x + k * 10 * sc},{y + 50 * sc}', 'racket', 1, .4))
        for k in range(-4, 5): it.append(S(f'M{x - 40 * sc},{y + k * 11 * sc} L{x + 40 * sc},{y + k * 11 * sc}', 'racket', 1, .4))
        it += [R(x - 3 * sc, y + 58 * sc, 6 * sc, 70 * sc, 'metal', 2), R(x - 9 * sc, y + 124 * sc, 18 * sc, 64 * sc, 'band', 6)]
        return G(it, f'transform="rotate({rot} {x} {y + 120 * sc})"')

    def shuttle(x, y, sc, rot=0):
        return G([P(f'M{x - 26 * sc},{y - 60 * sc} L{x + 26 * sc},{y - 60 * sc} L{x + 10 * sc},{y - 6 * sc} L{x - 10 * sc},{y - 6 * sc}Z', 'feather', .95),
                  *[S(f'M{x + k * 6 * sc},{y - 6 * sc} L{x + k * 13 * sc},{y - 60 * sc}', 'metal', 1.4, .6) for k in range(-2, 3)],
                  S(f'M{x - 18 * sc},{y - 34 * sc} L{x + 18 * sc},{y - 34 * sc}', 'band', 2.5), P(f'M{x - 12 * sc},{y - 8 * sc} L{x + 12 * sc},{y - 8 * sc} Q{x + 12 * sc},{y + 14 * sc} {x},{y + 14 * sc} Q{x - 12 * sc},{y + 14 * sc} {x - 12 * sc},{y - 8 * sc}Z', 'cork')],
                 f'transform="rotate({rot} {x} {y})"')
    s.layer('shuttle_air', [shuttle(1180, 300, 1.1, 150)], 'pop', .9, loop='bob')
    pr_ = [shadow(240, 960, 150, 12), R(110, 900, 260, 60, 'bag', 24), R(130, 886, 220, 20, 'bag', 10, .8), R(150, 920, 180, 8, 'frame', 4, .5), racket(140, 760, -18, .9),
           R(400, 900, 36, 60, 'bottle', 10), R(406, 890, 24, 14, 'frame', 4), R(470, 922, 120, 34, 'frame', 17), R(470, 922, 26, 34, 'band', 12),
           shuttle(1620, 990, .6, 70), shuttle(1700, 1000, .6, -60)]
    s.layer('props', pr_, 'rise', .85)
    return s


# ============ s017 游泳馆 ============
def pool():
    s = Scene('s017', '游泳馆', '体育', ['体育', '游泳', '防溺水', '安全教育'],
              dict(wall1='#EEF8FB', wall2='#D5EDF4', tile='#C3E3EC', roof='#FFFFFF', roof2='#C9DCE6', win1='#9FD9F5', win2='#EAF9FF', deck='#EAF2F4', deck2='#CFE0E6',
                   water1='#7FD3EA', water2='#3BA9D3', water3='#2B8FBE', laneline='#1F5F8B', rope1='#E8473B', rope2='#FFFFFF', rope3='#2F7FC9', rope4='#F7C531',
                   block='#FFFFFF', block2='#2F7FC9', flag1='#E8473B', flag2='#FFFFFF', flag3='#2F7FC9', clock='#FFFFFF', clock2='#2E3440', ring='#FF7A59', chair='#FFFFFF', chair2='#9AA8B3',
                   kick1='#F7C531', kick2='#FF7A59', kick3='#5CCB7A', shine='#FFFFFF', leaf='#5FAE74', leaf2='#9ED38C', pot='#FFFFFF'),
              desc='室内标准泳池（8 道）：出发台、分道线、池底泳道标志线与 T 形端头、两条仰泳转身标志旗、秒表大钟、救生椅与浮板。', stand={'ground_y': 950, 'x': [520, 1400]})
    s.layer('wall', [R(0, 0, W, 600, s.lg([(0, 'wall1'), (1, 'wall2')]))] + [R(0, y, W, 2, 'tile', 0, .8) for y in range(420, 600, 30)] + [R(x, 420, 2, 180, 'tile', 0, .8) for x in range(0, W, 30)], 'fade', 0)
    # 拱形屋顶 + 大窗
    rf = [P('M0,0 L1920,0 L1920,90 Q960,-10 0,90Z', 'roof2')]
    for k, x in enumerate(range(120, 1800, 240)):
        rf.append(sky_window(s, x, 130, 200, 250, 'win1', 'win2', 'roof', [cloud(x + 100, 230, .35), C(x + 60, 400, 80, 'leaf2', .9)], mull='v', rx=100 if False else 8, border=10))
    s.layer('windows', rf, 'fade', .1)
    # 秒表大钟（60 秒刻度，红针）
    cx, cy, r = 960, 250, 110
    ck = [C(cx, cy, r + 14, 'clock2', extra='filter="url(#sh)"'), C(cx, cy, r, 'clock')]
    for k in range(60):
        a = k * math.pi / 30 - math.pi / 2; big = k % 5 == 0
        r0 = r * (.8 if big else .88)
        ck.append(S(f'M{cx + r0 * math.cos(a):.1f},{cy + r0 * math.sin(a):.1f} L{cx + r * .95 * math.cos(a):.1f},{cy + r * .95 * math.sin(a):.1f}', 'clock2', 5 if big else 2))
    for n in range(0, 60, 15):
        a = n * math.pi / 30 - math.pi / 2
        ck.append(T(f'{cx + r * .6 * math.cos(a):.1f}', f'{cy + r * .6 * math.sin(a) + 10:.1f}', str(n if n else 60), 28, 'clock2', 900))
    ck += [S(f'M{cx},{cy} L{cx + r * .85 * math.cos(math.radians(20 * 6 - 90)):.1f},{cy + r * .85 * math.sin(math.radians(20 * 6 - 90)):.1f}', 'rope1', 6), C(cx, cy, 10, 'rope1')]
    s.layer('pace_clock', ck, 'pop', .35)
    # 泳池：近岸 y=880，远端 y=600；轻微汇聚（同十字路口样板的斜线手法）
    vx, vy = 960, 120
    def X(xb, y): return vx + (xb - vx) * (y - vy) / (880 - vy)
    lanes = 8; xL, xR = 160, 1760; lw = (xR - xL) / lanes
    pw = [R(0, 600, W, 480, s.lg([(0, 'deck'), (1, 'deck2')]))]
    pw.append(poly([(X(xL - 20, 590), 590), (X(xR + 20, 590), 590), (xR + 20, 880), (xL - 20, 880)], 'deck2'))
    pw.append(poly([(X(xL, 600), 600), (X(xR, 600), 600), (xR, 872), (xL, 872)], s.lg([(0, 'water1'), (1, 'water2')])))
    # 池底泳道线（每道中央，末端 T 形）
    for k in range(lanes):
        xc = xL + lw * (k + .5)
        pw += [poly([(X(xc - 9, 640), 640), (X(xc + 9, 640), 640), (xc + 9, 850), (xc - 9, 850)], 'laneline', .45),
               poly([(X(xc - 40, 836), 836), (X(xc + 40, 836), 836), (X(xc + 40, 850), 850), (X(xc - 40, 850), 850)], 'laneline', .45),
               poly([(X(xc - 26, 640), 640), (X(xc + 26, 640), 640), (X(xc + 26, 648), 648), (X(xc - 26, 648), 648)], 'laneline', .45),
               R(X(xc - 9, 600), 600, X(xc + 9, 600) - X(xc - 9, 600), 34, 'laneline', 2, .45)]
    s.layer('pool', pw, 'rise', .1)
    random.seed(17)
    s.layer('caustics', [S(f'M{x:.0f},{y:.0f} q24,-8 48,0 t48,0', 'shine', 3, .55) for x, y in [(random.uniform(300, 1600), random.uniform(640, 860)) for _ in range(26)]], 'fade', .6, loop='flow')
    # 分道线（浮标串），两端 5 m 为红色
    rp = []
    for k in range(1, lanes):
        xb = xL + lw * k
        for j in range(34):
            t = j / 33; y = 600 + (872 - 600) * t; x = X(xb, y)
            sc = (y - vy) / (880 - vy)
            col = 'rope1' if (t < .2 or t > .8) else ('rope3' if j % 2 else 'rope2')
            rp.append(E(x, y, 9 * sc, 6 * sc, col))
    rp += [R(X(xL, 600), 596, X(xR, 600) - X(xL, 600), 8, 'deck', 3), R(xL - 20, 872, xR - xL + 40, 16, 'deck', 4)]
    s.layer('lane_ropes', rp, 'fade', .45)
    # 仰泳转身标志旗（距两端 5 m，离水面约 1.8 m）
    fl = []
    for yw, sag in ((812, 12), (640, 8)):
        sc = (yw - vy) / (880 - vy); xa, xb = X(xL - 60, yw), X(xR + 60, yw); yy = yw - 1.8 * 80 * sc
        fl += [R(xa - 4, yy - 6, 8, yw - yy + 6, 'chair2', 3), R(xb - 4, yy - 6, 8, yw - yy + 6, 'chair2', 3)]
        fl += pennants(xa, xb, yy, sag, int(26 * sc + 6), ['flag1', 'flag2', 'flag3'], 13 * sc)
    s.layer('backstroke_flags', fl, 'drop', .7, loop='sway')
    # 出发台（近端，每道一个），台号
    bl = []
    for k in range(lanes):
        xc = xL + lw * (k + .5)
        bl += [shadow(xc, 902, 50, 6), R(xc - 30, 856, 60, 40, 'block2', 6), P(f'M{xc - 44},850 L{xc + 44},850 L{xc + 40},866 L{xc - 40},866Z', 'block'), R(xc - 44, 842, 88, 10, 'block', 4),
               S(f'M{xc - 36},842 L{xc - 36},818 L{xc + 36},818 L{xc + 36},842', 'chair2', 5), T(xc, 888, str(k + 1), 24, 'block', 900)]
    s.layer('blocks', bl, 'rise', .6)
    # 救生椅、救生圈、浮板、扶梯
    lx = 1810
    lg = [shadow(lx, 1000, 70, 8), S(f'M{lx - 50},1000 L{lx - 30},760 M{lx + 50},1000 L{lx + 30},760', 'chair2', 9), S(f'M{lx - 44},920 L{lx + 44},920 M{lx - 38},840 L{lx + 38},840', 'chair2', 6),
          R(lx - 54, 740, 108, 22, 'chair', 8, extra='filter="url(#shs)"'), R(lx - 48, 660, 96, 84, 'chair', 14, extra='filter="url(#shs)"'), S(f'M{lx + 40},700 L{lx + 40},560', 'chair2', 5), P(f'M{lx - 30},570 Q{lx + 40},500 {lx + 110},570Z', 'ring')]
    ring = [C(70, 470, 50, 'ring'), C(70, 470, 28, 'wall2'), *[R(70 - 8, 470 - 50, 16, 22, 'flag2', 3, extra=f'transform="rotate({a} 70 470)"') for a in (0, 90, 180, 270)]]
    kb = [shadow(200, 1006, 110, 8)] + [R(110, 990 - k * 18, 180, 18, ['kick1', 'kick2', 'kick3', 'flag3'][k % 4], 9) for k in range(5)]
    ld = [S(f'M{X(xR - 50, 690):.0f},690 Q{X(xR - 50, 690) + 10:.0f},640 {X(xR - 50, 690) + 30:.0f},640', 'chair2', 6), S(f'M{X(xR - 90, 690):.0f},690 Q{X(xR - 90, 690) + 10:.0f},640 {X(xR - 90, 690) + 30:.0f},640', 'chair2', 6)]
    s.layer('poolside', lg + ring + kb + [leafy(1560, 1030, .9, 'pot', 'leaf', 'leaf2', 7)], 'rise', .85)
    s.layer('sparkle', [star(x, y, 8, 'shine', op=.9) for x, y in [(520, 700), (1300, 760), (900, 650), (1500, 680)]], 'pop', 1.2, loop='twinkle')
    return s


# ============ s018 体操垫区 ============
def gymnastics():
    s = Scene('s018', '体操垫区', '体育', ['体育', '体操', '柔韧性', '前滚翻'],
              dict(wall1='#FBEFE6', wall2='#F2DCCB', panel='#F6C9B1', win1='#A8DDF7', win2='#EAF8FF', frame='#FFFFFF', floor1='#E6BC8A', floor2='#D2A472',
                   bar='#D9A066', bar2='#B57E46', mat1='#4F8FD8', mat2='#3C77BF', mat3='#F2B33D', mat4='#E8674F', mat5='#5CC38F', beam='#E9D6B8', beam2='#8C9BA7', leather='#C8553D',
                   box='#E8C79A', box2='#D4AE7E', spring='#3B4656', strap='#F6EEE2', ring='#C79A5C', hoop1='#FF8FA3', hoop2='#7FC4E8', ball='#9B7DE0', metal='#8C9BA7', lamp='#FFF4CF'),
              desc='体操房：肋木墙、平衡木、跳箱与踏板、吊环，地上铺蓝黄折叠体操垫，适合前滚翻、柔韧与平衡练习。', stand={'ground_y': 900, 'x': [520, 1300]})
    s.layer('wall', [R(0, 0, W, 700, s.lg([(0, 'wall1'), (1, 'wall2')])), R(0, 600, W, 100, 'panel', 0, .6), R(0, 596, W, 8, 'frame', 0, .8)], 'fade', 0)
    s.layer('windows', [sky_window(s, x, 110, 260, 240, 'win1', 'win2', 'frame', [cloud(x + 100, 200, .4), C(x + 210, 380, 100, 'mat5', .45)], mull='cross') for x in (640, 960, 1280)], 'pop', .15)
    s.layer('lamps', [high_lamp(x, 40, .55) for x in (560, 960, 1360)], 'drop', .2, loop='glow')
    fl = [R(0, 700, W, 380, s.lg([(0, 'floor1'), (1, 'floor2')]))] + floor_lines(700, 1080, 'floor2', step=160, op=.45, rows=(760, 840, 940), rowop=.35)
    s.layer('floor', fl, 'rise', .1)
    # 肋木（高约 2.6 m，横档间距约 15 cm）
    wb = []
    for k in range(3):
        x0 = 60 + k * 170
        wb += [R(x0, 140, 18, 570, 'bar2', 6), R(x0 + 140, 140, 18, 570, 'bar2', 6)]
        for j in range(17): wb.append(R(x0 + 12, 170 + j * 32, 134, 12, 'bar', 6))
        wb.append(R(x0 - 6, 128, 170, 16, 'bar2', 6))
    s.layer('wall_bars', [G(wb, 'filter="url(#shs)"')], 'rise', .3)
    # 吊环
    rg = []
    rg += [S('M1760,0 C1750,200 1772,400 1756,600', 'strap', 14), S('M1760,0 C1750,200 1772,400 1756,600', 'bar2', 3, .4), E(1756, 606, 12, 18, 'bar2')]
    for x in (1500, 1620):
        rg += [R(x - 6, 0, 12, 330, 'strap', 4), R(x - 7, 300, 14, 40, 'leather', 4), ER(x, 380, 40, 40, 'ring', 14)]
    s.layer('rings', rg, 'drop', .5, loop='sway', origin='1560 0')
    # 平衡木（长 5 m、宽 10 cm、高 1.25 m；缩放 100 px/m）
    k = 100; bx0, bx1, fy = 760, 760 + 5 * k, 740
    bm = [shadow((bx0 + bx1) / 2, fy + 4, 280, 10), R(bx0, fy - 1.25 * k, 5 * k, 16, 'beam', 6, extra='filter="url(#shs)"'), R(bx0, fy - 1.25 * k + 12, 5 * k, 6, 'beam2', 3, .6)]
    for x in (bx0 + 70, bx1 - 70):
        bm += [R(x - 7, fy - 1.25 * k + 16, 14, 1.25 * k - 30, 'beam2', 4), P(f'M{x - 60},{fy} L{x + 60},{fy} L{x + 40},{fy - 16} L{x - 40},{fy - 16}Z', 'beam2')]
    s.layer('beam', bm, 'rise', .45)
    # 跳箱（6 节，梯形）+ 踏板
    jx, jy = 1500, 880
    bx = [shadow(jx + 120, jy + 6, 200, 14)]
    for j in range(6):
        wt = 180 + j * 16; yy = jy - (j + 1) * 34
        x0 = jx + 120 - wt / 2 - 10
        bx.append(P(f'M{x0},{yy + 34} L{x0 + wt + 20},{yy + 34} L{x0 + wt + 12},{yy} L{x0 + 8},{yy}Z', 'box' if j % 2 else 'box2'))
        bx.append(R(x0 + wt / 2 - 10, yy + 12, 40, 10, 'bar2', 5, .6))
    tp = jy - 6 * 34
    bx = [bx[0]] + list(reversed(bx[1:]))
    bx += [R(jx + 120 - 106, tp - 22, 212, 26, 'leather', 12)]
    bx.insert(1, R(0, 0, 0, 0, 'box'))
    bxs = [bx[0]]
    for j in range(6):
        wt = 260 - j * 16; yy = jy - (j + 1) * 34; x0 = jx + 120 - wt / 2
        bxs += [P(f'M{x0},{yy + 34} L{x0 + wt},{yy + 34} L{x0 + wt - 8},{yy} L{x0 + 8},{yy}Z', 'box' if j % 2 else 'box2'), R(jx + 104, yy + 12, 32, 9, 'bar2', 4, .5)]
    bxs += [R(jx + 120 - 92, tp - 20, 184, 26, 'leather', 12), R(jx + 120 - 80, tp - 16, 160, 6, 'strap', 3, .35)]
    bxs += [P(f'M{jx - 260},{jy} L{jx - 60},{jy} L{jx - 60},{jy - 46} Z', 'mat4'), R(jx - 264, jy - 6, 210, 10, 'spring', 4), R(jx - 112, jy - 40, 46, 34, 'spring', 6, .8)]
    s.layer('vault', bxs, 'rise', .6)
    # 体操垫：折叠垫（4 折）与厚落地垫
    mt = []
    def fold_mat(x, y, w, h, c1, c2, n=4):
        it = [shadow(x + w / 2, y + h + 4, w / 2 + 20, 10, .12), R(x, y, w, h, c1, 12)]
        for k in range(1, n): it.append(R(x + k * w / n - 2, y, 4, h, c2, 0, .9))
        it += [R(x, y, w, 10, '#ffffff', 6, .25), R(x, y + h - 10, w, 10, c2, 6, .6)]
        return G(it)
    mt += [fold_mat(560, 860, 800, 46, 'mat1', 'mat2', 4), fold_mat(160, 900, 520, 40, 'mat3', 'mat4', 3), R(1380, 820, 420, 100, 'mat4', 20, extra='filter="url(#shs)"'), R(1380, 820, 420, 18, '#ffffff', 10, .25),
           S('M1400,870 L1780,870', 'mat3', 4, .6)]
    s.layer('mats', mt, 'rise', .75)
    # 呼啦圈与实心球
    pr = [ER(566, 690, 60, 116, 'hoop1', 12), ER(606, 700, 56, 108, 'hoop2', 12),
          shadow(1860, 946, 40, 7), C(1860, 910, 36, 'ball'), C(1848, 898, 10, '#ffffff', .35), S('M1826,910 Q1860,880 1894,910', 'mat2', 3, .5)]
    s.layer('props', pr, 'pop', .9)
    s.layer('sunlight', [beam(700, 940, 640, 1000, 290, 1000, s, .2), beam(1060, 1300, 1060, 1420, 290, 1000, s, .18)], 'fade', 1.0, loop='glow')
    return s


# ============ s019 武术馆 ============
def wushu():
    s = Scene('s019', '武术馆', '体育', ['体育', '武术', '传统文化', '健身'],
              dict(wall1='#FBEBD3', wall2='#F2D8B4', pillar='#C8392F', pillar2='#A82E26', beam='#8B5A3C', beam2='#6E452D', gold='#E8B84A', gold2='#C8962E', lattice='#8B5A3C', paper='#FFF6E4',
                   floor1='#C99364', floor2='#B07B4F', carpet='#D9534F', carpet2='#C5443F', cline='#FFFFFF', rack='#7A4B2E', blade='#E3E8EE', tassel='#E8473B', staff='#C99A5C',
                   drum='#C8392F', drumtop='#F2DEC0', nail='#E8B84A', lantern='#E8473B', lantern2='#FFB347', dummy='#9C6A43', plaque='#3D2A20', ink='#E8B84A', leaf='#5F9E6E', leaf2='#8CC08E', pot='#E9DCC6'),
              desc='中式武术馆：红柱、斗拱横梁与“武”字匾额、方格花窗，红色比赛地毯，兵器架（刀枪剑棍）、大鼓、木人桩与红灯笼。', stand={'ground_y': 900, 'x': [560, 1360]})
    s.layer('wall', [R(0, 0, W, 760, s.lg([(0, 'wall1'), (1, 'wall2')]))], 'fade', 0)
    # 花窗
    def lat_win(x, y, w, h):
        it = [R(x - 14, y - 14, w + 28, h + 28, 'lattice', 8, extra='filter="url(#shs)"'), R(x, y, w, h, 'paper', 4)]
        for k in range(1, 6): it.append(R(x + k * w / 6 - 3, y, 6, h, 'lattice'))
        for k in range(1, 7): it.append(R(x, y + k * h / 7 - 3, w, 6, 'lattice'))
        it.append(RR(x + w / 2 - 50, y + h / 2 - 50, 100, 100, 'lattice', 10))
        return G(it)
    s.layer('windows', [lat_win(380, 270, 300, 300), lat_win(1240, 270, 300, 300)], 'pop', .2)
    # 横梁、斗拱、匾额
    bm = [R(0, 0, W, 120, s.lg([(0, 'beam2'), (1, 'beam')])), R(0, 110, W, 18, 'gold2')]
    for x in range(40, W, 160):
        bm += [R(x, 128, 80, 22, 'beam', 4), R(x + 14, 148, 52, 18, 'beam2', 4), R(x + 30, 164, 20, 18, 'beam', 3)]
    for x in range(0, W, 80): bm += [R(x + 10, 40, 60, 40, 'pillar2', 6, .6), C(x + 40, 60, 10, 'gold', .8)]
    bm += [R(780, 150, 360, 130, 'gold', 12, extra='filter="url(#sh)"'), R(794, 164, 332, 102, 'plaque', 8), T(960, 248, '武', 84, 'ink', 900),
           S('M800,150 L760,110 M1120,150 L1160,110', 'gold2', 6)]
    s.layer('beam', bm, 'drop', .1)
    # 红柱
    pl = []
    for x in (110, 1750):
        pl += [R(x - 50, 140, 100, 640, s.lg([(0, 'pillar2'), (.45, 'pillar'), (1, 'pillar2')], 0, 0, 1, 0)), R(x - 66, 760, 132, 30, 'gold2', 6), R(x - 58, 140, 116, 20, 'gold', 4)]
    s.layer('pillars', pl, 'rise', .25)
    # 地面 + 比赛地毯（白色边线 5 cm）
    fl = [R(0, 780, W, 300, s.lg([(0, 'floor1'), (1, 'floor2')]))] + floor_lines(780, 1080, 'floor2', step=200, op=.5, rows=(840, 930))
    fl += [P('M300,800 L1620,800 L1760,1060 L160,1060Z', 'carpet'), P('M320,808 L1600,808 L1736,1050 L184,1050Z', 'carpet2', .25),
           S('M330,814 L1590,814 L1720,1044 L200,1044Z', 'cline', 5), ER(960, 920, 160, 34, 'cline', 4, .7)]
    s.layer('floor', fl, 'rise', .1)
    # 兵器架：刀、枪（红缨）、剑、棍
    rk = [shadow(330, 790, 200, 10), R(170, 560, 330, 22, 'rack', 6), R(170, 730, 330, 22, 'rack', 6), R(180, 470, 20, 320, 'rack', 6), R(470, 470, 20, 320, 'rack', 6), R(160, 770, 350, 20, 'rack', 6)]
    # 枪
    rk += [S('M240,770 L240,250', 'staff', 9), P('M240,210 L252,250 L228,250Z', 'blade'), P('M228,250 Q240,300 252,250 Q260,290 240,312 Q220,290 228,250Z', 'tassel')]
    # 棍
    rk += [S('M290,770 L290,280', 'staff', 12), R(284, 280, 12, 20, 'beam2', 4), R(284, 750, 12, 20, 'beam2', 4)]
    # 剑
    rk += [P('M346,330 L354,330 L356,660 L344,660Z', 'blade'), P('M350,300 L358,330 L342,330Z', 'blade'), R(326, 660, 48, 10, 'gold', 4), R(345, 670, 10, 70, 'beam2', 4), C(350, 746, 8, 'gold'), S('M350,750 q-10,30 6,50', 'tassel', 4)]
    # 刀
    rk += [P('M410,330 Q448,420 436,650 L408,650 Z', 'blade'), R(400, 650, 46, 12, 'gold', 4), R(415, 662, 14, 70, 'beam2', 4), S('M422,736 q12,26 -4,48', 'tassel', 4)]
    s.layer('weapon_rack', rk, 'slide-l', .4)
    # 大鼓
    dx, dy = 1500, 620
    dr = [shadow(dx, 790, 160, 12), S(f'M{dx - 120},790 L{dx - 60},560 M{dx + 120},790 L{dx + 60},560', 'rack', 12), S(f'M{dx - 100},720 L{dx + 100},720', 'rack', 10),
          E(dx, dy, 150, 120, 'drum', extra='filter="url(#sh)"'), E(dx, dy, 112, 120, 'drumtop'), ER(dx, dy, 112, 120, 'gold2', 8), E(dx - 20, dy - 30, 40, 50, '#ffffff', .25)]
    for k in range(14):
        a = k * 2 * math.pi / 14; dr.append(C(dx + 128 * math.cos(a), dy + 106 * math.sin(a), 6, 'nail'))
    dr += [S(f'M{dx + 120},{dy + 140} L{dx + 200},{dy + 30}', 'staff', 9), C(dx + 202, dy + 26, 13, 'tassel'), S(f'M{dx + 160},{dy + 150} L{dx + 230},{dy + 50}', 'staff', 9), C(dx + 232, dy + 46, 13, 'tassel')]
    s.layer('drum', dr, 'pop', .55)
    # 木人桩
    mx = 1260
    md = [shadow(mx, 800, 70, 9), R(mx - 34, 430, 68, 370, s.lg([(0, 'beam2'), (.5, 'dummy'), (1, 'beam2')], 0, 0, 1, 0), 30), R(mx - 120, 760, 240, 20, 'rack', 6),
          S(f'M{mx - 20},500 L{mx - 110},470 M{mx + 20},500 L{mx + 110},470', 'dummy', 18), S(f'M{mx},610 L{mx + 80},650', 'dummy', 18), S(f'M{mx - 10},680 Q{mx - 70},700 {mx - 80},770', 'dummy', 18),
          R(mx - 34, 520, 68, 10, 'beam2', 0, .6)]
    s.layer('wooden_dummy', md, 'rise', .7)
    # 灯笼
    ln = []
    for x, y in ((560, 200), (1360, 200)):
        ln += [S(f'M{x},120 L{x},{y - 50}', 'beam2', 3), R(x - 30, y - 56, 60, 14, 'gold2', 4), E(x, y + 10, 62, 60, 'lantern'), E(x, y + 10, 30, 60, 'lantern2', .35),
               S(f'M{x - 54},{y + 10} L{x + 54},{y + 10}', 'gold', 2, .6), R(x - 30, y + 64, 60, 14, 'gold2', 4)] + [S(f'M{x + k * 8},{y + 78} L{x + k * 8},{y + 116}', 'tassel', 3) for k in range(-3, 4)]
    s.layer('lanterns', ln, 'drop', .85, loop='sway')
    s.layer('lantern_glow', [C(560, 210, 110, 'lantern2', .3, 'filter="url(#b20)"'), C(1360, 210, 110, 'lantern2', .3, 'filter="url(#b20)"')], 'fade', 1.0, loop='glow')
    s.layer('plants', [leafy(640, 790, .8, 'pot', 'leaf', 'leaf2', 7), leafy(1840, 1000, 1.0, 'pot', 'leaf', 'leaf2', 9)], 'grow', 1.05, loop='sway')
    return s


# ============ s020 课间跳绳区 ============
def jumprope():
    s = Scene('s020', '课间跳绳区', '体育', ['体育', '跳绳', '课间活动', '健康'],
              dict(sky1='#86D0F3', sky2='#FFF4DE', bld='#FBE6CF', bld2='#F2D0AA', band='#5FB7B0', win='#BFE3F5', win2='#FFFFFF', tree='#5FAE74', tree2='#A2D88E', trunk='#8A5A3A',
                   fence='#F2B33D', ground1='#6CC3A0', ground2='#58AE8C', paint='#FFFFFF', pad1='#F28B6E', pad2='#F7C55E', pad3='#7FC4E8', pad4='#B9A6EE', rack='#3B4656', rope1='#FF6F91',
                   rope2='#FFB347', rope3='#4FA3E8', rope4='#9B7DE0', rope5='#5CCB7A', handle='#FFFFFF', bench='#E8854F', bench2='#C96A3A', bottle='#7FC4E8', sun='#FFE08A', flower='#FF8FA3'),
              desc='课间户外跳绳区：彩色地坪上画着跳房子格与圆圈，跳绳挂架、甩动中的长绳、长椅与水壶，背后教学楼与树。', stand={'ground_y': 900, 'x': [520, 1360]})
    s.layer('sky', [R(0, 0, W, 640, s.lg([(0, 'sky1'), (1, 'sky2')])), C(1680, 130, 64, 'sun'), C(1680, 130, 150, 'sun', .3, 'filter="url(#b40)"')], 'fade', 0)
    s.layer('clouds', [cloud(360, 140, .75, op=.95), cloud(1100, 100, .55, op=.85)], 'slide-l', .2, loop='drift')
    bl = [R(160, 250, 1600, 380, s.lg([(0, 'bld'), (1, 'bld2')]), 6), R(140, 236, 1640, 22, 'band', 6)]
    for r_ in range(3):
        bl.append(R(160, 330 + r_ * 100, 1600, 10, 'band', 0, .5))
        for k in range(17): bl += [R(196 + k * 92, 270 + r_ * 100, 58, 54, 'win', 4), R(196 + k * 92, 270 + r_ * 100, 58, 12, 'win2', 3, .8)]
    s.layer('building', bl, 'rise', .25)
    s.layer('trees', [blob_tree(x, 650, .85 + .12 * (k % 2), 'tree', 'tree2', 'trunk') for k, x in enumerate((70, 360, 1560, 1850))], 'grow', .35, loop='sway')
    fn = [R(0, 600, W, 8, 'fence'), R(0, 640, W, 8, 'fence')] + [R(x, 586, 10, 70, 'fence', 4) for x in range(0, W, 60)]
    s.layer('fence', fn, 'rise', .4)
    # 地坪
    gd = [R(0, 650, W, 430, s.lg([(0, 'ground1'), (1, 'ground2')]))] + floor_lines(650, 1080, 'ground2', step=240, op=.4, rows=(720, 820, 960), rowop=.3)
    # 跳房子（1-2-3-[4|5]-6-[7|8]，每格 0.5 m，纵深压缩）
    hx, hy, cw, ch = 300, 1066, 150, 56
    cells = [(0, 0, '1'), (0, 1, '2'), (0, 2, '3'), (-.5, 3, '4'), (.5, 3, '5'), (0, 4, '6'), (-.5, 5, '7'), (.5, 5, '8')]
    for u, v, n in cells:
        x = hx + u * cw - cw / 2; y = hy - (v + 1) * ch
        gd += [R(x, y, cw, ch, ['pad1', 'pad2', 'pad3', 'pad4'][int(n) % 4], 0, .5), RR(x, y, cw, ch, 'paint', 5),
               T(x + cw / 2, y + ch / 2 + 13, n, 36, 'paint', 900)]
    gd += [E(hx, hy - 6 * ch - 30, cw * .7, ch * .6, 'pad2', .6), ER(hx, hy - 6 * ch - 30, cw * .7, ch * .6, 'paint', 5)]
    # 圆圈跳点
    for k, (x, y) in enumerate([(1500, 990), (1640, 940), (1780, 990), (1640, 1044)]):
        gd += [E(x, y, 56, 22, ['pad1', 'pad3', 'pad2', 'pad4'][k], .7), ER(x, y, 56, 22, 'paint', 4)]
    gd += [ER(960, 900, 330, 46, 'paint', 5, .8, dash='22 16')]
    s.layer('ground', gd, 'rise', .1)
    # 跳绳挂架
    rx0 = 1430
    rk = [shadow(rx0 + 170, 742, 190, 10), R(rx0, 520, 14, 220, 'rack', 6), R(rx0 + 326, 520, 14, 220, 'rack', 6), R(rx0 - 10, 512, 360, 18, 'rack', 8), R(rx0 - 30, 730, 60, 10, 'rack', 4), R(rx0 + 303, 730, 60, 10, 'rack', 4)]
    for k, col in enumerate(['rope1', 'rope2', 'rope3', 'rope4', 'rope5']):
        x = rx0 + 40 + k * 64
        rk += [S(f'M{x},528 C{x - 26},620 {x + 26},640 {x - 6},690', col, 6), S(f'M{x + 20},528 C{x + 46},610 {x + 4},650 {x + 24},700', col, 6),
               R(x - 14, 686, 16, 40, 'handle', 6), R(x + 16, 696, 16, 40, 'handle', 6), R(x - 14, 686, 16, 8, col, 3), R(x + 16, 696, 16, 8, col, 3)]
    s.layer('rope_rack', rk, 'drop', .5, loop='sway')
    # 长绳（两根立桩之间甩动，带运动残影）
    p1, p2 = (620, 760), (1300, 760)
    lr = [shadow(p1[0], 806, 30, 6), shadow(p2[0], 806, 30, 6), R(p1[0] - 10, 700, 20, 104, 'rack', 6), R(p2[0] - 10, 700, 20, 104, 'rack', 6), C(p1[0], 700, 14, 'pad2'), C(p2[0], 700, 14, 'pad2'),
          S(f'M{p1[0]},710 Q960,420 {p2[0]},710', 'rope1', 7, .25), S(f'M{p1[0]},710 Q960,520 {p2[0]},710', 'rope1', 7, .45), S(f'M{p1[0]},710 Q960,350 {p2[0]},710', 'rope1', 8)]
    s.layer('long_rope', lr, 'grow', .7, loop='glow')
    # 长椅 + 水壶 + 毽子
    bx_ = 1500
    bn = [shadow(bx_ + 160, 880, 170, 10), R(bx_, 810, 320, 22, 'bench', 10), R(bx_, 770, 320, 18, 'bench', 9), R(bx_, 792, 320, 6, 'bench2', 3), R(bx_ + 24, 832, 14, 46, 'bench2', 4), R(bx_ + 284, 832, 14, 46, 'bench2', 4),
          R(bx_ + 50, 766, 30, 46, 'bottle', 8), R(bx_ + 56, 754, 18, 14, 'handle', 4), R(bx_ + 100, 774, 28, 38, 'pad1', 8), R(bx_ + 106, 764, 16, 12, 'handle', 4), R(bx_ + 190, 788, 90, 24, 'pad3', 10)]
    jz = [shadow(1180, 1010, 26, 5), E(1180, 1000, 18, 8, 'pad2'), P('M1172,996 L1150,950 L1166,956 L1176,940 L1184,956 L1200,948 L1188,996Z', 'rope1'), P('M1176,996 L1172,960 L1180,948 L1188,962 L1184,996Z', 'rope3')]
    s.layer('bench_props', bn + jz, 'rise', .85)
    s.layer('flowers', [G([S(f'M{x},{y} L{x},{y - 26}', 'tree', 3), C(x, y - 30, 8, 'flower' if k % 2 else 'sun'), C(x, y - 30, 3, '#ffffff')]) for k, (x, y) in enumerate([(30, 660), (60, 670), (1880, 664), (1900, 676), (520, 660), (1400, 662)])], 'grow', 1.0, loop='sway')
    return s


SCENES = [basketball, football, volleyball, tabletennis, badminton, pool, gymnastics, wushu, jumprope]
