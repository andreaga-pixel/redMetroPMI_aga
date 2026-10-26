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

(Pendiente)

## Formato

- Separador de columnas: coma (`,`)
- Separador de líneas dentro de una columna: barra vertical (`|`)
- Codificación: UTF-8
- La primera fila es la cabecera con los nombres de las columnas.