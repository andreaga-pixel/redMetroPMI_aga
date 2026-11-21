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

# ---------------------------------------------------------------
# C2: SIN LAZOS  ->  L = x_PE,PE + x_JV,JV + ... + x_MA,MA
# ---------------------------------------------------------------
L = 0                       # empezamos en 0 (False)
for a in V:
    L = int(L or x[a][a])   # OR acumulado con la diagonal

lazos = [a for a in V if x[a][a] == 1]   # qué estaciones tienen lazo
C2 = int(not L)                          # la condición se cumple si L = 0

print("\n=== C2: SIN LAZOS ===")
print(f"Estaciones comprobadas (diagonal): {len(V)}")
print(f"L = {L}")
print(f"Estaciones con lazo: {lazos}")
print(f"C2 = {C2}")

# Prueba: provoco un lazo en SC en una copia de la matriz
x_prueba2 = copy.deepcopy(x)
x_prueba2["SC"]["SC"] = 1
L_prueba = 0
for a in V:
    L_prueba = int(L_prueba or x_prueba2[a][a])
print(f"Prueba (lazo en SC): L = {L_prueba}, estaciones con lazo = "
      f"{[a for a in V if x_prueba2[a][a] == 1]}")


# ---------------------------------------------------------------
# C3: SERVICIO  ->  S_a = m1_a + m2_a   (simplificada)
#                   S = S_PE · S_JV · ... · S_MA
# ---------------------------------------------------------------
m1 = {a: int("M1" in g.lineas[a]) for a in V}   # 1 si para la M1
m2 = {a: int("M2" in g.lineas[a]) for a in V}   # 1 si para la M2

S = 1                      # empezamos en 1 para el AND acumulado
sin_servicio = []
simplificacion_ok = True

for a in V:
    S_a = int(m1[a] or m2[a])                            # simplificada
    S_larga = int((not m1[a] and m2[a]) or               # ¬m1·m2
                  (m1[a] and not m2[a]) or               # + m1·¬m2
                  (m1[a] and m2[a]))                     # + m1·m2
    if S_a != S_larga:
        simplificacion_ok = False
    if S_a == 0:
        sin_servicio.append(a)
    S = int(S and S_a)                                   # AND acumulado

C3 = S

print("\n=== C3: SERVICIO ===")
print(f"Estaciones donde para M1: {sum(m1.values())}")
print(f"Estaciones donde para M2: {sum(m2.values())}")
print(f"Estaciones sin ninguna línea: {sin_servicio}")
print(f"¿Ecuación larga = simplificada en las 17? {simplificacion_ok}")
print(f"C3 = {C3}")

# Prueba: quito las dos líneas a PI en una copia
m1_p, m2_p = dict(m1), dict(m2)
m1_p["PI"], m2_p["PI"] = 0, 0
S_prueba = 1
for a in V:
    S_prueba = int(S_prueba and (m1_p[a] or m2_p[a]))
print(f"Prueba (PI sin líneas): S = {S_prueba}, sin servicio = "
      f"{[a for a in V if not (m1_p[a] or m2_p[a])]}")



# ---------------------------------------------------------------
# C4: CONECTIVIDAD  ->  V_ab = AND de las estaciones (o) y los
#                       tramos (x) del camino de a a b
# ---------------------------------------------------------------
from itertools import combinations

def camino(origen, destino):
    # Recorrido BFS (como en es_conexo de la Parte 1), guardando
    # desde qué estación se llega a cada una para reconstruir el camino
    anterior = {origen: None}
    cola = [origen]
    while cola:
        v = cola.pop(0)
        for arista in g.vecinos(v):
            if arista.destino not in anterior:
                anterior[arista.destino] = v
                cola.append(arista.destino)
    ruta = [destino]
    while ruta[-1] != origen:               # vuelvo hacia atrás
        ruta.append(anterior[ruta[-1]])
    return ruta[::-1]                       # le doy la vuelta

def viaje_posible(a, b, o):
    # V_ab = o_a · x_a,v1 · o_v1 · ... · o_b
    ruta = camino(a, b)
    V_ab = 1
    for v in ruta:                          # AND de las estaciones
        V_ab = int(V_ab and o[v])
    for i in range(len(ruta) - 1):          # AND de los tramos
        V_ab = int(V_ab and x[ruta[i]][ruta[i + 1]])
    return V_ab

