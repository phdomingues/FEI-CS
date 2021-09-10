import math
import random
import statistics
try: import matplotlib.pyplot as plt
except: print("Biblioteca matplotlib nao instalada, o grafico nao sera plotado!")

# === ENUNCIADO === #
# VARIAVEIS DE SIMULACAO
NUM_SIMULACOES = 10 # Numero de simulacoes que devem ser realizadas
SEMENTE = 92 # Matricula = 222180192
A = 4 # [acessos] Numero de acessos minimo
B = 12 # [acessos] Moda do numero de acessos
C = 20 # [acessos] Numero de acessos maximo
# CPU 1
CPM1 = 128 # KB - Capacidade de memoria da placa 1
MEDIA1 = 90 # KB - Do tamanho dos programas na memoria 1
DESV_PAD1 = 40 # KB - Do tamanho dos programas na memoria 1
# CPU 2
CPM2 = 64 # KB - Capacidade de memoria da placa 2
MEDIA2 = 110 # KB - Do tamanho dos programas na memoria 2
DESV_PAD2 = 20 # KB - Do tamanho dos programas na memoria 1
# MEM CACHE 1
TC1 = 0.4
TM1 = 3
H1 = 0.7
# MEM CACHE 2
TC2 = 0.4
TM2 = 3
H2 = 0.7
# CONSTANTES
K = 1 # Conversao KB

# === DISTRIBUICOES === #
class Distribuicoes:
    @staticmethod
    def triangular(a, b, c, r):
        if r <= ((b-a)/(c-a)):
            return round(a+math.sqrt(r*(b-a)*(c-a)))
        else:
            return round(c-math.sqrt((1-r)*(c-b)*(c-a)))

# === METODOS ALEATORIOS === #
class Aleatorio:
    def __init__(self, semente=SEMENTE):
        self.semente = semente
    def meio_quadrado(self):
        tamanho = int(math.log10(abs(self.semente))+1) if self.semente != 0 else 1 # Numero de digitos na semente
        x = str(self.semente**2).zfill(2*tamanho) # Preenche zeros a esquerda
        x = x[::-1] # Inverte x pra facilitar a priorizacao dos menos significativos
        x = x[int(tamanho/2):int(3*tamanho/2)][::-1] # Pega a parte do meio
        self.semente = int(x) # Converte devolta para inteiro e atualiza a semente
        return self.semente/int('9'*tamanho) # Retorna normalizado
    def congruencia_linear(self, a=9, c=1, m=64):
        self.semente = (a*self.semente + c) % m # Atualiza semente e calcula o aleatorio ao mesmo tempo
        return self.semente / m

# === DEFINICOES === #
Z = lambda r1, r2: math.sqrt(-2*math.log(r1))*math.cos(2*math.pi*r2)
M = lambda z, desv_pad, media: z*desv_pad+media # Tamanho do programa
T = lambda theta, r3, num_acessos, t_medio, fc: ((-theta*math.log(r3))+(num_acessos*t_medio))*fc # Tempo de processamento do programa
T_MEDIO = lambda h, tc, tm: h*tc+(1-h)*tm # Tempo de acesso a memoria medio
FC = lambda io: 1 if io <= 50 else 1.5 if io <= 75 else 2.0 if io <= 85 else 4 # Fator de ocupacao
Theta = lambda m, k, factor: (factor*m)/k
IO = lambda cpm, m: 100*m/cpm

# === VARIAVEIS ALEATORIAS === #
Aleatorio_R1 = Aleatorio()
Aleatorio_R2 = Aleatorio()
R1 = [Aleatorio_R1.meio_quadrado() for _ in range(NUM_SIMULACOES)] # Aleatorios p/ alimentar z
R2 = [Aleatorio_R1.congruencia_linear() for _ in range(NUM_SIMULACOES)] # Aleatorios p/ alimentar z
random.seed(SEMENTE) # Setando a semente na funcao aleatoria do python
R3 = [random.random() for _ in range(NUM_SIMULACOES)] # Aleatorios p/ alimentar tempos de processamento
random.seed(SEMENTE*123) # Setando outra semente nova
R4 = [random.random() for _ in range(NUM_SIMULACOES)] # Aleatorios p/ alimentar o numero de acessos a cpu 1
random.seed(SEMENTE*321) # Setando outra semente nova
R5 = [random.random() for _ in range(NUM_SIMULACOES)] # Aleatorios p/ alimentar o numero de acessos a cpu 2

