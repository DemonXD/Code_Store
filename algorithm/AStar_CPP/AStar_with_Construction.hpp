#include <iostream>
#include <vector>
#include <array>
#include <tuple>
#include <map>
#include <algorithm> // reverse
#include <stdlib.h> // abs

struct Node
{
    int nx, ny, nh, ng, nf;
    // int nf = ng + nh;
    Node* nparent = nullptr;
    Node(){}
    Node(const Node* other);
    Node(int x, int y, Node* parent);
    ~Node(){}
    Node operator=(const Node* onode);
    int get_G();
    int get_H(std::tuple<int, int> end);
    int get_F(std::tuple<int, int> end);
    int manhattan(int from_x, int from_y, int end_x, int end_y);
};

void PrintArray(int map2d[15][15]);
void Printtuple(const std::tuple<int, int>& temp);
void Printmap(const std::map<std::tuple<int, int>, Node*>& temp);


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

    AStar(std::tuple<int, int> start, std::tuple<int, int> end, const int map2d[15][15]);
    ~AStar() { ; }
    bool is_in_map(int x, int y);
    bool in_closelist(int x, int y);
    void upd_openlist(Node* node);
    void add_in_openlist(Node* node);
    void add_in_closelist(Node* node);
    void pop_min_F(Node* node_min);
    void get_Q(Node* P, std::map<std::tuple<int, int>, Node*>& temp_points);
    void search();
    void run();
    void paintway();
};