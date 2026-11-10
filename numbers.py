DIGITS = "零一二三四五六七八九"

def digit_tokens(text):
    return [DIGITS[int(char)] for char in text] # 列表推导式

if __name__ == '__main__':
    text = input("请输入一串数字：")
    tokens = digit_tokens(text)
    print("读法："+"".join(tokens))

