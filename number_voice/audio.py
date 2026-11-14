"""检查WAV录音，不使用TTS"""
import wave
from pathlib import Path

from .config import RECOGNIZE_DIR, TOKEN_FILES, SAMPLE_RATE, CHANNELS, SAMPLE_WIDTH


# 加载设备
def load_sounddevice():
    """在需要的时候才加载"""
    try:
        import sounddevice
    except (ImportError, OSError) as e:
        raise RuntimeError("无法加载sounddevice,请按README安装音频依赖") from e
    return sounddevice


# 查找录音
class AudioStore:
    def __init__(self, directory=RECOGNIZE_DIR, device_factory=load_sounddevice):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self._device_factory = device_factory

    def path(self, token: str) -> Path:
        return self.directory / (TOKEN_FILES[token] + ".wav")

    def missing(self, tokens):
        return list(dict.fromkeys(token for token in tokens if not self.path(token).is_file()))

    # 播放音频
    def play(self, tokens) -> None:
        missing = self.missing(tokens)
        if missing:
            raise ValueError("请先准备录音文件：" + "、".join(missing))
        device = self._device_factory()
        with device.RawOutputStream(
                samplerate=SAMPLE_RATE, channels=CHANNELS, dtype="int16"
        ) as stream:
            for token in tokens:
                with wave.open(str(self.path(token)), "rb") as clip:
                    if (clip.getnchannels(), clip.getsampwidth(),
                        clip.getframerate()) != (
                            CHANNELS,
                            SAMPLE_WIDTH,
                            SAMPLE_RATE,
                    ):
                        raise ValueError(f"录音{token}的格式不符，请转换为{SAMPLE_RATE}Hz,单声道、16位WAV")
                    while True:
                        data = clip.readframes(2048)
                        if not data:
                            break
                        stream.write(data)
