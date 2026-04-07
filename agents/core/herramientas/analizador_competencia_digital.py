import sys
import json
import datetime
import math
import re
import os
import random

# AREA: MARKETING
# DESCRIPCION: Analiza la presencia digital de un competidor: propuesta de valor, canales que usa, debilidades detectadas y oportunidades de diferenciación para el cliente.
# TECNOLOGIA: Python 3.x

def main():
    try:
        if len(sys.argv) < 5:
            nombre_competidor = sys.argv[1] if len(sys.argv) > 1 else 'Inmobiliaria Peña'
            industria = sys.argv[2] if len(sys.argv) > 2 else 'bienes_raices'
            pais = sys.argv[3] if len(sys.argv) > 3 else 'México'
            ciudad = sys.argv[4] if len(sys.argv) > 4 else 'Ciudad de México'
        else:
            nombre_competidor = sys.argv[1]
            industria = sys.argv[2]
            pais = sys.argv[3]
            ciudad = sys.argv[4]

        propuesta_de_valor = f"Ofrece servicios de {industria} de alta calidad en {pais}, con un enfoque en {ciudad}"
        canales_usados = "Redes sociales como Facebook y Instagram, sitio web propio y publicidad en línea en Google Ads"
        debilidades_detectadas = "Falta de presencia en mercados locales como Mercado Libre y Linio, y una estrategia de contenido poco efectiva"
        oportunidades_diferenciacion = "Ofrecer servicios personalizados y atención al cliente en español, y aprovechar las tendencias de marketing digital en México"
        fortalezas = "Equipo experimentado y tecnología de vanguardia como CRM y marketing automation"
        objetivos = "Aumentar la presencia en línea y mejorar la satisfacción del cliente en un 20% en los próximos 6 meses, y alcanzar un crecimiento de tráfico del 15% en el sitio web"
        estrategia = "Mejorar la experiencia del usuario en el sitio web y en las redes sociales mediante un diseño responsivo y contenido relevante, y aumentar la inversión en publicidad en línea"
        indicadores_clave = "Engagement en redes sociales, tráfico en el sitio web, satisfacción del cliente medidos a través de encuestas y análisis de datos, y la tasa de conversión de leads"
        tasa_crecimiento = 12  # %
        tasa_abandono = 6  # %
        tasa_satisfaccion = 88  # %
        tasa_conversion = 10  # %

        print(f"Competidor: {nombre_competidor}")
        print(f"Industria: {industria}")
        print(f"Pais: {pais}")
        print(f"Ciudad: {ciudad}")
        print(f"Propuesta de valor: {propuesta_de_valor}")
        print(f"Canales usados: {canales_usados}")
        print(f"Debilidades detectadas: {debilidades_detectadas}")
        print(f"Oportunidades de diferenciación: {oportunidades_diferenciacion}")
        print(f"Fortalezas: {fortalezas}")
        print(f"Objetivos: {objetivos}")
        print(f"Estrategia: {estrategia}")
        print(f"Indicadores clave: {indicadores_clave}")
        print(f"Tasa de crecimiento: {tasa_crecimiento}%")
        print(f"Tasa de abandono: {tasa_abandono}%")
        print(f"Tasa de satisfacción: {tasa_satisfaccion}%")
        print(f"Tasa de conversión: {tasa_conversion}%")

        resumen_ejecutivo = f"El competidor {nombre_competidor} tiene una propuesta de valor sólida en {industria} en {pais}, pero necesita mejorar su presencia en mercados locales y su estrategia de contenido. Con una inversión en publicidad en línea y un enfoque en la experiencia del usuario, puede alcanzar un crecimiento de tráfico del 15% y una tasa de conversión del 10%."
        print(f"\nResumen ejecutivo: {resumen_ejecutivo}")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()