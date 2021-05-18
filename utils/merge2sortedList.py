class Solution:
    def mergeSortList(self, l1, l2):
        """
            Input:
                :paras l1:
                :paras l2:
            Output:
                :return: new merge list
            Desc.:
                1.原地排序
                2.遍历第二的数组，与第一个数组做对比
                3.插入第一个数组
        """
        import copy
        ll1 = copy.deepcopy(l1)
        ll2 = copy.deepcopy(l2)
        cursor = 0

        # 使用长数组做原数组
        olist, poplist = (ll1, ll2) if (len(ll1) >= len(ll2)) else (ll2, ll1)
        # 短数组弹出首元素
        while len(poplist) > 0:
            tmp = poplist.pop(0)
            # 因为是有序数组，所以可以记录当前插入位置的下标
            # 作为下次对比时的首位，可以有效减少遍历次数
            for idx in range(cursor, len(olist)):
                # 如果待插入元素小于当前对比元素，则插在当前位置
                # 并且将游标后移以为，下次直接从下一位开始对比
                if tmp < olist[idx]:
                    olist.insert(idx, tmp)
                    cursor = idx + 1
                    break
                else:
                    # 如果插入元素时原数组最大元素则，插入最后
                    if len(olist) == cursor+1:
                        olist.insert(cursor+1, tmp)
                        cursor += 1
                        break
                    # 如果插入元素大于当前元素，则直接将游标后移一位，进入下一次对比
                    cursor += 1
                    continue            
        return olist



if __name__ == "__main__":
    s = Solution()
    tests = [
    (([1], [1]), [1, 1]),
    (([], []), []),
    (([1, 2], [1, 2]), [1, 1, 2, 2]),
    (([1], [1, 2, 3, 4]), [1, 1, 2, 3, 4]),
    (([1, 2, 3, 4], [1, 2, 3, 4]), [1, 1, 2, 2, 3, 3, 4, 4]),
    (([1, 3, 5, 7, 9], [2, 4]), [1, 2, 3, 4, 5, 7, 9]),
    (([1, 2, 3], [4, 5, 6]), [1, 2, 3, 4, 5, 6]),
    (([4, 5, 6], [1, 2, 3]), [1, 2, 3, 4, 5, 6]),
    ]
    for each_test in tests:
        print(f"{each_test} => result: {s.mergeSortList(*each_test[0])}")
        assert s.mergeSortList(*each_test[0]) == each_test[-1]
    # print(s.mergeSortList([1, 7, 8, 19], [2, 3, 5, 10]))
    else:
        print("test done")