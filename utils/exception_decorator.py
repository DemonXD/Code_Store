# -*- coding:UTF-8 -*-
# @Time    : 2020/1/30 12:51
# @Author  : Lemo
# @Email   : 2655543796@qq.com
# @File    : 装饰器.py
from __future__ import annotations
import functools
from datetime import datetime
import traceback

# 异常输出
def except_output(msg='异常'):
    # msg用于自定义函数的提示信息
    def except_execute(func):
        @functools.wraps(func)
        def execept_print(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                sign = '=' * 60 + '\n'
                print(f'{sign}>>>异常时间：\t{datetime.now()}\n>>>异常函数：\t{func.__name__}\n>>>{msg}：\t{e}')
                print(f'{sign}{traceback.format_exc()}{sign}')
        return execept_print
    return except_execute

