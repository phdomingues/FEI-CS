import queue
import threading
import random
import time 
from tqdm import tqdm

def abrirBarbearia(time_scale):
    expediente = 8 # Barbeiro trabalha 8 horas no dia
    
    fila = queue.Queue(5) # Fila de clientes, maximo de 5
    barbeiro = Barbeiro(fila, time_scale) # Objeto que atende os clientes (tira da fila e espera)

    barbearia = threading.Thread(target=barbeiro.atender) # Thread onde o barbeiro trabalha
    barbearia.start() # Inicia o trabalho do barbeiro
    
    client_id = 0 # Id dos clientes
    
    # 2 Clientes chegam por hora
    for _ in range(expediente): # 1 loop = 1 hora

        #### PRIMEIRO CLIENTE ####
        # Cria id do cliente
        client_id += 1
        # Sorteia hora de chegada do primeiro cliente da hora (qualquer momento de 0 a 60 minutos)
        cliente1 = random.randint(0, 60) #10
        #...esperando o primeiro cliente da hora chegar
        time.sleep(cliente1 * time_scale)
        try:
            # Cliente senta na fila
            fila.put(client_id, block=False)
        except:
            # Ou vai embora se estiver cheio
            print(f"Barbearia cheia, cliente {client_id} foi embora")


        #### Segundo cliente ####
        # Cria id para o proximo cliente
        client_id += 1
        # Sorteia hora de chegada do segundo cliente da hora (desde o instante em que primeiro chegou)
        # -> 0              = chega junto do primeiro
        # -> 60 - cliente1  = chega no ultimo momento da hora
        cliente2 = random.randint(0, 60 - cliente1) #0 50
        #...esperando o segundo cliente chegar
        time.sleep(cliente2 * time_scale)
        try:
            # Cliente senta na fila
            fila.put(client_id, block=False)
        except:
            # Ou vai embora se estiver cheio
            print(f"Barbearia cheia, cliente {client_id} foi embora")
        

        #### Tempo restante no periodo de 1 hora ####
        # Espera a hora acabar
        # tempo que passou = cliente1 [tempo do primeiro cliente chegar] + cliente2 [tempo do segundo cliente chegar]
        # tempo que falta = 60 [periodo de 1 hr] - (tempo que passou)
        time.sleep((60 - cliente2 - cliente1) * time_scale)

    # Terminando o expediente, faz o barbeiro parar de trabalhar
    barbeiro.stop()
    # Aguarda a thread terminar
    barbearia.join()
    # Avisa quantos clientes foram atendidos no dia
    return barbeiro.clientesAtendidos


class Barbeiro:
    #construtor
    def __init__(self, cadeiras, time_scale):
        self.aberto = True
        self.estado = "Dormindo"
        self.cadeiras = cadeiras
        self.clientesAtendidos = 0
        self.time_scale = time_scale

    #metodo atender
    def atender(self):
        # Zera a contagem de clientes do dia
        self.clientesAtendidos = 0
        # Entra no loop de trabalho
        while self.aberto:
            # Tenta dormir
            self.estado = "Dormindo"
            try:
                # Se tiver um cliente na fila
                cliente = self.cadeiras.get(block=False)
                # Então começa a trabalhar
                self.estado = "Trabalhando"
                # Aguarda o trabalho finalizar (25 +- 5 minutos)
                time.sleep(random.randint(20, 30) * self.time_scale)
                # Contabiliza o cliente
                self.clientesAtendidos += 1
            except:
                # Se não tiver cliente na fila, aguarda uma quantidade pequena de tempo (para não sobrecarregar o processador)
                time.sleep(0.1*self.time_scale)

    def stop(self):
        # Para de trabalhar (atender sai do while)
        self.aberto = False
        # Esvazia as cadeiras
        while not self.cadeiras.empty():
            self.cadeiras.get()
        


if __name__ == "__main__":
    # Escala de tempo
    # para time_scale = 1 -> 1minuto = 1segundo
    time_scale = 0.0001
    # Quantos dias o barbeiro vai trabalhar para tirar a media de clientes atendidos
    dias = 100
    # Lista com quantos clientes foram atendidos em cada dia
    clientes_por_dia = []
    # Roda os dias (tqdm = barra de progresso)
    for _ in tqdm(range(dias)):
        atendidos = abrirBarbearia(time_scale)
        clientes_por_dia.append(atendidos)
    # Imprime a média de clientes atendidos
    print(f"Media de clientes atendidos nos ultimos {dias} dias: ", sum(clientes_por_dia)/len(clientes_por_dia))


    
    