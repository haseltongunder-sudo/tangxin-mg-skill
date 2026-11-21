import json, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'engine')); import camfx
CN={'push_in':'慢推','pull_out':'慢拉','pan_l':'左摇','pan_r':'右摇','tilt_up':'上摇','tilt_down':'下摇','crane_up':'升降揭示','crane_down':'俯冲下降','snap_zoom':'急推打点','snap_back':'急拉回全景','reveal_pull':'特写拉开','truck_l':'左移跟拍','truck_r':'右移跟拍','diagonal':'斜向推进','dolly_zoom':'希区柯克变焦','orbit':'环绕','dutch':'荷兰角倾斜','handheld':'手持晃动','impact':'冲击震屏','bounce':'弹性推近','double_punch':'两段急推','drift':'视差漂移','parallax_push':'3D视差推','rack_focus':'虚焦转实','focus_out':'实焦转虚','point_back':'推近再拉回','pan_settle':'甩到位回弹','pedestal_up':'垂直升起','spiral_in':'旋转推进','breath':'呼吸缩放','look_around':'左右环视','wide_reveal':'大全景揭示','lock':'固定机位'}
TN={'zoom':'穿越','whip':'甩镜','iris':'圆形开合','flash':'白闪','fade':'黑场','wipe':'擦除','clock':'时钟擦除','diamond':'菱形展开','square':'方形展开','star_in':'星形展开','blinds':'百叶窗','blinds_v':'竖百叶','checker':'棋盘格','doors':'关门开门','bars':'上下合幕','ink':'墨滴晕开','bubbles':'泡泡','stripes':'MG彩条','slide':'推移','shrink':'缩成卡片','flip':'翻转','spin':'旋转','blur':'模糊溶解','pixel':'像素化','glitch':'故障闪','whip_v':'竖向甩镜','dip':'色块过渡'}
pres=[p for p in camfx.PRESETS if p!='lock']
trs=list(TN)
scenes=['s115','s103','s101','s111','s104','s102','s066','s072','s105','s112','s116','s113','s001','s065','s071','s011']
targets={'s115':[700,700],'s103':[960,600],'s101':[1180,450],'s104':[900,600],'s102':[1000,620],'s066':[960,520],'s072':[1000,560],'s105':[960,520]}
shots=[]
for i,p in enumerate(pres):
    sc=scenes[i%len(scenes)]
    s={'scene':sc,'dur':2.6,'camera':{'preset':p,'at':targets.get(sc,[960,560])},'replay_enter':False,
       'cards':[{'style':'tag','x':60,'y':60,'items':[f'i:镜头 {i+1:02d} · {CN[p]}'],'t':0.15,'size':40}]}
    if i%3==0: s['actors']=[{'src':'../demo/teacher_R_idle','role':'teacher','shot':'full','x':1450}]
    if p in('impact','snap_zoom') : s['cards'].append({'style':'pain','x':targets.get(sc,[960,560])[0],'y':targets.get(sc,[960,560])[1],'r':50,'t':1.0})
    tr=trs[i%len(trs)] if i<len(pres)-1 else None
    if tr:
        o={'type':tr,'dur':.5}
        if tr in('zoom',):o['at']=targets.get(sc,[960,540])
        if tr=='whip':o['dir']=1
        if tr=='slide':o['dir']='l'
        s['out']=o; s['cards'].append({'style':'tag','x':60,'y':165,'items':[f'warn:转场 · {TN[tr]}'],'t':1.6,'size':34})
        nxt=dict(o)
        shots.append(s); s2_in=nxt
    else: shots.append(s)
    if i>0:
        prev_out=shots[i-1].get('out')
        if prev_out:
            n=dict(prev_out)
            if n['type']=='zoom': n['at']=[960,540]
            shots[i]['in']=n
# split into 4 files
k=8
for j in range(0,len(shots),k):
    json.dump({'fps':30,'ss_cap':1.3,'out':f'part{j//k+1}.mp4','shots':shots[j:j+k]},open(os.path.join(HERE, f'part{j//k+1}.json'),'w'),ensure_ascii=False)
print(len(shots), len(trs))
