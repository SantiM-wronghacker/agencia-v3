"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que genera reportes CSV con datos simulados de transacciones
TECNOLOGÍA: Python estándar (stdlib)
"""

import sys
import csv
import random
from datetime import datetime
import math

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

# Datos realistas para México
PRODUCTOS = ["Servicio de Consultoría", "Soporte Técnico", "Capacitación", "Desarrollo de Software", "Mantenimiento"]
ESTADOS = ["Pendiente", "En Proceso", "Completado", "Cancelado", "Reembolsado"]
CLIENTES = ["Empresarial", "Gobierno", "PYME", "Individual"]
METODOS_PAGO = ["Transferencia", "Tarjeta", "Efectivo", "PayPal"]

def generar_datos_aleatorios(num_registros):
    datos = []
    for i in range(1, num_registros + 1):
        fecha = datetime.now().strftime("%Y-%m-%d")
        cliente = f"{random.choice(CLIENTES)}-{random.randint(1000, 9999)}"
        monto = round(random.uniform(500, 20000), 2)
        iva = round(monto * 0.16, 2)
        total = monto + iva
        producto = random.choice(PRODUCTOS)
        status = random.choice(ESTADOS)
        metodo_pago = random.choice(METODOS_PAGO)
        dias_entrega = random.randint(1, 30)

        datos.append([
            i, fecha, cliente, monto, iva, total, producto,
            status, metodo_pago, dias_entrega
        ])
    return datos

def generar_reporte_csv(nombre_archivo, datos):
    with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo_csv:
        escritor = csv.writer(archivo_csv)
        escritor.writerow([
            "ID", "Fecha", "Cliente", "Monto (MXN)", "IVA (16%)",
            "Total (MXN)", "Producto", "Status", "Método de Pago", "Días para Entrega"
        ])
        escritor.writerows(datos)

def calcular_resumen(datos):
    total_ventas = sum(float(row[3]) for row in datos)
    total_iva = sum(float(row[4]) for row in datos)
    total_general = sum(float(row[5]) for row in datos)
    completados = len([row for row in datos if row[7] == "Completado"])
    pendientes = len([row for row in datos if row[7] == "Pendiente"])

    return {
        "Total Ventas": f"${total_ventas:,.2f}",
        "Total IVA": f"${total_iva:,.2f}",
        "Total General": f"${total_general:,.2f}",
        "Transacciones Completadas": completados,
        "Transacciones Pendientes": pendientes
    }

def main():
    try:
        if len(sys.argv) > 1:
            num_registros = int(sys.argv[1])
            if num_registros <= 0:
                raise ValueError("El número de registros debe ser mayor a 0")
        else:
            num_registros = 15  # Default

        if num_registros > 1000:
            print("Advertencia: Se generarán más de 1000 registros", file=sys.stderr)

        datos = generar_datos_aleatorios(num_registros)
        nombre_archivo = f"reporte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        generar_reporte_csv(nombre_archivo, datos)

        resumen = calcular_resumen(datos)
        print(f"Reporte generado: {nombre_archivo}")
        print("\n=== Resumen Ejecutivo ===")
        for clave, valor in resumen.items():
            print(f"{clave}: {valor}")

    except ValueError as ve:
        print(f"Error de valor: {str(ve)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()