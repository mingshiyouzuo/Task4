"""这里存放项目配置：比如录音路径、音频参数、文件名等"""
import sys
from pathlib import Path

# 源码运行时取项目根目录；PyInstaller 打包后取可执行文件所在目录
if getattr(sys, "frozen", False):
    PROJECT_DIR = Path(sys.executable).resolve().parent
else:
    PROJECT_DIR = Path(__file__).resolve().parent.parent

RECOGNIZE_DIR = PROJECT_DIR / "recordings"

# 音频设置
SAMPLE_RATE = 22050  # 每秒采样次数，如果要能直接采用手机录音，建议用44100
CHANNELS = 1  # 单声道
SAMPLE_WIDTH = 2  # 每次采样2字节，也就是位深16位

# 字符与音频的对应关系
TOKEN_FILES = dict(
    zip(
        "零一二三四五六七八九十百千万亿兆京",
        ("ling",
         "yi",
         "er",
         "san",
         "si",
         "wu",
         "liu",
         "qi",
         "ba",
         "jiu",
         "shi",
         "bai",
         "qian",
         "wan",
         "yi_large",
         "zhao",
         "jing",
         ),
    )
)

# 特殊符号的处理
TOKEN_FILES["负"] = "fu"
TOKEN_FILES["点"] = "dian"
