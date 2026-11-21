# CHANGELOG

版本号写在 `VERSION`。每次发布在最上面加一段 `## x.y.z — 日期`。

## 1.0.0 — 2026-11-21

首个 GitHub 发布版。
- 112 个分层矢量场景（c01–c12，含季节专题 s101–s106、通用讲解台/答题台 s111–s116）
- compose.py 成片：口型同步与眨眼（rig.py）、33 种运镜 + 27 种转场、知识点卡片、「考考你」答题、分角色配音（tts.py）
- assemble.py 总装（进度条标出考考你、章节、配乐），interactive.py 互动做题网页版
- lint.py 自动检查硬规则，doctor.py 检查环境
- 新增 engine/update.py：启动时检查 GitHub 上的新版本，经同意后更新
