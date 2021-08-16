package PROJETO;
/**
 * Classe Influenza se multiplica quando em contato com celulas da boca, nariz ou olhos e morre quando em contato com um leucocito
 * @author Pedro Domingues 22.218019-2
 */
public class Influenza extends Virus {
    // atributos
    /**
     * celula mantem controle sobre o virus ja estar sobre uma celula e ter se multiplicado
     */
    private boolean celula;

    // construtor
    /**
     * @param y linha da matriz
     * @param x coluna da matriz
     */
    public Influenza(int y, int x) {
        super(y, x);
        celula = false;
    }
    
    // metodos
    public void setCelula(boolean val) { celula = val; }
    public boolean estaNaCelula() { return celula; }
}
