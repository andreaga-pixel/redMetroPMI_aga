**ENTREGA INTERMEDIA 2**

**UNIT 18: DISCRETE MATH**

**PARTE 3**

Profesor: Jose Alvarez

Alumna: Andrea Gutierrez Arcas

\[2026/2027\]

22/11/2026

# ÍNDICE

- [DEFINICIÓN DE LAS VARIABLES BOOLEANAS](#definición-de-las-variables-booleanas)
  - [La variable principal](#la-variable-principal)
  - [Variables auxiliares](#variables-auxiliares)
- [CONDICIONES LÓGICAS DE LA RED: ECUACIONES, TABLAS DE VERDAD Y SIMPLIFICACIÓN](#condiciones-lógicas-de-la-red-ecuaciones-tablas-de-verdad-y-simplificación)
  - [CONDICIÓN C1: LA SIMETRÍA](#condición-c1-la-simetría)
    - [TABLA DE VERDAD C1](#tabla-de-verdad-c1)
    - [DE TABLA A ECUACIÓN C1](#de-tabla-a-ecuación-c1)
    - [CORRECCIÓN DE LA ECUACIÓN C1](#corrección-de-la-ecuación-c1)
    - [CIRCUITO C1](#circuito-c1)
  - [CONDICIÓN C2: SIN LAZOS](#condición-c2-sin-lazos)
    - [TABLA DE VERDAD C2](#tabla-de-verdad-c2)
    - [DE TABLA A ECUACIÓN C2](#de-tabla-a-ecuación-c2)
    - [CIRCUITO C2](#circuito-c2)
  - [CONDICIÓN C3: SERVICIO](#condición-c3-servicio)
    - [TABLA DE VERDAD C3](#tabla-de-verdad-c3)
    - [DE TABLA A ECUACIÓN C3](#de-tabla-a-ecuación-c3)
    - [SIMPLIFICACIÓN ALGEBRAICA C3](#simplificación-algebraica-c3)
    - [CIRCUITO C3](#circuito-c3)
  - [CONDICIÓN C4: CONECTIVIDAD](#condición-c4-conectividad)
    - [TABLA DE VERDAD C4](#tabla-de-verdad-c4)
    - [DE TABLA A ECUACIÓN C4 (Viaje JV -\> SF)](#de-tabla-a-ecuación-c4-viaje-jv---sf)
    - [CIRCUITO C4](#circuito-c4)
  - [SISTEMA DE VERIFICACIÓN DE LA RED](#sistema-de-verificación-de-la-red)
- [COMPROBACIÓN CON PYTHON](#comprobación-con-python)
  - [Comprobación de la condición C1: Simetría](#comprobación-de-la-condición-c1-simetría)
  - [Comprobación de la condición C2: Sin lazos](#comprobación-de-la-condición-c2-sin-lazos)
  - [Comprobación de la condición C3: Servicio](#comprobación-de-la-condición-c3-servicio)
  - [Comprobación de la condición C4: Conectividad](#comprobación-de-la-condición-c4-conectividad)
  - [Sistema de verificación de la red completa](#sistema-de-verificación-de-la-red-completa)
- [ESTRUCTURA ALGEBRAICA DE LA RED](#estructura-algebraica-de-la-red)
- [CÓMO AFECTAN LAS ECUACIONES BOOLEANAS SOBRE LA RED](#cómo-afectan-las-ecuaciones-booleanas-sobre-la-red)
  - [Lo que garantiza cada ecuación](#lo-que-garantiza-cada-ecuación)
  - [La forma de la ecuación revela la fragilidad de la red.](#la-forma-de-la-ecuación-revela-la-fragilidad-de-la-red)
  - [Las ecuaciones me señalan donde mejorar](#las-ecuaciones-me-señalan-donde-mejorar)
- [CONCLUSIÓN](#conclusión)
- [BIBLIOGRAFÍA](#bibliografía)
  - [Declaración de IA](#declaración-de-ia)

# DEFINICIÓN DE LAS VARIABLES BOOLEANAS

## La variable principal

**¿Por qué hacen falta las variables?**En álgebra de Boole las variables solo valen 1 (True) o 0 (False) (UCS, 2026). Para aplicarlo a mi red antes tengo que convertirla en preguntas de si o no.

Mi variable principal va a ser **x_ab** y no ab porque en Boole, dos letras juntas significan la operación AND. Por lo tanto, voy a definir mi variable de la siguiente manera:

**x_ab = 1** si hay **tramo directo** de a -\> b

**x_ab = 0** si **no hay tramo directo** de a -\> b

Por ejemplo:

| Variable | Valor | Por qué                                 |
|----------|-------|-----------------------------------------|
| X_PE,JV  | 1     | PE y JV son consecutivas                |
| X_PE,SC  | 0     | Para ir de PE a SC hay que pasar por JV |
| X_PE,PE  | 0     | Una estación no conecta consigo misma   |

\*Los valores los calculo mirando mi conexiones.csv

En conjunto tengo un total de **289 variables** (17x17), que forman una matriz booleana. Es la misma matriz de adyacencia que planteé anteriormente, pero interpretada como valores lógicos. Esta matriz se genera a partir de la lista enlazada.

Cuento 289 y no la mitad porque **x_ab** y **x_ba** son variables distintas, no es lo mismo poder ir de **a** a **b** que de **b** a **a** (por ejemplo, en una calle de sentido único). En mi metro coinciden porque los trenes circulan en los dos sentidos.

Por ejemplo: **x_SC,SF =x_SF,SC = 1**.

Pero esto es una propiedad de mi red, no algo que se cumpla siempre. En mi código guardo cada tramo en los dos sentidos. Por eso voy a tratarlos como dos variables separadas para comprobar que x_ab y x_ba coinciden.

## Variables auxiliares

Con la variable x-ab estoy hablando de tramos, pero también nos interesa saber que líneas de metro, la M1 o la M2, para en cada estación. Por eso he añadido dos variables más:

| Variable  | Significado                                 | De donde sale                                                                    |
|-----------|---------------------------------------------|----------------------------------------------------------------------------------|
| m1_a/m2_a | 1 si la línea M1 o M2 para en la estación a | Columna de líneas de estaciones.csv                                              |
| o_a       | 1 si la estación a está operativa           | En un supuesto que me inventore para analizar escenarios. No está en mi dataset. |

Por ejemplo: **SC** tiene **m1=1** y **m2=2** porque es compartida; **PI** tiene **m1=0** y **m2=1**.

Con la variable **o_a** voy a estudiar que pasa si se cierra una estación. En el análisis de la red vi que **SC** es un punto crítico y con esta variable podré evaluarlo mejor.

# CONDICIONES LÓGICAS DE LA RED: ECUACIONES, TABLAS DE VERDAD Y SIMPLIFICACIÓN

Voy a definir 4 condiciones en la siguiente tabla y luego voy a profundizar una a una.

| Condición        | Explicación                                                        |
|------------------|--------------------------------------------------------------------|
| C1: Simetría     | Si hay un tramo de **a** a **b**, también los hay de **b** a **a** |
| C2: Sin lazos    | Ninguna estación tiene un tramo consigo misma                      |
| C3: Servicio     | Por cada estación para al menos una línea                          |
| C4: Conectividad | Qué pasa si se cierra **SC**, el punto crítico.                    |

Una vez formuladas las condiciones voy a realizar las tablas de verdad de cada una de ellas, seguido de el paso inverso de tablas a ecuación y para comprobar que la tabla de verdad corresponde a su ecuación, para ello hago el camino inverso: obtengo la ecuación a partir de la tabla.

- Busco las filas en las que el resultado vale 1.

- Para cada una de esas filas escribo un AND de las variables: la variable tal cual si vale 1 y con NOT si vale 0.

- Si hay varias filas con resultado 1, uno sus términos con OR.

Por último, si encuentro una ecuación que no coincide, voy a hacer simplificaciones para comprobar que es la misma ecuación.

## CONDICIÓN C1: LA SIMETRÍA

Como mis tramos son de ambos sentidos la condición para que se cumpla la simetría tiene que ser “*si A, entonces B*”, es decir; si **x_ab = 1**, entonces **x_ba =1**.

Como con **AND**, **OR** y **NOT** no hay una operación “*entonces*”, hay que pensar cuándo se incumple la condición.

| x_ab | x_ba | ¿Se cumple “si hay de a a b, hay de b a a”?                   |
|------|------|---------------------------------------------------------------|
| 0    | 0    | Sí: no hay tramo en ningún sentido, no hay nada que incumplir |
| 0    | 1    | Sí: la condición solo dice algo cuando x_ab = 1               |
| 1    | 1    | Sí: hay tramo en los dos sentidos                             |
| 1    | 0    | NO: hay tramo de a a b pero no de b a a                       |

Solo hay un caso malo, cuando **x_ab = 1** y **x-ba =0**, Eso si se puede escribir con **AND** y **NOT**:

**F_ab = x_ab · ¬x_ba**

**F_ab** es la variable que me va a ayudar a detectar el fallo:

- **F_ab = 1** entonces hay un tramo de sentido único entre a y b y la condición falla.

- **F_ab = 0** entonces es que la condición se cumple.

Ejemplo con mis tramos:

**x_SC,SF = 1 x_PE,SC = 0**

**x_SF,SC= 1 x_SC,PE= 0**

**F_SC,FB = 1·¬1=0** -\> la condición se cumple. **F_PE,SC = 0·¬0=0** -\> se cumple.

Utilizo **AND** porque tienen que cumplirse dos cosas a la vez:

1.  Que haya tramo de **a** a **b**.

2.  Que no lo haya de **b** a **a**.

Si solo se da una condición, no hay fallo.

### TABLA DE VERDAD C1

Ecuación: **F_ab = x_ab · ¬x_ba**

Columnas:

1.  **x_ab** y **x_ba**: son las entradas, con sus 4 combinaciones posibles.

2.  **· ¬x_ba**: columna intermedia, el **NOT** de **x_ba**.

3.  **F_Ab**: el resultado, el **AND** de la columna 1 con la columna 2.

| x_ab | x_ba | ¬x_ba | F_ab = x_ab · ¬x_ba | Significado                    |
|------|------|-------|---------------------|--------------------------------|
| 0    | 0    | 1     | 0                   | No hay tramo en ningún sentido |
| 0    | 1    | 0     | 0                   | Solo de b a a                  |
| 1    | 0    | 1     | 1                   | Solo de a a b (sentido único)  |
| 1    | 1    | 0     | 0                   | Tramo en los dos sentidos      |

### DE TABLA A ECUACIÓN C1

En la tabla solo hay un 1. Como **x_ab** vale 1 se escribe tal cual, y como **x_ba** vale 0 se escribe negada.

**F_ab = x_ab · ¬x_ba**

Coincide con la ecuación planteada.

### CORRECCIÓN DE LA ECUACIÓN C1

Mi ecuación **da 1 cuando todo va mal** y en el brief del AB se me pide una ecuación que **de 1 cuando todo va bien**. Para darle la vuelta a mi detector de fallos debo ponerle un **NOT** delante, la ecuación quedaría así:

**¬F_ab = ¬(x_ab · ¬x_ba)**

Esta ecuación ya es correcta, pero es incómoda porque con el **NOT** delante que devuelve todo en un paréntesis hace que no se entienda bien lo que dice. Con el **teorema De Morgan** (¬(A · B) = ¬A + ¬B**)** puedo quitar ese **NOT**. Lo que va a hacer el meter el **NOT** dentro del paréntesis, Con eso, la ecuación queda sin paréntesis y se puede leer directamente en palabras.

| Paso | Expresión                    | Justificación                                          |
|------|------------------------------|--------------------------------------------------------|
| 0    | **¬F_ab = ¬(x_ab · ¬x_ba)**  | Negación del detector de fallo                         |
| 1    | **¬F_ab = ¬x_ab + ¬(¬x_ba)** | Primer teorema de De Morgan                            |
| 2    | **¬F_ab = ¬x_ab + x_ba**     | Doble negación: negar dos veces deja la variable igual |

Hago una comprobación con la tabla de verdad. Compruebo que las dos expresiones dan el mismo resultado en todas las combinaciones.

| x_ab | x_ba | F_ab | ¬F_ab | ¬x_ab | ¬x_ab + x_ba |
|------|------|------|-------|-------|--------------|
| 0    | 0    | 0    | 1     | 1     | 1            |
| 0    | 1    | 0    | 1     | 1     | 1            |
| 1    | 0    | 1    | 0     | 0     | 0            |
| 1    | 1    | 0    | 1     | 0     | 1            |

Las columans **¬F_ab** y **¬x_ab** + **x_ba** son iguales, así que la simplificación es correcta. Y la ecuación final es:

**¬x_ab + x_ba**

Que se lee “***o no hay tramo de a a b, o sí lo ha de b a a***”

### CIRCUITO C1

#### Circuito antes de la Ley De Morgan

Voy a utilizar esta página web que he encontrado de Logisim (<https://logisim.app/>) para crear el circuito.

1.  Creo las entradas que son **x_ab** y **x_ba**. Cada entrada es un interruptor que valdrá 0 o 1.

2.  Coloco una puerta **NOT Gate** a la derecha de **x_ba** porque la ecuación pide **¬x_ba**, así que **x_ba** tiene que pasar por un **NOT** antes del **AND**.

3.  Coloco un **AND Gate** a la derecha de ambas entradas. Cambio el *Number of Imputs* a 2. Esto lo hago porque la ecuación es **x_ab** · **¬x_ba**, y el **·** es un **AND.**

4.  Coloco la Salida (**F_ab**). Se coloca a la derecha de AND, es el resultado de la ecuación y mostrara 1 cuando haya fallo.

5.  Conecto los cables.

**Comprobaciones**

| x_ab | x_ba | F_ab esperado |
|------|------|---------------|
| 0    | 0    | 0             |

| x_ab | x_ba | F_ab esperado |
|------|------|---------------|
| 0    | 1    | 0             |

| x_ab | x_ba | F_ab esperado |
|------|------|---------------|
| 1    | 0    | 1             |

| x_ab | x_ba | F_ab esperado |
|------|------|---------------|
| 1    | 1    | 0             |

#### Después de aplicar Ley De Morgan

La ecuación: **¬F_ab = ¬x_ab + x_ba**

En este circuito la entrada **x_ab** es la que tiene el **NOT Gate** y ambas entradas están conectadas a un **OR Gate**.

| x_ab | x_ba | ¬F_ab |
|------|------|-------|
| 0    | 0    | 1     |

| x_ab | x_ba | ¬F_ab |
|------|------|-------|
| 0    | 1    | 1     |

| x_ab | x_ba | ¬F_ab |
|------|------|-------|
| 1    | 0    | 0     |

| x_ab | x_ba | ¬F_ab |
|------|------|-------|
| 1    | 1    | 1     |

#### Comparativa de los dos circuitos de C1

| Circuito               | Ecuación             | Puertas       | La salida vale 1 cuando…      |
|------------------------|----------------------|---------------|-------------------------------|
| 1\. Detector de fallo  | F_ab = x_ab · ¬x_ba  | 1 NOT + 1 AND | hay un tramo de sentido único |
| 2\. Condición cumplida | ¬F_ab = ¬x_ab + x_ba | 1 NOT + 1 OR  | la simetría se cumple         |

He probado las cuatro combinaciones de entrada en los dos circuitos y los resultados coinciden con la tabla de verdad. Además, con las mismas entradas las salidas son siempre opuestas, lo que confirma de forma visual que uno sea la negación del otro.

| x_ab | x_ba | F_ab (circuito 1) | ¬F_ab (circuito 2) |
|------|------|-------------------|--------------------|
| 0    | 0    | 0                 | 1                  |
| 0    | 1    | 0                 | 1                  |
| 1    | 0    | 1                 | 0                  |
| 1    | 1    | 0                 | 1                  |

## CONDICIÓN C2: SIN LAZOS

Un lazo es un tramo que sale de una estación y vuelve a la misma. Para comprobar que no hay un tramo por ejemplo **PE** a **PE** basta con mirar una variable **x_aa** y el detector de fallo es:

**L_a = x_aa**

Donde:

- **L_a=1** cuando la estación tiene un lazo, y la condición falla.

- **L_a=0** cuando la condición se cumple.

Para saber si alguna estación tiene lazo utilizo la operación **OR (+),** que da 1 en cuando al menos uno de los valores es 1:

**L = x_PE,PE + x_JV,JV + x_SC,SC + x_SFV,SFV + x_SCA,SCA + x_GVA,GVA + x_CR,CR + x_SS,SS + x_UIB,UIB + x_PB,PB + x_SF,SF + x_SCL,SCL + x_VL,VL + x_PI,PI + x_PIN,PIN + x_PM,PM + x_MA,MA**

Donde:

- **L=0** cuando ninguna estación tiene lazo y la red cumple C2.

- **L=1** cuando al menos una estación tiene lazo.

Estas **17** variables son la diagonal de la matriz de adyacencia. El resultado de L para mi red sería el siguiente:

**L = 0 + 0 + 0 + 0 + 0 + 0 + 0 + 0 + 0 + 0 + 0 + 0 + 0 + 0 + 0 + 0 + 0 = 0** -\> cumple C2.

Utilizo **OR** porque la red falla si cualquier estación tiene lazo, basta que se cumpla esta condición.

### TABLA DE VERDAD C2

**L-a = x_aa**, tiene solo una variable, así que salen 2 filas.

| x_aa | L_a | Significado                             |
|------|-----|-----------------------------------------|
| 0    | 0   | La estación no tiene lazo -\> se cumple |
| 1    | 1   | Tiene lazo -\> fallo                    |

### DE TABLA A ECUACIÓN C2

En la tabla solo hay un 1, en la fila **x_aa = 1**:

**L_a =x_aa**

Coincide con la ecuación planteada.

### CIRCUITO C2

Para poder representar mi red entera me harían falta 17 entradas y 16 puertas OR. Para la explicación voy a crear un circuito con 3 estaciones y luego voy a dejar representada mi red entera.

La ecuación reducida: **L = x_PE,PE + x_JV,JV + x_SC,SC**

1.  **Creo tres entradas** con label **x_PE,PE**, **x_JV,JV** y **x_SC,SC.**

2.  Una sola puerta **OR** con *Number of Inputs* = 3.

3.  Una salida con Label L.

4.  Conectar los cables.

Si dejo las tres entradas a 0, L=0, lo que significa que el recorrido no tiene ningún lazo. Pero si enciendo una cualquiera, la L=1. Esto demuestra que basta con que una estación tenga lazo para que la red falle.

**Circuito de mi red real**

La ecuación: **L = x_PE,PE + x_JV,JV + x_SC,SC + x_SFV,SFV + x_SCA,SCA + x_GVA,GVA + x_CR,CR + x_SS,SS + x_UIB,UIB + x_PB,PB + x_SF,SF + x_SCL,SCL + x_VL,VL + x_PI,PI + x_PIN,PIN + x_PM,PM + x_MA,MA**

Para la versión del circuito real podemos observar exactamente lo mismo que en el de la versión reducida. En mi primera captura podemos ver todas las entradas a 0 y L=0 por lo tanto la red cumple C2. En la segunda captura podemos ver que una entrada es 1 por lo que L=1 porque el circuito detecta el alzo.

## CONDICIÓN C3: SERVICIO

Por cada estación pasa al menos una línea, **M1** o **M2**. Una estación sin ninguna línea no tendría sentido en el metro. Como se dice “*al menos una*”, uso **OR**:

**S_a = m1_a + m2_a**

Donde:

- **S_a = 1** entonces por la estación pasa al menos una línea y la condición se cumple.

- **S_a = 0** entonces no pasa ninguna línea y la condición falla.

### TABLA DE VERDAD C3

**S_a = m1_a + m2_a**. Aquí tenemos dos variables así que salen 4 filas.

| m1_a | m2_a | S_a = m1_a + m2_a | Ejemplo real                      |
|------|------|-------------------|-----------------------------------|
| 0    | 0    | 0                 | Ninguna estación (sería un fallo) |
| 0    | 1    | 1                 | PI (solo M2)                      |
| 1    | 0    | 1                 | UIB (solo M1)                     |
| 1    | 1    | 1                 | SC (compartida)                   |

Mi red cumplirá esta condición si todas las estaciones tienen **S_a = 1**, por lo tanto, se utiliza **AND** para verificarlo.

**S = S_PE · S_JV · S_SC · S_SFV · S_SCA · S_GVA · S_CR · S_SS · S_UIB · S_PB · S_SF · S_SCL · S_VL · S_PI · S_PIN · S_PM · S_MA**

**S = 1 · 1 · 1 · 1 · 1 · 1 · 1 · 1 · 1 · 1 · 1 · 1 · 1 · 1 · 1 · 1 · 1 = 1** -\> cumple C3.

| Estación | Líneas | m1_a | m2_a | S_a = m1_a + m2_a |
|----------|--------|------|------|-------------------|
| PE       | M1\|M2 | 1    | 1    | 1 + 1 = 1         |
| JV       | M1\|M2 | 1    | 1    | 1 + 1 = 1         |
| SC       | M1\|M2 | 1    | 1    | 1 + 1 = 1         |
| SFV      | M1     | 1    | 0    | 1 + 0 = 1         |
| SCA      | M1     | 1    | 0    | 1 + 0 = 1         |
| GVA      | M1     | 1    | 0    | 1 + 0 = 1         |
| CR       | M1     | 1    | 0    | 1 + 0 = 1         |
| SS       | M1     | 1    | 0    | 1 + 0 = 1         |
| UIB      | M1     | 1    | 0    | 1 + 0 = 1         |
| PB       | M1     | 1    | 0    | 1 + 0 = 1         |
| SF       | M2     | 0    | 1    | 0 + 1 = 1         |
| SCL      | M2     | 0    | 1    | 0 + 1 = 1         |
| VL       | M2     | 0    | 1    | 0 + 1 = 1         |
| PI       | M2     | 0    | 1    | 0 + 1 = 1         |
| PIN      | M2     | 0    | 1    | 0 + 1 = 1         |
| PM       | M2     | 0    | 1    | 0 + 1 = 1         |
| MA       | M2     | 0    | 1    | 0 + 1 = 1         |

### DE TABLA A ECUACIÓN C3

En la tabla hay tres filas con resultado 1, así que salen tres términos unidos con **OR**:

| Fila con S_a = 1 | m1_a | m2_a | Término      |
|------------------|------|------|--------------|
| Solo M2          | 0    | 1    | ¬m1_a · m2_a |
| Solo M1          | 1    | 0    | m1_a · ¬m2_a |
| Compartida       | 1    | 1    | m1_a · m2_a  |

**S_a = ¬m1_a · m2_a + m1_a · ¬m2_a + m1_a · m2_a**

Esta ecuación es distinta a la que planteé (**S_a=m1_a+m2_a**), aunque las dos dan la misma tabla de verdad. Para demostrar que son equivalentes hay que simplificarla con las leyes de álgebra de Boole, como hago en el apartado siguiente.

### SIMPLIFICACIÓN ALGEBRAICA C3

Voy a demostrar con leyes, que estas dos ecuaciones son iguales (C3):

**¬m1·m2 + m1·¬m2 + m1·m2 = m1 + m2**

Para que se lea mejor voy a llamar **A =m1_a** y **B=m2_a**. La ecuación se queda así:

**S = ĀB + AB̄ + AB**

\*(la barra encima significa NOT)

Voy a utilizar de apoyo la tabla de leyes de la diapositiva 7 del Módulo VIII.

1.  **Ley idempotente (A+A=A), pero leída al revés.**

Lo que voy a hacer es duplicar **AB**, la ley idempotente dice que **X+X=X**, así que puedo escribir **AB** como **AB + AB** sin cambiar nada:

**S = ĀB + AB̄ + AB + AB**

Esto lo hago para poder emparejar AB con cada uno de los otros términos. Reordeno con la ley conmutativa (**A+B=B+A**):

**S = (ĀB + AB) + (AB̄ + AB)**

2.  **Ley distributiva (A(B+C)=AB+AC), pero leída al revés también.**

En cada paréntesis hay una letra repetida, que voy a sacar factor común:

- En **ĀB + AB** se repite **B**, así que queda **B(Ā + A)**.

- En **ĀB + AB** se repite **A**, así que queda **A(B̄ + B).**

**S= B(Ā + A) + A(B̄ + B).**

3.  **Ley inversa ((Ā + A)=1)**

En cada paréntesis aplico la ley en su forma **OR** y me queda la siguiente fórmula:

**S = B(1)+A(1)**

4.  **Ley de identidad. (1A=A), en su forma AND**.

La fórmula quedaría:

**S=B+A = m1_a +m2_a**

Por lo tanto, la ecuación obtenida a partir de la tabla de verdad tiene 3 términos y necesita 2 **NOT, 3 AND** **y 1OR**. La simplificada solo necesita 1 OR. Las dos son equivalentes, pero la simplificada es más fácil de entender.

### CIRCUITO C3

Para el circuito de la C3, voy a hacer una comparación entre la fórmula inicial y la misma después de simplificar.

**Circuito sin simplificar**: S = ¬m1·m2 + m1·¬m2 + m1·m2. Con las siguientes puertas :2 NOT + 3 AND + 1 OR

**Circuito simplificado**: S = m1 + m2. Con las siguientes puertas: 1 OR.

He probado las cuatro combinaciones de entrada en los dos circuitos y en todas las salidas es la misma, lo que confirma con el simulador la equivalencia que demostré con las leyes de álgebra de Boole. La simplificación ha permitido pasar de 6 puertas a 1 sin cambiar el resultado. En un sistema real esto significa un circuito más barato, más rápido y con menos componentes que pueden llegar a fallar.

| m1  | m2  | S esperado |
|-----|-----|------------|
| 0   | 0   | 0          |

| m1  | m2  | S esperado |
|-----|-----|------------|
| 0   | 1   | 1          |

| m1  | m2  | S esperado |
|-----|-----|------------|
| 1   | 0   | 1          |

| m1  | m2  | S esperado |
|-----|-----|------------|
| 1   | 1   | 1          |

## CONDICIÓN C4: CONECTIVIDAD

Primero voy a ver cómo puedo expresar con Boole si un viaje es posible. Voy a utilizar la variable **o_a**. Voy a suponer que si una estación está cerrada (**o_a=0**), los trenes no pueden pasar por ella, por ejemplo, por un incidente en la vía.

Un viaje concreto de **JV** a **SF**

Para llenar a **SF** desde **JV**, el único camino es **JV -\> SC -\> SF**. Para que ese viaje sea posible deben cumplirse todas estas condiciones a la vez:

- JV está abierto: **o_JV**.

- Existe el tramo JV-SC : **x_JV,SC.**

- SC está abierto: **o_SC**.

- Existe el tramo de SC-SF: **x_SC,SF**.

- SF está abierto: **o_SF**.

Como deben cumplirse todas a la vez utilizo **AND**:

**V_JV,SF = o_JV · x_JV,SC · o_SC · x_SC,SF · o_SF**

Donde:

- **V = 1** entonces el viaje es posible.

- **V= 0** entonces el viaje no es posible.

Me basta con un **AND** porque mi red es un árbol y entre dos estaciones hay exactamente un camino. Si hubiera más caminos, el viaje sería posible si funciona el camino 1 o el camino y, y habría que unirlos con un **OR**.

Cálculo del viaje **JV** a **SF**

**x_JV,SC = 1**

**x_SC,SF = 1**

*<u>**Situación 1:** todas las estaciones abiertas</u>*

**V_JV,SF = o_JV · x_JV,SC · o_SC · x_SC,SF · o_SF = 1 · 1 · 1 · 1 · 1 = 1**

El viaje es posible

*<u>**Situación2:** Son Costa – Son Fortesa cerrada (0_SC = 0)</u>*

**V_JV,SF = o_JV · x_JV,SC · o_SC · x_SC,SF · o_SF = 1 · 1 · 0 · 1 · 1 = 0**

El viaje no es posible. Basta con que una de las variables valga 0 para que todo el producto **AND** sea 0. Como mi red es un árbol, el único camino entre **JV** y **SF** pasa por **SC** y no existe una ruta alternativa con la que unir otro camino mediante OR. Por lo tanto, la ecuación booleana confirma lo que ví anteriormente que **SC** es un punto crítico.

Como ya he podido ver que la estación **SC** es un punto crítico, quiero plantear la situación de si SC cierra, ¿qué viajes siguen siendo posibles?

Para cualquier viaje, **V_ab** es un **AND** de todas las estaciones y tramos del camino. Por lo tanto:

- Si el camino pasa por **SC**, la ecuación incluye **o_SC = 0** y el resultado es **V.ab =0**.

- Si el camino no pasa por **SC, o_SC** no aparece en la ecuación y el viaje sigue siendo posible.

Como ya definí en la parte 1, si **SC** queda fuera de servicio, la red se divide en tres partes:

| Grupo        | Estaciones                     | Número |
|--------------|--------------------------------|--------|
| Tronco común | PE, JV                         | 2      |
| Rama M1      | SFV, SCA, GVA, CR, SS, UIB, PB | 7      |
| Rama M2      | SF, SCL, VL, PI, PIN, PM, MA   | 7      |
| Cerrada      | SC                             | 1      |

Comprobación = **2+7+7+1 = 17** estaciones

Con **SC** cerrada, solo se puede viajar entre estaciones del mismo grupo. Demostración:

1.  **Ecuación general de un viaje.** Como mi red es un árbol, entre dos estaciones **a** y **b** existe un único camino. Llamo **C_ab** al conjunto de estaciones de ese camino, incluidas **a** y **b**. Como todos los tramos del camino existen (**x=1**), la ecuación del viaje queda:

**V_ab = Π o_v, para cada v ∈ C_ab**

2.  **Efecto del cierre de SC**. Con **o_SC = 0** y el resto 1, el único factor que puede valer 0 es **o_SC**. Por la propiedad del **AND**, el producto vale = si y solo si alguno de sus factores es 0. Por lo tanto:

**V_ab = 0 ⟺ SC ∈ C_ab**

El viaje es imposible exactamente cuando el camino pasa por **SC.**

3.  **Cuando pasa el comino por SC**. Según *conexiones.csv*, los únicos tramos que tocan **SC**, son **JV-SC,SC-SFV** y **SC-SF** (SC tiene grado 3). Repasando los demás tramos:

    - Dentro de cada grupo hay un camino que no usa **SC**: el tramo **PE-JV** en el tronco, la cadena **SFV–SCA–GVA–CR–SS–UIB–PB** en la rama **M1** y la cadena **SF–SCL–VL–PI–PIN–PM–MA** en la rama **M2**. Como el camino es único, es ese y no contiene **SC**.

    - Entre grupos distintos no hay ningún tramo que una directamente dos estaciones de grupos diferentes. La única forma de pasar de un grupo a otro es a través de **SC**, así que **SC ∈ C_ab**.

4.  **Conclusión**, uniendo los pasos 2 y 3 con **o_SC = 0: V_ab = 1 ⟺ a y b** pertenecen al mismo grupo.

5.  **Consecuencias en números**. Con la red completa hay **17 · 16/2 =136** viajes posibles entre pares de estaciones. Con **SC** cerrada solo quedan los viajes dentro de cada grupo.

| Grupo        | Estaciones | Viajes posibles dentro del grupo |
|--------------|------------|----------------------------------|
| Tronco común | 2          | 2 · 1 / 2 = 1                    |
| Rama M1      | 7          | 7 · 6 / 2 = 21                   |
| Rama M2      | 7          | 7 · 6 / 2 = 21                   |
| Total        |            | 43                               |

Es decir, el cierre de una sola estación deja la red con **43** de los **136** viajes, aproximadamente el **32 %** y elimina el **68%** de los trayectos posibles.

### TABLA DE VERDAD C4

Sigo trabajando sobre la simulación del viaje de **JV -\> SF con SC cerrada**. Lo primero que hago es coger las variables que pueden cambiar, que son las tres estaciones: **o_JV, o_SC** y **o_SF**. Los tramos valen siempre 1 porque existen. Con tres variables en este caso salen 8 filas (2 elevado a 3). Ecuación: **V = o_JV · o_SC · o_SF**

| o_JV | o_SC | o_SF | V   |
|------|------|------|-----|
| 0    | 0    | 0    | 0   |
| 0    | 0    | 1    | 0   |
| 0    | 1    | 0    | 0   |
| 0    | 1    | 1    | 0   |
| 1    | 0    | 0    | 0   |
| 1    | 0    | 1    | 0   |
| 1    | 1    | 0    | 0   |
| 1    | 1    | 1    | 1   |

### DE TABLA A ECUACIÓN C4 (Viaje JV -\> SF)

En la tabla solo hay un 1, en la fila **o_JV=1, o_SC=1, o_SF=1**. Como las tres valen 1, se escriben tal cual:

**V = o_JV · o_SC · o_SF**

Coincide con la ecuación planteada.

### CIRCUITO C4

Voy a seguir utilizando el viaje que he usado en la explicación de JV a SF.

Ecuación: **V = o_JV · o_SC · o_SF**

1.  Es colocar las tres entradas del tramo a recorrer y lo que me van a indicar es si esta estación esta abierta (1) o está cerrada (0).

2.  Coloco la puerta AND a la derecha de los tres inputs pins.

3.  Colocar la salida que es V y conectar los cables.

| Situación      | o_JV | o_SC | o_Sf | V   |
|----------------|------|------|------|-----|
| Todas abiertas | 1    | 1    | 1    | 1   |

En este caso donde V=1, el viaje es posible. Ahora vemos V=0, donde el viaje es imposible.

| Situación  | o_JV | o_SC | o_Sf | V   |
|------------|------|------|------|-----|
| SC cerrada | 1    | 0    | 1    | 0   |

## SISTEMA DE VERIFICACIÓN DE LA RED

Después de implementar cada condición por separado, he diseñado el sistema que combinan todas en un solo circuito. El sistema tiene una salida, **RED_OK**, que vale 1 solo si se cumplen las cuatro condiciones a la vez y por eso las cuatro se juntan con una puerta **AND**.

Debido a que mi red tiene **289 variables x_ab,** y representarlas todas en el simulador no sería viable, he decidido que cada condición la represento con el caso explicado en cada una de las condiciones. El **objetivo** del circuito es mostrar cómo se combinan las condiciones es un sistema; la comprobación completa sobre toda la red la voy a realizar en Python en el apartado siguiente.

En total mi sistema tiene 10 entradas, 6 puertas lógicas y 5 salidas, las 5 salidas se deben a que así me sirven las 4 salidas intermedias de las condiciones (C1,C2,C3,C4) como indicadores de que todo está funcionando correctamente.

En el caso de que una de las condiciones no se cumplan la red no funciona correctamente:

# COMPROBACIÓN CON PYTHON

Con el simulador de circuitos he comprobado las condiciones con casos de ejemplo, pero para comprobarlo sobre toda mi red he creado un nuevo programa en Python, ***src/booleano_metro.py***.

Este programa reutiliza la función que creé de *cargar_grafo* en ***src/metro_palma.py***, que importa sin modificar el fichero original. Así no repito código, y las comprobaciones se hacen exactamente sobre el mismo grafo que ya he construido y verificado.

Mi red consta de **289** variables, **17** estaciones y todos los viajes posibles.

Primero creo la <u>matriz booleana</u>:

El programa sigue 3 pasos:

1.  **Carga la red desde los ficheros CSV** con la función *cargar_grafo* de *metro_palma.py* y en una lista (**V**) guarda los identificadores de las **17** estaciones.

2.  **Crea la matriz booleana x_ab** como un diccionario dentro de otro diccionario, que funciona como una tabla **x\[“PE”\]\[“JV”\]** es la casilla de la fila PE y la columna de JV. Al principio todas las casillas valen 0, es decir False.

3.  **Pone a 1 los tramos que existen**. Para ello recorre la lista enlazada de cada estación con el método vecinos y por cada vecina, cambia la casilla correspondiente por 1. Aquí se demuestra el planteamiento del inicio cuando dije que la estructura principal es la lista de adyacencia y se genera una matriz a partir de ella cuando hace falta.

Este es el resultado:

**Las variables x_ab:** 289 sale de 17 x 17.

**Las variables a 1:** 32 son 16 tramos por 2 porque es de doble sentido.

**Las variables a 0**: 257 viene de 289-32.

**<u>Errores encontrados al realizar el código:</u>**

1.  Se me olvido poner el *import* y no me detectaba la función *cargar_grafo*.

## Comprobación de la condición C1: Simetría

El programa recorre los 289 pares de estaciones (a,b) y, para cada uno, calcula dos ecuaciones:

1.  El detector de fallo **F_ab = x_ab · ¬x_ba.** En Python los operadores and, or y not corresponden a AND, OR, NOT, por lo que la ecuación se escribe casi igual que en álgebra de Boole. Uso *int()* para convertir los resultados *True/False* de Python en 1 y 0.

2.  La versión obtenida con De Morgan, **¬F_ab = ¬x_ab + x_ba.** El programa comprueba en cada par que esta ecuación vale exactamente lo contrario que **F_ab**.

Si un par tiene **F_ab =1**, se guarda en la lista ***fallos_c1***. Al final, la red cumple **C1** si esa lista está vacía.

Este resultado confirma sobre toda la red lo que había visto en el ejemplo **c_SC,SF =x_SF,SC = 1**: todos los tramos se pueden recorrer en los dos sentidos, como corresponde a un grafo no dirigido. También confirma en los 289 pares la simplificación con De Morgan, que antes había comprobado con la tabla de verdad.

**Prueba con un error provocado**

Una lista de fallos vacía podría significar que la red es correcta, pero también que el detector no funciona. Para descartar que este es el caso, he provocado un tramo de sentido único:

He trabajado sobre una copia de la matriz (***copy.deepcopy***) para no modificar la red real, que uso en las comprobaciones siguientes. En la copia he quitado el sentido **SF -\> SC**, como si el tramo solo pudiera recorrerse de **SC -\> SF**.

El detector encuentra exactamente el par donde dice que existe el tramo de SF a SC, pero no de SC a SF.

## Comprobación de la condición C2: Sin lazos

El programa calcula la ecuación **L**, que corresponde a la diagonal de la matriz booleana. La variable **L** empieza en 0 y en cada vuelta del bucle hace un **OR** con la casilla de la diagonal de la siguiente estación. Es el mismo funcionamiento que encadenar las **16 puertas** **OR** del circuito en cuanto una estación tiene lazo, **L** pasa por 1 y ya no vuelve a 0.

Como **L es un detector de fallo**, la condición se cumple cuando **L=0**. Por eso calculo **C2 = ¬L**, igual que en el sistema de verificación, dónde usé una puerta NOR para negar el resultado del **OR**.

**Prueba con un error provocado**

Igual que en la **C1**, he comprobado que el detector funciona provocando un error sobre una copia de la matriz: he puesto un lazo en **SC-SF**. El programa obtiene **L=1** e identifica **SC** como la estación con lazo. Esto demuestra que es el comportamiento del **OR** que había justificado al plantear la condición.

Este es el resultado de la comprobación y la prueba de error: donde se puede confirmar que toda la diagonal de la matriz esta a 0, es decir, ninguna estación tiene un tramo consigo misma.

## Comprobación de la condición C3: Servicio

Lo primero que hace mi programa es crear las variables auxiliares **m1_a** y **m2_a** a partir de la columna ***líneas*** de **estaciones.csv**, que guarda como una lista cada estación, por ejemplo, **\[“M1”, “M2”\]**. Si la línea aparece en la lista la variable vale 1, y si no, 0.

Después, para cada estación calcula dos versiones de la ecuación:

- **La ecuación simplificada,** S_a=m1_a + m2_a.

- **La ecuación obtenida de la tabla de verdad:** S_a = ¬m1_a · m2_a + m1_a · ¬m2_a + m1_a · m2_a.

El programa comprueba que las dos ecuaciones dan el mismo resultado en las 17 estaciones. Al final**, S** es el **AND** de todas las **S_a**. La red cumple **C3** solo si todas las estaciones tienen al menos una línea.

La variable **S** empieza en 1 porque se trata de un **AND** acumulado. Según la **ley de identidad** (1·A = A), empezar en 1 no altera el resultado. Si empezara en 0, por la **ley nula** (0·A = 0) el resultado sería siempre 0. En cambio, en la C2 L empezaba en 0, porque allí se hacía un OR acumulado y la **ley de identidad** del OR es 0 + A = A.

**Prueba con un error provocado**

He hecho una prueba sobre una copia de las variables de línea y en ella he quitado las dos líneas a **PI (m1_PI = m2_PI= 0)**. El programa obtiene **S = 0** e identifica **PI** como la estación sin servicio.

Esto demuestra que, por el comportamiento del **AND**, basta con que una sola estación se quede sin línea para que la red no cumpla la condición.

El resultado confirma que todas las estaciones de mi red tienen al menos una línea. Además, comprueba sobre los datos reales que la simplificación algebraica es correcta: las dos ecuaciones dan el mismo resultado en las 17 estaciones, igual que en la tabla de verdad y en los dos circuitos de Logisim.

## Comprobación de la condición C4: Conectividad

Para comprobar la conectividad sobre toda la red he definido dos funciones:

- ***camino(origen, destino)*** obtiene el camino entre dos estaciones. Se basa en el recorrido en anchura (BFS) que utilicé para comprobar que el grafo es conexo, con un añadido: cada vez que descubre una estación, guarda desde qué estación ha llegado a ella. Al terminar, reconstruye el camino yendo hacia atrás desde el destino hasta el origen. Como mi red es un árbol, este camino es el único que existe entre las dos estaciones.

- ***Viaje_posible(a, b, o)*** calcula la ecuación **V_ab**: el AND de las variables o de todas las estaciones del camino y de las variables x de todos sus tramos. Recibe como parámetro el estado de las estaciones (o), para poder simular distintos escenarios.

Con ***combinations(V,2)*** genero todos los pares distintos de estaciones. Como el grafo no dirigido, el viaje de **a** a **b** se cuenta una sola vez, así que hay **17 · 16 / 2 = 136 viajes posibles**.

Por otro lado, he comprobado también las dos situaciones que plantee en la explicación de la condición.

**Escenario 1**: **red normal**. Con todas las estaciones abiertas, los 136 viajes son posibles, así que C4 = 1. Esto coincide con la comprobación de que el grafo es conexo.

**Escenario 2:** es el cierre de SC-SF donde o_SC = 0.

Los resultados coinciden con los cálculos que hice a mano y con la demostración por grupos. De los **93 viajes perdidos, 77 son viajes entre estaciones de grupos distinto**s (que obligatoriamente pasan por SC) y **16 son los viajes con origen o destino en la propia SC**, que también son imposibles porque está cerrada.

El programa confirma que **basta con el cierre de una estación para dejar a la red con menos de un tercio de sus viajes**. **SC** es un **punto crítico** y la red es poco robusta ante incidencias.

## Sistema de verificación de la red completa

Por último, el programa combina las cuatro condiciones con la misma ecuación que el sistema de verificación diseñado en Logisim. **RED_OK = C1·C2·C3·C4**. La diferencia es que en el circuito cada condición se representa con un caso de ejemplo, mientras que aquí cada una se ha calculado sobre toda la red: **los 289 pares de la C1, las 17 estaciones de la C2 y la C3, y los 136 viajes de la C4.**

Lo he probado con **tres escenarios**. En todos he usado como ejemplo de la C1 un par de estaciones conectadas en los dos sentidos (**x_ab = x_ba = 1, como Sc-SF**), y como ejemplo de la C3 una estación solo de la línea M1 (**m1 = 1. M2 = 0, como UIB**).

En el primer escenario mi red cumple todas las condiciones. En los otros dos, un solo cambio basta para que RED_OK pase a 0, y la salida intermedia indica exactamente dónde está el problema: en el escenario 2 se apaga C4 (conectividad) y en el escenario 3 se apaga C1 (simetría). Esto muestra cómo las ecuaciones booleanas permiten diseñar un sistema que vigila automáticamente el estado de la red y localiza las incidencias.

# ESTRUCTURA ALGEBRAICA DE LA RED

Una estructura algebraica esta formada por un conjunto de elementos, unas operaciones definidas sobre ese conjunto y unas propiedades que esas operaciones cumplen siempre. En mi trabajo:

- **El conjunto** es B = {0, 1}, los dos valores que pueden tomar todas mis variables (x_ab, m1_a, m2_a y o_a).

- **Las operaciones** son OR (+), AND (·) y NOT (¬).

- **Las propiedades** son las leyes lógicas de los apuntes (UCS, 2026).

Esta estructura **(B, +, ·, ¬),** es un álgebra de Boole. Una característica importante es que le conjunto es cerrado para las tres operaciones: el resultado siempre es 0 o 1. Por ejemplo, en la estación compartida SC**, m1 + m2 = 1 + 1 = 1, y no 2** como en la suma habitual.

A lo largo del análisis de mi red he aplicado casi todas las leyes lógicas excepto la de absorción (A + AB = A). Cada una ha tenido un papel concreto al planear, simplificar, implementar o programar las condiciones de mi red.

| Ley | Fórmula | ¿Dónde la usé? |
|---|---|---|
| identidad | **1 · A = A / 0 + A = A** | **C3**: simplificación (paso5) y código.<br>**C2**: Codigo L empieza en 0 |
| Nula | **0 · A = 0** | **C3**: código al explicar porque S no puede empezar en 0.<br>**C4**: basta con una estación cerrada para que V = 0 |
| Idempotente | **A + A = A** | **C3:** simplificación (paso 1), también en SC: m1 + m2 = 1+1 = 1 |
| Inversa | **A + Ā = 1** | **C3**: simplificación (paso 4) |
| Conmutativa | **A + B = B + A** | Simplificación de la C3 (pasos 2 y 6) |
| Asociativa | **(A + B) + C = A + (B + C)** | **C3:** simplificación (paso 2).<br>**C2**: una puerta OR de 17 entradas equivale a encadenar 16 OR de 2, porque da igual cómo se agrupen. |
| Distributiva | **AB + AC = A(B + C)** | **C3**: simplificación (paso 3) para sacar el factor común |
| De Morgan | **¬(A · B) = Ā + B̄** | **C1**: de F_ab a ¬x_ab + x_ba |

Hasta ahora he hablado de la estructura de cada variable, a continuación, voy a centrarme en la **estructura de toda la red.** Mi red es un conjunto de tramos, E, con 16 elementos y cada línea es un subconjunto de E: M1 son los tramos que recorren la línea M1 y M2 los que recorren las de la M2.

En mis apuntes, las operaciones de AND, OR, NOT se representan con diagramas de Venn, porque cada operación booleana corresponde a una operación de la teoría de conjuntos:

| Álgebra de Boole | Teoría de conjuntos | Sobre la matriz booleana       |
|------------------|---------------------|--------------------------------|
| OR (+)           | Unión (∪)           | x_M1 + x_M2, casilla a casilla |
| AND (·)          | Intersección (∩)    | x_M1 · x_M2, casilla a casilla |
| NOT (¬)          | Complemento (ᶜ)     | ¬x, casilla a casilla          |

Por lo tanto, aplicar una operación booleana a dos matrices casilla a casilla equivale a aplicar la operación de conjuntos a sus tramos. Para comprobarlo, he creado una matriz booleana para cada línea a partir del atributo líneas de cada nodo de la lista enlazada, y he calculado las tres operaciones, como se puede ver en el código de la imagen de abajo.

| Operación     | Resultado                 | Interpretación en mi red                     |
|---------------|---------------------------|----------------------------------------------|
| M1            | 9 tramos                  | Tronco común (2) + rama M1 (7)               |
| M2            | 9 tramos                  | Tronco común (2) + rama M2 (7)               |
| M1 ∪ M2 (OR)  | 16 tramos                 | Es exactamente mi red completa               |
| M1 ∩ M2 (AND) | 2 tramos: PE–JV y JV–SC   | El tronco común que comparten las dos líneas |
| ¬x (NOT)      | 257 casillas (120 tramos) | Conexiones que no existen en mi red          |

***Unión e intersección.*** La unión de las dos líneas tiene 16 tramos y no 9 + 9 = 18, porque los dos tramos del tronco común pertenecen a las dos líneas y se contarían dos veces. Esto cumple el principio de inclusión-exclusión de la cardinalidad de conjuntos \|M1 U M2\| = \|M1\| + \|M2\| - \|M1 ∩ M2\| = 9 + 9 − 2 = 16. Además, confirma la decisión de diseño de representar cada tramo compartido como una sola arista con el atributo M1\|M2.

***Complemento.*** El complemento de la matriz tiene 257 casillas a 1, las mimas 257 casillas a 0 de la matriz de adyacencia del inicio del análisis. Si se descartan los lazos (la diagonal) y los tramos repetidos en los dos sentidos, quedan 120 tramos que podrían construirse y no existen. Coincide con el calculo de: 136 aristas posibles – 16 existentes = 120. Este conjunto representa todas las posibles ampliaciones de la red, y es el punto de partida para proponer mejoras en la Parte 4.

***Conclusión.*** Igual que el conjunto {0, 1} con OR, AND y NOT forma un álgebra de Boole, el conjunto de todas las redes posibles entre mis 17 estaciones, con la unión, la intersección y el complemento, cumple las mismas leyes. Por eso las ecuaciones booleanas no solo sirven para comprobar condiciones sobre tramos concretos, sino también para trabajar con líneas y redes completas: unirlas, ver que comparten o encontrar las conexiones que faltan.

# CÓMO AFECTAN LAS ECUACIONES BOOLEANAS SOBRE LA RED

## Lo que garantiza cada ecuación

Cada ecuación booleana traduce una propiedad de la red en algo que se puede comprobar. Cuando la condición se cumple, garantiza algo concreto al viajero o al gestor de la red:

- **C1: Simetría.** El viajero puede volver por el mismo camino por el que ha venido. Si no se cumpliera esta condición, habría tramos de sentido único y estaciones a las que se podría llegar, pero de las que no se podría volver.

- **C2: Sin lazos.** Los datos de la red son coherentes. Si esta condición fallara, habría un error en el dataset, ya que un tramo de una estación a sí misma no existe físicamente.

- ***C3: Servicio.*** En todas las estaciones para al menos una línea. Si esta condición fallara, habría una estación en el mapa sin ningún tren.

- ***C4:*** ***Conectividad.*** Se puede viajar entre cualquier par de estaciones. Si esta condición fallara, habría viajes imposibles y la red quedaría dividida.

Como ya he comprobado con las tablas de verdad, con un simulador de circuitos y con un programa de Python sobre mis datos, mi red cumple estas cuatro condiciones (RED_OK = 1).

## La forma de la ecuación revela la fragilidad de la red.

El resultado más importante del análisis es que la forma de las ecuaciones refleja la estructura de la red. Como mi red es un árbol, entre dos estaciones hay un único camino, y la ecuación de cada viaje es un único producto AND de todas las estaciones y tramos de ese camino. Por la **ley nula**, basta con que un solo factor valga = para que todo el viaje sea imposible.

Por eso el cierre de una sola estación, Son Costa -\> Son Fortesa, elimina 93 de los 136 viajes (el 68%). Las ecuaciones booleanas no solo confirman que SC es un punto crítico, sino que permiten medirlo con exactitud y explicar porque ocurre.

Si la red tuviera caminos alternativos, la ecuación de un viaje debería de ser un único AND y pasaría a ser un OR de varios AND, uno por cada camino:

**V_ab = (camino 1) + (camino 2)**

En ese caso, aunque un camino fallara, el viaje seguiría siendo posible siempre que el otro funcionara.

## Las ecuaciones me señalan donde mejorar.

Por último, el análisis indica que se puede mejorar. El complemento de la matriz booleana da los **120 tramos que no existen y que podrían construirse**, y la condición **C4** identifica el **punto débil** de la red. Combinando las dos cosas, una mejora útil sería añadir tramos que creen un camino alternativo que no pase por SC, de forma que la ecuación de los viajes entre ramas incluya un OR.

# CONCLUSIÓN

En esta parte del proyecto he aplicado el álgebra de Boole a la red de metro de Palma siguiendo este proceso:

| Fase                  | Resultado                                                                                                                                    |
|-----------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| Variables             | La red traducida a 289 variables booleanas x_ab (la matriz de adyacencia como matriz booleana) y a las variables auxiliares m1_a, m2_a y o_a |
| Condiciones           | Cuatro condiciones expresadas como ecuaciones: simetría, sin lazos, servicio y conectividad                                                  |
| Tablas de verdad      | Una tabla por condición, comprobada también al revés (de la tabla a la ecuación)                                                             |
| Simplificación        | Ecuación de la C3 simplificada con seis leyes, y teorema de De Morgan aplicado a la C1                                                       |
| Circuitos             | Circuitos de cada condición en Logisim y un sistema de verificación que las combina en una salida RED_OK                                     |
| Python                | Comprobación de las cuatro condiciones sobre todos los datos de la red                                                                       |
| Estructura algebraica | (B, +, ·, ¬) como álgebra de Boole y la red como conjunto de tramos con unión, intersección y complemento                                    |

Este proceso me ha ayudado a:

- **Entender la red:** las ecuaciones booleanas han permitido convertir afirmaciones sobre la red, en condiciones precisas que se pueden comprobar.

- **Optimizar la red:** el álgebra de Boole me ha ayudado a mejorar la red. LA simplificación de la C3 ha reducido el circuito de 6 puertas a 1 sin cambiar el resultado, lo que supone menos costes, menos componentes y menos puntos de fallo. El sistema de verificación muestra cómo se podría vigilar el estado de la red y localizar automáticamente una incidencia. Por último, el complemento de la matriz y la ecuación de la conectividad indican donde actuar.

También he podido ver que mi herramienta tiene **limitaciones** que conviene reconocer:

- **Solo trabaja con dos valores.** Una variable booleana dice si un tramo existe o si una estación está abierta, pero no recoge información como el tiempo de un trayecto, la frecuencia de los trenes o el número de viajeros.

- **Algunas variables son supuestos.** La variable o_a no forma parte del dataset y he supuesto que por una estación cerrada no pueden pasar trenes, cuando en la realidad a veces si pasan sin detenerse.

- **Los circuitos, usan casos de ejemplo.** Representar las 289 variables en un simulador no es viable, por eso la comprobación completa la he hecho en Python.

El álgebra de Boole es una herramienta útil para analizar una red de transporte: permite expresar sus reglas de forma precisa, comprobarlas automáticamente, detectar sus puntos débiles y diseñar sistemas que la vigilen. Su principal aportación es este trabajo ha sido demostrar que la red del metro de Palma es correcta pero frágil, y que la forma de mejorarla es crear caminos alternativos.

# BIBLIOGRAFÍA

- De-Rossi Consulting (2026) logisim.app \[Simulador de circuitos digitales\]. Disponible en: <https://logisim.app/> (Consultado: 19 noviembre 2026).

- Python Software Foundation (s.f.) copy — Shallow and deep copy operations. Disponible en: <https://docs.python.org/3/library/copy.html> (Consultado: 17 noviembre 2026).

- Python Software Foundation (s.f.) itertools — Functions creating iterators for efficient looping. Disponible en: <https://docs.python.org/3/library/itertools.html> (Consultado: 18 noviembre 2026).

- UCS (2026) Discrete Mathematics. Módulo III: Teoría de Conjuntos y Funciones \[Apuntes de clase\]. UCS.

- UCS (2026) Discrete Mathematics. Módulo VIII: Ecuaciones Booleanas \[Apuntes de clase\]. UCS.

## Declaración de IA

En esta parte he utilizado Claude (Anthropic, 2026) con un papel de tutor y de apoyo de código.

1.  **Organización**. Para divir la Parte 3 en pasos y estimar los tiempos.

2.  **Tutor.** para entender conceptos que me costaban (la implicación lógica, cuando usar AND u OR, la doble degación), con ejemplos y preguntas de comprobación que yo respondía antes de continuar.

3.  **Revisión** de mi redacción y me indicó correcciones.

4.  **Código.** debatir sobre estructuras de código y ayudarme a razonar la elección de estas.

5.  **Circuitos**. Para el rpier circuito pedí ayuda para que explicara como se utilizaba la herramienta y una vez lo entendía los hice yo todos.

Las decisiones sobre el trabajo las he tomado yo, como la notación x_ab, la organización del documento… He comprobado todos los resultados con mis datos y entiendo y soy capaz de explicar cada ecuación, circuito y bloque de código.
