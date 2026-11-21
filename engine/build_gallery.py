"""生成单文件场景图库：out/MG场景图库.html（内嵌全部 SVG、运行时与字体子集）"""
import os, json, base64, subprocess, glob, tempfile
TMP = tempfile.mkdtemp(prefix='mg_gal_')
D = os.path.dirname(os.path.abspath(__file__)); O = f'{D}/out'
meta = json.load(open(f'{O}/scenes.json'))
svgs = {k: open(f'{O}/svg/{k}.svg').read() for k in meta}
js = open(f'{D}/mgscene.js').read()
CATS = ['校园', '体育', '语文与历史', '数学', '科学', '艺术与劳动', '安全与法治', '家庭生活', '社会日常', '自然与地理', '季节专题', '讲解台']
ui = open(f'{D}/guide.html').read() + open(f'{D}/gallery_template.html').read() + '场景图库搜索全部重播配色原色冷调暖调黄昏夜晚柔和安全区下载复制使用说明适用角色站位字幕层入场循环共个张返回点击查看大图暂无结果'
chars = ''.join(sorted(set(ui + json.dumps(meta, ensure_ascii=False) + ''.join(svgs.values()) + ''.join(CATS) + '0123456789')))
open(f'{TMP}/gchars.txt', 'w').write(chars)
F = os.path.join(os.path.dirname(os.path.abspath(__file__)),'fonts','NotoSansSC-800.woff')
subprocess.run(['pyftsubset', F, f'--text-file={TMP}/gchars.txt', f'--output-file={TMP}/g.woff2', '--flavor=woff2'], check=True)
font = base64.b64encode(open(f'{TMP}/g.woff2', 'rb').read()).decode()
from PIL import Image
import io
thumbs = {}
for k in meta:
    im = Image.open(f'{O}/png/{k}.png').convert('RGB').resize((640, 360), Image.LANCZOS); bio = io.BytesIO(); im.save(bio, 'JPEG', quality=82)
    thumbs[k] = 'data:image/jpeg;base64,' + base64.b64encode(bio.getvalue()).decode()
guide = open(f'{D}/guide.html').read()
tpl = open(f'{D}/gallery_template.html').read().replace('/*GUIDE*/', guide).replace('/*THUMBS*/', json.dumps(thumbs))
html = (tpl.replace('/*FONT*/', font).replace('/*JS*/', js).replace('/*META*/', json.dumps(meta, ensure_ascii=False))
        .replace('/*SVGS*/', json.dumps(svgs, ensure_ascii=False)).replace('/*CATS*/', json.dumps(CATS, ensure_ascii=False)))
open(f'{O}/MG场景图库.html', 'w').write(html)
print(len(html) // 1024, 'KB', len(meta), 'scenes')
