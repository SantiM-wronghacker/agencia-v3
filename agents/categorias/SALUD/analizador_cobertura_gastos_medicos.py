import sys
import json
import random
from datetime import datetime, timedelta
import math

# AREA: SEGUROS
# DESCRIPCION: Agente que realiza analizador cobertura gastos medicos
# TECNOLOGIA: Python 3.x

def main():
    try:
        # Parámetros por defecto
        args = sys.argv[1:]
        if len(args) > 0:
            monto_asegurado = float(args[0]) if args[0].replace('.', '').isdigit() else 500000.0
            deducible = float(args[1]) if len(args) > 1 and args[1].replace('.', '').isdigit() else 5000.0
            coaseguro = float(args[2]) if len(args) > 2 and args[2].replace('.', '').isdigit() else 0.10
            edad = int(args[3]) if len(args) > 3 and args[3].isdigit() else 30
            sexo = args[4] if len(args) > 4 and args[4] in ['M', 'F'] else 'M'
        else:
            monto_asegurado = 500000.0
            deducible = 5000.0
            coaseguro = 0.10
            edad = 30
            sexo = 'M'

        # Simulación de gastos médicos
        gastos = {
            "hospitalizacion": random.uniform(20000, 80000),
            "medicamentos": random.uniform(5000, 30000),
            "consultas": random.uniform(2000, 10000),
            "laboratorio": random.uniform(3000, 15000),
            "cirugia": random.uniform(50000, 200000)
        }

        # Cálculo de cobertura
        total_gastos = sum(gastos.values())
        if total_gastos > monto_asegurado:
            total_gastos = monto_asegurado

        cobertura = total_gastos - deducible
        if cobertura < 0:
            cobertura = 0

        # Aplicar factor de ajuste por edad y sexo
        if edad < 25:
            factor_edad = 0.9
        elif edad < 40:
            factor_edad = 1.0
        elif edad < 60:
            factor_edad = 1.1
        else:
            factor_edad = 1.2

        if sexo == 'F':
            factor_sexo = 0.95
        else:
            factor_sexo = 1.0

        cobertura *= factor_edad * factor_sexo

        coaseguro_aplicado = cobertura * coaseguro
        cobertura_final = cobertura - coaseguro_aplicado

        # Impresión de resultados
        print(f"Análisis de cobertura de gastos médicos - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Monto asegurado: ${monto_asegurado:,.2f} MXN")
        print(f"Total de gastos médicos: ${total_gastos:,.2f} MXN")
        print(f"Gastos médicos detallados:")
        for gasto, monto in gastos.items():
            print(f"  - {gasto.capitalize()}: ${monto:,.2f} MXN")
        print(f"Cobertura después de deducible (${deducible:,.2f} MXN): ${cobertura:,.2f} MXN")
        print(f"Coaseguro aplicado: {coaseguro*100:.2f}%")
        print(f"Cobertura final: ${cobertura_final:,.2f} MXN")
        print(f"Factor de ajuste por edad: {factor_edad:.2f}")
        print(f"Factor de ajuste por sexo: {factor_sexo:.2f}")
        print(f"Resumen ejecutivo: La cobertura final es de ${cobertura_final:,.2f} MXN, considerando un monto asegurado de ${monto_asegurado:,.2f} MXN y un total de gastos médicos de ${total_gastos:,.2f} MXN.")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()