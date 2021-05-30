import random
import time
import threading

TIME_MULTIPLIER = 1
DEBUG = True

class Input:
    def __init__(self, name, min_qtt, max_qtt, min_periodo, max_periodo, stop_signal):
        self.stop_signal = stop_signal
        self.name = name
        self.input_amount = (min_qtt, max_qtt)
        self.periodo = (min_periodo, max_periodo)
        self.output_pipes = []
        self.inputlock = threading.Lock()
        self.total_input = 0

    def connect_pipe(self, pipe):
        self.output_pipes.append(pipe)

    def pump(self):
        while not self.stop_signal():
            if DEBUG: time.sleep(TIME_MULTIPLIER)
            # Sorteia a quantidade de entrada no range
            amount = random.SystemRandom().uniform(self.input_amount[0], self.input_amount[1])
            with self.inputlock:
                self.total_input += amount
            # Emite o valor pelos pipes
            for pipe in self.output_pipes:
                pipe(amount/len(self.output_pipes), self.name)
            # espera
            wait_time = random.SystemRandom().uniform(self.periodo[0], self.periodo[1])
            time.sleep(wait_time*TIME_MULTIPLIER)

    def start(self):
        thread = threading.Thread(target=self.pump, name="Input_{}".format(self.name))
        thread.start()
        return thread

    def __str__(self):
        with self.inputlock:
            log = self.name.ljust(20, ' ')
            return "{:<20} | {:.2f}".format(self.name, self.total_input)

class Pipe:
    def __init__(self, name, *output_list):
        self.name = name
        self.output_list = list(output_list)
        self.pipe_full = False
        self.pipelock = threading.Lock()

    def __call__(self, valor, product):
        if product == None:
            return valor
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
            if DEBUG: time.sleep(TIME_MULTIPLIER)
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
            products = ' / '.join(["{:.2f} ({})".format(amount, product_name).ljust(20, ' ') for product_name, amount in products.items()])
            status_string = "{:<30} | {:>10} | {:>10.2f} | ".format(self.name, self.capacity, self.level)
            status_string += products
        return status_string


class Reactor(Tank):
    def __init__(self, capacity, name, flow, stop_signal):
        super().__init__(capacity, name, stop_signal)
        self.flow = flow
        self.products = {
                        'NaOH': 0,
                        'Oleo': 0,
                        'EtOH': 0
                        }
        self.cumulated_output = 0

    def pump(self):
        # O Reator processa 5L/s, sendo: 1 parte NaOH, 1 parte Oleo e 2 partes EtOH
        # ou seja, para 5L, tem-se no maximo 1.25L de NaOH, 1.25L de Oleo e 2.5L de EtOh
        while not self.stop_signal():
            if DEBUG: time.sleep(TIME_MULTIPLIER)
            with self.tanklock:
                # limita a transferencia no maximo por segundo
                naoh = min(self.flow/4, self.products['NaOH'])
                oil  = min(self.flow/4, self.products['Oleo'])
                etoh = min(self.flow/2, self.products['EtOH'])
                # encontra o gargalo
                products_limited = {'NaOH': naoh, 'Oleo': oil, 'EtOH': etoh/2}
                bottleneck = min(products_limited.keys(), key=(lambda product: products_limited[product]))
                next_iter = products_limited[bottleneck] == 0
            # Se nao tiver nada para enviar, só espera pela proxima iteração
            if next_iter: continue
            # dado o gargalo escolhe as quantidades que serao processadas
            if bottleneck == 'NaOH':
                used =  {
                    'NaOH': naoh,
                    'Oleo': naoh,
                    'EtOH': 2*naoh
                }
            elif bottleneck == 'Oleo':
                used =  {
                    'NaOH': oil,
                    'Oleo': oil,
                    'EtOH': 2*oil
                }
            elif bottleneck == 'EtOH':
                used =  {
                    'NaOH': etoh/2,
                    'Oleo': etoh/2,
                    'EtOH': etoh
                }
            else:
                raise Exception("Invalid Product on reactor")
            # Calcula o total utilizado
            total = sum(used.values())
            # Reduz do tanque a quantidade processada
            with self.tanklock:
                for product, amount in used.items():
                    # Gera o produto resultado
                    throwback = 0
                    for pipe in self.output_pipes:
                        # Assume-se que o throwback simplesmente vaza do reator
                        throwback += pipe(amount/len(self.output_pipes), "Mistura")
                    self.products[product] -= (amount + throwback) 
            # Adiciona o que saiu ao total acumulado e reduz o nivel do tanque
            self.cumulated_output += total
            self.level -= total
            # Para por 1 seg pois a vazao é considerada em L/s
            time.sleep(1*TIME_MULTIPLIER)
            # Descansa se necessario
            if self.cumulated_output > 3:
                # Calcula tempo de descanso - 5s para cada 3L de output
                rest_time = (5*3/self.cumulated_output)-1 # -1 pois ja descansa 1 segundo sempre
                time.sleep(rest_time*TIME_MULTIPLIER)
                self.cumulated_output = 0

    def __call__(self, qtt, product):
        with self.tanklock:
            # Calcula quanto entra no tanque (entry) e quanto volta pelo pile (throwback)
            entry = self.capacity-self.level if qtt + self.level > self.capacity else qtt
            throwback = qtt - entry
            # Adiciona no tanque
            self.level += entry
            self.products[product] += entry
            return throwback

    def __str__(self):
        with self.tanklock:
            products_string = ' / '.join(["{:.2f} ({})".format(amount, product_name).ljust(20, ' ') for product_name, amount in self.products.items()])
            status_string = "{:<30} | {:>10} | {:>10.2f} | ".format(self.name, self.capacity, self.level)
            status_string += products_string
        return status_string

