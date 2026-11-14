"""检查文件是否齐全的脚本"""

from number_voice.audio import AudioStore
from number_voice.config import TOKEN_FILES

store = AudioStore()
missing = store.missing(list(TOKEN_FILES))
if missing:
    print("缺少：", "、".join(missing))
else:
    print(f"{len(TOKEN_FILES)}个文件齐全。")
