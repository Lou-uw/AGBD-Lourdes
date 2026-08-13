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

filtro_avanzado = filtro & condicion_extra 

resultado_original = df.loc [filtro & condicion_extra, ["gender","patient_nbr","race"]]
print(resultado_original)
print(f"\nFilas seleccionadas:{len(resultado_original)}")


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

#Punto 11

# Paso 1 y 2: agrupar y ordenar
agrupado = df.groupby("gender")["time_in_hospital"].sum().sort_values()

#Paso 3: grafico de lineas
fig, ax = plt.subplots(figsize=(10,5))
ax.plot(agrupado.index, agrupado.values, marker="o",
        color="#2E75B6",linewidth=2,markersize=8)

#Paso 4: detectar y anotar el maximo 
idx_max = agrupado.idxmax()
val_max = agrupado.max()

ax.annotate(
    f"Maximo: {val_max:,.0f}",
    xy=(idx_max, val_max),
    xytext=(1,val_max * 0.85),
    arrowprops=dict(arrowstyle="->",color="red"),
    fontsize=11, color="red", fontweight="bold"
)
#Paso 5: configuracion final
ax.set_title("Evolucion por categoria",fontsize=14,fontweight="bold")
ax.set_xlabel("Categoria")
ax.set_ylabel("Total")
plt.xticks(rotation=45,ha="right")
plt.tight_layout()
plt.savefig("grafico_lineas.png", dpi=150)
plt.show()

#Preguntas punto 11
#¿La línea que generaron tiene un patrón claro (sube, baja, tiene picos)? ¿A qué lo atribuyen?
#¿Tiene sentido usar un gráfico de líneas para sus datos o hubiera sido mejor otro tipo?
#¿Qué pasa si usan agrupado.sort_index() en vez de sort_values()? ¿Cuál conviene?

# Punto 12 - .query() - filtros como texto

minimo_paciente = 8222157

# Filtro original
resultado_original = df.loc[
    filtro & condicion_extra,
    ["gender", "patient_nbr", "race"]
]

# Mismo filtro usando .query()
resultado_query = df.query(
    "patient_nbr > @minimo_paciente and gender == 'Female'"
)[["gender", "patient_nbr", "race"]]

print("Con corchetes:")
print(resultado_original)

print("\nCon .query():")
print(resultado_query)

print("\n¿Son iguales?", resultado_original.equals(resultado_query))
#Preguntas punto 12
#¿El resultado de .query() es idéntico al de su filtro_avanzado? ¿Por qué?
#¿Cuál de las dos formas les parece más clara para leer?
#¿Qué ventaja tiene usar @ en lugar de escribir el valor directamente en el texto?

#Punto 13 - .isin() y ~ — incluir y excluir categorías
print("PUNTO 13")
# Incluir categorías seleccionadas
categorias_elegidas = ['AfricanAmericna', 'Caucasian']   # sus valores reales
df_incluidos = df[df['race'].isin(categorias_elegidas)]
 
# Excluir esas mismas categorías
df_excluidos = df[~df['race'].isin(categorias_elegidas)]
 
print(f'Filas incluidas ({len(df_incluidos)}):')
print(df_incluidos)
print(f'\nFilas excluidas ({len(df_excluidos)}):')
print(df_excluidos)
 
# Verificar que suman el total
total = len(df)
suma  = len(df_incluidos) + len(df_excluidos)
print(f'\nTotal original: {total}  |  Incluidos + Excluidos: {suma}')
print(f'¿Coinciden? {total == suma}')

#Preguntas punto 13 

#¿La suma de filas incluidas + excluidas da exactamente el total? ¿Por qué siempre debería ser así?

#¿Qué ventaja tiene .isin(['A','B','C']) frente a escribir == 'A' | == 'B' | == 'C'?
#¿Cuándo usarían la versión con ~ en un análisis real?



#Punto 14 — .value_counts(), .unique() y .nunique()

# Sobre el DataFrame COMPLETO
print("\n=== DataFrame completo ===")

print("Conteo por categoría:")
print(df["gender"].value_counts())

print("Valores únicos:")
print(df["gender"].unique())

print("Cantidad de categorías:")
print(df["gender"].nunique())

print("Porcentajes:")
print((df["gender"].value_counts(normalize=True) * 100).round(1))

