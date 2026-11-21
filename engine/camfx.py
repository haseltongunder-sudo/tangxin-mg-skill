"""镜头语言 + 特效（compose.py 调用）

镜头（shot.camera）
  keys      关键帧列表，每个 {t, zoom, center:[x,y], roll, ease}；t 是秒（负数表示从镜头结尾往前数）
            ease: inout(默认) | in | out | linear | back(冲过头再回弹) | snap(急推)
  parallax  3D 分层视差强度（0 关闭，常用 0.6–1.2）：镜头推拉/横移时，远景动得少、近景动得多，画面有纵深
  shake     轻微手持晃动幅度（px），如 3
  旧写法 zoom:[a,b] + center:[[x,y],[x,y]] 仍然可用

转场（shot.in / shot.out，各自只处理本镜头的开头 / 结尾，所以拆开并行渲染再直接拼接也成立）
  {type, dur, at:[x,y]}
  zoom  穿越：out 时向 at 点（门、窗、屏幕、标牌）急推并径向模糊，in 时从放大+模糊里拉出来
  whip  甩镜：横向急速运动模糊（dir: 1 向左甩 / -1 向右甩）
  iris  圆形遮罩：out 收成一个圆点，in 从圆点打开（at 指定圆心）
  flash 白闪
  fade  黑场淡入淡出

特效（shot.fx 列表）
  {type:'leaves', n, t_in}                     前景飘落的黄叶（屏幕空间，随镜头有视差）
  {type:'flame', x, y, s, t_in, t_out}         动态火苗（场景空间，跟着镜头走），可配 smoke:true
  {type:'stamp', x, y, kind:'no'|'ok', t, r}   在某处盖一个红叉 / 绿勾，强调对错
  {type:'focus', x, y, r, t, d}                聚光：周围压暗，突出知识点所在位置
"""
import math, random
from PIL import Image, ImageDraw, ImageFilter, ImageChops

EASE = {
    'linear': lambda u: u,
    'inout': lambda u: u * u * (3 - 2 * u),
    'in': lambda u: u ** 3,
    'out': lambda u: 1 - (1 - u) ** 3,
    'back': lambda u: 1 + 2.70158 * (u - 1) ** 3 + 1.70158 * (u - 1) ** 2,
    'snap': lambda u: 1 - (1 - u) ** 5,
}


def cam_keys(cam, dur):
    if cam.get('keys'):
        ks = []
        for k in cam['keys']:
            t = k['t'] if k['t'] >= 0 else dur + k['t']
            ks.append(dict(t=max(0, min(dur, t)), zoom=k.get('zoom', 1), center=k.get('center', [960, 540]), roll=k.get('roll', 0), ease=k.get('ease', 'inout')))
        ks.sort(key=lambda k: k['t'])
        return ks
    z0, z1 = cam.get('zoom', [1, 1]); c0, c1 = cam.get('center', [[960, 540], [960, 540]])
    return [dict(t=0, zoom=z0, center=c0, roll=0, ease='inout'), dict(t=dur, zoom=z1, center=c1, roll=0, ease='inout')]


def cam_at(ks, t):
    if t <= ks[0]['t']: k = ks[0]; return k['zoom'], k['center'][0], k['center'][1], k['roll']
    for a, b in zip(ks, ks[1:]):
        if t <= b['t']:
            u = (t - a['t']) / max(1e-6, b['t'] - a['t']); e = EASE.get(b['ease'], EASE['inout'])(u)
            L = lambda p, q: p + (q - p) * e
            # 推拉按对数插值，速度感更均匀
            z = math.exp(L(math.log(a['zoom']), math.log(b['zoom'])))
            return z, L(a['center'][0], b['center'][0]), L(a['center'][1], b['center'][1]), L(a['roll'], b['roll'])
    k = ks[-1]; return k['zoom'], k['center'][0], k['center'][1], k['roll']


def zmax_of(cam, dur):
    return max(k['zoom'] for k in cam_keys(cam, dur))


