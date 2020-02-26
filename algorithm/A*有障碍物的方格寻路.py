from itertools import permutations


class Node:
    '''
    定义相邻横竖的单元格距离是10，斜的的14
    '''
    def __init__(self, x, y, parent, g=0, h=0):
        self.x = x # 节点横坐标
        self.y = y # 节点纵坐标
        self.h = h
        self.g = g
        self.f = g + h
        self.parent = parent # 父节点

    def get_G(self):
        '''
        当前节点到起点的代价
        '''
        if self.g != 0:
            return self.g
        elif self.parent is None:
            self.g = 0
        elif self.parent.x == self.x or self.parent.y == self.y:
            self.g = self.parent.get_G() + 10
        else:
            self.g = self.parent.get_G() + 14
        return self.g
    
    def get_H(self, end):
        '''
        节点到终点的距离估值
        :param end: 终点坐标(x, y)
        '''
        if self.h == 0:
            self.h = self.manhattan(self.x, self.y, end[0], end[1]) * 10
        return self.h
    
    def get_F(self, end):
        '''
        节点评估值
        :param end: 终点坐标(x, y)
        '''
        if self.f == 0:
            self.f = self.get_G() + self.get_H(end)
        return self.f

    def manhattan(self, from_x, from_y, end_x, end_y):
        '''曼哈顿距离，x+y'''
        return abs(end_x - from_x) + abs(end_y - from_y)


class AStar:
    """
    使用A*算法找到最短移动路径
    """
    def __init__(self, start, end, map2d, obstruction=1):
        '''
        :param start:       起点坐标
        :param end:         终点坐标
        :param map2d:       地图
        :param obstruction: 障碍物标记
        '''
        self.start_x, self.start_y = start
        self.end = end
        self.map2d = map2d
        self.openlist = {}  # 待探索坐标列表
        self.closelist = {} # 已探索坐标列表
        # 垂直和水平方向的向量差
        self.v_hv = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        # 斜对角的向量差
        self.v_diagonal = [(-1, 1), (1, 1), (1, -1), (-1, -1)]
        self.obstruction = obstruction
        # 地图边界
        self.x_edge, self.y_edge = len(map2d), len(map2d[0])
        self.answer = None

    def is_in_map(self, x, y):
        """
        该位置是否在地图内
        """
        return 0 <= x < self.x_edge and 0 <= y < self.y_edge
    
    def in_closelist(self, x, y):
        """
        该位置是否在cliselist中
        """
        return self.closelist.get((x, y)) is not None
    
    def upd_openlist(self, node):
        """
        更新openlist中的数据替换为node
        """
        self.openlist[(node.x, node.y)] = node
    
    def add_in_openlist(self, node):
        """
        将node添加到openlist中
        """
        self.openlist[(node.x, node.y)] = node
    
    def add_in_closelist(self, node):
        """
        将node添加到closelist中
        """
        self.closelist[(node.x, node.y)] = node

    def pop_min_F(self):
        """
        弹出openlist中F值最小的点
        """
        key_min, node_min = None, None
        for key, node in self.openlist.items():
            if node_min is None:
                key_min, node_min = key, node
            elif node.get_F(self.end) < node_min.get_F(self.end):
                key_min, node_min = key, node
        if key_min is not None:
            self.openlist.pop(key_min)
        return node_min
    
    def get_Q(self, P):
        """
        找到P周围可以探索的节点
        """
        Q = {}
        # 将水平和垂直方向的方格加入Q
        for dir in self.v_hv:
            x, y = P.x + dir[0], P.y + dir[1]
            # 如果(x, y)不是障碍物并且不在closelist中，将(x, y)
            # 加到Q中
            if self.is_in_map(x, y) \
                and self.map2d[x][y] != self.obstruction \
                and not self.in_closelist(x, y):
                Q[(x, y)] = Node(x, y, P)

        for dir in  self.v_diagonal:
            x, y = P.x + dir[0], P.y + dir[1]
            # 如果(x, y)不是障碍物，且(x, y)能够与P联通
            # 且(x, y)不在closelist中，则将(x, y)加入到Q
            if self.is_in_map(x, y) \
                    and self.map2d[x][y] != self.obstruction \
                    and self.map2d[x][P.y] != self.obstruction \
                    and self.map2d[P.x][y] != self.obstruction \
                    and not self.in_closelist(x, y):
                Q[(x, y)] = Node(x, y, P)
        return Q
    
    def search(self):
        while True:
            # 找到openlist中的F值最小的节点作为探索节点
            P = self.pop_min_F()
            # openlist为空，表示没有通向终点的路
            if P is None:
                break
            # 将P加入closelist
            self.add_in_closelist(P)
            # P周围待探索的节点
            Q = self.get_Q(P)
            # Q中没有任何节点，表示该路径一定不是最短路径，重新从openlist中选择
            if Q == {}:
                continue
            # 找到了终点，推出循环
            if Q.get(self.end) is not None:
                self.answer = Node(self.end[0], self.end[1], P)
                break
            # Q中的节点与openlist中的比较 
            for item in Q.items():
                (x, y), node_Q = item[0], item[1]
                node_openlist = self.openlist.get((x, y))
                # 如果node_Q不在openlist中，直接将其加入openlist
                if node_openlist is None:
                    self.add_in_openlist(node_Q)
                # node_Q的F值比node_openlist更小，则用node_Q替换node_openlist
                elif node_Q.get_F(self.end) < node_openlist.get_F(self.end):
                    self.upd_openlist(node_Q)
    
    def start(self):
        node_start = Node(self.start_x, self.start_y, None)
        self.openlist[(self.start_x, self.start_y)] = node_start
        self.search()
    
    def paint(self):
        """打印最短路径"""
        node = self.answer
        result_x = []
        result_y = []
        dis = 0
        while node is not None:
            # print((node.x, node.y), f"G={node.g}, H={node.h}, F={node.f}")
            result_x.append(node.x)
            result_y.append(node.y)
            if node.g > dis:
                dis = node.g
            node = node.parent
        result_x.reverse()
        result_y.reverse()
        return result_x, result_y, dis

