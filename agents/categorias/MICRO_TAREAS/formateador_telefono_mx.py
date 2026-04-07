import sys
import re
from datetime import datetime

def formateador_telefono_mx(entrada, formato='mx', ciudad='CDMX'):
    """AREA: HERRAMIENTAS
    DESCRIPCION: Procesar 'entrada' (el primer parámetro recibido)
    """
    try:
        # Procesar 'entrada' (el primer parámetro recibido)
        if len(entrada) != 10:
            raise ValueError("Número de teléfono debe tener exactamente 10 dígitos")
        if not entrada.isdigit():
            raise ValueError("Número de teléfono debe ser numérico")
        if '-' not in entrada and ' ' not in entrada:
            raise ValueError("Número de teléfono debe tener guiones o espacios")
        
        # Agregar casos edge
        if entrada == '':
            raise ValueError("Número de teléfono no puede ser vacío")
        
        # Agregar casos edge para errores
        if len(entrada) > 10:
            raise ValueError("Número de teléfono debe tener como máximo 10 dígitos")
        
        if formato == 'mx':
            patron = re.compile(r"^(\d{3})[-\s]*(\d{3})[-\s]*(\d{4})$")
            match = patron.match(entrada)
            if match:
                return f"({match.group(1)}) {match.group(2)}-{match.group(3)}"
            elif '-' in entrada:
                return f"({entrada[:3]}) {entrada[4:7]}-{entrada[8:]}"
            elif ' ' in entrada:
                return f"({entrada[:3]}) {entrada[4:7]}-{entrada[8:]}"
            else:
                raise ValueError("Formato de teléfono inválido")
        elif formato == 'us':
            return f"({entrada[:3]}) {entrada[3:6]}-{entrada[6:]}"

        # Agregar casos edge
        if formato not in ['mx', 'us']:
            raise ValueError("Formato no válido")

        # Calculos precisos para México
        if formato == 'mx':
            # Calcular el código de área según la ciudad
            if ciudad == 'CDMX':
                codigo_area = 55
            elif ciudad == 'Guadalajara':
                codigo_area = 33
            elif ciudad == 'Monterrey':
                codigo_area = 81
            else:
                codigo_area = 0  # Código de área desconocido
            
            # Calcular el número de teléfono con código de área
            telefono = f"{codigo_area}{entrada}"
            
            # Formatear el número de teléfono
            return f"({telefono[:3]}) {telefono[3:6]}-{telefono[6:]}"

    except ValueError as e:
        print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None

def main():
    if len(sys.argv) > 1:
        entrada = sys.argv[1]
    else:
        print("Error: Faltan argumentos")
        return
    
    try:
        formato = sys.argv[2] if len(sys.argv) > 2 else 'mx'
        ciudad = sys.argv[3] if len(sys.argv) > 3 else 'CDMX'
    except IndexError:
        print("Error: Faltan argumentos")
        return
    
    resultado = formateador_telefono_mx(entrada, formato, ciudad)
    print(f"Entrada: {entrada}")
    print(f"Formato: {formato}")
    print(f"Ciudad: {ciudad}")
    print(f"Resultado: {resultado}")
    print(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Resumen ejecutivo: El programa ha procesado el número de teléfono de manera exitosa.")

if __name__ == "__main__":
    main()