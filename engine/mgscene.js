/* MGScene 运行时：让分层 SVG 场景逐层入场并循环动起来。
   用法：在页面中引入 mgscene.js 后
         MGScene.play(svgElement, {speed:1});          // 入场 + 循环
         MGScene.theme(svgElement, 'dusk');            // 换配色：original|cool|warm|dusk|night|soft
         MGScene.seek(svgElement, 1.2);                // 定格到第 1.2 秒（导出视频逐帧用）
*/
(function (g) {
  const ENTER = {
    fade:   [{opacity: 0}, {opacity: 1}],
    rise:   [{opacity: 0, transform: 'translateY(160px)'}, {opacity: 1, transform: 'translateY(-14px)', offset: .7}, {opacity: 1, transform: 'translateY(0)'}],
    drop:   [{opacity: 0, transform: 'translateY(-180px)'}, {opacity: 1, transform: 'translateY(12px)', offset: .7}, {opacity: 1, transform: 'translateY(0)'}],
    pop:    [{opacity: 0, transform: 'scale(0)'}, {opacity: 1, transform: 'scale(1.08)', offset: .7}, {opacity: 1, transform: 'scale(1)'}],
    grow:   [{opacity: 0, transform: 'scaleY(0)'}, {opacity: 1, transform: 'scaleY(1.06)', offset: .7}, {opacity: 1, transform: 'scaleY(1)'}],
    'slide-l': [{opacity: 0, transform: 'translateX(-260px)'}, {opacity: 1, transform: 'translateX(10px)', offset: .75}, {opacity: 1, transform: 'translateX(0)'}],
    'slide-r': [{opacity: 0, transform: 'translateX(260px)'}, {opacity: 1, transform: 'translateX(-10px)', offset: .75}, {opacity: 1, transform: 'translateX(0)'}],
    zoom:   [{opacity: 0, transform: 'scale(1.18)'}, {opacity: 1, transform: 'scale(1)'}]
  };
  const ORIGIN = {rise: '50% 100%', drop: '50% 0%', pop: '50% 50%', grow: '50% 100%', zoom: '50% 50%'};
  const LOOP = {
    drift:   [[{translate: '0 0'}, {translate: '26px 0'}], 7000],
    sway:    [[{rotate: '-1.6deg'}, {rotate: '1.6deg'}], 2600],
    bob:     [[{translate: '0 0'}, {translate: '0 -10px'}], 1600],
    twinkle: [[{opacity: 1}, {opacity: .35}], 1100],
    flow:    [[{translate: '0 0'}, {translate: '-24px 0'}], 2400],
    swing:   [[{rotate: '-11deg'}, {rotate: '11deg'}], 1100],
    glow:    [[{opacity: 1}, {opacity: .55}], 2600],
    fall:    [[{translate: '0 0'}, {translate: '46px 58px'}], 3400],          // 落叶飘
    flicker: [[{scale: '1 1'}, {scale: '1.06 .9'}], 260],                    // 火苗跳动（配 origin 设在火焰底部）
    smoke:   [[{translate: '0 0', opacity: .9}, {translate: '-30px -60px', opacity: .5}], 2200]
  };
  function layers(svg) { return [...svg.querySelectorAll('g.layer')]; }
  function stop(svg) { layers(svg).forEach(l => { l.getAnimations().forEach(a => a.cancel()); const c = l.querySelector(':scope>g.cam'); if (c) c.getAnimations().forEach(a => a.cancel()); }); }
  // 镜头：按图层深度（0 远 ~ 1 近）做缓推 / 横移视差
  function camera(svg, mode = 'push', opt = {}) {
    const dur = (opt.duration || 14) * 1000, amt = opt.amount || 1, fx = opt.focus || [960, 560];
    layers(svg).forEach(l => {
      const c = l.querySelector(':scope>g.cam'); if (!c) return; c.getAnimations().forEach(a => a.cancel());
      if (!l.dataset.depth || mode === 'none') return; const d = +l.dataset.depth;
      c.style.transformBox = 'view-box'; c.style.transformOrigin = `${fx[0]}px ${fx[1]}px`;
      const kf = mode === 'pan' ? [{transform: `translateX(${30 * d * amt}px)`}, {transform: `translateX(${-30 * d * amt}px)`}]
        : [{transform: 'scale(1)'}, {transform: `scale(${1 + .07 * d * amt}) translateY(${-6 * d * amt}px)`}];
      c.animate(kf, {duration: dur, iterations: Infinity, direction: 'alternate', easing: 'ease-in-out'});
    });
  }
  function play(svg, opt = {}) {
    const sp = opt.speed || 1, loops = opt.loop !== false;
    stop(svg);
    if (opt.camera !== 'none') camera(svg, opt.camera || 'push', opt);
    layers(svg).forEach(l => {
      const en = l.dataset.enter || 'fade', d = (+l.dataset.delay || 0) * 1000 / sp;
      if (l.dataset.origin) { l.style.transformBox = 'view-box'; const [x, y] = l.dataset.origin.split(' '); l.style.transformOrigin = `${x}px ${y}px`; }
      else { l.style.transformBox = 'fill-box'; l.style.transformOrigin = ORIGIN[en] || '50% 50%'; }
      l.animate(ENTER[en] || ENTER.fade, {duration: (en === 'fade' ? 600 : 750) / sp, delay: d, easing: 'cubic-bezier(.22,.8,.3,1)', fill: 'backwards'});
      const lp = LOOP[l.dataset.loop];
      if (loops && lp) l.animate(lp[0], {duration: lp[1], delay: d + 800 / sp, iterations: Infinity, direction: 'alternate', easing: 'ease-in-out'});
    });
  }
  function seek(svg, t) {  // 秒
    layers(svg).forEach(l => [l, l.querySelector(':scope>g.cam')].forEach(e => e && e.getAnimations().forEach(a => { a.pause(); a.currentTime = t * 1000; })));
  }
  // ---- 配色 ----
  function hex2hsl(h) { h = h.replace('#', ''); let r = parseInt(h.substr(0, 2), 16) / 255, g = parseInt(h.substr(2, 2), 16) / 255, b = parseInt(h.substr(4, 2), 16) / 255;
    const mx = Math.max(r, g, b), mn = Math.min(r, g, b); let hh = 0, s = 0, l = (mx + mn) / 2;
    if (mx !== mn) { const d = mx - mn; s = l > .5 ? d / (2 - mx - mn) : d / (mx + mn);
      hh = mx === r ? (g - b) / d + (g < b ? 6 : 0) : mx === g ? (b - r) / d + 2 : (r - g) / d + 4; hh /= 6; }
    return [hh * 360, s, l]; }
  function hsl2hex(h, s, l) { h = ((h % 360) + 360) % 360 / 360; s = Math.max(0, Math.min(1, s)); l = Math.max(0, Math.min(1, l));
    const f = (p, q, t) => { t = (t + 1) % 1; return t < 1 / 6 ? p + (q - p) * 6 * t : t < .5 ? q : t < 2 / 3 ? p + (q - p) * (2 / 3 - t) * 6 : p; };
    let r, g, b; if (!s) r = g = b = l; else { const q = l < .5 ? l * (1 + s) : l + s - l * s, p = 2 * l - q; r = f(p, q, h + 1 / 3); g = f(p, q, h); b = f(p, q, h - 1 / 3); }
    return '#' + [r, g, b].map(x => Math.round(x * 255).toString(16).padStart(2, '0')).join(''); }
  // [色相偏移, 饱和度倍数, 亮度倍数, 混合色, 混合比例]
  const THEMES = {original: null, cool: [12, .95, 1.02, '#6FA8DC', .12], warm: [-8, 1.05, 1.02, '#FFB070', .12],
    dusk: [0, 1.0, .9, '#FF8A5C', .26], autumn: 'autumn', maple: 'maple', night: [0, .7, .62, '#1B2550', .42], soft: [0, .6, 1.06, '#FFF4E6', .18]};
  function mix(h1, h2, k) { const a = [1, 3, 5].map(i => parseInt(h1.substr(i, 2), 16)), b = [1, 3, 5].map(i => parseInt(h2.substr(i, 2), 16));
    return '#' + a.map((x, i) => Math.round(x + (b[i] - x) * k).toString(16).padStart(2, '0')).join(''); }
  function theme(svg, name) {
    if (!svg._orig) { svg._orig = {}; for (const p of svg.style) if (p.startsWith('--')) svg._orig[p] = svg.style.getPropertyValue(p).trim(); }
    // "maple:leaf,leaf2" / "autumn:leaf" 只改列出的配色键（如室内只把窗外树叶变红，黑板墙面不动）
    let only = null; if (name && name.indexOf(':') > 0) { only = name.split(':')[1].split(',').map(x => '--' + x.trim().replace(/^--/, '')); name = name.split(':')[0]; }
    const t = THEMES[name];
    if (only && (t === 'maple' || t === 'autumn')) {
      for (const [k, v] of Object.entries(svg._orig)) {
        if (!only.includes(k) || !/^#[0-9a-fA-F]{6}$/.test(v)) { svg.style.setProperty(k, v); continue; }
        let [h, s, l] = hex2hsl(v); const u = Math.min(1, Math.max(0, (l - .3) / .45));
        svg.style.setProperty(k, t === 'maple' ? hsl2hex(2 + 20 * u, Math.max(.7, Math.min(.95, s * 1.25)), .38 + .2 * u) : hsl2hex(22 + 22 * u, Math.max(.72, Math.min(1, s * 1.3)), .42 + .2 * u));
      }
      return;
    }
    if (t === 'maple') {  // 红枫：绿、黄色系的树木转成枫红/橙红，其余颜色略加暖
      for (const [k, v] of Object.entries(svg._orig)) {
        if (!/^#[0-9a-fA-F]{6}$/.test(v)) { svg.style.setProperty(k, v); continue; }
        let [h, s, l] = hex2hsl(v);
        if (h >= 35 && h <= 185 && s > .25) { const u = Math.min(1, Math.max(0, (l - .3) / .45)); svg.style.setProperty(k, hsl2hex(2 + 20 * u, Math.max(.7, Math.min(.95, s * 1.25)), .38 + .2 * u)); }
        else svg.style.setProperty(k, mix(v, '#FF9A70', .08));
      }
      return;
    }
    if (t === 'autumn') {  // 金秋：绿色系（色相 70–170°）一律转成金黄/橙红，其余颜色略加暖
      for (const [k, v] of Object.entries(svg._orig)) {
        if (!/^#[0-9a-fA-F]{6}$/.test(v)) { svg.style.setProperty(k, v); continue; }
        let [h, s, l] = hex2hsl(v);
        if (h >= 60 && h <= 185 && s > .12) { const u = Math.min(1, Math.max(0, (l - .3) / .45)); svg.style.setProperty(k, hsl2hex(22 + 22 * u, Math.max(.72, Math.min(1, s * 1.3)), .42 + .2 * u)); }
        else svg.style.setProperty(k, mix(v, '#FFB070', .08));
      }
      return;
    }
    for (const [k, v] of Object.entries(svg._orig)) {
      if (!t || !/^#[0-9a-fA-F]{6}$/.test(v)) { svg.style.setProperty(k, v); continue; }
      let [h, s, l] = hex2hsl(v);
      svg.style.setProperty(k, mix(hsl2hex(h + t[0], s * t[1], l * t[2]), t[3], t[4]));
    }
  }
  function meta(svg) { const m = svg.querySelector('metadata'); return m ? JSON.parse(m.textContent) : {}; }
  g.MGScene = {play, stop, seek, theme, camera, meta, THEMES: Object.keys(THEMES)};
})(window);
