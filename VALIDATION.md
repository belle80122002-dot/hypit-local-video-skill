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
## Editing craft expansion — 2026-09-22

- Added 72 uniquely numbered entries in six categories; each row includes purpose/material requirements, editing action, failure check and execution level.
- Added 10 footage playbooks, a decision-record template, and concrete J/L, B-roll, overlap-duration and retiming examples.
- Referenced 24 primary documentation sources. This is broad coverage of everyday supplied-footage editing, not a claim to cover every specialty or commercial effect.
- Skill frontmatter validation passed; all local Markdown links in the companion and README resolve; all playbook technique IDs exist.
- All 73 upstream Skill files still match UPSTREAM.json. No official Hypit file or rendering script was changed in this expansion.
- Reviewed the documented decision paths: full talking-head keeps effective statements; pet footage uses actual action/reaction; tutorials preserve required steps; multicam requires synchronization; absent handles reject unsuitable transitions; low-frame-rate footage does not promise clean extreme slow motion.
- These are documentation and workflow checks. The advanced techniques have NOT all been rendered or visually/audibly tested by this update; the earlier basic-script tests do not establish advanced effect support.
- The basic EDL runner has no J/L, transition, speed, tracking, B-roll overlay or automatic-ducking fields. Advanced operations require a separately implemented and verified local composition as explained in execution-recipes.md.
