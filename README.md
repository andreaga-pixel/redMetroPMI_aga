# Red de Metro de Palma como grafo

**Unit 18: Discrete Mathematics** (Pearson HND).

**Parte 1:** representación de una red de transporte público urbano mediante teoría de grafos.

La red de metro de Palma (líneas M1 y M2) se modela como un grafo
G = (V, E) **no dirigido y ponderado**:

- **Nodos (V):** las 17 estaciones.
- **Aristas (E):** los 16 tramos entre estaciones consecutivas.
- **Peso:** tiempo estimado del tramo en minutos (dato simulado).

La representación elegida es una **lista de adyacencia implementada con listas enlazadas**,
adecuada para un grafo disperso como este.

## Estructura del repositorio

```
redMetroPMI_aga/
├── data/
│   ├── estaciones.csv    # Nodos: estaciones de la red
│   ├── conexiones.csv    # Aristas: tramos entre estaciones
│   └── README.md         # Diccionario de datos
├── src/
│   └── metro_palma.py    # Programa principal
└── README.md
```

## Requisitos

- Python 3.8 o superior.
- No necesita librerías externas: solo utiliza la librería estándar de Python.

## Cómo ejecutarlo

Desde la carpeta principal del repositorio:

```
python src/metro_palma.py
```

El programa lee el dataset, construye el grafo, muestra la lista de adyacencia
y realiza comprobaciones automáticas.

## Resultado esperado

```
=== VERIFICACIONES ===
|V| = 17 estaciones
|E| = 16 tramos
Suma de grados = 32 (lema del apretón de manos: 2|E| = 32)
¿Conexo? True
¿Es un árbol (conexo y |E| = |V| - 1)? True
Estaciones terminales (grado 1): ['PE', 'PB', 'MA']
Estaciones de bifurcación (grado >= 3): ['SC']
```

## Dataset

Los datos de la red se encuentran en la carpeta [`data`](data/), donde un
[diccionario de datos](data/README.md) explica el contenido de cada fichero.
Las estaciones y conexiones proceden del mapa de la red (Schwandl, 2025);
los tiempos de trayecto son simulados.

## Uso de inteligencia artificial

En el desarrollo se ha utilizado Claude (Anthropic) y GitHub Copilot como apoyo.
El detalle de su uso se recoge en la declaración de uso de IA del informe técnico.

## Autora

Andrea Gutiérrez Arcas