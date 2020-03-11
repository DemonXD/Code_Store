from algorithm.AStar_有障碍物的网格寻路算法 import *

if __name__ == "__main__":
    map2d = [[0]*10 for i in range(14)]
    for x in [2, 3, 6, 7, 10, 11]:
        for y in range(2, 8):
            map2d[x][y] = 1

    targets = [(0, 0), (4, 2), (4, 7), (8, 6), (12, 3), (0, 9)]
    result_x, result_y = result_way(targets, map2d)
    # from pprint import pprint
    # pprint(map2d)
    from matplotlib import pyplot as plt
    shelf_x = []
    shelf_y = []
    way_x = []
    way_y = []
    for index_x, idx in enumerate(map2d):
        for index_y, idy in enumerate(idx):
            if map2d[index_x][index_y] == 1:
                shelf_x.append(index_x)
                shelf_y.append(index_y)
            else:
                way_x.append(index_x)
                way_y.append(index_y)
    plt.figure(figsize=(10, 8))
    plt.title("store map2d")

    # 连线图
    plt.plot(result_x, result_y, linewidth=2, color='blue', marker='D', alpha=0.2)
    # plt.plot(x_label, y_label, label="2d map for store",
    #          linewidth=3, color='b', marker='0',
    #          markerfacecolor='blue', markersize=15)
    plt.xlabel('x length')
    plt.ylabel('y length')
    for a, b in zip(way_x, way_y):
        plt.text(a, b, (a, b), ha='center', va='bottom', fontsize=5)

    # 散点图
    plt.scatter([each[0] for each in targets], [each[1] for each in targets], marker='D', c='r', s=20, alpha=1)
    plt.scatter(way_x, way_y, marker='*', c='black', s=10 , alpha=0.3)
    plt.scatter(shelf_x, shelf_y, marker='*', c='r', s=10, alpha=0.7)


    plt.legend()
    plt.show()