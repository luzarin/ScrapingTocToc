import pandas as pd
import glob

# Ruta de la carpeta
carpeta = "C:\Repos\Scrape Toc Toc Propiedades"

# Unificar archivos CSV
print("=== PASO 1: Unificando archivos CSV ===")
archivos = glob.glob(f"{carpeta}/*.csv")
dataframes = [pd.read_csv(archivo) for archivo in archivos]
df = pd.concat(dataframes, ignore_index=True)
print(f"✓ {len(df)} registros unificados")

# Crear columna SUP TOTAL
print("\n=== PASO 2: Creando columna SUP TOTAL ===")
df['SUP TOTAL'] = df[['SUP TERRENO2', 'SUP UTIL2', 'SUP CONSTRUIDA2']].max(axis=1)
print(f"✓ Columna SUP TOTAL creada")

# Eliminar duplicados
print("\n=== PASO 3: Eliminando duplicados ===")
print(f"Registros antes: {len(df)}")
print(f"Nombre de columna URL: {df.columns[40]}")
df = df.drop_duplicates(subset=[df.columns[40]], keep='first')
print(f"Registros después: {len(df)}")

# Guardar 
df.to_csv(f"{carpeta}/prop_unificadas_final.csv", index=False)
print(f"\n✓ Proceso completo. Archivo guardado: prop_unificadas_final.csv")