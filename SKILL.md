---
name: tangxin-mg-skill
description: 平面 MG 教学动画场景库 + 成片引擎，任何学科、任何主题通用。112 个程序绘制的分层矢量场景（1920×1080、无人物，12 类 c01–c12，含季节专题和通用讲解台/答题台），每层带入场和循环动效，可整体或局部换配色，导出 PNG/MP4/单文件图库；compose.py 合成师生出镜成片：角色口型同步与眨眼（rig.py 由一张定稿图自动生成）、33 种运镜 + 27 种转场、知识点图卡和信息组件、「考考你」倒数答题、分角色配音；assemble.py 总装（进度条、章节、自动配乐）；interactive.py 出暂停做题的互动网页版。要做课件或科普动画、新增场景、导出场景视频、合成教学动画成片时加载。
---

# 平面 MG 教学动画（tangxin-mg-skill）

## 开工前：检查更新（每次对话第一次用本技能时做一次）
运行 `python engine/update.py`（在技能目录里）。
- `"update": true`：告诉对方「有新版本 本地版本 → 最新版本」，并用一两句话说 `notes` 里更新了什么，问要不要更新。对方同意才运行 `python engine/update.py --apply`，然后重新读一遍本 SKILL.md 再继续。不同意就用当前版本照常工作。
- `"update": false` 或连不上（`latest` 为 null）：不用提，直接开始工作。
- 更新源：https://github.com/haseltongunder-sudo/tangxin-mg-skill（版本号在 `VERSION`，更新说明在 `CHANGELOG.md`）。

## 0. 硬规则总表（任何主题都适用，与下文冲突时以本表为准）

| # | 规则 |
|---|---|
| 1 | **三步流程，每步等对方确认**：① 方案（分镜表：场景、人物站位、台词归属、卡片、运镜转场、考考你位置、总时长）→ 确认 → ② 关键帧预览（`--preview` 出每镜关键帧 + `out/preview/总览.jpg` 拼图）→ 确认 → ③ 渲染、总装、互动版。被否定就回到那一步，不直接重渲整片。 |
| 2 | **角色来源先问**：A 对方提供 / B 我按主题生成 / C 混合。对方选定并确认后才开工（§5）。 |
| 3 | **只有老师讲知识点**。学生只提问（「老师，为什么……？」）、简短回应（「原来是这样！」）或不说话的动作示范，台词里不出现知识点。 |
| 4 | **老师不站画面中间**：只站左侧 x 300–570 或右侧 x 1350–1620（`actor.x` 是人物中心，必须写；`flip` 只镜像不改位置），手指向另一侧。卡片放在老师的另一侧，绝不压住老师（尤其头部）。师生同框：老师一侧、学生另一侧，中间留给卡片或场景主体。 |
| 5 | **老师适度出镜**：非答题镜头中出镜约 40–60%，不连续 3 个以上镜头出镜。其余是画外音 + 居中知识主体（大卡片、分步示意图、图标宫格、口诀板、推近场景演示），画面不能空。 |
| 6 | **考考你每集最多 2 次，每次 1 道题**，放在两个最重要的知识段之后；MP4 版和互动版题目、位置一致；进度条要标出这 2 个位置。 |
| 7 | **口型**：说话的人才开口（`talk` 时段播 talk 帧）；不说话的人 `talk:[]`，闭嘴并眨眼（idle 帧）。有 idle 必须有 talk、有 talk 必须有 idle；动作循环素材（跑、弯腰）写 `"action": true`。时段用 `tts.py` 算。 |
| 8 | **镜头设计**：每集至少 8 种不同运镜 preset + 6 种不同转场（短片按镜头数 n 放宽为 min(8,n) / min(6,n+1)），相邻镜头的运镜和相邻两次转场都不重复。 |
| 9 | **转场只用 camfx 的 `in`/`out`**：每个镜头写自己的 `in` 和 `out`，前一镜 `out` 与后一镜 `in` 同类型（lint E-trans-pair），分镜头渲染后直接 concat 就是完整转场。不用 xfade / `dissolve`（§4）。 |
| 10 | **切镜不停顿**：`audio_at` 0.25（lint 允许 0.15–0.35）；compose 自动把镜头时长延长到「audio_at + 配音时长 + 0.4 s」，不要再手动加长 `dur`，也不要 0.5 s 前空 + 1 s 以上尾空。 |
| 11 | **画面贴题**：场景按台词内容、主题和季节挑选（秋天不出现绿树，冬天用雪景）；人物只站在清晰的地面上（场景 `stand.x` 范围、`ground_y` 地面线），不踩在桌椅、道具或其他物体上；画面文字与旁白同步出现（`board` 用 `times`、卡片用 `t`/`gap` 对齐配音）。 |
| 12 | **可选模块按需取舍**：顶部章节条、讲解台示意图、标签条、配乐都是可选的，按学科和内容灵活用，不要每集套同一个模板。 |
| 13 | 每个非答题镜头写 `"replay_enter": true`（背景元素逐层重新入场）；字幕一行 ≤22 字，最好 ≤14 字；不压 y 950 以下的字幕区。 |

