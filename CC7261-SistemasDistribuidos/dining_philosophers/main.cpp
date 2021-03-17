#include "headers/table.h"

int main(int argc, char* argv[])
{
    Table t = Table(5, 5, 3);

    std::cout << "Starting simulation" << std::endl;
    t.PlaySimulation();
    std::cout << "Ending simulation" << std::endl;
    return 0;
}