# ---------------- 3D 分层视差（在浏览器里逐层变换） ----------------
PAR_JS = """
window._par = function(cx, cy, z, p, dref){
  const ls=[...document.querySelectorAll('svg g.layer')].filter(l=>!/-(vignette|grain)$/.test(l.id));
  const n=ls.length;
  ls.forEach((l,i)=>{
    const c=l.querySelector(':scope>g.cam'); if(!c) return;
    const d = l.dataset.depth!==undefined ? +l.dataset.depth : (n>1? i/(n-1) : dref);
    const dl=(d-dref)*p;
    const tx=-(cx-960)*dl, ty=-(cy-540)*dl*0.5;
    let sc=Math.pow(z, dl*0.4);
    if(dl<0){ // 远景层：保证缩放+平移后仍铺满当前取景框，不露边
      const hw=960/z, hh=540/z;
      sc=Math.max(sc,(hw+tx)/Math.max(1,cx),(hw-tx)/Math.max(1,1920-cx),(hh+ty)/Math.max(1,cy),(hh-ty)/Math.max(1,1080-cy));
    }
    c.style.transformBox='view-box'; c.style.transformOrigin=cx+'px '+cy+'px';
    c.style.transform='translate('+tx+'px,'+ty+'px) scale('+sc+')';
  });
};
"""


# ---------------- 场景空间特效（画在 img 上，随镜头一起推拉） ----------------
def _flame_patch(t, s, seed=0):
    w, h = int(220 * s), int(300 * s)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); dr = ImageDraw.Draw(im)
    cx, by = w / 2, h - 10 * s
    for layer, (col, sc) in enumerate([((242, 98, 46, 235), 1.0), ((255, 178, 56, 240), .7), ((255, 236, 160, 250), .4)]):
        pts = []
        for j in range(25):
            a = j / 24 * 2 * math.pi
            fl = 1 + .12 * math.sin(t * 13 + j * 1.7 + seed + layer) + .08 * math.sin(t * 21 + j * .9)
            rx = 70 * s * sc * fl; ry = 200 * s * sc * fl
            x = cx + rx * math.sin(a) * (1 - .55 * max(0, -math.cos(a)))
            y = by - ry * (1 - math.cos(a)) / 2 * (1 + .25 * math.sin(t * 9 + layer)) * (.85 if -math.cos(a) < 0 else 1)
            x += 12 * s * sc * math.sin(t * 11 + (by - y) / (40 * s)) * (by - y) / (ry + 1)
            pts.append((x, y))
        dr.polygon(pts, fill=col)
    glow = Image.new('RGBA', (w, h), (0, 0, 0, 0)); ImageDraw.Draw(glow).ellipse((cx - 100 * s, by - 190 * s, cx + 100 * s, by + 10 * s), fill=(255, 140, 40, 90))
    glow = glow.filter(ImageFilter.GaussianBlur(28 * s)); glow.alpha_composite(im)
    return glow


def draw_scene_fx(img, fx, t, S):
    for f in fx:
        if t < f.get('t_in', 0) or t > f.get('t_out', 1e9): continue
        a = min(1, (t - f.get('t_in', 0)) / .35)
        if f['type'] == 'flame':
            s = f.get('s', 1) * S * (.4 + .6 * a)
            if f.get('smoke'):
                sm = Image.new('RGBA', (int(400 * s), int(600 * s)), (0, 0, 0, 0)); d = ImageDraw.Draw(sm)
                for j in range(7):
                    ph = (t * .5 + j / 7) % 1; r = (30 + 70 * ph) * s
                    x = sm.width / 2 + 40 * s * math.sin(ph * 5 + j); y = sm.height - 260 * s - ph * 330 * s
                    d.ellipse((x - r, y - r, x + r, y + r), fill=(120, 110, 105, int(120 * (1 - ph))))
                sm = sm.filter(ImageFilter.GaussianBlur(10 * s))
                img.alpha_composite(sm, (int(f['x'] * S - sm.width / 2), int(f['y'] * S - sm.height)))
            p = _flame_patch(t, s, f.get('seed', 0))
            img.alpha_composite(p, (int(f['x'] * S - p.width / 2), int(f['y'] * S - p.height + 10 * s)))
        elif f['type'] == 'stamp' and t >= f.get('t', 0):
            u = min(1, (t - f['t']) / .3); sc = 1.5 - .5 * EASE['back'](u) if u < 1 else 1
            r = f.get('r', 90) * S * sc; x, y = f['x'] * S, f['y'] * S
            lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay); w = int(r * .22)
            col = (226, 56, 47, int(240 * min(1, u * 2))) if f.get('kind', 'no') == 'no' else (46, 170, 90, int(240 * min(1, u * 2)))
            d.ellipse((x - r, y - r, x + r, y + r), outline=col, width=w)
            if f.get('kind', 'no') == 'no':
                q = r * .5; d.line((x - q, y - q, x + q, y + q), fill=col, width=w); d.line((x - q, y + q, x + q, y - q), fill=col, width=w)
            else:
                d.line((x - r * .5, y, x - r * .12, y + r * .4, x + r * .52, y - r * .38), fill=col, width=w, joint='curve')
            img.alpha_composite(lay)


