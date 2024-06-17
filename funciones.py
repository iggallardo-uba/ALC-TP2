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
consumidores_original = pd.read_csv('data/consumidores_libres.csv',sep=";",encoding='latin-1',skipinitialspace=True)
nutricional_original = pd.read_csv('data/tabla_nutricional.csv',sep=";",encoding='latin-1',skipinitialspace=True)

#Formateado de Dataframes
#Todas las filas en mayuscula
def Mayuscula(x): 
  if type(x)==str:
    res=x.upper()
  else:
    res=x
  return res

consumidores=consumidores_original.applymap(Mayuscula)
nutricional=nutricional_original.applymap(Mayuscula)

#Llenado de Ceros
consumidores=consumidores.fillna(0)
nutricional=nutricional.fillna(0)

#Cambio todos los datos en unidad de gramos
nutricional[['Na (mg)', 'Ca (mg)', 'Fe (mg)']] = nutricional[['Na (mg)', 'Ca (mg)', 'Fe (mg)']] / 1000
nutricional = nutricional.rename(columns={'Na (mg)': 'Na (gr)','Ca (mg)':'Ca (gr)','Fe (mg)':'Fe (gr)'})

#Agrego unidades a consumidores
consumidores = consumidores.rename(columns={'Cantidad': 'Cantidad (gr)','31/12/2023':'31/12/2023 ($)','31/1/2024':'31/1/2024 ($)',
                                            '29/2/2024':'29/2/2024 ($)','31/3/2024':'31/3/2024 ($)','30/4/2024':'30/4/2024 ($)'})

def tabla_nutricional():
    return nutricional

def tabla_consumidores():
    return consumidores

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
