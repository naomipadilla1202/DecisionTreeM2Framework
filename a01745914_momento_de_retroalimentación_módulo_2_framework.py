# -*- coding: utf-8 -*-
"""A01745914_Momento de Retroalimentación: Módulo 2-Framework.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jebVpiN3A2Cd-mkPGNFVwJ1Ttm7ryyJF?usp=sharing

#Momento de Retroalimentación: Módulo 2 Uso de framework o biblioteca de aprendizaje máquina para la implementación de una solución
##Naomi Padilla Mora A01745914

#Librerías

Importamos las librerias necesarias
"""

import pandas as pd
import numpy as np
from pandas import read_csv
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

"""#Base de datos
"""
#click derecho sobre el file > copy path > pegar path
df = pd.read_csv("titanic.csv", header=0)
df.head()

"""#Limpieza del Dataset

##Información del dataset

Información básica sobre la base de datos.



*   12 columnas y 891 filas
*   Inicialmente contamos con 5 variables categóricas (object), 7 variables numéricas (5 int y 2 float)
"""

df.shape

#Tipos de variables
df.dtypes

"""##Valores duplicados
Con el comando duplicated se observará si hay registros duplicados en el dataset.
"""

#comando para saber su hay alguna entrada duplicada en nuestro dataset
df.duplicated(subset=None)

"""Obteniendo el valor **False** para cada renglón, podemos confirmar que no hay ningún registro duplicado en el dataset, por lo que ningún procesamiento será necesario para esto.

##Valores faltantes o nulos
"""

#Comando para ver la cantidad de valores nulos en cada variable.
df.isna().sum()

"""Tras este análisis, con el comando **isna**, podemos destacar lo siguiente:

| Variable | Tipo | # NaN |
|----------|----------|----------|
| Age   | Float   | 177  |
| Cabin    | Object   | 687   |
| Embarked    | Object   | 2   |

Debido a las dimensiones del dataset, 891 filas y 12 columnas, no resulta conveniente solo eliminar los valores nulos, ya que, eliminar las entradas con estos valores, quitaríamos un mín de 687 entradas.

Por ello, la técnica de procesamiento será reemplazar los valores nulos en el caso de Age. Para la variable Cabin, como esta no proporciona información de real utilidad, se eliminará la columna completa. También se eliminarán los 2 valores nulos de Embarked.
"""

#Eliminamos los valores nulos de la variable Embarked
df = df.dropna(subset="Embarked")

#Eliminamos la columna Cabin
df = df.drop(columns=["Cabin"])

#calculamos la media de las edades de cada grupo (Sex: male, female) con el objetivo de sustituir nos nulos de Age
mean_age = df.groupby('Sex')['Age'].transform('mean')
mean_age = mean_age.round() #redondeamos las medias
df['Age'].fillna(mean_age, inplace=True) #reemplazamos los nulos con las medias

#comprobamos que ya no hay nulos
df.isna().sum().sum()

"""Tras utilizar nuevamente el comando isna podemos confirmar que ya no hay ningún valor nulo en nuestro dataset por lo que se encuentra listo para futuro análisis o implementación de un modelo.

Antes de continuar con la implementación del modelo, eliminamos las siguientes variables que no proporcionan información de valor para el análisis como:

Name: el nombre del pasajero no tiene gran relevancia en si este sobrevive o no.
Ticket: el número de ticket tampoco tiene mucha relevacia para si el pasajero sobrevive o no, además, podemos tener información más relacionada de Pclass.
"""

#eliminamos columna Name
df = df.drop(columns=["Name"])

#eliminamos columna Ticket
df = df.drop(columns=["Ticket"])

"""##Variables categóricas: Encoded

Convertimos las variables categóricas en numéricas para poder hacer un análisis de correlación con las variables restantes.

"""

reemplazo = {'Sex': {"male": 1, "female": 0},
            'Embarked': {"C": 1, "Q": 2, "S":3}}
# Aplicar el reemplazo a las columnas especificadas
df.replace(reemplazo, inplace=True)

df.dtypes

"""##Correlación"""

sns.heatmap(df.corr(), annot=True)

