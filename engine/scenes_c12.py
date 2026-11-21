"""第 12 类 · 通用讲解台与舞台（任何主题都能用）：s111–s116
讲知识点时切到干净的讲解台，画面中间放大号示意图（cards 的 img/tiles/ban 等）；s114 是答题专用深蓝星空台；
s115 运动会看台适合「情境开场」；s116 舞台幕布适合口诀、总结、颁奖。全部无文字，配色走 palette，可换主题。"""
from core import *
import math, random


def _stage(sid, name, pal, desc, stripe='v'):
    s = Scene(sid, name, '讲解台', ['通用', '讲解', '知识点'], pal, desc=desc, stand={'ground_y': 900, 'x': [300, 1620]})
    s.layer('wall', [R(0, 0, W, 700, 'wall')], 'fade', 0, depth=0)
    if stripe == 'v':
        s.layer('stripes', [R(x, 0, 3, 700, 'line', op=.55) for x in range(96, W, 96)], 'fade', .1, depth=.05)
    else:
        s.layer('stripes', [R(x, 0, 2, 700, 'line', op=.45) for x in range(80, W, 80)] + [R(0, y, W, 2, 'line', op=.45) for y in range(80, 700, 80)], 'fade', .1, depth=.05)
    s.layer('floor', [R(0, 700, W, 380, 'floor')] + [S(f'M{x},700 L{x - 120},1080', 'floor2', 3, .6) for x in range(120, W + 200, 120)], 'rise', .2, depth=.6)
    s.layer('skirting', [R(0, 692, W, 12, 'floor2', op=.8)], 'fade', .3, depth=.6)
    return s

def s111():
    return _stage('s111', '薄荷讲解台', dict(wall='#DDEFE8', line='#C7E2D8', floor='#BCCFD8', floor2='#A9BEC9'),
                  '浅薄荷绿竖条墙 + 灰蓝地面的干净讲解台，留白多，适合放大号示意图、图标宫格、标签条讲知识点（医学、急救、卫生、安全）。')

def s112():
    return _stage('s112', '暖杏讲解台', dict(wall='#FBEBDC', line='#F3DCC6', floor='#E6CDB4', floor2='#D6B99D'),
                  '暖杏色竖条墙 + 浅木色地面的讲解台，温暖柔和，适合生活习惯、饮食、情绪、家庭类知识点。')

def s113():
    return _stage('s113', '蓝格讲解板', dict(wall='#E3EEFB', line='#CADCF3', floor='#C3CFE0', floor2='#AEBCD1'),
                  '淡蓝方格纸背景 + 灰蓝地面，像一张大方格讲解板，适合数学、科学、步骤图、数据图解。', stripe='g')

def s114():
    s = Scene('s114', '深蓝星空答题台', '讲解台', ['通用', '答题', '考考你'], dict(bg1='#1E2F5C', bg2='#26396B', star='#FFFFFF', glow='#3B5394'),
              desc='深蓝渐变底 + 闪烁小星星，答题镜头专用（「考考你」题条 + 选项卡片 + 倒数圆环）。', stand={'ground_y': 900, 'x': [300, 1620]})
    s.layer('bg', [R(0, 0, W, H, s.lg([(0, 'bg1'), (1, 'bg2')]))], 'fade', 0, depth=0)
    s.layer('glow', [C(960, 1180, 700, 'glow', .35, 'filter="url(#b40)"')], 'fade', .1, depth=.1)
    random.seed(4); st = []
    for _ in range(26):
        x, y, r = random.uniform(40, W - 40), random.uniform(40, H - 40), random.uniform(5, 10)
        st.append(P(f'M{x},{y - r} L{x + r * .25},{y - r * .25} L{x + r},{y} L{x + r * .25},{y + r * .25} L{x},{y + r} L{x - r * .25},{y + r * .25} L{x - r},{y} L{x - r * .25},{y - r * .25}Z', 'star', .35))
    s.layer('stars', st, 'fade', .2, loop='twinkle', depth=.2)
    return s

