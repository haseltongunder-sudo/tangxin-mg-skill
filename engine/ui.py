"""MG 信息组件（compose.py 调用）——全部是可选积木，按主题自由搭配，不强制使用。

卡片新样式（写在 shot.cards 里，和 list/chips/steps/compare/big 并列；坐标都按 1920×1080）：
  tag    标签条：items 每条一行，逐条从左滑入堆叠。前缀定颜色：ok: 绿、no: 红、warn: 橙、i: 深蓝，无前缀用 color。
         字段 x y（第一条左上角）、gap 间隔、size 字号、stack 行距（默认 92）
  tiles  图标宫格：items 写 "图标名:文字"（或 "图片路径|文字"），cols 列数、cell 格子边长（默认 190）
         图标名：burst 剧痛 swell 肿胀 deform 变形 ban 禁止 ok no warn phone fire drop clock eye hand heart star bolt home book bell mask water sun moon
  ban    禁止图标组：items 写 "文字" 或 "图片路径|文字"，每个画红圈斜杠，下面标签；r 半径（默认 95）
  board  口诀板：title 标题，items 逐行出现，带彩色编号；行首写 "!" 这一行变红强调；w 宽度
  mark   圈注：x y 圆心、r 半径、label 小标签（黄色），可用来标关节、按钮、部位
  pain   痛点闪烁：x y、r，红色爆炸星 + 扩散圈（受伤、疼痛、危险点）
  img    道具/示意图：src 图片（PNG 透明底），x y 左上角、w 宽；enter: pop | fade | rise | wipe_l | wipe_r | wipe_d（逐渐画出来，适合包扎、画线、分步出现）
         多张 img 按 t 先后出现，就是分步示意动画
  arrow  箭头：from [x,y] to [x,y]，color、width，边画边出现

答题镜头新样式：quiz.style = "kit"（配 s114 深蓝星空台最好）
  顶部「考考你①」题条（no 题号）+ 急救箱式选项卡。每张卡中间的大图按优先级：
  option_imgs（插图路径）> option_icons（上面的矢量图标名）> option_glyphs（大字/符号，如 "火"、"119"；emoji 需系统有彩色 emoji 字体）
  > 都没有时自动画大号字母徽章（A/B/C），不会出现空白卡。color 改题条和徽章主色（默认 ACCENT）。
  + 卡片右侧倒数圆环；揭晓时正确卡上浮打绿勾，其余变灰。q 里可用 \\n 换行。
"""
import os, math
from PIL import Image, ImageDraw, ImageFilter

D = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(D, 'fonts', 'NotoSansSC-800.woff')
from PIL import ImageFont
_FC = {}
def F(sz):
    sz = max(8, int(sz))
    if sz not in _FC: _FC[sz] = ImageFont.truetype(FONT, sz)
    return _FC[sz]
def hexc(c):
    if isinstance(c, (list, tuple)): return tuple(c[:3])
    c = c.lstrip('#'); return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))
# 默认主色：中性教学蓝。消防/急救题材用 "fire"（#E8483B）或直接给颜色；compose/assemble 读 json 顶层 "accent"
ACCENTS = {'blue': '#2F6FDE', 'fire': '#E8483B', 'red': '#E8483B', 'green': '#2E9E5B', 'orange': '#F08A24', 'purple': '#7A5AF0', 'navy': '#22345F'}
ACCENT = '#2F6FDE'
def set_accent(c):
    global ACCENT
    if c: ACCENT = ACCENTS.get(c, c)
    return ACCENT
def eo(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def eb(u): u = max(0, min(1, u)); c = 1.70158; return 1 + (c + 1) * (u - 1) ** 3 + c * (u - 1) ** 2

COL = {'ok': (46, 158, 91), 'no': (226, 64, 52), 'warn': (240, 138, 36), 'i': (34, 52, 98), 'red': (226, 64, 52)}
NAVY = (30, 44, 86); CREAM = (252, 248, 238); INK = (40, 42, 58)
_IMG = {}
def _load(p, base):
    p = p if os.path.isabs(p) else os.path.join(base or '.', p)
    if p not in _IMG: _IMG[p] = Image.open(p).convert('RGBA')
    return _IMG[p]

def _shadow(img, box, r, k, op=70, blur=10, dy=8):
    sh = Image.new('RGBA', img.size, (0, 0, 0, 0)); x0, y0, x1, y1 = box
    ImageDraw.Draw(sh).rounded_rectangle((x0, y0 + dy * k, x1, y1 + dy * k), r, fill=(30, 30, 50, op))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur * k)))

def _cross(d, cx, cy, s, col='white'):
    w = s * .32; d.rectangle((cx - w / 2, cy - s / 2, cx + w / 2, cy + s / 2), fill=col); d.rectangle((cx - s / 2, cy - w / 2, cx + s / 2, cy + w / 2), fill=col)

