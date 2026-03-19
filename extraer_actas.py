import os
import pandas as pd
import re

# 📁 Rutas dinámicas (funciona en PC y Jenkins)
base_dir = os.path.dirname(os.path.abspath(__file__))
carpeta = os.path.join(base_dir, "actas")

archivo_historial = os.path.join(base_dir, "historial_actas.xlsx")
archivo_reporte = os.path.join(base_dir, "reporte_actas.xlsx")
archivo_nuevas = os.path.join(base_dir, "nuevas_actas.xlsx")

datos = []

# 🔍 Leer archivos PDF
if not os.path.exists(carpeta):
    print(" La carpeta no existe:", carpeta)
    exit()

for archivo in os.listdir(carpeta):
    if archivo.lower().endswith(".pdf"):
        # Extraer número de acta (4 dígitos)
        acta = re.search(r'(\d{4})', archivo)

        # Extraer año (ej: 2026)
        anio = re.search(r'(20\d{2})', archivo)

        datos.append({
            "archivo": archivo,
            "acta": acta.group(1) if acta else "",
            "anio": anio.group(1) if anio else ""
        })

# 📊 Crear DataFrame
df_actual = pd.DataFrame(datos)

# 📄 Guardar reporte general en Excel
df_actual.to_excel(archivo_reporte, index=False)
print(" Reporte general generado:", archivo_reporte)

# 🔄 Detectar nuevas actas
if os.path.exists(archivo_historial):
    df_hist = pd.read_excel(archivo_historial)
    nuevas = df_actual[~df_actual["archivo"].isin(df_hist["archivo"])]
else:
    nuevas = df_actual

# 📄 Guardar nuevas actas
nuevas.to_excel(archivo_nuevas, index=False)
print(" Nuevas actas detectadas:", len(nuevas))

# 💾 Actualizar historial
df_actual.to_excel(archivo_historial, index=False)
print(" Historial actualizado")

print(" Proceso terminado correctamente")