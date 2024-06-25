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

#Sacar Acentos 
def sacar_acentos(x):
    reemplazar = (('Á','A'),('É','E'),('Í','I'),('Ó','O'),('Ú','U'))
    if type(x)==str:
      for (i,j) in reemplazar:
          x = x.replace(i,j)
    return x

#Arreglo para el punto 4
def arreglo_observacional(x):
  if type(x)==str:
    if 'LECHE' in x and (x!='DULCE DE LECHE' or x!="LECHE ENTERA EN POLVO"):
      return "LECHE"
    elif 'ACEITE'  in x:
      return "ACEITE"
    elif 'ARROZ'  in x:
      return "ARROZ"
    elif 'AZUCAR'  in x:
      return "AZUCAR"
    elif 'FIDEOS'  in x:
      return "FIDEOS"
    elif 'HARINA'  in x and 'TRIGO' in x:
      return "HARINA DE TRIGO"
    elif 'HUEVO'  in x:
      return "HUEVO"
    elif 'PAN'  in x:
      return "PAN"
    elif 'YERBA'  in x:
      return "YERBA"
    elif 'TOMATE'  in x and x!="TOMATE ENVASADO":
      return "TOMATE"
    elif 'PAPA'  in x:
      return "PAPA"
    elif 'ACELGA'  in x:
      return "ACELGA"
    elif 'ZANAHORIA'  in x:
      return "ZANAHORIA"
    elif 'BERENJENA'  in x:
      return "BERENJENA"
    elif 'NARANJA'  in x:
      return "NARANJA"
    elif 'MANZANA' in x:
      return "MANZANA"
    elif 'CEBOLLA' in x:
      return "CEBOLLA"
    elif 'CARNE PICADA' in x:
      return "CARNE PICADA"
    elif 'PALETA' in x and x!="PALETA COCIDA":
      return "PALETA"
    elif 'BOLA DE LOMO' in x:
      return "BOLA DE LOMO"
    elif 'ASADO' in x:
      return "ASADO"
  return x

consumidores=consumidores_original.applymap(Mayuscula)
nutricional=nutricional_original.applymap(Mayuscula)

consumidores=consumidores.applymap(sacar_acentos)
nutricional=nutricional.applymap(sacar_acentos)

#Llenado de Ceros
consumidores=consumidores.fillna(0)
nutricional=nutricional.fillna(0)

#Cambio todos los datos en unidad de gramos
nutricional[['Na (mg)', 'Ca (mg)', 'Fe (mg)']] = nutricional[['Na (mg)', 'Ca (mg)', 'Fe (mg)']] / 1000
nutricional = nutricional.rename(columns={'Na (mg)': 'Na (gr)','Ca (mg)':'Ca (gr)','Fe (mg)':'Fe (gr)'})

#Agregado de Verduras/Frutas
#codigo binario 1= verdura o fruta y 0 no lo es
FrutasyVerduras=['ACELGA','ZANAHORIA','TOMATE','LECHUGA','CEBOLLA','ZAPALLO','MANZANA','NARANJA','MANDARINA','PERA','BANANA','PAPA','BATATA']
Verdura_fruta= []

for index, fila in nutricional.iterrows():
    if fila['Alimento'] in FrutasyVerduras:
        Verdura_fruta.append(1)
    else:
        Verdura_fruta.append(0)

# Agregamos la columna 'Verdura/Fruta' al DataFrame
nutricional['Verdura/Fruta'] = Verdura_fruta


#Agrego unidades a consumidores
consumidores = consumidores.rename(columns={'Cantidad': 'Cantidad (gr)'})

def tabla_nutricional():
    return nutricional

def tabla_consumidores():
    return consumidores

def chequeoDieta(data):
    chequeo = True
    
    #Frutas y Verduras
    data_VF = data[data["Verdura/Fruta"] == 1]

    data_Suma = data.drop(columns=["Alimento",	"Cantidad (gr/ml)","Verdura/Fruta"])
    suma = 0

    for col in data_Suma:
      suma += sum(data_Suma[col])

    #Cantidad Total
    cantidadTotal = suma
    
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
    print("HC")
    print(minHC, HC, maxHC) 
    if minHC > HC or HC > maxHC:
        chequeo = False
        print("False")
        
    print()
    print("Proteina")
    print(minProteina, proteina, maxProteina) 
    if minProteina > proteina or proteina > maxProteina:
        chequeo = False
        print("False")
        
    print()
    print("Grasas")
    print(minGrasas, grasas, maxGrasas) 
    if minGrasas > grasas or grasas > maxGrasas:
        chequeo = False
        print("False")
        
    print()
    print("Sodio")
    print(Na," > ", 0.2)
    if Na  < 0.2:
        chequeo = False
        print("False")
        
        
    print()
    print("Fibra")
    print(fibra," > ", 25) 
    if fibra < 25:
        chequeo = False
        print("False")
        
    print()
    print("Fruta y Verduras")
    print(VF, ">=", 400)
    if VF < 400:
        chequeo = False
        print("False")
        
    return chequeo
