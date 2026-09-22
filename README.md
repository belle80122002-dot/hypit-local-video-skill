# Hypit 本地视频精剪 Skill 分享包

把自己的实拍素材交给 AI 助手：分析内容 → 找出亮点 → 删除重复与等待 → 编排节奏 → 中文字幕与配乐 → 预览 → MP4。

这是一个**非官方分享包**，源于一次两段鹦鹉实拍素材剪成 34 秒竖屏短片的实际工作流。它包含官方 Hypit Skill 的固定版本，以及整理后的现有素材精剪配套 Skill。没有附带私人视频、账号配置或 API Key，也不保证所谓“爆款”播放量。

## 里面有什么

| 内容 | 作用 |
| --- | --- |
| `skills/hypit` | 官方 Hypit Skill，73 个文件保持原样，负责 Hypit 制片、Author / Run / Runtime 和 Studio 工作流 |
| `skills/supplied-video-editor` | 配套中文 Skill，聚焦实拍素材分析、精剪、口播去重、字幕、配乐和交付 |
| `scripts/edit_video.py`（在配套 Skill 内） | 根据人工/AI 看过后确定的 EDL，本地拼接、适配竖屏、烧录字幕、混音和生成预览 |
| `scripts/make_music.py`（在配套 Skill 内） | 可选的轻快器乐草稿生成器，纯本地计算 |
| `skills/supplied-video-editor/examples/edit-plan.json` | 去掉私人素材后的 34.2 秒剪辑计划示例，需替换成自己的源文件 |

## 原素材剪辑技法库

配套 Skill 现含 **72 项技法、6 类参考文档和 10 类素材选用方案**，每项包含用途、素材条件、剪法、失败检查和执行路径。

- 剪接与连续性 16 项：自然硬切、动作衔接、视线衔接、插入/切出、反应、多机位等。
- 叙事与结构 12 项：结果先行、因果链、交叉剪辑、过程蒙太奇、章节与呼应等。
- 节奏与时间 10 项：语义呼吸、动作节奏、卡点、留白、慢放、速度坡度等。
- 声音 12 项：J/L cut、环境底声、主音轨、音乐让位、音效与收尾等。
- 转场与合成 12 项：叠化、遮挡、甩镜、匹配、画中画、分屏、遮罩等。
- 画面整理 10 项：重构图、稳定、校色、字幕、标注与封面等。

从 [技法地图](skills/supplied-video-editor/references/editing-techniques.md) 进入，或直接看 [按素材选剪法](skills/supplied-video-editor/references/footage-playbooks.md)。[研究来源](skills/supplied-video-editor/references/research-sources.md)列出 24 份官方资料，检索日期为 2026-09-22；不宣称收齐所有流派和商业效果。

**这是助手的剪辑工作库，不是脚本新增了 72 个自动功能。** 基础脚本仍负责硬切、字幕和固定混音；J/L、变速、合成等需助手另行制作可验证的本地时间线/处理。[执行说明](skills/supplied-video-editor/references/execution-recipes.md)提供具体时码例子与能力边界。

你可以说：

> 使用 supplied-video-editor，先分析我的原素材，选出适合的剪辑手法，记录关键切点的理由，再剪出自然、有重点的版本。不要为了效果堆转场；只使用现有素材，先给我预览。

## 给朋友的安装方式

在支持 Agent Skills 的 Codex / Claude Code 等工具环境中，可运行：

```sh
npx skills add belle80122002-dot/hypit-local-video-skill -g
```

按提示选择 `hypit` 和 `supplied-video-editor`，以及实际使用的 AI 助手。已有官方 `hypit` 时可以只选配套 Skill，不必覆盖已有版本。

也可以把本仓库链接发给你的 AI 助手，并说：

> 请安装这个仓库的 supplied-video-editor Skill；如果没有 Hypit Skill，也安装里面的 hypit。检查本地依赖后再开始，不要调用收费生成模型。

手动安装时，将 `skills/` 内的对应文件夹复制到你的 Agent 的技能目录；不要仅复制一个 SKILL.md，引用文档和脚本也要一起保留。更新后可能需要开启新会话才能发现 Skill。

## 直接这样调用

**萌宠 / 日常素材**

> 使用 $supplied-video-editor，先分析这两段我自己拍的视频，剪成一条有趣的竖屏短片，发抖音和视频号。加中文字幕和合适的配乐，保留关键原声。只用现有素材，先给我预览。

**完整版口播去重**

> 使用 $supplied-video-editor，保留这条口播的完整有效内容，删掉重读、卡壳和无效停顿，让前后语气自然衔接。不要强行压成 30 秒。

**使用 Hypit 时间线**

> 使用 $hypit 和 $supplied-video-editor，为这次精剪保留可修改的 Hypit 时间线，用 Studio 预览。复用已经准备好的素材，不重复生成。

Skill 是给 AI 助手的工作指导，不是一个自动保证效果的视频网站。模型负责看素材和做判断，脚本执行已经确定的剪辑计划。

## 运行条件与费用

- 本地精剪：Python 3.10+、FFmpeg / FFprobe（含 libx264、libass）、可用的中文字体。
- 可选器乐草稿：NumPy。已有环境优先复用；缺失时可安装 `numpy`。
- Hypit Studio：需要另行安装 Hypit 可执行程序及其运行依赖。安装 Skill 不等于装好了 CLI。
- 本地剪辑脚本不会联网，也不请求生成 API；AI 助手订阅、本地算力和用户另行选择的模型服务有各自成本。
- 如确实需要新生成镜头或云端配音，应另行选择服务、确认费用与授权。不要把 API Key 发到公开仓库。

本次实际环境验证了 Hypit CLI 0.2.10。需要 CLI 时先让助手检查现有安装，再按官方安装说明准备；不是要求复制作者电脑的盘符或缓存。

更多本地执行和 EDL 说明见 [local-tools.md](skills/supplied-video-editor/references/local-tools.md)。

## 验证范围

- 原始案例：9 个片段、34.2 秒、720×1280、30fps，中文字幕、器乐配乐、原声版、封面及 HTML 预览；实际完整解码和浏览器播放通过，Hypit Studio 时间线可见。
- 分享脚本：在 Windows 上以合成素材测试有音轨/无音轨、横屏/竖屏适配、中文 ASS 字幕、配乐与 MP4 全片解码。验证记录见 [VALIDATION.md](VALIDATION.md)。
- 脚本使用可移植的 Python 与 FFmpeg 命令；Linux/macOS 尚未实机验证，中文字体名需按实际机器调整。
- 字幕、节奏、构图和音乐听感仍应预览判断。自动解码通过不等于人工试听完成。
- MP4 示例工作流是 FFmpeg 导出；Hypit Studio 预览成功不冒充原生 Hypit 最终渲染成功。

## 来源与许可证

官方来源：[hypit-ai/hypit](https://github.com/hypit-ai/hypit)。保留版本提交：`56057fd0c1b6ed6898b0c591d97f85b6e6472e85`（0.2.10）。完整的官方 Skill 文件 SHA-256 记录在 [UPSTREAM.json](UPSTREAM.json)，用于确认副本未改动。

本分享包按随附 [LICENSE](LICENSE) 提供，保留 Hypit 官方版权与附加条件。它是带附加条件的 Apache 2.0 许可，不能当作无附加条件的 Apache 2.0。托管多租户服务、收费转售/商业再分发等场景请查看原文。此仓库分享不代表 Hypit 官方背书。