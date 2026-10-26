# Dataset del metro de Palma

Dataset simulado de la red de metro de Palma (líneas M1 y M2),
modelada como un grafo G = (V, E) no dirigido y ponderado.

## estaciones.csv (nodos, V)

Cada fila es una estación. 17 estaciones en total.

| Columna | Descripción | Ejemplo |
|---|---|---|
| id | Identificador corto y único de la estación | SC |
| nombre | Nombre completo de la estación | Son Costa - Son Fortesa |
| lineas | Líneas que paran en la estación, separadas por "\|" | M1\|M2 |

- Las estaciones compartidas por M1 y M2 (PE, JV, SC) aparecen una sola vez.
- Orden: primero las compartidas, después las de M1 y por último las de M2.

## conexiones.csv (aristas, E)

Cada fila es un tramo entre dos estaciones consecutivas. 16 tramos en total.

| Columna | Descripción | Ejemplo |
|---|---|---|
| origen | id de una de las estaciones del tramo | SC |
| destino | id de la otra estación del tramo | SF |
| lineas | Líneas que recorren el tramo, separadas por "\|" | M2 |
| tiempo_min | Tiempo estimado del trayecto en minutos (simulado) | 2 |

- Cada tramo aparece una sola vez. Como el grafo es no dirigido,
  el programa lo guarda en los dos sentidos (origen → destino y destino → origen).
- Los ids de origen y destino deben existir en estaciones.csv.
- Orden: tronco común (PE-JV-SC), rama M1 (SC → PB) y rama M2 (SC → MA).
- Los tiempos son simulados (entre 1 y 4 minutos) y no son datos oficiales.

## Formato

- Separador de columnas: coma (`,`)
- Separador de líneas dentro de una columna: barra vertical (`|`)
- Codificación: UTF-8
- La primera fila es la cabecera con los nombres de las columnas.