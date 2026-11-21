"""并行渲染多个镜头 json（每个 json 调一次 compose.py），可断点续跑

用法：python3 render_shots.py shot*.json [-j 2] [--timeout 900] [--force] [--res 1080] [--no-lint]
  -j N         同时渲染的进程数（默认 2；每个进程一个 Chromium，内存约 1–1.5 GB）
  --timeout S  单个镜头超时秒数（默认 900），超时就杀掉并记为失败
  --force      忽略已有 mp4，全部重渲
  --res        传给 compose.py 的分辨率（1080 / 1440 / 2160）
  --no-lint    跳过开工前的整集规则检查
续跑规则：json 的 out 指向的 mp4 已存在，且比 json 本身和它引用的所有素材（角色帧、音频、图片）都新，就跳过。
预计耗时：约 40 秒渲染 / 1 秒成片 / 每进程（1080p），开跑前会打印估算。
"""
import os, sys, json, time, argparse, subprocess, tempfile, glob
from concurrent.futures import ThreadPoolExecutor, as_completed

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
import lint

SEC_PER_SEC = 40


def audio_len(p):
    try:
        import wave
        with wave.open(p) as w: return w.getnframes() / w.getframerate()
    except Exception:
        try: return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]).decode().strip())
        except Exception: return 0


def video_len(cfg, base):
    """按 compose.py 的规则估算成片时长"""
    tot = 0
    for s in cfg.get('shots', []):
        d = s.get('dur', 4)
        if s.get('audio'): d = max(d, audio_len(os.path.join(base, s['audio'])) + s.get('audio_at', .3) + .4)
        for x in s.get('audios', []): d = max(d, audio_len(os.path.join(base, x['file'])) + x.get('at', 0) + .6)
        tot += d
    return tot


def newest_input(jp, cfg):
    base = os.path.dirname(os.path.abspath(jp)); m = os.path.getmtime(jp)
    for s in cfg.get('shots', []):
        for _, rel in lint._assets(s):
            p = rel if os.path.isabs(rel) else os.path.join(base, rel)
            if os.path.isdir(p):
                for f in glob.glob(os.path.join(p, '*')): m = max(m, os.path.getmtime(f))
            elif os.path.exists(p): m = max(m, os.path.getmtime(p))
    return m


def fmt(s):
    s = int(s); return f'{s // 3600}h{s % 3600 // 60:02d}m' if s >= 3600 else f'{s // 60}m{s % 60:02d}s'


def run_one(jp, out, timeout, res, logdir):
    log = os.path.join(logdir, os.path.basename(jp) + '.log'); t0 = time.time()
    cmd = [sys.executable, os.path.join(D, 'compose.py'), os.path.abspath(jp), '--no-lint'] + (['--res', str(res)] if res else [])
    try:
        with open(log, 'w') as lf:
            r = subprocess.run(cmd, stdout=lf, stderr=subprocess.STDOUT, timeout=timeout, cwd=os.path.dirname(os.path.abspath(jp)))
        ok = r.returncode == 0 and os.path.exists(out); why = '' if ok else f'退出码 {r.returncode}'
    except subprocess.TimeoutExpired:
        ok, why = False, f'超时（>{timeout}s）'
    tail = '' if ok else ''.join(open(log, errors='replace').readlines()[-6:])
    return jp, ok, time.time() - t0, why, tail, log


def main():
    ap = argparse.ArgumentParser(description='并行渲染镜头 json')
    ap.add_argument('shots', nargs='+'); ap.add_argument('-j', type=int, default=2); ap.add_argument('--timeout', type=int, default=900)
    ap.add_argument('--force', action='store_true'); ap.add_argument('--res', type=int, default=0); ap.add_argument('--no-lint', action='store_true')
    a = ap.parse_args()
    try: sys.stdout.reconfigure(line_buffering=True)
    except Exception: pass
    jobs, skipped = [], []
    cfgs = {}
    for jp in a.shots:
        try: cfg = json.load(open(jp))
        except Exception as e: print(f'✘ 读不了 {jp}：{e}'); sys.exit(1)
        if 'shots' not in cfg: print(f'跳过 {jp}（不是镜头 json）'); continue
        cfgs[jp] = cfg
    if not a.no_lint:
        flat = []
        for jp, cfg in cfgs.items():
            if cfg.get('lint', True) is False: continue
            base = os.path.dirname(os.path.abspath(jp)); n = len(cfg['shots'])
            flat += [dict(s, _base=base, _src=os.path.basename(jp) + (f'#{i + 1}' if n > 1 else '')) for i, s in enumerate(cfg['shots'])]
        if flat:
            E, W = lint.check(flat, episode=len(flat) >= lint.EPISODE_MIN); lint.report(E, W)
            if E: sys.exit('规则检查未通过，已停止（确需跳过：--no-lint）')
    for jp, cfg in cfgs.items():
        base = os.path.dirname(os.path.abspath(jp)); out = os.path.join(base, cfg.get('out', 'out.mp4')); vl = video_len(cfg, base)
        if not a.force and os.path.exists(out) and os.path.getmtime(out) > newest_input(jp, cfg):
            skipped.append(jp); continue
        jobs.append((jp, out, vl))
    tot_v = sum(v for _, _, v in jobs); j = max(1, min(a.j, len(jobs) or 1))
    print(f'镜头 {len(cfgs)} 个：待渲染 {len(jobs)}，已是最新跳过 {len(skipped)}' + (f'（{", ".join(os.path.basename(x) for x in skipped)}）' if skipped else ''))
    if not jobs: print('没有需要渲染的镜头（要重渲加 --force）'); return
    print(f'成片时长约 {tot_v:.1f}s；预计耗时约 {fmt(tot_v * SEC_PER_SEC / j)}（按 {SEC_PER_SEC}s 渲染/1s 成片/进程，{j} 个进程并行）')
    for jp, _, vl in jobs: print(f'  · {os.path.basename(jp)}  {vl:.1f}s  ≈{fmt(vl * SEC_PER_SEC)}')
    logdir = tempfile.mkdtemp(prefix='mg_render_'); t0 = time.time(); res = []
    with ThreadPoolExecutor(max_workers=j) as ex:
        futs = [ex.submit(run_one, jp, out, a.timeout, a.res, logdir) for jp, out, _ in jobs]
        for f in as_completed(futs):
            jp, ok, el, why, tail, log = f.result(); res.append((jp, ok, el, why, log))
            print(f'{"✔" if ok else "✘"} {os.path.basename(jp)}  {fmt(el)}' + ('' if ok else f'  {why}\n    日志 {log}\n' + ''.join('    ' + l for l in tail.splitlines(True))), flush=True)
    bad = [r for r in res if not r[1]]
    print(f'\n汇总：成功 {len(res) - len(bad)}，失败 {len(bad)}，跳过 {len(skipped)}，用时 {fmt(time.time() - t0)}')
    for jp, _, _, why, log in bad: print(f'  ✘ {jp}：{why}（日志 {log}）')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
