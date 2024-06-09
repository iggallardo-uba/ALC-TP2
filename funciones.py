import scipy
import numpy as np
import pandas as pd
import seaborn as sns
import seaborn.objects as so

# Para clustering
from sklearn.datasets import make_blobs
from sklearn.datasets import make_circles
from sklearn.preprocessing import MinMaxScaler 
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN

# Para componentes principales
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

#Tabla nutricional
tabla_nutricional = pd.read_csv("data/tabla_nutricional.csv", sep=";")

tabla_nutricional[tabla_nutricional.isna()] = 0

#Datos de Precio
Precios = pd.read_csv("data/consumidores_libres.csv", sep=";")

def tabla_view():
    return tabla_nutricional

def chequeoDieta(data):
    #Cantidad Total
    cantidadTotal = sum(data["Cantidad"])
    
    #Maximo/Minimo Proteina
    minProteina = cantidadTotal*0.1
    maxProteina = cantidadTotal*0.15
    
    #Maximo/Minimo HC
    minHC = cantidadTotal*0.1
    maxHC = cantidadTotal*0.15
    
    #Maximo/Minimo Grasas
    minGrasas = cantidadTotal*0.15
    maxGrasas = cantidadTotal*0.3
    
    #Variables
    proteina = 0
    HC = 0
    Na = 0
    fibra = 0
    grasas = 0
        
    for index, row in data.iterrows():
        dataAlimento = tabla_nutricional[tabla_nutricional["Alimento"] == row["Producto"]]
        cantidadAlimento = row["Cantidad"] / dataAlimento["Cantidad (gr/ml)"].to_numpy()[0]
        
        #Proteina
        proteina += cantidadAlimento * dataAlimento["Proteinas (gr)"].to_numpy()[0]
        
        #Carbohidratos
        HC += cantidadAlimento * dataAlimento["HC (gr)"].to_numpy()[0]

        #Grasas Totales
        grasas += (cantidadAlimento * dataAlimento["Grasas (gr)"].to_numpy()[0])/30
        
        #Sodio
        # > 200 mg/dia Aceptado
        Na += (cantidadAlimento * dataAlimento["Na (mg)"].to_numpy()[0])/30
        
        #Fibra
        # > 25 g/dia aceptado
        fibra += (cantidadAlimento * dataAlimento["Fibra (gr)"].to_numpy()[0])/30
        
        
        #Frutas y Verduras
        # >= 400 g/dia Aceptado
        #Falta una forma de calificar Frutas y Verduras segun sus caracteristicas
        
    print(minProteina, proteina, maxProteina)   
    print(minHC, HC, maxHC) 
    print(minGrasas, grasas, maxGrasas) 
    print(200," > ", Na)
    print(25," > ", fibra) 
    print("Frutas y Verduras pendiente")
        
    return True