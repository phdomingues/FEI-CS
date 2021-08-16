#include <iostream>
#include <ctime>
#include <stdlib.h>
#include "Cabeca.h"


int main()
{
	Cabeca cab;

	for (int k = 0; k < 150; k++)
	{
		Influenza inf(rand() % 30, rand() % 60);
		cab.contamina(inf);
	}

	// inicia a contagem do tempo
	int tempo = 0;
	time_t inicio = time(0);
	// inicia as intera��es e plotagem
	while (tempo < 300)
	{ // roda por 5 minutos (300 seg)
		// data atual para compara��o
		tempo = (int)(time(0) - inicio);

		// print na tela
		system("CLS");
		std::cout << "\n\n\nTempo: " << tempo;
		cab.desenhaCabeca();

		// precisa esperar pois o netbeans n�o da conta de imprimir t�o rapido
		for (clock_t clk = clock(); (double)(clock() - clk)/CLOCKS_PER_SEC < 0.1;) {}
		//for (int t = time(0); time(0) - t < 1 ;){}

	}

}