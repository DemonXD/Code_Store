def CMlist(list1, list2):
    l = len(list1)  + len(list2)
    target_list = []
    for i in range(0, l-1):
        if len(list1) != 0:
            target_list.append(list1.pop(0))
        if len(list2) != 0:
            target_list.append(list2.pop(0))
    return target_list

# test func
# print(CMlist([1,3,5,7,9], [2,4,6,8,10,11,'a','b']))
# the result should be: 1,2,3,4,5,6,7,8,9,10,11,a,b