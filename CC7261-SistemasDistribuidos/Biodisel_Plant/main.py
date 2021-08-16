from Components import *
import threading
import signal
import math
import time
import os

SIMULATION_TIME = 360 # Tempo de simulação em segundos em tempo real (nao considera o TIME_MULTIPLIER)

threads = []

# ====== Ferramenta de logging
def logging(stop_signal, **components):
    while not stop_signal():
        os.system('cls' if os.name == 'nt' else 'clear')
        # Inputs
        print("{:^20} | {:^10} | Cicles".format("Input", "Total injetado no sistema"))
        print("{}+{}+{}".format("-"*21, '-'*27, "-"*8))
        for input in components.get('inputs', []):
            print(input)
        print("\n\n")

        # Reactors
        print("{:^30} | {:^10} | {:^10} | {:^6} | Products".format("Reator", "Capacidade", "Nível", "Cicles"))
        print("{}+{}+{}+{}+{}".format("-"*31, "-"*12, '-'*12, '-'*8, '-'*60))
        for r in components.get('reactors', []):
            print(r)
        print("\n\n")

        # Decanters
        print("{:^30} | {:^10} | {:^10} | {:^6} | Products".format("Decantador", "Capacidade", "Nível", "Cicles"))
        print("{}+{}+{}+{}+{}".format("-"*31, "-"*12, '-'*12, '-'*8, '-'*15))
        for decanter in components.get('decanters', []):
            print(decanter)
        print("\n\n")

        # Dryers
        print("{:^30} | {:^10} | {:^10} | {:^6} | {:^17} | Drying".format("Secador", "Capacidade", "Nível", "Cicles", "Products"))
        print("{}+{}+{}+{}+{}+{}".format("-"*31, "-"*12, '-'*12, '-'*8, '-'*19, '-'*20))
        for dryer in components.get('dryers', []):
            print(dryer)
        print("\n\n")

        # Tanks
        print("{:^30} | {:^10} | {:^10} | {:^6} | Products".format("Tanque", "Capacidade", "Nível", "Cicles"))
        print("{}+{}+{}+{}+{}".format("-"*31, "-"*12, '-'*12, '-'*8, '-'*15))
        for tank in components.get('tanks', []):
            print(tank)

        time.sleep(0.5)
        
        
    print("Finished executing...")
    print("Stoping threads...")


# ====== Sinais e handlers de parada
stop_lock = threading.Lock()
stop_variable = False
def stop_signal():
    global stop_variable, stop_lock
    with stop_lock: 
        return stop_variable
def stop_handler(num, stack):
    global stop_variable
    stop_variable = True
signal.signal(signal.SIGINT, stop_handler)

