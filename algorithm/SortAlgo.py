def insertSort(target_list):
    # 遍历原数组
    for idx_i in range(len(target_list)):
        # 遍历前部已排序数组
        for idx_y in range(idx_i):
            # 判断当前值在前部数组中的位置
            if target_list[idx_i] < target_list[idx_y]:
                # 弹出当前元素插入到前部数组
                target_list.insert(idx_y, target_list.pop(idx_i))
                break
    return target_list


def bubbleSort(target_list):
    target_list_length = len(target_list)
    for i in range(target_list_length):
        for j in range(i + 1, target_list_length):
            # 拿当前值和之后所有值做比较，小的放前面
            if target_list[i] > target_list[j]:
                target_list[i], target_list[j] = target_list[j], target_list[i]
    return target_list


def quickSort(target_list):
    if len(target_list) <= 1:
        return target_list
    qfirst = target_list[0]
    # 拿index=0之后的值做比较，小的放前面，大的放后面，然后再对之后的数组做同样的比较，递归进行
    qless = quickSort([l for l in target_list[1:] if l < qfirst])
    qmore = quickSort([m for m in target_list[1:] if m >= qfirst])
    return qless + [qfirst] + qmore


def selectSort(target_list):
    target_list_length = len(target_list)
    smallest = None
    for i in range(target_list_length):
        smallest = i
        # 扫描i之后的每个元素，找到比i位置的元素小的元素，然后和i对调
        for j in range(i+1, target_list_length):
            # 做比较标记到smallest
            if target_list[j] < target_list[smallest]:
                smallest = j
        # 扫描完一轮之后和当前值对调
        target_list[i], target_list[smallest] = target_list[smallest], target_list[i]
    return target_list


def mergeSort(target_list):
    """
        此处为二路归并
    """
    def merge_arr(arr_l, arr_r):
        """
          按照升序对两个数组的元素进行重组
        """
        target_list = []
        while len(arr_l) and len(arr_r):
            if arr_l[0] <= arr_r[0]:
                target_list.append(arr_l.pop(0))
            elif arr_l[0] > arr_r[0]:
                target_list.append(arr_r.pop(0))
        if len(arr_l) != 0:
            target_list += arr_l
        elif len(arr_r) != 0:
            target_list += arr_r
        return target_list
    # 将原始列表拆分为两个列表
    def recursive(target_list):
        """
            对数组一直进行拆分，直到两边各一个元素，
            然后在对两边的数进行排序合并
        """
        if len(target_list) <= 1:
            return target_list
        # 取中间位置的数作为分割点
        mid = len(target_list) // 2
        arr_l = recursive(target_list[:mid])
        arr_r = recursive(target_list[mid:])
        return merge_arr(arr_l, arr_r)
    return recursive(target_list)