# === PARAMETROS === #
# CPU 1
estatisticas_cpu1 = [(DESV_PAD1, MEDIA1, CPM1) for _ in range(NUM_SIMULACOES)]
desv_pad_cpu1, media_cpu1, cpms_cpu1 = zip(*estatisticas_cpu1)
# CPU 2
estatisticas_cpu2 = [(DESV_PAD2, MEDIA2, CPM2) for _ in range(NUM_SIMULACOES)]
desv_pad_cpu2, media_cpu2, cpms_cpu2 = zip(*estatisticas_cpu2)
# AUXILIAR
k = [K for _ in range(NUM_SIMULACOES)]
A_ = [A for _ in range(NUM_SIMULACOES)]
B_ = [B for _ in range(NUM_SIMULACOES)]
C_ = [C for _ in range(NUM_SIMULACOES)]
H1_ = [H1 for _ in range(NUM_SIMULACOES)]
TC1_ = [TC1 for _ in range(NUM_SIMULACOES)]
TM1_ = [TM1 for _ in range(NUM_SIMULACOES)]
H2_ = [H2 for _ in range(NUM_SIMULACOES)]
TC2_ = [TC2 for _ in range(NUM_SIMULACOES)]
TM2_ = [TM2 for _ in range(NUM_SIMULACOES)]

# === SIMULACAO === #
# COMPARTILHADO
z = list(map(Z, R1, R2)) # Valores de z
# CACHE 1
t_medio1 = list(map(T_MEDIO, H1_, TC1_, TM1_)) # Tempo medio de acesso ao cache 1
# CACHE 2
t_medio2 = list(map(T_MEDIO, H2_, TC2_, TM2_)) # Tempo medio de acesso ao cache 2
# CPU 1
num_acessos1 = list(map(Distribuicoes.triangular, A_, B_, C_, R4)) # num de acessos aos programas 1
m1 = list(map(M, z, desv_pad_cpu1, media_cpu1)) # Tamanho dos programas
io1 = list(map(IO, cpms_cpu1, m1)) # Indice de ocupacao
fc1 = list(map(FC, io1)) # Fator de correcao
theta1 = list(map(Theta, m1, k, [0.5 for _ in range(NUM_SIMULACOES)])) # Thetas
t1 = list(map(T, theta1, R3, num_acessos1, t_medio1, fc1)) # Tempos de processamento
tacc1 = [sum(t1[:i]) for i in range(1,NUM_SIMULACOES+1)] # Tempos acumulados
# CPU 2
num_acessos2 = list(map(Distribuicoes.triangular, A_, B_, C_, R5))
m2 = list(map(M, z, desv_pad_cpu2, media_cpu2)) # Tamanho dos programas
io2 = list(map(IO, cpms_cpu2, m2)) # Indice de ocupacao
fc2 = list(map(FC, io2)) # Fator de correcao
theta2 = list(map(Theta, m2, k, [0.7 for _ in range(NUM_SIMULACOES)])) # Thetas
t2 = list(map(T, theta2, R3, num_acessos2, t_medio2, fc2)) # Tempos de processamento
tacc2 = [sum(t2[:i]) for i in range(1,NUM_SIMULACOES+1)] # Tempos acumulados

# === ESTATISTICAS DA SIMULACAO === #
# Medias
m1_medio = statistics.mean(m1)
m2_medio = statistics.mean(m2)
t1_medio = statistics.mean(t1)
t2_medio = statistics.mean(t2)
io1_medio = statistics.mean(io1)
io2_medio = statistics.mean(io2)
# Desvios padrao
m1_desv_pad = statistics.stdev(m1)
m2_desv_pad = statistics.stdev(m2)
t1_desv_pad = statistics.stdev(t1)
t2_desv_pad = statistics.stdev(t2)
io1_desv_pad = statistics.stdev(io1)
io2_desv_pad = statistics.stdev(io2)
# Variancia
m1_variancia = statistics.variance(m1)
m2_variancia = statistics.variance(m2)
t1_variancia = statistics.variance(t1)
t2_variancia = statistics.variance(t2)
io1_variancia = statistics.variance(io1)
io2_variancia = statistics.variance(io2)

# === CABECALHO === #
cabecalho = """\
|    Programa   | Tamanho  | Tamanho  | Tempo de      | Tempo de      |   Tempo   |   Tempo   | Indice de  | Indice de  |  R1  |  R2  |  R3  |   Z   | Theta | Theta |
|               | Programa | Programa | Processamento | Processamento | Acumulado | Acumulado | ocupacao   | ocupacao   |      |      |      |       |   01  |   02  |
|               |    01    |    02    | na CPU 1      | na CPU 2      | na CPU 1  | na CPU 2  | na CPU 1   | na CPU 2   |      |      |      |       |       |       |"""
divisao = "+---------------+----------+----------+---------------+---------------+-----------+-----------+------------+------------+------+------+------+-------+-------+-------+"



