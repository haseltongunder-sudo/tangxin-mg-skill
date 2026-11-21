"""MG 场景库核心：分层 SVG（1920x1080），颜色走 CSS 变量，可整体换配色；每层带入场方式与循环动效标记。"""
import math, json, html

W, H = 1920, 1080


def c(col):
    """'#hex' 原样；否则视为配色变量名"""
    return col if (col.startswith('#') or col.startswith('rgb') or col == 'none') else f'var(--{col})'


def fill(col, op=None):
    s = f'fill:{c(col)}'
    if op is not None: s += f';fill-opacity:{op}'
    return s


class Scene:
    def __init__(self, sid, name, cat, tags, palette, desc='', stand=None):
        self.sid, self.name, self.cat, self.tags, self.pal, self.desc = sid, name, cat, tags, palette, desc
        self.defs, self.layers, self._n = [], [], 0
        # 角色站位（地面线 y 与可站 x 范围）与字幕安全区
        self.stand = stand or {'ground_y': 900, 'x': [560, 1360]}
        self.subtitle = [0, 950, 1920, 1060]
        self.vignette = .12
        self.grain = .05

    def uid(self, p='g'):
        self._n += 1
        return f'{self.sid}-{p}{self._n}'

    # ---------- defs ----------
    def lg(self, stops, x1=0, y1=0, x2=0, y2=1, units=None):
        i = self.uid('lg')
        u = f' gradientUnits="userSpaceOnUse"' if units else ''
        st = ''.join(f'<stop offset="{o}" style="stop-color:{c(col)};stop-opacity:{op}"/>' for o, col, op in [(s if len(s) == 3 else (s[0], s[1], 1)) for s in stops])
        self.defs.append(f'<linearGradient id="{i}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"{u}>{st}</linearGradient>')
        return f'url(#{i})'

    def rg(self, stops, cx=.5, cy=.5, r=.5, units=None):
        i = self.uid('rg')
        u = f' gradientUnits="userSpaceOnUse"' if units else ''
        st = ''.join(f'<stop offset="{o}" style="stop-color:{c(col)};stop-opacity:{op}"/>' for o, col, op in [(s if len(s) == 3 else (s[0], s[1], 1)) for s in stops])
        self.defs.append(f'<radialGradient id="{i}" cx="{cx}" cy="{cy}" r="{r}"{u}>{st}</radialGradient>')
        return f'url(#{i})'

    def clip(self, inner):
        i = self.uid('cp')
        self.defs.append(f'<clipPath id="{i}">{inner}</clipPath>')
        return f'url(#{i})'

    # ---------- layers ----------
    def layer(self, name, items, enter='rise', delay=0.0, loop=None, origin=None, depth=None, blur=0):
        """enter: fade|rise|drop|pop|grow|slide-l|slide-r|zoom ；loop: drift|sway|bob|twinkle|flow|swing|glow"""
        body = ''.join(items)
        if blur: body = f'<g filter="url(#{self.sid}-dof{blur})">{body}</g>'
        self.layers.append(dict(name=name, enter=enter, delay=round(delay, 2), loop=loop, origin=origin, depth=depth, body=body))

    def svg(self, standalone=True):
        vars_ = ';'.join(f'--{k}:{v}' for k, v in self.pal.items())
        out = []
        for L in self.layers:
            a = f' data-enter="{L["enter"]}" data-delay="{L["delay"]}"'
            if L['loop']: a += f' data-loop="{L["loop"]}"'
            if L['origin']: a += f' data-origin="{L["origin"]}"'
            if L['depth'] is not None: a += f' data-depth="{L["depth"]}"'
            out.append(f'<g class="layer" id="{self.sid}-{L["name"]}"{a}><g class="cam">{L["body"]}</g></g>')
        common = ('<filter id="sh" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#3a2a48" flood-opacity=".16"/></filter>'
                  '<filter id="shs" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#3a2a48" flood-opacity=".18"/></filter>'
                  '<filter id="b6"><feGaussianBlur stdDeviation="6"/></filter><filter id="b20" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="20"/></filter>'
                  '<filter id="b40" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="40"/></filter>'
                  '<filter id="wob" x="-2%" y="-2%" width="104%" height="104%"><feTurbulence type="fractalNoise" baseFrequency=".018" numOctaves="2" seed="4"/><feDisplacementMap in="SourceGraphic" scale="3.2"/></filter>'
                  '<filter id="t-plaster" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".008" numOctaves="5" seed="7"/><feColorMatrix values="0 0 0 0 .28  0 0 0 0 .22  0 0 0 0 .18  0 0 -1.6 0 1.05"/></filter>'
                  '<filter id="t-wood" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".003 .09" numOctaves="3" seed="2"/><feColorMatrix values="0 0 0 0 .30  0 0 0 0 .18  0 0 0 0 .08  0 0 -2.2 0 1.25"/></filter>'
                  '<filter id="t-paper" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".035" numOctaves="4" seed="9"/><feColorMatrix values="0 0 0 0 .35  0 0 0 0 .28  0 0 0 0 .2  0 0 -1.4 0 .9"/></filter>'
                  '<filter id="t-chalk" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".012 .03" numOctaves="4" seed="5"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 1.3 0 -.55"/></filter>'
                  '<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 .5  0 0 0 0 .4  0 0 0 0 .3  0 0 0 .55 0"/></filter>')
        dof = ''.join(f'<filter id="{self.sid}-dof{k}" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="{k}"/></filter>' for k in (1, 2, 3, 5, 8, 12))
        common += dof
        vig = (f'<radialGradient id="{self.sid}-vig" cx=".5" cy=".46" r=".75"><stop offset=".55" stop-color="#1a1020" stop-opacity="0"/><stop offset="1" stop-color="#1a1020" stop-opacity="{self.vignette}"/></radialGradient>')
        common += vig
        grain = f'<g class="layer" id="{self.sid}-vignette" data-enter="fade" data-delay="0"><rect width="{W}" height="{H}" fill="url(#{self.sid}-vig)"/></g>'
        grain += f'<g class="layer" id="{self.sid}-grain" data-enter="fade" data-delay="0"><rect width="{W}" height="{H}" filter="url(#grain)" opacity="{self.grain}" style="mix-blend-mode:multiply"/></g>'
        meta = dict(id=self.sid, name=self.name, cat=self.cat, tags=self.tags, desc=self.desc, stand=self.stand, subtitle=self.subtitle,
                    layers=[dict(name=L['name'], enter=L['enter'], delay=L['delay'], loop=L['loop'], depth=L['depth']) for L in self.layers], palette=self.pal)
        x = ' xmlns="http://www.w3.org/2000/svg"' if standalone else ''
        return (f'<svg{x} class="mgscene" viewBox="0 0 {W} {H}" width="{W}" height="{H}" data-scene="{self.sid}" style="{vars_}">'
                f'<metadata>{html.escape(json.dumps(meta, ensure_ascii=False))}</metadata>'
                f'<defs>{common}{"".join(self.defs)}</defs>{"".join(out)}{grain}</svg>')

    def meta(self):
        return dict(id=self.sid, name=self.name, cat=self.cat, tags=self.tags, desc=self.desc, stand=self.stand,
                    layers=[L['name'] for L in self.layers], palette=self.pal)


