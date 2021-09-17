from random import random
from math import log, log10, sqrt # log = base e

# === DADOS COMUNS === #
a = 110/3600 # msg/s (razao de mensagens no sistema)
theta = 8 # segundos

# === FORMULAS === #
# 4 formas diferentes de calcular o 'r' (nomeadas r, r_, r__ e r___)
def r(Lw):
    D = sqrt(pow(Lw,2)+(4*Lw))
    raiz1 = (-Lw-D)/2
    raiz2 = (-Lw+D)/2
    # Se a primeira raiz for maior q 1 ou menor que zero ela nao serve
    if raiz1 < 0 or raiz1 > 1:
        # Se a segunda raiz estiver entre 0 e 1 ela serve
        if raiz2 > 0 and raiz2 <= 1:
            return raiz2
        # Se nao nenhuma serve
        return None
    # Se 0 < r1 <= 1
    else:
        # E 0 < r2 <= 1
        if raiz2 > 0 and raiz2 <= 1:
            # Retorna a maior entre as duas (PIOR CASO)
            return max(raiz1, raiz2)
        # Caso contrario so a r1 serve
        return raiz1
def r_(Tw, K, a_):
    a = K/a_
    b = Tw
    c = -Tw
    D = sqrt(pow(b,2)-(4*a*c))
    raiz1 = (-b+D)/(2*a)
    raiz2 = (-b-D)/(2*a)
    # Se a primeira raiz for maior q 1 ou menor que zero ela nao serve
    if raiz1 < 0 or raiz1 > 1:
        # Se a segunda raiz estiver entre 0 e 1 ela serve
        if raiz2 > 0 and raiz2 <= 1:
            return raiz2
        # Se nao nenhuma serve
        return None
    # Se 0 < r1 <= 1
    else:
        # E 0 < r2 <= 1
        if raiz2 > 0 and raiz2 <= 1:
            # Retorna a maior entre as duas (PIOR CASO)
            return max(raiz1, raiz2)
        # Caso contrario so a r1 serve
        return raiz1
r__ = lambda Ppct, PPpct: pow(10,log10(1-(Ppct/100))/(PPpct+1))
r___ = lambda ts, a: a*ts
ts = lambda r, a: r/a
mi = lambda ts: 1/ts
Lw = lambda r: pow(r, 2)/(1-r)
Tw = lambda r, ts, k: r*ts*k/(1-r)
Tr = lambda ts, tw: ts+tw
PPpct = lambda r, Ppct: (log10(1-(Ppct/100))/log10(r))-1
amostra_exp = lambda theta, r: -theta*log(r)

# === COMPUTADOR 1 === #
K1 = 1.45
Ppct1 = 85 # %
PPpct1 = 2 # msg
r1 = r__(Ppct1, PPpct1)
ts1 = ts(r1, a)
mi1 = mi(ts1)
Lw1 = Lw(r1)
Tw1 = Tw(r1, ts1, K1)
Tr1 = Tr(ts1, Tw1)
print("====== COMPUTADOR 1 (C1) ======")
print("r = ", r1)
print("ts = ", ts1)
print("tw = ", Tw1)
print("tr = ", Tr1)
print("Lw = ", Lw1)
print("P({}%) = {}".format(Ppct1, PPpct1))

# === COMPUTADOR 2 === #
K2 = 1.25
Ppct2 = 85 # %
Lw2 = 3 # msg
r2 = r(Lw2)
ts2 = ts(r2, a)
mi2 = mi(ts2)
Tw2 = Tw(r2, ts2, K2)
Tr2 = Tr(ts2, Tw2)
PPpct2 = PPpct(r2, Ppct2)
print("====== COMPUTADOR 2 (C2) ======")
print("r = ", r2)
print("ts = ", ts2)
print("tw = ", Tw2)
print("tr = ", Tr2)
print("Lw = ", Lw2)
print("P({}%) = {}".format(Ppct2, PPpct2))

# === COMPUTADOR 3 === #
K3 = 1.45
Ppct3 = 85 # %
Tw3 = 12.15 # segundos
r3 = r_(Tw3, K3, a)
ts3 = ts(r3, a)
mi3 = mi(ts3)
Lw3 = Lw(r3)
Tr3 = Tr(ts3, Tw3)
PPpct3 = PPpct(r3, Ppct3)
print("====== COMPUTADOR 3 (C3) ======")
print("r = ", r3)
print("ts = ", ts3)
print("tw = ", Tw3)
print("tr = ", Tr3)
print("Lw = ", Lw3)
print("P({}%) = {}".format(Ppct3, PPpct3))

# === SERVIDOR === #
KS = 1 # K do servidor
Amostras = 20
PpctS = 85 # %
tsS = [amostra_exp(theta, random()) for _ in range(Amostras)]
rS = [r___(tsS[i], a) for i in range(Amostras)]
ts_medioS = sum(tsS)/Amostras
miS = [mi(tsS[i]) for i in range(Amostras)]
LwS = [Lw(rS[i]) for i in range(Amostras)]
TwS = [Tw(rS[i], tsS[i], KS) for i in range(Amostras)]
TrS = [Tr(tsS[i], TwS[i]) for i in range(Amostras)]
PPpctS = [PPpct(rS[i], PpctS) for i in range(Amostras)]
print("====== SERVIDOR ======")
print("r = ", sum(rS)/Amostras)
print("ts = ", list(map(float,list(map("{:.2f}".format, tsS)))))
print("ts (medio) = ", sum(tsS)/Amostras)
print("tw = ", sum(TwS)/Amostras)
print("tr = ", sum(TrS)/Amostras)
print("Lw = ", sum(LwS)/Amostras)
print("P({}%) = {}".format(PpctS, sum(PPpctS)/Amostras))