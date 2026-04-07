"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Simulador de hipoteca que calcula pago mensual, tabla de amortización
             e intereses totales. Acepta parámetros via sys.argv o usa defaults.
             Uso: python simulador_hipoteca.py monto tasa_anual plazo_años seguro_mensual
             Ejemplo: python simulador_hipoteca.py 2000000 10 20 500
TECNOLOGÍA: Python estándar
"""

import sys
import re

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

class SimuladorHipoteca:
    def __init__(self, monto_prestado, tasa_interes_anual, plazo_anios, seguro_mensual=500):
        self.monto_prestado       = float(monto_prestado)
        self.tasa_interes_anual   = float(tasa_interes_anual) / 100
        self.plazo_anios          = int(plazo_anios)
        self.seguro_mensual       = float(seguro_mensual)
        self.tasa_interes_mensual = self.tasa_interes_anual / 12

    def calcular_pago_mensual(self):
        tim = self.tasa_interes_mensual
        n   = self.plazo_anios * 12
        if tim == 0:
            return round(self.monto_prestado / n, 2)
        return round(self.monto_prestado * tim * (1 + tim) ** n / ((1 + tim) ** n - 1), 2)

    def calcular_tabla_amortizacion(self):
        tabla            = []
        saldo            = self.monto_prestado
        total_intereses  = 0
        total_pagos      = 0
        pago_mensual     = self.calcular_pago_mensual()

        for mes in range(1, self.plazo_anios * 12 + 1):
            interes      = round(saldo * self.tasa_interes_mensual, 2)
            pago_capital = round(pago_mensual - interes - self.seguro_mensual, 2)
            if saldo - pago_capital < 0:
                pago_capital = round(saldo, 2)
                pago_mensual = round(pago_capital + interes + self.seguro_mensual, 2)
            saldo           -= pago_capital
            total_intereses += interes
            total_pagos     += pago_mensual + self.seguro_mensual
            tabla.append({
                "Mes":          mes,
                "Pago mensual": round(pago_mensual + self.seguro_mensual, 2),
                "Intereses":    interes,
                "Seguro":       self.seguro_mensual,
                "Pago capital": pago_capital,
                "Saldo":        round(saldo, 2)
            })
        return tabla, round(total_intereses, 2), round(total_pagos, 2)

    def imprimir_resumen(self):
        tabla, total_intereses, total_pagos = self.calcular_tabla_amortizacion()
        pago_mensual = self.calcular_pago_mensual() + self.seguro_mensual

        print("=" * 50)
        print("SIMULACIÓN DE HIPOTECA")
        print("=" * 50)
        print(f"Monto prestado:        ${self.monto_prestado:,.2f}")
        print(f"Tasa de interés anual: {self.tasa_interes_anual*100:.1f}%")
        print(f"Plazo:                 {self.plazo_anios} años ({self.plazo_anios*12} meses)")
        print(f"Seguro mensual:        ${self.seguro_mensual:,.2f}")
        print("-" * 50)
        print(f"Pago mensual total:    ${pago_mensual:,.2f}")
        print(f"Total intereses:       ${total_intereses:,.2f}")
        print(f"Total pagos:           ${total_pagos:,.2f}")
        print(f"Costo total crédito:   ${total_pagos:,.2f}")
        print("=" * 50)
        print("PRIMEROS 3 MESES:")
        for pago in tabla[:3]:
            print(f"  Mes {pago['Mes']}: Pago ${pago['Pago mensual']:,.2f} | "
                  f"Interés ${pago['Intereses']:,.2f} | "
                  f"Capital ${pago['Pago capital']:,.2f} | "
                  f"Saldo ${pago['Saldo']:,.2f}")
        print("=" * 50)


def extraer_numero(texto):
    """Extrae el primer número válido de un string, ignorando caracteres extra."""
    if texto is None:
        return None
    # Eliminar comas de miles y extraer número
    limpio = re.sub(r'[^\d.]', '', str(texto).replace(',', ''))
    try:
        return float(limpio) if limpio else None
    except ValueError:
        return None


def main():
    # Defaults razonables
    monto          = 2_000_000
    tasa           = 10.0
    plazo          = 20
    seguro         = 500

    if len(sys.argv) >= 2:
        v = extraer_numero(sys.argv[1])
        if v: monto = v

    if len(sys.argv) >= 3:
        v = extraer_numero(sys.argv[2])
        if v: tasa = v

    if len(sys.argv) >= 4:
        v = extraer_numero(sys.argv[3])
        if v: plazo = int(v)

    if len(sys.argv) >= 5:
        v = extraer_numero(sys.argv[4])
        if v: seguro = v

    print(f"Parámetros: Monto ${monto:,.0f} | Tasa {tasa}% | Plazo {plazo} años | Seguro ${seguro}/mes")

    simulador = SimuladorHipoteca(monto, tasa, plazo, seguro)
    simulador.imprimir_resumen()


if __name__ == "__main__":
    main()