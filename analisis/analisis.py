import pandas as pd

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