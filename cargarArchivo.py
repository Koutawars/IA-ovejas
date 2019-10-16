def cargar():
    map = {}
    archivo = open('ovejas.txt','r')
    filas = archivo.readlines()
    for fila in filas:
        ptr = fila.split()
        id = int(ptr[0])
        peso = int(ptr[1])
        valor = int(ptr[2])
        map[id] = (peso, valor)
    return map