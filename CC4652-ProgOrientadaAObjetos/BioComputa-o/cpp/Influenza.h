#pragma once
#include "Virus.h"
class Influenza : public Virus
{
public:
	Influenza(int, int);
	void setCelula(bool);
	bool estaNaCelula();
	~Influenza();

private:
	bool celula;
};

