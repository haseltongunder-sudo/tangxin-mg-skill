"""成片合成：场景（逐层入场 + 循环动效）+ 教师/学生 GIF（全身/半身/特写）+ 镜头推移 + 字幕 + 配音 → 高清 MP4

用法：python3 compose.py shots.json [--res 1080|1440|2160] [--preview] [--at 1.5,-0.5] [--no-lint]
  --preview  只出每个镜头中间一帧的 PNG（out/preview/），用来快速检查构图
  --no-lint  跳过开工前的规则检查（也可在 json 顶层写 "lint": false）
  顶层 "accent": 卡片/箭头/标签默认主色，默认 "#2F6FDE"（教学蓝）；"fire" = 消防红 #E8483B，也可直接写 "#RRGGBB"

shots.json 示例见 ../examples/demo_shots.json；字段说明见 SKILL.md「出片」一节。
坐标一律按 1920×1080 来写，换分辨率时自动放大，素材不会糊。
"""
import os, sys, json, re, io, math, glob, wave, argparse, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import camfx, ui, lint
BASE = None

D = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(D, 'fonts', 'NotoSansSC-800.woff')

# ---------------- 角色 ----------------
SHOT = {  # 景别：露出人物身高的比例、露出部分占画面高度的比例
    'full':  None,            # 全身，脚踩场景地面线
    'knee':  (0.92, 0.80),    # 七分身（卡通大头比例下约到膝盖，头顶留空）
    'half':  (0.58, 0.90),    # 半身（腰部以上）
    'bust':  (0.40, 0.88),    # 特写（胸部以上）
}
ROLE_H = {'teacher': 640, 'student': 500, 'kid': 460}   # 全身时的默认身高（px，按 1080 高画面）

def ease_out(t): t = max(0, min(1, t)); return 1 - (1 - t) ** 3
def ease_back(t):
    t = max(0, min(1, t)); c = 1.70158; return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2

def load_frames(src, key=None, raw=False):
    """GIF 或 PNG 序列目录 → [(RGBA, 毫秒)]，统一裁到所有帧的人物外框"""
    fr = []
    if os.path.isdir(src):
        for f in sorted(glob.glob(os.path.join(src, '*.png'))):
            m = re.search(r'(\d+)ms', os.path.basename(f))
            fr.append((Image.open(f).convert('RGBA'), int(m.group(1)) if m else 80))
    else:
        im = Image.open(src)
        for i in range(getattr(im, 'n_frames', 1)):
            im.seek(i); fr.append((im.convert('RGBA'), im.info.get('duration', 80) or 80))
    if key:  # 非透明底：按白底/绿幕简单抠
        out = []
        for f, d in fr:
            px = f.load(); w, h = f.size
            for y in range(h):
                for x in range(w):
                    r, g, b, a = px[x, y]
                    if (key == 'white' and r > 236 and g > 236 and b > 236) or (key == 'green' and g > 120 and g > r * 1.35 and g > b * 1.35):
                        px[x, y] = (0, 0, 0, 0)
            out.append((f, d))
        fr = out
    if raw: return fr
    box = None
    for f, _ in fr:
        b = f.split()[3].point(lambda v: 255 if v > 16 else 0).getbbox()
        if b: box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3]))
    return [(f.crop(box), d) for f, d in fr]

def _bbox(frames):
    box = None
    for f, _ in frames:
        b = f.split()[3].point(lambda v: 255 if v > 16 else 0).getbbox()
        if b: box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3]))
    return box


def _asset(a, rel, what):
    """素材路径 → 绝对路径；不存在就报清楚是哪个镜头、哪个文件"""
    p = rel if os.path.isabs(rel) else os.path.join(a['_base'], rel)
    if not os.path.exists(p):
        raise FileNotFoundError(f'素材不存在：{p}（{a.get("_shot", "镜头 ?")} 的角色 {what}）')
    return p