pares = list(combinations(V, 2))            # todos los pares (a, b)

# Escenario 1: red normal (todas las estaciones abiertas)
o = {a: 1 for a in V}
posibles = sum(viaje_posible(a, b, o) for a, b in pares)
C4 = int(posibles == len(pares))

print("\n=== C4: CONECTIVIDAD ===")
print(f"Pares de estaciones (viajes): {len(pares)}")
print(f"Red normal -> viajes posibles: {posibles}")
print(f"C4 = {C4}")

# Escenario 2: cierre de Son Costa - Son Fortesa
o_cierre = dict(o)
o_cierre["SC"] = 0
print(f"\nCamino PB -> MA: {camino('PB', 'MA')}")
print(f"SC cerrada -> V_JV,SF = {viaje_posible('JV', 'SF', o_cierre)}, "
      f"V_PB,UIB = {viaje_posible('PB', 'UIB', o_cierre)}, "
      f"V_PB,MA = {viaje_posible('PB', 'MA', o_cierre)}")
posibles_cierre = sum(viaje_posible(a, b, o_cierre) for a, b in pares)
print(f"SC cerrada -> viajes posibles: {posibles_cierre} de {len(pares)} "
      f"({100 * posibles_cierre / len(pares):.1f} %)")
print(f"SC cerrada -> viajes perdidos: {len(pares) - posibles_cierre}")


# ---------------------------------------------------------------
# SISTEMA DE VERIFICACIÓN  ->  RED_OK = C1 · C2 · C3 · C4
# ---------------------------------------------------------------
RED_OK = int(C1 and C2 and C3 and C4)

print("\n=== SISTEMA DE VERIFICACIÓN DE LA RED ===")
print(f"Escenario 1 (red real):        C1={C1} C2={C2} C3={C3} C4={C4} "
      f"-> RED_OK = {RED_OK}")

# Escenario 2: cierre de SC (reutilizo el resultado del apartado C4)
C4_cierre = int(posibles_cierre == len(pares))
print(f"Escenario 2 (SC cerrada):      C1={C1} C2={C2} C3={C3} C4={C4_cierre} "
      f"-> RED_OK = {int(C1 and C2 and C3 and C4_cierre)}")

# Escenario 3: tramo de sentido único (reutilizo la prueba de C1)
C1_prueba = int(len(fallos_prueba) == 0)
print(f"Escenario 3 (sentido único):   C1={C1_prueba} C2={C2} C3={C3} C4={C4} "
      f"-> RED_OK = {int(C1_prueba and C2 and C3 and C4)}")

# ---------------------------------------------------------------
# ESTRUCTURA DE LA RED: operaciones de conjuntos con matrices booleanas
# ---------------------------------------------------------------
# Una matriz booleana para cada línea (columna "lineas" de conexiones.csv)
x_M1 = {a: {b: 0 for b in V} for a in V}
x_M2 = {a: {b: 0 for b in V} for a in V}
for a in V:
    for arista in g.vecinos(a):
        if "M1" in arista.lineas:
            x_M1[a][arista.destino] = 1
        if "M2" in arista.lineas:
            x_M2[a][arista.destino] = 1

def contar(m):
    return sum(m[a][b] for a in V for b in V)

# OR, AND y NOT casilla a casilla
union = {a: {b: int(x_M1[a][b] or x_M2[a][b]) for b in V} for a in V}
inter = {a: {b: int(x_M1[a][b] and x_M2[a][b]) for b in V} for a in V}
compl = {a: {b: int(not x[a][b]) for b in V} for a in V}

print("\n=== ESTRUCTURA DE LA RED (CONJUNTOS DE TRAMOS) ===")
print(f"Tramos de M1: {contar(x_M1) // 2}")
print(f"Tramos de M2: {contar(x_M2) // 2}")
print(f"M1 ∪ M2 (OR):  {contar(union) // 2} tramos. ¿Es la red completa? {union == x}")
print(f"M1 ∩ M2 (AND): {contar(inter) // 2} tramos: "
      f"{[(a, b) for a in V for b in V if inter[a][b] and V.index(a) < V.index(b)]}")
print(f"Complemento (NOT): {contar(compl)} casillas a 1")
print(f"  -> tramos nuevos posibles (sin diagonal, sin repetir): "
      f"{sum(compl[a][b] for a in V for b in V if a != b) // 2}")


