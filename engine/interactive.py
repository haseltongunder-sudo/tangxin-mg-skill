"""互动版：成片 MP4 + 打点做题 → 可离线打开的互动网页（文件夹 + zip）

用法：python3 interactive.py 互动.json [输出目录]
互动.json 示例：
{
  "title": "秋季防火安全",
  "video": "秋季防火安全.mp4",            # 相对互动.json 的路径
  "lock_seek": true,                     # 没答的题不能拖过去
  "accent": "#2F6FDE",                   # 主色，默认教学蓝；"fire" = 消防红
  "chapters": [{"t": 0, "title": "秋天为什么易着火"}, ...],
  "questions": [
    {"t": 26.5, "type": "single", "q": "秋游时可以在野外烧烤吗？",
     "options": ["可以", "不可以"], "answer": [1], "explain": "野外草木干燥……", "review": 13.0},
    {"t": 60, "type": "multi", "q": "报警时要说清哪些？", "options": [...], "answer": [0,1,2]},
    {"t": 70, "type": "judge", "q": "着火时可以坐电梯。", "answer": [1]}   # judge：0=对 1=错
  ]
}
t 是暂停出题的时间（秒），一般放在讲完这个知识点的镜头末尾；review 是答错时「回看」跳到的时间。
"""
import os, sys, json, shutil, html