class Decanter(Tank):
    # A saida do decantador é 0.02 Glicerina, 0.09 EtOH e 0.89 Solucao p/ lavagem
    def __init__(self, capacity, name, stop_signal):
        super().__init__(capacity, name, stop_signal)
        self.glycerin_pipe = None
        self.etoh_pipe = None
        self.wash_pipe = None

    def connect_glycerin_pipe(self, pipe):
        self.glycerin_pipe = pipe
    def connect_etoh_pipe(self, pipe):
        self.etoh_pipe = pipe
    def connect_wash_pipe(self, pipe):
        self.wash_pipe = pipe

    def pump(self):
        while not self.stop_signal():
            if DEBUG: time.sleep(TIME_MULTIPLIER)
            # remove tudo o que tiver nele
            total = 0
            with self.tanklock:
                total = sum([amount for amount, _ in self.content])
                self.content.clear()
                self.level -= total
            # Joga para o pipe
            throwback = 0
            throwback += self.glycerin_pipe(0.02*total, 'Glicerina')
            throwback += self.etoh_pipe(0.09*total, 'EtOH')
            throwback += self.wash_pipe(0.89*total, 'Lavagem')
            # Devolve o que restou pro tanque
            if throwback > 0:
                with self.tanklock:
                    self.content.insert(0, (throwback, 'throwback'))
                    self.level += throwback

class WashTank(Tank):
    def __init__(self, capacity, name, loss, stop_signal):
        super().__init__(capacity, name, stop_signal)
        self.loss = loss

    def pump(self):
        while not self.stop_signal():
            if DEBUG: time.sleep(TIME_MULTIPLIER)
            if len(self.output_pipes) > 0:
                # Puxa o proximo da fila
                amount = 0.0
                product = None
                with self.tanklock:
                    try:
                        amount, product = self.content.pop(0)
                        self.level -= amount
                        amount *= (1-self.loss)
                    except:
                        pass
                # Joga para o pipe
                throwback = 0
                for pipe in self.output_pipes:
                    throwback += pipe(amount/len(self.output_pipes), 'Biodisel')
                if throwback > 0:
                    with self.tanklock:
                        self.content.insert(0, (throwback, 'Biodisel'))
                        self.level += throwback

class Dryer(Tank):
    def __init__(self, capacity, name, stop_signal, loss, time_per_liter):
        super().__init__(capacity, name, stop_signal)
        self.loss = loss
        self.time_per_liter = time_per_liter
        self.drying_time = 0
        self.drying_liters = 0

    def pump(self):
        while not self.stop_signal():
            if DEBUG: time.sleep(TIME_MULTIPLIER)
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
                    self.drying_time = self.time_per_liter*amount
                    self.drying_liters = amount
                # Aguarda o tempo de secagem (N [segundos/Litro] * L [Litros])
                time.sleep(self.time_per_liter*amount*TIME_MULTIPLIER)
                # Joga para o pipe
                throwback = 0
                for pipe in self.output_pipes:
                    throwback += pipe(amount*(1-self.loss)/len(self.output_pipes), product)
                if throwback > 0:
                    with self.tanklock:
                        self.content.insert(0, (throwback, product))
                        self.level += throwback

    def __str__(self):
        with self.tanklock:
            products = {}
            for qtt, product in self.content:
                try: products[product] += qtt
                except: products[product] = qtt
            products = "{:<15}".format(' / '.join(["{:.2f} ({})".format(amount, product_name).ljust(15, ' ') for product_name, amount in products.items()]))
            drying_string = " | {:.2f} L ({:.2f} seconds)".format(self.drying_liters, self.drying_time)
            status_string = "{:<30} | {:>10} | {:>10.2f} | ".format(self.name, self.capacity, self.level)
            status_string += products + drying_string
        return status_string