# ---------- 形状小工具（返回 SVG 字符串） ----------
def R(x, y, w, h, col, rx=0, op=None, extra=''):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" style="{fill(col, op) if not col.startswith("url") else "fill:" + col}" {extra}/>'


def C(x, y, r, col, op=None, extra=''):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" style="{fill(col, op) if not col.startswith("url") else "fill:" + col}" {extra}/>'


def E(x, y, rx, ry, col, op=None, extra=''):
    return f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" style="{fill(col, op) if not col.startswith("url") else "fill:" + col}" {extra}/>'


def P(d, col, op=None, extra=''):
    return f'<path d="{d}" style="{fill(col, op) if not col.startswith("url") else "fill:" + col}" {extra}/>'


def S(d, col, w=4, op=1, cap='round', extra=''):
    """描边路径"""
    return f'<path d="{d}" style="fill:none;stroke:{c(col) if not col.startswith("url") else col};stroke-width:{w};stroke-opacity:{op};stroke-linecap:{cap};stroke-linejoin:round" {extra}/>'


def poly(pts, col, op=None, extra=''):
    return P('M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + 'Z', col, op, extra)


def G(items, extra=''):
    return f'<g {extra}>' + ''.join(items) + '</g>'


def T(x, y, s, size, col, weight=800, anchor='middle', extra=''):
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" '
            f'style="fill:{c(col)};font-family:\'Noto Sans SC\',\'PingFang SC\',sans-serif" {extra}>{html.escape(s)}</text>')


def cloud(x, y, s, col='#ffffff', op=1):
    parts = [E(x, y, 120 * s, 42 * s, col, op), C(x - 50 * s, y - 22 * s, 48 * s, col, op), C(x + 18 * s, y - 40 * s, 62 * s, col, op), C(x + 72 * s, y - 14 * s, 40 * s, col, op)]
    return G(parts)


def blob_tree(x, y, s, c1, c2, trunk):
    """圆冠树：x,y 为树干底部"""
    return G([R(x - 9 * s, y - 120 * s, 18 * s, 120 * s, trunk, 6 * s),
              C(x, y - 170 * s, 78 * s, c1), C(x - 52 * s, y - 135 * s, 50 * s, c1), C(x + 55 * s, y - 132 * s, 52 * s, c1),
              C(x - 22 * s, y - 196 * s, 46 * s, c2, .55), C(x + 30 * s, y - 150 * s, 30 * s, c2, .35)])


def pine(x, y, s, c1, c2, trunk):
    it = [R(x - 8 * s, y - 60 * s, 16 * s, 60 * s, trunk, 4)]
    for k in range(4):
        w = (110 - k * 22) * s; yy = y - 40 * s - k * 62 * s
        it.append(poly([(x - w, yy), (x + w, yy), (x, yy - 110 * s)], c1))
        it.append(poly([(x, yy), (x + w, yy), (x, yy - 110 * s)], c2, .5))
    return G(it)


def beam(x1, x2, x3, x4, y1, y2, sc, op=.35):
    """斜光束：上边 x1-x2 在 y1，下边 x3-x4 在 y2"""
    g = sc.lg([(0, '#ffffff', op), (1, '#ffffff', 0)], 0, y1, 0, y2, units=True)
    return P(f'M{x1},{y1} L{x2},{y1} L{x4},{y2} L{x3},{y2}Z', g)


# ---------- 一点透视 3D ----------