## 1. 这是什么 + 快速上手
- **场景库**：112 个场景，每个是一个 Python 函数 → 分层 SVG，`mgscene.js` 负责入场、循环、换色。**不含人物**，标有站位 `stand={'ground_y','x':[左,右]}`。编号表见 `STYLE.md`。
  - c01–c10：10 类学科与日常各 10 个（s001–s100）；c11 季节专题 s101–s106；c12 通用讲解台 s111–s113、答题星空台 s114、看台 s115、舞台 s116。
- **成片引擎**：compose.py（镜头合成）→ assemble.py（总装）→ interactive.py（互动版）。
- **包内**：`examples/svg` 带全部场景 SVG（compose 直接可用）；图库 HTML、镜头库样片由引擎重建：`render.py`、`build_gallery.py`、渲染 `examples/shot_library/part*.json` 再 `assemble.py asm.json`。

**5 条命令从零出样片**（在 skill 根目录执行）：
```bash
python3 engine/doctor.py                                   # 1 自检环境
pip install -r requirements.txt && python3 -m playwright install chromium   # 2 装依赖（doctor 报缺时）
python3 engine/render.py                                   # 3 生成场景 SVG/PNG（examples/svg 已带，可跳过）
python3 engine/compose.py examples/demo_shots.json --preview   # 4 关键帧预览 → engine/out/preview/（示例：火灾逃生·弯腰低姿 5 镜，lint 0 错 0 警告）
python3 engine/compose.py examples/demo_shots.json         # 5 成片 → examples/out/demo.mp4
```

## 2. 环境
- `requirements.txt`：playwright、pillow、fonttools、brotli、numpy、edge-tts（均锁版本）。系统需要 **ffmpeg/ffprobe**。
- `python3 engine/doctor.py` 检查依赖、Chromium、ffmpeg、字体；缺什么按提示装：`pip install -r requirements.txt`、`python3 -m playwright install chromium`。
- 字体已附（`engine/fonts/`），无需配置。配音用 edge-tts（已在 requirements，需联网）+ `engine/tts.py`。
- c08 引用了 c07 的共用工具，两个文件要一起保留。

