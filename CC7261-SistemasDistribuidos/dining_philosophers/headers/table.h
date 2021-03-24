#pragma once
#include <iostream>
#include <thread>
#include <windows.h>
#include <vector>
#include <mutex>
#include "philosopher.h"

class Table;

class Table
{
/* ATRIBUTOS */
public:
    int n_chairs;               // Numero total de cadeiras na mesa
    unsigned int log_interval;  // Intervalo entre logs em ms
private:
    std::mutex mtx;
    bool* forks;                // Array com a disponibilidade dos garfos na mesa
    bool center_fork;
    bool center_fork_enabled;
    std::vector<Philosopher> philosophers;  // Array com os filosofos sentados a mesa
    log_level log_type; // Tipo de log inicializado
    philosopher_state* last_state; // Estado dos filosofos no ultimo ciclo

/* Construtores */
public:
    // default
    Table( 
        int chairs, 
        unsigned int time2eat, 
        unsigned int time2think, 
        unsigned int log_interval=1000, 
        log_level log_type=log_level::SIMPLE,
        bool central_fork=true
    );
    // Construtor de copia (obrigatorio, pois caso nao tenha o compilador vai tentar criar um construtor de copia padrao, 
    // mas como mutex nao eh copiavel gera erro de compilacao)
    Table(const Table &t1);

/* Metodos */
public:
// Simulacao
    void PlaySimulation(); // Cria filosofos, inicia threads e simula ate um deadlock ocorrer
    static void Cicle(Table* table); // Realiza um ciclo da simulacao, realizando o log escolhido

// Gerenciamento de garfos
    fork_type GetFork(int chair); // Pega um garfo da mesa
    void ReturnFork(int chair, fork_type fork); // Devolve um garfo para a mesa

private:
    void simple_log(Table* table, std::chrono::high_resolution_clock::time_point start); // Metodo que realiza uma passagem do log em modo simples
    void illustrated_log(Table* table, std::chrono::high_resolution_clock::time_point start); // Metodo que realiza uma passagem do log em modo ilustrado
    bool state_changed(); // Verifica se algum filosofo mudou seu estado desde o ultimo ciclo
};