#include "../headfile/baseConcept.hpp"


void VARS()
{
    std::cout << "show each virable length." << std::endl;
    std::cout << "Char length: " << sizeof(char) << std::endl;
    std::cout << "Boolean length: " << sizeof(bool) << std::endl;
    std::cout << "int length: " << sizeof(int) << std::endl;
    std::cout << "short length: " << sizeof(short) << std::endl;
    std::cout << "long length: " << sizeof(long) << std::endl;
    std::cout << "float length: " << sizeof(float) << std::endl;
    std::cout << "double length: " << sizeof(double) << std::endl;
}

void KEYWORD()
{
    std::cout << "" << std::endl;
}

void CLASS()
{
    class Sample
    {
    public:
        Sample();
        ~Sample();
    private:
        int a;
        float b;
    };
}

void CONDITIONALOPERATOR()
{
    std::cout << "------------conditional operator ?:-----------" << std::endl;
    std::cout << "常规用法：int a = true ? 10 : 20;" << std::endl;
    int temp = true ? 10 : 20;
    std::cout << temp << std::endl;
    std::cout << "将三元运算当作左值 (condition ? a : b) = value" << std::endl;
    int a, b;
    const bool condition = true;
    // 可以利用先期条件决定给哪个变量进行赋值
    (condition ? a : b) = 10;
    std::cout << "a: " << a << ", b: " << b << std::endl;
}

void ARRAY()
{
    std::cout << "---------------------array--------------------" << std::endl;
    int luckyNums[] = {1, 2, 3, 4, 5};
    std::string luckybuddies[] = {"Tom", "Miles", "Jony"};
    for (const auto &e : luckyNums)
    {
        std::cout << e << ",";
    }
    std::cout << std::endl;
}

void ARRAY2D()
{
    // 2D Array and nested loop
    std::cout << "--------------------2D array-------------------" << std::endl;
    int numGrid[2][2] = {
        0, 1,
        2, 3,
    };
    int figures[7][4] =
        {
            1, 3, 5, 7, // I
            2, 4, 5, 7, // Z
            3, 5, 4, 6, // S
            3, 5, 4, 7, // T
            2, 3, 5, 7, // L
            3, 5, 7, 6, // J
            2, 3, 4, 5, // O
        };
    std::cout << "figures[0][0] :" << figures[0][0] << ",";
    std::cout << "figures[1][0] :" << figures[1][0] << std::endl;

    // nested loop
    for (const auto &a : numGrid)
    {
        for (const auto &e : a)
        {
            std::cout << e << ",";
        }
    }
    std::cout << std::endl;
}

void VECTOR()
{
    // vector
    std::cout << "-----------------vector---------------" << std::endl;
    std::vector<std::string> Temp;
    std::string temp;
    std::cout << "Enter some line stuff:" << std::endl;
    while (std::getline(std::cin, temp))
    {
        if (temp.size() == 0)
        {
            break;
        }
        Temp.push_back(temp);
    }
    for (const auto &i : Temp)
    {
        std::cout << i;
    }
    std::cout << std::endl;
}


void ITERATOR()
{
    
    // iterator
    std::cout << "----------------interator--------------" << std::endl;
    std::string temp_s("some std::string");
    if (temp_s.begin() != temp_s.end())
    {
        auto it = temp_s.begin();
        *it = toupper(*it);
    }
    std::cout << temp_s;
    std::cout << std::endl;
}


void MODULUS()
{
    std::cout << "----------------Modulus Operation---------------" << std::endl;
    // 对任何数进行取摸运算，都会生成0-n的数字
    for (int i = 1; i < 101; i++)
    {
        std::cout << i % 5 << " ";
        if (i % 10 == 0)
        {
            std::cout << std::endl;
        }
    }
    std::cout << std::endl;
}


void FPPBPP()
{
    std::cout << "test for ++ in front of variable and behind it." << std::endl;
    int testNum = 1;
	int testNum2 = 1;
    std::cout << "In Front of:" << std::endl;
    for (int i = 1; i<10; i++)
	{
		testNum = ++i;
		std::cout << "i=" << i << ",testNum=" << testNum  << std::endl;
	}
    std::cout << "Behind:" << std::endl;
    for (int i = 1; i<10; i++)
	{
		testNum2 = i++;
		std::cout << "i=" << i << ",testNum2=" << testNum2 << std::endl;
	}
}
