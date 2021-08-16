#pragma once
#include <vector>
#include <iostream>
#include <string>
#include "CelulaBoca.h"
#include "CelulaNasal.h"
#include "CelulaOcular.h"
#include "Influenza.h"
#include "Leucocito.h"

class Cabeca
{
public:
	Cabeca();
	int mapa[30][60];
	void contamina(Influenza);
	void desenhaCabeca();
	~Cabeca();

private:
	std::vector<Celula> _celulas;
	std::vector<Leucocito> _leucocitos;
	std::vector<Influenza> _virus;
	void atualizaLeucocitos();
	void atualizaMapa();
	void atualizaVirus();
	void criaLeucocito();
	void inicializaBoca();
	void inicializaLeucocitos();
	void inicializaNariz();
	void inicializaOlhos();

};

