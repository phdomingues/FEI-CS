#include "Celula.h"



Celula::Celula(int y, int x, int cor)
{
	this->y = y;
	this->x = x;
	this->cor = cor;
}

/* Set methods */
void Celula::setCor(int cor) { this->cor = (cor >= 0) ? this->cor : 0; }

void Celula::setPos(int x, int y)
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

/* Get methods */
int Celula::getCor() { return cor; }
int Celula::getX() { return x; }
int Celula::getY() { return y; }

Celula::~Celula()
{
}
