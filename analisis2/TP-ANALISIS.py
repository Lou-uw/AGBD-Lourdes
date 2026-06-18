import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#Importando csv
df= pd.read_csv("diabetic_data.csv")

print("OKEY! archivo cargado correctamente")

# Punto 1 - Total de filas y columnas

filas,columnas= df.shape
print(f"La tabla contiene {filas} filas y {columnas} columnas")

# Punto 2 - Filtrar por coincidencia exacta

print(f"Pacientes de sexo femenino")
filtro = df["gender"] == "Female"
df_filtrado = df[filtro]

print(df_filtrado.head())  # muestra las primeras filas
print(f"Hay {df_filtrado.shape[0]} mujeres")  # cuenta cuántas coincidencias

# Punto 3 - Filtro por texto parcial
print("\nFiltro parcial:")
df_raza= df[df["race"].str.startswith("A", na=False)]
total_registros = df_raza["race"].count()
print(df_raza.head())

print(f"Total de paises que empiezan con A:{total_registros}")

# Punto 4 - Selección de columnas clave

print("\nColumnas seleccionadas (Texto y Numérica):")
# Seleccionamos 'gender' (texto) y 'time_in_hospital' (numérica)
df_columnas_clave = df_filtrado[["gender", "time_in_hospital"]]

# Mostramos el resultado con .head() como pide el ejercicio
print(df_columnas_clave.head())

#Punto 5 - Agrupacion y resumen

resumen = df.groupby("gender")["time_in_hospital"].sum().sort_values(ascending=False)
print("\nResumen:")
print(resumen)

#Punto 6 - Estructura de Control Automatizada 

if (total := df_filtrado["time_in_hospital"].sum()) > 50000:
    print("\n Prioridad Alta")
else:
    print("\n Estado Normal")

print(f"Total acumulado: {total}")

#--------------- Graficos -----------------

# Punto 7 - Grafico de barras

plt.figure(figsize=(10, 5))

sns.barplot(
    data=df,
    x="age",
    y="time_in_hospital",
    estimator=sum,
    errorbar=None,
    palette="magma"
)

plt.title("Tiempo total de internación por edad")
plt.xlabel("Edad")
plt.ylabel("Tiempo en hospital")


plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("reporte_barras.png", dpi=300)
plt.close()

#Punto 8 - Grafico de torta

rangos_principales = resumen.nlargest(5)

plt.figure(figsize=(8, 8))

plt.pie(
    rangos_principales.values,
    labels=rangos_principales.index,
    autopct="%1.1f%%",
    wedgeprops={"edgecolor": "white"}
)

plt.title("Mayor tiempo de internacion según género")
plt.savefig("reporte_torta.png", dpi=300)
plt.close()
