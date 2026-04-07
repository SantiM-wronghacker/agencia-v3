import sys
import json
import datetime
import math
import re
import os

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def obtener_hashtags():
    if len(sys.argv) > 1:
        return sys.argv[1].split(',')
    else:
        return ["#mexico", "#instagram", "#marketing", "#python", "#analizador", "#mexicomarketing", "#mexicodigital", "#mexicoinstagram", "#mexicoinfluencer"]

def obtener_hashtags_parametros():
    if len(sys.argv) > 1:
        return sys.argv[1].split(',')
    else:
        return []

def calcular_porcentaje_marketing(hashtags):
    try:
        marketing_hashtags = [hashtag for hashtag in hashtags if 'marketing' in hashtag.lower()]
        return (len(marketing_hashtags) / len(hashtags)) * 100 if len(hashtags) > 0 else 0
    except ZeroDivisionError:
        return 0
    except Exception as e:
        print(f"Error al calcular porcentaje de marketing: {e}")
        return 0

def calcular_porcentaje_mexico(hashtags):
    try:
        mexico_hashtags = [hashtag for hashtag in hashtags if 'mexico' in hashtag.lower()]
        return (len(mexico_hashtags) / len(hashtags)) * 100 if len(hashtags) > 0 else 0
    except ZeroDivisionError:
        return 0
    except Exception as e:
        print(f"Error al calcular porcentaje de México: {e}")
        return 0

def obtener_top_3_hashtags_largos(hashtags):
    try:
        return sorted(hashtags, key=lambda x: len(x), reverse=True)[:3]
    except Exception as e:
        print(f"Error al obtener top 3 hashtags más largos: {e}")
        return []

def obtener_hashtags_con_numeros(hashtags):
    try:
        return [hashtag for hashtag in hashtags if any(char.isdigit() for char in hashtag)]
    except Exception as e:
        print(f"Error al obtener hashtags con números: {e}")
        return []

def obtener_hashtags_con_caracteres_especiales(hashtags):
    try:
        return [hashtag for hashtag in hashtags if any(not char.isalnum() and not char.isspace() for char in hashtag)]
    except Exception as e:
        print(f"Error al obtener hashtags con caracteres especiales: {e}")
        return []

def obtener_resumen_ejecutivo(hashtags, porcentaje_marketing, porcentaje_mexico):
    return f"Resumen ejecutivo: {len(hashtags)} hashtags analizados, {porcentaje_marketing:.2f}% relacionados con marketing y {porcentaje_mexico:.2f}% relacionados con México."

def obtener_resumen_detallado(hashtags):
    return f"Hashtags con números: {len(obtener_hashtags_con_numeros(hashtags))} hashtags\nHashtags con caracteres especiales: {len(obtener_hashtags_con_caracteres_especiales(hashtags))} hashtags\nTop 3 hashtags más largos: {', '.join(obtener_top_3_hashtags_largos(hashtags))}"

def obtener_resumen_final(hashtags, porcentaje_marketing, porcentaje_mexico):
    return f"Resumen final: {len(hashtags)} hashtags analizados, {porcentaje_marketing:.2f}% relacionados con marketing y {porcentaje_mexico:.2f}% relacionados con México."

def calcular_poblacion_mexico(hashtags):
    try:
        mexico_hashtags = [hashtag for hashtag in hashtags if 'mexico' in hashtag.lower()]
        poblacion_mexico = 126344000  # Población de México según el INEGI
        return (len(mexico_hashtags) / poblacion_mexico) * 1000000
    except ZeroDivisionError:
        return 0
    except Exception as e:
        print(f"Error al calcular población de México: {e}")
        return 0

def main():
    print("AREA: HERRAMIENTAS")
    print("DESCRIPCION: Analizador Hashtags Instagram")
    print("TECNOLOGIA: Python")
    print()

    hashtags = obtener_hashtags_parametros()
    if not hashtags:
        hashtags = ["#mexico", "#instagram", "#marketing", "#python", "#analizador", "#mexicomarketing", "#mexicodigital", "#mexicoinstagram", "#mexicoinfluencer"]

    porcentaje_marketing = calcular_porcentaje_marketing(hashtags)