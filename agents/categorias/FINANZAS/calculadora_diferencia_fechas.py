"""
ÁREA: FINANZAS
DESCRIPCIÓN: calculadora diferencia fechas
TECNOLOGÍA: Python estándar
"""

import sys
import re
from datetime import datetime, timedelta

def calculadora_diferencia_fechas(entrada, *args):
    """Función pura, sin prints, sin side effects."""
    try:
        fecha1 = datetime.strptime(entrada.split('-')[0], '%Y-%m-%d')
        fecha2 = datetime.strptime(entrada.split('-')[1], '%Y-%m-%d')
        
        # Verificar si las fechas están en el rango válido
        if fecha1 > fecha2:
            return "INVALIDO:fecha_invalida"
        
        # Verificar si las fechas tienen el formato correcto
        if len(entrada.split('-')) != 2:
            return "INVALIDO:fecha_falta"
        
        # Verificar si las fechas están en el rango válido para México
        if fecha1 > datetime(2024, 3, 21) or fecha2 < datetime(2023, 1, 1):
            return "INVALIDO:fecha_invalida_mexico"
        
        # Calcular la diferencia en días
        diferencia = (fecha2 - fecha1).days
        
        # Calcular la diferencia en horas, minutos y segundos
        diferencia_horas = diferencia * 24
        diferencia_minutos = diferencia_horas * 60
        diferencia_segundos = diferencia_minutos * 60
        
        # Calcular la diferencia en porcentaje
        diferencia_porcentaje = (diferencia / ((datetime.now() - fecha1).days)) * 100
        
        # Calcular la diferencia en años
        diferencia_anios = (fecha2 - fecha1).days / 365
        
        # Calcular la fecha de hoy
        fecha_hoy = datetime.now()
        
        # Calcular la diferencia entre la fecha de hoy y la fecha 1
        diferencia_hasta_hoy = (fecha_hoy - fecha1).days
        
        # Calcular la diferencia en días laborables
        diferencia_dias_laborables = (fecha2 - fecha1).days - ((fecha2 - fecha1).days // 7)
        
        # Calcular la diferencia en semanas
        diferencia_semanas = (fecha2 - fecha1).days // 7
        
        # Calcular la diferencia en meses
        diferencia_meses = (fecha2.year - fecha1.year) * 12 + (fecha2.month - fecha1.month)
        
        # Devolver los resultados
        return f"""
ÁREA: FINANZAS
DESCRIPCIÓN: calculadora diferencia fechas
TECNOLOGÍA: Python estándar

Diferencia de {diferencia} días
Diferencia en horas: {diferencia_horas}
Diferencia en minutos: {diferencia_minutos}
Diferencia en segundos: {diferencia_segundos}
Diferencia en porcentaje: {diferencia_porcentaje}%
Diferencia en años: {diferencia_anios}
Diferencia entre la fecha de hoy y la fecha 1: {diferencia_hasta_hoy} días
Diferencia en días laborables: {diferencia_dias_laborables} días
Diferencia en semanas: {diferencia_semanas} semanas
Diferencia en meses: {diferencia_meses} meses

Resumen ejecutivo:
La diferencia entre las dos fechas es de {diferencia} días, lo que equivale a {diferencia_anios} años.
La diferencia en porcentaje es del {diferencia_porcentaje}%.
La diferencia en días laborables es de {diferencia_dias_laborables} días.
La diferencia en semanas es de {diferencia_semanas} semanas.
La diferencia en meses es de {diferencia_meses} meses.
"""
    
    except ValueError:
        return "INVALIDO:fecha_invalida"
    except Exception as e:
        return f"Ocurrió un error: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python calculadora_diferencia_fechas.py <fecha1> <fecha2>")
    else:
        entrada = sys.argv[1] + "-" + sys.argv[2]
        resultado = calculadora_diferencia_fechas(entrada)
        print(resultado)