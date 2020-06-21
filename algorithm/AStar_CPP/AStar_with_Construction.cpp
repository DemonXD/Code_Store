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
    this->nf = other->nf;
    this->ng = other->ng;
    this->nh = other->nh;
}
Node::Node(int x, int y, Node* parent)
    : nx(x), ny(y), nh(0), ng(0), nparent(parent), nf(0) {}
Node Node::operator=(const Node* const onode)
{
    nx = onode->nx;
    ny = onode->ny;
    nh = onode->nh;
    ng = onode->ng;
    nf = onode->ng + nh;
    nparent = onode->nparent;
    return *this;
}
int Node::get_G(std::tuple<int, int>& start)
{
    int x_dis = this->nx - std::get<0>(start);
    int y_dis = this->ny - std::get<1>(start);
    this->ng = x_dis + y_dis + (std::sqrt(2) - 2) * std::min(x_dis, y_dis);
    return this->ng;
}
int Node::get_H(std::tuple<int, int>& end)
{
    int x_dis = std::get<0>(end) - this->nx;
    int y_dis = std::get<1>(end) - this->ny;
    this->nh = x_dis + y_dis + (std::sqrt(2) - 2) * std::min(x_dis, y_dis);
    return this->nh;
}
int Node::get_F(std::tuple<int, int>& start, std::tuple<int, int>& end)
{
    if (this->nf == 0)
    {
        this->nf = this->get_G(start) + this->get_H(end);
    }
    return this->nf;
}
int Node::manhattan(int from_x, int from_y, int end_x, int end_y)
{
    int dis = abs(end_x - from_x) + abs(end_y - from_y);
    return dis;
}


AStar::AStar(std::tuple<int, int> start, std::tuple<int, int> end, const int map2d[15][15])
    : nstart(start), nend(end), start_x(std::get<0>(start)), start_y(std::get<1>(start))
{
    for (int i = 0; i < 15; i++)
    {
        for (int j = 0; j < 15; j++)
        {
            this->nmap2d[i][j] = map2d[i][j];
        }
    }
}
bool AStar::is_in_map(int x, int y)
{
    bool temp = ((0 <= x) & (x < this->x_edge)) & ((0 <= y) & (y < this->y_edge));
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
    this->openlist[std::make_tuple(node->nx, node->ny)] = node;
}
void AStar::add_in_openlist(Node* node)
{
    this->openlist[std::make_tuple(node->nx, node->ny)] = node;
}
void AStar::add_in_closelist(Node* node)
{
    this->closelist[std::make_tuple(node->nx, node->ny)] = node;
}
Node* AStar::pop_min_F() // OK
{
    std::tuple<int, int> key_min(-1, -1);
    Node* node_min = nullptr;
    for (auto iter = this->openlist.begin(); iter != this->openlist.end(); iter++)
    {
        if (key_min == std::make_tuple(-1, -1))
        {
            key_min = iter->first;
            node_min = new Node(iter->second);
        }
        else if ((iter->second)->get_F(this->nstart, this->nend) < node_min->get_F(this->nstart, this->nend))
        {
            key_min = iter->first;
            node_min = new Node(iter->second);
        }
    }
    if (key_min != std::make_tuple(-1, -1))
    {
        this->openlist.erase(key_min);
    }
    return node_min;
}
void AStar::get_Q(Node* P, std::map<std::tuple<int, int>, Node*>& temp_points) // OK
{
    for (auto iter = this->v_hv.begin(); iter != this->v_hv.end(); iter++)
    {
        int x = P->nx + std::get<0>(*iter);
        int y = P->ny + std::get<1>(*iter);
        if (this->is_in_map(x, y) & (this->nmap2d[x][y] != this->obstruction) &
            (!this->in_closelist(x, y)))
        {
            temp_points[std::make_tuple(x, y)] = new Node(x, y, P);
        }
    }
    for (auto iter = this->v_diagonal.begin(); iter != this->v_diagonal.end(); iter++)
    {
        int x = P->nx + std::get<0>(*iter);
        int y = P->ny + std::get<1>(*iter);
        if (this->is_in_map(x, y) & (this->nmap2d[x][y] != this->obstruction) &
            (this->nmap2d[x][P->ny] != this->obstruction) &
            (this->nmap2d[P->nx][y] != this->obstruction) &
            (!this->in_closelist(x, y)))
        {
            temp_points[std::make_tuple(x, y)] = new Node(x, y, P);
        }
    }
}
void AStar::search()
{
    while (true)
    {
        std::cout << "********************************" << std::endl;
        Node* P = this->pop_min_F();
        if (P == nullptr) break;
        this->add_in_closelist(P);
        std::map<std::tuple<int, int>, Node*> Q = {};
        this->get_Q(P, Q);
        if (Q.begin() == Q.end()) continue;
        auto it = Q.find(this->nend);
        if (it != Q.end())
        {
            this->answer = new Node(std::get<0>(this->nend), std::get<1>(this->nend), P);
            break;
        }
        for (auto iter = Q.begin(); iter != Q.end(); iter++)
        {
            Node* node_Q = new Node(iter->second);
            auto it = this->openlist.find(std::make_tuple(
                std::get<0>(iter->first), std::get<1>(iter->first)));

            if (it == this->openlist.end()) // 如果openlist中无此点
            {
                this->add_in_openlist(node_Q);
            }
            else if (node_Q->get_F(this->nstart, this->nend) < it->second->get_F(this->nstart, this->nend))
            {
                this->upd_openlist(node_Q);
            }
        }
    }
}

void AStar::run()
{
    // PrintArray(this->nmap2d);
    Node* node_start = new Node(this->start_x, this->start_y, nullptr);
    this->openlist[std::make_tuple(this->start_x, this->start_y)] = node_start;
    this->search();
}

void AStar::paintway()
{
    std::vector<std::tuple<int, int>> result_way;
    int dis = 0;
    while (this->answer != nullptr)
    {
        result_way.push_back(std::make_tuple(this->answer->nx, this->answer->ny));
        if (this->answer->ng > dis)
        {
            dis = this->answer->ng;
        }
        this->answer = this->answer->nparent;
    }
    std::reverse(result_way.begin(), result_way.end());
    for (auto it = result_way.begin(); it != result_way.end(); it++)
        nmap2d[std::get<0>(*it)][std::get<1>(*it)] = 8;
        // Printtuple(*it);
    this->nmap2d[this->start_x][this->start_y] = 4;
    this->nmap2d[std::get<0>(this->nend)][std::get<1>(this->nend)] = 9;
    std::cout << "**************************************" << std::endl;
    PrintArray(this->nmap2d);
    std::cout << "总距离: " << dis << std::endl;
}





