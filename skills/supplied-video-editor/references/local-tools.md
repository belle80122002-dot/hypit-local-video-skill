# EDL �뱾�ع���

������Python 3.10+��FFmpeg/FFprobe���� libx264 �� libass����һ���Ѱ�װ���������塣��ѡ���ֽű�����Ҫ NumPy���ű���������������ģ�ͣ����Զ���װ�κ�������

ʾ�� `examples/edit-plan.json` �ڱ� Skill Ŀ¼����������ʾʱ��㣻�뻻��ʵ���زġ�·����� EDL �ļ�����Ŀ¼����ʹ�þ���·������Ҫ���Լ�����Ƶ����Կ�ύ���˲ֿ⡣

```json
{
  "title": "һ�����ӣ�����������",
  "tag": "���ӹ۲�Ա",
  "width": 720, "height": 1280, "fps": 30,
  "font": "Microsoft YaHei",
  "sources": {"a": "source1.mp4", "b": "source2.mp4"},
  "clips": [{"source":"b", "start":34.6, "end":37.0, "caption":"һ�����ӣ�\n����������", "hook":true}],
  "source_gain": 1.0,
  "music": {"path":"music.wav", "gain":1.0}
}
```

Windows �������� `Microsoft YaHei`��Linux ���� `Noto Sans CJK SC`��macOS �����Ѱ�װ�� `PingFang SC`������ȷ��ʵ��������ֲ�ȱ�֡�`caption` �Ǵ��ı��������� ASS ���ƴ��룻`hook` ����Ļ�����Ϸ���������ĻĬ�����·���ȫ����

��ѡ���������ֲݸ壨Ĭ��ֻ�ʺ�������Ƥ���ݣ���

```sh
python skills/supplied-video-editor/scripts/make_music.py --duration 34.2 --output my-project/music.wav
```

��׼�� EDL ���زģ��ٵ�����һ��**�����ڵ���Ŀ¼**��

```sh
python skills/supplied-video-editor/scripts/edit_video.py --edl my-project/edit-plan.json --output my-project/review-v1
```

��� `preview.mp4`��`original-sound.mp4`��`cover.jpg`��`preview.html`��`report.json` ���ɸ������Ļ/Ƭ�Ρ�δ�ṩ music ʱ preview ����ԭ����������ԭƬ�Ჹ�����죬����ƴ�ӡ�

�ű�ͳһ CFR �ͻ������ȱ��������ߣ������Զ�׷�����������ȥ�ء����������� EDL ��Ӳ�У���Ļ��¼��ԭ����Ҳ������ͬ��Ļ���ֶ��ر������ƴ�ӣ���Ƶ���뵭�����ܵ���΢С�߽���죬�貥�ż�顣�����ȹ�һ�� -18 LUFS �ٰ� gain ���ţ��ڲ�����ӽ�С gain �𲽣���ʵ�����������

����Ԥ����鿴 ffprobe ���ݡ����������������ȼ�飻�������� ended �¼�ֻ֤���������ųɹ�������֤���������кá�

## ���׼���

[������ͼ](editing-techniques.md)ָ������ѡ�������[ִ��˵��](execution-recipes.md)�������нű���������ʵ�ֵĴ�������ǰ EDL û�� transition��speed��broll��ducking�����������������ֶΣ�δ֪�ֶο��ܱ����ԡ������������ֶδ�������ʵ�֡����׾���ʹ�ö����ļ������߱��������Ӧ���ع��̺��ٱ�Ϊ��ִ�С�
