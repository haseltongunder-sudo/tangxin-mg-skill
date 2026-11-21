"""合成一段轻快、不抢人声的循环配乐（无版权问题）：python3 bgm.py out.wav 秒数 [bright|calm|tense]
bright 明快（默认，知识科普）  calm 舒缓（情绪、睡眠、总结）  tense 紧张（事故情境开场、警示）"""
import sys, wave, math, random
import numpy as np

SR = 44100
def note(f, d, a=.3, decay=3.5, harm=(1, .35, .12)):
    t = np.arange(int(SR * d)) / SR; env = np.exp(-t * decay) * np.minimum(1, t / .008)
    return a * env * sum(h * np.sin(2 * np.pi * f * (i + 1) * t) for i, h in enumerate(harm))
def hz(m): return 440 * 2 ** ((m - 69) / 12)

def make(sec, mood='bright'):
    bpm = {'bright': 104, 'calm': 80, 'tense': 120}[mood]; beat = 60 / bpm
    prog = {'bright': [[60, 64, 67], [55, 59, 62], [57, 60, 64], [53, 57, 60]], 'calm': [[60, 64, 67], [57, 60, 64], [53, 57, 60], [55, 59, 62]],
            'tense': [[57, 60, 64], [57, 60, 64], [53, 57, 60], [52, 56, 59]]}[mood]
    out = np.zeros(int(SR * (sec + 2))); random.seed(2); bar = 0; t0 = 0.0
    while t0 < sec:
        ch = prog[bar % 4]
        for b in range(4):
            tb = t0 + b * beat; i = int(tb * SR)
            bs = note(hz(ch[0] - 24), beat * .95, .22, 4, (1, .5)); out[i:i + len(bs)] += bs[:len(out) - i]
            for e in range(2):
                m = random.choice(ch) + 12 + (12 if random.random() < .3 else 0); te = tb + e * beat / 2; j = int(te * SR)
                pl = note(hz(m), beat * .9, .09 if mood != 'tense' else .07, 5, (1, .25, .08)); out[j:j + len(pl)] += pl[:len(out) - j]
            if mood != 'calm':
                hh = np.random.randn(int(SR * .03)) * np.exp(-np.arange(int(SR * .03)) / SR * 120) * .03; k = int((tb + beat / 2) * SR); out[k:k + len(hh)] += hh[:len(out) - k]
        pad = sum(note(hz(m), beat * 4, .03, .4, (1,)) for m in ch); k = int(t0 * SR); out[k:k + len(pad)] += pad[:len(out) - k]
        t0 += beat * 4; bar += 1
    out = out[:int(SR * sec)]; out /= max(1e-6, np.abs(out).max()) / .8
    fade = int(SR * 1.5); out[-fade:] *= np.linspace(1, 0, fade)
    return out

if __name__ == '__main__':
    p = sys.argv[1]; sec = float(sys.argv[2]) if len(sys.argv) > 2 else 60; mood = sys.argv[3] if len(sys.argv) > 3 else 'bright'
    a = (make(sec, mood) * 32767).astype(np.int16); st = np.stack([a, a], 1)
    with wave.open(p, 'w') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
    print('bgm', p, sec, mood)
