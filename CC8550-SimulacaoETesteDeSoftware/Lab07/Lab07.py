import random
from math import log, factorial # log = base e

# Seed para padronizar os resultados
random.seed(0)

# ================== #
# === DEFINICOES === #
# ================== #
class computador:
    def __init__(self, a, ts, c, kf, nome="Computador"):
        self.nome = nome
        self.kf = kf
        self.a = a/3600
        self.ts = ts
        self.c = c
        self.mi = 1/self.ts
        self.r = self.a / self.mi
        self.rho = self.a / (self.c * self.mi)
        self.P0 = self._P0()
        self.aef = self.a*(1-self.Pn(self.kf))
        self.U = self.aef / (self.c * self.rho)
        try:
            self.delta = ((self.c*self.rho)**c) / (factorial(c)*(1-self.rho)) * self.P0
        except:
            self.delta = None
        self.Lw = sum([(n-self.c)*self.Pn(n) for n in range(self.c+1, self.kf+1)])
        self.Lw = 0 if self.Lw < 0 else self.Lw
        self.Tw = self.Lw/self.aef
        self.Ls = sum([n*self.Pn(n) for n in range(1, self.kf+1)])
        self.Tr = self.Ls/self.aef
        self.Tr = 0 if self.Tr < 0 else self.Tr
        self.Tp = self.a*self.Pn(self.kf)
    def Pn(self, n):
        if n < self.c:
            return 1/factorial(n) * (self.a/self.mi)**n * self.P0
        elif n <= self.kf:
            return 1/(factorial(self.c)*c**(n-c)) * (self.a/self.mi)**n * self.P0
        else:
            return 0
    def _P0(self):
        somatoria = 0
        for n in range(1, c):
            somatoria += (1/factorial(n)) * (self.a/self.mi)**n
        try:
            return (somatoria + ((1-self.rho**(self.kf-(self.c-1))*(self.c*self.rho)**self.c))/(factorial(self.c)*(1-self.rho)) + 1)**-1
        except:
            return 1e-9

    def __str__(self):
        return \
            "=== {} ===\n".format(self.nome) + \
            "- ts       = {:n}\n".format(self.ts) + \
            "- mi       = {:n}\n".format(self.mi) + \
            "- r        = {:.4f}\n".format(self.r) + \
            "- rho      = {:.4f}\n".format(self.rho) + \
            "- U        = {:.4f}\n".format(self.U) + \
            "- P0       = {:.4f}\n".format(self.P0) + \
            "- delta    = {:.6f}\n".format(self.delta) + \
            "- Lw       = {:.6f}\n".format(self.Lw) + \
            "- Tw       = {:.6f}\n".format(self.Tw) + \
            "- Ls       = {:.4f}\n".format(self.Ls) + \
            "- Tr       = {:.4f}\n".format(self.Tr)

class servidor(computador):
    def __init__(self, a, c, theta, kf, amostras=20, nome="Servidor"):
        self.amostras = amostras
        self.theta = theta
        
        self.ts = [self._amostra_exp() for _ in range(amostras)]
        self.ts_medio = sum(self.ts)/amostras
        
        super().__init__(a=a, ts=self.ts_medio, c=c, kf=kf, nome=nome)
        
    def _amostra_exp(self):
        return -self.theta*log(random.random())
    def __str__(self):
        return \
            super().__str__() + \
            "- theta    = {:.4f}\n".format(self.theta) + \
            "- ts_medio = {:.4f}\n".format(self.ts_medio)

# ================= #
# === SIMULACAO === #
# ================= #

# === Parte 1: a = 210 mensagens / hora
a = 110 # mensagens / hora
c = 3 # Numero de servidores
# COMPUTADORES
computador_1 = computador(a=a, ts=2, c=c, kf=6, nome="Computador 1")
computador_2 = computador(a=a, ts=4, c=c, kf=6, nome="Computador 2")
computador_3 = computador(a=a, ts=12.15, c=c, kf=6, nome="Computador 3")
# SERVIDORES
servidores = [servidor(a=a, c=c, kf=6, theta=8, nome=f"Servidor {i+1}") for i in range(c)]
# Resultado da simulacao
for cpu in [computador_1, computador_2, computador_3] + servidores:
    print(cpu)