# ---------------- 屏幕空间特效 ----------------
def _leaf_poly(x, y, sz, ang):
    pts = [(0, 0), (-.6, -.5), (-.45, -1), (0, -.8), (.45, -1), (.6, -.5)]
    ca, sa = math.cos(ang), math.sin(ang)
    return [(x + (px * ca - py * sa) * sz, y + (px * sa + py * ca) * sz) for px, py in pts]


def draw_screen_fx(fr, fx, t, k, cam_dx=0):
    for f in fx:
        if f['type'] == 'leaves' and t >= f.get('t_in', 0):
            random.seed(f.get('seed', 7)); d = ImageDraw.Draw(fr)
            cols = [(246, 185, 48), (255, 217, 90), (224, 122, 34), (217, 84, 43)]
            W, H = fr.size
            for j in range(f.get('n', 16)):
                sp = random.uniform(.06, .12); ph = random.random(); x0 = random.uniform(-.1, 1.1); sz = random.uniform(14, 30) * k * f.get('size', 1)
                near = sz / (30 * k)
                yy = ((t * sp + ph) % 1.2 - .1) * H
                xx = x0 * W + 60 * k * math.sin(t * 1.6 + j) + yy * .25 - cam_dx * k * (.4 + .8 * near)
                xx %= (W + 200 * k)
                d.polygon(_leaf_poly(xx - 100 * k, yy, sz, t * 2.2 * (1 if j % 2 else -1) + j), fill=random.choice(cols))
        elif f['type'] == 'focus' and f.get('t', 0) <= t <= f.get('t', 0) + f.get('d', 99):
            u = min(1, (t - f.get('t', 0)) / .4, (f.get('t', 0) + f.get('d', 99) - t) / .4)
            m = Image.new('L', fr.size, int(120 * u)); r = f.get('r', 260) * k
            ImageDraw.Draw(m).ellipse((f['x'] * k - r, f['y'] * k - r, f['x'] * k + r, f['y'] * k + r), fill=0)
            m = m.filter(ImageFilter.GaussianBlur(40 * k))
            fr.paste(Image.new('RGBA', fr.size, (20, 14, 30, 255)), (0, 0), m)


# ---------------- 转场 ----------------
def zoom_blur(fr, amt, cx, cy, n=7):
    if amt <= .002: return fr
    W, H = fr.size; acc = fr.copy()
    for j in range(1, n):
        s = 1 + amt * j / n
        w, h = W / s, H / s; x0 = cx - cx / s; y0 = cy - cy / s
        acc = Image.blend(acc, fr.crop((round(x0), round(y0), round(x0 + w), round(y0 + h))).resize((W, H), Image.BILINEAR), 1 / (j + 1))
    return acc


def motion_blur(fr, dx, n=8):
    if abs(dx) < 1: return fr
    acc = fr.copy()
    for j in range(1, n):
        acc = Image.blend(acc, ImageChops.offset(fr, int(dx * j / n), 0), 1 / (j + 1))
    return acc