def s115():
    s = Scene('s115', '运动会看台', '讲解台', ['通用', '体育', '运动会', '情境开场'],
              dict(sky='#9ED0F2', stand='#36477A', stand2='#2D3C68', d1='#E8504A', d2='#F6C33B', d3='#4FA3E3', d4='#FFFFFF', track='#D5644A', lane='#F6E9E2',
                   f1='#E8504A', f2='#F6C33B', f3='#4FA3E3', f4='#5BBE6A', post='#222222', post2='#FFFFFF'),
              desc='彩旗串 + 彩点人群看台 + 红色跑道：校运会、体育课受伤、比赛情境开场。', stand={'ground_y': 900, 'x': [300, 1620]})
    s.layer('sky', [R(0, 0, W, 360, 'sky')], 'fade', 0, depth=0)
    fl = []
    for row, y0 in enumerate((95, 185)):
        fl.append(S(f'M-20,{y0} Q960,{y0 + 40} 1940,{y0 - 10}', '#FFFFFF', 2, .8))
        for i in range(24):
            x = -10 + i * 82 + row * 40; y = y0 + 40 * 4 * (x / 1920) * (1 - x / 1920) * .25 + 4
            fl.append(poly([(x, y), (x + 44, y), (x + 22, y + 44)], ['f1', 'f2', 'f3', 'f4'][(i + row) % 4]))
    s.layer('flags', fl, 'drop', .2, loop='sway', origin='960 100', depth=.15)
    dots = [R(0, 330, W, 270, 'stand'), R(0, 560, W, 40, 'stand2')]
    for r in range(4):
        for i in range(42):
            dots.append(C(25 + i * 46 + (r % 2) * 23, 370 + r * 52, 15, ['d1', 'd2', 'd3', 'd4'][(i * 7 + r * 3) % 4]))
    s.layer('crowd', dots, 'rise', .35, loop='twinkle', depth=.3)
    s.layer('track', [R(0, 600, W, 480, 'track')] + [R(0, y, W, 6, 'lane') for y in (650, 740, 830, 925, 1020)], 'rise', .5, depth=.6)
    s.layer('post', [R(1500, 600, 12, 320, 'post2')] + [R(1496, 620 + j * 40, 20, 18, 'post') for j in range(7)], 'pop', .8, depth=.62)
    return s

def s116():
    s = Scene('s116', '舞台幕布', '讲解台', ['通用', '总结', '口诀', '颁奖'],
              dict(bg='#3B2A4F', cur='#C8343A', cur2='#A3262D', val='#E2B04A', floor='#8A5A3C', floor2='#73492F', beam='#FFF4D6'),
              desc='红色幕布 + 金色帷幔 + 木地板舞台 + 聚光，用于口诀、总结、表彰的收尾镜头。', stand={'ground_y': 900, 'x': [400, 1520]})
    s.layer('bg', [R(0, 0, W, H, 'bg')], 'fade', 0, depth=0)
    s.layer('beam', [poly([(860, 0), (1060, 0), (1500, 900), (420, 900)], 'beam', .16)], 'fade', .6, loop='glow', depth=.2)
    s.layer('floor', [R(0, 840, W, 240, 'floor')] + [R(0, y, W, 4, 'floor2') for y in (880, 940, 1010)], 'rise', .2, depth=.6)
    cl = [P(f'M0,0 L{300 + 20 * i},0 Q{220 + 10 * i},{500} {320 + 20 * i},{900} L0,900Z', 'cur' if i % 2 == 0 else 'cur2') for i in range(3)]
    cr = [P(f'M{W},0 L{W - 300 - 20 * i},0 Q{W - 220 - 10 * i},{500} {W - 320 - 20 * i},{900} L{W},900Z', 'cur' if i % 2 == 0 else 'cur2') for i in range(3)]
    s.layer('curtain_l', cl, 'slide-l', .3, loop='sway', origin='0 0', depth=.9)
    s.layer('curtain_r', cr, 'slide-r', .3, loop='sway', origin=f'{W} 0', depth=.9)
    s.layer('valance', [R(0, 0, W, 90, 'cur2')] + [C(60 + i * 120, 90, 60, 'cur') for i in range(17)] + [R(0, 84, W, 10, 'val')], 'drop', .5, depth=.95)
    return s

SCENES = [s111, s112, s113, s114, s115, s116]
