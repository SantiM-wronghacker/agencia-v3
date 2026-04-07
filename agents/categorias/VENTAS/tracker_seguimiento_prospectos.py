"""
ÁREA: VENTAS
DESCRIPCIÓN: Agente que realiza tracker seguimiento prospectos
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
from datetime import datetime, timedelta

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Parámetros por defecto
        dias_seguimiento = 7
        prospectos_diarios = 10
        tasa_conversion = 0.15  # 15%

        if len(sys.argv) > 1:
            dias_seguimiento = int(sys.argv[1])
        if len(sys.argv) > 2:
            prospectos_diarios = int(sys.argv[2])
        if len(sys.argv) > 3:
            tasa_conversion = float(sys.argv[3])

        # Generar datos de seguimiento
        fecha_inicio = datetime.now().date()
        prospectos = []
        for dia in range(dias_seguimiento):
            fecha = fecha_inicio + timedelta(days=dia)
            prospectos_dia = random.randint(prospectos_diarios - 2, prospectos_diarios + 2)
            ventas = round(prospectos_dia * tasa_conversion)
            ingresos = round(ventas * 1000)  # suponiendo un ingreso promedio de $1000 por venta
            prospectos.append({
                "fecha": fecha.strftime("%Y-%m-%d"),
                "prospectos": prospectos_dia,
                "ventas": ventas,
                "ingresos": ingresos,
                "tasa_conversion": round(ventas / prospectos_dia * 100, 2)
            })

        # Calcular métricas
        total_prospectos = sum(p["prospectos"] for p in prospectos)
        total_ventas = sum(p["ventas"] for p in prospectos)
        total_ingresos = sum(p["ingresos"] for p in prospectos)
        tasa_conversion_promedio = round(total_ventas / total_prospectos * 100, 2)
        ingreso_promedio_por_venta = round(total_ingresos / total_ventas, 2)

        # Mostrar resultados
        print("=== REPORTE DE SEGUIMIENTO DE PROSPECTOS ===")
        print(f"Período: {prospectos[0]['fecha']} al {prospectos[-1]['fecha']}")
        print(f"Prospectos totales: {total_prospectos}")
        print(f"Ventas generadas: {total_ventas}")
        print(f"Ingresos totales: ${total_ingresos}")
        print(f"Tasa de conversión promedio: {tasa_conversion_promedio}%")
        print(f"Ingreso promedio por venta: ${ingreso_promedio_por_venta}")
        print(f"Prospectos por día: {prospectos_diarios} (promedio)")
        print(f"Ventas diarias promedio: {round(total_ventas / dias_seguimiento, 2)}")
        print(f"Ingresos diarios promedio: ${round(total_ingresos / dias_seguimiento, 2)}")

        # Resumen ejecutivo
        print("\n=== RESUMEN EJECUTIVO ===")
        print(f"En el período de {dias_seguimiento} días, se generaron {total_ventas} ventas con un ingreso total de ${total_ingresos}.")
        print(f"La tasa de conversión promedio fue de {tasa_conversion_promedio}%, con un ingreso promedio por venta de ${ingreso_promedio_por_venta}.")
        print(f"Se recomienda mantener el ritmo de {prospectos_diarios} prospectos diarios para alcanzar los objetivos de ventas y ingresos.")

    except Exception as e:
        print(f"Error en el seguimiento: {str(e)}", file=sys.stderr)
    except ValueError:
        print("Error: Los parámetros ingresados no son válidos.", file=sys.stderr)
    except IndexError:
        print("Error: No se ingresaron suficientes parámetros.", file=sys.stderr)

if __name__ == "__main__":
    main()