class Actor:
    """角色。字段：src talk idle poses sway x shot role height flip still speed key t_in t_out enter shadow z dy allow_close
    poses: [{"src": 说话帧目录, "idle": 待机帧目录, "t": [t0, t1], "height": 可选}]，t 窗口内换成该姿势（仍按 talk 切换张嘴/闭嘴）
    sway:  生命感微动强度（默认 1.0，0 关闭）：呼吸缩放 ±0.6%、轻微左右摆；说话时再加 1–2px 的点头/侧倾，确定性无随机"""
    def __init__(self, a, stand, k):
        if a.get('shot') in ('half', 'bust') and not a.get('allow_close'):
            print('提示：默认不用半身/特写，已改为七分身（确需特写时加 "allow_close": true）', file=sys.stderr)
            a = dict(a, shot='knee')
        self.a = a; self.k = k
        # 口型同步：talk=[[t0,t1],...] 说话时段播放 src（张嘴），其余时间播放 idle（闭嘴待机/眨眼）
        self.talk = a.get('talk')
        specs = [dict(src=a['src'], idle=a.get('idle'), t=None, height=a.get('height'), what='')]
        for j, p in enumerate(a.get('poses') or []):
            if 'src' not in p or 't' not in p: raise ValueError(f'{a.get("_shot", "")} 角色 poses[{j}] 需要 src 和 t')
            specs.append(dict(src=p['src'], idle=p.get('idle'), t=tuple(p['t']), height=p.get('height'), what=f'poses[{j}].'))
        raws = []
        for sp in specs:
            ft = load_frames(_asset(a, sp['src'], sp['what'] + 'src'), a.get('key'), raw=True)
            fi = load_frames(_asset(a, sp['idle'], sp['what'] + 'idle'), a.get('key'), raw=True) if (self.talk is not None and sp['idle']) else None
            raws.append((ft, fi))
        # 同尺寸画布（rig.py 输出的各姿势）共用一个裁切框，人物比例一致；尺寸不同就各自裁
        sizes = {f.size for ft, fi in raws for f, _ in ft + (fi or [])}
        shared = _bbox([x for ft, fi in raws for x in ft + (fi or [])]) if len(sizes) == 1 else None
        shot = a.get('shot', 'full'); gy = stand.get('ground_y', 860)
        if shot == 'full':
            H = a.get('height', ROLE_H.get(a.get('role', 'student'), 500))
            self.H = H; self.bottom = gy + a.get('dy', 12); self.cut = None
        else:
            vis, frac = SHOT[shot]
            self.H = a.get('height', 1080 * frac / vis); self.bottom = 1080 + self.H * (1 - vis); self.cut = 1080
        self.sets = []
        for sp, (ft, fi) in zip(specs, raws):
            box = shared or _bbox(ft + (fi or []))
            fr = [(f.crop(box), d) for f, d in ft]; idl = [(f.crop(box), d) for f, d in fi] if fi else None
            if a.get('flip'):
                fr = [(f.transpose(Image.FLIP_LEFT_RIGHT), d) for f, d in fr]
                if idl: idl = [(f.transpose(Image.FLIP_LEFT_RIGHT), d) for f, d in idl]
            H = sp['height'] or self.H
            fw, fh = fr[0][0].size
            self.sets.append(dict(frames=fr, idle=idl, total=sum(d for _, d in fr), itotal=sum(d for _, d in idl) if idl else 0,
                                  t=sp['t'], H=H, W=H * fw / fh, cache={}))
        base = self.sets[0]
        self.frames, self.idle, self.W = base['frames'], base['idle'], base['W']   # 兼容旧代码（free_span 等用 W）
        self.x = a.get('x', 960)
        self.t_in = a.get('t_in', 0.4); self.t_out = a.get('t_out'); self.enter = a.get('enter', 'slide' if shot != 'full' else 'pop')
        self.shadow = shot == 'full' and a.get('shadow', True)
        sw = a.get('sway', 1.0)
        self.sway = 0.0 if a.get('breathe') is False else float(sw or 0)
        self.ph = (self.x * 0.0137) % (2 * math.pi)   # 每个角色固定相位，几个人不会同步晃

    def set_at(self, t):
        for st in self.sets[1:]:
            if st['t'][0] <= t < st['t'][1]: return st
        return self.sets[0]

    def talking(self, t):
        return self.talk is not None and any(t0 <= t < t1 for t0, t1 in self.talk)

    def talk_env(self, t):
        """说话强度 0–1，进出说话段时 0.25 秒平滑过渡"""
        if not self.talk: return 0.0
        e = 0.0
        for t0, t1 in self.talk:
            if t1 <= t0: continue
            e = max(e, max(0.0, min(1.0, (t - t0 + .25) / .25, (t1 + .25 - t) / .25)))
        return e * e * (3 - 2 * e)

    def frame_at(self, t):
        st = self.set_at(t)
        Wd, Hd = max(1, round(st['W'] * self.k)), max(1, round(st['H'] * self.k))
        if self.talk is not None and not self.talking(t):
            if st['idle']:
                ms = (t * 1000) % st['itotal']; acc = 0; idx = 0
                for i, (_, d) in enumerate(st['idle']):
                    acc += d
                    if ms < acc: idx = i; break
                key = ('i', idx)
                if key not in st['cache']: st['cache'][key] = st['idle'][idx][0].resize((Wd, Hd), Image.LANCZOS)
                return st['cache'][key], st
            idx = 0  # 没有 idle 素材：不说话时定格首帧
        elif self.a.get('still'): idx = 0
        else:
            ms = (t * 1000 * self.a.get('speed', 1)) % st['total']; acc = 0; idx = 0
            for i, (_, d) in enumerate(st['frames']):
                acc += d
                if ms < acc: idx = i; break
        if idx not in st['cache']: st['cache'][idx] = st['frames'][idx][0].resize((Wd, Hd), Image.LANCZOS)
        return st['cache'][idx], st

    def draw(self, canvas, t, S):
        """S = 场景画布相对 1920 坐标的缩放"""
        if t < self.t_in: return
        img, st = self.frame_at(t)
        W_ = st['W']
        p = (t - self.t_in) / .55; alpha = 1.0; dx = dy = 0; sc = 1.0
        if self.enter == 'slide':
            side = 1 if self.x > 960 else -1; dx = side * (1 - ease_out(p)) * (W_ * .9 + 200)
        elif self.enter == 'pop': sc = .6 + .4 * ease_back(p); alpha = min(1, p * 3)
        elif self.enter == 'rise': dy = (1 - ease_out(p)) * 160; alpha = min(1, p * 2)
        elif self.enter == 'fade': alpha = ease_out(p)
        if self.t_out is not None and t > self.t_out:
            q = (t - self.t_out) / .4; alpha *= max(0, 1 - q)
            if alpha <= 0: return
        # 生命感微动（确定性）：呼吸缩放 + 慢速左右摆；说话时叠加轻微点头和侧倾
        sw = self.sway; ang = 0.0; sy = 1.0; sx = 1.0
        if sw:
            TAU = 2 * math.pi; ph = self.ph; env = self.talk_env(t)
            br = math.sin(TAU * t / 3.4 + ph)
            sy = 1 + 0.006 * sw * br; sx = 1 + 0.002 * sw * br
            dx += 1.6 * sw * math.sin(TAU * t / 5.7 + ph * 1.3)
            dy += 1.4 * sw * env * (0.5 - 0.5 * math.cos(TAU * t * 1.9 + ph))        # 点头：向下 0–1.4px
            lean_px = 2.0 * sw * env * math.sin(TAU * t * 0.85 + ph)                    # 头顶侧移 ±2px
            ang = math.degrees(math.atan2(lean_px, max(1, st['H'])))
        w, h = img.size; w2, h2 = round(w * sc * sx * S / self.k), round(h * sc * sy * S / self.k)
        if (w2, h2) != (w, h): img = img.resize((max(1, w2), max(1, h2)), Image.LANCZOS)
        if abs(ang) > 1e-3:
            pad = int(img.height * abs(math.sin(math.radians(ang)))) + 2
            big = Image.new('RGBA', (img.width + pad * 2, img.height), (0, 0, 0, 0)); big.paste(img, (pad, 0))
            img = big.rotate(ang, resample=Image.BICUBIC, center=(big.width / 2, big.height))   # 以脚底为轴
        if alpha < 1: img.putalpha(img.split()[3].point(lambda v: int(v * alpha)))
        cx = (self.x + dx) * S; by = (self.bottom + dy) * S
        x0 = round(cx - img.width / 2); y0 = round(by - img.height)
        if self.shadow:
            sw_ = int(W_ * .62 * S * sc); sh = max(4, int(sw_ * .16))
            shd = Image.new('RGBA', (sw_ + 40, sh + 40), (0, 0, 0, 0))
            ImageDraw.Draw(shd).ellipse((20, 20, 20 + sw_, 20 + sh), fill=(40, 30, 20, int(70 * alpha)))
            shd = shd.filter(ImageFilter.GaussianBlur(8 * S))
            canvas.alpha_composite(shd, (round(cx - sw_ / 2 - 20), round(by - sh / 2 - 20 - 4 * S)))
        _composite(canvas, img, x0, y0)