def trans_cam(s, t, dur):
    """转场对镜头的额外推拉：返回 (zoom 倍数, 目标点或 None, 混合比例)"""
    for side in ('in', 'out'):
        tr = s.get(side)
        if not tr or tr.get('type') != 'zoom': continue
        D = tr.get('dur', .5)
        if side == 'out' and t > dur - D:
            u = (t - (dur - D)) / D; return math.exp(math.log(tr.get('amount', 5)) * u ** 2.2), tr.get('at'), u
        if side == 'in' and t < D:
            u = 1 - t / D; return math.exp(math.log(tr.get('amount', 3)) * u ** 2.2), tr.get('at'), -u
    return 1, None, 0


def apply_trans(fr, s, t, dur, k):
    W, H = fr.size
    for side in ('in', 'out'):
        tr = s.get(side)
        if not tr: continue
        D = tr.get('dur', .5); typ = tr.get('type')
        if side == 'out' and t > dur - D: u = (t - (dur - D)) / D
        elif side == 'in' and t < D: u = 1 - t / D
        else: continue
        at = tr.get('at', [960, 540]); ax, ay = at[0] * k, at[1] * k
        if typ == 'zoom':
            fr = zoom_blur(fr, .9 * u ** 1.5, W / 2, H / 2)
            if u > .7: fr = Image.blend(fr, Image.new('RGBA', fr.size, (255, 255, 255, 255)), (u - .7) / .3 * .85)
        elif typ == 'whip':
            dr = tr.get('dir', 1) * (1 if side == 'out' else -1)
            fr = motion_blur(ImageChops.offset(fr, int(-dr * u ** 2 * W * .6), 0), -dr * u * 260 * k)
        elif typ == 'iris':
            r = (1 - u) ** 1.6 * math.hypot(W, H)
            m = Image.new('L', fr.size, 0); ImageDraw.Draw(m).ellipse((ax - r, ay - r, ax + r, ay + r), fill=255)
            bg = Image.new('RGBA', fr.size, tuple(tr.get('color', (36, 28, 52))) + (255,)); bg.paste(fr, (0, 0), m); fr = bg
        elif typ == 'flash':
            fr = Image.blend(fr, Image.new('RGBA', fr.size, (255, 255, 255, 255)), u ** 2)
        elif typ == 'fade':
            fr = Image.blend(fr, Image.new('RGBA', fr.size, (0, 0, 0, 255)), u)
        else:
            fr = apply_ext_trans(fr, typ, tr, max(0, min(1, u)), k, side)
    return fr


# =====================================================================
# 镜头预设库（camera.preset）—— 一个名字就是一种运镜，at 指定目标点，amt 调强度（默认 1）
# 和 keys 二选一；预设会自动带上合适的 parallax / shake / blur。
# =====================================================================
def _K(t, z=1, c=(960, 540), e='inout', roll=0, blur=0):
    return dict(t=t, zoom=z, center=list(c), ease=e, roll=roll, blur=blur)

