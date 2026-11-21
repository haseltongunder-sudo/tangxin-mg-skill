"""成片总装：拼接各镜头 MP4 → 顶部章节进度条（可选）/ 底部进度条（可选）→ 全程配乐（自动避让人声）→ MP4 章节

用法：python3 assemble.py 总装.json [--no-lint]
总装.json：
{
  "shots": ["shot01.mp4", "shot02.mp4", ...],      # 按顺序，路径相对本 json
  "out": "成片.mp4",
  "chapters": [{"shot": 1, "title": "骨折"}, {"shot": 4, "title": "四信号"}, {"shot": 9, "title": "考考你", "quiz": true}, ...],
  "topbar": true,          # 顶部章节进度条（节点 + 标签，已讲完打红十字、当前红字、未讲灰色）；不要就 false
  "topbar_style": {"y": 40, "x0": 180, "x1": 1600, "color": "#2F6FDE", "ink": "#22345F"},   # color 不填用顶层 accent（默认教学蓝；"fire"=消防红）
  "bottombar": "auto",     # 底部细进度条 + 「考」点；auto（默认）= 有答题镜头就自动开；true/false 强制开关
  "accent": "#2F6FDE",     # 进度条主色；"fire" = #E8483B
  "lint": true,            # 开工前对各镜头 json（与 mp4 同名的 .json）做规则检查，有错误就停；false 或 --no-lint 跳过
  "bgm": "auto",           # auto = 用 bgm.py 合成一段轻快配乐；也可以给自己的音乐文件路径；不要就删掉
  "bgm_vol": 0.16,         # 配乐音量（人声出现时自动压低，sidechain ducking）
  "title": "骨折急救",
  "interactive": "互动.json",   # 可选：同时出互动版。先比对 MP4 答题镜头和互动版 questions（数量/顺序/题目/答案/位置，
                                #   不一致报 E-quiz-mismatch 并停止），成片后调用 interactive.py → {title}_互动版/ + zip
  "interactive_video": "noquiz" # noquiz（默认）= 互动版用去掉答题镜头的「无题版」（自动拼 {out}_无题版.mp4），题目 t 按无题版时间轴；
                                # full = 互动版直接用完整成片，题目 t 落在对应答题镜头内
}
章节写进 MP4 元数据（播放器里可以按章节跳），进度条和章节用的是各镜头的实际时长，不用手算。
答题位置自动识别：与镜头 mp4 同名的 .json 里有 "quiz" 的镜头，或 chapters 里标了 "quiz": true 的章节；
顶部章节条和底部进度条都会在这些位置画「考」标记。
"""
import os, sys, json, subprocess, shutil, math, tempfile
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ui, lint

def dur(f): return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]))

def _kao(d, x, y, r, col=(240, 138, 36)):
    d.ellipse((x - r, y - r, x + r, y + r), fill=col, outline='white', width=3); d.text((x, y - 1), '考', font=ui.F(r * 1.15), fill='white', anchor='mm')

