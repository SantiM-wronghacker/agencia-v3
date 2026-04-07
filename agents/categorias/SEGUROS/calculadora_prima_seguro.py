"""
ÁREA: SEGUROS
DESCRIPCIÓN: Agente que realiza calculadora prima seguro
TECNOLOGÍA: Python estándar
"""
import sys
import math

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcular_prima(edad, monto_asegurado, tipo_vehiculo):
    # Parámetros base para México
    base_anual = 0.03  # 3% base
    factor_edad = 1.0
    factor_vehiculo = 1.0

    # Ajustes por edad
    if edad < 20:
        factor_edad = 1.8
    elif edad < 25:
        factor_edad = 1.5
    elif edad < 30:
        factor_edad = 1.3
    elif edad > 65:
        factor_edad = 1.2

    # Ajustes por tipo de vehículo
    if tipo_vehiculo.lower() == "lujo":
        factor_vehiculo = 1.8
    elif tipo_vehiculo.lower() == "suv":
        factor_vehiculo = 1.4
    elif tipo_vehiculo.lower() == "economico":
        factor_vehiculo = 0.9
    elif tipo_vehiculo.lower() == "deportivo":
        factor_vehiculo = 2.0

    prima_anual = monto_asegurado * base_anual * factor_edad * factor_vehiculo
    prima_mensual = prima_anual / 12
    prima_trimestral = prima_anual / 4
    prima_semestral = prima_anual / 2

    return {
        "prima_anual": round(prima_anual, 2),
        "prima_mensual": round(prima_mensual, 2),
        "prima_trimestral": round(prima_trimestral, 2),
        "prima_semestral": round(prima_semestral, 2),
        "factor_edad": factor_edad,
        "factor_vehiculo": factor_vehiculo
    }

def main():
    try:
        # Valores por defecto realistas para México
        edad = int(sys.argv[1]) if len(sys.argv) > 1 else 35
        monto_asegurado = float(sys.argv[2]) if len(sys.argv) > 2 else 300000.00
        tipo_vehiculo = sys.argv[3] if len(sys.argv) > 3 else "economico"

        resultado = calcular_prima(edad, monto_asegurado, tipo_vehiculo)

        print("Cálculo de prima de seguro de auto")
        print(f"Edad del asegurado: {edad} años")
        print(f"Monto asegurado: ${monto_asegurado:,.2f} MXN")
        print(f"Tipo de vehículo: {tipo_vehiculo}")
        print(f"Prima anual: ${resultado['prima_anual']:,.2f} MXN")
        print(f"Prima mensual: ${resultado['prima_mensual']:,.2f} MXN")
        print(f"Prima trimestral: ${resultado['prima_trimestral']:,.2f} MXN")
        print(f"Prima semestral: ${resultado['prima_semestral']:,.2f} MXN")
        print(f"Factor por edad: {resultado['factor_edad']:.2f}x")
        print(f"Factor por vehículo: {resultado['factor_vehiculo']:.2f}x")
        print("Resumen ejecutivo:")
        print(f"La prima anual para un vehículo {tipo_vehiculo} con un monto asegurado de ${monto_asegurado:,.2f} MXN y un asegurado de {edad} años es de ${resultado['prima_anual']:,.2f} MXN.")
        print(f"La prima mensual es de ${resultado['prima_mensual']:,.2f} MXN, la prima trimestral es de ${resultado['prima_trimestral']:,.2f} MXN y la prima semestral es de ${resultado['prima_semestral']:,.2f} MXN.")

    except Exception as e:
        print(f"Error en el cálculo: {str(e)}")
        print("Uso: python calculadora_prima_seguro.py <edad> <monto_asegurado> <tipo_vehiculo>")

if __name__ == "__main__":
    main()