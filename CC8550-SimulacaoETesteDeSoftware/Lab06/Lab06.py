import random
from math import log # log = base e

# Seed para padronizar os resultados
random.seed(0)

# ================== #
# === DEFINICOES === #
# ================== #
class computador:
    def __init__(self, a, ts, kf, nome="Computador"):
        self.nome = nome
        self.a = a/3600
        self.ts = ts
        self.kf = kf
        self.mi = 1/self.ts
        self.r = self.a / self.mi
        self.pho = self.a / (self.mi)
        self.aef = self.a*(1-self.Pn(self.kf))
        self.U = self.aef / self.mi
        self.P0 = self.P0_()
        self.Lw = self.Lw_()
        self.Tw = self.Tw_()
        self.Ls = self.Ls_()
        self.Tr = self.Tr_()
    def Pn(self, n):
        if self.a != self.mi:
            return (self.a/self.mi)**n * self.P0_()
        else:
            return 1/(self.kf+1)
    def P0_(self):
        if self.a != self.mi:
            return (1 - (self.a/self.mi)) / (1 - (self.a/self.mi)**(self.kf+1))
        else:
            return 1 / (self.kf + 1)
    def Ls_(self):
        if self.a != self.mi:
            rkf1 = self.r**(self.kf+1)
            return (self.r/(1-self.r))-((self.kf + 1) / (1-rkf1))*rkf1
        else:
            return self.kf/2
    def Lw_(self):
        if self.a != self.mi:
            return (self.r/(1-self.r)) - ((self.r*(1+self.kf*self.r**self.kf))/(1-self.r**(self.kf+1)))
        else:
            return self.kf*(self.kf-1)/(2*(self.kf+1))
    def Tw_(self):
        if self.a != self.mi:
            return (1/self.mi) * ((self.r/(1-self.r)) - ((self.kf*self.r**self.kf)/(1-self.r**self.kf)))
        else:
            return (self.kf-1) / (2*self.mi)
    def Tr_(self):
        if self.a != self.mi:
            return (1/self.mi) * (1/(1-self.r) - (self.kf*self.r**self.kf)/(1-self.r**self.kf))
        else:
            return (self.kf+1) / (2*self.mi)
    def __str__(self):
        return \
            "=== {} ===\n".format(self.nome) + \
            "- a        = {:n}\n".format(self.a) + \
            "- aef      = {:n}\n".format(self.aef) + \
            "- kf       = {:n}\n".format(self.kf) + \
            "- ts       = {:n}\n".format(self.ts) + \
            "- mi       = {:n}\n".format(self.mi) + \
            "- r        = {:.4f}\n".format(self.r) + \
            "- pho      = {:.4f}\n".format(self.pho) + \
            "- U        = {:.4f}\n".format(self.U) + \
            "- P0       = {:.4f}\n".format(self.P0) + \
            "- Pkf      = {:.4f}\n".format(self.Pn(self.kf)) + \
            "- Lw       = {:.6f}\n".format(self.Lw) + \
            "- Tw       = {:.6f}\n".format(self.Tw) + \
            "- Ls       = {:.4f}\n".format(self.Ls) + \
            "- Tr       = {:.4f}\n".format(self.Tr)

class servidor(computador):
    def __init__(self, a, kf, theta, amostras=20, nome="Servidor"):
        self.amostras = amostras
        self.theta = theta
        
        self.ts = [self._amostra_exp() for _ in range(amostras)]
        self.ts.sort()
        self.ts_medio = sum(self.ts)/amostras
        
        super().__init__(a=a, ts=self.ts_medio, kf=kf, nome=nome)

        self.delta = self._delta()
        
    def _delta(self):
        return (self.pho)/(1-self.pho)*self.P0
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

# === Parte 1: a = 110 mensagens / hora
a = 110 # mensagens / hora
# COMPUTADORES
computador_1 = computador(a=a, ts=2, kf=6, nome="Computador 1")
computador_2 = computador(a=a, ts=4, kf=6, nome="Computador 2")
computador_3 = computador(a=a, ts=12.15, kf=6, nome="Computador 3")
# SERVIDORES
servidor_ = servidor(a=a, kf=6, theta=8, nome=f"Servidor")
# Resultado da simulacao
for cpu in [computador_1, computador_2, computador_3, servidor_]:
    print(cpu)

# # === Parte 2: variando mensagens por segundo (a)
numero_simulacoes = 800
a_inicial = 20
a_step = 20
# Simulando
simulacoes = []
for sim in range(numero_simulacoes):
    a = a_inicial + a_step * sim
    # COMPUTADORES
    computador_1 = computador(a=a, ts=2, kf=6, nome="Computador 1")
    computador_2 = computador(a=a, ts=4, kf=6, nome="Computador 2")
    computador_3 = computador(a=a, ts=12.15, kf=6, nome="Computador 3")
    # SERVIDORES
    servidor_ = servidor(a=a, kf=6, theta=8, nome=f"Servidor")
    simulacoes.append({'computadores': (computador_1, computador_2, computador_3), 'servidor': servidor_, 'a': a})
# Gerando a tabela
template = " {:^13} | {:^8} | {:^7} | {:^7} | {:^7} | {:^7} | {:^7} | {:^7} |"
line_break = '-'*15+"+"+'-'*10+"+"+'-'*9+"+"+'-'*9+"+"+'-'*9+"+"+'-'*9+"+"+'-'*9+"+"+'-'*9+"|"
print(template.format("Num Simulacao", "a(msg/h)", "Tr - C1", "Lw - C1", "Tr - C2", "Lw - C2", "Tr - C3", "Lw - C3", "Tr - Sv", "Lw - Sv"))
print(line_break)
for iteracao, data in enumerate(simulacoes):
    print(template.format(
        iteracao+1,
        data['a'],
        "{:.4f}".format(data['computadores'][0].Tr), "{:.4f}".format(data['computadores'][0].Lw),
        "{:.4f}".format(data['computadores'][1].Tr), "{:.4f}".format(data['computadores'][1].Lw),
        "{:.4f}".format(data['computadores'][2].Tr), "{:.4f}".format(data['computadores'][2].Lw),
        "{:.4f}".format(data['servidor'].Tr), "{:.4f}".format(data['servidor'].Lw)
    ))
# Gerando os graficos
try: 
    import matplotlib.pyplot as plt
    # --- Graficos dos computadores --- #
    comp1, comp2, comp3 = zip(*map(lambda data: data['computadores'], simulacoes))
    sv = [*map(lambda data: data['servidor'], simulacoes)]
    a = [*map(lambda data: data['a'], simulacoes)]
    # COMPUTADORES
    fig, axs = plt.subplots(4, 2, figsize=(15,10))
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
    axs[3,0].set_xlabel("a [mensagens/hora]")
    axs[3,0].set_ylabel("Tr [segundos]")
    axs[3,0].set_title("Tr - Servidor")
    axs[3,0].plot(a, [*map(lambda comp: comp.Tr, sv)], c='black', label='Servidor')

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
    axs[3,1].set_xlabel("a [mensagens/hora]")
    axs[3,1].set_ylabel("Lw [mensagens]")
    axs[3,1].set_title("Lw - Servidor")
    axs[3,1].plot(a, [*map(lambda comp: comp.Lw, sv)], c='black', label='Servidor')
    
    for i in range(4):
        for j in range(2):
            axs[i,j].grid()

    plt.show()
except ModuleNotFoundError: 
    print("Biblioteca matplotlib nao instalada.. nao foi possivel criar os graficos")
