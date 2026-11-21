"""环境自检：python3 doctor.py
逐项检查 Python 包、无头 Chromium、ffmpeg/ffprobe、自带字体、临时目录可写，打印 ✔ / ✘ 和修复命令。全部通过时退回码 0。
"""
import os, sys, shutil, importlib, tempfile, subprocess

D = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(D)
PIP = f'pip install -r {os.path.join(ROOT, "requirements.txt")}'
ok_all = True


def row(ok, name, detail='', fix=''):
    global ok_all
    ok_all &= bool(ok)
    print(f'{"✔" if ok else "✘"} {name}' + (f'  {detail}' if detail else '') + ('' if ok or not fix else f'\n    修复：{fix}'))


def main():
    print(f'Python {sys.version.split()[0]}  ({sys.executable})')
    for mod, pipname in (('playwright', 'playwright'), ('PIL', 'pillow'), ('numpy', 'numpy'), ('fontTools', 'fonttools'), ('brotli', 'brotli'), ('edge_tts', 'edge-tts')):
        try:
            m = importlib.import_module(mod); v = getattr(m, '__version__', '')
            if not v:
                try:
                    from importlib.metadata import version; v = version(pipname)
                except Exception: v = ''
            row(True, f'python 包 {pipname}', v)
        except Exception as e:
            row(False, f'python 包 {pipname}', str(e).split('\n')[0], f'pip install {pipname}    （或一次装齐：{PIP}）')
    # Chromium
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch(); pg = b.new_page(); pg.set_content('<b>ok</b>'); ver = b.version; b.close()
        row(True, '无头 Chromium 可启动', ver)
    except ImportError:
        row(False, '无头 Chromium', '需要先装 playwright', 'pip install playwright && python3 -m playwright install chromium')
    except Exception as e:
        import re
        m = re.search(r'error while loading shared libraries: (\S+)', str(e))
        msg = f'缺系统库 {m.group(1)}' if m else str(e).strip().split('\n')[0][:160]
        fix = 'python3 -m playwright install chromium'
        if 'shared libraries' in str(e) or 'dependencies' in str(e).lower(): fix += '   （缺系统库时再运行：sudo python3 -m playwright install-deps chromium）'
        row(False, '无头 Chromium 可启动', msg, fix)
    # ffmpeg / ffprobe
    for exe in ('ffmpeg', 'ffprobe'):
        p = shutil.which(exe)
        if p:
            try: v = subprocess.check_output([exe, '-version'], stderr=subprocess.STDOUT, timeout=20).decode().split('\n')[0]
            except Exception as e: v = f'无法运行：{e}'; p = None
        row(bool(p), exe, v if p else '找不到', 'Linux: sudo apt install ffmpeg   macOS: brew install ffmpeg   Windows: winget install ffmpeg')
    # 字体
    fonts = os.path.join(D, 'fonts'); fp = os.path.join(fonts, 'NotoSansSC-800.woff')
    if os.path.exists(fp):
        try:
            from PIL import ImageFont
            f = ImageFont.truetype(fp, 40); w = f.getlength('考考你'); row(w > 0, '自带字体 NotoSansSC-800.woff', f'{os.path.getsize(fp) // 1024} KB，中文可渲染')
        except Exception as e:
            row(False, '自带字体 NotoSansSC-800.woff', f'PIL 读不了：{e}', 'pip install --force-reinstall pillow brotli    （woff 需要 brotli/zlib 支持）')
    else:
        row(False, '自带字体 NotoSansSC-800.woff', f'缺少 {fp}', '从技能包重新解压 engine/fonts/')
    # 临时目录
    try:
        d = tempfile.mkdtemp(prefix='mg_doctor_'); open(os.path.join(d, 'x'), 'w').write('x'); shutil.rmtree(d)
        row(True, '临时目录可写', tempfile.gettempdir())
    except Exception as e:
        row(False, '临时目录可写', str(e), '设置环境变量 TMPDIR 指向一个可写目录，如 export TMPDIR=$HOME/tmp')
    # 场景
    svg = [p for p in (os.path.join(D, 'out', 'svg'), os.path.join(ROOT, 'examples', 'svg')) if os.path.isdir(p) and os.listdir(p)]
    row(bool(svg), '场景 SVG', ', '.join(f'{p}（{len(os.listdir(p))} 个）' for p in svg) or '找不到', f'cd {D} && python3 render.py')
    print('\n全部通过，可以出片。' if ok_all else '\n有 ✘ 项，按上面的修复命令处理后再运行 python3 doctor.py。')
    sys.exit(0 if ok_all else 1)


if __name__ == '__main__':
    main()
