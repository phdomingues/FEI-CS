#include "Leucocito.h"

Leucocito::Leucocito(int y, int x) : Celula(y, x, 2)
{
	nascimento = time(NULL);
	velocidade = 2;
}

int Leucocito::getVelocidade() { return velocidade; }

time_t Leucocito::getNascimento() {	return nascimento; }

bool Leucocito::vivo()
{ // true = ainda não passou 7s --- false = passou 7s 
	return (time(0)-nascimento) <= 7;
}

void Leucocito::mover()
{
	for (int i = 0; i < velocidade; i++)
	{
		int movX = 0;
		int movY = 0;
		while (movX == 0 && movY == 0)
		{
			movX = (rand() % 3) - 1; // -1 /ou/ 0 /ou/ 1
			movY = (rand() % 3) - 1; // -1 /ou/ 0 /ou/ 1    
		}
		setPos(getX() + movX, getY() + movY);
	}
}

Leucocito::~Leucocito()
{
}
