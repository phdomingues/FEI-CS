package PROJETO;

import java.util.Random;
/**
 * Classe Virus implementa as caracteristicas genericas para qualquer tipo de virus
 * @author Pedro Domingues 22.218019-2
 */
public abstract class Virus implements IMovable {
    private final int velocidade;
    private final int cor;
    private int x;
    private int y;
    
    // construtor
    /**
     * @param y linha da matriz
     * @param x coluna da matriz
     */
    public Virus(int y, int x)
    {
        /**
         * @param y linha da matriz
         * @param x coluna da matriz
         */
        setPos(x,y);
        cor = 1;
        velocidade = 1;
    }
    
    // metodo set
    /**
     * Atualiza a posição x e y do Virus:
     * @param x varia de 0 a 60 no array ( comprimento )
     * @param y varia de 0 a 30 no array ( altura )
     */
    private void setPos(int x, int y)
    {        // x varia de 0 a 60 no array ( comprimento )
        if      (x < 0)   { this.x = x+60; } // reaparece na direita
        else if (x >= 60) { this.x = x-60; } // reaparece na esquerda
        else              { this.x =    x; }
        // y varia de 0 a 30 no array ( altura )
        if      (y < 0)   { this.y = y+30; } // reaparece em baixo
        else if (y >= 30) { this.y = y-30; } // reaparece em cima
        else              { this.y =    y; }
    }
    
    /**
     * Move o virus para uma direção sorteada aleatoriamente, não incluindo diagonais (a não movimentação acarreta no sorteio de uma nova direção).
     */
    @Override
    public void mover() {
        Random rand = new Random();
        for (int i = 0; i < getVelocidade(); i++)
        {
            int mov = 0;
            int direcao = rand.nextInt(2);
            while( mov == 0) { mov = rand.nextInt(3) - 1; } // -1, 0, 1
            if (direcao == 0) { setPos(getX() + mov , getY()); }
            else { setPos(getX() , getY() + mov); }
        }
    }
    
    // metodos get
    public int getVelocidade() { return velocidade; }
    public int getCor() { return cor; }
    public int getX() { return x; }
    public int getY() { return y; }
}
