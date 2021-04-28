import random
import time
import threading
import queue
from enum import Enum

class Operation(Enum):
    ADD = 0
    REMOVE = 1

class Input:
    def __init__(self, name, min_qtt, max_qtt, min_periodo, max_periodo, stop_signal):
        self.stop_signal = stop_signal
        self.name = name
        self.input_amount = (min_qtt, max_qtt)
        self.periodo = (min_periodo, max_periodo)
        self.output_pipes = []

    def connect_pipe(self, pipe):
        self.output_pipes.append(pipe)

    def __call__(self):
        while not self.stop_signal:
            # Sorteia a quantidade de entrada no range
            amount = random.SystemRandom().uniform(self.input_amount[0], self.input_amount[1])
            # Emite o valor pelos pipes
            for pipe in self.output_pipes:
                pipe(amount/len(self.output_pipes), self.name)
            # espera
            time.sleep(random.SystemRandom().uniform(self.periodo[0], self.periodo[1]))

    def start(self):
        thread = threading.Thread(target=self, name="Input_{}".format(self.name))
        thread.start()
        return thread

class Pipe:
    def __init__(self, name, *output_list):
        self.name = name
        self.output_list = list(output_list)
        self.pipe_full = False

    def __call__(self, valor, product):
        # Verifica se o pipe nao esta cheio
        if not self.pipe_full:
            # Divide a entrada pra cada cada saida
            for output in self.output_list:
                output(valor/len(self.output_list), product)

class Tank:
    def __init__(self, capacity, name, stop_signal):
        self.name = name
        self.stop_signal = stop_signal
        self.capacity = capacity
        self.level = 0
        self.products = []
        self.tanklock = threading.Lock()
        self.output_pipes = []
        # inicia thread do tanque

    def connect_pipe(self, pipe):
        self.output_pipes.append(pipe)

    def __call__(self, qtt, product, operation):
        with self.tanklock:
            if operation == Operation.ADD:
                # TODO: Mudar essa logica para usar fila
                entry = self.capacity-self.level if qtt + self.level > self.capacity else qtt
                self.level += entry
                try:
                    self.level[product] += entry
                except:
                    self.level[product] = entry
            elif operation == Operation.REMOVE:
                pass