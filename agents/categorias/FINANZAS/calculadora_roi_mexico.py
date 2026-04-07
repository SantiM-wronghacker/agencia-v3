"""
ÁREA: FINANZAS
DESCRIPCIÓN: Calculadora de ROI y flujo de caja neto para propiedades en México
TECNOLOGÍA: Python, sys
"""

import sys

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

class Propiedad:
    def __init__(self, valor_compra, renta_mensual, gastos_mantenimiento_mensual, predial_anual, impuesto_renta=0.1, gastos_administracion=0.05):
        self.valor_compra = valor_compra
        self.renta_mensual = renta_mensual
        self.gastos_mantenimiento_mensual = gastos_mantenimiento_mensual
        self.predial_anual = predial_anual
        self.impuesto_renta = impuesto_renta
        self.gastos_administracion = gastos_administracion

    def calcular_roi(self):
        roi_anual = ((self.renta_mensual * 12) * (1 - self.impuesto_renta)) / self.valor_compra
        return roi_anual

    def calcular_flujo_caja_neto(self):
        flujo_caja_neto_mensual = self.renta_mensual - self.gastos_mantenimiento_mensual - (self.renta_mensual * self.gastos_administracion)
        return flujo_caja_neto_mensual

    def calcular_flujo_caja_neto_anual(self):
        flujo_caja_neto_anual = (self.renta_mensual * 12) - (self.gastos_mantenimiento_mensual * 12) - self.predial_anual - (self.renta_mensual * 12 * self.gastos_administracion) - (self.renta_mensual * 12 * self.impuesto_renta)
        return flujo_caja_neto_anual


def main():
    print("Calculadora de ROI y flujo de caja neto para propiedades en México")

    if len(sys.argv) == 5:
        valor_compra = float(sys.argv[1])
        renta_mensual = float(sys.argv[2])
        gastos_mantenimiento_mensual = float(sys.argv[3])
        predial_anual = float(sys.argv[4])
    else:
        valor_compra = 2000000.0
        renta_mensual = 15000.0
        gastos_mantenimiento_mensual = 5000.0
        predial_anual = 20000.0
        print(f"Usando valores por defecto: valor_compra={valor_compra}, renta_mensual={renta_mensual}, gastos_mantenimiento_mensual={gastos_mantenimiento_mensual}, predial_anual={predial_anual}")

    try:
        propiedad = Propiedad(valor_compra, renta_mensual, gastos_mantenimiento_mensual, predial_anual)
        roi_anual = propiedad.calcular_roi()
        flujo_caja_neto_mensual = propiedad.calcular_flujo_caja_neto()
        flujo_caja_neto_anual = propiedad.calcular_flujo_caja_neto_anual()

        print(f"Valor de compra: ${valor_compra:.2f}")
        print(f"Renta mensual: ${renta_mensual:.2f}")
        print(f"Gastos de mantenimiento mensual: ${gastos_mantenimiento_mensual:.2f}")
        print(f"Predial anual: ${predial_anual:.2f}")
        print(f"ROI anual: {roi_anual * 100:.2f}%")
        print(f"Flujo de caja neto mensual: ${flujo_caja_neto_mensual:.2f}")
        print(f"Flujo de caja neto anual: ${flujo_caja_neto_anual:.2f}")
        print(f"Impuesto a la renta (10%): {propiedad.impuesto_renta * 100:.2f}%")
        print(f"Gastos de administración (5%): {propiedad.gastos_administracion * 100:.2f}%")
        print("Resumen ejecutivo:")
        print(f"La propiedad con un valor de compra de ${valor_compra:.2f} y una renta mensual de ${renta_mensual:.2f} tiene un ROI anual de {roi_anual * 100:.2f}% y un flujo de caja neto anual de ${flujo_caja_neto_anual:.2f}.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()