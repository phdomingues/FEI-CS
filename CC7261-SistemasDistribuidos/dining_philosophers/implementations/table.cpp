#include <mutex>
#include <chrono>
#include "../headers/table.h"
#include "../headers/philosopher.h"
#include "../headers/table_utils.h"

Table::Table(int chairs, unsigned int time2eat, unsigned int time2think, unsigned int log_interval, log_level log_type)
    : n_chairs(chairs), log_interval(log_interval), log_type(log_type)
{
    // Prepara o vetor de garfos (1 garfo para cada filosofo)
    this->forks = new bool[chairs];
    for (int i = 0; i < chairs; i++)
    {
        this->forks[i] = true;
    }

    this->last_state[this->n_chairs];

    // Instancia todos os filosofos
    for (int i = 0; i < chairs; i++)
    {
        this->philosophers.push_back(Philosopher(i, this));
        this->last_state[i] = this->philosophers[i].GetState();
    }
    // Define os tempos padrao
    this->philosophers[0].TIME2EAT = time2eat;
    this->philosophers[0].TIME2THINK = time2think;
}

Table::Table(const Table &t1)
{
    this->forks = t1.forks;
    this->last_state = t1.last_state;
    this->philosophers = t1.philosophers;
    this->n_chairs = t1.n_chairs;
    this->log_interval = t1.log_interval;
    this->log_type = t1.log_type;
}

fork_type Table::GetFork(int chair)
{
    // garfo a direita = proprio indice, garfo a esquerda = indice - 1 (se -1 for invalido da a volta no array - lista circular)
    int left = chair == 0 ? this->n_chairs-1 : chair-1;
    int right = chair;

    std::lock_guard<std::mutex> lock (mtx);
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

void Table::ReturnFork(int chair, fork_type fork)
{
    int left = chair == 0 ? this->n_chairs-1 : chair-1;
    int right = chair;
    
    std::lock_guard<std::mutex> lock (this->mtx);
    this->forks[left] = fork == fork_type::LEFT_FORK ? true : this->forks[left];
    this->forks[right] = fork == fork_type::RIGHT_FORK ? true : this->forks[right];
}

bool Table::state_changed()
{
    bool changed = false;
    for (int i = 0; i < this->n_chairs; i++)
    {
        if (this->last_state[i] != this->philosophers[i].GetState())
        {
            this->last_state[i] = this->philosophers[i].GetState();
            changed = true;
        }
    }
    return changed;
}

void Table::simple_log(Table* table, std::chrono::high_resolution_clock::time_point start)
{
    // Imprime apenas se for relevante (se mudou o estado de alguem)
    if (this->state_changed())
    {
        for (int i = 0; i < table->n_chairs; i++)
        {
            std::cout << "#" << i << ":" << table->philosophers[i].GetStateString() << "  ";
        }
        std::chrono::duration<double> elapsed = std::chrono::high_resolution_clock::now() - start;
        std::cout << "Elapsed time: " << elapsed.count() << " s\n";
    }
}

void Table::illustrated_log(Table* table, std::chrono::high_resolution_clock::time_point start)
{
    // Lambdas de impressao dos garfos
    auto fork2char = [](bool fork) { return (fork ? "w " : "  "); };
    auto fork2char2 = [](bool fork) { return (fork ? "| " : "_ "); };
    // Lambda de contagem de garfos disponiveis
    auto countforks = [table]() 
    {
        int c = 0;
        for (int i = 0; i < table->n_chairs; i++)
            c += table->forks[i];
        return c;
    };

    std::cout << "------------------------------------------------------------\n\n";

    // Imprime informacoes dos filosofos e garfos na mao deles
    for (int i = 0; i < table->n_chairs; i++)
    {
        std::cout   << "                 " 
                    << fork2char(table->philosophers[i].HoldingLeftFork()) << fork2char(table->philosophers[i].HoldingRightFork()) << std::endl
                    << "Philosopher #" << fixedLength(i,2) << ": " << fork2char2(table->philosophers[i].HoldingLeftFork()) << fork2char2(table->philosophers[i].HoldingRightFork()) 
                    << table->philosophers[i].GetStateString() << std::endl << std::endl;
    }

    // Imprime informacoes sobre a mesa
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

    // Imprime informacoes de simulacao + garfos disponiveis (facilita a visualizacao)
    std::chrono::duration<double> elapsed = std::chrono::high_resolution_clock::now() - start;
    std::cout << "Elapsed time: " << elapsed.count() << " s\n";
    std::cout << "Forks at table: " << countforks() << std::endl;
    Sleep(table->log_interval);
}

void Table::Cicle(Table* table)
{
    auto start = std::chrono::high_resolution_clock::now();

    bool deadlock = false;

    while (!deadlock)
    {
        // Escolhe metodo de impressao
        switch (table->log_type)
        {
        case log_level::SIMPLE :
            table->simple_log(table, start);
            break;
        case log_level::ILLUSTRATED :
            table->illustrated_log(table, start);
            break;
        default:
            break;
        }

        // verifica se há deadlock
        deadlock = true;
        for (int i = 0; i < table->n_chairs; i++)
        {
            if (table->philosophers[i].CountForks() != 1)
                deadlock = false;
        }
    }

    std::cout << "\n****** DEADLOCK ******\n";

    // Mata todos os processos (filosofos) para finalizar a execucao
    for (int i = 0; i < table->n_chairs; i++)
    {
        table->philosophers[i].ChangeState(philosopher_state::dead);
    }
}

void Table::PlaySimulation()
{
    // vetor de armazenamento das threads
    std::thread* philosopher_threads = new std::thread[this->n_chairs];

    // inicializacao da thread da mesa
    std::thread table_log = std::thread(Table::Cicle, this);

    // inicializacao das threads dos filosofos
    for (int i = 0; i < this->n_chairs; i++)
    {
        philosopher_threads[i] = std::thread(Philosopher::Simulate, &(this->philosophers[i]));
    }

    // aguarda a mesa decidir que ocorreu deadlock (nao precisa esperar os filosofos, essa informacao eh implicita a mesa)
    table_log.join();

}