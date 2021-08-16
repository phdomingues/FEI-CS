package PROJETO;

import java.util.ArrayList;
import java.util.Date;
import java.util.Random;
/**
 * @author Pedro Domingues 22.218019-2
 * 
 * <p>Esta classe é responsavel por simular o comportamento da cabeça </p>
 * 
 * <p>A classe é composta por ArrayLists que armazenam celulas estaticas, Leucocitos e Virus influenza;</p>
 */
public class Cabeca {
    /**
     * Mundo de grades 30x60 para representar o rosto
     */
    public int mapa[][] = new int[30][60];
    /**
     * Armazena CelulasBoca, CelulasNasais e CelulasOculares
     */
    private ArrayList <Celulas> _celulas = new ArrayList();
    /**
     * Arazena todos os Leucocitos
     */
    private ArrayList <Leucocitos> _leucocitos = new ArrayList();
    /**
     * Armazena os virus presentes no sistema
     */
    private ArrayList <Influenza> _virus = new ArrayList();
    
    // construtor
    public Cabeca(){
        inicializaOlhos();
        inicializaBoca();
        inicializaNariz();
        inicializaLeucocitos();
    }
    
    // criacao
    /** 
     * Função para criar um leucocito no sistema em uma posição aleatorioa
     */
    private void criaLeucocito()
    {
        Random rand = new Random();
        int linha = rand.nextInt(30);
        int coluna = rand.nextInt(60);
        _leucocitos.add( new Leucocitos(linha,coluna) );
    }
    
    // inicializacoes
    /**
     * Cria 10 leucocitos em posicoes aleatorias, necessario para inicialização da cabeça
     */
    private void inicializaLeucocitos()
    {
        for (int i=0;i<10;i++) { criaLeucocito(); }
    }
    /**
     * Instancia todas as celulas oculares e posiciona elas de forma a criar dois olhos --- Celulas armazenadas no ArrayList _celulas utilizando polimorfismo
     */
    private void inicializaOlhos()
    {
        for (int linha=5;linha<10;linha++)
        {
            for (int coluna=10;coluna<16;coluna++)
            {
                _celulas.add(new CelulasOculares(linha,coluna)); // celulas do olho esquerdo
                _celulas.add(new CelulasOculares(linha,60-coluna)); // celulas do olho direito
            }
        }
    }
    /**
     * Instancia todas as celulas da boca e posiciona para formar a boca --- Celulas armazenadas no ArrayList _celulas utilizando polimorfismo
     */
    private void inicializaBoca()
    {
        for (int linha=23;linha<25;linha++)
        {
            for (int coluna=20;coluna<40;coluna++)
            {
                _celulas.add(new CelulasBoca(linha,coluna));
            }
        }
    }
    /**
     * Instancia todas as celulas nasais e posiciona para formar o nariz --- Celulas armazenadas no ArrayList _celulas utilizando polimorfismo
     */
    private void inicializaNariz()
    {
        for (int linha=12;linha<16;linha++)
        {
            for (int coluna=27;coluna<33;coluna++)
            {
                _celulas.add(new CelulasNasais(linha,coluna));
            }
        }
    }
    
