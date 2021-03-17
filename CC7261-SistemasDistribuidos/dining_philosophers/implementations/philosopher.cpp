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
    this->forks = 0;
    this->current_state = Philosopher::hungry;
    std::cout << "Hello! I am philosopher #" << this->chair << " - " << this->table->n_chairs << std::endl;
}

void Philosopher::Iterate()
{
    switch (this->current_state)
    {
        case Philosopher::eating :
            Sleep(Philosopher::TIME2EAT);
            this->ReturnForks();
            this->ChangeState(Philosopher::thinking);
            break;

        case Philosopher::thinking :
            Sleep(Philosopher::TIME2THINK);
            this->ChangeState(Philosopher::hungry);
            break;

        case Philosopher::hungry :
            this->GetFork();
            if (this->forks == 2)
            {
                this->ChangeState(Philosopher::eating);
            }
            break;
        default:
            break;
    }
}

void Philosopher::ChangeState(Philosopher::state new_state)
{
    this->current_state = new_state;
}

void Philosopher::GetFork()
{
    // Verifica e pega na mesa os garfos disponiveis
    this->forks += this->table->GetFork(this->chair);
}

void Philosopher::ReturnForks()
{
   this->table->ReturnForks(this->chair, this->forks);
   this->forks = 0;
}

std::string Philosopher::GetState()
{
    switch (this->current_state)
    {
        case Philosopher::eating :
            return "Eating";
        case Philosopher::thinking :
            return "Thinking";
        case Philosopher::hungry :
            return "Hungry";
        case Philosopher::dead :
            return "Dead";
    }

    return "ERROR";
}

void Philosopher::Simulate(Philosopher* philosopher)
{
    while (philosopher->current_state != Philosopher::dead)
    {
        philosopher->Iterate();
    }
}