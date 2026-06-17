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

# Punto 3 - Filtro por texto parcial

df_parcial = df[df["age"].str.startswith("7", na=False)]

print("\nFiltro parcial:")
print(df_parcial.head())

# Punto 4 - Selección de columnas clave

print("\nColumnas seleccionadas:")
print(df_parcial[["age", "time_in_hospital"]].head())

#Punto 5 

resumen = df.groupby("age")["time_in_hospital"].sum().sort_values(ascending=False)
print("\nResumen:")
print(resumen)

#Punto 6

if (total := df_parcial["time_in_hospital"].sum()) > 50000:
    print("\n Prioridad Alta")
else:
    print("\n Estado Normal")

print(f"Total acumulado: {total}")

# Punto 7 - Grafico de barras

plt.figure(figsize=(10, 5))

sns.barplot(
    data=df,
    x="age",
    y="time_in_hospital",
    estimator=sum,
    errorbar=None,
    palette="viridis"
)

plt.title("Tiempo total de internación por rango etario")
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

plt.title("Top 5 rangos etarios por tiempo de internación")
plt.savefig("reporte_torta.png", dpi=300)
plt.close()
