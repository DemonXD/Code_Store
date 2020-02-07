from __future__ import annotations
import random
import time
import request_
from models import (
    db, init_tables, Employer,
    approvalTask, row2dict,
    Resource
)
from duty_chain import get_chain

def main():
    # 已经执行过，数据库有10条记录
    init_tables()

    for idx, each in enumerate(request_.get_requests()):
        print(f"-------{idx}-------")
        print(get_chain().handle(each))


if __name__ == "__main__":
    main()