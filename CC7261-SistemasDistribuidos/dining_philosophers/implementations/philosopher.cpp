#include "../headers/table.h"
#include "../headers/philosopher.h"
#include <windows.h>
#include <string>

class Table;
unsigned int Philosopher::TIME2EAT = 0;
unsigned int Philosopher::TIME2THINK = 0;

Philosopher::Philosopher(int _chair, Table* _table) 
    : chair(_chair), table(_table)
{
    this->forks[0] = fork_type::NO_FORK;
    this->forks[1] = fork_type::NO_FORK;
    this->current_state = philosopher_state::hungry;
}

void Philosopher::Simulate(Philosopher* philosopher)
{
    while (philosopher->current_state != philosopher_state::dead)
    {
        philosopher->Iterate();
    }
}

void Philosopher::Iterate()
{
    switch (this->current_state)
    {
        case philosopher_state::eating :
            Sleep(Philosopher::TIME2EAT);
            this->ReturnForks();
            if (this->CountForks() == 0)
                this->ChangeState(philosopher_state::thinking);
            break;

        case philosopher_state::thinking :
            Sleep(Philosopher::TIME2THINK);
            this->ChangeState(philosopher_state::hungry);
            break;

        case philosopher_state::hungry :
            this->GetFork();
            if (this->CountForks() == 2)
            {
                this->ChangeState(philosopher_state::eating);
                return;
            }
            break;
        default:
            break;
    }
}

void Philosopher::ChangeState(philosopher_state new_state)
{
    this->current_state = new_state;
}

void Philosopher::GetFork()
{
    fork_type table_fork = this->table->GetFork(this->chair);
    if (this->forks[0] == fork_type::NO_FORK)
        this->forks[0] = table_fork;
    else if (this->forks[1] == fork_type::NO_FORK)
        this->forks[1] = table_fork;
}

void Philosopher::ReturnForks()
{
    for (int i = 0; i < 2; i++)
    {
        this->table->ReturnFork(this->chair, this->forks[i]);
        this->forks[i] = fork_type::NO_FORK;
    }
}

int Philosopher::CountForks()
{
    int total = (int)(this->forks[0] != fork_type::NO_FORK) + (int)(this->forks[1] != fork_type::NO_FORK);
    return total;
}

philosopher_state Philosopher::GetState() 
{
    return this->current_state;
}

std::string Philosopher::GetStateString()
{
    switch (this->current_state)
    {
        case philosopher_state::eating :
            return "Eating  ";
        case philosopher_state::thinking :
            return "Thinking";
        case philosopher_state::hungry :
            return "Hungry  ";
        case philosopher_state::dead :
            return "Dead    ";
    }

    return "ERROR";
}