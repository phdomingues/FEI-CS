#include "Virus.h"



Virus::Virus(int y, int x)
{
	setPos(x, y);
	cor = 1;
	velocidade = 1;
}

void Virus::setPos(int x, int y)
{
	// x varia de 0 a 60 no array ( comprimento )
	if (x < 0)			{ this->x = x + 60; } // reaparece na direita
	else if (x >= 60)	{ this->x = x - 60; } // reaparece na esquerda
	else				{ this->x = x; }

	// y varia de 0 a 30 no array ( altura )
	if (y < 0)			{ this->y = y + 30; } // reaparece em baixo
	else if (y >= 30)	{ this->y = y - 30; } // reaparece em cima
	else				{ this->y = y; }
}

int Virus::getVelocidade() { return velocidade; }

int Virus::getCor() { return cor; }

int Virus::getX() {	return x; }

int Virus::getY() { return y; }

void Virus::mover()
{
	for (int i = 0; i < getVelocidade(); i++)
	{
		int mov = 0;
		int direcao = rand() % 2; // inteiro aleatorio de 0 a 1
		while (mov == 0) { mov = (rand() % 3) - 1; } // -1, 0, 1
		if (direcao == 0) { setPos(getX() + mov, getY()); }
		else { setPos(getX(), getY() + mov); }
	}
}


Virus::~Virus()
{
}
