"""
ÁREA: SALUD
DESCRIPCIÓN: Agente que realiza analizador costos seguro medico
TECNOLOGÍA: Python estándar
"""
import sys
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
        # Parámetros por defecto
        edad = int(sys.argv[1]) if len(sys.argv) > 1 else 35
        cobertura = sys.argv[2] if len(sys.argv) > 2 else "familiar"
        hospitales = int(sys.argv[3]) if len(sys.argv) > 3 else 3

        # Costos base en MXN (datos reales aproximados)
        costos_base = {
            "individual": 3500,
            "familiar": 6500,
            "ejecutivo": 12000
        }

        # Ajuste por edad
        if edad < 18:
            factor_edad = 0.8
        elif edad < 30:
            factor_edad = 0.95
        elif edad < 50:
            factor_edad = 1.0
        else:
            factor_edad = 1.2

        # Ajuste por hospitales
        factor_hospitales = 1 + (0.1 * (hospitales - 1))

        # Costo total
        costo_base = costos_base.get(cobertura, costos_base["familiar"])
        costo_total = round(costo_base * factor_edad * factor_hospitales, 2)

        # Generar datos adicionales
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        fecha_vencimiento = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
        deducible = random.randint(5000, 15000)
        copago = random.randint(100, 300)
        gastos_medicos = round(costo_total * 0.8, 2)
        gastos_hospitales = round(costo_total * 0.15, 2)
        gastos_consultas = round(costo_total * 0.05, 2)

        # Imprimir resultados
        print(f"Análisis de costo de seguro médico - {fecha_actual}")
        print(f"Cobertura: {cobertura.capitalize()}")
        print(f"Edad del titular: {edad} años")
        print(f"Costo mensual estimado: ${costo_total:,.2f} MXN")
        print(f"Deducible anual: ${deducible:,.2f} MXN")
        print(f"Copago por consulta: ${copago:,.2f} MXN")
        print(f"Vigencia hasta: {fecha_vencimiento}")
        print(f"Gastos médicos estimados: ${gastos_medicos:,.2f} MXN")
        print(f"Gastos hospitalarios estimados: ${gastos_hospitales:,.2f} MXN")
        print(f"Gastos por consultas estimados: ${gastos_consultas:,.2f} MXN")
        print(f"Total de gastos estimados: ${gastos_medicos + gastos_hospitales + gastos_consultas:,.2f} MXN")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"El costo total del seguro médico para {cobertura} es de ${costo_total:,.2f} MXN al mes.")
        print(f"El deducible anual es de ${deducible:,.2f} MXN y el copago por consulta es de ${copago:,.2f} MXN.")
        print(f"Se estima que los gastos médicos serán de ${gastos_medicos:,.2f} MXN, los gastos hospitalarios serán de ${gastos_hospitales:,.2f} MXN y los gastos por consultas serán de ${gastos_consultas:,.2f} MXN.")

    except ValueError as e:
        print(f"Error: {str(e)}")
    except KeyError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Error en el análisis: {str(e)}")

if __name__ == "__main__":
    main()