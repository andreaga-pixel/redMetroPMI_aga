#Parte 3: Ecuaciones booleanas sobre la de metro de Palma
#Reutiliza la carga del grafo de la Parte 1 (metro_palma.py)

from metro_palma import cargar_grafo, CARPETA_DATOS

#1. Cargar la red desde los CSV
g = cargar_grafo(CARPETA_DATOS / "estaciones.csv", CARPETA_DATOS / "conexiones.csv")
V = list(g.cabeza) #lista con las 17 estaciones

#2. Crear la matriz booleana x_ab, con todo a 0, es decir False
x = {a:{b: 0 for b in V} for a in V} #un diccionario dentro de otro, funciona como una tabla x["PE"]["JV"]


#3. Poner a los 1 los tramos que existen, corriendo la lista enlazada
for a in V:
    for arista in g.vecinos(a):
        x[a][arista.destino] = 1

#Comprobación 
unos =  sum(x[a][b] for a in V for b in V)
print("=== MATRIZ BOOLEANA ===")
print(f"Variables x_ab: {len(V) * len(V)}")
print(f"Variables a 1: {unos}")
print(f"Variables a 0: {len(V) * len(V) - unos}")
print("x_PE,JV =", x["PE"]["JV"], "| x_SC,SF =", x["SC"]["SF"],
      "| x_SF,SC =", x["SF"]["SC"], "| x_PE,SC =", x["PE"]["SC"],
      "| x_PE,PE =", x["PE"]["PE"])

