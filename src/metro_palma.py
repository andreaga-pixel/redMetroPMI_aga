
## Representación del Metro de Palma como grafo.
#Representación elegida: LISTA DE ADYACENCIA implementada con LISTAS ENLAZADAS.

#Modelo: G = (V, E), grafo NO dirigido y PONDERADO.
###V (nodos)   = estaciones -> data/estaciones.csv
###E (aristas) = tramos entre estaciones consecutivas -> data/conexiones.csv
###peso = tiempo estimado del tramo en minutos (dato simulado)

import csv #carga de datos desde ficheros CSV
from pathlib import Path #carga una herramienta para trabajar con rutas de carpetas

# Carpeta data/ del repositorio (un nivel por encima de src/)
CARPETA_DATOS = Path(__file__).resolve().parent.parent / "data"


#------------------------------------------------------------------------------
# NODO DE LA LISTA ENLAZADA: representa una arista que sale de una estación.
#------------------------------------------------------------------------------

class NodoArista:
    def __init__(self, destino, lineas, tiempo_min):
        self.destino = destino #guarda la estación vecina
        self.lineas = lineas #lista de lineas que recorren el tramo
        self.tiempo_min = tiempo_min #tiempo estimado del tramo en minutos.Peso de la arista.
        self.siguiente = None #puntero al siguiente nodo de la lista enlazada, al vecino. 

#-----------------------------------------------------------------------------------
# EL GRAFO: cada estación tiene la "cabecera" de su lista enlazada de vecinos
#----------------------------------------------------------------------------------

class GrafoMetro:
    def __init__(self):
        self.nombre = {} #id->nombre completo de la estación
        self.lineas ={} #id->lineas que paran en ella
        self.cabeza ={} #id->primer NodoArista. Las cabezas del diagrama o None si no tiene vecinos

    #añadir una estación
    def anadir_estacion(self, id_est, nombre, lineas):
        if id_est in self.cabeza: #validación, si ya existe (estación) -> ERROR
            raise ValueError(f"Estación duplicada:{id_est}")
        self.nombre[id_est]=nombre #guarda el nombre de la estación
        self.lineas[id_est]=lineas #guarda las lineas
        self.cabeza[id_est]= None #None porque aún no tiene vecinas

    #insertar un nodo al principio de la lista enlazada
    def _insertar(self, origen, destino, lineas, tiempo_min):
        nuevo = NodoArista(destino, lineas, tiempo_min) #se crea nuevo nodo [SF]
        nuevo.siguiente = self.cabeza[origen] #el nuevo apunta al que ela el 1º [SF]->SFV->JV->None
        self.cabeza[origen] = nuevo #la cabeza apunta al nuevo SC ->[SF]->SFV->JV->None

    #Añadir una conexión
    def anadir_conexion(self, a, b, lineas, tiempo_min):
        for i in (a,b): #validación: comprueba que las dos estaciones si existen
            if i not in self.cabeza:
                raise ValueError(f"Estación inexistente: {i}")
        self._insertar(a, b, lineas, tiempo_min) #el tramo se inserta en la lista de a apuntando a b
        self._insertar(b, a, lineas, tiempo_min) #el tramo se inserta en la lista b apuntando a a

    #Recorrer las vecinas de una estación
    def vecinos(self, id_est):
        #recorre la lista enlazada nodo a nodo
        actual = self.cabeza[id_est] #empieza en el primer nodo, cabeza
        while actual is not None: #mientras que no llegue al final=None
            yield actual # entrega ese nodo a quien lo ha pedido
            actual = actual.siguiente #sigue la flecha al siguiente nodo

    #Grado de una estación
    def grado(self, id_est):
        return sum(1 for _ in self.vecinos(id_est))
    #_ es una variable que no se usa, solo importa contar

    #Número de nodos y aristas
    #hay una cabeza por estación así que basta con contarlas
    def num_nodos(self):
        return len(self.cabeza)

    #Suma los grados de todas las estaciones y divide entre 2. 
    #porque cada tramo está guradado dos veces.
    def num_aristas(self):
        #cada arista aparece dos veces. Una en cada extremo
        return sum(self.grado(v) for v in self.cabeza) // 2

    #Recorrido en anchura BFS, ¿es conexo?
    def es_conexo(self):
        #recorrido en alchura desde cualquier estación
        inicio = next(iter(self.cabeza))
        visitados, cola = {inicio}, [inicio]
        while cola:
            v= cola.pop(0)
            for arista in self.vecinos(v):
                if arista.destino not in visitados:
                    visitados.add(arista.destino)
                    cola.append(arista.destino)
        return len(visitados) == self.num_nodos()

    #Mostrar lista de adyacencia
    def mostrar(self):
        for v in self.cabeza:
            cadena = " -> ".join(
                f"[{a.destino}, {'/'.join(a.lineas)}, {a.tiempo_min}']"
                for a in self.vecinos(v))
            print(f"{v:>4} ({self.nombre[v]}): {cadena} -> None")