def topbar_frame(chs, T, t, st, W=1920, H=140, quiz_t=()):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    y = st.get('y', 40); x0, x1 = st.get('x0', 180), st.get('x1', 1600); red = ui.hexc(st.get('color') or ui.ACCENT); ink = ui.hexc(st.get('ink', '#22345F')); grey = (190, 196, 206)
    n = len(chs); xs = [x0 + (x1 - x0) * i / max(1, n - 1) for i in range(n)]
    cur = max(i for i, c in enumerate(chs) if c['t'] <= t + 1e-6)
    c_end = chs[cur + 1]['t'] if cur + 1 < n else T; u = min(1, (t - chs[cur]['t']) / max(.01, c_end - chs[cur]['t']))
    head = xs[cur] + ((xs[cur + 1] - xs[cur]) * u if cur + 1 < n else 0)
    d.line([(x0, y), (x1, y)], fill=(255, 255, 255, 200), width=10); d.line([(x0, y), (x1, y)], fill=grey + (255,), width=6)
    d.line([(x0, y), (head, y)], fill=red + (255,), width=6)
    f = ui.F(st.get('size', 24))
    for i, (x, c) in enumerate(zip(xs, chs)):
        s = 11
        if i <= cur:
            d.rectangle((x - s, y - s, x + s, y + s), fill=red, outline='white', width=2); ui._cross(d, x, y, 13)
        else:
            d.rounded_rectangle((x - s + 2, y - s + 2, x + s - 2, y + s - 2), 4, fill='white', outline=grey, width=3)
        col = red if i == cur else (ink if i < cur else (150, 156, 168))
        d.text((x, y + 38), c['title'], font=ui.F(st.get('size', 24) * (1.15 if i == cur else 1)), fill=col, anchor='mm', stroke_width=3, stroke_fill=(255, 255, 255))
    # 答题位置的「考」标记：按时间落在相邻两个章节节点之间；和节点重合时挂在节点右上角
    for qt in quiz_t:
        j = max([i for i, c in enumerate(chs) if c['t'] <= qt + 1e-6] or [0]); e = chs[j + 1]['t'] if j + 1 < n else T
        qx = xs[j] + ((xs[j + 1] - xs[j]) * (qt - chs[j]['t']) / max(.01, e - chs[j]['t']) if j + 1 < n else 0)
        if min(abs(qx - x) for x in xs) < 26: _kao(d, qx + 16, y - 15, 11)
        else: _kao(d, qx, y, 14)
    if cur + 1 < n or u < 1:
        d.ellipse((head - 14, y - 14, head + 14, y + 14), fill='white', outline=ink, width=4); d.ellipse((head - 5, y - 5, head + 5, y + 5), outline=red, width=2)
    return im

def bottombar_png(quiz_t, T, path):
    X0, X1, Y0, Y1 = 60, 1860, 1050, 1060
    tr = Image.new('RGBA', (1920, 1080)); d = ImageDraw.Draw(tr); d.rounded_rectangle((X0, Y0, X1, Y1), 5, fill=(255, 255, 255, 150))
    for qt in quiz_t:
        _kao(d, X0 + (X1 - X0) * qt / T, 1055, 17, (232, 72, 59))
    tr.save(path)

def shot_jsons(cfg, shots):
    """每个镜头 mp4 对应的镜头 json（同名 .json，或 cfg["shot_jsons"] 显式给出）→ [(路径或 None, 镜头列表)]"""
    out = []
    explicit = cfg.get('shot_jsons')
    for i, mp4 in enumerate(shots):
        jp = os.path.join(os.path.dirname(mp4), explicit[i]) if explicit else os.path.splitext(mp4)[0] + '.json'
        if os.path.exists(jp):
            try: c = json.load(open(jp)); out.append((jp, c.get('shots', []), c)); continue
            except Exception: pass
        out.append((None, [], {}))
    return out

