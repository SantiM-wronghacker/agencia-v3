"""
AREA: HERRAMIENTAS
DESCRIPCION: Mueve archivos .bak que tienen más de 24 horas a la carpeta 'Historico'.
TECNOLOGIA: Python, os, shutil, datetime
"""

import os
import shutil
import datetime
import sys
import math

def mover_archivos_antiguos(ruta_actual, horas_limite=24):
    try:
        ruta_historico = os.path.join(ruta_actual, 'Historico')
        if not os.path.exists(ruta_historico):
            os.makedirs(ruta_historico)
            print(f"Se creó la carpeta {ruta_historico} porque no existía.")

        archivos_bak = glob.glob(os.path.join(ruta_actual, '*.bak'))
        print(f"Se encontraron {len(archivos_bak)} archivos .bak en {ruta_actual}.")

        archivos_movidose = 0
        archivos_no_movidose = 0

        for archivo in archivos_bak:
            fecha_creacion = datetime.datetime.fromtimestamp(os.path.getctime(archivo))
            diferencia = datetime.datetime.now() - fecha_creacion
            diferencia_horas = diferencia.total_seconds() / 3600

            if diferencia > datetime.timedelta(hours=horas_limite):
                nombre_archivo = os.path.basename(archivo)
                ruta_nueva = os.path.join(ruta_historico, nombre_archivo)
                shutil.move(archivo, ruta_nueva)
                print(f"Archivo {nombre_archivo} movido a {ruta_historico} porque tiene {diferencia_horas:.2f} horas de antigüedad.")
                archivos_movidose += 1
            else:
                print(f"Archivo {nombre_archivo} no se movió porque tiene {diferencia_horas:.2f} horas de antigüedad, que es menos de {horas_limite} horas.")
                archivos_no_movidose += 1

        print(f"Se movieron {archivos_movidose} archivos a {ruta_historico}.")
        print(f"Quedan {archivos_no_movidose} archivos .bak en {ruta_actual}.")
        print(f"Total de archivos .bak en {ruta_actual}: {len(glob.glob(os.path.join(ruta_actual, '*.bak')))}")
        print(f"Total de archivos .bak en {ruta_historico}: {len(glob.glob(os.path.join(ruta_historico, '*.bak')))}")
        print(f"Tamaño total de archivos .bak en {ruta_actual}: {sum(os.path.getsize(archivo) for archivo in glob.glob(os.path.join(ruta_actual, '*.bak')))/1024:.2f} KB")
        print(f"Tamaño total de archivos .bak en {ruta_historico}: {sum(os.path.getsize(archivo) for archivo in glob.glob(os.path.join(ruta_historico, '*.bak')))/1024:.2f} KB")

        print(f"Resumen ejecutivo:")
        print(f"- Se movieron {archivos_movidose} archivos .bak a la carpeta {ruta_historico}.")
        print(f"- Quedan {archivos_no_movidose} archivos .bak en la carpeta {ruta_actual}.")
        print(f"- El tamaño total de archivos .bak en la carpeta {ruta_actual} es de {sum(os.path.getsize(archivo) for archivo in glob.glob(os.path.join(ruta_actual, '*.bak')))/1024:.2f} KB.")
        print(f"- El tamaño total de archivos .bak en la carpeta {ruta_historico} es de {sum(os.path.getsize(archivo) for archivo in glob.glob(os.path.join(ruta_historico, '*.bak')))/1024:.2f} KB.")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ruta_actual = sys.argv[1]
    else:
        ruta_actual = os.getcwd()

    if len(sys.argv) > 2:
        horas_limite = int(sys.argv[2])
    else:
        horas_limite = 24

    mover_archivos_antiguos(ruta_actual, horas_limite)