# ====== Criando os objetos
# === Input - Geram um determinado produto
input_oil = Input("Oleo", 1, 2, 0, 10, stop_signal)
input_NaOH = Input("NaOH", 0.25, 0.25, 1, 1, stop_signal)
input_EtOH = Input("EtOH", 0.125, 0.125, 1, 1, stop_signal)
# === Tanque - Armazenam um produto e podem repassa-lo para outro lugar
tank_oil = Tank(math.inf, "Tanque de oleo", stop_signal)
tank_naoh_etoh = Tank(math.inf, "Tanque de NaOH/EtOH", stop_signal)
tank_glycerin = Tank(math.inf, "Tanque de Glicerina", stop_signal)
tank_biodisel = Tank(math.inf, "Tanque de Biodisel", stop_signal)
tank_etoh = Tank(math.inf, "Tanque de EtOH (Reaproveitado)", stop_signal)
# === Reator - Processa os produtos
reactor = Reactor(math.inf, "Reator",5, stop_signal)
# === Decantador - Processa os produtos
decanter = Decanter(10, "Decantador", stop_signal)
# === Lavagem - Perda de 7.5%
washing_tank_1 = WashTank(math.inf, "Tanque de Lavagem 1", 0.075, stop_signal)
washing_tank_2 = WashTank(math.inf, "Tanque de Lavagem 2", 0.075, stop_signal)
washing_tank_3 = WashTank(math.inf, "Tanque de Lavagem 3", 0.075, stop_signal)
# === Secadores
dryer_etoh = Dryer(math.inf, "Secador de EtOH", stop_signal, 0.03, 5)
dryer_biodisel = Dryer(math.inf, "Secador de Lavagem", stop_signal, 0.03, 5)
# === Pipes - Meio de comunicação, usado para passar produtos de um lado para o outro
pipe_oil_tank = Pipe("pipe(Oleo)", tank_oil)
pipe_naoh_tank = Pipe("pipe(NaOH)", tank_naoh_etoh)
pipe_etoh_tank = Pipe("pipe(EtOH)", tank_naoh_etoh)
pipe_oil_reactor = Pipe("pipe(Oleo)", reactor)
pipe_naoh_etoh_reactor = Pipe("Pipe(NaOH/EtOH)", reactor)
pipe_reactor_decanter = Pipe("Pipe(NaOh/2EtOH/Oleo)", decanter)
pipe_decanter_dryer = Pipe("Pipe(EtOH) decanter", dryer_etoh)
pipe_decanter_glycerin = Pipe("Pipe(Glicerina)", tank_glycerin)
pipe_decanter_washing_tank_1 = Pipe("Pipe(Lavagem)", washing_tank_1)
pipe_washing_tank_1_washing_tank_2 = Pipe("Pipe(Lavagem)", washing_tank_2)
pipe_washing_tank_2_washing_tank_3 = Pipe("Pipe(Lavagem)", washing_tank_3)
pipe_washing_tank_3_dryer_biodisel = Pipe("Pipe(Lavagem)", dryer_biodisel)
pipe_dryer_etoh_tank = Pipe("Pipe(EtOH)", tank_etoh)
pipe_etoh_tank_naoh_etoh = Pipe("Pipe(EtOH[R])",tank_naoh_etoh)
pipe_dryer_biodisel_tank = Pipe("Pipe(Biodisel)", tank_biodisel)
# ====== Conectando os pipes aos seus inputs
input_oil.connect_pipe(pipe_oil_tank)
input_NaOH.connect_pipe(pipe_naoh_tank)
input_EtOH.connect_pipe(pipe_etoh_tank)
tank_oil.connect_pipe(pipe_oil_reactor)
tank_naoh_etoh.connect_pipe(pipe_naoh_etoh_reactor)
reactor.connect_pipe(pipe_reactor_decanter)
decanter.connect_etoh_pipe(pipe_decanter_dryer)
decanter.connect_glycerin_pipe(pipe_decanter_glycerin)
decanter.connect_wash_pipe(pipe_decanter_washing_tank_1)
washing_tank_1.connect_pipe(pipe_washing_tank_1_washing_tank_2)
washing_tank_2.connect_pipe(pipe_washing_tank_2_washing_tank_3)
washing_tank_3.connect_pipe(pipe_washing_tank_3_dryer_biodisel)
tank_etoh.connect_pipe(pipe_etoh_tank_naoh_etoh)
dryer_etoh.connect_pipe(pipe_dryer_etoh_tank)
dryer_biodisel.connect_pipe(pipe_dryer_biodisel_tank)
# Logging tool
log_thread = threading.Thread(
    target=logging, 
    name="logging_tool", 
    args=([stop_signal]),
    kwargs={
            'inputs': [input_oil, input_NaOH, input_EtOH],
            'dryers': [dryer_etoh, dryer_biodisel],
            'reactors': [reactor],
            'decanters': [decanter],
            'tanks': [tank_oil, tank_naoh_etoh, tank_glycerin, tank_etoh, 
                      washing_tank_1, washing_tank_2, washing_tank_3, tank_biodisel]
            })

# Ligando threads
threads.append(input_oil.start())
threads.append(input_NaOH.start())
threads.append(input_EtOH.start())
threads.append(tank_oil.start())
threads.append(tank_naoh_etoh.start())
threads.append(reactor.start())
threads.append(decanter.start())
threads.append(washing_tank_1.start())
threads.append(washing_tank_2.start())
threads.append(washing_tank_3.start())
threads.append(dryer_biodisel.start())
threads.append(dryer_etoh.start())
threads.append(tank_etoh.start())
threads.append(log_thread.start())

# time.sleep(SIMULATION_TIME)
# stop_variable = True

for thread in threads:
    if thread: thread.join()