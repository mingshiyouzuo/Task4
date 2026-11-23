from typing import Tuple, Optional, List, Dict, Callable

# 数字、单位以及最大位数
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


# 分割小数位数字
# 小数位没有单位，直接分隔即可
def _digit_tokens(text: str) -> List[str]:
    return [DIGITS[int(char)] for char in text]  # 列表推导式 逐个替换为对应的汉字


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

    # 从高位向低位处理
    for position in range(3, -1, -1):
        digit = value // (10 ** position) % 10  # 先移位再取模
        if digit:  # 如果不是零,输出数字和单位
            if pending_zero:  # 补上欠下的零
                result.append("零")

            result.append(DIGITS[digit])  # 输出数字
            if position:  # 不是个位的时候才加单位
                result.append(SMALL_UNITS[position])  # 按位置加单位

            pending_zero = False  # 补零后置位
        elif result:
            pending_zero = True  # 标记有一个零且不重复标记

    return result


# 整数部分的读取，将整数部分转换为对应读法的字符串
def _integer_tokens(text: str) -> List[str]:
    significant = text.lstrip("0") or "0"  # 去除左侧零

    if len(significant) > MAX_DIGITS:  # 如果超过20位改为逐位读，我的读法最大单位是京
        return _digit_tokens(text)

    # 转为int并特殊处理零
    value = int(significant)
    if value == 0:
        return ["零"]

    # 四位分组，循环处理
    groups = []
    while value:
        groups.append(value % 10000)  # 取最低四位并右移动四位
        value //= 10000

    result = []
    skipped = False
    # 从高到低组倒序依次拼接
    for index in range(len(groups) - 1, -1, -1):
        group = groups[index]
        if group == 0:  # 记录一组零要跳过
            skipped = bool(result)  # 跳过标记
            continue
        if result and (skipped or group < 1000):  # 一组为零或者不足四位补零，且有内容的时候才补零
            result.append("零")

        # 对一十单独特殊处理，如果不纠结可以删除
        # 比如12表示为十二而不是一十二
        part = _group_tokens(group)  # 合并组数字
        if not result and len(part) >= 2 and part[:2] == ["一", "十"]:
            part.pop(0)  # 弹出之前跳过的零
        result.extend(part)

        # 跳过空串
        if index:
            result.append(GROUP_UNITS[index])  # 每一组后面添加对应的单位
        skipped = False

    return result


# 读取一个可选为负的十进制数；逐位读取小数位。
def number_tokens(text: str) -> List[str]:
    sign, integer, fraction = _parse(text)  # 元组解包
    result = ["负"] if sign == "-" else []
    arg = integer or "0"  # 如果整数部分是空则取0
    result.extend(_integer_tokens(arg))
    if fraction is not None:
        result.append("点")
        result.extend(_digit_tokens(fraction))
    return result


# 读取策略
# 注意字符对应的是函数
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
