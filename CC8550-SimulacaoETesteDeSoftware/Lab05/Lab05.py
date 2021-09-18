import random
from math import log, factorial # log = base e

# Seed para padronizar os resultados
random.seed(0)

# ================== #
# === DEFINICOES === #
# ================== #
class computador:
    def __init__(self, a, ts, c, nome="Computador"):
        self.nome = nome
        self.a = a/3600
        self.ts = ts
        self.c = c
        self.mi = 1/self.ts
        self.r = self.a / self.mi
        self.pho = self.a / (self.c * self.mi)
        self.U = self.pho
        self.P0 = self._P0()
        self.delta = ((self.c*self.pho)**c) / (factorial(c)*(1-self.pho)) * self.P0
        self.Lw = (self.pho*self.delta) / (1 - self.pho)
        self.Tw = self.delta / (self.c * self.mi * (1-self.pho))
        self.Ls = (self.c*self.pho) + ((self.pho*self.delta) / (1-self.pho))
        self.Tr = 1/self.mi * (1 + self.delta / (self.c*(1-self.pho)))
    def Pn(self, n):
        if n < self.c:
            return 1/factorial(n) * (self.a/self.mi)**n * self.P0
        else:
            return 1/(factorial(self.c)*c**(n-c)) * (self.a/self.mi)**n * self.P0
    def _P0(self):
        somatoria = 0
        for n in range(c):
            somatoria += (1/factorial(n)) * (self.a/self.mi)**n
        return (somatoria + (1/factorial(self.c)) * (self.a/self.mi)**self.c * (1/(1-self.pho)))**-1
    def __str__(self):
        return \
            "=== {} ===\n".format(self.nome) + \
            "- ts       = {:n}\n".format(self.ts) + \
            "- mi       = {:n}\n".format(self.mi) + \
            "- r        = {:.4f}\n".format(self.r) + \
            "- pho      = {:.4f}\n".format(self.pho) + \
            "- U        = {:.4f}\n".format(self.U) + \
            "- P0       = {:.4f}\n".format(self.P0) + \
            "- delta    = {:.6f}\n".format(self.delta) + \
            "- Lw       = {:.6f}\n".format(self.Lw) + \
            "- Tw       = {:.6f}\n".format(self.Tw) + \
            "- Ls       = {:.4f}\n".format(self.Ls) + \
            "- Tr       = {:.4f}\n".format(self.Tr)

class servidor(computador):
    def __init__(self, a, c, theta, amostras=20, nome="Servidor"):
        self.amostras = amostras
        self.theta = theta
        
        self.ts = [self._amostra_exp() for _ in range(amostras)]
        self.ts.sort()
        self.ts_medio = sum(self.ts)/amostras
        
        super().__init__(a=a, ts=self.ts_medio, c=c, nome=nome)

        self.delta = self._delta()
        
    def _delta(self):
        return ((self.c*self.pho)**self.c)/(factorial(self.c)*(1-self.pho))*self.P0
    def _amostra_exp(self):
        return -self.theta*log(random.random())
    def __str__(self):
        return \
            super().__str__() + \
            "- theta    = {:.4f}\n".format(self.theta) + \
            "- delta    = {:.4f}\n".format(self.delta) + \
            "- ts_medio = {:.4f}\n".format(self.ts_medio)

# ================= #
# === SIMULACAO === #
# ================= #

# === Parte 1: a = 210 mensagens / hora
a = 210 # mensagens / hora
c = 3 # Numero de servidores
# COMPUTADORES
computador_1 = computador(a=a, ts=2, c=c, nome="Computador 1")
computador_2 = computador(a=a, ts=4, c=c, nome="Computador 2")
computador_3 = computador(a=a, ts=12.15, c=c, nome="Computador 3")
# SERVIDORES
servidores = [servidor(a=a, c=c, theta=8, nome=f"Servidor {i+1}") for i in range(c)]
# Resultado da simulacao
for cpu in [computador_1, computador_2, computador_3] + servidores:
    print(cpu)

