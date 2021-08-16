package PROJETO;

import java.time.Instant;
import java.util.Date;
import java.util.Random;
/**
 * Classe Leucocito é um tipo especial de celula que se movimenta, tem vida de 7 segundos (caso hajam mais de 10 na cabeça) e se multiplica quando mata um virus influenza
 * @author Pedro Domingues 22.218019-2
 */
public class Leucocitos extends Celulas implements IMovable{
    private final int velocidade;
    private final Date nascimento;
    
    /**
     * @param y linha da matriz
     * @param x coluna da matriz
     */
    public Leucocitos(int y, int x)
    {
        super(y, x, 2);
        nascimento = new Date();
        velocidade = 2;
    }
    
    // metodos get
    public int getVelocidade() { return velocidade; }
    public Date getNascimento() { return nascimento; }

    // tempo de vida
    /**
     * @return true = ainda não passou 7s --- false = passou 7s
     */
    public boolean vivo()
    {
        Date agora = new Date();
        return ((int)(agora.getTime() - nascimento.getTime())/1000) <= 7; 
    }
    
    // sobrepondo metodos da abstract
    /**
     * Move o leucocito para uma direção sorteada aleatoriamente, incluindo diagonais (a não movimentação acarreta no sorteio de uma nova direção).
     */
    @Override
    public void mover() 
    {
        
        Random rand = new Random();
        for (int i = 0; i < velocidade ; i++)
        {
            int movX = 0;
            int movY = 0;
            while( movX == 0 && movY == 0 )
            {
                movX = rand.nextInt(3) - 1; // -1 /ou/ 0 /ou/ 1
                movY = rand.nextInt(3) - 1; // -1 /ou/ 0 /ou/ 1    
            }
            setPos(getX() + movX , getY() + movY);
        }
    }
    
}
