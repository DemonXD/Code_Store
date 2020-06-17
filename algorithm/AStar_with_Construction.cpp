#include <iostream>
#include <vector>
#include <array>
#include <tuple>
#include <map>
#include <algorithm> // reverse
#include <stdlib.h> // abs


void PrintArray(int map2d[15][15])
{
    for (int i = 0; i < 15; i++)
    {
        for (int j = 0; j < 15; j++)
        {
            std::cout << map2d[i][j] << " ";
        }
        std::cout << std::endl;
    }
}

struct Node
{
    int nx, ny, nh, ng, nf;
    // int nf = ng + nh;
    Node* nparent = nullptr;
    Node() {};
    Node(const Node& other)
    {
        this->nx = other.nx;
        this->ny = other.ny;
        this->nparent = other.nparent;
    }
    Node(int x, int y, Node* parent, int g = 0, int h = 0)
        : nx(x), ny(y), nh(h), ng(g), nparent(parent), nf(ng + nh) {}
    ~Node() {}
    Node operator=(const Node* onode)
    {
        nx = onode->nx;
        ny = onode->ny;
        nh = onode->nh;
        ng = onode->ng;
        nparent = onode->nparent;
        return *this;
    }
    int get_G()
        // 当前节点到起点的代价
    {
        if (this->ng != 0)
        {
            return this->ng;
        }
        else if (this->nparent == nullptr)
        {
            this->ng = 0;
        }
        else if ((this->nparent->nx == this->nx) | (this->nparent->ny == this->ny))
        {
            this->ng = this->nparent->get_G() + 10;
        }
        else
        {
            this->ng = this->nparent->get_G() + 14;
        }
        std::cout << this->nx << "， " << this->ny << "到起点的代价: " << this->ng << std::endl;
        return this->ng;
    }
    int get_H(std::tuple<int, int> end)
    {
        if (this->nh == 0)
        {
            this->nh = this->manhattan(this->nx, this->ny, std::get<0>(end), std::get<1>(end)) * 10;
        }
        std::cout << this->nx << "， " << this->ny << "到终点的估值: " << this->nh << std::endl;
        return this->nh;
    }
    int get_F(std::tuple<int, int> end)
    {
        if (this->nf == 0)
        {
            this->nf = this->get_G() + this->get_H(end);
        }
        std::cout << this->nx << "， " << this->ny << "到终点的总估值：" << this->nf << std::endl;
        return this->nf;
    }
    int manhattan(int from_x, int from_y, int end_x, int end_y)
    {
        int dis = abs(end_x - from_x) + abs(end_y - from_y);
        std::cout << "manhattan距离: " << dis << std::endl;
        return dis;
    }
};


class AStar
{
public:
    const int obstruction = 1;
    std::tuple<int, int> nstart, nend;
    int start_x, start_y;
    std::map<std::tuple<int, int>, Node*> openlist;
    std::map<std::tuple<int, int>, Node*> closelist;
    int nmap2d[15][15] = {
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    }; // 50x50 二维数组
    const int x_edge = 15;
    const int y_edge = 15;
    Node* answer = nullptr;
    std::vector<std::tuple<int, int>> v_hv = {
        std::make_tuple(-1, 0), std::make_tuple(0, 1),
        std::make_tuple(1, 0), std::make_tuple(0, -1)
    };
    std::vector<std::tuple<int, int>> v_diagonal = {
        std::make_tuple(-1, 1), std::make_tuple(1, 1),
        std::make_tuple(1, -1), std::make_tuple(-1, -1)
    };

