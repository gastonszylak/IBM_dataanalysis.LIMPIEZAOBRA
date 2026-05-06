import pandas as pd
import numpy as np
import io

df= pd.read_csv("datos_obras.csv")
print(df.info())
print(df.head(5))

#LIMPIEZA DE NULOS
df.replace("?", np.nan , inplace=True)
df["costo_materiales"] = df["costo_materiales"].astype("float")

df["metros_cuadrados"].replace(np.nan, df["metros_cuadrados"].mean(), inplace=True)
df["costo_materiales"].replace(np.nan, df["costo_materiales"].mean, inplace=True)
df["calificacion_cliente"].replace(np.nan, df["calificacion_cliente"].median(), inplace=True)

#FORMATO DE PRECIOS
df["precio_cobrado"] = df["precio_cobrado"].str.replace("$","",regex=False)
df["precio_cobrado"] = df["precio_cobrado"].astype("float")

print("---DATOS LIMPIOS---")
print(df[["id_obra", "metros_cuadrados" , "costo_materiales", "precio_cobrado" ,"calificacion_cliente"]])
#VARIABLES INDICADORAS 

print("\nOne-Hot encoding a tipo de pintura")
dummies_pintura = pd.get_dummies(df["tipo_pintura"])

#RENOMBRAMOS
dummies_pintura.rename(columns={
    "Epoxi" : "pintura_Epoxi",
    "Latex" : "pintura_Latex",
    "Sientetico" : "pintura_sintetico",

}, inplace=True)

# 3. Concatenamos (unimos) estas columnas al DataFrame original y borramos la de texto
df = pd.concat([df, dummies_pintura], axis=1)
df.drop("tipo_pintura", axis=1 , inplace=True)

#BINNING
print("Binning en metros cuadrados")
bins = np.linspace(min(df["metros_cuadrados"]), max(df["metros_cuadrados"]), 4)
#NOMBRES DE CAJONES
nombres_grupos = ["chica", "mediana", "grande"]
df['tamaño_obra'] = pd.cut(df['metros_cuadrados'], bins, labels=nombres_grupos, include_lowest=True)

#NORMALIZACION DE PRECIOS

# ==========================================
# FASE 5: NORMALIZACIÓN (Nivelamos los precios)
# ==========================================
print("Aplicando Fase 5...")

# Primero nos aseguramos que 'precio_cobrado' sea float (por las dudas)
df['precio_cobrado'] = df['precio_cobrado'].astype(float)

# Hacemos la cuenta y creamos la columna con un nombre CORTO para evitar errores
df['precio_norm'] = (df['precio_cobrado'] - df['precio_cobrado'].min()) / (df['precio_cobrado'].max() - df['precio_cobrado'].min())


# ==========================================
# ÚLTIMO PASO: VERIFICACIÓN Y PRINT
# ==========================================
print("\n--- REVISIÓN DE COLUMNAS DISPONIBLES ---")
print(df.columns.tolist()) 

print("\n--- TABLA FINAL DE LA CUADRILLA ---")
cols_a_mostrar = ['id_obra', 'pintor_asignado', 'precio_cobrado', 'precio_norm']

for col in df.columns:
    if 'pintura' in col or 'tamaño' in col:
        cols_a_mostrar.append(col)

print(df[cols_a_mostrar])


                   