# ---------------- 图标（矢量画，任意主题通用） ----------------
def icon(d, name, cx, cy, s, col=None):
    """在 (cx,cy) 画边长约 s 的图标"""
    r = s / 2; lw = max(2, int(s * .09))
    if name == 'burst':
        c = col or (232, 72, 59); d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=c)
        pts = []
        for i in range(16):
            a = math.radians(i * 22.5); rr = r * (.75 if i % 2 == 0 else .38); pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        d.polygon(pts, fill='white'); d.ellipse((cx - r * .2, cy - r * .2, cx + r * .2, cy + r * .2), fill=c)
    elif name == 'swell':
        c = col or (240, 138, 36); d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=c); d.ellipse((cx - r * .55, cy - r * .42, cx + r * .55, cy + r * .42), outline='white', width=lw)
    elif name == 'deform':
        c = col or (142, 84, 200); d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=c); d.line([(cx - r * .45, cy + r * .2), (cx, cy - r * .3), (cx + r * .45, cy + r * .2)], fill='white', width=lw, joint='curve')
    elif name in ('ban', 'still'):
        c = col or NAVY; d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=c); q = r * .5
        d.ellipse((cx - q, cy - q, cx + q, cy + q), outline='white', width=lw); d.line([(cx - q * .7, cy - q * .7), (cx + q * .7, cy + q * .7)], fill='white', width=lw)
    elif name == 'ok':
        c = col or COL['ok']; d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=c); d.line([(cx - r * .45, cy), (cx - r * .1, cy + r * .35), (cx + r * .48, cy - r * .35)], fill='white', width=lw, joint='curve')
    elif name == 'no':
        c = col or COL['no']; d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=c); q = r * .4
        d.line([(cx - q, cy - q), (cx + q, cy + q)], fill='white', width=lw); d.line([(cx - q, cy + q), (cx + q, cy - q)], fill='white', width=lw)
    elif name == 'warn':
        c = col or COL['warn']; d.polygon([(cx, cy - r), (cx + r, cy + r * .8), (cx - r, cy + r * .8)], fill=c); d.text((cx, cy + r * .2), '!', font=F(s * .6), fill='white', anchor='mm')
    elif name == 'phone':
        c = col or (46, 158, 91); d.rounded_rectangle((cx - r * .55, cy - r, cx + r * .55, cy + r), r * .2, fill=c); d.rounded_rectangle((cx - r * .42, cy - r * .78, cx + r * .42, cy + r * .6), r * .08, fill='white')
        d.ellipse((cx - r * .1, cy + r * .7, cx + r * .1, cy + r * .9), fill='white')
    elif name == 'fire':
        c = col or (242, 98, 46)
        d.polygon([(cx, cy - r), (cx + r * .55, cy - r * .1), (cx + r * .6, cy + r * .4), (cx + r * .3, cy + r * .9), (cx - r * .3, cy + r * .9), (cx - r * .6, cy + r * .4), (cx - r * .45, cy - r * .2), (cx - r * .15, cy + r * .05)], fill=c)
        d.ellipse((cx - r * .3, cy + r * .2, cx + r * .3, cy + r * .85), fill=(255, 210, 90))
    elif name in ('drop', 'water'):
        c = col or (66, 150, 230); d.polygon([(cx, cy - r), (cx + r * .7, cy + r * .2), (cx - r * .7, cy + r * .2)], fill=c); d.ellipse((cx - r * .7, cy - r * .3, cx + r * .7, cy + r * .95), fill=c)
    elif name == 'clock':
        c = col or NAVY; d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=c, width=lw); d.line([(cx, cy), (cx, cy - r * .6)], fill=c, width=lw); d.line([(cx, cy), (cx + r * .45, cy + r * .2)], fill=c, width=lw)
    elif name == 'eye':
        c = col or NAVY; d.ellipse((cx - r, cy - r * .55, cx + r, cy + r * .55), outline=c, width=lw); d.ellipse((cx - r * .3, cy - r * .3, cx + r * .3, cy + r * .3), fill=c)
    elif name == 'hand':
        c = col or (240, 170, 120)
        d.rounded_rectangle((cx - r * .55, cy - r * .1, cx + r * .55, cy + r), r * .25, fill=c)
        for i in range(4): x = cx - r * .5 + i * r * .33; d.rounded_rectangle((x, cy - r * .9 + abs(i - 1.5) * r * .12, x + r * .26, cy + r * .1), r * .13, fill=c)
    elif name == 'heart':
        c = col or (232, 72, 59); d.ellipse((cx - r, cy - r * .7, cx, cy + r * .3), fill=c); d.ellipse((cx, cy - r * .7, cx + r, cy + r * .3), fill=c); d.polygon([(cx - r * .97, cy - r * .1), (cx + r * .97, cy - r * .1), (cx, cy + r)], fill=c)
    elif name == 'star':
        c = col or (246, 190, 50); pts = []
        for i in range(10): a = math.radians(-90 + i * 36); rr = r if i % 2 == 0 else r * .45; pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        d.polygon(pts, fill=c)
    elif name == 'bolt':
        c = col or (246, 190, 50); d.polygon([(cx + r * .2, cy - r), (cx - r * .55, cy + r * .1), (cx - r * .05, cy + r * .1), (cx - r * .2, cy + r), (cx + r * .55, cy - r * .1), (cx + r * .05, cy - r * .1)], fill=c)
    elif name == 'home':
        c = col or NAVY; d.polygon([(cx, cy - r), (cx + r, cy - r * .05), (cx - r, cy - r * .05)], fill=c); d.rectangle((cx - r * .7, cy - r * .1, cx + r * .7, cy + r), fill=c); d.rectangle((cx - r * .18, cy + r * .35, cx + r * .18, cy + r), fill='white')
    elif name == 'book':
        c = col or (47, 111, 208); d.polygon([(cx - r, cy - r * .7), (cx, cy - r * .5), (cx, cy + r * .9), (cx - r, cy + r * .7)], fill=c); d.polygon([(cx + r, cy - r * .7), (cx, cy - r * .5), (cx, cy + r * .9), (cx + r, cy + r * .7)], fill=tuple(min(255, v + 40) for v in c))
    elif name == 'bell':
        c = col or (246, 170, 40); d.pieslice((cx - r * .8, cy - r, cx + r * .8, cy + r * .6), 180, 360, fill=c); d.rectangle((cx - r * .8, cy - r * .2, cx + r * .8, cy + r * .5), fill=c); d.ellipse((cx - r * .2, cy + r * .5, cx + r * .2, cy + r * .9), fill=c)
    elif name == 'mask':
        c = col or (120, 190, 230); d.rounded_rectangle((cx - r * .8, cy - r * .5, cx + r * .8, cy + r * .5), r * .3, fill=c)
        for y in (-.15, .15): d.line([(cx - r * .55, cy + r * y), (cx + r * .55, cy + r * y)], fill='white', width=max(2, lw // 2))
        d.line([(cx - r * .8, cy - r * .3), (cx - r, cy - r * .5)], fill=c, width=lw); d.line([(cx + r * .8, cy - r * .3), (cx + r, cy - r * .5)], fill=c, width=lw)
    elif name == 'sun':
        c = col or (246, 190, 50); d.ellipse((cx - r * .5, cy - r * .5, cx + r * .5, cy + r * .5), fill=c)
        for i in range(8): a = math.radians(i * 45); d.line([(cx + r * .65 * math.cos(a), cy + r * .65 * math.sin(a)), (cx + r * .95 * math.cos(a), cy + r * .95 * math.sin(a))], fill=c, width=lw)
    elif name == 'moon':
        c = col or (246, 200, 80); d.ellipse((cx - r * .8, cy - r * .8, cx + r * .8, cy + r * .8), fill=c); d.ellipse((cx - r * .4, cy - r * .95, cx + r * 1.1, cy + r * .55), fill=(255, 255, 255, 0))
    else:
        c = col or NAVY; d.ellipse((cx - r * .4, cy - r * .4, cx + r * .4, cy + r * .4), fill=c)

def _icon_or_img(img, d, spec, cx, cy, s, base):
    if spec and ('/' in spec or spec.endswith('.png')):
        im = _load(spec, base); sc = s / max(im.size); im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS)
        img.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))
    else: icon(d, spec, cx, cy, s)

