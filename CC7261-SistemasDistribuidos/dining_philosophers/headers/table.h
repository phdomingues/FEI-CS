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

/* Construtores */
public:
    Table(int chairs, unsigned int time2eat, unsigned int time2think, unsigned int log_interval=1000);

/* Metodos */
public:
    void PlaySimulation();
    fork_type GetFork(int chair);
    void ReturnForks(int chair);
    static void Cicle(Table* table);
};