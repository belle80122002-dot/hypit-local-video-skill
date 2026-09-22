# EDL 与本地工具

依赖：Python 3.10+、FFmpeg/FFprobe（含 libx264 和 libass）、一个已安装的中文字体。可选器乐脚本还需要 NumPy。脚本不联网，不调用模型，不自动安装任何依赖。

示例 `examples/edit-plan.json` 在本 Skill 目录，仅包含演示时间点；请换成实际素材。路径相对 EDL 文件所在目录，或使用绝对路径。不要把自己的视频或密钥提交进此仓库。

```json
{
  "title": "一个杯子，把它拿捏了",
  "tag": "杯子观察员",
  "width": 720, "height": 1280, "fps": 30,
  "font": "Microsoft YaHei",
  "sources": {"a": "source1.mp4", "b": "source2.mp4"},
  "clips": [{"source":"b", "start":34.6, "end":37.0, "caption":"一个杯子，\n把它拿捏了", "hook":true}],
  "source_gain": 1.0,
  "music": {"path":"music.wav", "gain":1.0}
}
```

Windows 常见字体 `Microsoft YaHei`；Linux 可用 `Noto Sans CJK SC`；macOS 可用已安装的 `PingFang SC`。必须确认实际输出汉字不缺字。`caption` 是纯文本，不接收 ASS 控制代码；`hook` 把字幕放在上方，其他字幕默认在下方安全区。

可选：生成器乐草稿（默认只适合轻松俏皮内容）：

```sh
python skills/supplied-video-editor/scripts/make_music.py --duration 34.2 --output my-project/music.wav
```

先准备 EDL 与素材，再导出到一个**不存在的新目录**：

```sh
python skills/supplied-video-editor/scripts/edit_video.py --edl my-project/edit-plan.json --output my-project/review-v1
```

输出 `preview.mp4`、`original-sound.mp4`、`cover.jpg`、`preview.html`、`report.json` 及可复查的字幕/片段。未提供 music 时 preview 仅有原声。无音轨原片会补静音轨，便于拼接。

脚本统一 CFR 和画布、等比适配留边，不会自动追踪主体或语音去重。它按已审阅 EDL 做硬切，字幕烧录；原声版也保留相同字幕。分段重编码后再拼接，音频淡入淡出可能导致微小边界差异，需播放检查。音乐先归一至 -18 LUFS 再按 gain 缩放；口播建议从较小 gain 起步，依实测混音调整。

生成预览后查看 ffprobe 数据、运行完整解码和响度检查；播放器的 ended 事件只证明技术播放成功，不能证明音乐听感好。
