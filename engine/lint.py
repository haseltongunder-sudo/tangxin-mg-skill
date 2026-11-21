"""出片规则检查（compose.py / assemble.py / render_shots.py 开工前自动调用；有错误就停）

用法：python3 lint.py 文件或目录 ... [--interactive 互动.json]
      镜头 json（compose 格式，含 "shots"），多个文件按顺序视为同一集
      目录：优先取其中的 shot*.json，没有就取所有含 "shots" 的 json
      --interactive：再拿互动版题目和 MP4 答题镜头比对数量、顺序、题目（E-quiz-mismatch）
代码里：import lint; errors, warnings = lint.check(shots)        # shots = 镜头 dict 列表（整集按顺序摊平）
      每个镜头可带 _base（素材相对路径的基准目录，默认当前目录）和 _src（报错时显示的来源）
      check(shots, episode=False) 只做逐镜头检查，不做整集统计类警告；CLI 和各脚本在镜头数 <4 时自动这样做
      quiz_match(shots, questions, ...) 比对 MP4 答题镜头和互动版 questions（assemble.py 用）

坐标约定（与 compose.py 一致）：actor.x 是人物**中心**横坐标（按 1920 宽）；flip 只做水平镜像，不改变位置。

错误（必须改）：
  E-quiz-count    全集答题镜头超过 2 个
  E-quiz-multi    一个答题镜头里出了不止一道题
  E-teacher-mid   老师（role=teacher）站在画面中间带 x∈[700,1220]
  E-teacher-pos   老师 x 不在 300–570 或 1350–1620（没写 x 时 compose 默认 960，同样报错）
  E-card-side     卡片和老师在同一侧（卡片中心在 860–1060 的居中卡片不算）
  E-talk-idle     角色有 talk 却没有 idle（不说话时会定格张嘴帧）
  E-idle-talk     角色有 idle 却没有 talk（compose 只在有 talk 时才用 idle，idle 等于没写，全程播说话帧）
  E-trans-pair    前一镜 out.type 和后一镜 in.type 不一致（分镜头 concat 后转场对不上）
  E-quiz-mismatch MP4 答题镜头和互动版 questions 的数量、顺序或题目不一致（assemble.py / --interactive）
  E-asset         引用的素材文件 / 场景 SVG 不存在
  E-no-talk       镜头有配音，角色却既没 talk 也没 idle → 全程播说话帧（动作循环素材写 "action": true 跳过）
警告（建议改）：
  W-audio-at       audio_at 不在 0.15–0.35（规范 0.25；没写时 compose 用 0.3）
  W-adjacent       相邻镜头用了同一个 camera.preset，或相邻两次转场类型相同
  W-teacher-ratio  老师出镜镜头占非答题镜头比例不在 40%–60%（短片按整数取整：n 镜允许 floor(0.4n)–ceil(0.6n) 个）
  W-teacher-run    连续 3 个及以上镜头都有老师
  W-variety        运镜 preset 少于 min(8, 镜头数) 种，或转场少于 min(6, 镜头数+1) 种（短片自动按镜头数放宽）
"""
import os, sys, json, glob, math, re, difflib

D = os.path.dirname(os.path.abspath(__file__))
MID = (700, 1220)
TEACHER_X = ((300, 570), (1350, 1620))   # 老师只站左右两侧（人物中心）
CENTER_CARD = (860, 1060)                # 卡片中心落在这里算居中卡片，不分边
AUDIO_AT = (0.15, 0.35)
EPISODE_MIN = 4                          # 不少于 4 个镜头才做整集统计（compose/render_shots/assemble 同一口径）
SMALL_CARDS = ('mark', 'pain', 'arrow')   # 圈注/痛点/箭头是指示物，不算“卡片”


def _p(s, rel):
    return rel if os.path.isabs(rel) else os.path.join(s.get('_base', '.'), rel)


def _label(i, s):
    return s.get('_src') or f'第 {i + 1} 个镜头'


