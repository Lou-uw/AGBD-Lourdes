import pandas as pd
import seaborn as snb
import matplotlib.pyplot as plot

#Importando csv
df= pd.read_csv("diabetic_data.csv")

print("OKEY! archivo cargado correctamente")

filas,columnas= df.shape
print(f"La tabla contiene {filas} filas y {columnas} columnas")

filtro = df["gender"] == "Female"
df_filtrado = df[filtro]

print(df_filtrado.head())  # muestra las primeras filas
print(f"Hay {df_filtrado.shape[0]} mujeres")  # cuenta cuántas coincidencias

