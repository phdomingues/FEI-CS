import random
import time
import threading

class Input:
    def __init__(self, name, min_qtt, max_qtt, min_periodo, max_periodo, stop_signal):
        self.stop_signal = stop_signal
        self.name = name
        self.input_amount = (min_qtt, max_qtt)
        self.periodo = (min_periodo, max_periodo)
        self.output_pipes = []
        self.inputlock = threading.Lock()

    def connect_pipe(self, pipe):
        self.output_pipes.append(pipe)

    def pump(self):
        while not self.stop_signal():
            # Sorteia a quantidade de entrada no range
            amount = random.SystemRandom().uniform(self.input_amount[0], self.input_amount[1])
            # Emite o valor pelos pipes
            for pipe in self.output_pipes:
                throwback = pipe(amount/len(self.output_pipes), self.name)
            # espera
            time.sleep(random.SystemRandom().uniform(self.periodo[0], self.periodo[1]))

    def start(self):
        thread = threading.Thread(target=self.pump, name="Input_{}".format(self.name))
        thread.start()
        return thread

class Pipe:
    def __init__(self, name, *output_list):
        self.name = name
        self.output_list = list(output_list)
        self.pipe_full = False
        self.pipelock = threading.Lock()

    def __call__(self, valor, product):
        with self.pipelock:
            throwback = 0
            # Verifica se o pipe nao esta cheio
            if not self.pipe_full:
                # Divide a entrada pra cada cada saida
                for output in self.output_list:
                    throwback += output(valor/len(self.output_list), product)
        return throwback

class Tank:
    def __init__(self, capacity, name, stop_signal):
        self.name = name
        self.stop_signal = stop_signal
        self.capacity = capacity
        self.level = 0
        self.content = []
        self.tanklock = threading.Lock()
        self.output_pipes = []
        # inicia thread do tanque

    def connect_pipe(self, pipe):
        self.output_pipes.append(pipe)

    def pump(self):
        while not self.stop_signal():
            if len(self.output_pipes) > 0:
                # Puxa o proximo da fila
                amount = 0.0
                product = None
                with self.tanklock:
                    try:
                        amount, product = self.content.pop(0)
                        self.level -= amount
                    except:
                        pass
                # Joga para o pipe
                throwback = 0
                for pipe in self.output_pipes:
                    throwback += pipe(amount/len(self.output_pipes), product)
                # Devolve o que restou pro tanque
                if throwback > 0:
                    with self.tanklock:
                        self.content.insert(0, (throwback, product))
                        self.level += throwback
            time.sleep(0.1) # Sleep para nao sobrecarregar processador

    def start(self):
        thread = threading.Thread(target=self.pump, name="Tank_{}".format(self.name))
        thread.start()
        return thread

    def __call__(self, qtt, product):
        with self.tanklock:
            # Calcula quanto entra no tanque (entry) e quanto volta pelo pile (throwback)
            entry = self.capacity-self.level if qtt + self.level > self.capacity else qtt
            throwback = qtt - entry
            # Adiciona no tanque
            self.level += entry
            if entry > 0:
                self.content.append((entry, product))

        # Devolve pro pipe o que nao coube
        return throwback

    def __str__(self):
        with self.tanklock:
            products = {}
            for qtt, product in self.content:
                try: products[product] += qtt
                except: products[product] = qtt
            products = ' | '.join(["{:>6.2f} ({})".format(amount, product_name).ljust(20, ' ') for product_name, amount in products.items()])
            status_string = "{:<30} | {:>10} | {:>10.2f} | ".format(self.name, self.capacity, self.level)
            status_string += products
        return status_string


class Reactor(Tank):
    def __init__(self, capacity, name, flow, stop_signal):
        super().__init__(capacity, name, stop_signal)
        self.flow = flow


class Decanter(Tank):
    def __init__(self, capacity, name, stop_signal):
        super().__init__(capacity, name, stop_signal)


class WashTank(Tank):
    def __init__(self, capacity, name, loss, stop_signal):
        super().__init__(capacity, name, stop_signal)
        self.loss = loss

    def pump(self):
        while not self.stop_signal():
            if len(self.output_pipes) > 0:
                # Puxa o proximo da fila
                amount = 0.0
                product = None
                with self.tanklock:
                    try:
                        amount, product = self.content.pop(0)
                        if (self.output_pipes[0].output_list[0].name == "Secador Maior"):
                            amount *= (1-self.output_pipes[0].output_list[0].loss)
                            self.level -= ((amount*(1+self.output_pipes[0].output_list[0].loss)))
                            self.output_pipes[0].output_list[0].limit += amount
                        else:
                            amount *= (1-self.loss)
                            self.level -= ((amount*(1+self.loss)))
                    except:
                        pass
                # Joga para o pipe
                throwback = 0
                for pipe in self.output_pipes:
                    throwback += pipe(amount/len(self.output_pipes), product)
                # Devolve o que restou pro tanque
                if throwback > 0:
                    with self.tanklock:
                        self.content.insert(0, (throwback, product))
                        self.level += throwback

                if (self.output_pipes[0].output_list[0].name == "Secador Maior") and (self.output_pipes[0].output_list[0].limit >= 1):
                    time.sleep(5)
                    self.output_pipes[0].output_list[0].limit = 0

            time.sleep(0.1) # Sleep para nao sobrecarregar processador

class Dryer(Tank):
    def __init__(self, capacity, name, limit, loss, stop_signal):
        super().__init__(capacity, name, stop_signal)
        self.loss = loss
        self.limit = limit
