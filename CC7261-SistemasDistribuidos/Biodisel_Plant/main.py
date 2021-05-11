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
        print("{:^30} | {:^10} | {:^10} | Products".format("Tanque", "Capacidade", "Level"))
        print("{}+{}+{}+{}".format("-"*31, "-"*12, '-'*12, '-'*30))
        for tank in tanks:
            print(tank)
        time.sleep(0.1)
        os.system('cls' if os.name == 'nt' else 'clear')
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
input_oil = Input("Oleo sujo", 1, 2, 0, 10, stop_signal)
input_NaOH = Input("NaOH", 0.25, 0.25, 1, 1, stop_signal)
input_EtOH = Input("EtOH", 0.125, 0.125, 1, 1, stop_signal)
# === Tanque - Armazenam um produto e podem repassa-lo para outro lugar
tank_oil = Tank(math.inf, "Tanque de oleo", stop_signal)
tank_naoh_etoh = Tank(math.inf, "Tanque de NaOH/EtOH", stop_signal)
tank_glicerina = Tank(math.inf, "Tanque de Glicerina", stop_signal)
tank_biodisel = Tank(math.inf, "Tanque de Biodisel", stop_signal)
tank_etoh = Tank(math.inf, "Tanque de EtOH (Reaproveitado)", stop_signal)
# === Pipes - Meio de comunicação, usado para passar produtos de um lado para o outro
pipe_oil_tank = Pipe("pipe(Oleo)", tank_oil)
pipe_naoh_tank = Pipe("pipe(NaOH)", tank_naoh_etoh)
pipe_etoh_tank = Pipe("pipe(EtOH)", tank_naoh_etoh)
# Test pipe
pipe_tank2tank = Pipe("pipe(Teste)", tank_etoh)

# ====== Conectando os pipes aos seus inputs
input_oil.connect_pipe(pipe_oil_tank)
input_NaOH.connect_pipe(pipe_naoh_tank)
input_EtOH.connect_pipe(pipe_etoh_tank)
tank_naoh_etoh.connect_pipe(pipe_tank2tank)


# Logging tool
log_thread = threading.Thread(target=logging, name="logging_tool", args=(stop_signal, tank_oil, tank_naoh_etoh, tank_glicerina, tank_biodisel, tank_etoh))

# Ligando threads
threads.append(input_oil.start())
threads.append(input_NaOH.start())
threads.append(input_EtOH.start())
threads.append(tank_naoh_etoh.start())
threads.append(log_thread.start())

for thread in threads:
    thread.join()