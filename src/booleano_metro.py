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

# ---------------------------------------------------------------
# C1: SIMETRÍA  ->  F_ab = x_ab · ¬x_ba   (detector de fallo)
#                   ¬F_ab = ¬x_ab + x_ba  (versión De Morgan)
# ---------------------------------------------------------------
fallos_c1 = []          # aquí se guardan los pares que fallen
de_morgan_ok = True     # pasa a False si De Morgan no coincide

for a in V:
    for b in V:
        F = int(x[a][b] and not x[b][a])          # x_ab AND (NOT x_ba)
        cumple = int((not x[a][b]) or x[b][a])    # (NOT x_ab) OR x_ba
        if F == 1:
            fallos_c1.append((a, b))
        if cumple != int(not F):                  # ¿¬F_ab = ¬x_ab + x_ba?
            de_morgan_ok = False

C1 = int(len(fallos_c1) == 0)   # 1 si no hay ningún fallo

print("\n=== C1: SIMETRÍA ===")
print(f"Pares comprobados: {len(V) * len(V)}")
print(f"Tramos de sentido único encontrados: {fallos_c1}")
print(f"¿De Morgan coincide en todos los pares? {de_morgan_ok}")
print(f"C1 = {C1}")

# Prueba: provoco un tramo de sentido único en una COPIA de la matriz
import copy
x_prueba = copy.deepcopy(x)   # copia independiente: la red real no cambia
x_prueba["SF"]["SC"] = 0      # quito el sentido SF -> SC

fallos_prueba = [(a, b) for a in V for b in V
                 if x_prueba[a][b] and not x_prueba[b][a]]
print(f"Prueba (quitando SF -> SC): fallos = {fallos_prueba}")