    AStar(std::tuple<int, int> start, std::tuple<int, int> end, const int map2d[15][15])
        : nstart(start), nend(end)
    {
        start_x = std::get<0>(start);
        start_y = std::get<1>(start);
        for (int i = 0; i < 15; i++)
        {
            for (int j = 0; j < 15; j++)
            {
                nmap2d[i][j] = map2d[i][j];
            }
        }
        std::cout << "AStar 初始化成功" << std::endl;
    }
    ~AStar() { ; }
    bool is_in_map(int x, int y)
    {
        bool temp = ((0 <= x) & (x < 15)) & ((0 <= y) & (y < 15));
        return temp;
    }
    bool in_closelist(int x, int y)
    {
        auto point = std::make_tuple(x, y);
        bool temp = this->closelist.find(point) != this->closelist.end();
        return temp;
    }
    void upd_openlist(Node* node)
    {
        // Node* temp = node;
        std::cout << "x:" << node->nx << ", y:" << node->ny << " " << "更新openlist节点列表" << std::endl;
        this->openlist[std::make_tuple(node->nx, node->ny)] = node;
        std::cout << "upd_openlist 执行完成" << std::endl;
    }
    void add_in_openlist(Node* node)
    {
        // Node* temp = node;
        std::cout << "x:" << node->nx << ", y:" << node->ny << " " << "添加进openlist列表中" << std::endl;
        this->openlist[std::make_tuple(node->nx, node->ny)] = node;
        std::cout << "add_in_openlist 执行完成" << std::endl;
    }
    void add_in_closelist(Node* node)
    {
        // Node* temp = node;
        std::cout << "节点: (" << node->nx << ", " << node->ny << ") " << "添加进closelist列表中" << std::endl;
        this->closelist[std::make_tuple(node->nx, node->ny)] = node;
        std::cout << "add_in_closelist 执行完成" << std::endl;
    }
    Node* pop_min_F() // OK
    {
        std::tuple<int, int> key_min(-1, -1);
        Node* node_min = nullptr;
        for (auto iter = this->openlist.begin(); iter != this->openlist.end(); iter++)
        {
            if (key_min == std::make_tuple(-1, -1))
            {
                key_min = iter->first;
                node_min = iter->second;
            }
            else if ((iter->second)->get_F(this->nend) < node_min->get_F(this->nend))
            {
                key_min = iter->first;
                node_min = iter->second;
            }
        }
        if (key_min != std::make_tuple(-1, -1))
        {
            this->openlist.erase(key_min);
        }
        std::cout << " 最小F值node点: (" << node_min->nx << ", " << node_min->ny << ")" << std::endl;
        return node_min;
    }
    std::map<std::tuple<int, int>, Node> get_Q(Node* P) // OK
    {
        std::cout << "获取P点周围可用点" << std::endl;
        std::map<std::tuple<int, int>, Node> temp_points;
        for (auto iter = this->v_hv.begin(); iter != this->v_hv.end(); iter++)
        {
            int x = P->nx + std::get<0>(*iter);
            int y = P->ny + std::get<1>(*iter);
            // std::cout << "(" << x << ", " << y << ")" << ", ";
            // std::cout << "is_in_map: " << is_in_map(x, y) << ", ";
            // std::cout << "是否是路障: " << (this->nmap2d[x][y] == this->obstruction) << ", ";
            // std::cout << "是否是已探索点：" << this->in_closelist(x, y) << std::endl;
            if (this->is_in_map(x, y) & (this->nmap2d[x][y] != this->obstruction) &
                (!this->in_closelist(x, y)))
            {
                std::cout << "上下左右方位添加： (" << x << ", " << y << ")" << std::endl;
                temp_points[std::make_tuple(x, y)] = Node(x, y, P);
            }
        }
        for (auto iter = this->v_diagonal.begin(); iter != this->v_diagonal.end(); iter++)
        {
            int x = P->nx + std::get<0>(*iter);
            int y = P->ny + std::get<1>(*iter);
            // std::cout << "(" << x << ", " << y << ")" << ", ";
            // std::cout << "is_in_map: " << is_in_map(x, y) << ", ";
            // std::cout << "该点点值：" << this->nmap2d[x][y] << ", 路障是：" << this->obstruction << " ";
            // std::cout << "是否是路障: " << (this->nmap2d[x][y] == this->obstruction) << ", ";
            // std::cout << "x,P.y 是否是路障: " << (this->nmap2d[x][P->ny] == this->obstruction) << ",";
            // std::cout << "P.x,y 是否是路障: " << (this->nmap2d[P->nx][y] == this->obstruction) << ",";
            // std::cout << "是否是已探索点：" << this->in_closelist(x, y) << std::endl;
            if (this->is_in_map(x, y) & (this->nmap2d[x][y] != this->obstruction) &
                (this->nmap2d[x][P->ny] != this->obstruction) &
                (this->nmap2d[P->nx][y] != this->obstruction) &
                !this->in_closelist(x, y))
            {
                std::cout << "四角方位添加： (" << x << ", " << y << ")" << std::endl;
                temp_points[std::make_tuple(x, y)] = Node(x, y, P);
            }
        }
        return temp_points;
    }
    void search()
    {
        int count = 0;
        std::cout << "搜索开始" << std::endl;
        while (true)
        {

            std::cout << "----------------" << count << "-----------------" << std::endl;
            std::cout << "openlist(待探索坐标列表): ";
            for (auto it = this->openlist.begin(); it != this->openlist.end(); it++)
            {
                std::cout << "(" << it->second->nx << ", " << it->second->ny << ")" << " ";
            }
            std::cout << std::endl;

            std::cout << "closelist(已探索坐标列表): ";
            for (auto it = this->closelist.begin(); it != this->closelist.end(); it++)
            {
                std::cout << "(" << it->second->nx << ", " << it->second->ny << ")" << " ";
            }
            std::cout << std::endl;

            Node* P = this->pop_min_F();
            if (P == nullptr) break;
            this->add_in_closelist(P);
            std::map<std::tuple<int, int>, Node> Q = {};
            Q = this->get_Q(P);
            if (Q.begin() == Q.end()) continue;
            std::cout << "P周围可用点: ";
            for (auto it = Q.begin(); it != Q.end(); it++)
            {
                std::cout << "(" << std::get<0>(it->first) << ", " << std::get<1>(it->first) << ") ";
            }
            std::cout << std::endl;
            // ok
            auto it = Q.find(this->nend);
            if (it != Q.end())
            {
                *(this->answer) = Node(std::get<0>(this->nend), std::get<1>(this->nend), P);
                break;
            }
            // ok
            std::cout << "开始比较openlist和Q" << std::endl;
            std::cout << "openlist 中的点：";
            for (auto it = this->openlist.begin(); it != this->openlist.end(); it++)
            {
                std::cout << std::get<0>(it->first) << ", " << std::get<1>(it->first);
            }
            std::cout << std::endl;
            for (auto iter = Q.begin(); iter != Q.end(); iter++)
            {
                Node* node_Q = new Node(iter->second);
                std::cout << "*****当前点: (" << std::get<0>(iter->first) << ", " << std::get<1>(iter->first) << ")" << std::endl;
                int temp_x = std::get<0>(iter->first);
                int temp_y = std::get<1>(iter->first);

                auto it = this->openlist.find(std::make_tuple(temp_x, temp_y));
                // error
                if (it == this->openlist.end()) // 如果openlist中无此点
                {
                    this->add_in_openlist(node_Q);
                    std::cout << "Q不在openlist中，添加" << std::endl;
                }
                else if (node_Q->get_F(this->nend) < it->second->get_F(this->nend))
                {
                    std::cout << "node_Q的F值比node_openlist更小，则用node_Q替换node_openlist" << std::endl;
                    this->upd_openlist(node_Q);
                }
                std::cout << "*****当前点: (" << std::get<0>(iter->first) << ", " << std::get<1>(iter->first);
                std::cout << ")" << "检查完毕" << std::endl;
                delete node_Q;
            }
            std::cout << "=========================" << std::endl;
        }
    }

