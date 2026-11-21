**ENTREGA INTERMEDIA 1**

**UNIT 18: DISCRETE MATH**

Profesor: Jose Alvarez

Alumna: Andrea Gutierrez Arcas

\[2026/2027\]

30/10/2026

# ÍNDICE

- [REPRESENTATION OF AN URBAN PUBLIC TRANSPORT NETWORK (ALIGNMENT PHASE)](#representación-de-una-red-de-transporte-público)
  - [URBAN PUBLIC TRANSPORT NETWORK](#red-de-transporte-público-urbano)
  - [INVENTARIO DE NODOS (estaciones)](#inventario-de-nodos-estaciones)
  - [INVENTARIO DE ARISTAS (tramo)](#inventario-de-aristas-tramo)
  - [LISTA DE ADYACIENCIA FRENTE A UNA MATRIZ DE ADYACIENCIA](#lista-de-adyacencia-frente-a-una-matriz-de-adyacencia)
    - [Ventajas y desventajas](#ventajas-y-desventajas)
    - [Conclusión](#conclusión)
  - [DATASET DE LA RED DE METRO](#dataset-de-la-red-de-metro)
    - [Estructura general](#estructura-general)
    - [Fichero de estaciones (estaciones.csv)](#fichero-de-estaciones-estacionescsv)
    - [Ficheros de conexiones (conexiones.csv)](#ficheros-de-conexiones-conexionescsv)
    - [Los tiempos simulados](#los-tiempos-simulados)
    - [Decisiones de diseño del dataset](#decisiones-de-diseño-del-dataset)
  - [DISEÑO DE LA LISTA ENLAZADA](#diseño-de-la-lista-enlazada)
    - [¿Qué es una lista enlazada?](#qué-es-una-lista-enlazada)
    - [¿Cómo se aplica a mi red?](#cómo-se-aplica-a-mi-red)
    - [Ejemplo con diagrama](#ejemplo-con-diagrama)
    - [¿Por qué cada tramo se guarda dos veces?](#por-qué-cada-tramo-se-guarda-dos-veces)
  - [IMPLEMENTACIÓN](#implementación)
    - [Construcción del entorno de trabajo](#construcción-del-entorno-de-trabajo)
    - [Creación de clases, funciones y el programa](#creación-de-clases-funciones-y-el-programa)
  - [EJECUCIÓN Y VERIFICACIÓN](#ejecución-y-verificación)
    - [¿Cómo se ejecuta?](#cómo-se-ejecuta)
    - [Resultado en Terminal y comprobaciones](#resultado-en-terminal-y-comprobaciones)
    - [La red es un árbol](#la-red-es-un-árbol)
    - [Errores encontrados y mi resolución](#errores-encontrados-y-mi-resolución)
  - [CONCLUSIÓN](#conclusión-1)
  - [BIBLIOGRAFÍA](#bibliografía)
  - [Declaración de IA](#declaración-de-ia)

# REPRESENTACIÓN DE UNA RED DE TRANSPORTE PÚBLICO

## RED DE TRANSPORTE PÚBLICO URBANO

He decidido utilizar el mapa del metro de Palma de Mallorca que tiene dos líneas la M1 y la M2.

Voy a modelar el metro como un grafo G = (V, E), donde:

- **V (vértices/nodos):** las estaciones.

- **E (aristas):** los tramos entre dos estaciones consecutivas.

- **No dirigido:** si puedes ir de A a B, puedes ir de B a A, el metro circula en ambos sentidos.

- **Ponderado:** cada arista lleva un tiempo en minutos.

Para mi trabajo voy a trabajar solo sobre las líneas de metro que son M1 y M2, la línea marrón que es el tren de Sóller y la continuación de M2 hacia Inca/Sa Pobla/Manacor son trenes, no metro, por lo tanto, los voy a dejar fuera del alcance por ahora.

**Las estaciones compartidas** son un solo nodo. Plaça d’Espanya, Jacint Verdaguer y Son Costa-Son Fortesa las usan tanto M1 como M2, pero físicamente son la misma estación, así que cuentan solo una vez. También estos tramos compartidos van a ser **una sola arista** con un atributo **M1\|M2.**

## INVENTARIO DE NODOS (estaciones)

Voy a asignar a cada estación un identificador corto.

| *Compartidas (M1\|M2)* |                       |
|------------------------|-----------------------|
| PE                     | Plaça d’Espanya       |
| JV                     | Jacint Verdaguer      |
| SC                     | Son Costa-Son Fortesa |

| *Solo M1* |                 |
|-----------|-----------------|
| SFV       | Son Fuster Vell |
| SCA       | Son Castelló    |
| GVA       | Gran Via Asima  |
| CR        | Camí del Reis   |
| SS        | Son Sardina     |
| UIB       | Universitat     |
| PB        | ParcBit         |

| *SOLO M2* |                       |
|-----------|-----------------------|
| SF        | Son Fuster            |
| SCL       | Son Cladera-Es Vivero |
| VL        | Verge de Lluc         |
| PI        | Pont d’Inca           |
| PIN       | Pont d’Inca Nou       |
| PM        | Polígono de Marratxi  |
| MA        | Marratxi              |

**Total:** 10 de M1 + 10 de M2 -3 compartidas = 17 nodos.

## INVENTARIO DE ARISTAS (tramo)

Une cada estación con la siguiente de su línea:

- **Tronco común**: PE-JV, JV-SC (dos aristas)

- **Rama M1:** SC-SFV-SCA-GVA-CR-SS-UIB-PB (7 aristas)

- **Rama M2:** SC-SF-SCL-VL-PI-PIN-PM-MA (7 aristas)

**Total**:16 aristas.

Este grafo sería un grafo disperso porque tiene muy pocas aristas en comparación con todas las que podría tener. Para calcular el máximo de aristas posibles es V\*(V-1) /2 donde V son los nodos y se divide entre 2 porque la arista A-B es la misma que B-A.

Para mi metro, con 17 estaciones:

17\*16/2 = 136 aristas posibles.

Eso sería un metro en el que desde cualquier estación pudieras ir directamente, sin paradas intermedias, a cualquier otra de las 16.

Mi metro tiene realmente 16 aristas como hemos podido ver antes. Ahora calculo la densidad para ver si es disperso o no. Con la densidad mido que proporción de las conexiones posibles existen:

Densidad = aristas reales/aristas posibles = 16/136 = 0,12

Es decir, solo existe el 12% de las conexiones posibles. El 88% restante no existe. Por eso es disperso.

## LISTA DE ADYACENCIA FRENTE A UNA MATRIZ DE ADYACENCIA

Si utilizara una matriz, esta reservaría una casilla para cada pareja posible de estaciones, tanto si están conectadas como si no. En mi caso**, la matriz sería una tabla de 17x17, es decir 289 casillas**. Cada una de estas casillas indica si existe un tramo entre dos estaciones: con un valor 1 si están conectadas y con 0 si no lo están. Como mi grafo es no dirigido, cada tramo aparece dos veces en la matriz.

**Por ejemplo***: el tramo PE-JV ocupa una casilla de la fila PE y columna JV, y también de la fila JV y columna PE.*

Por eso, **las 16 aristas de mi red ocupan 16 x 2 = 32 casillas con valor 1**. El **resto** de las casillas **serían 0** (**289-32 = 257**). Esto significa que el **89% de la matriz estaría ocupada por 0** que no nos aportan ningún tipo de información, solo nos indican conexiones que no existen.

**Por ejemplo:** *la fila de Plaça d’Espanya tendría 16 ceros y un único 1, porque solo conecta con Jacint Verdaguer.*

Esto es una consecuencia directa de que mi grafo sea disperso: como solo existe el 12% de las conexiones posibles, la mayor parte de la matriz quedaría vacía. En la siguiente imagen se muestra la matriz de adyacencia de mi red. Las casillas azules son las 32 que contienen 1 (los tramos que existen).

Comentarios de la matriz:

- **Es simétrica respecto a la diagonal:** cada 1 tiene su “pareja” al otro lado, porque A-B y B-A son el mismo tramo. Así se ve que cada tramo se cuenta dos veces.

- **La diagonal está toda a 0** (casillas grises): ninguna estación se conecta consigo misma.

- **La fila de PE tiene un solo 1** entre 17 casillas. Es el ejemplo que he explicado antes.

- **La fila de SC tiene tres 1 (**JV, SFV y SF**):** es la bifurcación donde se separan M1 y M2. El tramo SC-SF es el único que se aleja de la diagonal, porque conecta el tronco común con el inicio de la rama M2.

Este desperdicio de espacio me lleva a analizar la otra opción, la lista de adyacencia.

La lista de adyacencia solo almacena dos tipos de elementos: una cabeza por cada estación, que indica dónde empieza su lista de vecinas y un nodo por cada conexión que realmente existe. Como mi grafo es no dirigido, cada tramo también se guarda dos veces, una en cada estación.

**Por ejemplo:** el tramo PE-JV aparece en la lista de PE y en la lista de JV.

Por lo tanto, la lista ocupa: 17 cabezas + 32 nodos = 49 elementos. Frente a las 289 casillas de la matriz, la lista necesita aproximadamente seis veces menos espacio (289/49 ≈ 5,9) para guardar exactamente la misma información.

**Por ejemplo:** Plaça d’Espanya, que en la matriz necesitaba una fila completa de 17 casillas, en la lista solo necesita su cabeza y un nodo: PE -\> JV.

De manera general, la matriz ocupa un espacio proporcional a \|V\|² (número de estaciones al cuadrado), mientras que la lista ocupa un espacio proporcional a \|V\| + \|E\| (número de estaciones más el número de tramos). En mi grafo disperso \|E\| es mucho menor que \|V\|², por lo que la lista resulta más eficiente.

### Ventajas y desventajas

En la siguiente tabla resumo las ventajas y desventajas de cada representación aplicadas a mi red:

|  | **Matriz de adyacencia** | **Lista de Adyacencia** |
|---|---|---|
| **Ventajas** | • Comprobar si existe un tramo entre dos estaciones es inmediato: basta con mirar una casilla.<br>• Es fácil de entender y dibujar.<br>• Permite usar operaciones con matrices. | • Ocupa mucho menos espacio.<br>• Encontrar las vecinas de una estación es rápido, solo recorre sus vecinas (máximo 3 en mi red.)<br>• Añadir una estación nueva es sencillo.<br>• Cada nodo guarda todos los datos del tramo juntos. |
| **Desventajas** | • Ocupa mucho espacio.<br>• Para encontrar las vecinas de una estación hay que revisar toda su fila.<br>• Añadir una estación obliga a añadir una fila y una columna completas.<br>• Cada casilla solo guarda un valor, por lo que haría falta una matriz para los tiempos y otra para las líneas. | • Comprobar si existe un tramo concreto requiere recorrer la lista de vecinas de la estación.<br>• Es algo más complejo de implementar, porque se utilizan nodos y punteros. |

### Conclusión

Por todo lo anterior, **elijo la lista de adyacencia**, implementada mediante listas enlazadas como representación de la red de metro de Palma.

Mi grafo es disperso, por lo que una matriz desperdiciaría la mayor parte de su espacio: 257 de sus 289 casillas serían ceros. La lista, en cambio, solo guarda las 32 conexiones que existen realmente.

La única ventaja relevante que le he visto a la matriz es que me podría ayudar a comprobar de forma inmediata si existe un tramo, pero en mi red no compensa ya que cada estación tiene como máximo 3 vecinas.

## DATASET DE LA RED DE METRO

Una vez he definido el modelo matemático de la red y elegido la representación, el siguiente paso es crear el dataset.

Según Universidad Europea (2025), un dataset es un conjunto de datos “*almacenados en tablas y formatos concretos*”, ordenados de forma estratégica “*con el propósito de encontrar cualquier información de manera rápida*”. En mi caso, el dataset contiene toda la información de la red de metro de Palma; sus estaciones y los tramos que las conectan.

El dataset es necesario porque las tablas de inventario que he creado son útiles para una persona, pero un programa no puede interpretarlo directamente. Por eso la información de la red se guarda en ficheros con un formato estructurado, que el programa lee para construir un grafo, es el puente que necesito para pasar del modelo abstracto a su implementación.

Hay que aclarar que se trata de un dataset simulado. Las estaciones y las conexiones entre ellas son reales, pero los tiempos de trayecto entre estaciones son estimados, ya que no dispongo de los datos oficiales (apoyándome de IA para ver cuál es el mejor criterio para estimar).

### Estructura general

El dataset de mi red es estructurado, es decir, uno en el que “*los registros se almacenan en una columna y fila determinada de una tabla*” (Universidad Europea, 2025). Además, es un dataset de archivo, ya que toda la información se guarda en ficheros de extensión .**csv**, que guardan “*toda la información necesaria para trabajar*” (Universidad Europea, 2025).

El dataset está formado por dos ficheros, en el repositorio del proyecto en GitHub dentro de la carpeta data/:

- estaciones.csv: contiene los nodos (V) -\> las 17 estaciones de la red.

- conexiones.csv: contiene las aristas (E) -\> los 16 tramos que conectan las estaciones.

He elegido el formato CSV (Comma-Seoarated Values) porque es “*una forma ligera de almacenar e intercambiar datos estructurados*”, que se utiliza “*para representar filas y columnas en texto plano*” (DataSurise, 2024). En este formato, “*Cada línea representa una fila*” y “*los valores están separados por comas*” (DataSurise, 2024). Este formato me ofrece varias **ventajas**:

- Se puede leer con cualquier editor de texto y abrir con programas como Excel.

- Python puede leerlo directamente con su librería estándar.

- Al ser texto plano GitHub permite visualizarlo como una tabla y ver los cambios realizados en cada versión.

### Fichero de estaciones (estaciones.csv)

El fichero de estaciones contiene los nodos del grafo, es decir, las 17 estaciones de la red. Cada fila corresponde a una estación y tiene tres columnas.

| **Columna** | **Significado**                            |
|-------------|--------------------------------------------|
| id          | Identificador corto y único de la estación |
| nombre      | Nombre completo de la estación             |
| lineas      | Líneas que paran en la estación            |

Fichero estaciones.csv y el mismo fichero con la extensión edit CSV.

He **utilizado IDs cortos** por dos motivos:

- Cada **identificador es único**, por lo que permite distinguir cada estación sin ambigüedad.

- Son más **fáciles de manejar** que los nombres completos.

El programa utiliza los IDs internamente y los nombres completos para mostrar los resultados.

En la **columna líneas**, las estaciones compartidas por las dos líneas se indican con el valor M1\|M2 (no he utilizado coma “,”, porque en .csv se utilizan para separar columnas).

Las estaciones las he **ordenado** por línea, primero las tres estaciones compartidas (PE, JV y SC), después las estaciones exclusivas de M1 y, por último, las exclusivas de M2 (coincidiendo con el orden del inventario de nodos realizado anteriormente).

**Reglas de formato:**

| **Regla**              | **En el fichero**                      | **Motivo**                                          |
|------------------------|----------------------------------------|-----------------------------------------------------|
| Una fila por línea     | Cada línea es una estación             | Lee el fichero línea a línea                        |
| Cabeza                 | La primera línea es id, nombre, lineas | Indica el nombre de cada columna                    |
| Separador de columnas  | La coma (,)                            | El separador propio del formato csv                 |
| Mismo núm. de columnas | Todas las filas tienen 3 valores       | Si no, los datos quedarían descolocados             |
| Separador interno      | La barra vertical (\|) en M1\|M2       | La coma partiría la columna en dos                  |
| Sin espacios sobrantes | PE, Plaça d’Espanya                    | Evita que los valores se guarden con espacios       |
| Codificación UTF-8     | Configurada en el editor               | Permite leer correctamente caracteres como ç, í u ó |

Debido a que en el formato CSV no se permite poner comentarios porque lo lee como una línea de texto he creado dentro de la misma carpeta de data/ un fichero README.md, donde se encuentran las explicaciones del dataset.

### Ficheros de conexiones (conexiones.csv)

Este fichero contiene las aristas del grafo, es decir, los 16 tramos que conectan las estaciones. Cada fila corresponde a un tramo entre dos estaciones consecutivas y tiene cuatro columnas:

| **Columna** | **Significado**                                  |
|-------------|--------------------------------------------------|
| Origen      | Identificador de una de las estaciones del tramo |
| Destino     | Identificador de la otra estación del tramo      |
| Líneas      | Líneas o líneas que recorren el tramo            |
| Tiempo min  | Tiempo estimado del trayecto, en minutos         |

**Por ejemplo,** la fila SC, SF, M2, 2 indica que existe un tramo entre Son Costa- Son Fortesa y Son Fuster, que lo recorre la línea M2 y que le trayecto dura 2 minutos. El contenido completo del fichero es el siguiente:

Las **columnas origen y destino** no contienen nombres, sino los identificadores definidos en estanciones.csv. De esta forma, los dos ficheros quedan relacionados: cada conexión hace referencia a dos estaciones que deben existir en el fichero de estaciones.csv.

Aunque mi grafo es no dirigido, cada tramo aparece una sola vez en el fichero. No es necesario escribir el tramo PE-JV y también el tramo JV-PE, porque es el programa el que, al leer cada fila, guarda la conexión en los dos sentidos. Así se evita repetir información y se reduce el riesgo de errores, como escribir por equivocación un tiempo diferente para cada sentido de un mismo tramo. Por este motivo, el fichero tiene 16 filas, una por cada arista del grafo, mientras que la lista de adyacencia tendrá 32 nodos.

Los **tramos compartidos** por las dos líneas (PE-JV y JV-SC) se indican con el valor M1\|M2, siguiendo el mismo criterio que en el fichero de estaciones. Este fichero sigue también las mismas reglas de formato descritas en el apartado anterior.

Las filas están **ordenadas** siguiendo el recorrido de las líneas: primero los dos tramos conjuntos, después los 7 tramos de la rama M1 y por último los 7 tramos de la rama M2. Este orden coincide con el inventario de aristas realizado anteriormente.

### Los tiempos simulados

Los tiempos del trayecto de la columna tiempo_min son la única parte simulada del dataset, son estimaciones que he creado para poder trabajar con un grafo ponderado.

Para estimarlo, aunque al principio pensé en utilizar las distancias del mapa, luego me di cuenta de que las estaciones se sitúan para facilitar la lectura y no es su distancia real. En su lugar, he seguido un criterio basado en el tipo de zona en el que se encuentra cada tramo:

| Tipo de tramo                       | Tiempo estimado | Tramos                                               |
|-------------------------------------|-----------------|------------------------------------------------------|
| Estaciones muy próximas             | 1 minuto        | SCA-GVA                                              |
| Zona urbana                         | 2 minutos       | Tronco común, primeros tramos M1 y la mayoría de M2. |
| Zona periurbana                     | 3 minutos       | CR-SS, PIN-PM y PM-MA                                |
| Tramo hacia el campus universitario | 4 minutos       | SS-UIB                                               |

Mi razonamiento se basa en que, en la zona urbana, las estaciones se encuentran más cerca entre sí, mientras que a medida que las líneas se alejan del centro de Palma, las estaciones están más separadas y el trayecto entre ellas es más largo.

Con estos valores el recorrido de la línea M1 = 20 minutos y M2 = 20 minutos. Estos tiempos son el peso de cada arista del grafo, su función es permitir calcular el tiempo de los recorridos entre estaciones.

Como **limitación**, al ser valores estimados, los resultados que se obtengan con ellos serán aproximados. Sin embargo, gracias a que los datos están separados del código, si en un futuro tuviera acceso al tiempo real, bastaría con actualizar la columna tiempo_min del fichero conexiones.csv.

### Decisiones de diseño del dataset

Para terminar con el dataset, voy a resumir las principales decisiones de diseño que he tomado:

1.  **Separar los datos del código**. La información de la red no está escrita dentro del programa, sino en ficheros independientes que el programa lee al ejecutarse. Esto me permite modificar la red sin cambiar el código.

2.  **Separa nodos (estaciones) y aristas (conexiones) en dos ficheros.** El dataset está organizado en dos ficheros, uno para estaciones y otro para las conexiones, porque así sigue la misma estructura que le modelo matemático G = (V, E): estaciones.csv -\> conjunto de nodos V y conexiones.csv -\> conjunto de aristas E.

3.  **Comprobar la validez del dataset**. Antes de pasar a la implementación, he comprobado que el dataset es coherente con el modelo de la red:

    - Estaciones.csv tiene 17 filas, que coinciden con los 17 nodos.

    - Conexiones.csv tiene 16 filas que coinciden con las 16 aristas.

    - Todos los IDs de las columnas origen y destino existen en el fichero de estaciones.csv.

    - No hay estaciones ni tramos repetidos.

## DISEÑO DE LA LISTA ENLAZADA

Una vez definido el dataset, el siguiente paso es diseñar como se guardará la red dentro del programa. Para implementar la lista de adyacencia he utilizado listas enlazadas.

### ¿Qué es una lista enlazada?

Una **lista enlazada** es “*una estructura de datos clave para organizar y gestionar información*” (Selvaraj, 2026). Está formada por una cadena de nodos, y cada nodo tiene dos componentes principales: los datos, que son “*la información que almacena el nodo*” y un puntero, que es “*una referencia al siguiente nodo”* (Selvaraj, 2026).

La lista recorre desde la cabeza hasta la cola, siguiendo los punteros de un nodo al siguiente. El puntero del último nodo no apunta a ningún nodo, sino que suele tener el valor null, que en Python se representa con None.

Las listas enlazadas “*pueden crecer y reducirse dinámicamente sin necesidad de reasignaciones ni redimensionamientos”* (Selvaraj, 2026). Por eso son adecuadas para guardar las estaciones vecinas, ya que cada estación tiene un número distinto de ellas, y para añadir nuevas conexiones en el futuro.

### ¿Cómo se aplica a mi red?

En mi red, cada estación tiene su propia lista enlazada con sus estaciones vecinas. La estructura tiene dos partes:

- **Cabeza:** cada estación tiene una cabeza que apunta al primer nodo de su lista. Si una estación no tuviera vecinas, su cabeza apuntaría a None.

- **Nodos:** cada nodo representa un tramo que sale de la estación y guarda cuatro datos:

  - **Destino:** estación vecina.

  - **Líneas:** línea o líneas del tramo.

  - **Tiempo:** tiempo del tramo en minutos.

  - **Siguiente:** puntero al siguiente nodo de la lista.

Cuando el programa añade una conexión, inserta el nuevo nodo al principio de la lista de la estación. He elegido esta forma de inserción porque “*insertar y eliminar un nodo al principio es muy eficiente O(1)*”(Selvaraj, 2026), es decir, tiene un coste constante. No es necesario recorrer la lista hasta el final, sino que basta con que el nuevo nodo apunte al que antes era el primero y la cabeza pase a apuntar al nuevo nodo. Como consecuencia, las vecinas aparecen en orden inverso al de lectura del fichero, pero esto no afecta al grafo, ya que el orden de las vecinas no tiene ningún significado.

### Ejemplo con diagrama

En la siguiente figura se muestra la estructura de tres estaciones de mi red:

Lista enlazada de las estaciones PE, JV y SC

- PE (Plaça d’Espanya): es una estación terminal, su lista solo tiene un nodo que apunta a JV y después termina en None.

- JV (Jacint Verdaguer): es una estación intermedia, su lista tiene dos nodos, uno para cada estación que conecta, SC y PE.

- SC (Son Costa-SonFortesa): es la estación de bifurcación, su lista tiene tres nodos, uno hacia el tronco común (JV), otro hacia la rama M1 (SFV) y otro hacia la rama M2 (SF). Es la única estación de la red con tres vecinas.

En número de nodos de la lista de cada estación es su grado en el grafo.

### ¿Por qué cada tramo se guarda dos veces?

Como mi grafo es no dirigido, cada tramo debe poder recorrerse en los dos sentidos. Por eso, cuando el programa lee una fila del fichero conexiones.csv, crea dos nodos, uno en la lista de la estación de origen y otro en la de la estación de destino.

**Por ejemplo:** la fila PE, JV, M1\|M2, 2 -\> genera un nodo JV en la lista PE y un nodo PE en la lista JV, como se puede ver en el diagrama anterior.

Así, las 16 filas del fichero de conexiones generan 32 nodos (16x2) en la estructura, que, sumados a las 17 cabeza, dan los 49 elementos calculados al justificar la elección de lista de adyacencia.

## IMPLEMENTACIÓN

### Construcción del entorno de trabajo

Para la implementación he utilizado las siguientes herramientas:

- **Python**, he elegido este lenguaje de programación porque es un lenguaje sencillo y legible, muy utilizado en ciencia de datos y porque su librería estándar incluye el módulo csv, que permite leer el dataset sin necesidad de instalar herramientas adicionales.

- **Visual Studio Code** como IDE.

- **Git y GitHub**, donde el proyecto se encuentra en un repositorio de GitHub, lo que permite guardar un historial de cambios y compartir el código completo. EL repositorio esta disponible en :\[ <https://github.com/andreaga-pixel/redMetroPMI_aga.git> \]

El **repositorio esta organizado de la siguiente forma**:

```
redMetroPMI_aga/
├── data/
│   ├── estaciones.csv
│   ├── conexiones.csv
│   └── README.md
├── src/
│   └── Metro_palma.py
├── .gitignore
└── README.md
```

Esta organización separa los datos del código, siguiendo la decisión de diseño explicada anteriormente. Para que el programa encuentre los ficheros de datos independientemente de la carpeta desde la que se ejecute, la ruta a la carpeta data se calcula a partir de la ubicación del propio fichero del programa.

### Creación de clases, funciones y el programa

El programa se organiza en cuatro partes: la clase NodoArista, la clase GrafoMetro, la función cargar_grafo y el programa principal.

#### Clase NodoArista

Esta representa cada uno de los nodos de la lista enlazada, es decir, cada tramo que sale de una estación. Es la implementación directa de los nodos representados en el diagrama anterior.

La clase tiene un constructor (init), que se ejecuta automáticamente cada vez que se crea un nodo y guarda sus cuatro atributos:

- **Destino:** el identificador de la estación vecina.

- **Lineas**: la lista de líneas que recorren el tramo.

- **Tiempo**: el tiempo del tramo en minutos, que es el peso de la arista.

- **Siguiente:** el puntero al siguiente nodo de la lista. Se inicializa con el valor None porque, en el momento de crearse, el nodo todavía no está enlazad con ningún otro.

Cada vez que el programa lee un tramo del fichero conexionex.csv, crea dos objetos de esta clase, uno para cada sentido del tramo.

#### Clase GrafoMetro

Esta clase representa la red de metro completa. Es la implementación de la lista de adyacencia: guarda todas las estaciones y para cada una de ellas, la cabeza de su lista enlazada a las vecinas.

Su constructor crea tres diccionarios, en los que la clave es siempre el identificador de la estación:

- **Nombre:** guarda el nombre completo de cada estación.

- **Lineas:** guarda las líneas que paran en cada estación.

- **Cabeza:** guarda la cabeza de la lista enlazada de cada estación, es decir, su primer nodo.

Los métodos de la clase se pueden agrupar en dos grupos, los que construyen el grafo y los que permiten consultarlo.

##### Métodos de construcción

anadir_estacion: añade una estación al grafo, guardando su nombre y sus líneas, e inicializa su cabeza a None, ya que todavía no tiene vecinas. Antes de añadirla, comprueba que la estación no exista ya; si está duplicada, detiene el programa con un error.

\_insertar: crea un nodo nuevo (NodoArista) y lo inserta al principio de la lista enlazada de una estación. Para ello, el nuevo nodo pasa a apuntar al que antes era el primero y la cabeza pasa a apuntar al nuevo nodo, con un coste constante, O(1). Es un método interno, que solo utiliza la propia clase.

anadir_conexion: añade un tramo entre dos estaciones. Primero comprueba que las dos estaciones existan y después llama dos veces a \_insertar, una para cada sentido del tramo, ya que el grafo es no dirigido.

##### Métodos de consulta

vecinos: recorre la lista enlazada de una estación desde la cabeza, siguiendo los punteros de un nodo al siguiente hasta llegar a None, y devuelve sus nodos uno a uno.

grado: calcula el grado de una estación, contando los nodos de su lista enlazada.

num_nodos y num_aristas: num_nodos devuelve el numero de estaciones del grafo, que coincide con el número de cabezas. num_aristas calcula el número de tramo sumando los grados de todas las estaciones y dividiendo entre 2, ya que cada tramo está guardado dos veces. Se basa en el lema del apretón de manos, según el cual la suma de los grados de un grafo es igual al doble de su número de aristas.

es_conexo: comprueba si se puede llegar desde cualquier estación a cualquier otra. Para ello, utiliza un recorrido en anchura (BFS): parte de una estación, visita sus vecinas, después las vecinas de estas, y así sucesivamente. Si al final se han visitado todas las estaciones, el grafo es conexo.

mostrar: muestra por pantalla la lista de adyacencia completa. Para cada estación, escribe sus vecinas con su línea y su tiempo, unidas por flechas y terminando en None, de forma parecida al diagrama de diseño.

#### Función cargar_grafo

Esta función se encarga de leer el dataset y construir el grafo a partir de él. Es el punto en el que se unen el dataset y el código, siguiendo la decisión de diseño de separar los datos del programa.

La función crea un grafo vacío (g) y luego lee los dos ficheros CSV utilizando la clase DictReader del módulo csv. Esta clase utiliza la cabeza de cada fichero para que cada fila pueda consultarse por el nombre de sus columnas, por ejemplo, fila\[“nombre”\]. Los ficheros se abren con codificaciones UTF-8 para leer correctamente los caracteres especiales de los nombres de las estaciones.

En primer lugar, se cargan las estaciones, llamando a anadir_estacion por cada fila de estaciones.csv, y después las conexiones, llamando a anadir_conexion por cada fila de conexiones.csv. Este orden es necesario porque, al añadir una conexión, el programa comprueba que sus dos estaciones existan. Si las conexiones se cargan primero, ninguna estación existiría todavía y se produciría un error. Además, sigue el mismo orden que el modelo matemático: primero se definen los nodos (V) y después las aristas (E) que los unen.

Durante la lectura, los datos se transforman al tipo adecuado:

- El valor de la columna lineas (por ejemplo, M1\|M2) se separa por la barra vertical y se convierte en una lista de líneas (\[“M1”, “M2”\]).

- El valor de la columna tiempo_min se convierte de texto a número entero, ya que en un fichero CSV todos los valores se leen como texto. Esta conversión es necesaria para poder operar con los tiempos, por ejemplo, para sumarlos al calcular la duración de un recorrido.

Al terminar, la función devuelve el grafo completo, con 17 estaciones y 16 tramos.

#### Programa principal

Esta es la parte del código que se ejecuta al lanzar el programa. Se encuentra dentro del bloque id name == “main”, que hace que solo se ejecute cuando el fichero se lanza directamente, y no cuando otro programa lo importa.

El programa principal realiza tres tareas:

1.  **Carga el grafo** a partir de los ficheros del dataset, mediante la función cargar_grafo.

2.  **Muestra la lista de adyacencia completa**, mediante el método mostrar.

3.  Realiza una serie de **comprobaciones automáticas** para verificar que el grafo construido es correcto:

    - El número de estaciones (\|V\|) y de tramos (\|E\|), que deben coincidir con los inventarios.

    - La suma de los grados de todas las estaciones, que según el lema del apretón de manos debe ser igual al doble del número de aristas.

    - Si el grafo es conexo.

    - Si el grafo es un árbol, es decir, conexo y con \|E\| = \|V\| − 1.

    - Las estaciones terminales (de grado 1) y las de bifurcación (de grado 3 o más).

## EJECUCIÓN Y VERIFICACIÓN

### ¿Cómo se ejecuta?

El programa se ejecuta desde **Visual Studio Code**, abriendo el fichero metro_palma.py y pulsando el botón de ejecutar. Gracias a que la ruta de la carpeta de datos se calcula a partir de la ubicación del propio programa, este funciona correctamente independientemente de la carpeta desde la que se ejecute.

Al ejecutarse, el programa lee los ficheros del dataset, construye el grafo y muestra por pantalla la lista de adyacencia y los resultados de las comprobaciones.

### Resultado en Terminal y comprobaciones

La **primera parte** señalada con una caja amarilla es la lista de adyacencia de la red. Cada línea corresponde a una estación y muestra los nodos de su lista enlazada, con la estación vecina, la línea y el tiempo del tramo, terminando en None. Aquí también podemos observar que se confirma que el grafo es no dirigido. Porque, por ejemplo, el tramo PE-JV aparece en la lista PE (que apunta a JV) y en la de JV (que apunta a PE).

La **segunda parte** de la salida (caja verde) muestra los resultados de las comprobaciones automáticas, que se resumen en la siguiente tabla:

| Comprobación                          | Resultado esperado         | Resultado obtenido | Correcto |
|---------------------------------------|----------------------------|--------------------|----------|
| Número de estaciones \|V\|            | 17 (inventario de nodos)   | 17                 | SÍ       |
| Número de tramos \|E\|                | 16 (inventario de aristas) | 16                 | SÍ       |
| Suma de grados = 2\|E\|               | 32                         | 32                 | SÍ       |
| Grafo conexo                          | Sí                         | True               | SÍ       |
| Estaciones terminales (grado 1)       | PE, PB y MA                | PE, PB y MA        | SÍ       |
| Estaciones de bifurcación (grado ≥ 3) | SC                         | SC                 | SÍ       |

Todas las verificaciones coinciden con los resultados esperados, lo que confirma que el dataset se ha cargado correctamente y que el grafo representa fielmente la red de metro:

- El número de estaciones y tramos coincide con los inventarios realizados a partir del mapa.

- La suma de los grados es 32, el doble del número de aristas, lo que confirma que cada tramo se ha guardado exactamente dos veces, una en cada sentido.

- El grafo es conexo, es decir, desde cualquier estación se puede llegar a cualquier otra de la red.

- Las estaciones terminales son Plaça d’Espanya, ParBit y Marratxí, que son los extremos de las líneas en el mapa y la única estación de bifurcación es Son Costa- Son Fortesa (donde se separan M1 y M2).

### La red es un árbol

Un árbol es un “*grafo conexo acíclico”,* en el que “*dos vértices cualesquiera están conectados exactamente por un camino"* (UCS, 2026). Un grafo conexo con n vértices y n-1 aristas es un árbol. Mi red cumple esta condición: es conexa y tiene 17 nodos y 16 aristas.

Esto tiene tres consecuencias para la red:

1.  **No hay rutas alternativas**: para ir de Marratxi a ParcBit, por ejemplo, es obligatorio pasar por Son Costa – Son Fortesa.

2.  **Cada tramo es imprescindible:** si se corta cualquiera, la red queda dividida. Si se corta SC-SF, las 7 estaciones de la rama M2 quedarían aisladas, por ejemplo.

3.  **Son Costa – Son Fortesa es un punto crítico:** si quedara fuera de servicio, la red se dividiría en tres partes.

Con esto en mente se puede ver que la red es poco robusta ante incidencias.

### Errores encontrados y mi resolución

Durante el desarrollo se produjeron los siguientes errores:

**Error 1: AttributeError**

Se produce cuando falla la referencia a un atributo (Python Software Foundation, s.f.). El diccionario de nombres tenía un nombre distinto en el constructor (nombre) y en un método (nombres). Lo corregí eligiendo la variable nombre en singular.

**Error 2: TypeError**

Se produce cuando hice una operación a un objeto de tipo inadecuado (Python Software Foundation, s.f.), en num_aristas coloqué un paréntesis mal después de la división y debía ser antes y luego dividir.

**Error 2: ValueError en la prueba**

Se produce cuando una función recibe un valor inadecuado (Python Software Foundation, s.f.). Este error lo hice apropósito para comprobar que la validación de anadir_conexion funciona, si el dataset tuviera un id mal escrito, el programa lo detectaría.

## CONCLUSIÓN

En esta primera parte del proyecto he representado la red del metro de Palma como un grafo, siguiendo un proceso en cuatro fases:

| Fase | Resultado |
|---|---|
| Idea abstracta | Decisión de modelo matemático: G = (V, E) no dirigido y ponderado, con 17 estaciones y 16 tramos.<br>Matriz Vs Lista de Adyacencia |
| Diseño | He creado un repositorio con el Dataset en dos ficheros CSV y he implementado la lista adyacencia con listas enlazadas. |
| Implementación | Programa en Python en la carpeta del repositorio src (metro_palma.py) que lee el dataset y construye el grafo. |
| Ejecución | Grafo verificado automáticamente, con todas las comprobaciones correctas. |

## BIBLIOGRAFÍA

Anthropic (2026) Claude (Opus 5.5) \[Modelo de lenguaje de gran tamaño\]. Disponible en: <https://claude.ai> (Consultado: 27 octubre 2026).

DataSunrise (2024) ¿Qué es un archivo CSV? El valor duradero de los archivos CSV. Disponible en: <https://www.datasunrise.com/es/centro-de-conocimiento/que-es-un-archivo-csv/> (Consultado: 26 octubre 2026).

GitHub (2026) GitHub Copilot \[Herramienta de IA\]. Disponible en: <https://github.com/features/copilot> (Consultado: 27 octubre 2026).

Python Software Foundation (s.f.) Built-in Exceptions. Disponible en: <https://docs.python.org/3/library/exceptions.html> (Consultado: 27 octubre 2026).

Schwandl, R. (2025) Palma de Mallorca \[Mapa\]. UrbanRail.Net. Disponible en: <https://urbanrail.net/eu/es/palma/palma.htm> (Consultado: 27 octubre 2026).

Selvaraj, N. (2026) Listas enlazadas en Python: tutorial con ejemplos. DataCamp. Disponible en: <https://www.datacamp.com/es/tutorial/python-linked-lists> (Consultado: 27 octubre 2026).

UCS (2026) Discrete Mathematics. Módulo IV: Teoría de Grafos \[Apuntes de clase\]. UCS.

Universidad Europea (2025) Datasets: qué es, tipos y dónde encontrarlos. Disponible en: <https://universidadeuropea.com/blog/datasets-que-es/> (Consultado: 26 octubre 2026).

## Declaración de IA

En la elaboración de esta parte del proyecto he utilizado herramientas de inteligencia artificial generativa:

**Claude (Anthopic, 2026)** lo he utilizado para tres cosas en concreto:

1.  **Organización:** para organizar el trabajo que se me pedía realizar y dividirlo en pasos y tiempos estimados de realización.

2.  **Tutor:** para terminar de entender conceptos como la densidad de un grafo. Cuando había un concepto que no terminaba de entender le he pedido que me lo explique de forma sencilla con ejemplos que se puedan aplicar a la vida cuotidiana. También le pedí que me hiciera la imagen del diagrama, pero a partir de un esquema que yo le proporcioné y también la matriz, pero el razonamiento ha sido mío basándome en los apuntes de las sesiones.

3.  **Razonamiento de tiempo estimado:** me ha ayudado a encontrar una lógica detrás de inventarme los números ya que si me los invento de manera aleatoria no tiene tanto peso.

4.  **Aclaraciones de código:** he realizado el programa en VS Code apoyándome de GutHub Copilot pero a veces aún así había cosas que me costaba entender, así que le pedía que me explicara línea a línea que es lo que esta haciendo y como funciona la lógica para entenderlo completamente antes de seguir. Y esto me ha ayudado a poner comentarios explicativos con mis propias palabras.

**GitHub Copilot** me ha dado sugerencias de autocompletado en el código y correcciones durante la escritura en Visual Studio Code.

Aclaración importante: he utilizado estas herramientas como apoyo al aprendizaje y no como sustituto de mi trabajo:

- He escrito el código por mí mismo, bloque a bloque, comprobando cada parte con pruebas antes de continuar.

- He identificado y corregido los errores surgidos durante el desarrollo.

- He tomado decisiones propias sobre el código, como la utilización de bucles y la organización del repositorio.

- He contrastado los conceptos y definiciones con las fuentes citadas en la bibliografía.

Entiendo la lógica de cada parte del programa y soy capaz de explicarla gracias a que me he apoyado en estas herramientas.
