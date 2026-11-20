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

