#include "AStar_with_Construction.hpp"

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

void Printtuple(const std::tuple<int, int>& temp)
{
    std::cout << "(" << std::get<0>(temp) << ", ";
    std::cout << std::get<1>(temp) << ")";
}

void Printmap(const std::map<std::tuple<int, int>, Node*>& temp)
{
    for (auto it = temp.begin(); it != temp.end(); it++)
    {
        std::cout << "(" << it->second->nx << ", " << it->second->ny << ")" << " ";
    }
    std::cout << std::endl;
}

Node::Node(const Node* other)
    {
        this->nx = other->nx;
        this->ny = other->ny;
        this->nparent = other->nparent;
    }
Node::Node(int x, int y, Node* parent)
        : nx(x), ny(y), nh(0), ng(0), nparent(parent), nf(0) {}
Node Node::operator=(const Node* onode)
    {
        nx = onode->nx;
        ny = onode->ny;
        nh = onode->nh;
        ng = onode->ng;
        nparent = onode->nparent;
        return *this;
    }
int Node::get_G()
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
int Node::get_H(std::tuple<int, int> end)
    {
        if (this->nh == 0)
        {
            this->nh = this->manhattan(this->nx, this->ny, std::get<0>(end), std::get<1>(end)) * 10;
        }
        std::cout << this->nx << "， " << this->ny << "到终点的估值: " << this->nh << std::endl;
        return this->nh;
    }
int Node::get_F(std::tuple<int, int> end)
    {
        if (this->nf == 0)
        {
            this->nf = this->get_G() + this->get_H(end);
        }
        std::cout << this->nx << "， " << this->ny << "到终点的总估值：" << this->nf << std::endl;
        return this->nf;
    }
int Node::manhattan(int from_x, int from_y, int end_x, int end_y)
    {
        int dis = abs(end_x - from_x) + abs(end_y - from_y);
        std::cout << "manhattan距离: " << dis << std::endl;
        return dis;
    }


AStar::AStar(std::tuple<int, int> start, std::tuple<int, int> end, const int map2d[15][15])
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
bool AStar::is_in_map(int x, int y)
{
    bool temp = ((0 <= x) & (x < 15)) & ((0 <= y) & (y < 15));
    return temp;
}