def _composite(canvas, img, x0, y0):
    """越界也能正确 alpha 合成（只合成与画布相交的部分）"""
    l, t_ = max(0, x0), max(0, y0); r, b = min(canvas.width, x0 + img.width), min(canvas.height, y0 + img.height)
    if r <= l or b <= t_: return
    canvas.alpha_composite(img.crop((l - x0, t_ - y0, r - x0, b - y0)), (l, t_))

# ---------------- 字幕 ----------------
def free_span(actors):
    """半身/特写角色占住的横向范围之外，最宽的一段空位（字幕放这里，不压人物）"""
    occ = sorted((a.x - a.W / 2, a.x + a.W / 2) for a in actors if a.cut)
    gaps, cur = [], 60
    for l, r in occ:
        if l > cur: gaps.append((cur, l))
        cur = max(cur, r)
    if cur < 1860: gaps.append((cur, 1860))
    g = max(gaps, key=lambda g: g[1] - g[0]) if gaps else None
    return g if g and g[1] - g[0] >= 760 else (60, 1860)   # 空位太窄就居中整行

def draw_sub(img, text, t, t0, d, W, k, span=(60, 1860)):
    p = (t - t0) / .3; q = (t0 + d - t) / .25
    a = max(0, min(1, p, q))
    if a <= 0: return
    size = 54; dr = ImageDraw.Draw(img)
    while True:
        f = ImageFont.truetype(FONT, int(size * k)); tw = dr.textlength(text, font=f)
        if tw <= (span[1] - span[0] - 40) * k or size <= 38: break
        size -= 2
    x = (span[0] + span[1]) / 2 * k - tw / 2; y = (1004 + (1 - ease_out(p)) * 18) * k - size * k / 2
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.text((x, y), text, font=f, fill=(255, 255, 255, int(255 * a)), stroke_width=int(7 * k), stroke_fill=(35, 40, 60, int(235 * a)))
    img.alpha_composite(lay)


# ---------------- 知识点卡片 ----------------
# 镜头里加 "cards": [...]，每张卡在画面坐标（1920×1080，镜头运动之后叠加，不跟着推拉）里显示知识点。
# 通用字段：style（list/big/steps/chips/compare）、t 出现时间、d 显示时长（不填就到镜头结束）、x y w 左上角和宽度、
#           title 标题、color 主色（默认 ui.ACCENT 教学蓝 #2F6FDE，顶层 accent 可整片换色，如 "fire"）、gap 条目逐个出现的间隔（默认 .6 秒）、items 条目。
# 条目写法："ok:人走关火" ✓、"no:玩打火机" ✗、"warn:小火星引发火灾" !、"1:说清地址" 编号、或纯文字（圆点）。
# big 风格：title 小标题 + big 大字（如 "119"）+ note 说明；compare 风格：items 恰好两条，左右对比。
ICON_C = {'ok': (46, 170, 90), 'no': (228, 64, 52), 'warn': (245, 150, 30)}
def _hex(c): c = c.lstrip('#'); return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))
def _font(sz): return ImageFont.truetype(FONT, max(8, int(sz)))
def _parse(it):
    m = re.match(r'^(ok|no|warn|\d+):(.*)$', it)
    return (m.group(1), m.group(2)) if m else ('dot', it)
