"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza analizador ciclo venta
TECNOLOGÍA: Python estándar
"""
import sys
import json
import random
from datetime import datetime, timedelta
import math

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión a Internet
except ImportError:
    WEB = False

def main():
    try:
        # Parámetros por defecto
        if len(sys.argv) > 1:
            dias_ciclo = int(sys.argv[1])
            ventas_diarias = int(sys.argv[2])
            conversion = float(sys.argv[3])
            ticket_promedio = float(sys.argv[4])
            meta_mensual = float(sys.argv[5])
        else:
            dias_ciclo = 30
            ventas_diarias = 15
            conversion = 0.25
            ticket_promedio = 1250.50
            meta_mensual = 150000.00

        # Procesamiento
        if dias_ciclo <= 0:
            raise ValueError("Días del ciclo deben ser un número positivo")

        if ventas_diarias <= 0:
            raise ValueError("Ventas diarias deben ser un número positivo")

        if conversion < 0 or conversion > 1:
            raise ValueError("Tasa de conversión debe ser un número entre 0 y 1")

        if ticket_promedio <= 0:
            raise ValueError("Ticket promedio debe ser un número positivo")

        if meta_mensual <= 0:
            raise ValueError("Meta mensual debe ser un número positivo")

        ventas_mes = ventas_diarias * dias_ciclo
        ventas_convertidas = ventas_mes * conversion
        ingresos = ventas_convertidas * ticket_promedio
        porcentaje_meta = (ingresos / meta_mensual) * 100

        # Generar datos aleatorios para muestra
        datos_muestra = []
        for _ in range(10):
            fecha = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
            clientes = random.randint(10, 25)
            ventas = random.randint(2, 5)
            ingresos_muestra = round(ventas * ticket_promedio, 2)
            datos_muestra.append({
                'fecha': fecha,
                'clientes': clientes,
                'ventas': ventas,
                'ingresos': ingresos_muestra
            })

        # Salida
        print(f"ÁREA: VENTAS")
        print(f"DESCRIPCIÓN: Agente que realiza analizador ciclo venta")
        print(f"TECNOLOGÍA: Python estándar")
        print(f"Ciclo de ventas: {dias_ciclo} días")
        print(f"Ventas diarias promedio: {ventas_diarias} clientes")
        print(f"Tasa de conversión: {conversion*100:.1f}%")
        print(f"Ingresos proyectados: ${ingresos:,.2f} MXN")
        print(f"Cumplimiento de meta: {porcentaje_meta:.1f}%")
        print(f"Meta mensual: ${meta_mensual:,.2f} MXN")
        print(f"Ticket promedio: ${ticket_promedio:,.2f} MXN")
        print(f"Días del ciclo: {dias_ciclo}")
        print(f"Ventas diarias: {ventas_diarias}")
        print(f"Conversión: {conversion}")
        print(f"Meta mensual: ${meta_mensual:,.2f} MXN")
        print(f"Resumen ejecutivo: El análisis del ciclo de ventas indica que se proyectan ingresos de ${ingresos:,.2f} MXN, lo que representa un cumplimiento de meta del {porcentaje_meta:.1f}%.")

        # Mostrar datos de muestra
        print("\nDatos de muestra:")
        for i, dato in enumerate(datos_muestra):
            print(f"Fecha {i+1}: {dato['fecha']}")
            print(f"Clientes: {dato['clientes']}")
            print(f"Ventas: {dato['ventas']}")
            print(f"Ingresos: ${dato['ingresos']:.2f} MXN")
            print()

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()