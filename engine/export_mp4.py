"""把场景的入场 + 循环动画导出成 MP4。
用法：python3 export_mp4.py s001 4 out.mp4 [--theme dusk] [--fps 30]
"""
import os, sys, subprocess, argparse, tempfile
D = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser(); ap.add_argument('sid'); ap.add_argument('dur', type=float); ap.add_argument('out')
ap.add_argument('--theme', default='original'); ap.add_argument('--fps', type=int, default=30)
a = ap.parse_args()
svgp = next(p for p in (f'{D}/svg/{a.sid}.svg', f'{D}/out/svg/{a.sid}.svg', f'{D}/../examples/svg/{a.sid}.svg') if os.path.exists(p))
html = f'<style>body{{margin:0;overflow:hidden}}</style>{open(svgp).read()}<script>{open(D + "/mgscene.js").read()}</script>'
TMP = os.path.join(tempfile.mkdtemp(prefix='mg_exp_'), 'scene.html'); open(TMP, 'w').write(html)
from playwright.sync_api import sync_playwright
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(a.fps), '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
                       '-r', str(a.fps), '-g', str(a.fps), '-crf', '18', '-movflags', '+faststart', a.out], stdin=subprocess.PIPE)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1920, 'height': 1080})
    pg.goto('file://' + TMP)
    pg.evaluate(f"(()=>{{const s=document.querySelector('svg');MGScene.theme(s,'{a.theme}');MGScene.play(s);}})()")
    for n in range(int(a.dur * a.fps)):
        pg.evaluate(f"MGScene.seek(document.querySelector('svg'),{n / a.fps})")
        ff.stdin.write(pg.screenshot(type='jpeg', quality=92))
    b.close()
ff.stdin.close(); ff.wait(); print('done', a.out)
