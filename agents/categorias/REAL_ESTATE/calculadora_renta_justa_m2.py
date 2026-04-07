import sys
import math

def calcula_renta_justa(m2, ubicacion, tipo_inmueble, precio_base, ajuste_por_tipo):
    """
    Calcula la renta justa por m2 según la ubicación y tipo de inmueble
    """
    # Impuesto ISR (8% de la renta justa)
    impuesto_isr = m2 * precio_base * ajuste_por_tipo * 0.08

    # Impuesto IVA (16% de la renta justa)
    impuesto_iva = m2 * precio_base * ajuste_por_tipo * 0.16

    # Total a pagar incluyendo impuestos
    total_a_pagar = m2 * precio_base * ajuste_por_tipo + impuesto_isr + impuesto_iva

    # Impuesto predial (0.1% de la renta justa)
    impuesto_predial = m2 * precio_base * ajuste_por_tipo * 0.001

    # Total a pagar incluyendo impuestos y predial
    total_a_pagar_incluyendo_predial = total_a_pagar + impuesto_predial

    return m2 * precio_base * ajuste_por_tipo, impuesto_isr, impuesto_iva, impuesto_predial, total_a_pagar, total_a_pagar_incluyendo_predial

def main():
    try:
        if len(sys.argv) < 6:
            print("ERROR: Faltan argumentos. Utilice: python calculadora_renta_justa_m2.py m2 ubicacion tipo_inmueble precio_base ajuste_por_tipo")
            return

        m2 = float(sys.argv[1])
        ubicacion = sys.argv[2]
        tipo_inmueble = sys.argv[3]
        precio_base = float(sys.argv[4])
        ajuste_por_tipo = float(sys.argv[5])

        if m2 <= 0:
            raise ValueError("M2 debe ser mayor que 0")

        if ubicacion not in ['centro', 'norte', 'sur']:
            print("ERROR: Ubicación debe ser centro, norte o sur")
            return

        if tipo_inmueble not in ['departamento', 'casa']:
            print("ERROR: Tipo de inmueble debe ser departamento o casa")
            return

        if precio_base <= 0:
            raise ValueError("Precio base debe ser mayor que 0")

        if ajuste_por_tipo <= 0:
            raise ValueError("Ajuste por tipo debe ser mayor que 0")

        renta_justa, impuesto_isr, impuesto_iva, impuesto_predial, total_a_pagar, total_a_pagar_incluyendo_predial = calcula_renta_justa(m2, ubicacion, tipo_inmueble, precio_base, ajuste_por_tipo)

        print("ÁREA: FINANZAS")
        print("DESCRIPCIÓN: Agente que realiza calculadora renta justa m2")
        print("TECNOLOGÍA: Python estándar")
        print(f"M2: {m2} m2")
        print(f"Ubicación: {ubicacion}")
        print(f"Tipo de inmueble: {tipo_inmueble}")
        print(f"Precio base: ${precio_base:.2f} por m2")
        print(f"Ajuste por tipo: {ajuste_por_tipo*100}%")
        print(f"Renta justa: ${renta_justa:.2f} por m2")
        print(f"Impuesto ISR: ${impuesto_isr:.2f} por m2")
        print(f"Impuesto IVA: ${impuesto_iva:.2f} por m2")
        print(f"Impuesto predial: ${impuesto_predial:.2f} por m2")
        print(f"Total a pagar: ${total_a_pagar:.2f} por m2")
        print(f"Total a pagar incluyendo predial: ${total_a_pagar_incluyendo_predial:.2f} por m2")
        print("RESEÑA EJECUTIVA: La renta justa por el inmueble es de ${renta_justa:.2f} por m2, lo que incluye un total de impuestos de ${impuesto_isr+impuesto_iva+impuesto_predial:.2f} por m2.")

    except ValueError as e:
        print(f"ERROR: {e}")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()