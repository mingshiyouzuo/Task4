# recordings 目录说明

本目录存放**外部录制**的 19 个单字 WAV 文件。程序不提供录音界面，只负责检查并播放这些文件。WAV 不提交到 Git；请不要把个人录音提交到公开仓库。

当前 19 个 WAV 已按 22050 Hz、单声道、16 位转换，并裁剪了首尾静音。原始 M4A 保留在 `original_m4a/`，程序不读取该子目录。

## 文件格式

统一使用：

```text
22050 Hz、单声道、16 位 PCM WAV
```

如果原文件是手机常见的 44.1 kHz 立体声，可以用 ffmpeg 转换：

```bash
ffmpeg -i input.m4a -ar 22050 -ac 1 -sample_fmt s16 recordings/er.wav
```

也可以用 Audacity 导出为“WAV (Microsoft) signed 16-bit PCM”，采样率 22050，声道单声道。

## 文件对照表

| 汉字 | 文件名 | 汉字 | 文件名 |
| --- | --- | --- | --- |
| 零 | `ling.wav` | 一 | `yi.wav` |
| 二 | `er.wav` | 三 | `san.wav` |
| 四 | `si.wav` | 五 | `wu.wav` |
| 六 | `liu.wav` | 七 | `qi.wav` |
| 八 | `ba.wav` | 九 | `jiu.wav` |
| 十 | `shi.wav` | 百 | `bai.wav` |
| 千 | `qian.wav` | 万 | `wan.wav` |
| 亿 | `yi_large.wav` | 兆 | `zhao.wav` |
| 京 | `jing.wav` | 负 | `fu.wav` |
| 点 | `dian.wav` |  |  |

程序只检查文件是否存在以及格式是否匹配；文件内容是否清晰、是否需要裁剪静音，由录制者自行决定。
