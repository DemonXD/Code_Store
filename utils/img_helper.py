#################################
# Date: 2021/05/08
# Author: Miles Xu
# Email: kanonxmm@163.com
# Desc.: 图片处理函数
# 3th-Libs: Pillow
#################################
# -*- coding: utf-8 -*-
import os
from typing import List
from PIL import Image


def rmBrokenImage(img_list: List) -> None:
    typs = [".png", ".jpg", ".jpeg", ".gif"]
    badFilesList = []
    for root, dirs, files in os.walk(img_list):
        # 检查当前目录中的损坏的图片文件
        for each in files:
            # for each in os.listdir('./'):
            if any(map(each.lower().endswith, typs)):
                try:
                    im = Image.open(os.path.join(root, each))
                except Exception as e:
                    badFilesList.append(os.path.join(root, each))
    if len(badFilesList) > 0:
        for each in badFilesList:
            try:
                os.remove(each)
            except Exception as e:
                pass