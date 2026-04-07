import os
import sys
import json
import datetime
import math
import re
import random

def main():
    if __name__ == "__main__":
        try:
            # Obtener parámetros desde la línea de comandos
            nombre_empresa = sys.argv[1] if len(sys.argv) > 1 else "Agencia Santi"
            direccion_empresa = sys.argv[2] if len(sys.argv) > 2 else "Calle Ejemplo 123, Ciudad de México"
            telefono_empresa = sys.argv[3] if len(sys.argv) > 3 else "55 1234 5678"
            correo_empresa = sys.argv[4] if len(sys.argv) > 4 else "info@agenciasanti.com"
            fecha_actual = datetime.date.today().strftime("%d/%m/%Y")
            hora_actual = datetime.datetime.now().strftime("%H:%M:%S")

            # Obtener fechas de inicio y fin (opcional)
            if len(sys.argv) > 5:
                try:
                    fecha_inicio = datetime.datetime.strptime(sys.argv[5], "%Y-%m-%d").date()
                    fecha_fin = datetime.datetime.strptime(sys.argv[6], "%Y-%m-%d").date()
                except ValueError:
                    print("Error: Fecha debe estar en formato YYYY-MM-DD")
                    return
            else:
                fecha_inicio = None
                fecha_fin = None

            # Obtener datos de la empresa desde la web (opcional)
            if len(sys.argv) > 7:
                datos_empresa = sys.argv[7]
                direccion_empresa = datos_empresa.get('direccion') if datos_empresa else direccion_empresa
                telefono_empresa = datos_empresa.get('telefono') if datos_empresa else telefono_empresa
                correo_empresa = datos_empresa.get('correo') if datos_empresa else correo_empresa

            # Generar aviso de privacidad
            aviso_privacidad = f"""
            ÁREA: FINANZAS
            DESCRIPCIÓN: Agente que realiza generador aviso privacidad
            TECNOLOGÍA: Python estándar

            Aviso de Privacidad de {nombre_empresa}

            {nombre_empresa} con domicilio en {direccion_empresa}, es responsable del tratamiento de tus datos personales.
            Nuestro objetivo es proteger tu información y garantizar que se utilice de manera segura y ética.

            Información recopilada:
            - Nombre y apellido
            - Dirección de correo electrónico
            - Número de teléfono
            - Fecha de nacimiento

            Uso de tus datos:
            - Para prestar servicios financieros
            - Para enviar comunicaciones y promociones
            - Para mejorar nuestros productos y servicios

            Acceso y modificación de tus datos:
            - Puedes acceder a tus datos personales en cualquier momento
            - Puedes solicitar la modificación o eliminación de tus datos

            Protección de tus datos:
            - Utilizamos medidas de seguridad para proteger tus datos
            - Limitamos el acceso a tus datos a personal autorizado

            Reclamo y contacto:
            - Si tienes alguna pregunta o inquietud sobre nuestro aviso de privacidad, por favor contacta con nosotros en {correo_empresa}

            Fecha de actualización: {fecha_actual}
            Hora de actualización: {hora_actual}

            Resumen ejecutivo:
            Nuestro objetivo es proporcionar servicios financieros de alta calidad y seguridad. Este aviso de privacidad se aplica a todos los servicios que ofrecemos.
            """

            print(aviso_privacidad)

        except IndexError:
            print("Error: Faltan parámetros en la línea de comandos")
            return

if __name__ == "__main__":
    main()