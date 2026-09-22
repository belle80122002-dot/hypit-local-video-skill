"""Render an inspected edit decision list locally; Python standard library + FFmpeg."""
import argparse, html, json, math, shutil, subprocess
from pathlib import Path


def command(args, cwd=None):
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if result.returncode:
        raise RuntimeError(f'{args[0]} failed: {result.stderr[-3500:]}')
    return result.stdout


def probe(path):
    return json.loads(command(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)]))


def timestamp(seconds):
    cs = round(seconds * 100)
    return f'{cs//360000}:{cs//6000%60:02}:{cs//100%60:02}.{cs%100:02}'


def plain(text):
    return str(text).replace('\\', '／').replace('{', '｛').replace('}', '｝').replace('\r', '').replace('\n', r'\N')


def finite(value, name, minimum=0):
    x = float(value)
    if not math.isfinite(x) or x < minimum:
        raise ValueError(f'Invalid {name}: {value}')
    return x


def run(edl_path, output):
    for executable in ('ffmpeg', 'ffprobe'):
        if not shutil.which(executable):
            raise RuntimeError(f'Install {executable} and put it on PATH first')
    edl_path = edl_path.resolve()
    plan = json.loads(edl_path.read_text(encoding='utf-8-sig'))
    base = edl_path.parent
    width, height, fps = (int(plan.get(k, d)) for k, d in [('width', 720), ('height', 1280), ('fps', 30)])
    if not (width > 0 and height > 0 and width % 2 == 0 and height % 2 == 0 and 1 <= fps <= 120):
        raise ValueError('Use positive even width/height and 1–120 fps')
    font = plan.get('font', 'Microsoft YaHei')
    if not isinstance(font, str) or any(c in font for c in ',\r\n'):
        raise ValueError('font must be an installed font family name without commas or line breaks')
    sources = {k: (base / v).resolve() for k, v in plan['sources'].items()}
    metadata = {k: probe(p) for k, p in sources.items()}
    clips = plan['clips']
    if not clips:
        raise ValueError('clips must not be empty')
    durations = []
    for clip in clips:
        info = metadata[clip['source']]
        if not any(s['codec_type'] == 'video' for s in info['streams']):
            raise ValueError('Every selected source must have a video stream')
        start, end = finite(clip['start'], 'start'), finite(clip['end'], 'end')
        if end <= start or end > float(info['format']['duration']) + 0.02:
            raise ValueError(f'Invalid source interval: {start}–{end}')
        duration = round((end - start) * fps) / fps
        if duration < 0.2:
            raise ValueError('Each clip must be at least 0.2 seconds')
        durations.append(duration)
    source_gain = finite(plan.get('source_gain', 1), 'source_gain')
    music = plan.get('music')
    if music:
        music_path = (base / music['path']).resolve()
        if not any(s['codec_type'] == 'audio' for s in probe(music_path)['streams']):
            raise ValueError('Music must contain audio')
        music_gain = finite(music.get('gain', 1), 'music.gain')
    # A fresh folder avoids replacing inputs or silently overwriting a prior edit.
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    (output / 'clips').mkdir()
    (output / 'subtitles').mkdir()
    scale = width / 720
    styles = f'''[Script Info]
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}
WrapStyle: 2
ScaledBorderAndShadow: yes
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Main,{font},{round(38*scale)},&H00E7FFFF,&H00FFFFFF,&H00251C15,&H80000000,-1,0,0,0,100,100,0,0,1,{2.5*scale},1,2,{round(60*scale)},{round(80*scale)},{round(height*.184)},1
Style: Hook,{font},{round(49*scale)},&H00E7FFFF,&H00FFFFFF,&H00251C15,&H80000000,-1,0,0,0,100,100,0,0,1,{3*scale},1,8,{round(65*scale)},{round(80*scale)},{round(height*.109)},1
Style: Tag,{font},{round(21*scale)},&H00FFFFFF,&H00FFFFFF,&H50251C15,&H80000000,0,0,0,0,100,100,0,0,1,1.5,0,7,{round(36*scale)},{round(36*scale)},{round(height*.05)},1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
    for index, (clip, duration) in enumerate(zip(clips, durations)):
        ass = styles
        if plan.get('tag'):
            ass += f'Dialogue: 0,0:00:00.00,{timestamp(duration)},Tag,,0,0,0,,{plain(plan["tag"])}\n'
        if clip.get('caption'):
            style = 'Hook' if clip.get('hook') else 'Main'
            ass += f'Dialogue: 1,0:00:00.03,{timestamp(duration-.03)},{style},,0,0,0,,{{\\fad(60,60)}}{plain(clip["caption"])}\n'
        (output / f'subtitles/{index:03}.ass').write_text(ass, encoding='utf-8-sig')
        src = clip['source']
        has_audio = any(s['codec_type'] == 'audio' for s in metadata[src]['streams'])
        args = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-ss', str(clip['start']), '-i', str(sources[src])]
        if not has_audio:
            args += ['-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo']
        vf = f'fps={fps},scale={width}:{height}:force_original_aspect_ratio=decrease:force_divisible_by=2,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=0x151812,setsar=1,ass=subtitles/{index:03}.ass'
        af = f'highpass=f=80,afade=t=in:d=0.025,afade=t=out:st={duration-.04}:d=0.04,apad'
        args += ['-map', '0:v:0', '-map', '0:a:0' if has_audio else '1:a:0', '-t', str(duration), '-vf', vf, '-af', af, '-c:v', 'libx264', '-preset', 'fast', '-crf', '19', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2', '-movflags', '+faststart', f'clips/{index:03}.mp4']
        command(args, output)
        print(f'Prepared clip {index+1}/{len(clips)}', flush=True)
    total = sum(durations)
    (output/'concat.txt').write_text('\n'.join(f"file 'clips/{i:03}.mp4'" for i in range(len(clips))), encoding='utf-8')
    ff = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y']
    command(ff + ['-f', 'concat', '-safe', '0', '-i', 'concat.txt', '-t', str(total), '-c', 'copy', '-movflags', '+faststart', 'original-sound.mp4'], output)
    args = ff + ['-i', 'original-sound.mp4']
    if music:
        command(ff + ['-stream_loop', '-1', '-i', str(music_path), '-t', str(total), '-af', f'loudnorm=I=-18:TP=-2:LRA=7,afade=t=in:d=0.15,afade=t=out:st={max(0,total-1.1)}:d=1.1', '-ar', '48000', 'music-mix.wav'], output)
        args += ['-i', 'music-mix.wav', '-filter_complex', f'[0:a]volume={source_gain}[a];[1:a]volume={music_gain}[b];[a][b]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.89:level=false[m]', '-map', '0:v:0', '-map', '[m]']
    else:
        args += ['-af', f'volume={source_gain},alimiter=limit=0.89:level=false']
    command(args + ['-t', str(total), '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', 'preview.mp4'], output)
    command(ff + ['-i', 'preview.mp4', '-ss', str(min(.9,total/2)), '-frames:v', '1', '-q:v', '2', 'cover.jpg'], output)
    title = html.escape(plan.get('title', '视频预览'))
    (output/'preview.html').write_text(f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>body{{background:#101713;color:#faf5e3;font:18px system-ui;text-align:center;margin:24px}}video{{max-width:100%;max-height:76vh;border-radius:16px}}a{{color:#e4ed9d;margin:10px;display:inline-block}}</style><h1>{title}</h1><video controls playsinline preload="metadata" src="preview.mp4" poster="cover.jpg"></video><p><a href="preview.mp4" download>下载 MP4</a><a href="original-sound.mp4" download>无新增配乐版</a><a href="cover.jpg" download>封面</a></p><p>请检查字幕、切口及配乐听感。</p></html>''', encoding='utf-8')
    command(['ffmpeg', '-v', 'error', '-i', 'preview.mp4', '-f', 'null', '-'], output)
    report = {'duration_requested':total, 'metadata':probe(output/'preview.mp4'), 'full_decode':'passed', 'visual_review':'required', 'audio_listening':'required', 'edl':plan}
    (output/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Ready: {output / "preview.html"}')

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--edl',required=True,type=Path)
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    run(args.edl,args.output)