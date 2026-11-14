"""这里是测试文件"""
import unittest

from number_voice.numbers import digit_tokens, number_tokens


class NumberReaderTests(unittest.TestCase):
    def test_number_examples(self):
        examples = {
            "0": "零",
            "000": "零",
            "10": "十",
            "11": "十一",
            "20": "二十",
            "101": "一百零一",
            "1000": "一千",
            "1001": "一千零一",
            "2382": "二千三百八十二",
            "10000": "一万",
            "10010": "一万零一十",
            "100000": "十万",
            "100000001": "一亿零一",
            "100010001": "一亿零一万零一",
            "100010000": "一亿零一万",
            "1000000000000": "一兆",
            "10000000000000000": "一京",
            "-23": "负二十三",
            "-0": "负零",
            "12.34": "十二点三四",
            "12.05": "十二点零五",
            "12.50": "十二点五零",
            ".5": "零点五",
            "-0.5": "负零点五",
            "00012.030": "十二点零三零",
            "10001.001": "一万零一点零零一",
            "99999999999999999999": "九千九百九十九京九千九百九十九兆九千九百九十九亿九千九百九十九万九千九百九十九",
        }
        for text, expected in examples.items():
            with self.subTest(text=text):
                self.assertEqual("".join(number_tokens(text)), expected)

    # 测试阻止前导零
    def test_digit_mode_preserves_zero(self):
        self.assertEqual("".join(digit_tokens("00238")), "零零二三八")
        self.assertEqual("".join(digit_tokens("-0023.50")), "负零零二三点五零")

    # 测试长输入数字文本
    def test_long_input_falls_back_to_digits(self):
        text = "123456789012345678901"
        self.assertEqual(number_tokens(text), digit_tokens(text))
        self.assertEqual("".join(number_tokens("0" * 5000 + "23")), "二十三")
        self.assertEqual(len(digit_tokens("7" * 5000)), 5000)

    # 测试非法输入
    def test_invalid_input(self):
        for text in (
                "",
                " 12", "12 ", "+1", "１２", "1\n", "-", "-.", ".", "1.", "1.2.3",
                "--1", "1,2",
        ):
            for converter in (number_tokens, digit_tokens):
                with self.subTest(text=text, converter=converter.__name__):
                    with self.assertRaises(ValueError):
                        converter(text)


if __name__ == "__main__":
    unittest.main()
