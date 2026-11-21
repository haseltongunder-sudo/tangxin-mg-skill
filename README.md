# tangxin-mg-skill · 平面 MG 教学动画

给 AI 助手用的技能（Skill）：任何学科、任何主题的平面 MG 教学动画，从场景、师生出镜、配音口型、运镜转场、「考考你」答题，到总装成片和互动做题网页。

## 安装
1. 点本页绿色 **Code → Download ZIP**，或 `git clone https://github.com/haseltongunder-sudo/tangxin-mg-skill.git`
2. 把解压后的文件夹改名为 `tangxin-mg-skill`，放进所用工具的技能目录（里面直接能看到 `SKILL.md`）。
3. 安装依赖：`pip install -r requirements.txt`，再运行 `python engine/doctor.py` 检查环境。

## 更新
技能每次被使用时会先运行 `python engine/update.py` 检查这里的 `VERSION`。有新版本时，助手会告诉你更新了什么，**问过你之后**才运行 `python engine/update.py --apply` 更新。你自己生成的 `out/` 等内容不会被覆盖。

也可以随时手动：重新下载 ZIP 覆盖，或在仓库目录里 `git pull`。

## 文件
- `SKILL.md` 用法和硬规则（助手读这个）
- `STYLE.md` 场景编号表和画风
- `engine/` 引擎脚本；`examples/` 场景 SVG、示例流程
- `VERSION` 当前版本；`CHANGELOG.md` 更新记录
