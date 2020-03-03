'''
定义：由顶点的有穷非空集合和顶点之间的集合组成
通常表示为：G(V,E)，G表示图，V表示顶点集合，
E表示边的集合。
- 线性表中的数据元素被称为元素，树中将数据元素称为结点，
  而图中数据元素被称为顶点。
- 线性表可以没有数据元素，称为空表；
  树也可以没有结点，称为空树。
  但是图的定义中强调了顶点集合V是有穷非空的集合，
  所以图结构中不能没有顶点。
- 线性表中，相邻的数据元素之间具有线性关系；
  树结构中，相邻两层的结点具有层次关系。
  而图中，任意两个顶点之间都可能有关系，
  顶点之间的逻辑关系用边来表示，边集可以是空的。
'''
# ←↑→↓↖↙↗↘↕↔️
#  A  ➡️  C    E
#  ↓  ↗  ↕  ↖ ↓
#  B  ➡️  D    F
# Python中一般通过字典和列表来构造图
graph = {
    'A': ['B', 'C'],
    'B': ['C', 'D'],
    'C': ['D'],
    'D': ['C'],
    'E': ['F'],
    'F': ['C']
}

def BFS(graph, point):
    """
    广度优先
    """
    queue = []
    queue.append(point)
    seen = set()
    seen.add(point)
    while len(queue) > 0:
        vertex = queue.pop(0)
        nodes = graph[vertex]
        for node in nodes:
            if node not in seen:
                queue.append(node)
                seen.add(node)
        print(vertex)
# 从A点开始，所有可以到达的点
BFS(graph, 'A')


def DFS(graph, s):
    """
    深度优先
    """
    stack = []
    stack.append(s)
    seen = set()
    seen.add(s)
    while len(stack) > 0:
        vertex = stack.pop()
        nodes  = graph[vertex]
        for node in nodes:
            if node not in seen:
                stack.append(node)
                seen.add(node)
        print(vertex)
# 搜索最长路径，并定位到最后一个分岔点
DFS(graph, 'A')