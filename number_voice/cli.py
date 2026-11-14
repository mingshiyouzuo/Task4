"""UI界面"""
from .audio import AudioStore
from .config import TOKEN_FILES
from .numbers import READING_MODES


def read_text(prompt="请输入数字："):
    return input(prompt).strip()


def choose_mode():
    print("选择读法：1. 数值读法 2. 逐位读法")
    choice = input("请选择【1-2】：").strip()
    if choice == "2":
        return "逐位读法"
    return "数值读法"


def show_reading(text, mode):
    tokens = READING_MODES[mode](text)
    print("读法：", "".join(tokens))
    print("字音顺序：", "/".join(tokens))
    return tokens


def print_file_list(store):
    for index, token in enumerate(TOKEN_FILES, 1):
        state = "已准备" if store.path(token).is_file() else "缺失"
        print(f"{index:2d}. {token} [{state}]")
    missing = store.missing(list(TOKEN_FILES))
    print("缺失：", "、".join(missing) if missing else "无")


def choose_token(store):
    print_file_list(store)
    value = input("请输入序号").strip()
    tokens = list(TOKEN_FILES)
    if not value.isdigit() or not 1 <= int(value) <= len(tokens):
        raise ValueError("序号超出范围")
    return tokens[int(value) - 1]


def preview_token(store):
    try:
        token = choose_token(store)
        store.play(token)
    except (ValueError, IndexError) as e:
        print("试听失败：", e)


def play_number(store):
    text = read_text()
    mode = choose_mode()
    try:
        tokens = show_reading(text, mode)
        store.play(tokens)
    except (ValueError, RuntimeError) as e:
        print("无法播放：", e)


# 主函数
def main():
    store = AudioStore()
    print("数字录音播放器")
    while True:
        print("\n1. 查看读法")
        print("2. 播放数字")
        print("3. 查看录音文件状态")
        print("4. 试听单字")
        print("5. 退出")
        choice = input("请选择【1-5】：").strip()
        if choice == "1":
            try:
                show_reading(read_text(), choose_mode())
            except ValueError as e:
                print("输入错误：", e)
        elif choice == "2":
            play_number(store)
        elif choice == "3":
            print_file_list(store)
        elif choice == "4":
            preview_token(store)
        elif choice == "5":
            print("再见。")
            break
        else:
            print("输入有误，请重新选择")
