import scipy
import numpy as np
import pandas as pd
import seaborn as sns
import seaborn.objects as so
import matplotlib as mpl
import matplotlib.pyplot as plt
import datetime as dt
from sklearn import linear_model 


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
    if 'LECHE' in x and x!='DULCE DE LECHE' and x!="LECHE ENTERA EN POLVO":
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
    elif 'ASADO' in x and x != "TOMATE ENVASADO":
      return "ASADO"
  return x

consumidores_original=consumidores_original.map(Mayuscula)
nutricional_original=nutricional_original.map(Mayuscula)

consumidores_original=consumidores_original.map(sacar_acentos)
nutricional_original=nutricional_original.map(sacar_acentos)

#Llenado de Ceros
consumidores_original=consumidores_original.fillna(0)
nutricional_original=nutricional_original.fillna(0)

#Cambio todos los datos en unidad de gramos
nutricional_original[['Na (mg)', 'Ca (mg)', 'Fe (mg)']] = nutricional_original[['Na (mg)', 'Ca (mg)', 'Fe (mg)']] / 1000
nutricional_original = nutricional_original.rename(columns={'Na (mg)': 'Na (gr)','Ca (mg)':'Ca (gr)','Fe (mg)':'Fe (gr)'})

#Agregado de Verduras/Frutas
#codigo binario 1= verdura o fruta y 0 no lo es
FrutasyVerduras=['ACELGA','ZANAHORIA','TOMATE','LECHUGA','CEBOLLA','ZAPALLO','MANZANA','NARANJA','MANDARINA','PERA','BANANA','PAPA','BATATA']
Verdura_fruta= []

for index, fila in nutricional_original.iterrows():
    if fila['Alimento'] in FrutasyVerduras:
        Verdura_fruta.append(1)
    else:
        Verdura_fruta.append(0)

# Agregamos la columna 'Verdura/Fruta' al DataFrame
nutricional_original['Verdura/Fruta'] = Verdura_fruta


#Agrego unidades a consumidores
consumidores_original = consumidores_original.rename(columns={'Cantidad': 'Cantidad (gr)'})

def tabla_nutricional():
    return nutricional_original

def tabla_consumidores():
    return consumidores_original

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
    #print("HC")
    #print(minHC, HC, maxHC) 
    if minHC > HC or HC > maxHC:
        chequeo = False
        print("Los Hidratos de Carbono no cumplen los estandares de la OMS")
        
    #print("Proteina")
    #print(minProteina, proteina, maxProteina) 
    if minProteina > proteina or proteina > maxProteina:
        chequeo = False
        print("Las Proteinas no cumplen los estandares de la OMS")
        
    #print("Grasas")
    #print(minGrasas, grasas, maxGrasas) 
    if minGrasas > grasas or grasas > maxGrasas:
        chequeo = False
        print("Las Grasas no cumplen los estandares de la OMS")

        
    #print("Sodio")
    #print(Na," > ", 0.2)
    if Na  < 0.2:
        chequeo = False
        print("El Sodio no cumple los estandares de la OMS")
        
        
    #print("Fibra")
    #print(fibra," > ", 25) 
    if fibra < 25:
        chequeo = False
        print("La Fibra no cumple los estandares de la OMS")

    #print("Fruta y Verduras")
    #print(VF, ">=", 400)
    if VF < 400:
        chequeo = False
        print("La cantidad de Frutas y Verduras no cumple los estandares de la OMS")
        
    return chequeo

def graficosPCA(data):
  display(
  so.Plot()
  .add(so.Dot(), data=data, x="Z1", y="Z2")
  )
  display(
  so.Plot()
  .add(so.Dot(), data=data, x="Z2", y="Z3")
  )
  display(
  so.Plot()
  .add(so.Dot(), data=data, x="Z1", y="Z3")
  )
  

def graficosNutricionales(data):
  #HC
  HC__Nutricional = data[data["HC (gr)"] > 0].drop(columns=["Proteinas (gr)", "Grasas (gr)"]).reset_index(drop=True)

  HC__Nutricional["Precio por gr ($)"] = HC__Nutricional["Precio por gr ($)"] / HC__Nutricional["HC (gr)"]

  HC__Nutricional = HC__Nutricional.rename(columns={"Precio por gr ($)":"Precio por gr de HC ($)"})

  #Proteina
  Pr__Nutricional = data[data["Proteinas (gr)"] > 0].drop(columns=["HC (gr)", "Grasas (gr)"]).reset_index(drop=True)

  Pr__Nutricional["Precio por gr ($)"] = Pr__Nutricional["Precio por gr ($)"] / Pr__Nutricional["Proteinas (gr)"]

  Pr__Nutricional = Pr__Nutricional.rename(columns={"Precio por gr ($)":"Precio por gr de Proteinas ($)"})

  #Grasas
  Gr__Nutricional = data[data["Grasas (gr)"] > 0].drop(columns=["HC (gr)", "Proteinas (gr)"]).reset_index(drop=True)

  Gr__Nutricional["Precio por gr ($)"] = Gr__Nutricional["Precio por gr ($)"] / Gr__Nutricional["Grasas (gr)"]

  Gr__Nutricional = Gr__Nutricional.rename(columns={"Precio por gr ($)":"Precio por gr de Grasas ($)"})

  display(
    so.Plot(data=data, x="Fecha", y="Precio por gr ($)", color="Alimento")
    .add(so.Dot())
    .add(so.Line(linewidth=1), so.PolyFit(1))
  )
  if len(Pr__Nutricional) !=0:
    display(
      so.Plot(data=Pr__Nutricional, x="Fecha", y="Precio por gr de Proteinas ($)", color="Alimento")
      .add(so.Dot())
      .add(so.Line(linewidth=1), so.PolyFit(1))
    )
  else:
     print("Los Alimentos seleccionados no tienen Proteinas")
  if len(HC__Nutricional) != 0:
    display(
      so.Plot(data=HC__Nutricional, x="Fecha", y="Precio por gr de HC ($)", color="Alimento")
      .add(so.Dot())
      .add(so.Line(linewidth=1), so.PolyFit(1))
    )
  else:
     print("Los Alimentos seleccionados no tienen Hidratos de Carbono (HC)")
  if len(Gr__Nutricional) != 0:
    display(
      so.Plot(Gr__Nutricional, x="Fecha", y="Precio por gr de Grasas ($)", color="Alimento")
      .add(so.Dot())
      .add(so.Line(linewidth=1), so.PolyFit(1))
    )
  else:
     print("Los Alimentos seleccionados no tienen Grasas (Gr)")

