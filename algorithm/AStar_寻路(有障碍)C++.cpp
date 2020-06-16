#include <iostream>
#include <vector>
#include <array>
#include <tuple>
#include <map>
#include <algorithm> // reverse


struct Node
{
    int nx, ny, nh, ng, nf;
    // int nf = ng + nh;
    Node* nparent;
    Node(){}
    Node(int x, int y, Node* parent, int g=0, int h=0)
        : nx(x), ny(y), nh(h), ng(g), nparent(parent), nf(ng + nh) {}
    ~Node(){ delete nparent;}
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
    {
        if(this->ng != 0)
        {
            return this->ng;
        }else if(this->nparent == nullptr)
        {
            this->ng = 0;
        }else if(this->nparent->nx == this->nx | this->nparent->ny == this->ny)
        {
            this->ng = this->nparent->get_G() + 10;
        }else
        {
            this->ng = this->nparent->get_G() + 14;
        }
        return this->ng;
    }
    int get_H(std::tuple<int, int> end)
    {
        if (this->nh == 0)
        {
            this->nh = this->manhattan(this->nx, this->ny, std::get<0>(end), std::get<1>(end)) * 10;
        }
        return this->nh;
    }
    int get_F(std::tuple<int, int> end)
    {
        if (this->nf == 0)
        {
            this->nf = this->get_G() + this->get_H(end);
        }
        return this->nf;
    }
    int manhattan(int from_x, int from_y, int end_x, int end_y)
    {
        return abs(end_x - from_x) + abs(end_y - from_y);
    }
};


class AStar
{
public:
    int obstruction;
    std::tuple<int, int> nstart, nend;
    int start_x, start_y;
    std::map<std::tuple<int, int>, Node> openlist;
    std::map<std::tuple<int, int>, Node> closelist;
    int nmap2d[50][50]; // 50x50 二维数组
    int x_edge = 50;
    int y_edge = 50;
    Node* answer;
    std::vector<std::tuple<int, int>> v_hv = {
        std::make_tuple(-1, 0), std::make_tuple(0, 1),
        std::make_tuple(1, 0), std::make_tuple(0, -1)
    };
    std::vector<std::tuple<int, int>> v_diagonal = {
        std::make_tuple(-1, 1), std::make_tuple(1, 1),
        std::make_tuple(1, -1), std::make_tuple(-1, -1)
    };

    AStar(std::tuple<int, int> start, std::tuple<int, int> end, const int map2d[50][50], int obstruction = 1)
        : nstart(start), nend(end)
        {
            start_x = std::get<0>(start);
            start_y = std::get<1>(start);
            for (int i = 0; i < 50; i++)
            {
                for (int j = 0; j < 50; j++)
                {
                    nmap2d[i][j] = map2d[i][j];
                }
            }

        }
    ~AStar() {}
    bool is_in_map(int x, int y)
    {
        return (0 <= x & x < 50) & (0 <= y & y < 50);
    }
    bool in_closelist(int x, int y)
    {
        auto point = std::make_tuple(x, y);
        return this->closelist.find(point) != this->closelist.end();
    }
    void upd_openlist(Node node)
    {
        auto temp_node = this->openlist.find(std::make_tuple(node.nx, node.ny));
        if (temp_node != this->openlist.end())
        {
            this->openlist[std::make_tuple(node.nx, node.ny)] = node;
        }else
        {
            temp_node->second = node;
        }
    }
    void add_in_openlist(Node node)
    {
        auto temp_node = this->openlist.find(std::make_tuple(node.nx, node.ny));
        if (temp_node != this->openlist.end())
        {
            this->openlist[std::make_tuple(node.nx, node.ny)] = node;
        }else
        {
            temp_node->second = node;
        }
    }
    void add_in_closelist(Node node)
    {
        auto temp_node = this->closelist.find(std::make_tuple(node.nx, node.ny));
        if (temp_node != this->closelist.end())
        {
            this->closelist[std::make_tuple(node.nx, node.ny)] = node;
        }else
        {
            temp_node->second = node;
        }
    }
    Node* pop_min_F()
    {
        std::tuple<int, int> key_min(-1, -1);
        Node* node_min = nullptr;
        for (auto iter = this->openlist.begin(); iter != this->openlist.end(); iter ++)
        {
            if (key_min == std::make_tuple(-1, -1))
            {
                key_min = iter->first;
                *node_min = iter->second;
            }else if((iter->second).get_F(this->nend) < node_min->get_F(this->nend))
            {
                key_min = iter->first;
                *node_min = iter->second;
            }
        }
        if (key_min != std::make_tuple(-1, -1))
        {
            this->openlist.erase(key_min);
        }
        return node_min;
    }
    std::map<std::tuple<int, int>, Node> get_Q(Node* P)
    {
        std::map<std::tuple<int, int>, Node> temp_points;
        for (auto iter = this->v_hv.begin(); iter != this->v_hv.end(); iter ++)
        {
            int x = P->nx + std::get<0>(*iter);
            int y = P->ny + std::get<1>(*iter);
            if (this->is_in_map(x, y) & (this->nmap2d[x][y] != this->obstruction) &
                !this->in_closelist(x, y))
            {
                temp_points[std::make_tuple(x, y)] = Node(x, y, P);
            }
        }
        for (auto iter = this->v_diagonal.begin(); iter != this->v_diagonal.end(); iter ++)
        {
            int x = P->nx + std::get<0>(*iter);
            int y = P->ny + std::get<1>(*iter);
            if (this->is_in_map(x, y) & (this->nmap2d[x][y] != obstruction) &
                (this->nmap2d[x][P->ny] != obstruction) & (this->nmap2d[P->nx][y] != obstruction) &
                !this->in_closelist(x, y))
            {
                temp_points[std::make_tuple(x, y)] = Node(x, y, P);
            }
        }
        return temp_points;
    }
    void search()
    {
        while (true)
        {
            Node* P = &(this->pop_min_F());
            if (P == nullptr) break;
            this->add_in_closelist(P);
            std::map<std::tuple<int, int>, Node> Q={};
            Q = this->get_Q(P);
            if (Q.begin() == Q.end()) continue;

            auto it = Q.find(this->nend);
            if (it != Q.end())
            {
                *(this->answer) = Node(std::get<0>(this->nend), std::get<1>(this->nend), P);
                break;
            }

            for (auto iter=Q.begin(); iter != Q.end(); iter ++)
            {
                int temp_x = std::get<0>(iter->first);
                int temp_y = std::get<1>(iter->first);
                Node node_Q = iter->second;
                auto it = this->openlist.find(std::make_tuple(temp_x, temp_y));
                if (it != this->openlist.end())
                {
                    this->add_in_openlist(node_Q);
                }else if(node_Q.get_F(this->nend) < (it->second).get_F(this->nend))
                {
                    this->upd_openlist(node_Q);
                }
                
            }
        }
    }

    void run()
    {
        Node node_start = Node(this->start_x, this->start_y, nullptr);
        this->openlist[std::make_tuple(this->start_x, this->start_y)] = node_start;
        this->search();
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
        for (auto it = result_x.begin(); it != result_x.end(); it ++)
            std::cout << "x: " << *it << std::endl;
        for (auto it = result_y.begin(); it != result_y.end(); it ++)
            std::cout << "y: " << *it << std::endl;
        std::cout << "dis: " << dis << std::endl;
    }


};

int main()
{
    return 0;
}