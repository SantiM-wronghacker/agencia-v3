import sys
import json
import datetime
import math

def calcular_iva(costo_mensual):
    return costo_mensual * 0.16  # IVA en México es del 16%

def calcular_total(costo_mensual, iva):
    return costo_mensual + iva

def calcular_descuento(costo_mensual, calificacion):
    if calificacion >= 4:
        return costo_mensual * 0.05  # Descuento del 5% para calificaciones 4 y 5
    else:
        return 0

def calcular_ganancia(costo_mensual, iva, descuento):
    return costo_mensual + iva - descuento

def main():
    if __name__ == "__main__":
        try:
            if len(sys.argv) == 1:
                proveedores = [
                    {"nombre": "Proveedor 1", "servicio": "Internet", "costo_mensual": 500, "calificacion": 4},
                    {"nombre": "Proveedor 2", "servicio": "Telefono", "costo_mensual": 300, "calificacion": 3},
                    {"nombre": "Proveedor 3", "servicio": "Electricidad", "costo_mensual": 800, "calificacion": 5},
                    {"nombre": "Proveedor 4", "servicio": "Agua", "costo_mensual": 200, "calificacion": 4},
                    {"nombre": "Proveedor 5", "servicio": "Gas", "costo_mensual": 400, "calificacion": 3}
                ]
            else:
                proveedores = json.loads(sys.argv[1])
            
            if len(proveedores) == 0:
                print("No hay proveedores registrados.")
                return
            
            print("ÁREA: HERRAMIENTAS")
            print("DESCRIPCIÓN: Gestiona y evalúa proveedores de servicios para una empresa.")
            print("TECNOLOGÍA: Python estándar")
            print("\nRanking de proveedores:")
            total_costo_mensual = 0
            total_iva = 0
            total_descuento = 0
            for i, proveedor in enumerate(proveedores):
                try:
                    iva = calcular_iva(proveedor["costo_mensual"])
                    descuento = calcular_descuento(proveedor["costo_mensual"], proveedor["calificacion"])
                    total_costo_mensual += proveedor["costo_mensual"]
                    total_iva += iva
                    total_descuento += descuento
                    ganancia = calcular_ganancia(proveedor["costo_mensual"], iva, descuento)
                    print(f"\nProveedor {i+1}: {proveedor['nombre']}")
                    print(f"Servicio: {proveedor['servicio']}")
                    print(f"Costo mensual: {proveedor['costo_mensual']}")
                    print(f"Calificación: {proveedor['calificacion']}")
                    print(f"IVA: {iva:.2f}")
                    print(f"Descuento: {descuento:.2f}")
                    print(f"Ganancia: {ganancia:.2f}")
                except KeyError as e:
                    print(f"Error: Faltan datos para el proveedor {proveedor['nombre']}.")
            
            print("\nResumen ejecutivo:")
            print(f"Total costo mensual: {total_costo_mensual:.2f}")
            print(f"Total IVA: {total_iva:.2f}")
            print(f"Total descuento: {total_descuento:.2f}")
            print(f"Ganancia total: {calcular_ganancia(total_costo_mensual, total_iva, total_descuento):.2f}")
        except json.JSONDecodeError:
            print("Error: El archivo JSON es inválido.")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()