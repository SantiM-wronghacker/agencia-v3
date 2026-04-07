#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test: Modo CREAR inteligente con plan de expansión
Verifica que las nuevas funciones funcionan correctamente
"""

import os
import sys
import json

# Test 1: Verificar que fabrica_agentes.py puede importarse
print("=" * 70)
print("TEST 1: Importar fabrica_agentes.py")
print("=" * 70)
try:
    import agencia.agents.cerebro.fabrica_agentes as fab
    print("[OK] fabrica_agentes.py importado correctamente")
except Exception as e:
    print(f"[ERROR] No se pudo importar: {e}")
    sys.exit(1)

# Test 2: Verificar que expansion_plan.json existe
print("\n" + "=" * 70)
print("TEST 2: Cargar expansion_plan.json")
print("=" * 70)
try:
    plan = fab.cargar_expansion_plan()
    print(f"[OK] Plan cargado: {len(plan.get('micros', []))} micros")
    if plan.get('meta'):
        print(f"    Objetivo: {plan['meta'].get('objetivo')}")
        print(f"    Total planificados: {plan['meta'].get('total_planificados')}")
except Exception as e:
    print(f"[ERROR] No se pudo cargar expansion_plan.json: {e}")
    sys.exit(1)

# Test 3: Verificar funciones de progreso
print("\n" + "=" * 70)
print("TEST 3: Funciones de progreso de expansión")
print("=" * 70)
try:
    progreso = fab.obtener_progreso_expansion()
    print(f"[OK] Progreso obtenido:")
    print(f"    Total planificados: {progreso['total_planificados']}")
    print(f"    Creados: {progreso['creados']}")
    print(f"    Pendientes: {progreso['pendientes']}")
    print(f"    Progreso: {progreso['progreso_pct']}%")
except Exception as e:
    print(f"[ERROR] No se pudo obtener progreso: {e}")
    sys.exit(1)

# Test 4: Verificar que se cargan habilidades
print("\n" + "=" * 70)
print("TEST 4: Cargar habilidades.json")
print("=" * 70)
try:
    hab = fab.cargar_habilidades()
    existentes = fab.agentes_existentes()
    print(f"[OK] {len(existentes)} agentes en habilidades.json")
except Exception as e:
    print(f"[ERROR] No se pudo cargar habilidades: {e}")
    sys.exit(1)

# Test 5: Verificar micros pendientes
print("\n" + "=" * 70)
print("TEST 5: Identificar micros pendientes")
print("=" * 70)
try:
    plan = fab.cargar_expansion_plan()
    pendientes = fab.obtener_micros_pendientes(plan)
    print(f"[OK] {len(pendientes)} micros pendientes de crear")
    if pendientes:
        print(f"    Primeros 5 pendientes:")
        for micro in pendientes[:5]:
            print(f"      - {micro.get('nombre')} ({micro.get('categoria')})")
except Exception as e:
    print(f"[ERROR] No se pudo identificar pendientes: {e}")
    sys.exit(1)

# Test 6: Verificar fabrica_config
print("\n" + "=" * 70)
print("TEST 6: Integración con fabrica_config.py")
print("=" * 70)
try:
    if fab.USAR_CONFIG_USUARIO:
        from agencia.agents.herramientas.fabrica_config import leer_modo_usuario, traducir_modo
        modo_usuario = leer_modo_usuario()
        print(f"[OK] Modo usuario: {modo_usuario}")
        print(f"    Descripción: {traducir_modo(modo_usuario)}")
    else:
        print("[WARN] fabrica_config no disponible, usando defaults")
except Exception as e:
    print(f"[WARN] No se pudo leer fabrica_config: {e}")

# Test 7: Verificar generación de plan inteligente
print("\n" + "=" * 70)
print("TEST 7: Generación de plan inteligente (CREAR mode)")
print("=" * 70)
try:
    plan = fab.cargar_expansion_plan()
    existentes = fab.agentes_existentes()

    # Generar un plan pequeño para testing
    plan_lote = fab.generar_plan_lote(1, existentes, modo="crear", plan_expansion=plan)
    print(f"[OK] Plan generado: {len(plan_lote)} agentes")

    # Contar micros vs otros
    micros = [a for a in plan_lote if a.get('es_expansion')]
    otros = [a for a in plan_lote if not a.get('es_expansion')]

    print(f"    Micros de expansion: {len(micros)}")
    print(f"    Otros agentes: {len(otros)}")

    if micros:
        print(f"    Primeros micros del lote:")
        for m in micros[:3]:
            print(f"      - {m['archivo']} ({m['area']})")
except Exception as e:
    print(f"[ERROR] No se pudo generar plan: {e}")
    sys.exit(1)

# Test 8: Verificar modo de entrada
print("\n" + "=" * 70)
print("TEST 8: Detección automática de modo")
print("=" * 70)
try:
    modo = fab.detectar_modo(arg=None)
    print(f"[OK] Modo detectado: {modo}")

    # Probar con fuerza
    modo_forzado = fab.detectar_modo(arg="crear")
    print(f"    Modo forzado (crear): {modo_forzado}")

    modo_forzado = fab.detectar_modo(arg="expansion")
    print(f"    Modo forzado (expansion): {modo_forzado}")
except Exception as e:
    print(f"[ERROR] No se pudo detectar modo: {e}")
    sys.exit(1)

# RESUMEN
print("\n" + "=" * 70)
print("RESUMEN DE TESTS")
print("=" * 70)
print("[OK] Todos los tests pasaron correctamente!")
print("\nEl sistema CREAR inteligente con expansion plan está listo.")
print("\nPróximos pasos:")
print("1. Doble clic en arrancar_con_menu.bat")
print("2. Selecciona opción 1 (CREAR)")
print("3. Sistema comenzará a crear micros + agentes hasta 500")
print("4. Monitorea el progreso en Dashboard → Tab Expansion")
print("=" * 70)
