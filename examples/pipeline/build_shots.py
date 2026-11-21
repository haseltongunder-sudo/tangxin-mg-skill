"""流水线第 3 步：lines.json（tts.py 产出）+ plan.json（分镜计划）→ 每镜一个 shot json + 总装 asm.json + 互动.json，然后自动 lint

用法（在 examples/pipeline/ 下）：
  python3 ../../engine/tts.py lines.txt voice            # 1 配音 + 说话时段 → voice/*.mp3、voice/lines.json
  python3 ../../engine/rig.py ../rig/chars.json          # 2 定稿老师图 → ../rig/frames/teacher_talk|idle、teacher_lean_talk|idle
  python3 build_shots.py                                 # 3 → shots/shot01..04.json、asm.json、互动.json，并 lint（0 错 0 警告）
  python3 ../../engine/render_shots.py shots/*.json -j 2 # 4 逐镜渲染 → shots/shotNN.mp4（后台跑，约 40 s/秒）
  python3 ../../engine/assemble.py asm.json              # 5 成片 + 无题版 + 互动版（asm.json 的 interactive 字段调用 interactive.py）

计划字段（plan.json 的每个镜头）：line 台词 id、scene、teacher "L"/"R"/null（null = 画外音）、pose（老师第二姿势名，
后半句切换）、student {x, bend_at}、camera、in（转场类型；前一镜 out 自动取同类型，保证 E-trans-pair）、cards、
subs（字幕分段，按说话时段自动排时间）、chapter；答题镜头写 quiz（MP4 和互动版共用这一份题目，天然一致）。
"""
import os, sys, json, subprocess

H = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.normpath(os.path.join(H, '../../engine'))
sys.path.insert(0, ENGINE)
import lint

FPS = 30
RIG = '../../rig/frames/'          # 相对 shots/ 目录
DEMO = '../../demo/'
TEACHER_X = {'L': 450, 'R': 1480}  # 人物中心，落在 lint 的 300–570 / 1350–1620
TRANS_DUR = {'fade': .5, 'whip': .35, 'iris': .6, 'star_in': .6, 'dip': .5}


def adur(p):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]).decode())


def tr(typ):
    d = {'type': typ, 'dur': TRANS_DUR.get(typ, .45)}
    if typ == 'whip': d['dir'] = 1
    return d


def sub_times(texts, win, end_pad=.3):
    """字幕分段按说话时段排：第 k 段从第 round(k·n/N) 个时段开始，到下一段开始（最后一段到说话结束 + 0.3）"""
    n, N = len(win), len(texts); starts = [win[min(n - 1, round(k * n / N))][0] for k in range(N)]
    ends = starts[1:] + [win[-1][1] + end_pad]
    return [{'t': round(a, 2), 'd': round(b - a, 2), 'text': t} for t, a, b in zip(texts, starts, ends)]