    void run()
    {
        PrintArray(this->nmap2d);
        Node* node_start = new Node(this->start_x, this->start_y, nullptr);
        this->openlist[std::make_tuple(this->start_x, this->start_y)] = node_start;
        this->search();
        delete node_start;
    }

    void paintway()
    {
        Node* node = this->answer;
        std::vector<int> result_x;
        std::vector<int> result_y;
        int dis = 0;
        while (node != nullptr)
        {
            result_x.push_back(node->nx);
            result_y.push_back(node->ny);
            if (node->ng > dis)
            {
                dis = node->ng;
            }
            node = node->nparent;
        }
        std::reverse(result_x.begin(), result_x.end());
        std::reverse(result_y.begin(), result_y.end());
        for (auto it = result_x.begin(); it != result_x.end(); it++)
            std::cout << "x: " << *it << std::endl;
        for (auto it = result_y.begin(); it != result_y.end(); it++)
            std::cout << "y: " << *it << std::endl;
        std::cout << "dis: " << dis << std::endl;
    }


};

int main()
{
    int map2d[15][15] = {
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    };
    for (int i = 4; i < 7; i++)
    {
        map2d[i][7] = 1;
        map2d[6][i] = 1;
    }
    for (int i = 10; i < 13; i++)
    {
        map2d[i][10] = 1;
        map2d[10][i] = 1;
    }
    for (int i = 9; i < 13; i++)
    {
        map2d[i][4] = 1;
    }
    for (int i = 10; i < 13; i++)
    {
        map2d[5][i] = 1;
    }
    // PrintArray(map2d);

    std::tuple<int, int> start_point = std::make_tuple(0, 0);
    std::tuple<int, int> end_point = std::make_tuple(13, 14);
    AStar away = AStar(start_point, end_point, map2d);
    away.run();
    away.paintway();
    return 0;
}