"""Tomamos las variables con correlación > |0.15| respecto a la variable Survived que es la variable a predecir"""

df = df[["Pclass","Sex","Fare","Embarked","Age","Survived"]]
df

"""#Modelo

Implementación de un modelo de árbol de decisión con el uso de Framework

##Separación de los datos en train y test
"""

#definimos las variables que tendremos en X y en y (variable a predecir)
X = df.drop(columns=["Survived"]) #eliminamos la columna Survived
y = pd.DataFrame(df["Survived"]) #mantenemos solo la columna Survived

#haciendo uso del train_test_split con un 30% para test y 70% para train, separamos nuestro df
train_data, test_data = train_test_split(df, test_size=0.3, random_state=42)
#damos una semilla aleatoria, esta se puede cambiar pero alteraría los resultados del modelo en cada ocasión.

X_train = X.values
y_train = y.values
X_test = X.values
y_test = y.values

"""##Árbol de decisión"""

#Haciendo uso de la libreria from sklearn.tree import DecisionTreeRegressor
#creamos nuestro albol con al profundidad deseada
#como no es una base de datos muy grande, no requiere una profundidad muy grande
regressor = DecisionTreeRegressor(max_depth=10)

#hacemos un fit del modelo para ajustar los parámetros internos de la manera más adecuada
regressor.fit(X_train, y_train)

#preddición del modelo
y_pred = regressor.predict(X_test)

"""##Metricas de evaluación del modelo"""

#solo correr
def metricas_modelo(y_test, predicciones):

#Métricas ideales para una regression


#Se utilizan tres métricas para la evaluaación del modelo: MAE, MSE y R-square ya que al ser un modelo de regression, no se puede utiizar alguna otra como precision, recall o f1.


    # Mean Absolute Error (mae)
    # Prom. de las diferencias absolutas entre las predicc. y los valores reales.
    # Cuanto menor sea el MAE, mejor será el rendimiento.
    mae = mean_absolute_error(y_test, y_pred)
    print("Mean Absolute Error (MAE):" ,mae)

    # Mean Square Error (mse)
    # Penaliza los errores más grandes al tomar la raíz cuadrada de la media de los errores al cuadrado.
    # Igual que el mae, cuanto menor sea el MSE, mejor será el rendimiento.
    mse = mean_squared_error(y_test, y_pred)
    print("Mean Squared Error (MSE):", mse)

    # R-square (r**2)
    #Proporción de la varianza en los datos en el modelo.
    # Un valor cercano a 1 indica un buen ajuste del modelo.
    r2 = r2_score(y_test, y_pred)
    print("R-squared (R2):", r2)

print("Modelo max detph=10 \n")
metricas = metricas_modelo(y_test, y_pred)


"""#Generalización del modelo

La generalización del modelo consiste en dos partes.

1. La creación del árbol y su evaluación.

2. El cálculo de las predicciones según las entradas.

Una entrada se conforma de todas las siguientes variables:

feature_names=['Pclass', 'Sex', 'Fare', 'Embarked', 'Age']

Pclass: Ticket class, 1 = 1st, 2 = 2nd, 3 = 3rd

Sex:0 female, 1 male

Fare: Passenger fare

Embarked: Port of Embarkation,	C = Cherbourg, Q = Queenstown, S = Southampton

Age: Age in years (float 'cause babies less that 1y)


Se pueden utilizar los valores deseados para estas pero para fines de practicidad de tomaran entradas específicas del df de test.

Esto con el objetivo de predecir si ese pasajero sobrevivió o no (0 = No, 1 = Yes).

##Árbol profundidad_máxima=10

Como se observó, el árbol con una profundidad máxima no tiene buenos puntajes en las métricas por lo que se esperan predicciones alejadas de la realidad.
"""
print("\n Generalización del modelo \n")

print("Modelo max detph=10 \n")
regressor = DecisionTreeRegressor(max_depth=10) #creación del modelo
regressor.fit(X_train, y_train) #fit del modelo
y_pred = regressor.predict(X_test) #predicción del modelo
metricas = metricas_modelo(y_test, y_pred) #métricas del modelo