def get_per_dis(start, end, map2d):
    a_way = AStar(start, end, map2d)
    a_way.start()
    result_x, result_y, dis = a_way.paint()
    return result_x, result_y, dis

def result_way(alist, map2d):
    p_start = alist[0]
    p_end = alist[-1]
    all_possible = [ [p_start] + list(x) + [p_end] for x in permutations(alist[1:-1])]
    all_result = {}
    for each_way in all_possible:
        each_way_result = 0
        each_way_points_x = []
        each_way_points_y = []
        for idx, _ in enumerate(each_way):
            if idx < len(each_way)-1:
                # print(f"each way start:end--{each_way[idx]}:{each_way[idx+1]}")
                result_x, result_y, dis = get_per_dis(each_way[idx], each_way[idx+1], map2d)
                each_way_result += dis
                each_way_points_x += result_x
                each_way_points_y += result_y
        # print(f"{each_way},way:points{list(zip(each_way_points_x, each_way_points_y))}")
        all_result[each_way_result] = [each_way_points_x, each_way_points_y]
    min_one = min(list(all_result.keys()))
    return all_result[min_one]


if __name__ == "__main__":
    map2d = [[0]*10 for i in range(14)]
    for x in [2, 3, 6, 7, 10, 11]:
        for y in range(2, 8):
            map2d[x][y] = 1

    result_x, result_y = result_way([(0, 0), (4, 7), (12, 3), (0, 9)], map2d)
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
    # 散点图
    plt.scatter(way_x, way_y, marker='*', c='b', s=10 , alpha=0.5)
    plt.scatter(shelf_x, shelf_y, marker='*', c='r', s=10, alpha=0.5)
    # 连线图
    plt.plot(result_x, result_y, linewidth=2, color='blue', marker='D')
    # plt.plot(x_label, y_label, label="2d map for store",
    #          linewidth=3, color='b', marker='0',
    #          markerfacecolor='blue', markersize=15)
    plt.xlabel('x length')
    plt.ylabel('y length')
    for a, b in zip(way_x, way_y):
        plt.text(a, b, (a, b), ha='center', va='bottom', fontsize=5)


    plt.legend()
    plt.show()