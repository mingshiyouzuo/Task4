from number_voice.audio import AudioStore
from number_voice.numbers import number_tokens

text = input("请输入数字：")
try:
    tokens = number_tokens(text)
    print("读法：" + "".join(tokens))
    AudioStore().play(tokens)
except ValueError as e:
    print("无法播放：", e)