def _teachers(s):
    return [a for a in s.get('actors', []) or [] if a.get('role') == 'teacher']


def _cards(s):
    return [c for c in s.get('cards', []) or [] if c.get('style', 'list') not in SMALL_CARDS]


def _card_cx(c):
    """卡片水平中心（估算，坐标按 1920）"""
    st = c.get('style', 'list'); x = c.get('x', 100)
    if st == 'tiles':
        n = len(c.get('items', [])); cols = c.get('cols', n) or 1; cell = c.get('cell', 190)
        return x + (min(n, cols) * (cell + 26)) / 2
    if st == 'ban':
        n = len(c.get('items', [])); R = c.get('r', 95); g = c.get('spacing', R * 2 + 70)
        return x + (n - 1) * g / 2
    if st == 'tag':
        longest = max([len(i.split(':', 1)[-1]) for i in c.get('items', [''])] + [1])
        return x + (longest * c.get('size', 34) + 140) / 2
    if st == 'img':
        return x + c.get('w', 400) / 2
    return x + c.get('w', 760) / 2


def _side(x):
    return 'L' if x < CENTER_CARD[0] else 'R' if x > CENTER_CARD[1] else 'C'


def _has_audio(s):
    return bool(s.get('audio') or any(isinstance(x, dict) and x.get('file') for x in s.get('audios', []) or []))


def _tr(t):
    return t.get('type') if isinstance(t, dict) else None


def _trans_seq(shots):
    """转场序列：第 1 镜的 in、每个镜头交界处（后一镜 in，没写就用前一镜 out）、最后一镜的 out"""
    seq = [_tr(shots[0].get('in'))] if shots else []
    for i in range(1, len(shots)):
        seq.append(_tr(shots[i].get('in')) or _tr(shots[i - 1].get('out')))
    if shots: seq.append(_tr(shots[-1].get('out')))
    return seq


def _quiz_count_q(q):
    """一个 quiz 里有几道题"""
    if isinstance(q, list): return len(q)
    if isinstance(q, dict):
        if isinstance(q.get('questions'), list): return len(q['questions'])
        if isinstance(q.get('q'), list): return len(q['q'])
        txt = str(q.get('q', ''))
        return max(1, sum(txt.count(ch) for ch in '？?')) if txt else 1
    return 1


def _assets(s):
    """(描述, 相对路径) 列表：本镜头引用的所有文件"""
    out = []
    for j, a in enumerate(s.get('actors', []) or []):
        for key in ('src', 'idle'):
            if a.get(key): out.append((f'actors[{j}].{key}', a[key]))
        for pi, p in enumerate(a.get('poses') or []):
            for key in ('src', 'idle'):
                if p.get(key): out.append((f'actors[{j}].poses[{pi}].{key}', p[key]))
    if s.get('audio'): out.append(('audio', s['audio']))
    for j, x in enumerate(s.get('audios', []) or []):
        if x.get('file'): out.append((f'audios[{j}].file', x['file']))
    for j, c in enumerate(s.get('cards', []) or []):
        st = c.get('style', 'list')
        if st == 'img' and c.get('src'): out.append((f'cards[{j}].src', c['src']))
        if st in ('tiles', 'ban'):
            for it in c.get('items', []):
                pic = it.split('|', 1)[0] if '|' in it else None
                if pic and ('/' in pic or pic.endswith('.png')): out.append((f'cards[{j}].items', pic))
    q = s.get('quiz')
    if isinstance(q, dict):
        for j, im in enumerate(q.get('option_imgs', []) or []):
            if im and ('/' in im or im.endswith('.png')): out.append((f'quiz.option_imgs[{j}]', im))
    return out


def _scene_ok(sid):
    return any(os.path.exists(p) for p in (f'{D}/out/svg/{sid}.svg', f'{D}/../examples/svg/{sid}.svg'))


