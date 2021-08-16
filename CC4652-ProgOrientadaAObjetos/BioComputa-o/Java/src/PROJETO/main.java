package PROJETO;

import java.util.Date;
import java.util.Random;
import java.util.concurrent.TimeUnit;
/**
 * Criação da cabeça - Contaminação com 3 virus influenza e loop para visualização
 * @author Pedro Domingues 22.218019-2
 */
public class main {
    public static void main (String[] args){
        // cria cabeça
        Cabeca C = new Cabeca();
        
        // cria doença
        Random rand = new Random();
        for (int w = 0 ; w < 15000 ; w++){
            Influenza inf = new Influenza(rand.nextInt(30),rand.nextInt(60));
            C.contamina(inf);
        }
        
        // inicia a contagem do tempo
        Date inicio = new Date();
        int tempo = 0;
        
        // inicia as interações e plotagem
        while(tempo<300)
        { // roda por 5 minutos (300 seg)
            // data atual para comparação
            Date agora = new Date();
            tempo = (int) ((agora.getTime()-inicio.getTime())/1000);
            
            // imprime o tempo
            System.out.printf("\n\n\n\u001B[47m Tempo: %d \u001B[0m",tempo);
            // print na tela
            C.desenhaCabeca();
            
            // precisa esperar pois o netbeans não da conta de imprimir tão rapido
            try { TimeUnit.MILLISECONDS.sleep(200); } 
            catch (InterruptedException ex) {}
            
        }
            
    }
}