def _split(it, sep):
    return it.split(sep, 1) if sep in it else (None, it)

def _alpha(im, a):
    if a >= 1: return im
    im = im.copy(); im.putalpha(im.split()[3].point(lambda v: int(v * a))); return im

# ---------------- 各组件 ----------------
def _tag_img(kind, txt, k, size, main):
    col = COL.get(kind, main); f = F(size * k); tw = ImageDraw.Draw(Image.new('RGBA', (1, 1))).textlength(txt, font=f)
    h = size * 1.75 * k; bw = h * .78; w = 14 * k + bw + 22 * k + tw + 30 * k; pad = 16 * k
    img = Image.new('RGBA', (int(w + pad * 2), int(h + pad * 2)), (0, 0, 0, 0)); _shadow(img, (pad, pad, pad + w, pad + h), 4 * k, k, 60, 6, 5)
    d = ImageDraw.Draw(img); x0, y0 = pad, pad
    d.rectangle((x0, y0, x0 + w, y0 + h), fill=CREAM)
    d.rectangle((x0, y0 - 3 * k, x0 + 9 * k, y0 + h + 3 * k), fill=col); d.rectangle((x0 + w - 9 * k, y0 - 3 * k, x0 + w, y0 + h + 3 * k), fill=col)
    bx = x0 + 16 * k; d.rounded_rectangle((bx, y0 + (h - bw) / 2, bx + bw, y0 + (h + bw) / 2), 8 * k, fill=col)
    gl = {'ok': 'ok', 'no': 'no', 'warn': 'warn'}.get(kind)
    if gl == 'ok': d.line([(bx + bw * .28, y0 + h / 2), (bx + bw * .45, y0 + h / 2 + bw * .17), (bx + bw * .74, y0 + h / 2 - bw * .17)], fill='white', width=max(2, int(bw * .1)))
    elif gl == 'no': q = bw * .17; d.line([(bx + bw / 2 - q, y0 + h / 2 - q), (bx + bw / 2 + q, y0 + h / 2 + q)], fill='white', width=max(2, int(bw * .1))); d.line([(bx + bw / 2 - q, y0 + h / 2 + q), (bx + bw / 2 + q, y0 + h / 2 - q)], fill='white', width=max(2, int(bw * .1)))
    elif gl == 'warn': d.text((bx + bw / 2, y0 + h / 2 + bw * .06), '!', font=F(bw * .6), fill='white', anchor='mm')
    else: _cross(d, bx + bw / 2, y0 + h / 2, bw * .58)
    d.text((bx + bw + 22 * k, y0 + h / 2), txt, font=f, fill=INK, anchor='lm')
    return img, pad

