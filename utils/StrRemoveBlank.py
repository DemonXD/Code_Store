import re

def process(input_str: str) -> str:
    """[summary]

    Args:
        input_str ([str]): [be processed string]

    Returns:
        [str]: [remove blank string]

    Desc.:
        use re
    """
    pattern_rm_blank_within_cn = re.compile(r"([\u4e00-\u9fa5]+)\s+([\u4e00-\u9fa5]+)")
    pattern_rm_multi_blank = re.compile(r"\s+", re.S)
    str1 = input_str.strip()
    str1 = re.sub(pattern_rm_multi_blank, " ", str1)
    while re.search(pattern_rm_blank_within_cn, str1) is not None:
        str1 = re.sub(pattern_rm_blank_within_cn, r"\1\2", str1)
    return str1


def process_algo(input_str: str) -> str:
    """[summary]

    Args:
        input_str (str): [be processed string]

    Returns:
        str: [remove blank string]
    """
    def isCN(word):
        if '\u4e00' <= word <= '\u9fa5':
            return True
        return False
    # 1. 按照指定窗口大小进行滑动
        # - 从后端向前滑动
    # 2. 判断规则
    # 3. 处理
    str1_list = input_str.split() # 剔除多余空格
    result = []
    for idx in range(0, len(str1_list)):
        if idx+1 == len(str1_list):
            result.append(str1_list[idx])
            break
        if isCN(str1_list[idx]) and isCN(str1_list[idx+1]):
            result.append(str1_list[idx])
        else:
            result.append(str1_list[idx])
            result.append(" ")

    return "".join(result)
    



if __name__ == "__main__":
    a = "abc   a 哦 abc abc    abc 你谁    他  我 "
    print(f"process by re|{process(a)}|")
    print(f"process by algo|{process_algo(a)}|")