def preset_keys(p, dur):
    """返回 (keys, extra)；extra 可含 parallax、shake、shake_at"""
    n = p['preset']; a = p.get('amt', 1); X, Y = p.get('at', [960, 540]); d = dur; ex = {}
    m = lambda z: 1 + (z - 1) * a
    if n == 'push_in':        ks = [_K(0, 1), _K(d, m(1.12))]
    elif n == 'pull_out':     ks = [_K(0, m(1.14), (X, Y)), _K(d, 1)]
    elif n == 'pan_l':        ks = [_K(0, 1.14, (960 + 150 * a, Y)), _K(d, 1.14, (960 - 150 * a, Y), 'linear')]
    elif n == 'pan_r':        ks = [_K(0, 1.14, (960 - 150 * a, Y)), _K(d, 1.14, (960 + 150 * a, Y), 'linear')]
    elif n == 'tilt_up':      ks = [_K(0, 1.16, (X, 540 + 70 * a)), _K(d, 1.16, (X, 540 - 70 * a))]
    elif n == 'tilt_down':    ks = [_K(0, 1.16, (X, 540 - 70 * a)), _K(d, 1.16, (X, 540 + 70 * a))]
    elif n == 'crane_up':     ks = [_K(0, m(1.5), (X, Y)), _K(min(.9, d * .2), m(1.5), (X, Y)), _K(min(3, d * .7), 1)]; ex['parallax'] = 1
    elif n == 'crane_down':   ks = [_K(0, 1, (960, 480)), _K(d, m(1.22), (X, Y + 60))]; ex['parallax'] = 1
    elif n == 'snap_zoom':    ks = [_K(0, 1), _K(d * .35, 1.03), _K(d * .35 + .35, m(1.7), (X, Y), 'snap'), _K(d, m(1.75), (X, Y), 'linear')]
    elif n == 'snap_back':    ks = [_K(0, m(1.7), (X, Y)), _K(.35, 1, (960, 540), 'snap'), _K(d, 1.04)]
    elif n == 'reveal_pull':  ks = [_K(0, m(1.8), (X, Y)), _K(1.2, m(1.75), (X, Y)), _K(min(d, 3), 1, (960, 540), 'out')]
    elif n == 'truck_l':      ks = [_K(0, 1.18, (1160, Y)), _K(d, 1.18, (760, Y), 'linear')]; ex['parallax'] = .8
    elif n == 'truck_r':      ks = [_K(0, 1.18, (760, Y)), _K(d, 1.18, (1160, Y), 'linear')]; ex['parallax'] = .8
    elif n == 'diagonal':     ks = [_K(0, 1.05, (860, 600)), _K(d, m(1.18), (1060, 470))]
    elif n == 'dolly_zoom':   ks = [_K(0, 1, (X, Y)), _K(d, m(1.28), (X, Y), 'inout')]; ex['parallax'] = -1.1
    elif n == 'orbit':        ks = [_K(0, 1.16, (820, Y), roll=-3 * a), _K(d, 1.16, (1100, Y), 'inout', 3 * a)]; ex['parallax'] = 1
    elif n == 'dutch':        ks = [_K(0, 1.08), _K(.8, 1.12, (X, Y), 'out', -6 * a), _K(d, 1.14, (X, Y), 'linear', -6 * a)]
    elif n == 'handheld':     ks = [_K(0, 1.06), _K(d, 1.08)]; ex['shake'] = 3 * a
    elif n == 'impact':       t0 = d * .4; ks = [_K(0, 1), _K(t0, 1.02), _K(t0 + .2, m(1.3), (X, Y), 'snap'), _K(d, m(1.32), (X, Y))]; ex['shake_at'] = [t0 + .15, .5, 14 * a]
    elif n == 'bounce':       ks = [_K(0, 1), _K(min(d, 1.2), m(1.25), (X, Y), 'back'), _K(d, m(1.27), (X, Y))]
    elif n == 'double_punch': ks = [_K(0, 1), _K(d * .3, 1), _K(d * .3 + .3, m(1.25), (X, Y), 'snap'), _K(d * .6, m(1.25), (X, Y)), _K(d * .6 + .3, m(1.55), (X, Y), 'snap'), _K(d, m(1.56), (X, Y))]
    elif n == 'drift':        ks = [_K(0, 1.08, (900, 540)), _K(d, 1.08, (1020, 530), 'linear')]; ex['parallax'] = 1.2
    elif n == 'parallax_push':ks = [_K(0, 1), _K(d, m(1.16), (X, Y))]; ex['parallax'] = 1
    elif n == 'rack_focus':   ks = [_K(0, 1.02, blur=14 * a), _K(min(1.1, d * .3), 1.04, e='out'), _K(d, 1.09)]
    elif n == 'focus_out':    ks = [_K(0, 1), _K(max(0, d - .9), 1.06), _K(d, 1.08, blur=14 * a, e='in')]
    elif n == 'point_back':   ks = [_K(0, 1), _K(d * .3, m(1.6), (X, Y), 'out'), _K(d * .65, m(1.6), (X, Y)), _K(d, 1)]
    elif n == 'pan_settle':   ks = [_K(0, 1.2, (960 - 260 * a, Y)), _K(min(d, 1.4), 1.2, (X, Y), 'back'), _K(d, 1.22, (X, Y))]
    elif n == 'pedestal_up':  ks = [_K(0, 1.14, (X, 600)), _K(d, 1.14, (X, 470), 'linear')]
    elif n == 'spiral_in':    ks = [_K(0, 1, roll=0), _K(d, m(1.35), (X, Y), 'inout', 8 * a)]
    elif n == 'breath':       ks = [_K(i * d / 4, 1.03 if i % 2 == 0 else 1.07) for i in range(5)]
    elif n == 'look_around':  ks = [_K(0, 1.16, (760, Y)), _K(d * .45, 1.16, (1160, Y)), _K(d, 1.12, (960, Y))]; ex['parallax'] = .8
    elif n == 'wide_reveal':  ks = [_K(0, m(1.4), (X, Y)), _K(d, 1, (960, 540), 'linear')]; ex['parallax'] = .9
    elif n == 'lock':         ks = [_K(0, 1), _K(d, 1)]
    else: raise ValueError('未知镜头预设 ' + n)
    for k in ks: k['t'] = max(0, min(d, k['t']))
    return ks, ex