## 3. 命令表（脚本都在 `engine/`）
| 脚本 | 用法 | 产出 / 说明 |
|---|---|---|
| render.py | `render.py [模块名…]` | 不带参数渲染全部 `scenes_*`；`out/svg/`、`out/png/`、`out/meta/`，总表 `out/scenes.json` 自动合并 |
| build_gallery.py | `build_gallery.py` | `out/MG场景图库.html`（单文件离线图库，需先 render） |
| export_mp4.py | `export_mp4.py s001 4 out.mp4 [--theme dusk] [--fps 30]` | 纯场景入场 + 循环动画 MP4 |
| compose.py | `compose.py 镜头表.json [--res 1080\|1440\|2160] [--preview] [--at 0.1,1.5,-0.2] [--no-lint]` | 成片；`--preview` 每镜出中间帧（`--at` 指定时刻，负数从结尾数）到 `out/preview/` |
| render_shots.py | `render_shots.py 镜头表…json -j 2 --timeout 900 [--force]` | 批量逐镜渲染，跳过已是最新的，支持断点续跑（§8） |
| lint.py | `lint.py 文件或目录… [--interactive 互动.json]` | 按硬规则检查，有错误退出码 1（代码表见 §8）。单镜头文件只查单镜，整集统计由 render_shots/assemble 做 |
| tts.py | `tts.py lines.txt out_dir [--voices teacher=…,student=…] [--force] [--vad-only]` | `id\|speaker\|text` → `<id>.mp3` + `lines.json`（`{id:{file,dur,talk}}`，能量 VAD）；没网络时明确报错 |
| doctor.py | `doctor.py` | 环境自检 |
| rig.py | `rig.py chars.json` | 由定稿角色图生成口型/眨眼帧（§5） |
| assemble.py | `assemble.py 总装.json [--no-lint]` | 拼接 + 进度条 + 章节 + 配乐；写 `interactive` 时比对题目并同时出互动版（§6） |
| interactive.py | `interactive.py 互动.json [输出目录]` | `{标题}_互动版/`（index.html + video.mp4）和同名 zip |
| bgm.py | `bgm.py out.wav 秒数 [bright\|calm\|tense]` | 合成配乐 |

配色主题：original、cool、warm、dusk、night、soft、autumn（绿转金秋）、maple（绿/黄转枫红）。

## 4. 镜头表 JSON 参考（坐标一律按 1920×1080）
文件级：`shots`、`out`、`fps`(30)、`ss_cap`(超采样上限，默认 2.0)、`bgm`/`bgm_vol`、`dissolve`、`lint`(false 关闭检查)。

**shot 字段**
| 字段 | 说明 |
|---|---|
| `scene` | 场景编号，如 `s072` |
| `dur` | 秒数；有配音时自动延长到 `audio_at + 配音 + 0.4` |
| `audio` / `audio_at` | 本镜配音及开口时间（默认 0.3，规范用 0.25） |
| `audios` | 多段配音 `[{file, at}]`（答题镜头用） |
| `theme` | 配色；**局部换色** `"maple:leaf,leaf2"` / `"autumn:t1,t2"`：只改列出的 palette 键（如室内只把窗外树叶变红，黑板墙面不动），仅 maple、autumn 支持 |
| `camera` | `{"preset":名,"at":[x,y],"amt":1}`；或手写 `keys:[{t,zoom,center,roll,ease,blur}]`（ease：inout/in/out/linear/back/snap）+ `parallax`(0.8–1.2) `dref`(0.62) `shake`(px)；旧写法 `zoom:[a,b]`+`center` 仍可用 |
| `in` / `out` | 转场 `{type, dur(0.35–0.6), at, dir, color:[r,g,b], amount}` |
| `replay_enter` | true = 背景逐层重新入场 |
| `actors` | 角色列表（下表） |
| `cards` | 知识点卡片和信息组件（§6） |
| `subs` | 字幕 `[{t, d, text}]`，相邻自动不重叠；`sub_span:[x0,x1]` 手动限定字幕横向范围 |
| `fx` | 场景特效：`flame{x,y,s,smoke,t_in,t_out}`、`stamp{x,y,kind:no/ok,t,r}`、`focus{x,y,r,t,d}`、`leaves{n,t_in,size}` |
| `quiz` | 答题（§6）；配 `static:true`（背景只截一次）、`bg_blur` |

`dissolve`（默认 0.4）只对同一 json 里没写 `in` 的镜头用上一镜末帧淡入，分镜头拼接时无效；所以每镜都写 `in`，柔和用 `blur`/`fade`/`dip`。

