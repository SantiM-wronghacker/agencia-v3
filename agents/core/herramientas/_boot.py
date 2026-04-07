import base64, os, sys, json, datetime, math, re, random

def main():
    if len(sys.argv) != 2:
        print("Uso: python _boot.py <data>")
        sys.exit(1)

    data = sys.argv[1].encode('utf-8')
    try:
        decoded = base64.b64decode(data)
        output = decoded.decode().splitlines()
        
        # Agregar encabezado
        output = [
            "AREA: HERRAMIENTAS",
            "DESCRIPCION: Boot",
            "TECNOLOGIA: Python"
        ]
        
        # Agregar datos si tiene menos de 20 lineas de output
        if len(output) < 20:
            output += [
                f"Total de lineas: {len(output)}",
                f"Fecha y hora: {datetime.datetime.now()}",
                f"Usuario que ejecuto el script: {os.getlogin()}",
                f"Nombre del sistema operativo: {os.name}",
                f"Versión del sistema operativo: {sys.version}",
                f"País: {os.name.split('-')[0]}",
                f"Nombre del host: {os.uname().nodename}",
                f"Versión del kernel: {os.uname().release}",
                f"Nombre del procesador: {os.uname().machine}",
                f"Memoria disponible: {os.sysconf_names['SC_AVPHYS_PAGES']} bytes",
                f"Memoria total: {os.sysconf_names['SC_PHYS_PAGES']} bytes",
                f"Memoria utilizada: {(os.sysconf_names['SC_PHYS_PAGES'] - os.sysconf_names['SC_AVPHYS_PAGES'])} bytes",
                f"CPU física: {os.cpu_count()}",
                f"CPU lógica: {os.cpu_count() * os.sched_getaffinity(0).nprocessors()}"
            ]
        else:
            output = [f"Linea {i+1}: {linea}" for i, linea in enumerate(output[:20])]
            output += [
                f"Total de lineas: {len(output)}",
                f"Fecha y hora: {datetime.datetime.now()}",
                f"Usuario que ejecuto el script: {os.getlogin()}",
                f"Nombre del sistema operativo: {os.name}",
                f"Versión del sistema operativo: {sys.version}",
                f"País: {os.name.split('-')[0]}",
                f"Nombre del host: {os.uname().nodename}",
                f"Versión del kernel: {os.uname().release}",
                f"Nombre del procesador: {os.uname().machine}",
                f"Memoria disponible: {os.sysconf_names['SC_AVPHYS_PAGES']} bytes",
                f"Memoria total: {os.sysconf_names['SC_PHYS_PAGES']} bytes",
                f"Memoria utilizada: {(os.sysconf_names['SC_PHYS_PAGES'] - os.sysconf_names['SC_AVPHYS_PAGES'])} bytes",
                f"CPU física: {os.cpu_count()}",
                f"CPU lógica: {os.cpu_count() * os.sched_getaffinity(0).nprocessors()}"
            ]
            output += [f"Linea {i+21}: {linea}" for i, linea in enumerate(output[20:])]
        
        # Agregar resumen ejecutivo al final del output
        output += [
            f"Resumen ejecutivo: El script se ejecutó correctamente y proporcionó información sobre el sistema operativo y el hardware.",
            f"Recomendaciones: Verificar la estabilidad del sistema operativo y asegurarse de que el hardware esté funcionando correctamente."
        ]
        
        # Imprimir el output
        for linea in output:
            print(linea)
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()