bool AStar::in_closelist(int x, int y)
{
    auto point = std::make_tuple(x, y);
    bool temp = this->closelist.find(point) != this->closelist.end();
    return temp;
}
void AStar::upd_openlist(Node* node)
{
    // Node* temp = node;
    std::cout << "x:" << node->nx << ", y:" << node->ny << " " << "更新openlist节点列表" << std::endl;
    auto it = this->openlist.find(std::make_tuple(node->nx, node->ny));
    if (it != this->openlist.end())
        this->openlist[std::make_tuple(node->nx, node->ny)] = node;
    std::cout << "upd_openlist 执行完成" << std::endl;
}
void AStar::add_in_openlist(Node* node)
{
    // Node* temp = node;
    std::cout << "x:" << node->nx << ", y:" << node->ny << " " << "添加进openlist列表中" << std::endl;
    auto it = this->openlist.find(std::make_tuple(node->nx, node->ny));
    if (it == this->openlist.end())
        this->openlist[std::make_tuple(node->nx, node->ny)] = node;
    std::cout << "add_in_openlist 执行完成" << std::endl;
}
void AStar::add_in_closelist(Node* node)
{
    // Node* temp = node;
    std::cout << "节点: (" << node->nx << ", " << node->ny << ") " << "添加进closelist列表中" << std::endl;
    auto it = this->closelist.find(std::make_tuple(node->nx, node->ny));
    if (it == this->closelist.end()) 
        this->closelist[std::make_tuple(node->nx, node->ny)] = node;
    std::cout << "add_in_closelist 执行完成" << std::endl;
}
void AStar::pop_min_F(Node* node_min) // OK
{
    std::tuple<int, int> key_min(-1, -1);
    for (auto iter = this->openlist.begin(); iter != this->openlist.end(); iter++)
    {
        if (key_min == std::make_tuple(-1, -1))
        {
            key_min = iter->first;
            node_min->nx = iter->second->nx;
            node_min->ny = iter->second->ny;
            node_min->nparent = iter->second->nparent;
        }
        else if ((iter->second)->get_F(this->nend) < node_min->get_F(this->nend))
        {
            key_min = iter->first;
            node_min->nx = iter->second->nx;
            node_min->ny = iter->second->ny;
            node_min->nparent = iter->second->nparent;
        }
    }
    if (key_min != std::make_tuple(-1, -1))
    {
        this->openlist.erase(key_min);
    }
    std::cout << " 最小F值node点: (" << node_min->nx << ", " << node_min->ny << ")" << std::endl;
}
void AStar::get_Q(Node* P, std::map<std::tuple<int, int>, Node*>& temp_points) // OK
{
    std::cout << "获取P点周围可用点" << std::endl;
    for (auto iter = this->v_hv.begin(); iter != this->v_hv.end(); iter++)
    {
        int x = P->nx + std::get<0>(*iter);
        int y = P->ny + std::get<1>(*iter);
        if (this->is_in_map(x, y) & (this->nmap2d[x][y] != this->obstruction) &
            (!this->in_closelist(x, y)))
        {
            std::cout << "上下左右方位添加： (" << x << ", " << y << ")" << std::endl;
            Node* temp = new Node(x, y, P);
            temp_points[std::make_tuple(x, y)] = temp;
        }
    }
    for (auto iter = this->v_diagonal.begin(); iter != this->v_diagonal.end(); iter++)
    {
        int x = P->nx + std::get<0>(*iter);
        int y = P->ny + std::get<1>(*iter);
        if (this->is_in_map(x, y) & (this->nmap2d[x][y] != this->obstruction) &
            (this->nmap2d[x][P->ny] != this->obstruction) &
            (this->nmap2d[P->nx][y] != this->obstruction) &
            !this->in_closelist(x, y))
        {
            std::cout << "四角方位添加： (" << x << ", " << y << ")" << std::endl;
            Node* temp = new Node(x, y, P);
            temp_points[std::make_tuple(x, y)] = temp;
        }
    }
}
void AStar::search()
{
    int count = 0;
    std::cout << "搜索开始" << std::endl;
    while (true)
    {

        std::cout << "----------------" << count << "-----------------" << std::endl;
        std::cout << "openlist(待探索坐标列表): ";
        Printmap(this->openlist);

        std::cout << "closelist(已探索坐标列表): ";
        Printmap(this->closelist);

        Node* P;
        this->pop_min_F(P);
        if (P == nullptr) break;
        this->add_in_closelist(P);
        std::map<std::tuple<int, int>, Node*> Q = {};
        this->get_Q(P, Q);
        if (Q.begin() == Q.end()) continue;
        std::cout << "P周围可用点: ";
        Printmap(Q);
        // ok
        auto it = Q.find(this->nend);
        if (it != Q.end())
        {
            *(this->answer) = Node(std::get<0>(this->nend), std::get<1>(this->nend), P);
            std::cout << "终点找到: ";
            std::cout << this->answer->nx << ", " << this->answer->ny << std::endl;
            break;
        }
        // ok
        std::cout << "开始比较openlist和Q" << std::endl;
        std::cout << "openlist 中的点：";
        Printmap(this->openlist);
        for (auto iter = Q.begin(); iter != Q.end(); iter++)
        {
            Node* node_Q = new Node(iter->second);
            std::cout << "*****当前点: ";
            Printtuple(iter->first);
            std::cout << std::endl;
            auto it = this->openlist.find(std::make_tuple(std::get<0>(iter->first), std::get<1>(iter->first)));
            // error
            if (it == this->openlist.end()) // 如果openlist中无此点
            {
                this->add_in_openlist(node_Q);
                std::cout << "Q不在openlist中，添加:";
                std::cout << "(" << node_Q->nx << ", " << node_Q->ny << ")" << std::endl;
            }
            else if (node_Q->get_F(this->nend) < it->second->get_F(this->nend))
            {
                std::cout << "node_Q的F值比node_openlist更小，则用node_Q替换node_openlist" << std::endl;
                this->upd_openlist(node_Q);
            }
            std::cout << "*****当前点: " ;
            Printtuple(iter->first);
            std::cout << "检查完毕" << std::endl;
            // delete node_Q;
        }
        std::cout << "目前openlist(待探索坐标列表): ";
        Printmap(this->openlist);
        std::cout << "=========================" << std::endl;
        count += 1;
    }
}

void AStar::run()
{
    PrintArray(this->nmap2d);
    Node* node_start = new Node(this->start_x, this->start_y, nullptr);
    this->openlist[std::make_tuple(this->start_x, this->start_y)] = node_start;
    this->search();
    // delete node_start;
}

void AStar::paintway()
{
    std::vector<int> result_x;
    std::vector<int> result_y;
    int dis = 0;
    while (this->answer != nullptr)
    {
        result_x.push_back(this->answer->nx);
        result_y.push_back(this->answer->ny);
        if (this->answer->ng > dis)
        {
            dis = this->answer->ng;
        }
        this->answer = this->answer->nparent;
    }
    std::reverse(result_x.begin(), result_x.end());
    std::reverse(result_y.begin(), result_y.end());
    for (auto it = result_x.begin(); it != result_x.end(); it++)
        std::cout << "x: " << *it << std::endl;
    for (auto it = result_y.begin(); it != result_y.end(); it++)
        std::cout << "y: " << *it << std::endl;
    std::cout << "dis: " << dis << std::endl;
}





