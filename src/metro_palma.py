
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
    def __init__(self, destino, lineas, tiempo):
        self.destino = destino #guarda la estación vecina
        self.lineas = lineas #lista de lineas que recorren el tramo
        self.tiempo = tiempo #tiempo estimado del tramo en minutos.Peso de la arista.
        self.siguiente = None #puntero al siguiente nodo de la lista enlazada, al vecino. 