    // update
    /**
     * Atualização do mundo de grades, uma matriz 30x60, com as cores de cada uma das celulas
     */
    private void atualizaMapa()
    {
        // inicializa o mapa em branco primeiro
        for (int i=0;i<30;i++)
        {
            for (int j=0;j<60;j++)
            {
                mapa[i][j] = ( (i==0 || i==29) || (j==0 || j==59) ) ? 6:0;
            }
        }
        
        for (Celulas cel : _celulas) { mapa[cel.getY()][cel.getX()] = cel.getCor(); } // atualiza todas as celulas
        for (Celulas leuc : _leucocitos) { mapa[leuc.getY()][leuc.getX()] = leuc.getCor(); }
        for (Influenza virus : _virus) { mapa[virus.getY()][virus.getX()] = virus.getCor(); } // atualiza os virus
        
    }
    /**
     * Função responsavel pela movimentação e controle da população de leucocitos
     */
    private void atualizaLeucocitos()
    {
        int contador = _leucocitos.size();
        for (int i=0;i<_leucocitos.size();i++)
        { // para todos os leucocitos
            if ( !(_leucocitos.get(i)).vivo() && contador > 10)
            { // se estiver vivo a mais de 7 segundos e tiverem mais de 10 Leucocitos remove
                contador -= 1;
                _leucocitos.remove(i);
            }
            else 
            { // se não só move ele
                (_leucocitos.get(i)).mover();
            }
        }
    }

    
    // virus
    /**
     * Função para adição de virus do tipo Influenza no ArrayList _virus
     * @param virus = virus a ser guardado no ArrayList
     */
    public void contamina(Influenza virus)
    {
        _virus.add(virus);
    }
    /**
     * Função para controle da população dos virus influenza na cabeça (multiplicação, morte e movimentação dos virus)
     */
    private void atualizaVirus()
    {
        boolean naCelula, removido;
        Random rand = new Random();
        
        for (int i = 0 ; i < _virus.size() ; i++)
        {
            naCelula = false;
            removido = false;
            _virus.get(i).mover(); // inicia a atualização movendo o virus
            
            for (int j = 0 ; j < _celulas.size() ; j++) {
                if (_virus.get(i).getX() == _celulas.get(j).getX() && _virus.get(i).getY() == _celulas.get(j).getY())
                { // se o virus estiver na mesma casa da celula
                    if (_virus.get(i).estaNaCelula() == false) 
                    { // se ele não estava em uma celula na ultima interação
                        int linha = rand.nextInt(30);
                        int coluna = rand.nextInt(60);
                        contamina(new Influenza(linha,coluna));
                        naCelula = true;
                        break;
                    }
                }
            }
            
            for (int j = 0 ; j < _leucocitos.size() ; j++)
            {
                if (_virus.get(i).getX() == _leucocitos.get(j).getX() && _virus.get(i).getY() == _leucocitos.get(j).getY())
                { // se esta na mesma casa do leucocito
                    criaLeucocito(); // multiplica leucocito
                    _virus.remove(i); // mata virus
                    removido = true;
                    break; // termina o loop pois este virus morreu
                }
            }
            
            if (removido == false) { _virus.get(i).setCelula(naCelula); } // se o virus ainda estiver vivo, escolhe se continua multiplicando ou não
        }
    }
    
    // imprime mapa
    /**
     * Função principal da classe cabeça, responsavel por chamar todas as atualizaçãoes necessarias para o sistema funcionar, realizar a tradução das cores e impressão do rosto na tela
     * 
     * <p> ***Diagrama de cores:</p>
     * <p> - 0 - Vazio          - Preto</p>
     * <p> - 1 - Virus          - Vermelho</p>
     * <p> - 2 - Leucocito      - Ciano</p>
     * <p> - 3 - Celula Ocular  - Azul</p>
     * <p> - 4 - Celula Nasal   - Verde</p>
     * <p> - 5 - Celula Boca    - Amarelo</p>
     * <p> - 6 - Borda          - Branco</p>
     */
    public void desenhaCabeca()
    {
        atualizaMapa(); // atualiza os valores do mapa com os valores mais recentes
        
        System.out.printf("\n\n\u001B[41m \u001B[0m\u001B[31m Influenza (%d) \u001B[0m",_virus.size());
        System.out.printf("  \u001B[46m \u001B[0m\u001B[36m Leucocitos (%d) \u001B[0m\n\n",_leucocitos.size());
        String cor;
        // roda em todo o mapa
        for (int i=0;i<30;i++)
        { // para cada linha
            for (int j=0;j<60;j++)
            { // para cada coluna
                switch (mapa[i][j]) 
                { // escolhe a cor corretamente
                    case 0:
                        cor = "\u001B[40m";
                        break;
                    case 1:
                        cor = "\u001B[41m";
                        break;
                    case 2:
                        cor = "\u001B[46m";
                        break;
                    case 3:
                        cor = "\u001B[44m";
                        break;
                    case 4:
                        cor = "\u001B[42m";
                        break;
                    case 5:
                        cor = "\u001B[43m";
                        break;
                    case 6:
                        cor = "\u001B[47m";
                        break;
                    default:
                        cor = "";
                        break;
                }
                // imprime
                System.out.print(cor + " " + "\u001B[0m");
            } System.out.println();
        }
        
        // atualiza leucocitos e virus
        atualizaVirus(); // atualiza virus / mata virus / trata casos de multiplicação de leucocito
        atualizaLeucocitos(); // atualiza posição dos leucocitos e decide se vive ou morre
    }
    
}
