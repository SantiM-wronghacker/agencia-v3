"""
AREA: MARKETING
DESCRIPCION: Genera secuencia de 3 emails de seguimiento para prospectos inmobiliarios o de negocio. Personaliza según etapa del embudo: frío, tibio o caliente.
TECNOLOGIA: Python estándar
"""

import sys
import datetime
import random

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

def generar_precio(tipo_propiedad):
    precios = {
        'casa': 500000,
        'departamento': 300000,
        'terreno': 200000
    }
    return precios.get(tipo_propiedad.lower(), 0)

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

        tipo_propiedades_validas = ['casa', 'departamento', 'terreno']
        if tipo_propiedad.lower() not in tipo_propiedades_validas:
            raise ValueError(f'Tipo de propiedad debe ser: {", ".join(tipo_propiedades_validas)}')

        fecha_seguimiento = generar_fecha_seguimiento(etapa_funnel)
        prioridad = generar_prioridad(etapa_funnel)
        precio = generar_precio(tipo_propiedad)

        emails = [
            f'Hola {nombre_prospecto}, gracias por considerar nuestra {tipo_propiedad}. ¿Te gustaría agendar una visita?',
            f'Estimado {nombre_prospecto}, ¿necesitas más información sobre nuestra {tipo_propiedad} en {random.choice(["Zona Norte", "Centro", "Sur"])}, {random.choice(["CDMX", "Estado de México", "Querétaro"])}?',
            f'Sr. {nombre_prospecto}, su {tipo_propiedad} {etapa_funnel} está lista para ser visitada. ¿Qué día te conviene?'
        ]

        print(f'Nombre del prospecto: {nombre_prospecto}')
        print(f'Etapa del embudo: {etapa_funnel}')
        print(f'Tipo de propiedad: {tipo_propiedad}')
        print(f'Fecha de seguimiento: {fecha_seguimiento}')
        print(f'Prioridad: {prioridad}')
        print(f'Precio aproximado: ${precio:,.2f}')
        print('Secuencia de emails:')
        for i, email in enumerate(emails):
            print(f'Email {i+1}: {email}')
        print('Resumen ejecutivo:')
        print(f'El prospecto {nombre_prospecto} se encuentra en la etapa {etapa_funnel} del embudo y ha mostrado interés en una {tipo_propiedad}. Se le ha asignado una fecha de seguimiento para {fecha_seguimiento} y una prioridad de {prioridad}. El precio aproximado de la propiedad es de ${precio:,.2f}.')
    except ValueError as e:
        print(f'Error: {e}')
    except Exception as e:
        print(f'Error inesperado: {e}')

if __name__ == "__main__":
    main()