# === TABELA === #
print()
print(divisao)
print(cabecalho)
print(divisao)
for i in range(NUM_SIMULACOES):
    # Lista dos valores a serem impressos nesta linha
    valores = [
        i+1,
        m1[i], 
        m2[i], 
        t1[i],
        t2[i], 
        tacc1[i],
        tacc2[i], 
        io1[i],
        io2[i],
        R1[i], R2[i], R3[i],
        z[i], theta1[i], theta2[i]
    ]
    # Formatacao para imprimir
    formatacao = f"| {'{:^13}'} | {'{:^8.2f}'} | {'{:^8.2f}'} | {'{:^13.2f}'} | {'{:^13.2f}'} | {'{:^9.2f}'} | {'{:^9.2f}'} | {'{:^10.2f}'} | {'{:^10.2f}'} | {'{:^4.2f}'} | {'{:^4.2f}'} | {'{:^4.2f}'} | {'{:^5.2f}'} | {'{:^5.2f}'} | {'{:^5.2f}'} |"
    print(formatacao.format(*valores))

print(divisao)
formatacao_media = "| {:^13} | {:^8.2f} | {:^8.2f} | {:^13.2f} | {:^13.2f} | {:^9} | {:^9} | {:^10.2f} | {:^10.2f} |" 
formatacao_desv_pad = "| {:^13} | {:^8.2f} | {:^8.2f} | {:^13.2f} | {:^13.2f} | {:^9} | {:^9} | {:^10.2f} | {:^10.2f} |" 
formatacao_var_pad = "| {:^13} | {:^8.2f} | {:^8.2f} | {:^13.2f} | {:^13.2f} | {:^9} | {:^9} | {:^10.2f} | {:^10.2f} |" 
print(formatacao_media.format('Media', m1_medio, m2_medio, t1_medio, t2_medio, '---', '---', io1_medio, io2_medio))
print(formatacao_desv_pad.format('Desvio Padrao', m1_desv_pad, m2_desv_pad, t1_desv_pad, t2_desv_pad, '---', '---', io1_desv_pad, io2_desv_pad))
print(formatacao_desv_pad.format('Variancia', m1_variancia, m2_variancia, t1_variancia, t2_variancia, '---', '---', io1_variancia, io2_variancia))
print(divisao[:121])
print()

# === PLOTA O GRAFICO (SE TIVER A BIBLIOTECA MATPLOTLIB INSTALADA) === #
try:
    fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(10,7))

    w = 0.2
    x1 = [i-w/2 for i in range(1,NUM_SIMULACOES+1)]
    x2 = [i+w/2 for i in range(1,NUM_SIMULACOES+1)]
    ax1.bar(x1, m1, width=w, color='b', align='center', label="Tamanho Programa 01")
    ax1.bar(x2, m2, width=w, color='r', align='center', label="Tamanho Programa 02")
    ax1.autoscale(tight=True)
    ax1.grid(axis='y')
    ax1.set_xticks(list(range(1,NUM_SIMULACOES+1)))
    ax1.legend()

    ax2.bar(x1, t1, width=w, color='b', align='center', label="Tempo de processamento 01")
    ax2.bar(x2, t2, width=w, color='r', align='center', label="Tempo de processamento 02")
    ax2.autoscale(tight=True)
    ax2.grid(axis='y')
    ax2.set_xticks(range(1,NUM_SIMULACOES+1))
    ax2.legend()

    ax3.bar(x1, io1, width=w, color='b', align='center', label="Indice de ocupação 01")
    ax3.bar(x2, io2, width=w, color='r', align='center', label="Indice de ocupação 02")
    ax3.autoscale(tight=True)
    ax3.grid(axis='y')
    ax3.set_xticks(range(1,NUM_SIMULACOES+1))
    ax3.legend()

    plt.show()

    fig, (ax1, ax2) = plt.subplots(2, figsize=(5,5))
    fig.suptitle("Distribuicao triangular gerada a partir dos numeros aleatorios")
    ax1.hist(num_acessos1, color='b', label="numero de acessos cpu 1")
    ax1.autoscale(tight=True)
    ax1.grid(axis='y')
    ax1.legend()
    ax2.hist(num_acessos2, color='r', label="numero de acessos cpu 2")
    ax2.autoscale(tight=True)
    ax2.grid(axis='y')
    ax2.legend()

    plt.show()

except Exception as e:
    print(e)