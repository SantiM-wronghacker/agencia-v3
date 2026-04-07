"""
AREA: MARKETING
DESCRIPCION: Genera secuencia de 3 emails de seguimiento para prospectos inmobiliarios o de negocio. Personaliza según etapa del embudo: frío, tibio o caliente.
TECNOLOGIA: Python estándar
"""

import sys
import datetime
import random

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def generar_fecha_seguimiento(etapa):
    if etapa.lower() == 'frío':
        return datetime.date.today() + datetime.timedelta(days=14)
    elif etapa.lower() == 'tibio':
        return datetime.date.today() + datetime.timedelta(days=7)
    else:  # caliente
        return datetime.date.today() + datetime.timedelta(days=3)

def generar_prioridad(etapa):
    prioridades = {
        'frío': 'Baja',
        'tibio': 'Media',
        'caliente': 'Alta'
    }
    return prioridades.get(etapa.lower(), 'Media')

def main():
    try:
        if len(sys.argv) == 4:
            nombre_prospecto = sys.argv[1]
            etapa_funnel = sys.argv[2]
            tipo_propiedad = sys.argv[3]
        else:
            nombre_prospecto = 'Juan'
            etapa_funnel = 'tibio'
            tipo_propiedad = 'casa'

        if not nombre_prospecto or not etapa_funnel or not tipo_propiedad:
            raise ValueError('Parámetros inválidos')

        etapas_validas = ['frío', 'tibio', 'caliente']
        if etapa_funnel.lower() not in etapas_validas:
            raise ValueError(f'Etapa del embudo debe ser: {", ".join(etapas_validas)}')

        emails = [
            f'Hola {nombre_prospecto}, gracias por considerar nuestra {tipo_propiedad}. ¿Te gustaría agendar una visita?',
            f'Estimado {nombre_prospecto}, ¿necesitas más información sobre nuestra {tipo_propiedad} en {random.choice(["Zona Norte", "Centro", "Sur"])}, {random.choice(["CDMX", "Estado de México", "Querétaro"])}?',
            f'Sr. {nombre_prospecto}, su {tipo_propiedad} {etapa_funnel} está lista para ser visitada. ¿Qué día te conviene más?'
        ]

        print(f'Fecha de hoy: {datetime.date.today()}')
        print(f'Nombre del prospecto: {nombre_prospecto}')
        print(f'Etapa del embudo: {etapa_funnel.capitalize()}')
        print(f'Tipo de propiedad: {tipo_propiedad}')
        print(f'Ubicación sugerida: {random.choice(["Residencial", "Comercial", "Industrial"])}')

        for i, email in enumerate(emails):
            print(f'Email {i+1}: {email}')

        print('\nResumen ejecutivo:')
        print(f'Prospecto: {nombre_prospecto} - Etapa: {etapa_funnel.capitalize()} - Propiedad: {tipo_propiedad}')
        print(f'Fecha de seguimiento: {generar_fecha_seguimiento(etapa_funnel)}')
        print(f'Prioridad: {generar_prioridad(etapa_funnel)}')
        print(f'Recomendación: {random.choice(["Contactar por WhatsApp", "Enviar catálogo digital", "Agendar visita presencial"])}')

    except Exception as e:
        print(f'Error: {e}')
    except IndexError:
        print('Error: No se proporcionaron los parámetros necesarios.')
    except ValueError as ve:
        print(f'Error de validación: {ve}')

if __name__ == "__main__":
    main()