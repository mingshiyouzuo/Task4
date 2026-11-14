"""这里存放项目配置：比如录音路径、音频参数、文件名等"""
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
RECOGNIZE_DIR = PROJECT_DIR / "recordings"

# 音频设置
SAMPLE_RATE = 22050  # 每秒采样次数
CHANNELS = 1  # 单声道
SAMPLE_WIDTH = 2  # 每次采样2字节
CLIP_SECONDS = 1.2  # 每段录音1.2秒

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

TOKEN_FILES["负"] = "fu"
TOKEN_FILES["点"] = "dian"