def main():
    args = [x for x in sys.argv[1:] if not x.startswith('--')]; no_lint = '--no-lint' in sys.argv
    if not args: print(__doc__); sys.exit(1)
    cp = args[0]; cfg = json.load(open(cp)); base = os.path.dirname(os.path.abspath(cp)); tmp = tempfile.mkdtemp(prefix='mg_asm_')
    ui.set_accent(cfg.get('accent'))
    shots = [os.path.join(base, s) for s in cfg['shots']]
    miss = [s for s in shots if not os.path.exists(s)]
    if miss: sys.exit('镜头文件不存在：\n  ' + '\n  '.join(miss))
    sj = shot_jsons(cfg, shots)
    ds = [dur(s) for s in shots]; st = [sum(ds[:i]) for i in range(len(ds) + 1)]; T = st[-1]
    inter = None
    if cfg.get('interactive'):
        ic = cfg['interactive']; inter = json.load(open(os.path.join(base, ic))) if isinstance(ic, str) else dict(ic)
    if not no_lint and cfg.get('lint', True) is not False:
        flat, spans = [], []
        for i, (jp, ss, _) in enumerate(sj):
            if not jp: continue
            dd = [x.get('dur', 4) for x in ss]; tot = sum(dd) or 1; acc = 0
            for k, x in enumerate(ss):
                flat.append(dict(x, _base=os.path.dirname(jp), _src=os.path.basename(jp) + (f'#{k + 1}' if len(ss) > 1 else '')))
                a0 = st[i] + ds[i] * acc / tot; acc += dd[k]; spans.append((a0, st[i] + ds[i] * acc / tot))
        errs, warns = lint.check(flat, episode=len(flat) >= lint.EPISODE_MIN) if flat else ([], [])
        if inter is not None:
            full = all(jp for jp, _, _ in sj)
            errs += lint.quiz_match(flat, inter.get('questions', []), spans if full else None, cfg.get('interactive_video', 'noquiz'))
        if flat or errs: lint.report(errs, warns)
        if errs: sys.exit('规则检查未通过，已停止（确需跳过：--no-lint 或 json 顶层 "lint": false）')
    chs = [dict(c, t=st[c['shot'] - 1]) for c in cfg.get('chapters', [])]
    # 答题位置：镜头 json 里的 quiz（按该镜头内多个子镜头的时长比例估算起点），以及 chapters 里的 quiz:true
    quiz_t = []
    for i, (jp, ss, _) in enumerate(sj):
        if any(x.get('quiz') for x in ss):
            dd = [x.get('dur', 4) for x in ss]; tot = sum(dd) or 1; acc = 0
            for x, d_ in zip(ss, dd):
                if x.get('quiz'): quiz_t.append(st[i] + ds[i] * acc / tot)
                acc += d_
    for c in chs:
        if c.get('quiz') and not any(abs(c['t'] - q) < .5 for q in quiz_t): quiz_t.append(c['t'])
    quiz_t.sort()
    bb = cfg.get('bottombar', 'auto'); bottombar = bool(quiz_t) if bb == 'auto' else bool(bb)
    open(f'{tmp}/l.txt', 'w').write(''.join(f"file '{s}'\n" for s in shots))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{tmp}/l.txt', '-c', 'copy', f'{tmp}/raw.mp4'], check=True)
    vw, vh = map(int, subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', shots[0]]).decode().strip().split(','))
    sk = vw / 1920; tbh = int(round(140 * sk / 2)) * 2
    fps = 30; ins = ['-i', f'{tmp}/raw.mp4']; fc = '[0:v]null[v0]'; last = 'v0'; idx = 1
    if cfg.get('topbar') and chs:
        tb = f'{tmp}/topbar.mov'
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{vw}x{tbh}', '-r', str(fps), '-i', '-', '-c:v', 'qtrle', tb], stdin=subprocess.PIPE)
        for i in range(int(math.ceil(T * fps))): fm = topbar_frame(chs, T, i / fps, cfg.get('topbar_style', {}), quiz_t=quiz_t); p.stdin.write((fm if sk == 1 else fm.resize((vw, tbh), Image.LANCZOS)).tobytes())
        p.stdin.close(); p.wait()
        ins += ['-i', tb]; fc += f';[{last}][{idx}:v]overlay=0:0:eof_action=pass[v{idx}]'; last = f'v{idx}'; idx += 1
    if bottombar:
        bottombar_png(quiz_t, T, f'{tmp}/track.png'); sp = Image.new('RGBA', (3600, 10)); ImageDraw.Draw(sp).rectangle((0, 0, 1799, 9), fill=(240, 138, 36, 255)); sp.save(f'{tmp}/strip.png')
        ins += ['-i', f'{tmp}/track.png', '-loop', '1', '-i', f'{tmp}/strip.png']
        fc += f";[{idx + 1}:v]crop=1800:10:x='1800-1800*t/{T:.3f}':y=0[s];[{last}][{idx}:v]overlay[b0];[b0][s]overlay=x=60:y=1050:shortest=1[vb]"; last = 'vb'; idx += 2
    amap = '0:a'
    if cfg.get('bgm'):
        bg = cfg['bgm']
        if bg == 'auto':
            bg = f'{tmp}/bgm.wav'; subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bgm.py'), bg, str(int(T) + 2), cfg.get('bgm_mood', 'bright')], check=True)
        else: bg = os.path.join(base, bg)
        ins += ['-stream_loop', '-1', '-i', bg]
        fc += (f";[0:a]asplit=2[vo][sc];[{idx}:a]volume={cfg.get('bgm_vol', .16)},atrim=0:{T:.3f},afade=t=out:st={T - 2:.3f}:d=2[m0];[m0][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[m1];"
               f"[vo][m1]amix=inputs=2:duration=first:normalize=0[a]"); amap = '[a]'; idx += 1
    m = f";FFMETADATA1\ntitle={cfg.get('title', '')}\n"
    for i, c in enumerate(chs):
        e = chs[i + 1]['t'] if i + 1 < len(chs) else T; m += f"[CHAPTER]\nTIMEBASE=1/1000\nSTART={int(c['t'] * 1000)}\nEND={int(e * 1000)}\ntitle={c['title']}\n"
    open(f'{tmp}/chap.txt', 'w').write(m); ins += ['-i', f'{tmp}/chap.txt']
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + ins + ['-filter_complex', fc, '-map', f'[{last}]', '-map', amap, '-map_metadata', str(idx), '-map_chapters', str(idx),
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', f'{tmp}/final.mp4'], check=True)
    out = os.path.join(base, cfg.get('out', '成片.mp4')); shutil.copy(f'{tmp}/final.mp4', out)   # 先写本地临时目录再拷贝（网络盘上 faststart 会失败）
    if inter is not None: build_interactive(cfg, inter, base, out, shots, sj, tmp)
    shutil.rmtree(tmp, ignore_errors=True)
    print('done', out, round(T, 1), [(c['title'], round(c['t'], 1)) for c in chs], '考:', [round(q, 1) for q in quiz_t])


def build_interactive(cfg, inter, base, out, shots, sj, tmp):
    """互动版：默认用去掉答题镜头的无题版视频（答题交给网页弹题），再调 interactive.py"""
    mode = cfg.get('interactive_video', 'noquiz'); video = out
    if mode != 'full':
        mixed = [os.path.basename(m) for m, (jp, ss, _) in zip(shots, sj) if any(x.get('quiz') for x in ss) and not all(x.get('quiz') for x in ss)]
        if mixed: sys.exit(f'无题版需要答题镜头单独成文件，这些 mp4 里答题和讲解混在一起：{mixed}；拆开或写 "interactive_video": "full"')
        keep = [m for m, (jp, ss, _) in zip(shots, sj) if not any(x.get('quiz') for x in ss)]
        open(f'{tmp}/nq.txt', 'w').write(''.join(f"file '{m}'\n" for m in keep))
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{tmp}/nq.txt', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                        '-movflags', '+faststart', f'{tmp}/nq.mp4'], check=True)
        video = os.path.splitext(out)[0] + '_无题版.mp4'; shutil.copy(f'{tmp}/nq.mp4', video)
    ic = dict(inter, video=os.path.abspath(video))
    ic.setdefault('title', cfg.get('title') or '互动微课'); ic.setdefault('accent', cfg.get('accent'))
    if ic.get('accent') is None: ic.pop('accent')
    jp = f'{tmp}/互动.json'; json.dump(ic, open(jp, 'w'), ensure_ascii=False)
    od = os.path.join(base, ic['title'] + '_互动版')
    subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'interactive.py'), jp, od], check=True)

if __name__ == '__main__':
    main()
