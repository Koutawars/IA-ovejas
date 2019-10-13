from random import randrange, choice
import time as tm
import math

peso = 20 # peso del carro
v = 1 # numero de vecinos

# mapa de ovejas
# ID: (PESO, VALOR)
Mapa = {
    1: (10, 100),
    2: (8, 95),
    3: (9, 80),
    4: (10, 80),
    5: (9, 70),
    6: (8, 90)
}

def medirPeso(a):
    result = 0
    for x in a:
        result += Mapa[x][0]
    return result

def conseguirVecino(mapa, num):
    vecinos = [] 
    i = 0
    while True:
        aux = list(mapa.keys())
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
        vecinos.append(vecino)
        i = i + 1 
        if(i >= num): 
            break
    vecinos.sort(reverse = True, key = valor)
    return vecinos

def hillClimbing(mapa, numVecinos):
    current = conseguirVecino(mapa, 1)[0]
    vecinos = conseguirVecino(mapa, numVecinos)
    t=tm.time()
    while True:
        print("Ahora: ", current)
        print("Vecinos: ", vecinos)
        if(valor(vecinos[0]) <= valor(current)):
            print("_______________________________")
            print("Con vecinos n = ", numVecinos, " peso = ", peso)
            print("Resultado: ", current, " -> valor: ", valor(current))
            print("---------Time: %02.03f ----------" % (tm.time()-t))
            return current
        current = vecinos[0]
        vecinos = conseguirVecino(mapa, numVecinos)

def valor(vec):
    suma = 0
    for x in vec:
        suma += Mapa[x][1]
    return suma

hillClimbing(Mapa, v)