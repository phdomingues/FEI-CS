#pragma once
#include <ctime>
#include <stdlib.h>
#include "Celula.h"
#include "IMovable.h"

class Leucocito : public Celula, public IMovable
{
public:
	Leucocito(int, int);
	int getVelocidade();
	time_t getNascimento();
	bool vivo();
	void mover();
	~Leucocito();

private:
	int velocidade;
	time_t nascimento;
};