# Sobre el DataFrame FILTRADO
print("\n=== DataFrame filtrado ===")

df_filtrado = df[filtro_avanzado]

# Cuántas veces aparece cada categoría
print("Conteo por categoría:")
print(df_filtrado["gender"].value_counts())

# Qué valores únicos hay
print('\n Valores unicos:', df_filtrado["gender"].unique())

# Cuántos valores únicos hay (solo el número)
print('\n Cantidad de valores únicos:', df_filtrado["gender"].nunique())

# En porcentaje
print("\n Porcentaje:")
print((df_filtrado["gender"].value_counts(normalize=True) * 100).round(1))

#Preguntas punto 14

# ¿Cambia la distribución de categorías entre el DataFrame completo y el filtrado? ¿Qué dice eso?
#Si cambia porque con el dataframe filtrado al tener condiciones solo se toma una parte de este y 
# las demas se descartan, por lo que las cantidades y porcentajes de las categorias pueden cambiar.

# ¿Hay alguna categoría que desapareció completamente al aplicar el filtro?
#Hay dos, las de Male y Unknown/Invalid


# ¿value_counts() y groupby().count() dan el mismo resultado? ¿Cuándo usarían cada uno?
#value_counts() sirve para contar directamente cuántas veces 
#aparece cada categoría de una columna. groupby().count()también
#puede contar registros agrupándolos por una categoría,pero
#groupby() permite realizar análisis más complejos, como sumar o
#calcular promedios dentro de cada grupo. Por eso, para contar
#categorías usaría value_counts(), mientras que para hacer otros
#cálculos por grupo usaría groupby().


#Punto 15 — Exportar a CSV + Heatmap de correlación

import numpy as np

# Paso 1: exportar el DataFrame filtrado
df_filtrado = df[filtro_avanzado]
df_filtrado.to_csv("resultado_filtrado.csv", index=False)

print(f"Archivo exportado: {len(df_filtrado)} filas guardadas.")

# Paso 2: calcular la correlación del DataFrame COMPLETO
correlacion = df.corr(numeric_only=True)

print("\nMatriz de correlación:")
print(correlacion.round(2))

# Paso 3 y 4: crear y guardar el heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(
    correlacion,
    annot=True,
    fmt=".2f",
    cmap="YlGnBu",
    linewidths=0.5,
    vmin=-1,
    vmax=1
)
plt.title(
    "Correlación entre variables - Mi Dataset",
    fontweight="bold"
)
plt.tight_layout()
plt.savefig("heatmap_mi_dataset.png", dpi=150)
plt.show()


# Paso 5: identificar el par más y menos correlacionado
mask = np.triu(
    np.ones(correlacion.shape),
    k=0
).astype(bool)

correlacion_sin_diag = correlacion.where(~mask)

par_max = correlacion_sin_diag.stack().idxmax()
par_min = correlacion_sin_diag.stack().idxmin()

print(f"\nPar más correlacionado: {par_max[0]} ↔ {par_max[1]}")
print(f"Par menos correlacionado: {par_min[0]} ↔ {par_min[1]}")

#Preguntas punto 15

#¿Qué par de columnas tiene la correlación más alta? ¿Tiene sentido con sus datos?
#En nuestro dataset, el par de columnas con la correlación matemática más alta es encounter_id 
#y patient_nbr (0.51), aunque esto no tiene sentido clínico y solo responde al orden en que se 
#registraron los datos. Excluyendo los IDs, el par con mayor correlación es time_in_hospital 
#y num_medications (0.47), lo cual tiene un sentido médico, a más días de internación, mayor
#tiende a ser la cantidad de medicamentos administrados.

#¿Qué significa una correlación cercana a 1? ¿Y cercana a 0? ¿Y negativa?
#En cuanto a los valores, una correlación cercana a 1 indica que si una variable aumenta, la otra
#también lo hace (relación directa), cercana a 0 significa que no existe relación entre ellas y 
#negativa indica que si una sube, la otra baja (relación inversa).

#¿Por qué usamos el DataFrame completo para calcular la correlación y no el filtrado?
#Usamos el DataFrame completo en lugar de uno filtrado para tener una visión general de todos 
#los datos desde el principio y evitar sesgos o conclusiones falsas que podrían surgir al 
#recortar la muestra antes de tiempo.