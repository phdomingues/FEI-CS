from Components import *
import threading
import signal
import math
import time
import os

threads = []

# ====== Ferramenta de logging
def logging(stop_signal, *tanks):
    while not stop_signal():
        os.system('cls' if os.name == 'nt' else 'clear')
        print("{:^30} | {:^10} | {:^10} | Products".format("Tanque", "Capacidade", "Level"))
        print("{}+{}+{}+{}".format("-"*31, "-"*12, '-'*12, '-'*30))
        for tank in tanks:
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
# === Pipes - Meio de comunicação, usado para passar produtos de um lado para o outro
pipe_oil_tank = Pipe("pipe(Oleo)", tank_oil)
pipe_naoh_tank = Pipe("pipe(NaOH)", tank_naoh_etoh)
pipe_etoh_tank = Pipe("pipe(EtOH)", tank_naoh_etoh)
pipe_oil_reactor = Pipe("pipe(Oleo)", reactor)
pipe_naoh_etoh_reactor = Pipe("Pipe(NaOH/EtOH)", reactor)
pipe_reactor_decanter = Pipe("Pipe(NaOh/2EtOH/Oleo)", decanter)
# pipe_decanter_etoh = Pipe("Pipe(EtOH) decanter", tank_etoh)
# pipe_decanter_glycerin = Pipe("Pipe(Glicerina)", tank_glycerin)
# pipe_decanter_washing_tank_1 = Pipe("Pipe(Solução)", washing_tank_1)
# pipe_washing_tank_1_washing_tank_2 = Pipe("Pipe(Solução)", washing_tank_2)
# pipe_washing_tank_2_washing_tank_3 = Pipe("Pipe(Solução)", washing_tank_3)
# ====== Conectando os pipes aos seus inputs
input_oil.connect_pipe(pipe_oil_tank)
input_NaOH.connect_pipe(pipe_naoh_tank)
input_EtOH.connect_pipe(pipe_etoh_tank)
tank_oil.connect_pipe(pipe_oil_reactor)
tank_naoh_etoh.connect_pipe(pipe_naoh_etoh_reactor)
reactor.connect_pipe(pipe_reactor_decanter)
# decanter.connect_pipe(pipe_decanter_etoh)
# decanter.connect_pipe(pipe_decanter_glycerin)
# decanter.connect_pipe(pipe_decanter_washing_tank_1)
# washing_tank_1.connect_pipe(pipe_washing_tank_1_washing_tank_2)
# washing_tank_2.connect_pipe(pipe_washing_tank_2_washing_tank_3)
# Logging tool
log_thread = threading.Thread(target=logging, name="logging_tool", args=(stop_signal, tank_oil, tank_naoh_etoh, tank_glycerin, tank_biodisel, tank_etoh, reactor, decanter, washing_tank_1, washing_tank_2, washing_tank_3))

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
#threads.append(washing_tank_3.start())
threads.append(log_thread.start())

for thread in threads:
    if thread:
        thread.join()