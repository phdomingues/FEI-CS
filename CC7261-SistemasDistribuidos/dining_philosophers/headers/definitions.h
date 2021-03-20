#pragma once

enum philosopher_state
{
    hungry,     // Esta esperando a liberacao de garfos para poder comer
    eating,     // Possui dois garfos, logo está comendo
    thinking,   // Nao possui nenhum garfo, mas tambem nao esta solicitando 
    dead        // Ficou muito tempo sem comer, logo morreu
};

enum fork_type {
    LEFT_FORK,
    RIGHT_FORK,
    NO_FORK
};

enum log_level {
    NONE,
    SIMPLE,
    ILLUSTRATED
};