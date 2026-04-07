"""
ÁREA: FINANZAS
DESCRIPCIÓN: Asistente para calcular IVA y subtotal de montos
TECNOLOGÍA: Python
"""

import sys
import math

class AsistenteIVAContable:
    def __init__(self, montos, iva_porcentaje=0.16):
        self.montos = montos
        self.iva_porcentaje = iva_porcentaje

    def separar_iva(self):
        iva_total = 0
        subtotal_total = 0
        resumen = []

        for monto in self.montos:
            try:
                iva = monto * self.iva_porcentaje
                subtotal = monto / (1 + self.iva_porcentaje)

                iva_total += iva
                subtotal_total += subtotal

                resumen.append({
                    'monto': monto,
                    'iva': iva,
                    'subtotal': subtotal
                })
            except ZeroDivisionError:
                print("Error: No se puede dividir por cero.")
                return None, None, None
            except TypeError:
                print("Error: El monto debe ser un número.")
                return None, None, None

        return resumen, iva_total, subtotal_total

    def generar_resumen(self):
        resumen, iva_total, subtotal_total = self.separar_iva()

        if resumen is None:
            return

        print("Resumen de Montos:")
        for i, item in enumerate(resumen):
            print(f"Monto {i+1}: {item['monto']:.2f}, IVA: {item['iva']:.2f}, Subtotal: {item['subtotal']:.2f}")

        print("\nTotales:")
        print(f"Total de Montos: {sum(self.montos):.2f}")
        print(f"Total de IVA: {iva_total:.2f}")
        print(f"Total de Subtotales: {subtotal_total:.2f}")
        print(f"Promedio de Montos: {sum(self.montos) / len(self.montos):.2f}")
        print(f"Mayor Monto: {max(self.montos):.2f}")
        print(f"Menor Monto: {min(self.montos):.2f}")
        print(f"Desviación Estándar de Montos: {math.sqrt(sum((x - sum(self.montos) / len(self.montos)) ** 2 for x in self.montos) / len(self.montos)):.2f}")
        print(f"Varianza de Montos: {sum((x - sum(self.montos) / len(self.montos)) ** 2 for x in self.montos) / len(self.montos):.2f}")
        print(f"Media de IVA: {iva_total / len(resumen):.2f}")
        print(f"Media de Subtotales: {subtotal_total / len(resumen):.2f}")
        print(f"Total de Montos sin IVA: {subtotal_total:.2f}")
        print(f"Total de Montos con IVA: {sum(self.montos):.2f}")

        print("\nResumen Ejecutivo:")
        print(f"El total de montos es de {sum(self.montos):.2f}, con un total de IVA de {iva_total:.2f} y un total de subtotales de {subtotal_total:.2f}.")
        print(f"El promedio de montos es de {sum(self.montos) / len(self.montos):.2f}, con un mayor monto de {max(self.montos):.2f} y un menor monto de {min(self.montos):.2f}.")
        print(f"La desviación estándar de montos es de {math.sqrt(sum((x - sum(self.montos) / len(self.montos)) ** 2 for x in self.montos) / len(self.montos)):.2f}.")

def main():
    if len(sys.argv) > 1:
        montos = [float(x) for x in sys.argv[1:]]
    else:
        montos = [100.0, 200.0, 300.0, 400.0, 500.0]

    asistente = AsistenteIVAContable(montos)
    asistente.generar_resumen()

if __name__ == "__main__":
    main()