def _icon(dr, kind, cx, cy, r, k, main):
    col = ICON_C.get(kind, main)
    if kind == 'dot': dr.ellipse((cx - r * .35, cy - r * .35, cx + r * .35, cy + r * .35), fill=main); return
    dr.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col)
    w = max(2, int(r * .22))
    if kind == 'ok': dr.line([(cx - r * .5, cy), (cx - r * .12, cy + r * .4), (cx + r * .52, cy - r * .38)], fill='white', width=w, joint='curve')
    elif kind == 'no':
        dr.line([(cx - r * .42, cy - r * .42), (cx + r * .42, cy + r * .42)], fill='white', width=w)
        dr.line([(cx - r * .42, cy + r * .42), (cx + r * .42, cy - r * .42)], fill='white', width=w)
    else:
        txt = '!' if kind == 'warn' else kind; f = _font(r * 1.25)
        dr.text((cx, cy), txt, font=f, fill='white', anchor='mm')
def render_card(c, n, k):
    """画一张卡（前 n 个条目可见），返回 RGBA；坐标按 1920 写，乘 k 输出"""
    main = _hex(c.get('color') or ui.ACCENT); W = c.get('w', 760) * k; pad = 34 * k
    items = [_parse(i) for i in c.get('items', [])]; st = c.get('style', 'list')
    tf = _font(46 * k); f = _font(c.get('size', 42) * k)
    hh = 84 * k if c.get('title') else 0
    tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    if st == 'big': H = hh + 240 * k + (70 * k if c.get('note') else 0) + pad
    elif st in ('steps', 'chips', 'compare'): H = hh + 150 * k + pad
    else: H = hh + pad * 1.3 + len(items) * 78 * k
    sh = 18 * k; img = Image.new('RGBA', (int(W + sh * 2), int(H + sh * 2)), (0, 0, 0, 0))
    shd = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(shd).rounded_rectangle((sh, sh * 1.5, sh + W, sh * 1.5 + H), 30 * k, fill=(40, 30, 30, 70))
    img.alpha_composite(shd.filter(ImageFilter.GaussianBlur(10 * k)))
    dr = ImageDraw.Draw(img); x0, y0 = sh, sh
    dr.rounded_rectangle((x0, y0, x0 + W, y0 + H), 30 * k, fill=(255, 253, 247, 245), outline=main + (255,), width=int(5 * k))
    if hh:
        dr.rounded_rectangle((x0, y0, x0 + W, y0 + hh), 30 * k, fill=main)
        dr.rectangle((x0, y0 + hh - 30 * k, x0 + W, y0 + hh), fill=main)
        dr.text((x0 + W / 2, y0 + hh / 2), c['title'], font=tf, fill='white', anchor='mm')
    yb = y0 + hh
    if st == 'big':
        if n >= 1:
            bf = _font(200 * k)
            dr.text((x0 + W / 2, yb + 130 * k), c.get('big', ''), font=bf, fill=main, anchor='mm', stroke_width=int(6 * k), stroke_fill='white')
        if c.get('note') and n >= 2: dr.text((x0 + W / 2, yb + 275 * k), c['note'], font=f, fill=(60, 60, 75), anchor='mm')
    elif st in ('steps', 'chips', 'compare'):
        m = max(1, len(items)); gapx = 46 * k if st == 'steps' else 22 * k
        bw = (W - pad * 2 - gapx * (m - 1)) / m
        for i, (kind, txt) in enumerate(items[:n]):
            bx = x0 + pad + i * (bw + gapx); by = yb + 28 * k
            col = ICON_C.get(kind, main)
            lt = tuple(int(v * .14 + 255 * .86) for v in col)
            dr.rounded_rectangle((bx, by, bx + bw, by + 100 * k), 22 * k, fill=lt + (255,), outline=col + (255,), width=int(3 * k))
            r = 26 * k; _icon(dr, kind if kind != 'dot' else str(i + 1) if st == 'steps' else 'dot', bx + 22 * k + r, by + 50 * k, r, k, main)
            avail = bw - 30 * k - 2 * r - 14 * k; sz = c.get('size', 40) * k
            while tmp.textlength(txt, font=_font(sz)) > avail and sz > 22 * k: sz -= 2 * k
            dr.text((bx + 30 * k + 2 * r, by + 50 * k), txt, font=_font(sz), fill=(45, 45, 60), anchor='lm')
            if st == 'steps' and i < m - 1 and i < n - 1:
                ax = bx + bw + 8 * k; ay = by + 50 * k
                dr.polygon([(ax, ay - 14 * k), (ax + 30 * k, ay), (ax, ay + 14 * k)], fill=main)
    else:
        for i, (kind, txt) in enumerate(items[:n]):
            cy = yb + pad * .8 + i * 78 * k + 39 * k; r = 27 * k
            _icon(dr, kind, x0 + pad + r, cy, r, k, main)
            sz = c.get('size', 42) * k; avail = W - pad * 2 - 2 * r - 22 * k
            while tmp.textlength(txt, font=_font(sz)) > avail and sz > 24 * k: sz -= 2 * k
            dr.text((x0 + pad + 2 * r + 22 * k, cy), txt, font=_font(sz), fill=(45, 45, 60), anchor='lm')
    return img, sh
