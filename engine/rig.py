"""程序化口型 / 眨眼生成器：在定稿角色底图上贴嘴型、闭眼，输出 compose.py 直接能用的 talk / idle 帧序列

用法：python3 rig.py chars.json

chars.json（路径都相对这个 json 文件）：
{
  "out_dir": "frames",
  "chars": {
    "teacher": {
      "src": "teacher.png",                      # 透明底 PNG（正面、闭嘴微笑的定稿图）
      "mouth": [cx, cy, w],                      # 嘴中心坐标 + 嘴宽（像素，按底图原尺寸）
      "eyes": [[cx, cy, rx, ry], [cx, cy, rx, ry]],  # 每只眼睛的中心和半径
      "crop": [x0, y0, x1, y1],                  # 可选：输出前裁切（不填就整图输出，compose 会自动裁到人物外框）
      "scale": 1.0,                              # 可选：嘴部细节（上唇弧、张口深度）的像素放大倍数，底图很大/很小时调
      "poses": {                                 # 可选：其他姿势（如指黑板），mouth / eyes 不填就沿用上面的
        "point": {"src": "teacher_point.png", "mouth": [...], "eyes": [...]}
      }
    }
  }
}
输出：<out_dir>/<name>_talk/  <name>_idle/  以及每个姿势 <name>_<pose>_talk/  <name>_<pose>_idle/
帧文件名 <首字母>_<序号>_<毫秒>ms.png（compose.py load_frames 按文件名里的 “数字ms” 读每帧时长）。
另存 <out_dir>/rig_check.jpg：每个角色/姿势的 闭嘴 / 半张 / 大张 / 闭眼 四格检查图。
在 compose 里这样用：{"src": "frames/teacher_talk", "idle": "frames/teacher_idle", "talk": [[0.4, 2.1]], ...}
"""
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import numpy as np
import os, sys, json, math, shutil

SS = 4
TALK = [(1, 'open', 90), (3, 'open', 100), (2, 'open', 90), (4, 'open', 110), (2, 'open', 80), (1, 'open', 70), (3, 'open', 100), (2, 'half', 70),
        (1, 'closed', 80), (2, 'half', 70), (4, 'open', 110), (3, 'open', 90), (1, 'open', 80), (2, 'open', 90)]
IDLE = [(0, 'open', 2600), (0, 'half', 60), (0, 'closed', 90), (0, 'half', 60), (0, 'open', 1900), (0, 'closed', 100)]


def skin(im, x, y, r=3):
    """取肤色：只看邻域里不透明的像素（alpha>200），取各通道中位数；邻域里没有就逐步扩大。
    这样嘴/眼靠近轮廓或透明边时不会取到透明像素的黑色 RGB（旧版的暗色光晕就是这么来的）"""
    W, H = im.size; x = max(0, min(W - 1, int(x))); y = max(0, min(H - 1, int(y)))
    for rr in (r, r * 3, r * 8, r * 20):
        px = np.asarray(im.crop((max(0, x - rr), max(0, y - rr), min(W, x + rr + 1), min(H, y + rr + 1))))
        m = px[..., 3] > 200
        if m.sum() >= 3: return tuple(int(v) for v in np.median(px[m][:, :3], axis=0))
    return im.getpixel((x, y))[:3]


def _over(im, lay):
    """把 lay 叠到 im 上，但只叠在 im 原本不透明的地方（按 im 的 alpha 裁剪），不会把肤色涂到人物轮廓外"""
    a = ImageChops.multiply(lay.getchannel('A'), im.getchannel('A'))
    lay = lay.copy(); lay.putalpha(a); im.alpha_composite(lay)


def patch(im, draw_fn):
    """4 倍超采样画矢量补丁再缩回（Pillow 的 RGBA 缩放内部按预乘 alpha 处理，透明区不会混入黑色）"""
    W, H = im.size; big = Image.new('RGBA', (W * SS, H * SS)); d = ImageDraw.Draw(big); draw_fn(d)
    _over(im, big.resize((W, H), Image.LANCZOS))