**actor 字段**
| 字段 | 说明 |
|---|---|
| `src` | 说话帧：GIF 或 PNG 序列文件夹（文件名带 `_90ms` 即该帧时长） |
| `idle` | 闭嘴待机/眨眼帧；不在 `talk` 时段播放 |
| `talk` | `[[t0,t1],…]` 本镜说话时段（秒）；`[]` = 全程闭嘴 |
| `role` | teacher / student / kid，决定全身默认身高 640 / 500 / 460 |
| `shot` | full 全身（踩地面线、自动接地阴影）/ knee 七分身；half、bust 默认被改成 knee，确需时加 `allow_close:true` |
| `x` | 人物中心横坐标（老师见硬规则 4） |
| `height` | 手动身高；`dy` 脚底微调 |
| `t_in` / `t_out` | 入场 / 退场时间 |
| `enter` | slide / pop / rise / fade |
| `key` | white / green：非透明底时抠图 |
| `flip` | 水平镜像（朝向另一侧）；示例只带 teacher_R，左侧老师用它加 `"flip": true` |
| `z` `speed` `still` `shadow` | 层次、播放速度、定格首帧、阴影开关 |
| `action` | true = 动作循环素材（跑、弯腰），不说话也不需要 talk/idle（免 E-no-talk） |
| `poses` | `[{src, idle, t:[t0,t1], height?}]`，在该时段切换到另一姿势（如指黑板、举手）的 talk/idle 帧，口型照常按 `talk` |
| `sway` | 身体轻微呼吸起伏 + 说话时轻点头，浮点，默认 1.0，0 关闭（旧 `breathe:false` 等同 0） |
| `accent`（镜头表顶层） | 卡片/题条主色，默认教学蓝 `#2F6FDE`；写 `"fire"` 为消防红，或直接写颜色 |

## 5. 角色
场景库不含人物。出方案时列出需要的角色和动作，**问对方选来源**：
- **A 对方提供**：GIF/PNG 序列，透明底、全身、单人，老师 ≥900px（七分身要高清）、学生 ≥700px；收到后查透明底（否则 `key`）、脚底一致、朝向（`flip`）、12–15fps。
- **B 我来生成**：用 generate_image 为每个角色生成**一张定稿底图**（透明底、正面、闭嘴微笑、全身、高 ≥1000px），先给对方确认；需要时再生成 2–4 张同一人物的姿势图（指向、举手、点赞、弯腰等）。然后用 rig.py 自动出口型和眨眼。同一主角全片同一张脸、同一套衣服；不用骨骼木偶小人。
- **C 混合**：对方给已有动作，缺的按 B 补，补前列清单确认。

**rig.py**：`python3 engine/rig.py chars.json`，格式照 `examples/rig/chars.json`：`chars.<名>` = `src`、`mouth`、`eyes`，可选 `crop`、`scale`、`poses:{姿势名:{src, mouth?, eyes?}}`。
- 输出 `<name>_talk/`、`<name>_idle/`、`<name>_<pose>_talk/`、`<name>_<pose>_idle/`，以及 `rig_check.jpg`（闭嘴/半张/大张/闭眼四格，必须看一遍）。姿势的 mouth/eyes 不填就沿用底图的。`scale` 是嘴部细节放大倍数（底图缩小时同比调小），`talk_seq`/`idle_seq` 自定义帧序列。
- **量坐标**（底图原尺寸）：`mouth=[嘴中心x, 微笑线y, 嘴宽]`，`eyes` 每只 `[cx, cy, rx, ry]`；按候选坐标画红框看图微调。底图缩放 k 倍时坐标、半径一起乘 k。
- compose 里：`{"src":"frames/teacher_talk","idle":"frames/teacher_idle","talk":[[0.25,2.1]]}`。
- 示例：缩小量化的老师底图（438×972，<300 KB）+ 程序倾斜 3° 的姿势 `lean`；`rig_check_expected.jpg` 是预期检查图。肤色只从不透明像素（alpha>200）取邻域中位数，补丁按原图 alpha 裁剪，靠近透明边也不会出暗边。

**talk 时段**：`tts.py` 每句一个 mp3，并在 `lines.json` 给出句内说话时段（相对音频开头）；放进镜头时 `talk=[[audio_at+t0, audio_at+t1],…]`。

**配音分角色**：台词写成 `说话人|台词`，edge-tts 选声：T 女教师 zh-CN-XiaoxiaoNeural、男教师 zh-CN-YunxiNeural、S 男学生 zh-CN-YunxiaNeural、G 女学生 zh-CN-XiaoyiNeural（先看角色性别再分配）。代理问题 tts.py 已内置处理，无需手动补丁。