PRESETS = ['push_in', 'pull_out', 'pan_l', 'pan_r', 'tilt_up', 'tilt_down', 'crane_up', 'crane_down', 'snap_zoom', 'snap_back', 'reveal_pull',
           'truck_l', 'truck_r', 'diagonal', 'dolly_zoom', 'orbit', 'dutch', 'handheld', 'impact', 'bounce', 'double_punch', 'drift',
           'parallax_push', 'rack_focus', 'focus_out', 'point_back', 'pan_settle', 'pedestal_up', 'spiral_in', 'breath', 'look_around', 'wide_reveal', 'lock']

def expand_cam(cam, dur):
    """把 preset 展开成 keys，并补上 parallax/shake；其余字段（手写的 parallax 等）优先"""
    if not cam.get('preset'): return cam
    ks, ex = preset_keys(cam, dur); c = dict(ex); c.update({k: v for k, v in cam.items() if k != 'preset'}); c['keys'] = ks
    return c

def blur_at(ks, t):
    if not any(k.get('blur') for k in ks): return 0
    if t <= ks[0]['t']: return ks[0].get('blur', 0)
    for a, b in zip(ks, ks[1:]):
        if t <= b['t']:
            u = (t - a['t']) / max(1e-6, b['t'] - a['t']); e = EASE.get(b['ease'], EASE['inout'])(u)
            return a.get('blur', 0) + (b.get('blur', 0) - a.get('blur', 0)) * e
    return ks[-1].get('blur', 0)

def shake_off(cam, t):
    dx = dy = 0
    if cam.get('shake'): a_ = cam['shake']; dx += a_ * (math.sin(t * 7.1) + .5 * math.sin(t * 13.3)); dy += a_ * (math.sin(t * 6.3 + 1) + .5 * math.sin(t * 11.7))
    if cam.get('shake_at'):
        t0, D, A = cam['shake_at']
        if t0 <= t <= t0 + D:
            f = (1 - (t - t0) / D) ** 2 * A; dx += f * math.sin(t * 61); dy += f * math.cos(t * 53)
    return dx, dy


# =====================================================================
# 扩展转场（shot.in / shot.out 的 type）—— 每个镜头只管自己的头尾，拼接后两半合成一个完整转场
# 通用参数：dur 时长、color 色板颜色（默认深紫 [36,28,52]）、dir 方向（l/r/u/d）、at 中心点
# =====================================================================
def _plate(fr, tr, default=(36, 28, 52)):
    return Image.new('RGBA', fr.size, tuple(tr.get('color', default))[:3] + (255,))

def _star(cx, cy, R, n=5, rot=-90):
    pts = []
    for i in range(n * 2):
        r = R if i % 2 == 0 else R * .45; a = math.radians(rot + i * 180 / n); pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts

