#!/usr/bin/env python3
# ÁREA: HERRAMIENTAS
# DESCRIPCIÓN: Agente que realiza generador de prompts optimizados
# TECNOLOGÍA: Python estándar

import sys
import json
import datetime
import math
import re
import random
import os

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def main():
    try:
        # Configuración de parámetros
        num_prompts = int(sys.argv[1]) if len(sys.argv) > 1 else 10
        longitud_min = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        longitud_max = int(sys.argv[3]) if len(sys.argv) > 3 else 20

        # Validación de parámetros
        if num_prompts <= 0:
            raise ValueError("El número de prompts debe ser mayor que 0")
        if longitud_min <= 0:
            raise ValueError("La longitud mínima debe ser mayor que 0")
        if longitud_max <= 0:
            raise ValueError("La longitud máxima debe ser mayor que 0")
        if longitud_min > longitud_max:
            raise ValueError("La longitud mínima no puede ser mayor que la longitud máxima")

        # Generación de prompts
        prompts = []
        for _ in range(num_prompts):
            longitud = random.randint(longitud_min, longitud_max)
            prompt = ''
            for _ in range(longitud):
                prompt += chr(random.randint(97, 122))  # Letras minúsculas
            prompts.append(prompt)

        # Impresión de resultados
        print(f"Fecha y hora actual: {datetime.datetime.now()}")
        print(f"Número de prompts generados: {len(prompts)}")
        print(f"Longitud mínima de los prompts: {longitud_min}")
        print(f"Longitud máxima de los prompts: {longitud_max}")
        print(f"Prompts generados:")
        for i, prompt in enumerate(prompts):
            print(f"{i+1}. {prompt}")
        print(f"Longitud promedio de los prompts: {sum(len(prompt) for prompt in prompts) / len(prompts):.2f}")
        print(f"Longitud máxima de los prompts generados: {max(len(prompt) for prompt in prompts)}")
        print(f"Longitud mínima de los prompts generados: {min(len(prompt) for prompt in prompts)}")
        print(f"Promedio de frecuencia de letras 'a' en los prompts: {sum(prompt.count('a') for prompt in prompts) / len(prompts):.2f}")
        print(f"Promedio de frecuencia de letras 'e' en los prompts: {sum(prompt.count('e') for prompt in prompts) / len(prompts):.2f}")
        print(f"Promedio de frecuencia de letras 'i' en los prompts: {sum(prompt.count('i') for prompt in prompts) / len(prompts):.2f}")
        print(f"Promedio de frecuencia de letras 'o' en los prompts: {sum(prompt.count('o') for prompt in prompts) / len(prompts):.2f}")
        print(f"Promedio de frecuencia de letras 'u' en los prompts: {sum(prompt.count('u') for prompt in prompts) / len(prompts):.2f}")

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"El agente ha generado {len(prompts)} prompts con longitudes entre {longitud_min} y {longitud_max} caracteres.")
        print(f"El promedio de frecuencia de letras 'a', 'e', 'i', 'o' y 'u' en los prompts es de {sum(prompt.count('a') for prompt in prompts) / len(prompts):.2f}, {sum(prompt.count('e') for prompt in prompts) / len(prompts):.2f}, {sum(prompt.count('i') for prompt in prompts) / len(prompts):.2f}, {sum(prompt.count('o') for prompt in prompts) / len(prompts):.2f} y {sum(prompt.count('u') for prompt in prompts) / len(prompts):.2f}, respectivamente.")

    except ValueError as e:
        print(f"Error de validación: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()