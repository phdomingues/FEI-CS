#include "Influenza.h"



Influenza::Influenza(int y, int x) : Virus(y,x)
{
	celula = false;
}


void Influenza::setCelula(bool val) { celula = val; }

bool Influenza::estaNaCelula() { return celula; }

Influenza::~Influenza()
{
}
