package PROJETO;

/**
 * Classe celula possui as caracteristicas gerais de uma celula
 * @author Pedro Domingues 22.218019-2
 */
public abstract class Celulas {
    // atributos
    /**
     * Coordenada x (coluna) da matriz onde ficara armazenado
     */
    private int x;
    /**
     * Coordenada y (linha) da matriz onde ficara armazenado
     */
    private int y;
    /**
     * cor representativa da celula
     */
    private int cor;
    
    // construtor
    /**
     * @param x coordenada x = coluna da matriz
     * @param y coordenada y = linha da matriz
     * @param cor inteiro representativo da cor de impressão da celula
     */
    public Celulas(int y, int x, int cor)
    {
        this.x = x;
        this.y = y;
        this.cor = cor;
    }
    
    // metodos set
    /**
     * set cor, mas não permite cores negativas
     * @param cor não permite cores negativas
     */
    public void setCor(int cor)
    {    
        if (cor >= 0){ this.cor = cor; }
        else { this.cor = 0; }
    }
    /**
     * Altera as posições da celula
     * @param x varia de 0 a 60 no array ( comprimento / colunas )
     * @param y varia de 0 a 30 no array ( altura / linhas )
     */
    public void setPos(int x, int y)
    {
        if      (x < 0)   { this.x = x+60; } // reaparece na direita
        else if (x >= 60) { this.x = x-60; } // reaparece na esquerda
        else              { this.x =    x; }
        
        if      (y < 0)   { this.y = y+30; } // reaparece em baixo
        else if (y >= 30) { this.y = y-30; } // reaparece em cima
        else              { this.y =    y; }
    }
    
    // metodos get
    public int getCor() { return cor; }
    public int getX()   { return x; }
    public int getY()   { return y; }

}