def _cover_mask(typ, tr, u, W, H, k):
    """返回 L 掩膜：255 = 被色板盖住；u=0 不盖、u=1 全盖"""
    m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m); at = tr.get('at', [960, 540]); ax, ay = at[0] * k, at[1] * k
    dr = tr.get('dir', 'r'); diag = math.hypot(W, H)
    if typ == 'wipe':
        if dr == 'r': d.rectangle((0, 0, W * u, H), fill=255)
        elif dr == 'l': d.rectangle((W * (1 - u), 0, W, H), fill=255)
        elif dr == 'd': d.rectangle((0, 0, W, H * u), fill=255)
        else: d.rectangle((0, H * (1 - u), W, H), fill=255)
    elif typ == 'clock': d.pieslice((ax - diag, ay - diag, ax + diag, ay + diag), -90, -90 + 360 * u, fill=255)
    elif typ == 'diamond': r = diag * u; d.polygon([(ax, ay - r), (ax + r, ay), (ax, ay + r), (ax - r, ay)], fill=255)
    elif typ == 'square': r = diag * .55 * u; d.rectangle((ax - r, ay - r, ax + r, ay + r), fill=255)
    elif typ == 'star_in': d.polygon(_star(ax, ay, diag * 1.4 * u, rot=-90 + 90 * u), fill=255)
    elif typ == 'blinds':
        n = tr.get('n', 8); h = H / n
        for i in range(n): d.rectangle((0, i * h, W, i * h + h * u), fill=255)
    elif typ == 'blinds_v':
        n = tr.get('n', 10); w = W / n
        for i in range(n): d.rectangle((i * w, 0, i * w + w * u, H), fill=255)
    elif typ == 'checker':
        n = 8; cw, ch = W / n, H / (n * 9 / 16); rows = int(math.ceil(H / ch))
        for i in range(n):
            for j in range(rows):
                v = min(1, max(0, u * 2 - ((i + j) % 2) * .5 - (i / n) * .5)); s = v / 2
                cx, cy = (i + .5) * cw, (j + .5) * ch; d.rectangle((cx - cw * s, cy - ch * s, cx + cw * s, cy + ch * s), fill=255)
    elif typ == 'doors': d.rectangle((0, 0, W / 2 * u, H), fill=255); d.rectangle((W - W / 2 * u, 0, W, H), fill=255)
    elif typ == 'bars': d.rectangle((0, 0, W, H / 2 * u), fill=255); d.rectangle((0, H - H / 2 * u, W, H), fill=255)
    elif typ == 'ink':
        random.seed(tr.get('seed', 3)); R = diag * u * 1.05; pts = []
        ph = [random.uniform(0, 6.3) for _ in range(4)]
        for j in range(72):
            a = j / 72 * 2 * math.pi; rr = R * (1 + .12 * math.sin(a * 3 + ph[0]) + .07 * math.sin(a * 7 + ph[1]) + .04 * math.sin(a * 13 + ph[2]))
            pts.append((ax + rr * math.cos(a), ay + rr * math.sin(a)))
        d.polygon(pts, fill=255)
    elif typ == 'bubbles':
        random.seed(tr.get('seed', 5))
        for j in range(26):
            x, y = random.uniform(0, W), random.uniform(0, H); st = random.uniform(0, .5); v = min(1, max(0, (u - st) / .5))
            r = v * random.uniform(.25, .4) * diag; d.ellipse((x - r, y - r, x + r, y + r), fill=255)
    return m

def _stripes(fr, tr, u, k, side):
    """MG 斜条色带扫过：几条彩色斜带依次划过，最后一条铺满（out）/ 退出（in）"""
    W, H = fr.size; cols = tr.get('colors', [[240, 138, 36], [232, 72, 59], [47, 111, 208]])
    out = fr.copy(); sk = H * .45
    for i, c in enumerate(cols):
        v = min(1, max(0, u * (1 + .25 * (len(cols) - 1)) - .25 * i)) if side == 'out' else min(1, max(0, u * (1 + .25 * (len(cols) - 1)) - .25 * (len(cols) - 1 - i)))
        if v <= 0: continue
        x = -sk + (W + sk * 2) * v
        lay = Image.new('L', fr.size, 0); ImageDraw.Draw(lay).polygon([(-sk, 0), (x + sk, 0), (x, H), (-sk * 2, H)] if side == 'out' else [(W + sk, 0), (W - (x - sk) + sk, 0), (W - (x - sk), H), (W + sk * 2, H)], fill=255)
        out.paste(Image.new('RGBA', fr.size, tuple(c) + (255,)), (0, 0), lay)
    return out

EXT_TRANS = ['wipe', 'clock', 'diamond', 'square', 'star_in', 'blinds', 'blinds_v', 'checker', 'doors', 'bars', 'ink', 'bubbles',
             'stripes', 'slide', 'shrink', 'flip', 'spin', 'blur', 'pixel', 'glitch', 'whip_v', 'dip']