## 6. 卡片、答题、互动版、总装、配乐
**基础卡片 `cards`**（叠在镜头运动之后，不随推拉变形）：`style` = `list` 清单 / `chips` 关键词 / `steps` 步骤 / `compare` 对错两条 / `big` 大字（`big`+`note`）；`title`、`color`（默认 #E8483B；橙 #F08A24 提醒、绿 #2E9E5B 正确、蓝 #2F6FD0 步骤）、`items`（前缀 `ok:` 绿勾、`no:` 红叉、`warn:` 感叹号、`1:` 编号，纯文字圆点）、`x y w`、`t` 出现、`d` 时长、`gap` 逐条间隔、`size`。条目 2–4 条、每条 ≤10 字。
**信息组件（ui.py，全部可选）**
| style | 用途 | 关键字段 |
|---|---|---|
| `tag` | 标签条逐条滑入堆叠 | items 前缀 ok:/no:/warn:/i:；x y size stack gap |
| `tiles` | 图标宫格 | items `图标名:文字` 或 `图片.png\|文字`；cols cell |
| `ban` | 禁止图标组 | items `图标或图片\|文字`；r spacing |
| `board` | 口诀板逐行出现，`!` 开头的行红色 | title items w line head；`times:[秒,…]` 逐行出现时刻（对齐朗读）；`cross:false` 去掉标题红十字 |
| `mark` | 黄色圈注 + 小标签 | x y r label |
| `pain` | 红色闪烁 + 扩散圈 | x y r |
| `img` | 示意图，多张按 t 先后出现即分步动画 | src x y w enter(pop/fade/rise/wipe_l/r/d) in_dur |
| `arrow` | 边画边出现的箭头 | from to color width |

内置图标：burst swell deform ban ok no warn phone fire drop water clock eye hand heart star bolt home book bell mask sun moon。示意图用 core.py 画或 generate_image 生成扁平透明图。

**答题镜头 `quiz`**（每集 ≤2 个，见硬规则 6）：
```json
{"scene":"s114","static":true,"dur":16,"camera":{"preset":"lock"},
 "audios":[{"file":"q1a.wav","at":0.3},{"file":"q1b.wav","at":11.4}],
 "quiz":{"style":"kit","no":1,"q":"前臂骨折，\n夹板要固定哪两个关节？","options":["只绑受伤处","手腕和手肘","手肘和肩膀"],
         "answer":[1],"t":0.2,"cd_at":5.5,"countdown":5}}
```
- 时间轴：`t` 弹题 → 题干配音（「考考你：……倒数五秒！」，不读选项）→ `cd_at`=题干结束+0.3 倒数 → `cd_at+countdown` 揭晓 → 答案配音在揭晓后约 0.4 s。滴答和「叮」自动生成（`tick:false` 关）。
- `style:"kit"`：深蓝星空底（配 s114）、顶部「考考你①」题条、选项是急救箱式卡片；选项图 `option_imgs` / 图标 `option_icons` / 大字 `option_glyphs`，都没有显示 A/B/C；题条色 `quiz.color`、位置 `bar:{w,x,y,size,align}`。不写 style 是居中题卡（`x w max_w y size color`），老师在右时设 `x≈70, w≈1080`。
- `kind`：单选/多选/判断（`options:["对","错"]`）。题干 ≤24 字，选项 2–4 个、≤12 字；题框自适应，`\n` 换行。

**互动版（默认随 MP4 交付）**：`互动.json` = `title` `video` `lock_seek` `chapters:[{t,title}]` `questions:[{t, type:single|multi|judge, q, options, answer, explain, review}]`（judge 0=对 1=错）。题目 `t` 按镜头 MP4 实际时长累加，与 MP4 版一致（assemble 的 `interactive` 自动比对、自动生成）。交付 zip，解压双击 index.html。

