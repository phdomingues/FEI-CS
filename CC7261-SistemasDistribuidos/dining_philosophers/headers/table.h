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
private:
    bool* forks;                // Array com os garfos
    std::vector<Philosopher> philosophers;  // Array com os filosofos sentados a mesa

/* Construtores */
public:
    Table(int chairs, unsigned int time2eat, unsigned int time2think);

/* Metodos */
public:
    void PlaySimulation();
    bool GetFork(int chair);
    void ReturnForks(int chair, uint8_t nforks);
    static void Cicle(Table* table);
};