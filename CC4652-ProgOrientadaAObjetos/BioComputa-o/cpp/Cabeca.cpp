#include "Cabeca.h"



Cabeca::Cabeca()
{
	inicializaOlhos();
	inicializaBoca();
	inicializaNariz();
	inicializaLeucocitos();
}

void Cabeca::contamina(Influenza v)
{
	_virus.push_back(v);
}

void Cabeca::desenhaCabeca()
{
	/*
	Diagrama de cores:
	0 -> Vazio          - Preto    - "\u001B[40m"
	1 -> Virus          - Vermelho  - "\u001B[41m"
	2 -> Leucocito      - Ciano     - "\u001B[46m"
	3 -> Celula Ocular  - Azul      - "\u001B[44m"
	4 -> Celula Nasal   - Verde     - "\u001B[42m"
	5 -> Celula Boca    - Amarelo   - "\u001B[43m"
	6 -> Borda          - Branco     - "\u001B[47m"

	Reset -> "\u001B[0m"
	*/

	atualizaMapa(); // atualiza os valores do mapa com os valores mais recentes

	std::cout << "\n\nInfluenza (" << _virus.size() << ")";
	std::cout << "  Leucocitos (" << _leucocitos.size() << ")\n\n";
	std::string cor;
	// roda em todo o mapa
	for (int i = 0; i < 30; i++)
	{ // para cada linha
		for (int j = 0; j < 60; j++)
		{ // para cada coluna
			switch (mapa[i][j])
			{ // escolhe a cor corretamente
			case 0:
				cor = " ";
				break;
			case 1:
				cor = "X";
				break;
			case 2:
				cor = "@";
				break;
			case 3:
				cor = "*";
				break;
			case 4:
				cor = "*";
				break;
			case 5:
				cor = "*";
				break;
			case 6:
				cor = "O";
				break;
			default:
				cor = "";
				break;
			}
			// imprime
			std::cout << cor;
		} std::cout << std::endl;
	}

	// atualiza leucocitos e virus
	atualizaVirus(); // atualiza virus / mata virus / trata casos de multiplicação de leucocito
	atualizaLeucocitos(); // atualiza posição dos leucocitos e decide se vive ou morre
}

void Cabeca::atualizaLeucocitos()
{
	int contador = _leucocitos.size();
	for (unsigned int i = 0; i < _leucocitos.size(); i++)
	{ // para todos os leucocitos
		if (!(_leucocitos.at(i).vivo()) && contador > 10)
		{ // se estiver vivo a mais de 7 segundos e tiverem mais de 10 Leucocitos remove
			contador -= 1;
			_leucocitos.erase(_leucocitos.begin()+i);
		}
		else
		{ // se não só move ele
			(_leucocitos.at(i)).mover();
		}
	}
}

void Cabeca::atualizaMapa()
{
	// inicializa o mapa em branco primeiro
	for (int i = 0; i < 30; i++)
	{
		for (int j = 0; j < 60; j++)
		{
			mapa[i][j] = ((i == 0 || i == 29) || (j == 0 || j == 59)) ? 6 : 0;
		}
	}

	for (Celula cel : _celulas) { mapa[cel.getY()][cel.getX()] = cel.getCor(); } // atualiza todas as celulas
	for (Leucocito leuc : _leucocitos) { mapa[leuc.getY()][leuc.getX()] = leuc.getCor(); }
	for (Influenza virus : _virus) { mapa[virus.getY()][virus.getX()] = virus.getCor(); } // atualiza os virus
}

void Cabeca::atualizaVirus()
{
	bool naCelula, removido;

	for (unsigned int i = 0; i < _virus.size(); i++)
	{
		naCelula = false;
		removido = false;
		_virus.at(i).mover(); // inicia a atualização movendo o virus

		for (unsigned int j = 0; j < _celulas.size(); j++)
		{
			if (_virus.at(i).getX() == _celulas.at(j).getX() && _virus.at(i).getY() == _celulas.at(j).getY())
			{ // se o virus estiver na mesma casa da celula
				if (_virus.at(i).estaNaCelula() == false)
				{ // se ele não estava em uma celula na ultima interação
					contamina(Influenza(rand() % 30, rand() % 60));
					naCelula = true;
					break;
				}
			}
		}

		for (unsigned int j = 0; j < _leucocitos.size(); j++)
		{
			if (_virus.at(i).getX() == _leucocitos.at(j).getX() && _virus.at(i).getY() == _leucocitos.at(j).getY())
			{ // se esta na mesma casa do leucocito
				criaLeucocito(); // multiplica leucocito
				_virus.erase(_virus.begin()+i);
				removido = true;
				break; // termina o loop pois este virus morreu
			}
		}

		if (removido == false) { _virus.at(i).setCelula(naCelula); } // se o virus ainda estiver vivo, escolhe se continua multiplicando ou não
	}
}

void Cabeca::criaLeucocito()
{
	int linha = rand() % 30;
	int coluna = rand() % 60;
	_leucocitos.push_back(Leucocito(linha, coluna));
}

void Cabeca::inicializaBoca()
{
	for (int linha = 23; linha < 25; linha++)
	{
		for (int coluna = 20; coluna < 40; coluna++)
		{
			_celulas.push_back(CelulaBoca(linha,coluna));
		}
	}
}

void Cabeca::inicializaLeucocitos()
{
	for (int i = 0; i < 10; i++) { criaLeucocito(); }
}

void Cabeca::inicializaNariz()
{
	for (int linha = 12; linha < 16; linha++)
	{
		for (int coluna = 27; coluna < 33; coluna++)
		{
			_celulas.push_back(CelulaNasal(linha, coluna));
		}
	}
}

void Cabeca::inicializaOlhos()
{
	for (int linha = 5; linha < 10; linha++)
	{
		for (int coluna = 10; coluna < 16; coluna++)
		{
			_celulas.push_back(CelulaOcular(linha, coluna)); // celulas do olho esquerdo
			_celulas.push_back(CelulaOcular(linha, 60 - coluna)); // celulas do olho direito
		}
	}
}


Cabeca::~Cabeca()
{
}