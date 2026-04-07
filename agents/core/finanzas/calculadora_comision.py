"""
ÁREA: VENTAS
DESCRIPCIÓN: Calcula comisiones de ventas para agentes inmobiliarios o vendedores. Soporta esquemas fijos, escalonados y con bonos por meta. Muestra desglose mensual, anual y proyecciones.
TECNOLOGÍA: Python estándar
"""

import sys
from datetime import datetime

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcula_comision(valor_venta, porcentaje_comision, esquema, meta_anual=5000000, bono_meta=50000):
    try:
        valor_venta = float(valor_venta)
        porcentaje_comision = float(porcentaje_comision)

        if esquema == "fijo":
            return valor_venta * (porcentaje_comision / 100)
        elif esquema == "escalonado":
            if valor_venta < 1000000:
                return valor_venta * (2 / 100)
            elif valor_venta < 5000000:
                return valor_venta * (3 / 100)
            else:
                return valor_venta * (5 / 100)
        elif esquema == "bono":
            comision_base = valor_venta * (3 / 100)
            if valor_venta > meta_anual:
                return comision_base + bono_meta
            return comision_base
        else:
            raise ValueError("Esquema no reconocido")
    except ValueError as e:
        raise ValueError(f"Error en parámetros: {e}")

def main():
    try:
        if len(sys.argv) < 4:
            valor_venta = 2000000
            porcentaje_comision = 3
            esquema = "escalonado"
            meta_anual = 5000000
            bono_meta = 50000
        else:
            valor_venta = sys.argv[1]
            porcentaje_comision = sys.argv[2]
            esquema = sys.argv[3]
            meta_anual = float(sys.argv[4]) if len(sys.argv) > 4 else 5000000
            bono_meta = float(sys.argv[5]) if len(sys.argv) > 5 else 50000

        comision = calcula_comision(valor_venta, porcentaje_comision, esquema, meta_anual, bono_meta)

        print("="*50)
        print(f"REPORTE DE COMISIONES - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("="*50)
        print(f"Valor de venta: ${valor_venta:,.2f}")
        print(f"Esquema de comisión: {esquema.upper()}")
        print(f"Comisión total: ${comision:,.2f}")
        print(f"Desglose mensual: ${comision/12:,.2f}")
        print(f"Desglose anual: ${comision*12:,.2f}")
        print(f"Meta anual: ${meta_anual:,.2f}")
        print(f"Bono por meta: ${bono_meta:,.2f}")

        if esquema == "bono":
            print("\n[BONO APLICADO]" if float(valor_venta) > meta_anual else "\n[BONO NO APLICADO]")

        print("\n=== RESUMEN EJECUTIVO ===")
        print(f"El agente generó una comisión de ${comision:,.2f} por esta venta.")
        print(f"Esto representa ${comision/12:,.2f} mensuales o ${comision*12:,.2f} anuales.")
        print(f"Para alcanzar la meta anual de ${meta_anual:,.2f}, necesita vender {meta_anual/float(valor_venta):.2f} propiedades más.")
        print("="*50)
    except Exception as e:
        print(f"ERROR: {str(e)}")
        print("Uso correcto: python calculadora_comision.py <valor_venta> <porcentaje> <esquema> [meta_anual] [bono_meta]")
        print("Ejemplo: python calculadora_comision.py 2000000 3 escalonado 5000000 50000")

if __name__ == "__main__":
    main()