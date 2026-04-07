#!/usr/bin/env python3
"""Diagnóstico rápido de salud de agentes."""
import json
import sys

def main():
    try:
        archivo = sys.argv[1] if len(sys.argv) > 1 else 'habilidades.json'
        with open(archivo, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Agentes no saludables
        no_ok = {name: info for name, info in data.items() if info.get('salud') != 'OK'}

        print(f"\n{'='*70}")
        print(f"DIAGNOSTICO DE AGENTES - Total: {len(data)}")
        print(f"{'='*70}\n")

        print(f"[NO SALUDABLES] ({len(no_ok)}):")
        if no_ok:
            for nombre, info in sorted(no_ok.items()):
                print(f"   - {nombre}")
                print(f"     Salud: {info.get('salud', 'DESCONOCIDO')}")
                print(f"     Categoria: {info.get('categoria', '?')}")
                print(f"     Conexión a Internet: {'Sí' if info.get('con_web', False) else 'No'}")
        else:
            print("   [OK] TODOS los agentes estan saludables")

        # Agentes sin internet
        sin_web = {name: info for name, info in data.items() if not info.get('con_web', False)}

        print(f"\n[SIN INTERNET] ({len(sin_web)}):")
        categorias_sin_web = {}
        for nombre, info in sin_web.items():
            cat = info.get('categoria', 'DESCONOCIDA')
            if cat not in categorias_sin_web:
                categorias_sin_web[cat] = []
            categorias_sin_web[cat].append(nombre)

        for cat in sorted(categorias_sin_web.keys()):
            agentes = categorias_sin_web[cat]
            print(f"   {cat} ({len(agentes)}):")
            for agente in sorted(agentes)[:5]:
                print(f"      - {agente}")
            if len(agentes) > 5:
                print(f"      ... y {len(agentes)-5} mas")

        # Resumen por categoría
        print(f"\n[RESUMEN POR CATEGORIA]:")
        categorias = {}
        for name, info in data.items():
            cat = info.get('categoria', 'SIN_CATEGORÍA')
            if cat not in categorias:
                categorias[cat] = {'total': 0, 'ok': 0, 'web': 0}
            categorias[cat]['total'] += 1
            if info.get('salud') == 'OK':
                categorias[cat]['ok'] += 1
            if info.get('con_web'):
                categorias[cat]['web'] += 1

        for cat in sorted(categorias.keys()):
            print(f"   {cat}:")
            print(f"     Total de agentes: {categorias[cat]['total']}")
            print(f"     Agentes saludables: {categorias[cat]['ok']} ({(categorias[cat]['ok'] / categorias[cat]['total']) * 100 if categorias[cat]['total'] > 0 else 0:.2f}%)")
            print(f"     Agentes con conexión a Internet: {categorias[cat]['web']} ({(categorias[cat]['web'] / categorias[cat]['total']) * 100 if categorias[cat]['total'] > 0 else 0:.2f}%)")

        # Resumen ejecutivo
        print(f"\n[RESUMEN EJECUTIVO]:")
        print(f"   Total de agentes: {len(data)}")
        print(f"   Agentes no saludables: {len(no_ok)} ({(len(no_ok) / len(data)) * 100 if len(data) > 0 else 0:.2f}%)")
        print(f"   Agentes sin conexión a Internet: {len(sin_web)} ({(len(sin_web) / len(data)) * 100 if len(data) > 0 else 0:.2f}%)")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()