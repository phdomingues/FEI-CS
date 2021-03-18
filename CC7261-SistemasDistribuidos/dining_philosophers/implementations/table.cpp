#include "../headers/table.h"
#include "../headers/philosopher.h"
#include "../headers/table_utils.h"
#include <chrono>

Table::Table(int chairs, unsigned int time2eat, unsigned int time2think, unsigned int log_interval)
    : n_chairs(chairs), log_interval(log_interval)
{
    // Prepara o vetor de garfos (1 garfo para cada filosofo)
    this->forks = new bool[chairs];
    for (int i = 0; i < chairs; i++)
    {
        this->forks[i] = true;
    }

    // Instancia todos os filosofos
    for (int i = 0; i < chairs; i++)
    {
        this->philosophers.push_back(Philosopher(i, this));
    }
    // Define os tempos padrao
    this->philosophers[0].TIME2EAT = time2eat;
    this->philosophers[0].TIME2THINK = time2think;
}

fork_type Table::GetFork(int chair)
{
    int left = chair == 0 ? this->n_chairs-1 : chair-1;
    int right = chair;

    if (this->forks[left] == true)
    {
        this->forks[left] = false;
        return fork_type::LEFT_FORK;
    }
    if (this->forks[right] == true)
    {
        this->forks[right] = false;
        return fork_type::RIGHT_FORK;
    }

    return fork_type::NO_FORK;
}

void Table::ReturnForks(int chair)
{
    int left = chair == 0 ? this->n_chairs-1 : chair-1;
    int right = chair;

    this->forks[left] = true;
    this->forks[right] = true;
}

void Table::Cicle(Table* table)
{
    auto start = std::chrono::high_resolution_clock::now();

    bool deadlock = false;

    while (!deadlock)
    {
        auto fork2char = [](bool fork) { return (fork ? "w " : "  "); };
        auto fork2char2 = [](bool fork) { return (fork ? "| " : "_ "); };

        std::cout << "------------------------------------------------------------\n\n";

        deadlock = true;
        for (int i = 0; i < table->n_chairs; i++)
        {
            if (table->philosophers[i].CountForks() != 1)
                deadlock = false;

            std::cout << "                 " 
                      << fork2char(table->philosophers[i].HoldingLeftFork()) << fork2char(table->philosophers[i].HoldingRightFork()) << std::endl
                      << "Philosopher #" << fixedLength(i,2) << ": " << fork2char2(table->philosophers[i].HoldingLeftFork()) << fork2char2(table->philosophers[i].HoldingRightFork()) 
                      << table->philosophers[i].GetState() << std::endl << std::endl;
        }

        std::cout << std::endl << "Table:\n======\n\n";
        for (int i = 0; i < table->n_chairs; i++)
        {
            std::cout << " #" << fixedLength(i,2) << "  " << fork2char(table->forks[i]);
        } std::cout << std::endl;
        for (int i = 0; i < table->n_chairs; i++)
        {
            std::cout << "      " << fork2char2(table->forks[i]);
        }
        std::cout << std::endl << std::endl;

        std::chrono::duration<double> elapsed = std::chrono::high_resolution_clock::now() - start;
        std::cout << "Elapsed time: " << elapsed.count() << " s\n";
        Sleep(table->log_interval);

    }

    std::cout << "\n****** DEADLOCK ******\n";
}

void Table::PlaySimulation()
{
    std::thread* philosopher_threads = new std::thread[this->n_chairs];

    std::thread table_log = std::thread(Table::Cicle, this);

    for (int i = 0; i < this->n_chairs; i++)
    {
        philosopher_threads[i] = std::thread(Philosopher::Simulate, &(this->philosophers[i]));
    }

    for (int i = 0; i < this->n_chairs; i++)
    {
        philosopher_threads[i].join();
    }

    std::cout << "O crap" << std::endl;

}