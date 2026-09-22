# Validation — 2026-09-22

- Both Skill entrypoints passed skill-creator quick_validate.py.
- 73 files in skills/hypit match the SHA-256 manifest of upstream commit 56057fd0c1b6ed6898b0c591d97f85b6e6472e85.
- On Windows, a real FFmpeg run joined a 30fps vertical clip with audio and a 24fps horizontal clip without audio into a 4-second 360×640 30fps H.264/AAC MP4. Padding preserved the horizontal picture.
- Local instrumental generation, music mixing, ASS Chinese subtitles, cover extraction, HTML preview and full MP4 decode passed. A rendered Chinese-title frame was visually inspected.
- A second 1.1-second silent-video test without music completed and decoded successfully.
- Personal source videos, audio, keys, runtime profiles, account identifiers and local workstation paths are not bundled. Tests used generated test patterns outside the repository.
- The original production workflow was exercised on a 34.2-second, 720×1280, 30fps real video; full browser playback and the Hypit Studio composition were verified. This does not imply every future EDL will have good pacing or music.
- Linux/macOS have not been tested. Chinese font availability and FFmpeg build capabilities must be checked on each machine.
- Technical decode and loudness checks do not replace listening. Human review of actual footage, captions and music remains part of the Skill.