def check(shots, episode=True):
    """shots: 镜头 dict 列表（按播放顺序）。返回 (errors, warnings)，都是字符串列表"""
    E, W = [], []
    quiz_idx = [i for i, s in enumerate(shots) if s.get('quiz')]
    if len(quiz_idx) > 2:
        E.append(f'E-quiz-count 答题镜头有 {len(quiz_idx)} 个（{", ".join(_label(i, shots[i]) for i in quiz_idx)}），一集最多 2 个')
    for i, s in enumerate(shots):
        L = _label(i, s)
        if s.get('quiz') and _quiz_count_q(s['quiz']) > 1:
            E.append(f'E-quiz-multi {L}：一个答题镜头只能出 1 道题（现在像是 {_quiz_count_q(s["quiz"])} 道）')
        cards = _cards(s)
        for a in _teachers(s):
            x = a.get('x')
            if x is None:
                E.append(f'E-teacher-pos {L}：老师没写 x（compose 默认 960 = 画面正中）；写 300–570（左）或 1350–1620（右）'); continue
            if MID[0] <= x <= MID[1]:
                E.append(f'E-teacher-mid {L}：老师 x={x} 站在中间带 {MID[0]}–{MID[1]}；改到 300–570（左）或 1350–1620（右）')
            elif not any(lo <= x <= hi for lo, hi in TEACHER_X):
                E.append(f'E-teacher-pos {L}：老师 x={x} 不在 300–570（左）或 1350–1620（右）（x 是人物中心）')
            tside = 'L' if x < 960 else 'R'
            for c in cards:
                cx = _card_cx(c)
                if _side(cx) == tside:
                    E.append(f'E-card-side {L}：{c.get("style", "list")} 卡片（中心≈{int(cx)}）和老师（x={x}）在同一侧，放到另一侧或居中（中心 {CENTER_CARD[0]}–{CENTER_CARD[1]}）')
        for j, a in enumerate(s.get('actors', []) or []):
            who = f'actors[{j}]（{a.get("src")}）'
            if a.get('talk') is not None and not a.get('idle'):
                E.append(f'E-talk-idle {L}：{who} 有 talk 但没有 idle，不说话时会定格在张嘴帧')
            if a.get('idle') and a.get('talk') is None:
                E.append(f'E-idle-talk {L}：{who} 有 idle 但没有 talk，compose 不会用 idle，全程播说话帧；不说话写 "talk": []')
            for pi, p in enumerate(a.get('poses') or []):
                if a.get('talk') is not None and not p.get('idle'):
                    E.append(f'E-talk-idle {L}：actors[{j}].poses[{pi}] 有 talk 但姿势没有 idle')
            if _has_audio(s) and a.get('talk') is None and not a.get('idle') and not a.get('action') and not a.get('still'):
                E.append(f'E-no-talk {L}：{who} 没有 talk/idle，本镜有配音时会全程播说话帧；不说话写 "talk": [] + idle，动作循环素材写 "action": true')
        if s.get('audio'):
            at = s.get('audio_at', .3)
            if not AUDIO_AT[0] <= at <= AUDIO_AT[1]:
                W.append(f'W-audio-at {L}：audio_at={at}，规范 0.25（{AUDIO_AT[0]}–{AUDIO_AT[1]}），开头空太久会像卡顿')
        for what, rel in _assets(s):
            if not os.path.exists(_p(s, rel)):
                E.append(f'E-asset {L}：{what} 引用的文件不存在：{_p(s, rel)}')
        if s.get('scene') and not _scene_ok(s['scene']):
            E.append(f'E-asset {L}：场景 {s["scene"]} 的 SVG 不存在（engine/out/svg 或 examples/svg）')
    # 相邻镜头：转场成对、运镜/转场不重复（单文件多镜头时也查）
    for i in range(1, len(shots)):
        o, n = _tr(shots[i - 1].get('out')), _tr(shots[i].get('in'))
        if o and n and o != n:
            E.append(f'E-trans-pair {_label(i - 1, shots[i - 1])} out.type={o} 和 {_label(i, shots[i])} in.type={n} 不一致，concat 后转场对不上；改成同一类型')
        p0, p1 = (shots[i - 1].get('camera') or {}).get('preset'), (shots[i].get('camera') or {}).get('preset')
        if p0 and p0 == p1:
            W.append(f'W-adjacent {_label(i - 1, shots[i - 1])} 和 {_label(i, shots[i])} 用了同一个运镜 {p0}')
    seq = _trans_seq(shots)
    for k in range(1, len(seq)):
        if seq[k] and seq[k] == seq[k - 1]:
            j = min(k, len(shots) - 1)
            W.append(f'W-adjacent {_label(j, shots[j])} 前后两次转场都是 {seq[k]}，换一种')
    if episode and shots:
        nq = [i for i, s in enumerate(shots) if not s.get('quiz')]
        if nq:
            withT = [i for i in nq if _teachers(shots[i])]
            n = len(nq); lo, hi = math.floor(.4 * n + 1e-9), math.ceil(.6 * n - 1e-9)
            if not lo <= len(withT) <= hi:
                W.append(f'W-teacher-ratio 老师出镜 {len(withT)}/{n} 个非答题镜头（{len(withT) / n:.0%}），建议 40%–60%（{n} 镜即 {lo}–{hi} 个）')
        run = 0
        for i, s in enumerate(shots + [{}]):
            if _teachers(s): run += 1; continue
            if run >= 3: W.append(f'W-teacher-run 第 {i - run + 1}–{i} 个镜头连续 {run} 个都有老师，建议穿插纯场景/学生镜头')
            run = 0
        presets = {(s.get('camera') or {}).get('preset') for s in shots} - {None}
        trans = set(seq) - {None}
        need_p, need_t = min(8, len(shots)), min(6, len(shots) + 1)
        if len(presets) < need_p or len(trans) < need_t:
            W.append(f'W-variety 运镜 preset {len(presets)} 种（{len(shots)} 镜要求 ≥{need_p}）、转场 {len(trans)} 种（要求 ≥{need_t}）')
    return E, W


