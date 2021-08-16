import math
import random
import statistics

# === ENUNCIADO === #
NUM_SIMULACOES = 10 # Numero de simulacoes que devem ser realizadas
CPM1 = 128 # KB - Capacidade de memoria da placa 1
CPM2 = 64 # KB - Capacidade de memoria da placa 2
MEDIA1 = 90 # KB - Do tamanho dos programas na memoria 1
MEDIA2 = 110 # KB - Do tamanho dos programas na memoria 2
DESV_PAD1 = 40 # KB - Do tamanho dos programas na memoria 1
DESV_PAD2 = 20 # KB - Do tamanho dos programas na memoria 1
K = 1

# === DEFINICOES === #
Z = lambda R1, R2: math.sqrt(-2*math.log(R1))*math.cos(2*math.pi*R2)
M = lambda Z, desv_pad, media: Z*desv_pad+media # Tamanho do programa
T = lambda theta, R3: -1*theta*math.log(R3) # Tempo de processamento do programa
Theta = lambda M, K: (0.5*M)/K
IO = lambda cpm, m: 100*m/cpm

# === VARIAVEIS ALEATORIAS === #
R1 = [random.random() for _ in range(NUM_SIMULACOES)]
R2 = [random.random() for _ in range(NUM_SIMULACOES)]
R3 = [random.random() for _ in range(NUM_SIMULACOES)]

# === AUXILIARES === #
estatisticas = [(DESV_PAD2, MEDIA2) if i%2 else (DESV_PAD1, MEDIA1) for i in range(NUM_SIMULACOES)] # Calcula um vetor com as estatisticas intercaladas
desv_pad, media = zip(*estatisticas) # Duas listas, uma para desvio padrao e outra para media
cpms = [CPM2 if i%2 else CPM1 for i in range(NUM_SIMULACOES)] # Lista com os cpm intercalados 
k = [K for _ in range(NUM_SIMULACOES)] # Lista com valores de k

# === CALCULOS === #
z = list(map(Z, R1, R2)) # Valores de z
m = list(map(M, z, desv_pad, media)) # Tamanho dos programas
theta = list(map(Theta, m, k)) # Thetas
t = list(map(T, theta, R3)) # Tempos de processamento
tacc = [sum(t[:i]) for i in range(1,NUM_SIMULACOES+1)] # Tempos acumulados
io = list(map(IO, cpms, m)) # Indice de ocupacao

# === ESTATISTICAS DA SIMULACAO === #
# Medias
m1_medio = statistics.mean(m[::2])
m2_medio = statistics.mean(m[1::2])
t_medio = statistics.mean(t)
io1_medio = statistics.mean(io[::2])
io2_medio = statistics.mean(io[1::2])
# Desvios padrao
m1_desv_pad = statistics.stdev(m[::2])
m2_desv_pad = statistics.stdev(m[1::2])
t_desv_pad = statistics.stdev(t)
io1_desv_pad = statistics.stdev(io[::2])
io2_desv_pad = statistics.stdev(io[1::2])
# Variancia
m1_variancia = statistics.variance(m[::2])
m2_variancia = statistics.variance(m[1::2])
t_variancia = statistics.variance(t)
io1_variancia = statistics.variance(io[::2])
io2_variancia = statistics.variance(io[1::2])

# === CABECALHO === #
cabecalho = """\
|    Programa   | Tamanho1 | Tamanho2 | Tempo de      |   Tempo   | Indice de  | Indice de  |  R1  |  R2  |  R3  |   Z   | Theta |
|               |          |          | Processamento | Acumulado | ocupacao 1 | ocupacao 2 |      |      |      |       |       |"""
divisao = "+---------------+----------+----------+---------------+-----------+------------+------------+------+------+------+-------+-------+"

# === TABELA === #
print()
print(divisao)
print(cabecalho)
print(divisao)
for i in range(NUM_SIMULACOES):
    m1 = i%2 == 0
    # Lista dos valores a serem impressos nesta linha
    valores = [
        i+1,
        m[i] if m1 else '---', 
        m[i] if not m1 else '---', 
        t[i], 
        tacc[i], 
        io[i] if m1 else '---',
        io[i] if not m1 else '---',
        R1[i], R2[i], R3[i],
        z[i], theta[i]
    ]
    # Formatacao para imprimir
    formatacao = f"| {'{:^13}'} | {'{:^8.2f}' if m1 else '{:^8}'} | {'{:^8.2f}' if not m1 else '{:^8}'} | {'{:^13.2f}'} | {'{:^9.2f}'} | {'{:^10.2f}' if m1 else '{:^10}'} | {'{:^10.2f}' if not m1 else '{:^10}'} | {'{:^4.2f}'} | {'{:^4.2f}'} | {'{:^4.2f}'} | {'{:^5.2f}'} | {'{:^5.2f}'} |"
    print(formatacao.format(*valores))

print(divisao)
formatacao_media = "| {:^13} | {:^8.2f} | {:^8.2f} | {:^13.2f} | {:^9} | {:^10.2f} | {:^10.2f} |" 
formatacao_desv_pad = "| {:^13} | {:^8.2f} | {:^8.2f} | {:^13.2f} | {:^9} | {:^10.2f} | {:^10.2f} |" 
formatacao_var_pad = "| {:^13} | {:^8.2f} | {:^8.2f} | {:^13.2f} | {:^9} | {:^10.2f} | {:^10.2f} |" 
print(formatacao_media.format('Media', m1_medio, m2_medio, t_medio, '---', io1_medio, io2_medio))
print(formatacao_desv_pad.format('Desvio Padrao', m1_desv_pad, m2_desv_pad, t_desv_pad, '---', io1_desv_pad, io2_desv_pad))
print(formatacao_desv_pad.format('Variancia', m1_variancia, m2_variancia, t_variancia, '---', io1_variancia, io2_variancia))
print(divisao[:93])
print()