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
    pattern_rm_blank_within_cn = re.compile(r"([\u4e00-\u9fa5]+)\s+([\u4e00-\u9fa5]+)", re.S | re.M)
    pattern_rm_multi_blank = re.compile(r"\s+", re.S)
    str1 = input_str.strip()
    str2 = re.sub(pattern_rm_multi_blank, " ", str1)
    str3 = re.sub(pattern_rm_blank_within_cn, r"\1\2", str2)
    # TODO: re.sub 的使用
    return str3


def process_algo(input_str: str) -> str:
    """[summary]

    Args:
        input_str (str): [be processed string]

    Returns:
        str: [remove blank string]
    """
    pass



if __name__ == "__main__":
    a = "abc   a 哦 abc abc    abc 你谁    他  我 "
    print(f"|{process(a)}|")
    print(f"|{process_algo(a)}|")