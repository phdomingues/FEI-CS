#include "headers/table.h"

int main(int argc, char* argv[])
{
    // Numero de filosofos na simulacao
    int chairs = 4;
    // tempo (em ms) que um filosofo passa comendo
    unsigned int time2eat = 1000U;
    // tempo (em ms) que um filosofo passa pensando
    unsigned int time2think = 1000U;
    // tempo (em ms) entre intervalos (valido apenas para log ilustrado)
    unsigned int log_interval = 1000U;
    // tipo de log (disponiveis: SIMPLE, ILLUSTRATED, NONE)
    log_level log_type = log_level::ILLUSTRATED;

    Table t = Table(chairs, time2eat, time2think, log_interval=log_interval, log_type=log_type);

    std::cout << "Starting simulation" << std::endl;
    t.PlaySimulation();
    std::cout << "Ending simulation" << std::endl;
    return 0;
}