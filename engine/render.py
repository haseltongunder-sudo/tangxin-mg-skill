"""生成全部场景：svg/*.svg、png/*.png（最终静帧）、scenes.json"""
import os, sys, json, importlib, tempfile
sys.path.insert(0, os.path.dirname(__file__))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
mods = [m for m in sys.argv[1:] if not m.startswith('-')] or sorted(f[:-3] for f in os.listdir(os.path.dirname(os.path.abspath(__file__))) if f.startswith('scenes_'))
os.makedirs(f'{OUT}/svg', exist_ok=True); os.makedirs(f'{OUT}/png', exist_ok=True)
FONT = os.path.join(os.path.dirname(os.path.abspath(__file__)),'fonts','NotoSansSC-800.woff')
os.makedirs(f'{OUT}/meta', exist_ok=True)
jobs = []
for m in mods:
    for fn in importlib.import_module(m).SCENES:
        sc = fn(); svg = sc.svg()
        open(f'{OUT}/svg/{sc.sid}.svg', 'w').write(svg)
        json.dump(sc.meta(), open(f'{OUT}/meta/{sc.sid}.json', 'w'), ensure_ascii=False); jobs.append(sc.sid)
import glob
allmeta = {os.path.basename(f)[:-5]: json.load(open(f)) for f in sorted(glob.glob(f'{OUT}/meta/*.json'))}
json.dump(allmeta, open(f'{OUT}/scenes.json', 'w'), ensure_ascii=False, indent=1)
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1920, 'height': 1080})
    for sid in jobs:
        svg = open(f'{OUT}/svg/{sid}.svg').read()
        TMPH = os.path.join(tempfile.gettempdir(), f'_scene_{os.getpid()}.html'); open(TMPH, 'w').write(f'<style>@font-face{{font-family:"Noto Sans SC";src:url(file://{FONT})}}body{{margin:0}}</style>{svg}')
        pg.goto('file://' + TMPH); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(200)
        pg.screenshot(path=f'{OUT}/png/{sid}.png'); print(sid)
    b.close()