_KIND = {'单选': 'single', '多选': 'multi', '判断': 'judge', 'single': 'single', 'multi': 'multi', 'judge': 'judge'}


def _norm_q(t):
    t = re.sub(r'^\s*(再)?考考你[：:，,]?', '', str(t or ''))
    return re.sub(r'[\s，。、；：:,.;!！?？“”"\'‘’（）()…—\-]', '', t)


def _same_q(a, b):
    a, b = _norm_q(a), _norm_q(b)
    if not a or not b: return True
    return a in b or b in a or difflib.SequenceMatcher(None, a, b).ratio() >= .8


def quiz_match(shots, questions, spans=None, video='noquiz', tol=1.0):
    """MP4 答题镜头 vs 互动版 questions：数量、顺序（按时间）、题目文字、答案、题型；
    spans 可选 = 每个镜头的 (开始, 结束) 秒（按 MP4 实际时长累加），给了就再查位置：
      video='noquiz'（互动版用去掉答题镜头的无题版）：第 k 题应在第 k 个答题镜头前一个镜头的结尾附近；
      video='full'（互动版直接用完整 MP4）：第 k 题应落在第 k 个答题镜头的时间范围内。返回错误列表"""
    E = []
    qi = [i for i, s in enumerate(shots) if s.get('quiz')]
    qs = sorted(questions or [], key=lambda q: q.get('t', 0))
    if len(qi) != len(qs):
        E.append(f'E-quiz-mismatch MP4 版有 {len(qi)} 道答题镜头，互动版有 {len(qs)} 道题；两版题目数量、位置要一致')
        return E
    nq_start, acc = {}, 0.0
    if spans:
        for i, (a, b) in enumerate(spans):
            if not shots[i].get('quiz'): nq_start[i] = acc; acc += b - a
    for k, (i, q) in enumerate(zip(qi, qs)):
        mq = shots[i]['quiz']; L = _label(i, shots[i])
        if not _same_q(mq.get('q'), q.get('q')):
            E.append(f'E-quiz-mismatch 第 {k + 1} 题顺序或题目不同：MP4「{mq.get("q")}」 vs 互动版「{q.get("q")}」')
            continue
        if mq.get('answer') is not None and q.get('answer') is not None and sorted(mq['answer']) != sorted(q['answer']):
            E.append(f'E-quiz-mismatch 第 {k + 1} 题答案不同：MP4 {mq["answer"]} vs 互动版 {q["answer"]}（{L}）')
        mk, ik = _KIND.get(mq.get('kind')), _KIND.get(q.get('type', 'single'))
        if mk and ik and mk != ik:
            E.append(f'E-quiz-mismatch 第 {k + 1} 题题型不同：MP4 {mq.get("kind")} vs 互动版 {q.get("type")}（{L}）')
        if spans:
            t = q.get('t', 0)
            if video == 'full':
                a, b = spans[i]; ok = a - tol <= t <= b + tol; want = f'{a:.1f}–{b:.1f}s'
            else:
                prev = [j for j in range(i) if not shots[j].get('quiz')]
                if not prev: continue
                j = prev[-1]; end = nq_start[j] + spans[j][1] - spans[j][0]
                ok = end - 1.5 - tol <= t <= end + tol; want = f'无题版 {end:.1f}s 附近（{_label(j, shots[j])} 结尾）'
            if not ok: E.append(f'E-quiz-mismatch 第 {k + 1} 题位置 t={t} 和 MP4 版不一致，应在 {want}')
    return E


