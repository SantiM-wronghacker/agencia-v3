import sys
import json
import datetime
import math

# AREA: FINANZAS
# DESCRIPCION: Agente que realiza proyección de flujo de caja 3 años
# TECNOLOGIA: Python

def main():
    try:
        # Parametros por defecto
        años = 3
        ingresos_anuales = 1000000  # Ingresos anuales promedio de una empresa en México
        gastos_anuales = 500000  # Gastos anuales promedio de una empresa en México
        tasa_interes = 0.05  # Tasa de interés promedio en México
        inflacion = 0.03  # Tasa de inflación promedio en México

        # Verificar parámetros por línea de comandos
        if len(sys.argv) > 1:
            try:
                años = int(sys.argv[1])
                ingresos_anuales = float(sys.argv[2])
                gastos_anuales = float(sys.argv[3])
                tasa_interes = float(sys.argv[4])
                if len(sys.argv) > 5:
                    inflacion = float(sys.argv[5])
            except ValueError:
                print("Error: Parámetros inválidos. Utilice: python proyector_flujo_caja_3_anos.py <años> <ingresos_anuales> <gastos_anuales> <tasa_interes> <inflacion>")
                return

        # Verificar valores negativos
        if ingresos_anuales < 0 or gastos_anuales < 0 or tasa_interes < 0 or inflacion < 0:
            print("Error: Valores negativos no permitidos")
            return

        # Calculo de flujo de caja
        flujo_caja = []
        for año in range(años):
            ingresos = ingresos_anuales * (1 + (año * 0.1)) * (1 + inflacion)
            gastos = gastos_anuales * (1 + (año * 0.05)) * (1 + inflacion)
            flujo = ingresos - gastos
            flujo_caja.append({
                "año": año + 1,
                "ingresos": round(ingresos, 2),
                "gastos": round(gastos, 2),
                "flujo": round(flujo, 2),
                "utilidad_neta": round(flujo + (flujo * tasa_interes), 2)
            })

        # Calculo de intereses
        intereses = []
        saldo = 0
        for año in range(años):
            saldo += flujo_caja[año]["flujo"]
            interes = saldo * tasa_interes
            intereses.append({
                "año": año + 1,
                "interes": round(interes, 2),
                "saldo": round(saldo, 2)
            })

        # Resumen ejecutivo
        resumen = {
            "ingresos_promedio": round(sum([flujo_caja[i]["ingresos"] for i in range(años)]) / años, 2),
            "gastos_promedio": round(sum([flujo_caja[i]["gastos"] for i in range(años)]) / años, 2),
            "flujo_promedio": round(sum([flujo_caja[i]["flujo"] for i in range(años)]) / años, 2),
            "utilidad_neta_promedio": round(sum([flujo_caja[i]["utilidad_neta"] for i in range(años)]) / años, 2)
        }

        # Impresión de resultados
        print("Flujo de caja por año:")
        for flujo in flujo_caja:
            print(f"Año {flujo['año']}: Ingresos {flujo['ingresos']}, Gastos {flujo['gastos']}, Flujo {flujo['flujo']}, Utilidad Neta {flujo['utilidad_neta']}")
        print("\nIntereses por año:")
        for interes in intereses:
            print(f"Año {interes['año']}: Interés {interes['interes']}, Saldo {interes['saldo']}")
        print("\nResumen ejecutivo:")
        for key, value in resumen.items():
            print(f"{key.capitalize().replace('_', ' ')}: {value}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()