"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza proyector flujo caja 3 años
TECNOLOGÍA: Python estándar
"""
import sys
import json
import math
from datetime import datetime

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Parámetros por defecto
        ingresos_mensuales = float(sys.argv[1]) if len(sys.argv) > 1 else 50000.0
        gastos_fijos = float(sys.argv[2]) if len(sys.argv) > 2 else 30000.0
        tasa_interes = float(sys.argv[3]) if len(sys.argv) > 3 else 0.05
        inflacion = float(sys.argv[4]) if len(sys.argv) > 4 else 0.03

        flujo_caja = []
        fecha_actual = datetime.now()

        for año in range(1, 4):
            flujo_anual = 0
            for mes in range(1, 13):
                mes_actual = fecha_actual.month + mes - 1
                año_actual = fecha_actual.year + año - 1
                if mes_actual > 12:
                    mes_actual -= 12
                    año_actual += 1

                # Ajustar por inflación
                ingresos = ingresos_mensuales * (1 + inflacion) ** año
                gastos = gastos_fijos * (1 + inflacion) ** año

                flujo_mensual = ingresos - gastos
                flujo_anual += flujo_mensual

                flujo_caja.append({
                    'año': año_actual,
                    'mes': mes_actual,
                    'ingresos': round(ingresos, 2),
                    'gastos': round(gastos, 2),
                    'flujo': round(flujo_mensual, 2)
                })

            # Calcular interés anual
            flujo_anual += flujo_anual * tasa_interes
            flujo_caja.append({
                'año': año_actual,
                'mes': 12,
                'ingresos': 0,
                'gastos': 0,
                'flujo': round(flujo_anual, 2),
                'tipo': 'total_anual'
            })

        # Imprimir resultados
        print("Proyección de flujo de caja para los próximos 3 años:")
        for item in flujo_caja:
            if 'tipo' in item:
                print(f"Año {item['año']}: Flujo total anual = {item['flujo']}")
            else:
                print(f"Año {item['año']}, Mes {item['mes']}: Ingresos = {item['ingresos']}, Gastos = {item['gastos']}, Flujo = {item['flujo']}")

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        total_ingresos = sum(item['ingresos'] for item in flujo_caja if 'tipo' not in item)
        total_gastos = sum(item['gastos'] for item in flujo_caja if 'tipo' not in item)
        total_flujo = sum(item['flujo'] for item in flujo_caja if 'tipo' not in item)
        print(f"Total de ingresos: {round(total_ingresos, 2)}")
        print(f"Total de gastos: {round(total_gastos, 2)}")
        print(f"Total de flujo: {round(total_flujo, 2)}")
        print(f"Tasa de crecimiento de ingresos: {(total_ingresos / (ingresos_mensuales * 12)) - 1:.2%}")
        print(f"Tasa de crecimiento de gastos: {(total_gastos / (gastos_fijos * 12)) - 1:.2%}")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()