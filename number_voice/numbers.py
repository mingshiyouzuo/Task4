from typing import Tuple, Optional, List, Dict, Callable

DIGITS = "零一二三四五六七八九"
SMALL_UNITS = ("", "十", "百", "千")
GROUP_UNITS = ("", "万", "亿", "兆", "京")
MAX_DIGITS = 20


# 校验输入是否合法
def _parse(text: str) -> Tuple[str, str, Optional[str]]:
    """分割可选的负号、整数部分和小数部分"""
    if not text:
        raise ValueError("请输入数字，比如2382,-23或者12.34")
    sign = ""
    body = text
    if text.startswith("-"):  # 如果开头是负号，就提取出来
        sign = "-"
        body = text[1:]
    if not body:
        raise ValueError("负号后面必须有数字")
    if body.count(".") > 1:
        raise ValueError("小数点只能出现一次")
    integer, dot, fraction = body.partition(".")
    if dot and not fraction:
        raise ValueError("小数点后面必须有数字")
    if not (integer or dot):
        raise ValueError("请输入数字")
    digits = integer + fraction  # 整数+小数部分
    if not digits or any(char < "0" or char > "9" for char in digits):
        raise ValueError("请输出非空的阿拉伯数字")
    return sign, integer, fraction if dot else None


# 分割输入的数字
def _digit_tokens(text: str) -> List[str]:
    return [DIGITS[int(char)] for char in text]  # 列表推导式


# 读取每一位，并且去除先导零
def digit_tokens(text: str) -> List[str]:
    sign, integer, fraction = _parse(text)
    result = ["负"] if sign == "-" else []
    result.extend(_digit_tokens(integer or "0"))
    if fraction is not None:
        result.append("点")
        result.extend(_digit_tokens(fraction))
    return result


# 按组读数字,每一组四个数字
def _group_tokens(value: int) -> List[str]:
    result = []
    pending_zero = False  # 添加零的处理逻辑
    for position in range(3, -1, -1):
        digit = value // (10 ** position) % 10
        if digit:  # 如果不是零,输出数字和单位
            if pending_zero:
                result.append("零")
            result.append(DIGITS[digit])  # 输出数字
            if position:  # 不是个位的时候才加单位
                result.append(SMALL_UNITS[position])  # 按位置加单位
            pending_zero = False
        elif result:
            pending_zero = True  # 实现重复的零只加一个
    return result


# 整数部分的读取
def _integer_tokens(text: str) -> List[str]:
    significant = text.lstrip("0") or "0"
    if len(significant) > MAX_DIGITS:
        return _digit_tokens(text)
    value = int(significant)
    if value == 0:
        return ["零"]
    groups = []
    while value:
        groups.append(value % 10000)
        value //= 10000
    result = []
    skipped = False
    for index in range(len(groups) - 1, -1, -1):
        group = groups[index]
        if group == 0:
            skipped = bool(result)
            continue
        if result and (skipped or group < 1000):
            result.append("零")
        part = _group_tokens(group)
        if not result and len(part) >= 2 and part[:2] == ["一", "十"]:
            part.pop(0)
        result.extend(part)
        if index:
            result.append(GROUP_UNITS[index])
        skipped = False
    return result


# 读取一个可选为负的十进制数；逐位读取小数位。
def number_tokens(text: str) -> List[str]:
    sign, integer, fraction = _parse(text)
    result = ["负"] if sign == "-" else []
    result.extend(_integer_tokens(integer or "0"))
    if fraction is not None:
        result.append("点")
        result.extend(_digit_tokens(fraction))
    return result


# 读取策略
READING_MODES: Dict[str, Callable[[str], List[str]]] = {
    "数值读法": number_tokens,
    "逐位读法": digit_tokens,
}

# if __name__ == '__main__':
# text = input("请输入一串数字：")
# # 异常处理
# try:
#     tokens = digit_tokens(text)
# except ValueError as e:
#     print("输入有误：",e)
# else:
#     print("读法为："+"".join(tokens))

# 测试四位数以内
# for text in ("2382","1001","1000","101","10"):
#     print(text,"->","".join(number_tokens(text)))
