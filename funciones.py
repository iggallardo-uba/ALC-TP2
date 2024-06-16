import scipy
import numpy as np
import pandas as pd
import seaborn as sns
import seaborn.objects as so
import matplotlib.pyplot as plt

# Para clustering
from sklearn.datasets import make_blobs
from sklearn.datasets import make_circles
from sklearn.preprocessing import MinMaxScaler 
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN

# Para componentes principales
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

#Datos de Precio
Precios = pd.read_csv("data/consumidores_libres.csv")

def tabla_view():
    #Tabla nutricional
    tabla_nutricional = pd.read_csv("data/tabla_nutricional.csv", sep=",")

    #Completar ceros
    tabla_nutricional[tabla_nutricional.isna()] = 0

    #Renombramiento y recalculo de NA, Ca y Fe
    tabla_nutricional = tabla_nutricional.rename(columns={"Na (mg)":"Na (gr)", "Ca (mg)": "Ca (gr)", "Fe (mg)": "Fe (gr)"})

    tabla_nutricional[["Na (gr)","Ca (gr)","Fe (gr)"]] = tabla_nutricional[["Na (gr)","Ca (gr)","Fe (gr)"]]  / 1000

    return tabla_nutricional

def chequeoDieta(data):
    chequeo = True
    
    #Frutas y Verduras
    data_VF = data[data["Verdura/Fruta"] == 1]

    #Cantidad Total
    cantidadTotal = sum(data["Cantidad (gr/ml)"])
    
    #Maximo/Minimo Proteina
    minProteina = cantidadTotal*0.1
    maxProteina = cantidadTotal*0.15
    
    #Maximo/Minimo HC
    minHC = cantidadTotal*0.55
    maxHC = cantidadTotal*0.75
    
    #Maximo/Minimo Grasas
    minGrasas = cantidadTotal*0.15
    maxGrasas = cantidadTotal*0.3
    
    #Variables    
    proteina = sum(data["Proteinas (gr)"])
    HC = sum(data["HC (gr)"])
    grasas = sum(data["Grasas (gr)"])
    Na = sum(data["Na (gr)"])
    fibra = sum(data["Fibra (gr)"])
    VF = sum(data_VF["Cantidad (gr/ml)"])
        
    #Chequeos
    print(minProteina, proteina, maxProteina) 
    if minProteina < proteina < maxProteina:
        chequeo = False
      
    print(minHC, HC, maxHC) 
    if minHC < HC < maxHC:
        chequeo = False
        
    print(minGrasas, grasas, maxGrasas) 
    if minGrasas < grasas < maxGrasas:
        chequeo = False
        
    print(Na," > ", 0.2)
    if Na  < 0.2:
        chequeo = False
        
    print(fibra," > ", 25) 
    if fibra < 25:
        chequeo = False
        
    print(VF, ">=", 400)
    if VF < 400:
        chequeo = False
        
    return chequeo
