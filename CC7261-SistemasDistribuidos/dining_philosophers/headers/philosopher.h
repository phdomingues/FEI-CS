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
    // Ciclos que definem a atividade de qualquer filosofo
    static unsigned int TIME2DIE;   // Quantos ciclos fica vivo sem comer antes de morrer
    static unsigned int TIME2EAT;   // Quantos ciclos o filosofo passa comendo
    static unsigned int TIME2THINK; // Quantos ciclos o filosofo passa pensando

private:
    // Definicao do filosofo no momento atual
    friend class Table;                     // Garante a mesa acesso aos metodos privados do filosofo
    Table* table;                           // Mesa que o filosofo esta sentado
    int chair;                              // Cadeira que ele esta sentado
    bool left_fork;                         // Segurando garfo esquerdo
    bool right_fork;                        // Segurando o garfo direito
    philosopher_state current_state;        // Qual o estado deste filosofo

/* CONSTRUTORES */
public:
    Philosopher(int chair, Table* table);

/* METODOS */
// Simulacao geral
public:
    static void Simulate(Philosopher* philosopher); // Processo que mantem a simulacao do filosofo iterando
    void Iterate(); // Metodo que realiza um ciclo de vida do filosofo (comer, pensar, estar com fome)

// Operacoes com o garfo
public:
    int CountForks(); // Retorna o numero de garfos que o filosofo esta segurando
    bool HoldingLeftFork(); // Verifica se tem um garfo na mao esquerda
    bool HoldingRightFork(); // Verifica se tem um garfo na mao direita
private:
    void GetFork(); // Faz com que o filosofo tente pegar um garfo na mesa
    void ReturnFork(fork_type fork); // Devolve o garfo definido para a mesa

// Funcoes do estado atual do filosofo
public:
    std::string GetStateString(); // Retorna o estado do filosofo em formato string
    philosopher_state GetState(); // Retorna o estado do filosofo como enumerador philosopher_state
private:
    void ChangeState(philosopher_state new_state); // Modifica o estado atual do filosofo (para uso da funcao de iteracao apenas)

};