**总装 `assemble.py 总装.json`**：`shots`（镜头 MP4 列表）、`out`、`title`、`chapters:[{shot:第几个文件, title, quiz:true}]`、`topbar`（顶部章节条，可选）+`topbar_style{y,x0,x1,color,ink,size}`、`bgm`（`"auto"` 调 bgm.py，`bgm_mood` bright/calm/tense；或音乐文件）、`bgm_vol`（默认 0.16，人声出现自动压低）。`bottombar` 默认 `"auto"`：有考题自动画底部细进度条和「考」标记（写 true/false 强制开关），顶部章节条也标出考题；`accent` 主色；章节写入 MP4 元数据；临时文件走 tempfile 再拷贝（网络盘 faststart 会失败）。
`interactive`：`"互动.json"`（或内联对象）→ 开工前比对 MP4 答题镜头和互动版 questions 的数量、顺序、题目、答案、位置（不一致报 E-quiz-mismatch 停止），成片后自动出互动版；`interactive_video` 默认 `"noquiz"`（拼 `{out}_无题版.mp4`，题目 t 按无题版时间轴、放在答题镜头前一镜结尾）/ `"full"`（用完整成片）。

## 7. 镜头库：33 运镜 + 27 转场 = 60（camfx.py）
样片配置 `examples/shot_library/`（mk.py 生成 part1–4.json + asm.json）。
- **运镜 preset（33）**：推拉 push_in pull_out diagonal breath wide_reveal point_back ｜ 摇移 pan_l pan_r tilt_up tilt_down look_around pan_settle ｜ 升降跟拍 crane_up crane_down pedestal_up truck_l truck_r ｜ 打点 snap_zoom snap_back reveal_pull impact bounce double_punch ｜ 3D/风格 parallax_push drift dolly_zoom orbit spiral_in dutch handheld ｜ 焦点 rack_focus focus_out lock
- **转场 type（27）**：镜头式 zoom whip whip_v spin blur flash fade ｜ 形状 iris diamond square star_in clock ink bubbles ｜ 擦除拼块 wipe blinds blinds_v checker doors bars ｜ MG 风格 stripes slide shrink flip dip pixel glitch
- 选用：开场 crane_up/wide_reveal/rack_focus，打点 snap_zoom/bounce，警示 impact/handheld，跟人 truck，讲解 parallax_push/drift，收尾 pull_out/focus_out，答题 lock；转场：进讲解台 stripes/shrink/slide，进考考你 iris/star_in，警示 glitch/flash，同场景 whip/blur，穿越门窗 zoom（`at`）。`dir`：whip 1/-1，wipe/slide l/r/u/d。

## 8. 批量渲染
- 速度：2 核机器 1080p 约 **40 秒算 1 秒视频（每进程）**，4K 约 3 倍。必须先 `--preview`。
- 长片按镜头拆成多个 json（每个 1–2 镜），用 `python3 engine/render_shots.py shots/*.json -j 2 --timeout 900` 并行；已是最新的镜头自动跳过，中断后重跑即续；`--force` 全部重渲。
- 沙箱单条命令有时限：`nohup … &` 后台跑、写日志、轮询。
- lint 在 compose/assemble 里自动运行，跳过用 `--no-lint` 或 `"lint": false`。最后 assemble 拼接（同分辨率、同 fps）。
- **lint 代码**。错误：E-quiz-count（>2 题）E-quiz-multi（一题多问）E-teacher-mid（x 在 700–1220）E-teacher-pos（x 不在 300–570/1350–1620 或没写）E-card-side（卡片与老师同侧，中心 860–1060 的居中卡片除外）E-talk-idle / E-idle-talk（talk、idle 缺一）E-trans-pair（前 out≠后 in）E-quiz-mismatch（MP4 题与互动版不一致）E-asset（素材缺失）E-no-talk（有配音但无 talk/idle）。警告：W-audio-at（不在 0.15–0.35）W-adjacent（相邻同运镜/同转场）W-teacher-ratio（40–60%，n 镜允许 ⌊0.4n⌋–⌈0.6n⌉）W-teacher-run（连续 ≥3 镜）W-variety（运镜 <min(8,n) 或转场 <min(6,n+1)）。

