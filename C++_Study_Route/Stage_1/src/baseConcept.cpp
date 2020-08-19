#include "../headfile/Normal.hpp"


void VirableConcept()
{
    // array
    std::cout << "---------------------array--------------------" << std::endl;
    int luckyNums[] = {1, 2, 3, 4, 5};
    std::string luckybuddies[] = {"Tom", "Miles", "Jony"};
    for (const auto &e : luckyNums)
    {
        std::cout << e << ",";
    }

    // sayHi("Miles");
    // std::cout << calValue(2, 3) << std::endl;
    // std::cout << getDayOfWeek(3) << std::endl;
    // countNum(6);

    // 2D Array and nested loop
    std::cout << "--------------------2D array-------------------" << std::endl;
    int numGrid[2][2] = {
        0,
        1,
        2,
        3,
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
    for (const auto &a : numGrid)
    {
        for (const auto &e : a)
        {
            std::cout << e << ",";
        }
    }

    // vector
    std::cout << "-----------------vector---------------" << std::endl;
    // vector<std::string> Temp;
    // std::string temp;
    // while (getline(cin, temp))
    // {
    //     if (temp.size() == 0)
    //     {
    //         break;
    //     }
    //     Temp.push_back(temp);
    // }
    // for (const auto &i : Temp)
    // {
    //     std::cout << i;
    // }
    // std::cout << std::endl;

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

	int testNum = 1;
	int testNum2 = 1;
	for (int i = 1; i<10; i++)
	{
		testNum = ++i;
		std::cout << "i=" << i << ",testNum=" << testNum  << std::endl;
	}
	for (int i = 1; i<10; i++)
	{
		testNum2 = i++;
		std::cout << "i=" << i << ",testNum2=" << testNum2 << std::endl;
	}
}
