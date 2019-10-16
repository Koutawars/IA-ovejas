from random import randrange, choice
import time as tm
import math
import random
import cargarArchivo as ca

def conseguirVecino():
    aux = list(Mapa.keys())
    vecino = []
    while True:
        x = choice(aux)
        aux.remove(x)
        vecino.append(x)
        if(medirPeso(vecino) > peso):
            vecino.pop()
            break
        if(len(aux) == 0):
            break
    return vecino

def medirPeso(a):
    result = 0
    for x in a:
        result += Mapa[x][0]
    return result

def valor(vec):
    suma = 0
    for x in vec:
        suma += Mapa[x][1]
    return suma

peso = 20 # peso del carro
v = 1 # numero de vecinos

# mapa de ovejas
# ID: (PESO, VALOR)
'''
Mapa = {
    1: (10, 100),
    2: (8, 95),
    3: (9, 80),
    4: (10, 80),
    5: (9, 70),
    6: (8, 90)
}
'''
Mapa = ca.cargar()


# Numero de ciclos
n = 50
# Numero de intentos por ciclo
m = 50

# Probabilidad de elegir la peor solución
p1 = 0.7
# Probabilidad de elegir la peor solución al final
p50 = 0.001
# Temperatura inicial
t1 = -1.0/math.log(p1)
# Temperatura final
t50 = -1.0/math.log(p50)
# Reduccion por cada ciclo
frac = (t50/t1)**(1.0/(n-1.0))
# Temperatura
t = t1

# configuraciones
na = 1.0
fc = valor(conseguirVecino())
DeltaE_avg = 0.0
j = 0
for i in range(n):
    print('Cycle: ' + str(i) + ' with Temperature: ' + str(t))
    for j in range(m):
        vecino = conseguirVecino()
        DeltaE = abs(valor(vecino) - fc)
        
        if (valor(vecino) < fc):
            if (i==0 and j==0 or DeltaE_avg == 0.0): DeltaE_avg = DeltaE
            p = math.exp(-DeltaE/(DeltaE_avg * t))
            if (random.random() < p):
                accept = True
            else:
                accept = False
        else:
            accept = True
        if (accept==True):
            current = vecino
            fc = valor(current)
            na = na + 1.0
            DeltaE_avg = (DeltaE_avg * (na-1.0) +  DeltaE) / na
    t = frac * t
print("Solución: ", current)