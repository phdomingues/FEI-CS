from BaseClasses import *
import signal
import math

threads = []

# Sinais e handlers de parada
def stop(num, stack):
    print(f"STOP! {num} - {stack}")
stop_signal = signal.signal(signal.SIGUSR1, stop)

# ====== Criando os objetos
# === Input
input_oil = Input("Oleo sujo", 1, 2, 0,10, stop_signal)
input_NaOH = Input("NaOH", 0.25, 0.25, 1, 1, stop_signal)
input_EtOH = Input("EtOH", 0.125, 0.125, 1, 1, stop_signal)
# === Tanque
tank_oil = Tank(math.inf, "Tanque de oleo", stop_signal)
tank_naoh_etoh = Tank(math.inf, "Tanque de NaOH/EtOH", stop_signal)
tank_glicerina = Tank(math.inf, "Tanque de Glicerina", stop_signal)
tank_biodisel = Tank(math.inf, "Tanque de Biodisel", stop_signal)
tank_etoh = Tank(math.inf, "Tanque de EtOH (Reaproveitado)", stop_signal)
# === Pipes
pipe_oil_tank = Pipe("pipe(Oleo)", tank_oil)
pipe_naoh_tank = Pipe("pipe(NaOH)", tank_naoh_etoh)
pipe_etoh_tank = Pipe("pipe(EtOH)", tank_naoh_etoh)

# Conectando os objetos
input_oil.connect_pipe(pipe_oil_tank)
input_NaOH.connect_pipe(pipe_naoh_tank)
input_EtOH.connect_pipe(pipe_etoh_tank)

# Ligando threads
threads.append(input_oil.start())
threads.append(input_NaOH.start())
threads.append(input_EtOH.start())

# os.system('cls' if os.name == 'nt' else 'clear')

for thread in threads:
    thread.join()