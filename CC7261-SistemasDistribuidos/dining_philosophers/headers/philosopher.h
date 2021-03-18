#pragma once
#include <stdint.h>
#include <string>
#include "table.h"
#include "definitions.h"

class Table;

class Philosopher 
{
/* ATRIBUTOS */
public:
    enum state
    {
        hungry,     // Esta esperando a liberacao de garfos para poder comer
        eating,     // Possui dois garfos, logo está comendo
        thinking,   // Nao possui nenhum garfo, mas tambem nao esta solicitando 
        dead        // Ficou muito tempo sem comer, logo morreu
    };
    // Ciclos que definem a atividade de qualquer filosofo
    //static unsigned int TIME2DIE;   // Quantos ciclos fica vivo sem comer antes de morrer
    static unsigned int TIME2EAT;   // Quantos ciclos o filosofo passa comendo
    static unsigned int TIME2THINK; // Quantos ciclos o filosofo passa pensando

private:

    // Definicao do filosofo no momento atual
    Table* table;               // Mesa que o filosofo esta sentado
    int chair;                  // Cadeira que ele esta sentado
    bool left_fork;             // Segurando garfo esquerdo
    bool right_fork;            // Segurando o garfo direito
    state current_state;        // Qual o estado deste filosofo

/* CONSTRUTORES */
public:
    Philosopher(int chair, Table* table);

/* METODOS */
public:
    void Iterate();
    std::string GetState();
    int CountForks();
    void ChangeState(state new_state);
    void GetFork();
    void ReturnForks();
    static void Simulate(Philosopher* philosopher);
    bool HoldingLeftFork();
    bool HoldingRightFork();

};