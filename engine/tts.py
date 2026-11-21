"""台词 → 分角色配音 + 说话时段（口型用）

用法：python3 tts.py lines.txt out_dir [--voices teacher=zh-CN-XiaoxiaoNeural,student=zh-CN-YunxiaNeural,...]
                                       [--rate +0%] [--force] [--vad-only]
lines.txt 每行 `id|speaker|text`（空行和 # 开头的行跳过），例如：
    l1|teacher|同学们好，今天我们学习火灾逃生。
    l2|student|老师，烟很大怎么办？
产出：
    out_dir/<id>.mp3                  edge-tts 配音（文本和声音没变时复用，不重复请求；--force 全部重做）
    out_dir/lines.json                {id: {file, speaker, text, voice, dur, talk: [[t0, t1], ...]}}
                                      talk 是该文件内的说话时段（秒，相对音频开头）；放进镜头时加上 audio_at：
                                      actor.talk = [[audio_at + t0, audio_at + t1], ...]（build_shots.py 示例就是这么做的）
说话时段：ffmpeg 解码成 16 kHz 单声道 PCM → numpy 能量 VAD（20 ms 帧，阈值 = 峰值 8%，
          间隔 <0.18 s 合并，<0.08 s 丢弃，两端各留 0.03 s）。不依赖 pydub。
--vad-only：不联网，只对 out_dir 里已有的 <id>.mp3 重算 lines.json。
默认声音：teacher/T 女教师 zh-CN-XiaoxiaoNeural，teacher_m 男教师 zh-CN-YunxiNeural，
          student/boy/S 男学生 zh-CN-YunxiaNeural，girl/G 女学生 zh-CN-XiaoyiNeural。
"""
import os, sys, json, argparse, asyncio, hashlib, subprocess
import numpy as np

VOICES = {'teacher': 'zh-CN-XiaoxiaoNeural', 'T': 'zh-CN-XiaoxiaoNeural', 'teacher_m': 'zh-CN-YunxiNeural',
          'student': 'zh-CN-YunxiaNeural', 'boy': 'zh-CN-YunxiaNeural', 'S': 'zh-CN-YunxiaNeural',
          'girl': 'zh-CN-XiaoyiNeural', 'G': 'zh-CN-XiaoyiNeural'}
SR = 16000


def parse_lines(path):
    out = []
    for n, raw in enumerate(open(path, encoding='utf-8'), 1):
        line = raw.strip()
        if not line or line.startswith('#'): continue
        parts = line.split('|', 2)
        if len(parts) != 3 or not all(p.strip() for p in parts):
            sys.exit(f'tts.py：{path} 第 {n} 行格式应为 id|speaker|text：{line}')
        out.append(tuple(p.strip() for p in parts))
    ids = [i for i, _, _ in out]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup: sys.exit(f'tts.py：id 重复：{", ".join(sorted(dup))}')
    return out


def decode(path):
    """任意音频 → float32 单声道 16 kHz"""
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 's16le', '-ac', '1', '-ar', str(SR), '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32)


def vad(x, hop=.02, rel=.08, gap=.18, min_len=.08, pad=.03):
    """能量 VAD → [[t0, t1], ...]（秒）"""
    n = int(SR * hop)
    if len(x) < n: return []
    m = len(x) // n
    r = np.sqrt((x[:m * n].reshape(m, n) ** 2).mean(1) + 1e-9)
    on = r > max(r.max() * rel, 60.0)          # 60 ≈ -55 dBFS 的底噪下限，全静音文件不会误报
    seg, i = [], 0
    while i < m:
        if on[i]:
            j = i
            while j < m and on[j]: j += 1
            seg.append([i * hop, j * hop]); i = j
        else: i += 1
    merged = []
    for a, b in seg:
        if merged and a - merged[-1][1] < gap: merged[-1][1] = b
        else: merged.append([a, b])
    T = len(x) / SR
    return [[round(max(0, a - pad), 2), round(min(T, b + pad), 2)] for a, b in merged if b - a >= min_len]


async def synth(jobs, rate):
    try:
        import edge_tts
    except ImportError:
        sys.exit('tts.py：没有安装 edge-tts，先 pip install -r requirements.txt')
    try:
        import aiohttp.helpers as h
        h.proxies_from_env = lambda: {}        # 沙箱里的代理环境变量会让 edge-tts 连不上
    except Exception: pass
    for lid, voice, text, path in jobs:
        tmp = path + '.part'
        try:
            await edge_tts.Communicate(text, voice, rate=rate).save(tmp)
        except Exception as ex:
            if os.path.exists(tmp): os.remove(tmp)
            sys.exit(f'tts.py：edge-tts 生成 {lid} 失败（{type(ex).__name__}: {ex}）。\n'
                     '  edge-tts 需要联网访问微软语音服务（speech.platform.bing.com）。请检查网络/代理后重试；\n'
                     '  已经有 mp3 时可用 --vad-only 只重算说话时段。')
        if not os.path.exists(tmp) or os.path.getsize(tmp) < 500:
            sys.exit(f'tts.py：edge-tts 没有返回 {lid} 的音频（声音名 {voice} 是否正确？网络是否可用？）')
        os.replace(tmp, path)
        print('tts', lid, voice, f'{os.path.getsize(path) // 1024} KB')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('lines'); ap.add_argument('out_dir')
    ap.add_argument('--voices', default='', help='speaker=声音名,逗号分隔，覆盖默认')
    ap.add_argument('--rate', default='+0%'); ap.add_argument('--force', action='store_true'); ap.add_argument('--vad-only', action='store_true')
    a = ap.parse_args()
    voices = dict(VOICES)
    for kv in filter(None, a.voices.split(',')):
        if '=' not in kv: sys.exit(f'tts.py：--voices 写法是 speaker=声音名：{kv}')
        k, v = kv.split('=', 1); voices[k.strip()] = v.strip()
    lines = parse_lines(a.lines)
    os.makedirs(a.out_dir, exist_ok=True)
    jp = os.path.join(a.out_dir, 'lines.json')
    old = json.load(open(jp)) if os.path.exists(jp) else {}
    jobs, info = [], {}
    for lid, spk, text in lines:
        if spk not in voices: sys.exit(f'tts.py：{lid} 的说话人 "{spk}" 没有对应声音；用 --voices {spk}=zh-CN-…Neural 指定（已有：{", ".join(sorted(voices))}）')
        voice = voices[spk]; f = f'{lid}.mp3'; p = os.path.join(a.out_dir, f)
        key = hashlib.md5(f'{voice}|{a.rate}|{text}'.encode()).hexdigest()[:12]
        fresh = os.path.exists(p) and old.get(lid, {}).get('key') == key
        if a.vad_only:
            if not os.path.exists(p): sys.exit(f'tts.py：--vad-only 但 {p} 不存在')
        elif a.force or not fresh: jobs.append((lid, voice, text, p))
        info[lid] = dict(file=f, speaker=spk, text=text, voice=voice, key=key)
    if jobs: asyncio.run(synth(jobs, a.rate))
    for lid, d in info.items():
        x = decode(os.path.join(a.out_dir, d['file']))
        d['dur'] = round(len(x) / SR, 3); d['talk'] = vad(x)
        if not d['talk']: print(f'⚠ {lid} 没检测到人声', file=sys.stderr)
    json.dump(info, open(jp, 'w'), ensure_ascii=False, indent=1)
    print(f'done {jp}：{len(info)} 句，新生成 {len(jobs)} 句，总时长 {sum(d["dur"] for d in info.values()):.1f}s')


if __name__ == '__main__':
    main()
