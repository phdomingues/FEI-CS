#pragma once
class Celula
{
public:
	Celula(int, int, int);
	void setCor(int);
	void setPos(int, int);
	int getCor();
	int getX();
	int getY();
	virtual ~Celula();

private:
	int x;
	int y;
	int cor;
};

