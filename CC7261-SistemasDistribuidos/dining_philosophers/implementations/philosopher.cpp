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
    this->left_fork = false;
    this->right_fork = false;
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
            this->ReturnFork(fork_type::LEFT_FORK);
            this->ReturnFork(fork_type::RIGHT_FORK);
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
    // Verifica e pega na mesa os garfos disponiveis
    switch (this->table->GetFork(this->chair))
    {
    case fork_type::LEFT_FORK :
        this->left_fork = true;
        break;
    case fork_type::RIGHT_FORK :
        this->right_fork = true;
        break;
    case fork_type::NO_FORK :
        break;
    default:
        break;
    }
}

void Philosopher::ReturnFork(fork_type fork)
{
    this->table->ReturnFork(this->chair, fork);
    this->left_fork = fork == fork_type::LEFT_FORK ? false : this->left_fork;
    this->right_fork = fork == fork_type::RIGHT_FORK ? false : this->right_fork;
}

int Philosopher::CountForks()
{
    return (int)(this->right_fork + this->left_fork);
}

bool Philosopher::HoldingLeftFork()
{
    return this->left_fork;
}

bool Philosopher::HoldingRightFork()
{
    return this->right_fork;
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