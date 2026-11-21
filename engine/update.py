#!/usr/bin/env python3
"""检查 / 安装 tangxin-mg-skill 新版本（只用 Python 标准库）。

  python engine/update.py            # 只检查：打印 本地版本、最新版本、更新说明
  python engine/update.py --apply    # 下载最新版覆盖技能文件（保留 out/ 等自己生成的内容）

更新源：https://github.com/haseltongunder-sudo/tangxin-mg-skill
"""
import io, json, os, shutil, sys, time, urllib.request, zipfile

REPO = 'haseltongunder-sudo/tangxin-mg-skill'
RAW = f'https://raw.githubusercontent.com/{REPO}/main/'
ZIP = f'https://github.com/{REPO}/archive/refs/heads/main.zip'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEEP = {'out', 'shots', 'frames', '__pycache__'}  # 用户生成内容，更新时不动


def ver(s):
    try:
        return tuple(int(x) for x in s.strip().lstrip('v').split('.'))
    except ValueError:
        return (0,)


def get(url, timeout=10):
    if url.startswith(RAW):  # 绕过 CDN 缓存，保证拿到最新版本号
        url += '?t=%d' % time.time()
    req = urllib.request.Request(url, headers={'User-Agent': 'tangxin-mg-skill-updater', 'Cache-Control': 'no-cache'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def get_file(name):
    """先走 raw.githubusercontent.com，失败再走 GitHub API。"""
    try:
        return get(RAW + name)
    except Exception:
        import base64
        j = json.loads(get(f'https://api.github.com/repos/{REPO}/contents/{name}?ref=main'))
        return base64.b64decode(j['content'])


def local_version():
    try:
        return open(os.path.join(ROOT, 'VERSION'), encoding='utf-8').read().strip()
    except OSError:
        return '0'


def check():
    loc = local_version()
    try:
        latest = get_file('VERSION').decode().strip()
    except Exception as e:  # 没网 / 被墙：不影响正常使用
        return {'local': loc, 'latest': None, 'update': False, 'error': str(e)}
    notes = ''
    if ver(latest) > ver(loc):
        try:
            log = get_file('CHANGELOG.md').decode('utf-8')
            # 只取比本地新的段落
            parts, keep = [], False
            for line in log.splitlines():
                if line.startswith('## '):
                    keep = ver(line[3:].split()[0]) > ver(loc)
                if keep:
                    parts.append(line)
            notes = '\n'.join(parts).strip()
        except Exception:
            pass
    return {'local': loc, 'latest': latest, 'update': ver(latest) > ver(loc), 'notes': notes}


def apply():
    data = get(ZIP, timeout=120)
    z = zipfile.ZipFile(io.BytesIO(data))
    top = z.namelist()[0].split('/')[0]
    n = 0
    for info in z.infolist():
        rel = info.filename[len(top) + 1:]
        if not rel or info.is_dir():
            continue
        if KEEP & set(rel.split('/')[:-1]):
            continue
        dst = os.path.join(ROOT, *rel.split('/'))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with z.open(info) as src, open(dst, 'wb') as out:
            shutil.copyfileobj(src, out)
        n += 1
    return n


if __name__ == '__main__':
    r = check()
    if '--apply' in sys.argv:
        if r.get('latest') is None:
            sys.exit('连不上 GitHub，暂时无法更新：' + r.get('error', ''))
        n = apply()
        print(f'已更新到 {local_version()}（写入 {n} 个文件）')
    else:
        print(json.dumps(r, ensure_ascii=False, indent=1))
