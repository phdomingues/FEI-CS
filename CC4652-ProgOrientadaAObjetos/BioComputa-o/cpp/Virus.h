#pragma once
#include <stdlib.h>
#include "IMovable.h"

class Virus : public IMovable
{
public:
	Virus(int, int);
	int getVelocidade();
	int getCor();
	int getX();
	int getY();
	void mover();
	virtual ~Virus();

private:
	int velocidade;
	int cor;
	int x;
	int y;
	void setPos(int, int);
};