def mouth(im, m, op, s=1.0):
    """自然口型：先用肤色盖掉原来的微笑线，再画一张“笑着张开”的嘴：上沿是浅浅的笑弧，下沿随张口变深，嘴角收尖"""
    cx, cy, w = m
    a1 = skin(im, cx - w * 1.0, cy - 6 * s); a2 = skin(im, cx + w * 1.0, cy - 6 * s); sk = tuple((p + q) // 2 for p, q in zip(a1, a2))
    lay = Image.new('RGBA', im.size, sk + (0,)); ImageDraw.Draw(lay).ellipse((cx - w * .9, cy - 14 * s, cx + w * .9, cy + 11 * s), fill=sk + (255,))
    _over(im, lay.filter(ImageFilter.GaussianBlur(2 * s)))   # lay 的透明底色就是肤色，模糊时边缘不会变暗

    def f(d):
        S = SS
        hw = w * (.58 + .02 * op); top = cy - 9 * s; hh = (2 + op * 2.6) * s; N = 24; arc = 5 * s
        up = [(cx - hw + 2 * hw * i / N, top + arc * math.sin(math.pi * i / N)) for i in range(N + 1)]
        lo = [(cx + hw - 2 * hw * i / N, top + arc * math.sin(math.pi * i / N) + hh * math.sin(math.pi * i / N) ** 0.8) for i in range(N + 1)]
        pts = [(x * S, y * S) for x, y in up + lo]
        d.polygon(pts, fill=(122, 42, 40, 255))
        if op >= 2:
            tw = hw * .5; ty = top + arc + hh * .55
            d.chord(((cx - tw) * S, ty * S, (cx + tw) * S, (top + arc + hh + hh * .5) * S), 180, 360, fill=(226, 118, 112, 255))
        d.line(pts[:N + 1], fill=(96, 42, 36, 255), width=max(1, int(1.6 * S * s)))
    patch(im, f)


def eyes(im, E, st, s=1.0):
    if st == 'open': return

    def f(d):
        S = SS; lw = max(1, int(3 * S * s))
        for cx, cy, rx, ry in E:
            sk = skin(im, cx, cy + ry + 6 * s)
            if st == 'closed':
                d.ellipse(((cx - rx - 3 * s) * S, (cy - ry - 2 * s) * S, (cx + rx + 3 * s) * S, (cy + ry + 3 * s) * S), fill=sk + (255,))
                d.arc(((cx - rx) * S, (cy - ry * .9) * S, (cx + rx) * S, (cy + ry * .9) * S), 15, 165, fill=(40, 30, 30, 255), width=lw)
            else:
                d.chord(((cx - rx - 3 * s) * S, (cy - ry - 3 * s) * S, (cx + rx + 3 * s) * S, (cy + ry + 3 * s) * S), 180, 360, fill=sk + (255,))
                d.line(((cx - rx) * S, cy * S, (cx + rx) * S, cy * S), fill=(40, 30, 30, 255), width=lw)
    patch(im, f)


def frame(spec, op, st):
    im = Image.open(spec['src']).convert('RGBA'); s = spec.get('scale', 1.0)
    if op > 0: mouth(im, spec['mouth'], op, s)
    eyes(im, spec['eyes'], st, s)
    return im.crop(tuple(spec['crop'])) if spec.get('crop') else im


def variants(name, c, base):
    """展开 base + poses → [(输出名, spec)]"""
    def norm(d, inherit):
        sp = dict(inherit); sp.update({k: v for k, v in d.items() if k != 'poses'})
        sp['src'] = os.path.join(base, d['src']) if 'src' in d else inherit.get('src')
        for key in ('mouth', 'eyes'):
            if not sp.get(key): raise SystemExit(f'rig.py：{name} 缺少 {key}')
        if not sp.get('src') or not os.path.exists(sp['src']): raise SystemExit(f'rig.py：找不到底图 {sp.get("src")}（角色 {name}）')
        return sp
    b = norm(c, {}); out = [(name, b)]
    for pn, pd in (c.get('poses') or {}).items():
        out.append((f'{name}_{pn}', norm(pd, {k: v for k, v in b.items() if k in ('mouth', 'eyes', 'scale', 'crop', 'src')})))
    return out


def main():
    if len(sys.argv) < 2: print(__doc__); sys.exit(1)
    cp = os.path.abspath(sys.argv[1]); base = os.path.dirname(cp); cfg = json.load(open(cp))
    od = os.path.join(base, cfg.get('out_dir', 'frames')); os.makedirs(od, exist_ok=True)
    talk = [tuple(x) for x in cfg.get('talk_seq', TALK)]; idle = [tuple(x) for x in cfg.get('idle_seq', IDLE)]
    allv = []
    for name, c in cfg['chars'].items(): allv += variants(name, c, base)
    for vn, sp in allv:
        pre = vn[0]
        for kind, seq in (('talk', talk), ('idle', idle)):
            dd = os.path.join(od, f'{vn}_{kind}'); shutil.rmtree(dd, ignore_errors=True); os.makedirs(dd)
            for i, (op, st, ms) in enumerate(seq): frame(sp, op, st).save(f'{dd}/{pre}_{i:02d}_{ms}ms.png')
        print('rig', vn, '→', f'{vn}_talk/ ({len(talk)} 帧)', f'{vn}_idle/ ({len(idle)} 帧)')
    # 检查图：每个变体 闭嘴 / 半张 / 大张 / 闭眼，裁到嘴眼附近
    cw = 190; sheet = Image.new('RGB', (len(allv) * 4 * cw, 200), 'white')
    for j, (vn, sp) in enumerate(allv):
        (mx, my, mw) = sp['mouth']; ex = [e[0] for e in sp['eyes']]; ey = [e[1] for e in sp['eyes']]
        x0 = min(ex + [mx - mw]) - 60; x1 = max(ex + [mx + mw]) + 60; y0 = min(ey) - 60; y1 = my + 50
        ox, oy = (sp['crop'][0], sp['crop'][1]) if sp.get('crop') else (0, 0)
        for i, (op, st) in enumerate([(0, 'open'), (2, 'open'), (4, 'open'), (0, 'closed')]):
            im = frame(sp, op, st).crop((int(x0 - ox), int(y0 - oy), int(x1 - ox), int(y1 - oy)))
            bg = Image.new('RGBA', im.size, 'white'); bg.alpha_composite(im); bg = bg.convert('RGB'); bg.thumbnail((cw, 200))
            sheet.paste(bg, ((j * 4 + i) * cw, 0))
    sheet.save(os.path.join(od, 'rig_check.jpg')); print('check', os.path.join(od, 'rig_check.jpg'))


if __name__ == '__main__':
    main()
