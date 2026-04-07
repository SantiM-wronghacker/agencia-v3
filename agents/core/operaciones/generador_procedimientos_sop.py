"""
ÁREA: OPERACIONES
DESCRIPCIÓN: Agente que realiza generador procedimientos sop
TECNOLOGÍA: Python estándar
"""

import sys
import os
import json
import random
from datetime import datetime, timedelta

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Configuración por defecto
        dias = 30
        clientes = 10
        monto_min = 500
        monto_max = 5000

        # Procesar argumentos
        if len(sys.argv) > 1:
            dias = int(sys.argv[1])
        if len(sys.argv) > 2:
            clientes = int(sys.argv[2])
        if len(sys.argv) > 3:
            monto_min = int(sys.argv[3])
        if len(sys.argv) > 4:
            monto_max = int(sys.argv[4])

        # Validar argumentos
        if dias < 1:
            raise ValueError("El número de días debe ser mayor que 0")
        if clientes < 1:
            raise ValueError("El número de clientes debe ser mayor que 0")
        if monto_min < 0:
            raise ValueError("El monto mínimo no puede ser negativo")
        if monto_max < monto_min:
            raise ValueError("El monto máximo debe ser mayor que el monto mínimo")

        # Generar datos de procedimientos
        procedimientos = []
        for i in range(clientes):
            fecha = (datetime.now() - timedelta(days=random.randint(0, dias))).strftime('%Y-%m-%d')
            monto = round(random.uniform(monto_min, monto_max), 2)
            procedimientos.append({
                "id": f"PROC-{i+1:04d}",
                "fecha": fecha,
                "cliente": f"CLIENTE-{i+1:03d}",
                "monto": monto,
                "status": random.choice(["PENDIENTE", "APROBADO", "RECHAZADO"])
            })

        # Guardar en archivo JSON
        output_file = "procedimientos_sop.json"
        with open(output_file, 'w') as f:
            json.dump(procedimientos, f, indent=4)

        # Mostrar resumen
        print(f"Generador de procedimientos SOP - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Clientes procesados: {clientes}")
        print(f"Rango de fechas: últimos {dias} días")
        print(f"Montos generados: entre ${monto_min:,.2f} y ${monto_max:,.2f} MXN")
        print(f"Archivo generado: {os.path.abspath(output_file)}")
        print("Procedimientos generados:")
        for proc in procedimientos[:5]:  # Mostrar 5 ejemplos
            print(f"  {proc['id']}: {proc['cliente']} - ${proc['monto']:,.2f} ({proc['status']})")
        print(f"Total de procedimientos: {len(procedimientos)}")
        print(f"Monto total: ${sum(proc['monto'] for proc in procedimientos):,.2f}")
        print(f"Promedio de monto: ${sum(proc['monto'] for proc in procedimientos) / len(procedimientos):,.2f}")
        print("Resumen ejecutivo:")
        print(f"  * Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  * Número de clientes: {clientes}")
        print(f"  * Rango de fechas: últimos {dias} días")
        print(f"  * Monto total: ${sum(proc['monto'] for proc in procedimientos):,.2f}")

    except ValueError as e:
        print(f"Error de valor: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()