"""###Caso 1

Evaluación del modelo con una profundidad máxima de 10, caso de ejemplo la entrada 0 del df.

Y el resultado esperado para esta entrada es Survived = 0 = No Survived


"""
print("\n Caso 1")

print("verdadero: ", y_test[0])

entrada = X_test[0]
# Hacer la predicción
entrada = entrada.reshape(1, -1)
prediccion = regressor.predict(entrada)


# Imprimir la predicción
print(f"Predicción para la entrada {entrada[0]}: {prediccion[0]}")
print("Predicción no acertada")

"""La predicción no fue acertada.

###Caso 2

Evaluación del modelo con una profundidad máxima de 10, caso de ejemplo la entrada 2 del df.

Y el resultado esperado para esta entrada es Survived = 1 = Survived
"""

print("\n Caso 2")

print("verdadero: ", y_test[2])

entrada = X_test[2]
# Hacer la predicción
entrada = entrada.reshape(1, -1)
prediccion = regressor.predict(entrada)


# Imprimir la predicción
print(f"Predicción para la entrada {entrada[0]}: {prediccion[0]}")

print("Predicción no acertada")

"""La predicción no fue acertada.


##Árbol profundidad_máxima=15


Tomando en cuenta los resultados anteriores y que a mayor profundidad mejor será la precisión del modelo, tenemos lo siguiente:
"""

print("\n Modelo max detph=15 \n")


regressor = DecisionTreeRegressor(max_depth=15)
regressor.fit(X_train, y_train)
y_pred = regressor.predict(X_test)
metricas = metricas_modelo(y_test, y_pred)

"""Como se observa en las métricas, la profundidad ayudó bastante a mejorar la precisión del modelo y sus métricas. Pero segumos sin obtener un R^2 mayor a 95 y el mae y mse pueden ser menores, por lo que el modelo puede mejorar.

###Caso 1

Evaluación del modelo con una profundidad máxima de 15, caso de ejemplo la entrada 649 del df.

Y el resultado esperado para esta entrada es Survived = 0 = No Survived
"""

print("\n Caso 1")

print("veradero: ", y_test[649])

entrada = X_test[649]
# Hacer la predicción
entrada = entrada.reshape(1, -1)
prediccion = regressor.predict(entrada)


# Imprimir la predicción
print(f"Predicción para la entrada {entrada[0]}: {prediccion[0]}")

print("Predicción acertada")

"""La predicción fue acertada.

###Caso 2

Evaluación del modelo con una profundidad máxima de 15, caso de ejemplo la entrada 383 del df.

Y el resultado esperado para esta entrada es Survived = 0 = No Survived
"""

print("\n Caso 2")

print("verdadedro: ", y_test[383])

entrada = X_test[383]
# Hacer la predicción
entrada = entrada.reshape(1, -1)
prediccion = regressor.predict(entrada)


# Imprimir la predicción
print(f"Predicción para la entrada {entrada[0]}: {prediccion[0]}")

print("Predicción acertada")

"""La predicción fue acertada.

###Caso 3

Evaluación del modelo con una profundidad máxima de 15, caso de ejemplo la entrada 527 del df.

Y el resultado esperado para esta entrada es Survived = 0 = No Survived
"""

print("\n Caso 3")

print("verdadero: ", y_test[527])

entrada = X_test[527]
# Hacer la predicción
entrada = entrada.reshape(1, -1)
prediccion = regressor.predict(entrada)


# Imprimir la predicción
print(f"Predicción para la entrada {entrada[0]}: {prediccion[0]}")
print("Predicción no acertada")

"""La predicción no fue acertada.

El modelo ya muestra una precisión aceptable en el cálculo de la predicción, sin embargo, se creará un árbol con una mayor profundidad solo para ver si aumentan sus métricas.

##Árbol profundidad_máxima=30
"""

print("\n Modelo max detph=30 \n")

regressor = DecisionTreeRegressor(max_depth=30)
regressor.fit(X_train, y_train)
y_pred = regressor.predict(X_test)
metricas = metricas_modelo(y_test, y_pred)

