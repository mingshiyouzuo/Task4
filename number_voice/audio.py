"""检查WAV录音，不使用TTS"""
import wave
from pathlib import Path

from .config import RECOGNIZE_DIR, TOKEN_FILES, SAMPLE_RATE, CHANNELS, SAMPLE_WIDTH


# 在真正要播放时才导入 sounddevice，导入失败就把错误换成一条中文提示
def load_sounddevice():
    """在需要的时候才加载"""
    try:
        import sounddevice
    except (ImportError, OSError) as e:
        raise RuntimeError("无法加载sounddevice,请按README安装音频依赖") from e
    return sounddevice


# 定义类AudioStore，负责与播放有关的实现
class AudioStore:
    # 构造函数
    def __init__(self, directory=RECOGNIZE_DIR, device_factory=load_sounddevice):
        self.directory = Path(directory)  # 设定音频的根路径
        self.directory.mkdir(parents=True, exist_ok=True)  # 目录不存在就创建，已存在不报错
        self._device_factory = device_factory  # 加载函数

    # 查找字对应的音频的路径，以便play()去播放
    def path(self, token: str) -> Path:
        return self.directory / (TOKEN_FILES[token] + ".wav")

    # 素材完整性检查，返回缺失的字的列表
    def missing(self, tokens):
        result = []
        for token in tokens:
            if not self.path(token).is_file():  # 如果字对应的音频文件不存在
                if token not in result:  # 去重
                    result.append(token)  # 保序
        return result

    # 播放音频函数
    def play(self, tokens) -> None:
        missing = self.missing(tokens)  # 如果缺文件就跳出异常
        if missing:
            raise ValueError("请先准备录音文件：" + "、".join(missing))

        # 加载设备
        device = self._device_factory()

        # 打开原始音频流
        with device.RawOutputStream(
                samplerate=SAMPLE_RATE, channels=CHANNELS, dtype="int16"  # 每 2 字节一帧样本，单声道、22050Hz
        ) as stream:
            # 每个 token 一个独立文件，按读法顺序依次打开，这就是“拼句”的方式
            for token in tokens:
                with wave.open(str(self.path(token)), "rb") as clip:
                    if (clip.getnchannels(), clip.getsampwidth(),  # 如果单个音频对应的属性和config规定的不同
                        clip.getframerate()) != (
                            CHANNELS,
                            SAMPLE_WIDTH,
                            SAMPLE_RATE,
                    ):
                        raise ValueError(f"录音{token}的格式不符，请转换为{SAMPLE_RATE}Hz,单声道、16位WAV")
                    # 读 2048 帧，22050Hz 下约 93 毫秒一块
                    while True:
                        data = clip.readframes(2048)
                        if not data:
                            break
                        stream.write(data)  # 阻塞式的：输出缓冲满时会等待，实现边播边读
