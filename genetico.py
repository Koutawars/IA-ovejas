from random import randrange, choice, random
import numpy as np

peso = 20 # peso del carro
numPoblacion = 10 # numero de población
numHijos = 2 # 1 = 2 padres o num hijos
tamanoCampeonato = 2 # tamaño del campeonato
pMutacion = 0.15 # probabilidad de mutación
generacionesMaxima = 300 # generaciones máxima

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

def valorSolo(a):
    return Mapa[a][1]

def valor(vec):
    suma = 0
    for x in vec:
        suma += Mapa[x][1]
    return suma

def elegirAzar(vec, num):
    aux = vec[:]
    azar = []
    i = 0
    while True:
        cho = choice(aux)
        azar.append(cho)
        aux.remove(cho)
        i+=1
        if(i >= num):
            break
    return azar

# mutar en un indice aleatorio con una oveja aleatoria
def mutar(hijo):
    indice = randrange(len(hijo))
    ovejas = set(Mapa.keys())
    ovejas = list(ovejas - set(hijo))
    while True:
        hijo[indice] = choice(ovejas)
        if(medirPeso(hijo) <= peso): 
            break
        ovejas.remove(hijo[indice]) 
        if(len(ovejas) == 0):
            break
    return hijo

# conseguir población N
def conseguirPoblacion(num):
    vecinos = [] 
    i = 0
    while True:
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
        vecinos.append(vecino)
        i = i + 1 
        if(i >= num): 
            break
    return vecinos

def main():
    # generación de población inicial
    poblacion = conseguirPoblacion(numPoblacion)
    poblacionAnt = poblacion
    # evaluación (ordenar de mayor a  menor por valor)
    poblacion.sort(reverse = True, key = valor)
    for i in range(generacionesMaxima):
        # selección por campeonato
        select = []
        for k in range(numHijos):
            compiten = elegirAzar(poblacion, tamanoCampeonato)
            compiten.sort(reverse = True, key = valor)
            padre1 = compiten[0]
            compiten = elegirAzar(poblacion, tamanoCampeonato)
            compiten.sort(reverse = True, key = valor)
            padre2 = compiten[0]
            select.append((padre1, padre2))
        # cruzamiento
        hijos = []
        for k in select:
            unidos = k[0] + k[1]
            unidos = list(dict.fromkeys(unidos).keys())
            unidos.sort(reverse = True, key = valorSolo)
            aux = []
            for p in unidos:
                aux.append(p)
                if (medirPeso(aux) > peso):
                    aux.pop()
                    break
                if(len(aux) == 0):
                    break
            hijos.append(aux)
        # mutación
        for k in range(len(hijos)):
            numberRandom = random()
            if(numberRandom < pMutacion):
                hijos[k] = mutar(hijos[k])
        # reemplazo (reemplazo los peores)
        poblacion = poblacion[:len(poblacion) - numHijos]
        poblacion = poblacion[:] + hijos[:]
        poblacion.sort(reverse = True, key = valor)
        print("Generación n.", i,": ", poblacion)
        if(np.array_equal(poblacion, poblacionAnt)):
            break 
        poblacionAnt = poblacion
    print("Resultado: ", poblacion[0])

if __name__ == "__main__":
    main()