"""Como podemos ver, las métricas aumentaron, pero no a más de 0.95 pero si muy cerca, ya no es necesario aumentar la profundidad del parbol, pero se puede seguir intentando esperando tener mejores valores en las métricas.

###Caso 1

Evaluación del modelo con una profundidad máxima de 30, caso de ejemplo la entrada 124 del df.

Y el resultado esperado para esta entrada es Survived = 1 = Survived
"""

print("\n Caso 1")

print("verdadero: ", y_test[124])

entrada = X_test[124]
# Hacer la predicción
entrada = entrada.reshape(1, -1)
prediccion = regressor.predict(entrada)


# Imprimir la predicción
print(f"Predicción para la entrada {entrada[0]}: {prediccion[0]}")

print("Predicción acertada")

"""La predicción fue acertada.

###Caso 2

Evaluación del modelo con una profundidad máxima de 30, caso de ejemplo la entrada 761 del df.

Y el resultado esperado para esta entrada es Survived = 1 = Survived
"""

print("\n Caso 2")

print("verdadero: ", y_test[761])

entrada = X_test[761]
# Hacer la predicción
entrada = entrada.reshape(1, -1)
prediccion = regressor.predict(entrada)


# Imprimir la predicción
print(f"Predicción para la entrada {entrada[0]}: {prediccion[0]}")

print("Predicción acertada")

"""La predicción fue acertada.

###Caso 3

Evaluación del modelo con una profundidad máxima de 30, caso de ejemplo la entrada 188 del df.

Y el resultado esperado para esta entrada es Survived = 0 = No Survived
"""

print("\n Caso 3")

print("verdadero: ", y_test[188])

entrada = X_test[188]
# Hacer la predicción
entrada = entrada.reshape(1, -1)
prediccion = regressor.predict(entrada)


# Imprimir la predicción
print(f"Predicción para la entrada {entrada[0]}: {prediccion[0]}")

print("Predicción acertada")

"""La predicción fue acertada.

###Caso 4

Evaluación del modelo con una profundidad máxima de 30, caso de ejemplo la entrada 66 del df.

Y el resultado esperado para esta entrada es Survived = 0 = No Survived
"""

print("\n Caso 4")

print("verdadero: ", y_test[66])

entrada = X_test[66]
# Hacer la predicción
entrada = entrada.reshape(1, -1)
prediccion = regressor.predict(entrada)


# Imprimir la predicción
print(f"Predicción para la entrada {entrada[0]}: {prediccion[0]}")

print("Predicción acertada")

"""La predicción fue acertada.

###Caso 5
Evaluación del modelo con una profundidad máxima de 30, caso de ejemplo la entrada libre:

feature_names=['Pclass', 'Sex', 'Fare', 'Embarked', 'Age'])
entrada = [1,0,6.9234, 2, 20]
"""

print("\n Caso 5")

entrada = [1,0,6.9234, 2, 20]
# Hacer la predicción
entrada = np.array(entrada)
entrada = entrada.reshape(1, -1)
prediccion = regressor.predict(entrada)


# Imprimir la predicción
print(f"Predicción para la entrada {entrada[0]}: {prediccion[0]}")

"""Como podemos comprobar, el modelo funciona de manera apropiada y es posible generalizarlo a la profundidad deseada y con los valores de ejemplo deseados.
Para mayor practicidad se recomienda usar uno de los valores de df de X_test, usando la instraucción X_test[i] donde i = 0 a 888.
Ademas en la seleccion de los hiperparametros como ya se menciono, a mayor sea la profundidad, mejor sera el puntaje del modelo.


#Finalmente

Para probar el modelo solo es necesario realizar lo siguiente:

1. La creación del árbol y su evaluación.

2. El cálculo de las predicciones según las entradas.
"""

"""
regressor = DecisionTreeRegressor(max_depth=0) #colocar la max_depth deseada
regressor.fit(X_train, y_train)
y_pred = regressor.predict(X_test)
metricas = metricas_modelo(y_test, y_pred)

entrada = X_test[0] #colocar el ejemplo de predicción deseado
# Hacer la predicción
entrada = entrada.reshape(1, -1)
prediccion = regressor.predict(entrada)
# Imprimir la predicción
print(f"Predicción para la entrada {entrada[0]}: {prediccion[0]}")
"""
