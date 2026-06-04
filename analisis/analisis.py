import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#Importando csv
df= pd.read_csv("01_semiconductor_trade_flows.csv")

print("OKEY! archivo cargado correctamente")

#Mostrando las primeras columnas
print(df.head())

#Cuenta el total de filas y columnas que tiene mi archivo
filas,columnas= df.shape
print(f"el dataframe tiene {filas} filas y {columnas} columnas")

#Cuenta el total de fila con años
total_anios = df["year"].count()
print(f"Cantidad de filas con año valido: {total_anios}")

#df es dataframe 

print("-----Analis avanzado de datos-----")

#filtro_avanzado = df["nombre de la columna"]

filtro_avanzado = df["hardware_type"].str.startswith("Advance", na = False)
df_filtrado = df[filtro_avanzado]

total_registros = df_filtrado["hardware_type"].count()
print(f"Cantidad de enviso de tecnologia 'Advance': {total_registros}")

suma_dinero = df_filtrado ["trade_value_usd_millions"].sum()
#print(f"Valor total de este comercio: USD{suma_dinero: 2f} millones ")
#2f es los centecimos que quiero mostrar, si no lo pongo lo deja entero

print("--Reporte Automatizado--")

print(f"Monto total: USD {suma_dinero: .2f} millones")

if Default_limite_alto:= (suma_dinero>500):
    print("Alerta: el volumen de mercado es Ciritico y de alta prioridad")
    print("Requiere revision inmediata")

elif suma_dinero > 200:
    print("Aviso: volumen mercado moderado/alto")
    print("Monitorear comportamiento proximo trimestre")

else: 
    print("Estado: volumen de mercado bajo o dentro del parametro")
    print("No se requiere accion adicional")


#-----------------------------------
#GRAFICO 1: Grafico de barras(con Seaborn)
#-----------------------------------

print("\n Generando Grafico de barras")

#configura el estilo de la grilla
sns.set_theme(style="whitegrid")

#determina el tamaño de la figura(en este caso barra)
plt.figure(figsize=(9,5))

#Defino lo que se va a mostrar en el grafico
sns.barplot(
    data=df, 
    x="hardware_type",
    y="trade_value_usd_millions",
    estimator=sum,
    errorbar=None,
    palette="magma",#variacion de colores
    )
plt.title("Distribucion economica de tecnologia avanzada",fontsize=14)
plt.xlabel("Tipo de hardware", fontsize=11)#Nombre del eje x
plt.ylabel("Total(millones USD)", fontsize=11)#Nombre del eje y

plt.tight_layout()
#Rota y cambia el tamaño de las palabras en el eje x
plt.xticks(rotation=20, fontsize=7)
plt.savefig("grafico_barras.png", dpi= 250)
plt.close()
print("Grafico de barras guardado correctamente")

#-----------------------------------
#GRAFICO 2: Grafico de tortas(con Seaborn)
#-----------------------------------

print("\n Generando ")

datos_torta =(
   df.groupby("hardware_type")["trade_value_usd_millions"]
   .sum()
   .nlargest(5)
)

plt.figure(figsize=(7,7))
plt.pie(
    datos_torta,
    labels=datos_torta.index,
    autopct="%1.1f%%",
    colors=sns.color_palette("Set2")[0:5],
    startangle=140,
    wedgeprops={"edgecolor":"white","linewidth": 2}
)
plt.title("Distribucion interna: Tecnologia Avanzada",fontsize=15)
plt.savefig("grafico_tortas.png", dpi= 250)
plt.close()
print("Grafico de tortas guardado correctamente")

#-----------------------------------
#GRAFICO 3: Grafico de
#-----------------------------------
