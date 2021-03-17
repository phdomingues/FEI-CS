#include "../headers/table.h"
#include "../headers/philosopher.h"

Table::Table(int chairs, unsigned int time2eat, unsigned int time2think)
    : n_chairs(chairs)
{
    // Prepara o vetor de garfos (1 garfo para cada cadeira)
    std::cout << "Prepairing table for philosophers..." << std::endl;
    this->forks = new bool[chairs];
    for (int i = 0; i < chairs; i++)
    {
        this->forks[i] = true;
    }

    // Instancia todos os filosofos
    std::cout << "Philosophers are entering the restaurant..." << std::endl;
    for (int i = 0; i < chairs; i++)
    {
        try
        {
            std::cout << "now you will meet philosopher #" << i << std::endl;
            this->philosophers.push_back(Philosopher(i, this));
            std::cout << "Lets go to the next philosopher" << i << std::endl;
        }
        catch (int e)
        {
            std::cout << "An exception occurred. Exception Nr. " << e << '\n';
        }
    }
    // Define os tempos padrao
    this->philosophers[0].TIME2EAT = time2eat;
    this->philosophers[0].TIME2THINK = time2think;
}

bool Table::GetFork(int chair)
{
    int left = chair == 0 ? this->n_chairs-1 : chair-1;
    int right = chair == chair-1 ? 0 : chair+1;

    if (this->forks[left] == true)
    {
        this->forks[left] = false;
        return true;
    }
    if (this->forks[right] == true)
    {
        this->forks[right] = false;
        return true;
    }

    return false;
}

void Table::ReturnForks(int chair, uint8_t nforks)
{
    int left = chair == 0 ? this->n_chairs-1 : chair-1;
    int right = chair == chair-1 ? 0 : chair+1;

    this->forks[left] = true;
    this->forks[right] = true;
}

void Table::Cicle(Table* table)
{
    while (true)
    {
        for (int i = 0; i < table->n_chairs; i++)
        {
            std::cout << "Philosopher #" << i << ": " << table->philosophers[i].GetState() << std::endl;
        }
        
        std::cout << "Forks: ";
        for (int i = 0; i < table->n_chairs; i++)
        {
            std::cout << table->forks[i] ? "w " : "_ ";
        }
        std::cout << std::endl << std::endl;

        Sleep(10);

    }
}

void Table::PlaySimulation()
{
    std::thread* philosopher_threads = new std::thread[this->n_chairs];

    std::thread table_log = std::thread(Table::Cicle, this);

    for (int i = 0; i < this->n_chairs; i++)
    {
        std::cout << "Philosopher #" << i << " is ready!" << std::endl;
        philosopher_threads[i] = std::thread(Philosopher::Simulate, &(this->philosophers[i]));
    }

    for (int i = 0; i < this->n_chairs; i++)
    {
        philosopher_threads[i].join();
    }

    std::cout << "O crap" << std::endl;

}