_CARD_CACHE = {}
def draw_cards(fr, cards, t, k, shot_end):
    for ci, c in enumerate(cards):
        t0 = c.get('t', .6); t1 = t0 + c['d'] if c.get('d') else shot_end + 1
        if t < t0 or t > t1: continue
        st = c.get('style', 'list')
        if st in ui.EXT_STYLES: ui.draw_ext(fr, c, t, k, t0, t1, BASE); continue
        cnt = 2 if st == 'big' else len(c.get('items', []))
        gap = c.get('gap', .6)
        n = sum(1 for i in range(cnt) if t >= t0 + .35 + i * gap)
        key = (id(c), n, k)
        if key not in _CARD_CACHE: _CARD_CACHE[key] = render_card(c, n, k)
        img, sh = _CARD_CACHE[key]
        p = (t - t0) / .45; a = min(1, max(0, p * 2.2)); sc = .82 + .18 * ease_back(p)
        q = (t1 - t) / .3
        if c.get('d') and q < 1: a *= max(0, q)
        if a <= 0: continue
        im = img
        if sc != 1: im = img.resize((max(1, int(img.width * sc)), max(1, int(img.height * sc))), Image.LANCZOS)
        if a < 1: im = im.copy(); im.putalpha(im.split()[3].point(lambda v: int(v * a)))
        cx = (c.get('x', 100) * k - sh) + img.width / 2; cy = (c.get('y', 100) * k - sh) + img.height / 2
        fr.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