def main():
    plan = json.load(open(os.path.join(H, 'plan.json')))
    lp = os.path.join(H, 'voice/lines.json')
    if not os.path.exists(lp): sys.exit('先跑 tts.py：python3 ../../engine/tts.py lines.txt voice')
    lines = json.load(open(lp)); AT = plan.get('audio_at', .25)
    if not os.path.isdir(os.path.join(H, '../rig/frames/teacher_talk')):
        sys.exit('先跑 rig.py：python3 ../../engine/rig.py ../rig/chars.json')
    os.makedirs(os.path.join(H, 'shots'), exist_ok=True)
    P = plan['shots']; shots, durs = [], []
    for i, p in enumerate(P):
        s = {'scene': p['scene'], 'camera': p['camera'], 'in': tr(p['in'])}
        nxt = P[i + 1]['in'] if i + 1 < len(P) else p.get('out', 'fade')
        s['out'] = tr(nxt)                                   # 本镜 out = 下一镜 in，同类型
        if p.get('quiz'):
            q = {k: v for k, v in p['quiz'].items() if k != 'explain'}
            q.update(t=.2, cd_at=1.6, countdown=5)
            s.update(static=True, bg_blur=4, dur=9.5, quiz=q,
                     subs=[{'t': 7.0, 'd': 2.3, 'text': p['quiz']['explain'][:22]}])
            shots.append(s); durs.append(int(9.5 * FPS) / FPS); continue
        L = lines[p['line']]; win = [[round(AT + a, 2), round(AT + b, 2)] for a, b in L['talk']]
        audio = f'../voice/{L["file"]}'
        s.update(dur=3, audio=audio, audio_at=AT, replay_enter=True, actors=[], subs=sub_times(p['subs'], win))
        if p.get('teacher'):
            side = p['teacher']
            a = {'src': RIG + 'teacher_talk', 'idle': RIG + 'teacher_idle', 'talk': win, 'role': 'teacher', 'shot': 'knee',
                 'x': TEACHER_X[side], 'flip': side == 'L', 't_in': .2, 'enter': 'slide'}
            if p.get('pose'):
                mid = win[len(win) // 2][0] if len(win) > 1 else win[0][0] + .8
                a['poses'] = [{'src': RIG + f'teacher_{p["pose"]}_talk', 'idle': RIG + f'teacher_{p["pose"]}_idle', 't': [mid, 99]}]
            s['actors'].append(a)
        if p.get('student'):
            st = p['student']
            s['actors'].append({'src': DEMO + 'student_idle', 'idle': DEMO + 'student_idle', 'talk': [], 'role': 'student', 'shot': 'full',
                                'x': st['x'], 't_in': .3, 'enter': 'pop',
                                'poses': [{'src': DEMO + 'student_bend', 'idle': DEMO + 'student_bend', 't': [st['bend_at'], 99], 'height': 430}]})
        speech = win[-1][1] - win[0][0]; cards = []
        for c in p.get('cards', []):
            c = dict(c, t=round(win[0][0] + .3, 2))
            if c.get('style') == 'board': c['times'] = [w[0] for w in win][:len(c['items'])]
            elif len(c.get('items', [])) > 1: c['gap'] = round(speech / len(c['items']), 2)
            cards.append(c)
        s['cards'] = cards
        shots.append(s); durs.append(int(max(3, adur(os.path.join(H, 'shots', audio)) + AT + .4) * FPS) / FPS)   # compose 的时长规则
    for i, s in enumerate(shots):
        json.dump({'fps': FPS, 'out': f'shot{i + 1:02d}.mp4', 'dissolve': 0, 'accent': plan.get('accent'), 'shots': [s]},
                  open(os.path.join(H, f'shots/shot{i + 1:02d}.json'), 'w'), ensure_ascii=False, indent=1)
    # 时间轴：完整版 / 无题版（互动版用无题版，题目放在答题镜头前一个讲解镜头结尾前 0.35 s）
    st_full = [sum(durs[:i]) for i in range(len(durs) + 1)]
    nq, acc = {}, 0.0
    for i, s in enumerate(shots):
        if not s.get('quiz'): nq[i] = (acc, acc + durs[i]); acc += durs[i]
    questions, chapters = [], []
    for i, (p, s) in enumerate(zip(P, shots)):
        if p.get('chapter') and not s.get('quiz'): chapters.append({'t': round(nq[i][0], 2), 'title': p['chapter']})
        if s.get('quiz'):
            prev = max(j for j in nq if j < i); q = p['quiz']
            questions.append({'t': round(nq[prev][1] - .35, 2), 'type': {'单选': 'single', '多选': 'multi', '判断': 'judge'}[q.get('kind', '单选')],
                              'q': q['q'], 'options': q['options'], 'answer': q['answer'], 'explain': q.get('explain', ''),
                              'review': round(nq[prev][0], 2)})
    json.dump({'title': plan['title'], 'lock_seek': True, 'accent': plan.get('accent'), 'chapters': chapters, 'questions': questions},
              open(os.path.join(H, '互动.json'), 'w'), ensure_ascii=False, indent=1)
    json.dump({'shots': [f'shots/shot{i + 1:02d}.mp4' for i in range(len(shots))], 'out': 'pipeline_demo.mp4', 'title': plan['title'],
               'accent': plan.get('accent'), 'bgm': 'auto', 'bgm_mood': 'calm',
               'chapters': [{'shot': i + 1, 'title': p['chapter'], **({'quiz': True} if p.get('quiz') else {})} for i, p in enumerate(P) if p.get('chapter')],
               'interactive': '互动.json'}, open(os.path.join(H, 'asm.json'), 'w'), ensure_ascii=False, indent=1)
    print(f'写出 {len(shots)} 个镜头 json（shots/）、asm.json、互动.json；预计成片 {st_full[-1]:.1f}s')
    flat = lint.load([os.path.join(H, 'shots')])
    E, W = lint.check(flat)
    spans = list(zip(st_full[:-1], st_full[1:]))
    E += lint.quiz_match(flat, questions, spans)
    lint.report(E, W, out=sys.stdout)
    sys.exit(1 if E else 0)


if __name__ == '__main__':
    main()
