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

#Punto 9 ---Filtro Avanzado con .loc[] — Doble Condición y Selección Simultánea

#Reutilizar el filtro que tenemos y agregar una condicion más
condicion_extra = df["patient_nbr"] > 8222157

resultado = df.loc [filtro & condicion_extra, [
    "gender","patient_nbr","race"
]
]
print(resultado)
print(f"\nFilas seleccionadas:{len(resultado)}")

#Lo que deben observar y anotar
# ¿Cuántas filas quedaron después de aplicar el doble filtro?
#  Quedaron 46308 filas despues de aplicar el doble filtro

# ¿El resultado con .loc[] es igual al que hubieran obtenido en dos pasos separados?
#  Si, el resultado seria el mismo, pero al usar .loc[] se hace mas rapido y eficiente, en un solo paso.

# ¿Qué pasa si cambian & por | en el filtro? ¿Tiene sentido para sus datos?
#  No lo tendria porque ya no tendria dos condiciones, seria aunque una o la otra se cumpla 
#  y me traeria muchos datos no útiles para lo que quiero en este caso.



#Punto 10 -- Detección y Manejo de Valores Nulos
 # Paso 1: diagnóstico
print('Nulos por columna:')
print(df.isnull().sum())

# Paso 2: introducir nulos si no hay (para practicar)
#Aunque ya tenia columnas con nulos, no eran numericas por lo que no me funcionaria el media, entonces
#agregué nulos en una numerica igual.
df_con_nulos = df.copy()
df_con_nulos.loc[[0, 3, 7], 'time_in_hospital'] = None
 
# Paso 3: confirmar
print('\nNulos después de modificar:')
print(df_con_nulos.isnull().sum())
 
# Paso 4a: eliminar filas con nulos
df_sin_nulos = df_con_nulos.dropna()
 
# Paso 4b: reemplazar nulos con la media
media = df_con_nulos['time_in_hospital'].mean()
df_rellenado = df_con_nulos.fillna({'time_in_hospital': round(media, 2)})
 
# Paso 5: comparar
print(f'\nOriginal:   {len(df_con_nulos)} filas')
print(f'Con dropna: {len(df_sin_nulos)} filas  (se eliminaron filas)')
print(f'Con fillna: {len(df_rellenado)} filas  (se rellenaron los huecos)')

print(df_rellenado["time_in_hospital"].head(10))

#Para pensar y responder en la entrega

# ¿Cuál de las dos estrategias (dropna o fillna) es más conveniente para sus datos? ¿Por qué?
#  Para estos datos la estrategia mas conveniente seria fillna, porque borrar una columna completa 
#  con dropna podria afectar mucho la informacion del dataset al ser registros médicos, en cambio rellenar los vacios con la media nos permite 
#  conservarlo sin alterar tanto la columna.

# ¿Qué problema puede generar fillna con la media si los nulos son muchos?
#  Se perderian los datos originales y serian muchos datos inventados, por lo tanto informacion falsa.
#  en este caso, si un paciente no estuvo 3 dias en el hospital y ponemos fillna, se le agregarian dias 
#  que no estuvo

# ¿Cambiaría algo en sus análisis anteriores si hubiera nulos reales en sus datos?
#  Si, cambiaria porque faltarian datosAl haber nulos reales, las barras de el gráfico quedarían 
# más bajas de lo que deberían porque ignoraría esos huecos vacíos al sumar. Además, el
#  if recibiría una suma total de días menor a la real, haciendo que dé
# un diagnóstico no correcto de "Estado Normal" cuando en verdad correspondía 
# una "Prioridad Alta".