# ---------------- 答题镜头（MP4 版倒数答题） ----------------
# 镜头里加 "quiz": {"q": 题干, "options": [...], "answer": [正确选项序号], "t": 出题时间, "cd_at": 倒数开始时间,
#                   "countdown": 5, "explain": 解析, "kind": "单选"/"多选"/"判断"}
# 画面：题卡居中，右上角倒数圆环 5→1（每秒滴一声），倒数结束「叮」一声，正确选项变绿打勾，下方出解析。
# 可选 "x"/"w"：题卡左边和宽度（老师站右侧时设 x≈70、w≈1080，避免挡住老师）。
# 建议同时设 "static": true（背景只截一次，渲染快）和 "bg_blur": 6（背景虚化突出题卡）。
def draw_quiz(fr, qz, t, k):
    t0 = qz.get('t', .3); 
    if t < t0: return
    cd_at = qz.get('cd_at', t0 + 2); N = qz.get('countdown', 5); rv = cd_at + N
    opts = qz.get('options', ['对', '错']); ans = qz.get('answer', [0])
    # 题框随文字自适应：宽度按题目和选项长度算（qz["w"] 可固定），题目和选项自动换行、缩字号，高度随行数变化
    tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1))); L = lambda txt, f: tmp.textlength(txt, font=_font(f))
    def wrap(txt, f, mw):
        out = []
        for para in txt.split('\n'):
            cur = ''
            for ch in para:
                if cur and L(cur + ch, f) > mw: out.append(cur); cur = ch
                else: cur += ch
            out.append(cur)
        return out
    MAXW = qz.get('max_w', 1400); qf = qz.get('size', 50); of = 40
    tagw = L('考考你 · 多选', 32) + 72
    need = max([L(x, qf) for x in qz['q'].split('\n')] + [L(f'{chr(65 + i)}. {op}', of) + 140 for i, op in enumerate(opts)] + [tagw])
    W = qz.get('w') or max(760, min(MAXW, need + 80))
    ql = wrap(qz['q'], qf, W - 80)
    while len(ql) > 3 and qf > 32: qf -= 2; ql = wrap(qz['q'], qf, W - 80)
    olines = [wrap(f'{chr(65 + i)}. {op}', of, W - 200) for i, op in enumerate(opts)]
    qh = len(ql) * qf * 1.3; rows = [max(80, len(x) * of * 1.25 + 26) for x in olines]
    qy0 = 100; oy0 = qy0 + qh + 24; H = int(oy0 + sum(rows) + 16 * (len(rows) - 1) + 40)
    x0 = qz.get('x', (1920 - W) / 2 - 60); y0 = qz.get('y', max(40, (930 - H) / 2))
    p = (t - t0) / .45; a = min(1, max(0, p * 2.2)); sc = .85 + .15 * ease_back(p)
    img = Image.new('RGBA', (int((W + 40) * k), int((H + 40) * k)), (0, 0, 0, 0)); dr = ImageDraw.Draw(img); o = 20 * k
    sh = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((o, o + 10 * k, o + W * k, o + H * k + 10 * k), 34 * k, fill=(40, 30, 30, 80))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12 * k)))
    main = _hex(qz.get('color', '#F08A24'))
    dr.rounded_rectangle((o, o, o + W * k, o + H * k), 34 * k, fill=(255, 253, 247, 250), outline=main, width=int(6 * k))
    tag = '考考你 · ' + qz.get('kind', '多选' if len(ans) > 1 else '单选'); tf = _font(32 * k)
    tw = dr.textlength(tag, font=tf); dr.rounded_rectangle((o + 36 * k, o + 28 * k, o + 36 * k + tw + 36 * k, o + 78 * k), 14 * k, fill=main)
    dr.text((o + 54 * k, o + 53 * k), tag, font=tf, fill='white', anchor='lm')
    for j, ln in enumerate(ql): dr.text((o + 40 * k, o + (qy0 + qf * .65 + j * qf * 1.3) * k), ln, font=_font(qf * k), fill=(40, 40, 55), anchor='lm')
    show = t >= rv; yy = oy0
    for i, op in enumerate(opts):
        by = o + yy * k; rh = rows[i]; ok = i in ans
        fill, line = ((228, 245, 234), (46, 170, 90)) if show and ok else (((246, 240, 236), (222, 214, 206)) if show else ((253, 241, 230), (240, 200, 160)))
        dr.rounded_rectangle((o + 40 * k, by, o + (W - 40) * k, by + rh * k), 18 * k, fill=fill, outline=line, width=int(4 * k))
        for j, ln in enumerate(olines[i]): dr.text((o + 70 * k, by + (rh / 2 + (j - (len(olines[i]) - 1) / 2) * of * 1.25) * k), ln, font=_font(of * k), fill=(40, 40, 55) if not show or ok else (150, 150, 160), anchor='lm')
        if show and ok: _icon(dr, 'ok', o + (W - 90) * k, by + rh / 2 * k, 26 * k, k, main)
        yy += rh + 16
    if sc != 1: img = img.resize((max(1, int(img.width * sc)), max(1, int(img.height * sc))), Image.LANCZOS)
    if a < 1: img.putalpha(img.split()[3].point(lambda v: int(v * a)))
    cx = (x0 + W / 2) * k; cy = (y0 + H / 2) * k
    fr.alpha_composite(img, (int(cx - img.width / 2), int(cy - img.height / 2)))
    # 倒数圆环
    rx, ry, R = (x0 + W + 40 + 75) * k, (y0 + 75) * k, 72 * k
    if t >= cd_at - .3:
        lay = Image.new('RGBA', fr.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        ld.ellipse((rx - R, ry - R, rx + R, ry + R), fill=(255, 255, 255, 245), outline=(230, 220, 210), width=int(10 * k))
        if t < rv:
            left = rv - t; frac = left / N; num = str(int(math.ceil(left - 1e-6)))
            col = (232, 72, 59) if left <= 2 else main
            ld.arc((rx - R, ry - R, rx + R, ry + R), -90, -90 + 360 * frac, fill=col, width=int(10 * k))
            ph = (left % 1); s2 = 1 + .25 * max(0, ph - .75) * 4
            ld.text((rx, ry), num, font=_font(80 * k * s2), fill=col, anchor='mm')
        else:
            ld.ellipse((rx - R, ry - R, rx + R, ry + R), fill=(46, 170, 90), outline=(46, 170, 90), width=int(10 * k))
            al = ''.join(chr(65 + i) for i in ans) if qz.get('kind') != '判断' else ('对' if ans == [0] else '错')
            ld.text((rx, ry - 4 * k), al, font=_font({1: 70, 2: 54, 3: 40}.get(len(al), 32) * k), fill='white', anchor='mm')
        fr.alpha_composite(lay)

# ---------------- 场景帧 ----------------
class SceneRenderer:
    def __init__(self, pg): self.pg = pg; self.cur = None
    def open(self, sid, theme, S, par=0):
        svgp = next((p for p in (f'{D}/out/svg/{sid}.svg', f'{D}/../examples/svg/{sid}.svg') if os.path.exists(p)), None)
        if not svgp: raise FileNotFoundError(f'场景 {sid} 的 SVG 不存在（找过 engine/out/svg 和 examples/svg）；先运行 render.py 生成，或检查 scene 字段')
        html = (f'<style>@font-face{{font-family:"Noto Sans SC";src:url(file://{FONT})}}body{{margin:0;overflow:hidden}}svg{{display:block}}</style>'
                f'{open(svgp).read()}<script>{open(D + "/mgscene.js").read()}</script>')
        fn = os.path.join(tempfile.gettempdir(), f'_compose_{os.getpid()}.html'); open(fn, 'w').write(html)
        self.pg.set_viewport_size({'width': 1920, 'height': 1080})
        self.pg.goto('file://' + fn); self.pg.evaluate('document.fonts.ready')
        self.pg.evaluate(f"(()=>{{const s=document.querySelector('svg');s.setAttribute('width',1920);s.setAttribute('height',1080);MGScene.theme(s,'{theme}');MGScene.play(s,{{camera:{"'none'" if par else "'push'"}}});}})()")
        self.pg.evaluate(camfx.PAR_JS)
    def frame(self, t, replay=True):
        self.pg.evaluate(f"MGScene.seek(document.querySelector('svg'),{t if replay else 30 + t})")
        return Image.open(io.BytesIO(self.pg.screenshot(type='jpeg', quality=93))).convert('RGBA')

def lerp(a, b, u): return a + (b - a) * u

def wav_len(p):
    """音频时长（秒）：wav 直接读，mp3/m4a 等用 ffprobe"""
    if not os.path.exists(p): raise FileNotFoundError(f'音频不存在：{p}')
    try:
        with wave.open(p) as w: return w.getnframes() / w.getframerate()
    except (wave.Error, EOFError):
        return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]).decode().strip())