TPL = r'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__ · 互动版</title>
<style>
:root{--accent:__ACCENT__}*{box-sizing:border-box}body{margin:0;font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:#FFF6EC;color:#2d2d3a}
header{padding:14px 20px;font-size:22px;font-weight:800;color:#fff;background:var(--accent);display:flex;justify-content:space-between;align-items:center}
header span{font-size:15px;font-weight:600;background:rgba(255,255,255,.2);padding:6px 12px;border-radius:20px}
.wrap{display:flex;gap:18px;padding:18px;max-width:1500px;margin:auto;flex-wrap:wrap}
.stage{flex:1 1 820px;min-width:300px}.vbox{position:relative;border-radius:16px;overflow:hidden;background:#000;box-shadow:0 8px 24px rgba(0,0,0,.15)}
video{width:100%;display:block}
.bar{position:relative;height:14px;background:#f1dccb;border-radius:8px;margin:16px 6px 6px;cursor:pointer}
.fill{position:absolute;left:0;top:0;bottom:0;background:var(--accent);border-radius:8px}
.dot{position:absolute;top:50%;width:20px;height:20px;margin:-10px 0 0 -10px;border-radius:50%;border:3px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,.3);cursor:pointer}
.dot.q{background:#F08A24}.dot.q.ok{background:#2E9E5B}.dot.q.bad{background:#999}.dot.c{background:#2F6FD0;width:12px;height:12px;margin:-6px 0 0 -6px;border-width:2px}
.ctl{display:flex;align-items:center;gap:12px;padding:6px}
button{font:inherit;border:0;border-radius:12px;padding:10px 18px;font-weight:700;cursor:pointer}
.play{background:var(--accent);color:#fff}.time{color:#776;font-variant-numeric:tabular-nums}
aside{flex:0 1 340px;min-width:260px;background:#fff;border-radius:16px;padding:16px;box-shadow:0 4px 14px rgba(0,0,0,.08);align-self:flex-start}
aside h3{margin:4px 0 10px}.ch{padding:10px 12px;border-radius:10px;cursor:pointer;display:flex;gap:10px}.ch:hover,.ch.on{background:#FDEBDD}
.ch b{color:#2F6FD0;min-width:46px}.score{margin-top:14px;padding:12px;border-radius:12px;background:#EAF6EE;font-weight:700}
.mask{position:fixed;inset:0;z-index:9;background:rgba(30,25,25,.55);display:none;align-items:center;justify-content:center;padding:4%}
.card{background:#fffdf7;border-radius:20px;padding:26px 28px;width:min(720px,100%);border:5px solid #F08A24;max-height:92vh;overflow:auto}
.card .tag{display:inline-block;background:#F08A24;color:#fff;border-radius:10px;padding:4px 12px;font-size:15px;margin-bottom:10px}
.card h2{margin:4px 0 18px;font-size:clamp(18px,2.4vw,28px)}
.opt{display:block;width:100%;text-align:left;margin:10px 0;background:#FDF1E6;border:3px solid transparent;font-size:clamp(15px,1.9vw,22px)}
.opt.sel{border-color:#2F6FD0;background:#E8F0FC}.opt.right{border-color:#2E9E5B;background:#E4F5EA}.opt.wrong{border-color:#E8483B;background:#FCE6E3}
.fb{margin-top:12px;font-size:clamp(14px,1.7vw,20px);display:none;padding:12px;border-radius:12px}
.fb.ok{background:#E4F5EA;color:#1f7a44;display:block}.fb.no{background:#FCE6E3;color:#b23628;display:block}
.acts{display:flex;gap:10px;justify-content:flex-end;margin-top:14px;flex-wrap:wrap}.go{background:#2E9E5B;color:#fff}.sub{background:#2F6FD0;color:#fff}.rv{background:#eee}
.end h2{color:var(--accent)}
</style></head><body>
<header>__TITLE__ <span id="sc">答题 0/0</span></header>
<div class="wrap"><div class="stage"><div class="vbox"><video id="v" src="__VIDEO__" playsinline preload="metadata"></video>
<div class="mask" id="m"><div class="card" id="card"></div></div></div>
<div class="bar" id="bar"><div class="fill" id="fill"></div></div>
<div class="ctl"><button class="play" id="pb">▶ 开始学习</button><span class="time" id="tm">0:00 / 0:00</span>
<span style="margin-left:auto;font-size:14px;color:#998">● 蓝点：章节　● 橙点：做题</span></div></div>
<aside><h3>章节目录</h3><div id="chs"></div><div class="score" id="sum">看到橙点会暂停出题，答完继续播放。</div></aside></div>
<script>
const D=__DATA__;const v=document.getElementById('v'),m=document.getElementById('m'),card=document.getElementById('card');
const st=D.questions.map(()=>null);let cur=-1;const fmt=s=>{s=Math.max(0,s|0);return (s/60|0)+':'+String(s%60).padStart(2,'0')};
const bar=document.getElementById('bar');
function dots(){bar.querySelectorAll('.dot').forEach(e=>e.remove());const T=v.duration||1;
 D.chapters.forEach(c=>{const d=document.createElement('div');d.className='dot c';d.style.left=(c.t/T*100)+'%';d.title=c.title;d.onclick=e=>{e.stopPropagation();seek(c.t)};bar.appendChild(d)});
 D.questions.forEach((q,i)=>{const d=document.createElement('div');d.className='dot q'+(st[i]===true?' ok':st[i]===false?' bad':'');d.style.left=(q.t/T*100)+'%';d.title='第'+(i+1)+'题';d.onclick=e=>{e.stopPropagation();if(st[i]!==null||!lockAt(q.t-.05)){v.currentTime=q.t-.05;ask(i)}};bar.appendChild(d)})}
function lockAt(t){if(!D.lock_seek)return false;return D.questions.some((q,i)=>st[i]===null&&q.t<t)}
function seek(t){if(D.lock_seek){const j=D.questions.findIndex((q,i)=>st[i]===null&&q.t<t);if(j>=0){v.currentTime=D.questions[j].t-.05;ask(j);return}}v.currentTime=t}
bar.onclick=e=>{const r=bar.getBoundingClientRect();seek((e.clientX-r.left)/r.width*(v.duration||0))};
const chs=document.getElementById('chs');D.chapters.forEach(c=>{const d=document.createElement('div');d.className='ch';d.innerHTML='<b>'+fmt(c.t)+'</b>'+c.title;d.onclick=()=>seek(c.t);chs.appendChild(d)});
const pb=document.getElementById('pb');pb.onclick=()=>{if(m.style.display==='flex')return;v.paused?v.play():v.pause()};
v.onplay=()=>pb.textContent='❚❚ 暂停';v.onpause=()=>pb.textContent='▶ 继续';v.onloadedmetadata=dots;
v.ontimeupdate=()=>{const T=v.duration||1;document.getElementById('fill').style.width=(v.currentTime/T*100)+'%';document.getElementById('tm').textContent=fmt(v.currentTime)+' / '+fmt(T);
 [...chs.children].forEach((e,i)=>e.classList.toggle('on',v.currentTime>=D.chapters[i].t&&(i==D.chapters.length-1||v.currentTime<D.chapters[i+1].t)));
 if(m.style.display==='flex')return;const i=D.questions.findIndex((q,i)=>st[i]===null&&v.currentTime>=q.t&&v.currentTime<q.t+1.5);if(i>=0){v.pause();ask(i)}};
v.onended=()=>{const ok=st.filter(x=>x===true).length;card.style.borderColor='#2E9E5B';card.innerHTML='<div class="end"><h2>学习完成！</h2><p style="font-size:22px">答对 '+ok+' / '+D.questions.length+' 题</p><div class="acts"><button class="rv" onclick="location.reload()">再学一遍</button></div></div>';m.style.display='flex'};
function upd(){const n=st.filter(x=>x!==null).length,ok=st.filter(x=>x===true).length;document.getElementById('sc').textContent='答题 '+n+'/'+D.questions.length+'　答对 '+ok;document.getElementById('sum').textContent='已答 '+n+' 题，答对 '+ok+' 题。';dots()}
function ask(i){cur=i;v.pause();const q=D.questions[i];const opts=q.type==='judge'?['✔ 对','✘ 错']:q.options;const multi=q.type==='multi';let sel=[];
 card.style.borderColor='#F08A24';card.innerHTML='<span class="tag">第'+(i+1)+'题 · '+(multi?'多选':q.type==='judge'?'判断':'单选')+'</span><h2>'+q.q+'</h2>'+opts.map((o,k)=>'<button class="opt" data-k="'+k+'">'+String.fromCharCode(65+k)+'. '+o+'</button>').join('')+'<div class="fb" id="fb"></div><div class="acts" id="acts">'+(multi?'<button class="sub" id="sb">提交</button>':'')+'</div>';
 m.style.display='flex';const bs=[...card.querySelectorAll('.opt')];let done=false;
 const check=()=>{if(done)return;done=true;const ans=q.answer.slice().sort().join(),me=sel.slice().sort().join(),ok=ans===me;if(st[i]===null)st[i]=ok;
  bs.forEach((b,k)=>{if(q.answer.includes(k))b.classList.add('right');else if(sel.includes(k))b.classList.add('wrong')});
  const fb=document.getElementById('fb');fb.className='fb '+(ok?'ok':'no');fb.innerHTML=(ok?'答对了！':'再想想：正确答案是 '+q.answer.map(k=>String.fromCharCode(65+k)).join('、')+'。')+(q.explain?'<br>'+q.explain:'');
  const a=document.getElementById('acts');a.innerHTML=(!ok&&q.review!=null?'<button class="rv" id="rb">↺ 回看这段</button>':'')+'<button class="go" id="gb">继续播放 ▶</button>';
  document.getElementById('gb').onclick=()=>{m.style.display='none';v.currentTime=q.t+1.6;v.play()};
  const rb=document.getElementById('rb');if(rb)rb.onclick=()=>{m.style.display='none';v.currentTime=q.review;v.play()};upd()};
 bs.forEach((b,k)=>b.onclick=()=>{if(done)return;if(multi){sel=sel.includes(k)?sel.filter(x=>x!==k):[...sel,k];b.classList.toggle('sel')}else{sel=[k];check()}});
 if(multi)document.getElementById('sb').onclick=()=>{if(sel.length)check()}}
upd();
</script></body></html>'''

def main():
    cfg_p = sys.argv[1]; cfg = json.load(open(cfg_p)); base = os.path.dirname(os.path.abspath(cfg_p))
    title = cfg.get('title', '互动微课')
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(base, title + '_互动版')
    os.makedirs(out, exist_ok=True)
    vsrc = os.path.join(base, cfg['video']); vname = 'video.mp4'
    shutil.copy(vsrc, os.path.join(out, vname))
    for q in cfg['questions']:
        q.setdefault('type', 'single')
        if q['type'] == 'judge': q['options'] = ['对', '错']
    data = {'chapters': cfg.get('chapters', []), 'questions': sorted(cfg['questions'], key=lambda q: q['t']), 'lock_seek': cfg.get('lock_seek', True)}
    _acc = {'blue': '#2F6FDE', 'fire': '#E8483B', 'red': '#E8483B'}.get(cfg.get('accent') or 'blue', cfg.get('accent'))
    page = TPL.replace('__ACCENT__', _acc).replace('__TITLE__', html.escape(title)).replace('__VIDEO__', vname).replace('__DATA__', json.dumps(data, ensure_ascii=False))
    open(os.path.join(out, 'index.html'), 'w').write(page)
    z = shutil.make_archive(out, 'zip', os.path.dirname(out), os.path.basename(out))
    print('done', out, z)

if __name__ == '__main__':
    main()
