#include "headers/table.h"

int main(int argc, char* argv[])
{
    Table t = Table(4, 10, 10, 1000);

    std::cout << "Starting simulation" << std::endl;
    t.PlaySimulation();
    std::cout << "Ending simulation" << std::endl;
    return 0;
}