def contact_sheet(paths, out, cols=3, w=640):
    from PIL import Image, ImageDraw
    ims = [Image.open(x).convert('RGB') for x in paths]
    h = int(w * 9 / 16); rows = (len(ims) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * w + (cols + 1) * 8, rows * (h + 8) + 8), (40, 40, 48)); d = ImageDraw.Draw(sheet)
    for i, im in enumerate(ims):
        x, y = 8 + (i % cols) * (w + 8), 8 + (i // cols) * (h + 8)
        sheet.paste(im.resize((w, h)), (x, y)); d.rectangle((x, y, x + 34, y + 22), fill=(0, 0, 0)); d.text((x + 5, y + 5), f'{i + 1:02d}', fill=(255, 255, 255))
    sheet.save(out, quality=85)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('shots'); ap.add_argument('--res', type=int, default=1080); ap.add_argument('--preview', action='store_true'); ap.add_argument('--at', default='', help='预览指定时刻（秒，逗号分隔，负数从镜头结尾数），配合 --preview')
    ap.add_argument('--no-lint', action='store_true', help='跳过规则检查')
    a = ap.parse_args()
    cfg = json.load(open(a.shots)); base = os.path.dirname(os.path.abspath(a.shots)); global BASE; BASE = base
    ui.set_accent(cfg.get('accent'))
    if not a.no_lint and cfg.get('lint', True) is not False:
        shots_l = [dict(x, _base=base, _src=f'{os.path.basename(a.shots)}#{i + 1}') for i, x in enumerate(cfg['shots'])]
        errs, warns = lint.check(shots_l, episode=len(shots_l) >= lint.EPISODE_MIN)
        lint.report(errs, warns)
        if errs: sys.exit('规则检查未通过，已停止（确需跳过：--no-lint 或 json 顶层 "lint": false）')
    meta = {}
    for p in (f'{D}/out/scenes.json', f'{D}/../reference/scenes.json'):
        if os.path.exists(p): meta = json.load(open(p)); break
    fps = cfg.get('fps', 30); k = a.res / 1080; W, H = round(1920 * k), round(1080 * k)
    out = os.path.join(base, cfg.get('out', 'out.mp4'))
    os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
    from playwright.sync_api import sync_playwright
    os.makedirs(f'{D}/out/preview', exist_ok=True); PV = []
    tmpd = tempfile.mkdtemp()
    durs = []
    for s in cfg['shots']:
        d = s.get('dur', 4)
        if s.get('audio'): d = max(d, wav_len(os.path.join(base, s['audio'])) + s.get('audio_at', .3) + .4)
        for x in s.get('audios', []): d = max(d, wav_len(os.path.join(base, x['file'])) + x.get('at', 0) + .6)
        durs.append(d)
    for i, s in enumerate(cfg['shots']): s['camera'] = camfx.expand_cam(s.get('camera', {}), durs[i])
    zmax = max([camfx.zmax_of(s.get('camera', {}), durs[i]) for i, s in enumerate(cfg['shots'])] + [1])
    S_dsf = k * min(zmax, cfg.get('ss_cap', 2.0))  # 场景按镜头最大推近倍数超采样（转场急推不计入，靠模糊遮盖）
    ff = None
    if not a.preview:
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(fps), '-i', '-', '-c:v', 'libx264', '-preset', 'slow',
                               '-crf', '16', '-pix_fmt', 'yuv420p', '-r', str(fps), '-movflags', '+faststart', f'{tmpd}/v.mp4'], stdin=subprocess.PIPE)
    prev = None; XF = int(cfg.get('dissolve', .4) * fps)
    with sync_playwright() as p:
        b = p.chromium.launch(); ctx = b.new_context(viewport={'width': 1920, 'height': 1080}, device_scale_factor=S_dsf); pg = ctx.new_page()
        sr = SceneRenderer(pg)
        for si, s in enumerate(cfg['shots']):
            sid = s['scene']; stand = meta.get(sid, {}).get('stand', {}) or {}
            cam = s.get('camera', {}); par = cam.get('parallax', 0); dref = cam.get('dref', .62)
            sr.open(sid, s.get('theme', 'original'), S_dsf, par)
            ks = camfx.cam_keys(cam, durs[si]); fx = s.get('fx', [])
            for ac in s.get('actors', []): ac['_base'] = base; ac['_shot'] = f'{os.path.basename(a.shots)} 第 {si + 1} 个镜头（{sid}）'
            actors = [Actor(ac, stand, S_dsf) for ac in s.get('actors', [])]
            n = int(durs[si] * fps); span = free_span(actors)
            subs_c = sorted([dict(x) for x in s.get('subs', [])], key=lambda x: x['t'])
            for j in range(len(subs_c) - 1):  # 字幕不重叠：前一条在下一条开始前收掉
                subs_c[j]['d'] = min(subs_c[j]['d'], subs_c[j + 1]['t'] - subs_c[j]['t'])
            rng = ([min(n - 1, max(0, int((float(x) if float(x) >= 0 else durs[si] + float(x)) * fps))) for x in a.at.split(',')] if a.at else [n // 2]) if a.preview else range(n)
            for i in rng:
                t = i / fps
                z, cx0, cy0, roll = camfx.cam_at(ks, t)
                sdx, sdy = camfx.shake_off(cam, t); cx0 += sdx; cy0 += sdy
                tz, tat, tu = camfx.trans_cam(s, t, durs[si])
                if tat: w_ = min(1, abs(tu) * 1.6); cx0 += (tat[0] - cx0) * w_; cy0 += (tat[1] - cy0) * w_
                if par and not s.get('static'):
                    hw_, hh_ = 960 / z, 540 / z; pcx = min(max(cx0, hw_), 1920 - hw_); pcy = min(max(cy0, hh_), 1080 - hh_)
                    pg.evaluate(f"_par({pcx:.2f},{pcy:.2f},{z:.4f},{par},{dref})")
                if s.get('static'):
                    if i == rng[0] if a.preview else i == 0:
                        bg = sr.frame(0, False)
                        if s.get('bg_blur'): bg = bg.filter(ImageFilter.GaussianBlur(s['bg_blur'] * S_dsf)); bg.alpha_composite(Image.new('RGBA', bg.size, (255, 250, 240, 60)))
                    img = bg.copy()
                else: img = sr.frame(t, s.get('replay_enter', (s.get('in') or {}).get('type', 'iris') in ('iris', 'fade')))
                camfx.draw_scene_fx(img, fx, t, S_dsf)
                for ac in sorted(actors, key=lambda x: x.a.get('z', 0)): ac.draw(img, t, S_dsf)
                zc = z * tz * (1 + abs(math.sin(math.radians(roll))) * 1.9); cx = cx0 * S_dsf; cy = cy0 * S_dsf; z = zc
                vw, vh = 1920 * S_dsf / z, 1080 * S_dsf / z
                x0 = min(max(0, cx - vw / 2), img.width - vw); y0 = min(max(0, cy - vh / 2), img.height - vh)
                fr = img.crop((round(x0), round(y0), round(x0 + vw), round(y0 + vh))).resize((W, H), Image.LANCZOS if tz < 1.05 else Image.BILINEAR)
                if roll: fr = fr.rotate(roll, resample=Image.BICUBIC)
                bl = camfx.blur_at(ks, t)
                if bl > .3: fr = fr.filter(ImageFilter.GaussianBlur(bl * k))
                camfx.draw_screen_fx(fr, fx, t, k, (cx0 - 960) * z)
                draw_cards(fr, s.get('cards', []), t, k, durs[si])
                if s.get('quiz'): (ui.draw_quiz_kit(fr, s['quiz'], t, k, BASE) if s['quiz'].get('style') == 'kit' else draw_quiz(fr, s['quiz'], t, k))
                for sub in subs_c: draw_sub(fr, sub['text'], t, sub['t'], sub['d'], W, k, tuple(s['sub_span']) if s.get('sub_span') else span)
                fr = camfx.apply_trans(fr, s, t, durs[si], k)
                if prev is not None and i < XF and not s.get('in'): fr = Image.blend(prev, fr, (i + 1) / (XF + 1))
                if a.preview: _pp = f'{D}/out/preview/{si:02d}_{sid}_{t:05.2f}.png'; fr.convert('RGB').save(_pp); PV.append(_pp); print('preview', si, sid, round(t, 2)); continue
                ff.stdin.write(_jpg(fr)); last = fr
            if not a.preview: prev = last; print('shot', si, sid, f'{durs[si]:.1f}s')
        b.close()
    if a.preview:
        if PV: contact_sheet(PV, f'{D}/out/preview/总览.jpg'); print('总览图', f'{D}/out/preview/总览.jpg')
        return
    ff.stdin.close(); ff.wait()
    # 音频：每镜头配音按 audio_at 对齐，补静音；可选全片 bgm
    segs = []
    for si, s in enumerate(cfg['shots']):
        seg = f'{tmpd}/a{si}.wav'
        clips = ([(os.path.join(base, s['audio']), s.get('audio_at', .3))] if s.get('audio') else []) + [(os.path.join(base, x['file']), x.get('at', 0)) for x in s.get('audios', [])]
        qz = s.get('quiz')
        if qz and qz.get('tick', True):  # 倒数滴答 + 揭晓叮
            tk, dg = f'{tmpd}/tick.wav', f'{tmpd}/ding.wav'
            if not os.path.exists(tk):
                subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi', '-i', 'sine=f=1200:d=0.09', '-af', 'afade=out:st=0.03:d=0.06,volume=0.5', '-ar', '48000', tk], check=True)
                subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi', '-i', 'sine=f=1568:d=0.6', '-f', 'lavfi', '-i', 'sine=f=2093:d=0.6', '-filter_complex', 'amix=inputs=2,afade=out:st=0.1:d=0.5,volume=0.8', '-ar', '48000', dg], check=True)
            ca, N = qz.get('cd_at', qz.get('t', .3) + 2), qz.get('countdown', 5)
            clips += [(tk, ca + j) for j in range(N)] + [(dg, ca + N)]
        if clips:
            ins = sum((['-i', c] for c, _ in clips), [])
            fc = ';'.join(f"[{j}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={int(at * 1000)}:all=1[c{j}]" for j, (_, at) in enumerate(clips))
            fc += ';' + ''.join(f'[c{j}]' for j in range(len(clips))) + f"amix=inputs={len(clips)}:normalize=0:duration=longest,apad,atrim=0:{durs[si]}[o]"
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + ins + ['-filter_complex', fc, '-map', '[o]', '-ar', '48000', '-ac', '2', seg], check=True)
        else:
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-t', str(durs[si]), seg], check=True)
        segs.append(seg)
    open(f'{tmpd}/l.txt', 'w').write(''.join(f"file '{x}'\n" for x in segs))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{tmpd}/l.txt', f'{tmpd}/vo.wav'], check=True)
    aud = f'{tmpd}/vo.wav'
    if cfg.get('bgm'):
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', aud, '-stream_loop', '-1', '-i', os.path.join(base, cfg['bgm']), '-filter_complex',
                        f"[1:a]volume={cfg.get('bgm_vol', .12)}[m];[0:a][m]amix=inputs=2:duration=first:normalize=0", f'{tmpd}/mix.wav'], check=True)
        aud = f'{tmpd}/mix.wav'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{tmpd}/v.mp4', '-i', aud, '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', out], check=True)
    print('done', out, f'{sum(durs):.1f}s', f'{W}x{H}')

def _jpg(im):
    bio = io.BytesIO(); im.convert('RGB').save(bio, 'JPEG', quality=95, subsampling=0); return bio.getvalue()

if __name__ == '__main__':
    main()