def comparacionAumentos(data):
  predicion = pd.DataFrame(columns=["Rubro","Fecha", "Precio por gr ($)"])

  data['Fecha'] = pd.to_datetime(data['Fecha'], format="%d/%m/%Y")
  data['Fecha']=data['Fecha'].map(dt.datetime.toordinal)
  fechas = data["Fecha"].unique()

  # Dataframes Derivados
  carne_nutricional = data[data["Alimento"].isin(["CARNE PICADA", "BOLA DE LOMO", "ASADO", "PALETA"])].reset_index(drop=True)
  VF_nutricional = data[data["Alimento"].isin(["TOMATE", "PAPA", "ACELGA", "ZANAHORIA","MANZANA" ,"NARANJA", "CEBOLLA"])].reset_index(drop=True)
  almacen_nutricional = data[~data["Alimento"].isin(["TOMATE", "PAPA", "ACELGA", "ZANAHORIA","MANZANA" ,"NARANJA", "CEBOLLA","CARNE PICADA", "BOLA DE LOMO", "ASADO", "PALETA"])].reset_index(drop=True)

  # Inicializamos un modelo de Regresion Lineal
  modelo = linear_model.LinearRegression()
  
  for j in range(0,4):
    if j == 0:
      precio = "Precio por gr ($)"
      nutriente = ""
    if j == 1:
      precio = "Precio por gr de HC ($)"
      nutriente = "HC (gr)"
      excluidos = ["Proteinas (gr)", "Grasas (gr)"]
    if j == 2:
      precio = "Precio por gr de Proteinas ($)"
      nutriente = "Proteinas (gr)"
      excluidos = ["HC (gr)", "Grasas (gr)"]
    if j == 3:
      precio = "Precio por gr de Grasas ($)"
      nutriente = "Grasas (gr)"
      excluidos = ["Proteinas (gr)", "HC (gr)"]
  
    predicion = pd.DataFrame(columns=["Rubro","Fecha", precio])
    
    if j == 0:
      for i in range(0,4):
        if i == 0:
          data_analizar = data
          rubro = "Todos"
        if i == 1:
          data_analizar = carne_nutricional
          rubro = "Carnes"
        if i == 2:
          data_analizar = VF_nutricional
          rubro = "Frutas y Verduras"
        if i == 3:
          data_analizar = almacen_nutricional
          rubro = "Almacen"
      
        #Calculo de Minimos Cuadrados
        modelo.fit(data_analizar[['Fecha']], data_analizar[[precio]])
        
        #Coeficientes
        beta_1 = modelo.coef_[0][0]   # Con .coef_ recuperamos el valor de beta_1 (dentro de un array)
        beta_0 = modelo.intercept_[0]   # Con .intercept_ recuperamos el valor de beta_0 (dentro de  un array)

        for fecha in fechas:
          predicion.loc[len(predicion.index)] = [rubro,dt.date.fromordinal(fecha), beta_1*fecha+beta_0] 

      display(
        so.Plot(data=predicion, x="Fecha", y=precio, color="Rubro")
        .add(so.Line(linewidth=2), so.PolyFit(1))
      )
      
    if j > 0:
      for i in range(0,4):
        if i == 0:
          data_analizar = data
          rubro = "Todos"
        if i == 1:
          data_analizar = carne_nutricional
          rubro = "Carnes"
        if i == 2:
          data_analizar = VF_nutricional
          rubro = "Frutas y Verduras"
        if i == 3:
          data_analizar = almacen_nutricional
          rubro = "Almacen"
        
        HC__Nutricional = data_analizar[data_analizar[nutriente] > 0].drop(columns=excluidos).reset_index(drop=True)

        if len(HC__Nutricional) == 0:
          continue

        HC__Nutricional["Precio por gr ($)"] = HC__Nutricional["Precio por gr ($)"] / HC__Nutricional[nutriente]

        HC__Nutricional = HC__Nutricional.rename(columns={"Precio por gr ($)":precio})
        
        #Calculo de Minimos Cuadrados
        modelo.fit(HC__Nutricional[['Fecha']], HC__Nutricional[[precio]])
        
        #Coeficientes
        beta_1 = modelo.coef_[0][0]   # Con .coef_ recuperamos el valor de beta_1 (dentro de un array)
        beta_0 = modelo.intercept_[0]   # Con .intercept_ recuperamos el valor de beta_0 (dentro de  un array)

        for fecha in fechas:
          predicion.loc[len(predicion.index)] = [rubro,dt.date.fromordinal(fecha), beta_1*fecha+beta_0] 
        
      display(
        so.Plot(data=predicion, x="Fecha", y=precio, color="Rubro")
        .add(so.Line(linewidth=2), so.PolyFit(1))
      )
    