# === Parte 2: variando mensagens por segundo (a)
numero_simulacoes = 1000
a_inicial = 5
a_step = 5
c = 3
# Simulando
simulacoes = []
for sim in range(numero_simulacoes):
    a = a_inicial + a_step * sim
    # COMPUTADORES
    computador_1 = computador(a=a, ts=2.0, c=c, kf=6, nome="Computador 1")
    computador_2 = computador(a=a, ts=4.0, c=c, kf=6, nome="Computador 2")
    computador_3 = computador(a=a, ts=12.15, c=c, kf=6, nome="Computador 3")
    # SERVIDORES
    servidores = [servidor(a=a, c=c, kf=6, theta=8, nome=f"Servidor {i+1}") for i in range(c)]
    simulacoes.append({'computadores': (computador_1, computador_2, computador_3), 'servidores': servidores, 'a': a})
# Gerando a tabela
template = " {:^13} | {:^8} | {:^7} | {:^7} | {:^7} | {:^7} |"
line_break = '-'*15+"+"+'-'*10+"+"+'-'*9+"+"+'-'*9+"+"+'-'*9+"+"+'-'*9+"|"
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
except ModuleNotFoundError: 
    print("Biblioteca matplotlib nao instalada.. nao foi possivel criar os graficos")
else:
    # --- Graficos dos computadores --- #
    comp1, comp2, comp3 = zip(*map(lambda data: data['computadores'], simulacoes))
    sv1, sv2, sv3 = zip(*map(lambda data: data['servidores'], simulacoes))
    a = [*map(lambda data: data['a'], simulacoes)]
    # COMPUTADORES
    fig, axs = plt.subplots(1, 2, figsize=(15,10))
    fig.tight_layout(pad=5.0)
    # Tr
    axs[0].set_xlabel("a [mensagens/hora]")
    axs[0].set_ylabel("Tr [segundos]")
    axs[0].set_title("Tr")
    axs[0].plot(a, [*map(lambda comp: comp.Tr, comp1)], c='r', label='C1')
    axs[0].plot(a, [*map(lambda comp: comp.Tr, comp2)], c='g', label='C2')
    axs[0].plot(a, [*map(lambda comp: comp.Tr, comp3)], c='b', label='C3')
    axs[0].plot(a, [*map(lambda comp: comp.Tr, sv1)], c='k', label='Servidor 1')
    axs[0].plot(a, [*map(lambda comp: comp.Tr, sv2)], c='c', label='Servidor 2')
    axs[0].plot(a, [*map(lambda comp: comp.Tr, sv3)], c='y', label='Servidor 3')
    # Lw
    axs[1].set_xlabel("a [mensagens/hora]")
    axs[1].set_ylabel("Lw [mensagens]")
    axs[1].set_title("Lw")
    axs[1].plot(a, [*map(lambda comp: comp.Lw, comp1)], c='r', label='C1')
    axs[1].plot(a, [*map(lambda comp: comp.Lw, comp2)], c='g', label='C2')
    axs[1].plot(a, [*map(lambda comp: comp.Lw, comp3)], c='b', label='C3')
    axs[1].plot(a, [*map(lambda comp: comp.Lw, sv1)], c='k', label='Servidor 1')
    axs[1].plot(a, [*map(lambda comp: comp.Lw, sv2)], c='c', label='Servidor 2')
    axs[1].plot(a, [*map(lambda comp: comp.Lw, sv3)], c='y', label='Servidor 3')
    
    # for i in range(3):
    for j in range(2):
        axs[j].grid()
        axs[j].legend()
    plt.show()
