#pragma once
#include <iostream>
#include <thread>
#include <windows.h>
#include <vector>
#include "philosopher.h"

class Table;

class Table
{
/* ATRIBUTOS */
public:
    int n_chairs;               // Numero de cadeiras na mesa
    unsigned int log_interval;  // Intervalo entre logs em ms
private:
    bool* forks;                // Array com os garfos
    std::vector<Philosopher> philosophers;  // Array com os filosofos sentados a mesa
    log_level log_type;
    philosopher_state* last_state;

/* Construtores */
public:
    Table( 
        int chairs, 
        unsigned int time2eat, 
        unsigned int time2think, 
        unsigned int log_interval=1000, 
        log_level log_type=log_level::SIMPLE
    );

/* Metodos */
public:
    void PlaySimulation();
    fork_type GetFork(int chair);
    void ReturnFork(int chair, fork_type fork);
    static void Cicle(Table* table);

private:
    void simple_log(Table* table, std::chrono::high_resolution_clock::time_point start);
    void illustrated_log(Table* table, std::chrono::high_resolution_clock::time_point start);
    bool state_changed();
};