def report(errors, warnings, out=sys.stderr):
    for e in errors: print('✘', e, file=out)
    for w in warnings: print('⚠', w, file=out)
    if not errors and not warnings: print('✔ lint 通过', file=out)
    elif not errors: print(f'✔ lint 无错误（{len(warnings)} 条警告）', file=out)
    else: print(f'✘ lint：{len(errors)} 个错误，{len(warnings)} 条警告', file=out)


def load(paths):
    """文件/目录 → 摊平的镜头列表（带 _base/_src）"""
    files = []
    for p in paths:
        if os.path.isdir(p):
            fs = sorted(glob.glob(os.path.join(p, 'shot*.json'))) or sorted(glob.glob(os.path.join(p, '*.json')))
            files += fs
        else: files.append(p)
    shots = []
    for f in files:
        try: cfg = json.load(open(f))
        except Exception as ex: print(f'跳过 {f}：{ex}', file=sys.stderr); continue
        if not isinstance(cfg, dict) or 'shots' not in cfg or not all(isinstance(x, dict) for x in cfg['shots']): continue
        base = os.path.dirname(os.path.abspath(f)); n = len(cfg['shots'])
        for i, s in enumerate(cfg['shots']):
            shots.append(dict(s, _base=base, _src=os.path.basename(f) + (f'#{i + 1}' if n > 1 else '')))
    return shots


def main():
    args = sys.argv[1:]; inter = None
    if '--interactive' in args:
        k = args.index('--interactive'); inter = args[k + 1] if k + 1 < len(args) else None; del args[k:k + 2]
        if not inter: print('--interactive 后面要跟 互动.json', file=sys.stderr); sys.exit(2)
    if not args: print(__doc__); sys.exit(2)
    shots = load(args)
    if not shots: print('没有找到镜头 json', file=sys.stderr); sys.exit(2)
    E, W = check(shots, episode=len(shots) >= EPISODE_MIN)
    if inter: E += quiz_match(shots, json.load(open(inter)).get('questions', []))
    print(f'检查 {len(shots)} 个镜头', file=sys.stderr)
    report(E, W)
    sys.exit(1 if E else 0)


if __name__ == '__main__':
    main()