## 8.1 流水线示例：配音 → 口型 → 镜头 → 成片（`examples/pipeline/`）
```bash
cd examples/pipeline
python3 ../../engine/tts.py lines.txt voice             # 1 → voice/*.mp3 + voice/lines.json
python3 ../../engine/rig.py ../rig/chars.json           # 2 定稿老师图 → ../rig/frames/teacher_talk|idle（+ lean 姿势），看 rig_check.jpg
python3 build_shots.py                                  # 3 lines.json + plan.json → shots/*.json + asm.json + 互动.json，自动 lint
python3 ../../engine/render_shots.py shots/*.json -j 2  # 4 逐镜渲染（后台跑）
python3 ../../engine/assemble.py asm.json               # 5 成片 + 无题版 + 互动版（interactive 字段调 interactive.py）
```
plan.json 每镜写 line、scene、teacher L/R/null、camera、in、cards、subs（按说话时段排时间）；quiz 同时生成 MP4 题和互动版题。

## 9. 新增场景 + 验收
1. 读 `STYLE.md`，挑 1–2 个相近样板（scenes_01、scenes_02 是定稿样板）。
2. 在对应 `scenes_cXX.py` 写函数返回 `Scene(...)`，加进文件末尾 `SCENES`：
```python
def s120():
    pal = {'sky':'#BFE3F5', 'wall':'#F6EBDD'}                          # 颜色全在 palette
    s = Scene('s120', '场景名', '类别', ['学科', '课题'], pal, desc='一句话', stand={'ground_y': 820, 'x': [560, 1360]})
    s.layer('sky', [R(0, 0, 1920, 1080, 'sky')], enter='fade', delay=0, depth=0)
    return s                                                          # 共 8–14 层，delay 递增到 ~1.3
```
3. API（core.py）：R C E P S poly G T、`s.lg`/`s.rg`/`s.clip`、cloud blob_tree pine beam；阴影 `extra='filter="url(#sh)"'`（弱 `#shs`）；`depth` 0 远 ~ 1 近（视差）。入场：fade rise drop pop grow slide-l slide-r zoom；循环：drift sway bob twinkle flow swing glow fall flicker smoke。
4. `python3 engine/render.py scenes_cXX` → 看 PNG → 改到满意。多人并行时各改各的模块，最后一人跑全量 render + build_gallery。

**验收清单**
- [ ] 平面正视；无透视房间、塑料高光、写实纹理、厚重暗角。
- [ ] 地面线 y 760–900（讲解台/特殊外景可到 930，写准 stand）；有清晰站位地面；y 950–1060 不放关键物件。
- [ ] 一个记忆点主体 + 4–8 个小道具；结构按真实比例；基本无文字。
- [ ] 8–14 层、2–4 层循环；颜色全走 palette；不撞已有构图和配色。
- [ ] **自评 ≥85/100**：缩小拼总览图与样板对比。

## 10. 附录：主题示例（示例，不是默认）
- **秋季防火**（c11 s101–s105：护林瞭望塔、秸秆禁烧、银杏校园、取暖用电客厅、金秋消防站）：户外加 `fx` `leaves`；其他户外场景 `"theme":"autumn"`（s083 绿树写死，不用）；隐患 `flame`+`stamp` 红叉，正确做法绿勾或 `focus`；台词带季节特色。
- **古诗《山行》**（s106 秋山枫林）：`"theme":"maple:t1,t2,t3,t4,far,far2"` 只把树叶转枫红；朗读用 `board`（`cross:false`，`times` 对齐每句朗读，末句 `!` 强调）；开场 crane_up 沿石径升到人家，「白云生处」snap_zoom，「停车坐爱」drift。

## 11. 已知局限 + 路线
- 场景弱项见 `ROADMAP.md` A3。
- 人物是贴图，无骨骼动作，姿势靠多张底图切换（`poses`）；rig.py 只适合正面、嘴眼清晰的扁平角色；talk 时段是 tts.py 的能量 VAD（到句内停顿），无逐字口型；渲染慢（§8）。
- `reference/scenes.json` 是全部场景的元数据总表（render 后以 `engine/out/scenes.json` 为准）。
- **路线**（详见 `ROADMAP.md`）：内容插槽 slot（黑板/屏幕可填题）、共用道具库 props.py、昼夜/天气按层变体、前景遮挡层、竖屏 9:16 和分层 PNG 导出。