def draw_ext(fr, c, t, k, t0, t1, base=None):
    st = c['style']; main = hexc(c.get('color') or ACCENT); gap = c.get('gap', .5)
    fade = 1 if not c.get('d') else max(0, min(1, (t1 - t) / .3))
    if fade <= 0: return
    if st == 'tag':
        y = c.get('y', 120)
        for i, it in enumerate(c.get('items', [])):
            ti = t0 + i * gap
            if t < ti: break
            kind, txt = (it.split(':', 1) if ':' in it and it.split(':', 1)[0] in COL else (None, it))
            key = ('tag', it, k, c.get('size', 34), main)
            if key not in _IMG: _IMG[key] = _tag_img(kind, txt, k, c.get('size', 34), main)
            im, pad = _IMG[key]; u = eo((t - ti) / .4)
            x = c.get('x', 100) * k - pad - (1 - u) * 60 * k
            fr.alpha_composite(_alpha(im, min(1, u * 1.5) * fade), (int(x), int(y * k - pad)))
            y += c.get('stack', 92)
    elif st == 'tiles':
        its = c.get('items', []); cols = c.get('cols', len(its)); cell = c.get('cell', 190); g = 26
        for i, it in enumerate(its):
            ti = t0 + i * gap
            if t < ti: break
            ic, txt = (it.split('|', 1) if '|' in it else it.split(':', 1) if ':' in it else (None, it))
            cx = (c.get('x', 100) + (i % cols) * (cell + g)) * k; cy = (c.get('y', 120) + (i // cols) * (cell + g)) * k
            u = (t - ti) / .45; sc = .6 + .4 * eb(u); a = min(1, u * 2) * fade
            sz = int(cell * k); pad = int(16 * k); im = Image.new('RGBA', (sz + pad * 2, sz + pad * 2), (0, 0, 0, 0)); _shadow(im, (pad, pad, pad + sz, pad + sz), 22 * k, k, 55)
            d = ImageDraw.Draw(im); d.rounded_rectangle((pad, pad, pad + sz, pad + sz), 22 * k, fill=CREAM)
            _icon_or_img(im, d, ic, pad + sz / 2, pad + sz * .4, sz * .38, base)
            d.text((pad + sz / 2, pad + sz * .8), txt, font=F(c.get('size', 34) * k), fill=INK, anchor='mm')
            if sc != 1: im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS)
            fr.alpha_composite(_alpha(im, a), (int(cx + sz / 2 + pad - im.width / 2 - pad), int(cy + sz / 2 + pad - im.height / 2 - pad)))
    elif st == 'ban':
        its = c.get('items', []); R = c.get('r', 95); g = c.get('spacing', R * 2 + 70)
        for i, it in enumerate(its):
            ti = t0 + i * gap
            if t < ti: break
            pic, txt = _split(it, '|'); cx = (c.get('x', 200) + i * g) * k; cy = c.get('y', 300) * k; r = R * k
            u = (t - ti) / .45; sc = .5 + .5 * eb(u); a = min(1, u * 2) * fade
            sz = int(r * 2 + 30 * k); im = Image.new('RGBA', (sz, int(sz + 90 * k)), (0, 0, 0, 0)); d = ImageDraw.Draw(im); o = 15 * k
            d.ellipse((o, o, o + 2 * r, o + 2 * r), fill=(255, 238, 230))
            if pic: _icon_or_img(im, d, pic, o + r, o + r, r * 1.3, base)
            lw = int(r * .14); d.ellipse((o, o, o + 2 * r, o + 2 * r), outline=COL['no'], width=lw)
            q = r * .7; d.line([(o + r - q, o + r - q), (o + r + q, o + r + q)], fill=COL['no'], width=lw)
            if txt:
                f = F(c.get('size', 28) * k); tw = d.textlength(txt, font=f); yy = o + 2 * r + 34 * k
                d.rectangle((sz / 2 - tw / 2 - 14 * k, yy - 22 * k, sz / 2 + tw / 2 + 14 * k, yy + 22 * k), fill=CREAM)
                d.rectangle((sz / 2 - tw / 2 - 14 * k, yy - 22 * k, sz / 2 - tw / 2 - 9 * k, yy + 22 * k), fill=COL['no']); d.rectangle((sz / 2 + tw / 2 + 9 * k, yy - 22 * k, sz / 2 + tw / 2 + 14 * k, yy + 22 * k), fill=COL['no'])
                d.text((sz / 2, yy), txt, font=f, fill=INK, anchor='mm')
            if sc != 1: im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS)
            fr.alpha_composite(_alpha(im, a), (int(cx - im.width / 2), int(cy - im.width / 2)))
    elif st == 'board':
        its = c.get('items', []); Wd = c.get('w', 760) * k; hh = 78 * k; lh = c.get('line', 74) * k; pad = 20 * k
        H = hh + 30 * k + lh * len(its) + 20 * k; x0, y0 = c.get('x', 100) * k, c.get('y', 80) * k
        u = (t - t0) / .45; a = min(1, u * 2) * fade
        im = Image.new('RGBA', (int(Wd + pad * 2), int(H + pad * 2)), (0, 0, 0, 0)); _shadow(im, (pad, pad, pad + Wd, pad + H), 20 * k, k, 70)
        d = ImageDraw.Draw(im); d.rounded_rectangle((pad, pad, pad + Wd, pad + H), 20 * k, fill=CREAM)
        hc = hexc(c.get('head', NAVY)); d.rounded_rectangle((pad, pad, pad + Wd, pad + hh), 20 * k, fill=hc); d.rectangle((pad, pad + hh - 20 * k, pad + Wd, pad + hh), fill=hc)
        (_cross(d, pad + 40 * k, pad + hh / 2, 30 * k) if c.get('cross', True) else None); d.text((pad + Wd / 2, pad + hh / 2), c.get('title', ''), font=F(38 * k), fill='white', anchor='mm')
        cols = [(226, 64, 52), (34, 52, 98), (186, 120, 50), (60, 170, 130), (142, 84, 200), (47, 111, 208)]
        for i, it in enumerate(its):
            ti = c['times'][i] if c.get('times') and i < len(c['times']) else t0 + .4 + i * gap  # times：逐条指定出现时刻（与朗读对齐）
            if t < ti: break
            hl = it.startswith('!'); txt = it[1:] if hl else it; yy = pad + hh + 30 * k + i * lh + lh / 2
            v = eo((t - ti) / .35); bx = pad + 48 * k - (1 - v) * 30 * k
            lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
            ld.rounded_rectangle((bx, yy - 19 * k, bx + 38 * k, yy + 19 * k), 7 * k, fill=cols[i % len(cols)]); ld.text((bx + 19 * k, yy), str(i + 1), font=F(24 * k), fill='white', anchor='mm')
            ld.text((bx + 60 * k, yy), txt, font=F(c.get('size', 40) * k), fill=COL['red'] if hl else INK, anchor='lm')
            im.alpha_composite(_alpha(lay, v))
        sc = .85 + .15 * eb(u)
        if sc != 1: im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS)
        fr.alpha_composite(_alpha(im, a), (int(x0 - pad + (Wd + 2 * pad - im.width) / 2), int(y0 - pad + (H + 2 * pad - im.height) / 2)))
    elif st == 'mark':
        u = eo((t - t0) / .5); a = min(1, u * 2) * fade; r = c.get('r', 70) * k * (.6 + .4 * u); x, y = c['x'] * k, c['y'] * k
        lay = Image.new('RGBA', fr.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay); col = hexc(c.get('color', '#F6C33B'))
        d.ellipse((x - r, y - r, x + r, y + r), outline=col + (int(255 * a),), width=int(6 * k))
        if c.get('label'):
            f = F(c.get('size', 28) * k); tw = d.textlength(c['label'], font=f); ly = y - c.get('r', 70) * k - 40 * k
            d.rounded_rectangle((x - tw / 2 - 16 * k, ly - 22 * k, x + tw / 2 + 16 * k, ly + 22 * k), 12 * k, fill=col + (int(255 * a),))
            d.text((x, ly), c['label'], font=f, fill=INK + (int(255 * a),), anchor='mm')
        fr.alpha_composite(lay)
    elif st == 'pain':
        x, y, r = c['x'] * k, c['y'] * k, c.get('r', 60) * k; ph = (t - t0) * 2.2
        lay = Image.new('RGBA', fr.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        for j in range(2):
            p = (ph + j * .5) % 1; rr = r * (1 + p * 1.1); d.ellipse((x - rr, y - rr, x + rr, y + rr), outline=(232, 72, 59, int(160 * (1 - p) * fade)), width=int(4 * k))
        s = 1 + .12 * math.sin((t - t0) * 12); pts = []
        for i in range(16):
            a_ = math.radians(i * 22.5 + 8); rr = r * s * (1 if i % 2 == 0 else .48); pts.append((x + rr * math.cos(a_), y + rr * math.sin(a_)))
        d.polygon(pts, fill=(232, 72, 59, int(225 * min(1, (t - t0) * 4) * fade)))
        fr.alpha_composite(lay)
    elif st == 'img':
        im = _load(c['src'], base); w = c.get('w', im.width) * k; sc = w / im.width; im = im.resize((max(1, int(w)), max(1, int(im.height * sc))), Image.LANCZOS)
        en = c.get('enter', 'pop'); u = (t - t0) / c.get('in_dur', .5 if en in ('pop', 'fade', 'rise') else 1.2); x, y = c.get('x', 0) * k, c.get('y', 0) * k
        if en.startswith('wipe'):
            v = eo(u); m = Image.new('L', im.size, 0); dd = ImageDraw.Draw(m)
            if en == 'wipe_l': dd.rectangle((0, 0, im.width * v, im.height), fill=255)
            elif en == 'wipe_r': dd.rectangle((im.width * (1 - v), 0, im.width, im.height), fill=255)
            else: dd.rectangle((0, 0, im.width, im.height * v), fill=255)
            im2 = im.copy(); im2.putalpha(Image.composite(im.split()[3], Image.new('L', im.size, 0), m)); fr.alpha_composite(_alpha(im2, fade), (int(x), int(y)))
        else:
            a = min(1, u * 2) * fade; dy = (1 - eo(u)) * 40 * k if en == 'rise' else 0
            if en == 'pop':
                s2 = .6 + .4 * eb(u); im = im.resize((max(1, int(im.width * s2)), max(1, int(im.height * s2))), Image.LANCZOS); x += (w - im.width) / 2; y += (w * 0 + (im.height / s2 - im.height)) / 2
            fr.alpha_composite(_alpha(im, a), (int(x), int(y + dy)))
    elif st == 'arrow':
        (x0, y0), (x1, y1) = c['from'], c['to']; v = eo((t - t0) / .6); xe, ye = x0 + (x1 - x0) * v, y0 + (y1 - y0) * v
        col = hexc(c.get('color') or ACCENT) + (int(255 * fade),); lw = int(c.get('width', 10) * k)
        lay = Image.new('RGBA', fr.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay); d.line([(x0 * k, y0 * k), (xe * k, ye * k)], fill=col, width=lw)
        ang = math.atan2(y1 - y0, x1 - x0); hs = lw * 2.6
        d.polygon([(xe * k + math.cos(ang) * hs, ye * k + math.sin(ang) * hs), (xe * k + math.cos(ang + 2.4) * hs, ye * k + math.sin(ang + 2.4) * hs), (xe * k + math.cos(ang - 2.4) * hs, ye * k + math.sin(ang - 2.4) * hs)], fill=col)
        fr.alpha_composite(lay)

EXT_STYLES = ('tag', 'tiles', 'ban', 'board', 'mark', 'pain', 'img', 'arrow')

# ---------------- 答题：急救箱卡片版 ----------------
_EMOJI_FONTS = ['/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', '/usr/share/fonts/noto/NotoColorEmoji.ttf', '/System/Library/Fonts/Apple Color Emoji.ttc',
                'C:/Windows/Fonts/seguiemj.ttf']
def _emoji_font(sz):
    for p in [os.environ.get('MG_EMOJI_FONT', '')] + _EMOJI_FONTS:
        if p and os.path.exists(p):
            try: return ImageFont.truetype(p, 109)   # 彩色 emoji 字体只有固定字号，画完再缩放
            except OSError: continue
    return None
def _is_emoji(s): return any(ord(ch) >= 0x1F000 or 0x2600 <= ord(ch) <= 0x27BF for ch in s)
def _kit_glyph(im, d, glyph, letter, col, cx, cy, s):
    """选项没有插图时的大图：彩色 emoji / 大字符号 / 字母徽章"""
    if glyph and _is_emoji(glyph):
        ef = _emoji_font(s)
        if ef:
            g = Image.new('RGBA', (int(109 * 1.4 * max(1, len(glyph))), 160), (0, 0, 0, 0))
            ImageDraw.Draw(g).text((g.width / 2, 80), glyph, font=ef, embedded_color=True, anchor='mm')
            bb = g.getbbox()
            if bb:
                g = g.crop(bb); sc = s * 1.15 / max(g.size); g = g.resize((max(1, int(g.width * sc)), max(1, int(g.height * sc))), Image.LANCZOS)
                im.alpha_composite(g, (int(cx - g.width / 2), int(cy - g.height / 2))); return
        glyph = None   # 没有 emoji 字体：退回字母徽章
    lt = tuple(int(v * .16 + 255 * .84) for v in col); r = s * .62
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=lt, outline=col, width=max(2, int(r * .07)))
    txt = glyph or letter; fs = r * (1.25 if len(txt) == 1 else 1.6 / max(1.4, len(txt)))
    d.text((cx, cy + r * .02), txt, font=F(fs), fill=col, anchor='mm')

