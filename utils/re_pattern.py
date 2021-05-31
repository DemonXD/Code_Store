import re


Digit_pattern = re.compile(r"\d+")

# 小数点可选，如果前面有整数对后面不做要求，如果前面没有整数后面一定要有数值，可选的指数部分。
Decimal_pattern = re.compile(r"^[-+]?([0-9]+(.[0-9]*)?|.[0-9]+)$", re.S)

# 匹配电话好嘛
text = "(021)88776543 010-55667890 02584533622 057184720483 837922740"
telephone_pattern = re.compile(r'\(?0\d{2,3}[)-]?\d{7,8}', re.S)

# 邮箱
email_pattern = re.compile(r'''([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+(\.[a-zA-Z]{2,4}))''', re.VERBOSE)

