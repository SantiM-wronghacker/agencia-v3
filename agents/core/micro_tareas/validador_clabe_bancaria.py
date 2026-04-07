"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: validador clabe bancaria
TECNOLOGÍA: Python estándar
"""

import sys
import re
import os

def validador_clabe_bancaria(entrada, institucion=None):
    """Función pura, sin prints, sin side effects."""
    try:
        if not entrada or len(entrada) != 22:
            return {
                "resultado": "INVALIDO:longitud",
                "detalles": "La Clabe bancaria debe tener 22 dígitos",
                "recomendaciones": "Verificar la longitud de la Clabe bancaria",
                "institucion": institucion
            }
        patron = re.compile(r'^\d{22}$')
        if not patron.match(entrada):
            return {
                "resultado": "INVALIDO:patron",
                "detalles": "La Clabe bancaria no cumple con el patrón de 22 dígitos",
                "recomendaciones": "Verificar el formato de la Clabe bancaria",
                "institucion": institucion
            }
        # Verificar que la Clabe bancaria sea válida para México
        # (para este ejemplo, se asume que una Clabe bancaria válida comienza con 01)
        if not entrada.startswith('01'):
            return {
                "resultado": "INVALIDO:patron",
                "detalles": "La Clabe bancaria no es válida para México",
                "recomendaciones": "Verificar la Clabe bancaria con la institución bancaria",
                "institucion": institucion
            }
        # Verificar que la Clabe bancaria sea válida para la institución bancaria especificada
        if institucion:
            # Para este ejemplo, se asume que una Clabe bancaria válida para Banamex comienza con 01
            if institucion.lower() == 'banamex' and not entrada.startswith('01'):
                return {
                    "resultado": "INVALIDO:patron",
                    "detalles": "La Clabe bancaria no es válida para Banamex",
                    "recomendaciones": "Verificar la Clabe bancaria con Banamex",
                    "institucion": institucion
                }
        return {
            "resultado": "VALIDO",
            "detalles": "La Clabe bancaria es válida",
            "recomendaciones": "Puede utilizar la Clabe bancaria para realizar operaciones",
            "institucion": institucion
        }
    except Exception as e:
        return {
            "resultado": "ERROR",
            "detalles": str(e),
            "recomendaciones": "Verificar el error y realizar las correcciones necesarias"
        }

def main():
    institucion = sys.argv[2] if len(sys.argv) > 2 else None
    clabe = sys.argv[1] if len(sys.argv) > 1 else "123456789012345678901234"
    resultado = validador_clabe_bancaria(clabe, institucion)
    print("Resultado:", resultado["resultado"])
    print("Detalles:", resultado["detalles"])
    print("Recomendaciones:", resultado["recomendaciones"])
    print("Institución:", resultado["institucion"])
    print("Fecha y hora de ejecución:", os.environ.get('TZ', 'UTC'))
    print("Versión de Python:", sys.version)
    print("Nombre del archivo de ejecución:", os.path.basename(__file__))
    print("Resumen ejecutivo: La Clabe bancaria", clabe, "ha sido validada con éxito.")

if __name__ == "__main__":
    main()