# === Parte 2: variando mensagens por segundo (a)
numero_simulacoes = 100
a_inicial = 5
a_step = 5
c = 3
# Simulando
simulacoes = []
for sim in range(numero_simulacoes):
    a = a_inicial + a_step * sim
    # COMPUTADORES
    computador_1 = computador(a=a, ts=2, c=c, nome="Computador 1")
    computador_2 = computador(a=a, ts=4, c=c, nome="Computador 2")
    computador_3 = computador(a=a, ts=12.15, c=c, nome="Computador 3")
    # SERVIDORES
    servidores = [servidor(a=a, c=c, theta=8, nome=f"Servidor {i+1}") for i in range(c)]
    simulacoes.append({'computadores': (computador_1, computador_2, computador_3), 'servidores': servidores, 'a': a})
# Gerando a tabela
template = " {:^13} | {:^8} | {:^7} | {:^7} | {:^7} | {:^7} | {:^7} | {:^7} |"
line_break = '-'*15+"+"+'-'*10+"+"+'-'*9+"+"+'-'*9+"+"+'-'*9+"+"+'-'*9+"+"+'-'*9+"+"+'-'*9+"|"
print(template.format("Num Simulacao", "a(msg/h)", "Tr - C1", "Lw - C1", "Tr - C2", "Lw - C2", "Tr - C3", "Lw - C3"))
print(line_break)
for iteracao, data in enumerate(simulacoes):
    print(template.format(
        iteracao+1,
        data['a'],
        "{:.4f}".format(data['computadores'][0].Tr), "{:.4f}".format(data['computadores'][0].Lw),
        "{:.4f}".format(data['computadores'][1].Tr), "{:.4f}".format(data['computadores'][1].Lw),
        "{:.4f}".format(data['computadores'][2].Tr), "{:.4f}".format(data['computadores'][2].Lw)
    ))
# Gerando os graficos
try: 
    import matplotlib.pyplot as plt
    # --- Graficos dos computadores --- #
    comp1, comp2, comp3 = zip(*map(lambda data: data['computadores'], simulacoes))
    a = [*map(lambda data: data['a'], simulacoes)]
    # COMPUTADORES
    fig, axs = plt.subplots(3, 2, figsize=(15,10))
    fig.tight_layout(pad=5.0)
    # Tr
    axs[0,0].set_xlabel("a [mensagens/hora]")
    axs[0,0].set_ylabel("Tr [segundos]")
    axs[0,0].set_title("Tr - C1")
    axs[0,0].plot(a, [*map(lambda comp: comp.Tr, comp1)], c='r', label='C1')
    axs[1,0].set_xlabel("a [mensagens/hora]")
    axs[1,0].set_ylabel("Tr [segundos]")
    axs[1,0].set_title("Tr - C2")
    axs[1,0].plot(a, [*map(lambda comp: comp.Tr, comp2)], c='g', label='C2')
    axs[2,0].set_xlabel("a [mensagens/hora]")
    axs[2,0].set_ylabel("Tr [segundos]")
    axs[2,0].set_title("Tr - C3")
    axs[2,0].plot(a, [*map(lambda comp: comp.Tr, comp3)], c='b', label='C3')
    # Lw
    axs[0,1].set_xlabel("a [mensagens/hora]")
    axs[0,1].set_ylabel("Lw [mensagens]")
    axs[0,1].set_title("Lw - C1")
    axs[0,1].plot(a, [*map(lambda comp: comp.Lw, comp1)], c='r', label='C1')
    axs[1,1].set_xlabel("a [mensagens/hora]")
    axs[1,1].set_ylabel("Lw [mensagens]")
    axs[1,1].set_title("Lw - C2")
    axs[1,1].plot(a, [*map(lambda comp: comp.Lw, comp2)], c='g', label='C2')
    axs[2,1].set_xlabel("a [mensagens/hora]")
    axs[2,1].set_ylabel("Lw [mensagens]")
    axs[2,1].set_title("Lw - C3")
    axs[2,1].plot(a, [*map(lambda comp: comp.Lw, comp3)], c='b', label='C3')
    
    for i in range(3):
        for j in range(2):
            axs[i,j].grid()

    plt.show()
except ModuleNotFoundError: 
    print("Biblioteca matplotlib nao instalada.. nao foi possivel criar os graficos")