def apply_ext_trans(fr, typ, tr, u, k, side):
    W, H = fr.size
    if typ in ('wipe', 'clock', 'diamond', 'square', 'star_in', 'blinds', 'blinds_v', 'checker', 'doors', 'bars', 'ink', 'bubbles'):
        uu = u if typ not in ('ink', 'bubbles', 'clock') else u ** .9
        m = _cover_mask(typ, tr, uu, W, H, k); out = fr.copy(); out.paste(_plate(fr, tr), (0, 0), m); return out
    if typ == 'stripes': return _stripes(fr, tr, u, k, side)
    if typ == 'slide':
        dr = tr.get('dir', 'l'); e = u ** 2 if side == 'out' else u ** 2
        dx, dy = {'l': (-W, 0), 'r': (W, 0), 'u': (0, -H), 'd': (0, H)}[dr]
        if side == 'in': dx, dy = -dx, -dy
        bg = _plate(fr, tr); bg.alpha_composite(fr, (int(dx * e), int(dy * e))); return bg
    if typ == 'shrink':
        s = max(.02, 1 - u * .85); w, h = int(W * s), int(H * s); im = fr.resize((w, h), Image.BILINEAR)
        mk = Image.new('L', (w, h), 0); ImageDraw.Draw(mk).rounded_rectangle((0, 0, w, h), int(40 * k * (1 - s) + 1), fill=int(255 * min(1, (1 - u) * 3)))
        bg = _plate(fr, tr); bg.paste(im, ((W - w) // 2, (H - h) // 2 - int(u * 40 * k)), mk); return bg
    if typ == 'flip':
        s = max(.01, abs(math.cos(u * math.pi / 2))); w = max(1, int(W * s)); im = fr.resize((w, H), Image.BILINEAR)
        bg = _plate(fr, tr); bg.paste(im, ((W - w) // 2, 0)); return bg
    if typ == 'spin':
        z = 1 + u * 1.5; im = fr.rotate(u * 160 * (1 if side == 'out' else -1), resample=Image.BILINEAR)
        w, h = W / z, H / z; im = im.crop((int((W - w) / 2), int((H - h) / 2), int((W + w) / 2), int((H + h) / 2))).resize((W, H), Image.BILINEAR)
        return Image.blend(im, Image.new('RGBA', fr.size, (255, 255, 255, 255)), u ** 3)
    if typ == 'blur':
        im = fr.filter(ImageFilter.GaussianBlur(u * 38 * k)); return Image.blend(im, Image.new('RGBA', fr.size, (255, 255, 255, 255)), u ** 4 * .6)
    if typ == 'pixel':
        n = max(1, int(1 + u ** 2 * 60 * k)); im = fr.resize((max(1, W // n), max(1, H // n)), Image.BILINEAR).resize((W, H), Image.NEAREST); return im
    if typ == 'glitch':
        random.seed(int(u * 40)); r, g, b, a = fr.split(); o = int(u * 40 * k)
        im = Image.merge('RGBA', (ImageChops.offset(r, o, 0), g, ImageChops.offset(b, -o, 0), a))
        for _ in range(int(u * 10)):
            y = random.randint(0, H - 40); h = random.randint(8, int(60 * k)); sl = im.crop((0, y, W, y + h)); im.paste(ImageChops.offset(sl, random.randint(-int(120 * k * u), int(120 * k * u)), 0), (0, y))
        return Image.blend(im, Image.new('RGBA', fr.size, (255, 255, 255, 255)), max(0, u - .8) * 4)
    if typ == 'whip_v':
        dr = 1 if tr.get('dir', 'u') == 'u' else -1; dr *= (1 if side == 'out' else -1); dy = int(-dr * u ** 2 * H * .6); acc = ImageChops.offset(fr, 0, dy); base = acc.copy()
        for j in range(1, 8): acc = Image.blend(acc, ImageChops.offset(base, 0, int(-dr * u * 200 * k * j / 8)), 1 / (j + 1))
        return acc
    if typ == 'dip': return Image.blend(fr, _plate(fr, tr, (240, 138, 36)), u)
    return fr