KIT_COL = [(226, 64, 52), (240, 138, 36), (60, 170, 130), (47, 111, 208)]
def draw_quiz_kit(fr, qz, t, k, base=None):
    t0 = qz.get('t', .3)
    if t < t0: return
    cd_at = qz.get('cd_at', t0 + 2); N = qz.get('countdown', 5); rv = cd_at + N; ans = qz.get('answer', [0]); opts = qz.get('options', ['对', '错'])
    lay = Image.new('RGBA', fr.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    # 题条：宽高随题目文字自适应（自动换行、自动缩字号），可用 qz["bar"] 覆盖 x/y/w/size/align
    bar = qz.get('bar', {}); fs = bar.get('size', 44); bw = 260; padx = 40
    maxw = bar.get('w', 1620) - bw - padx * 2
    def _wrap(txt, f):
        out = []
        for para in txt.split('\n'):
            cur = ''
            for ch_ in para:
                if cur and F(f).getlength(cur + ch_) > maxw: out.append(cur); cur = ch_
                else: cur += ch_
            out.append(cur)
        return out
    lines = _wrap(qz['q'], fs)
    while len(lines) > 2 and fs > 30: fs -= 2; lines = _wrap(qz['q'], fs)
    tw = max(F(fs).getlength(x) for x in lines); lh = fs * 1.3
    hh_ = max(110, len(lines) * lh + 44); bwid = bar.get('w') or min(1620, max(900, bw + padx * 2 + tw))
    align = bar.get('align', 'center'); bx = bar.get('x', (1920 - bwid) / 2 - 60 if align == 'center' else 90); by = bar.get('y', 60)
    u = eo((t - t0) / .45); hx0, hy0, hx1 = bx * k, (by - (1 - u) * 40) * k, (bx + bwid) * k; hh = hh_ * k; bw = bw * k
    _shadow(lay, (hx0, hy0, hx1, hy0 + hh), 12 * k, k, 80); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((hx0, hy0, hx1, hy0 + hh), 12 * k, fill=CREAM)
    hc = hexc(qz.get('color') or ACCENT)
    d.rounded_rectangle((hx0, hy0, hx0 + bw, hy0 + hh), 12 * k, fill=hc); d.rectangle((hx0 + bw - 14 * k, hy0, hx0 + bw, hy0 + hh), fill=hc)
    no = qz.get('no', 1); d.text((hx0 + bw / 2, hy0 + hh / 2), f'考考你 {"①②③④⑤⑥⑦⑧"[no - 1] if 1 <= no <= 8 else no}', font=F(42 * k), fill='white', anchor='mm')
    for i, ln in enumerate(lines): d.text((hx0 + bw + padx * k, hy0 + hh / 2 + (i - (len(lines) - 1) / 2) * lh * k), ln, font=F(fs * k), fill=INK, anchor='lm')
    bar_bottom = by + hh_
    # 选项卡
    n = len(opts); cw = min(470, (1500 - 40 * (n - 1)) / n); ch = 520; gx = 40; tot = n * cw + (n - 1) * gx; X0 = (1710 + 90 - tot) / 2 - 60; Y0 = max(330, bar_bottom + 100)
    ch = min(ch, 930 - Y0)
    show = t >= rv; imgs = qz.get('option_imgs', []); icons = qz.get('option_icons', []); glyphs = qz.get('option_glyphs', [])
    for i, op in enumerate(opts):
        ti = t0 + .5 + i * .15
        if t < ti: continue
        v = (t - ti) / .45; sc = .7 + .3 * eb(v); ok = i in ans
        lift = -24 * eo((t - rv) / .4) if show and ok else 0
        cwk, chk = cw * k, ch * k; pad = int(24 * k)
        im = Image.new('RGBA', (int(cwk + pad * 2), int(chk + pad * 2 + 40 * k)), (0, 0, 0, 0)); o = pad + 40 * k
        _shadow(im, (pad, o, pad + cwk, o + chk), 18 * k, k, 80, 12, 10); dd = ImageDraw.Draw(im); col = KIT_COL[i % 4]
        dd.rounded_rectangle((pad + cwk * .32, o - 34 * k, pad + cwk * .68, o + 10 * k), 14 * k, outline=(225, 225, 232), width=int(9 * k))
        dd.rounded_rectangle((pad, o, pad + cwk, o + chk), 18 * k, fill=(255, 255, 255)); dd.rounded_rectangle((pad, o, pad + cwk, o + 86 * k), 18 * k, fill=col); dd.rectangle((pad, o + 60 * k, pad + cwk, o + 86 * k), fill=col)
        dd.text((pad + 34 * k, o + 43 * k), chr(65 + i), font=F(40 * k), fill='white', anchor='mm'); (_cross(dd, pad + cwk - 40 * k, o + 43 * k, 34 * k) if qz.get('cross', True) else None)
        if i < len(imgs) and imgs[i]: _icon_or_img(im, dd, imgs[i], pad + cwk / 2, o + 86 * k + chk * .3, min(cwk * .7, chk * .4), base)
        elif i < len(icons) and icons[i]: icon(dd, icons[i], pad + cwk / 2, o + 86 * k + chk * .26, min(cwk, chk) * .3)
        else: _kit_glyph(im, dd, glyphs[i] if i < len(glyphs) else None, chr(65 + i), col, pad + cwk / 2, o + 86 * k + chk * .27, min(cwk, chk) * .36)
        fs2 = 38; mw = cw - 48
        def _wr(txt, f):
            out = []
            for para in txt.split('\n'):
                cur = ''
                for ch_ in para:
                    if cur and F(f).getlength(cur + ch_) > mw: out.append(cur); cur = ch_
                    else: cur += ch_
                out.append(cur)
            return out
        tl = _wr(op, fs2)
        while len(tl) > 3 and fs2 > 26: fs2 -= 2; tl = _wr(op, fs2)
        for j, ln in enumerate(tl): dd.text((pad + cwk / 2, o + chk * .78 + (j - (len(tl) - 1) / 2) * fs2 * 1.3 * k), ln, font=F(fs2 * k), fill=INK, anchor='mm')
        if show and not ok:
            gr = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(gr).rounded_rectangle((pad, o - 40 * k, pad + cwk, o + chk), 18 * k, fill=(120, 130, 160, int(150 * eo((t - rv) / .4))))
            im.alpha_composite(gr)
        if show and ok:
            r = 34 * k; cx, cy = pad + cwk - 26 * k, o + 6 * k; dd.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(46, 158, 91), outline='white', width=int(5 * k))
            dd.line([(cx - r * .45, cy), (cx - r * .1, cy + r * .35), (cx + r * .48, cy - r * .35)], fill='white', width=int(7 * k), joint='curve')
        s2 = sc * (1.04 if show and ok else 1)
        if s2 != 1: im = im.resize((max(1, int(im.width * s2)), max(1, int(im.height * s2))), Image.LANCZOS)
        cx_ = (X0 + i * (cw + gx) + cw / 2) * k; cy_ = (Y0 + ch / 2 + lift / k * 0) * k + lift * k - 20 * k
        lay.alpha_composite(_alpha(im, min(1, v * 2)), (int(cx_ - im.width / 2), int(cy_ - im.height / 2)))
    # 倒数圆环
    rx, ry, R = (X0 + tot + 95) * k, (Y0 + 30) * k, 62 * k
    if rx + R > 1900 * k: rx, ry = 1820 * k, 125 * k
    if t >= cd_at - .3:
        d = ImageDraw.Draw(lay); d.ellipse((rx - R, ry - R, rx + R, ry + R), fill=(255, 255, 255, 250), outline=(230, 220, 215), width=int(9 * k))
        if t < rv:
            left = rv - t; num = str(int(math.ceil(left - 1e-6))); col = (226, 64, 52)
            d.arc((rx - R, ry - R, rx + R, ry + R), -90, -90 + 360 * left / N, fill=col, width=int(9 * k))
            s2 = 1 + .25 * max(0, (left % 1) - .75) * 4; d.text((rx, ry), num, font=F(64 * k * s2), fill=(60, 50, 60), anchor='mm')
        else:
            d.ellipse((rx - R, ry - R, rx + R, ry + R), fill=(46, 158, 91), outline=(255, 255, 255), width=int(6 * k))
            al = ''.join(chr(65 + i) for i in ans); d.text((rx, ry), al, font=F(56 * k), fill='white', anchor='mm')
    fr.alpha_composite(lay)
