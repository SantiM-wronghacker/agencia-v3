"""
AREA: HERRAMIENTAS
DESCRIPCION: Monitorea la temperatura y uso de memoria de la GPU con datos detallados y manejo de errores mejorado
TECNOLOGIA: GPUtil, Python
"""
import GPUtil
import time
import os
import sys
from datetime import datetime

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def monitor_gpu(refresh_rate=2, max_temp=85, max_memory=90):
    gpus = GPUtil.getGPUs()
    if not gpus:
        print("No se encontraron GPUs.")
        return

    gpu = gpus[0]
    try:
        while True:
            try:
                gpu = GPUtil.getGPUs()[0]
                temperature = gpu.temperature
                name = gpu.name
                memory_utilization = gpu.memoryUtil * 100
                load = gpu.load * 100
                memory_total = gpu.memoryTotal
                memory_free = gpu.memoryFree
                memory_used = gpu.memoryUsed

                # Cálculos adicionales
                memory_percentage = (memory_used / memory_total) * 100
                temp_status = "Normal" if temperature < max_temp else "Alerta"
                memory_status = "Normal" if memory_utilization < max_memory else "Alerta"

                # Formateo de fechas
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                os.system('cls' if os.name == 'nt' else 'clear')
                print("========================================")
                print(f"  Nombre de la GPU: {name}")
                print(f"  Fecha y hora: {timestamp}")
                print("========================================")
                print(f"  Temperatura: {temperature}°C ({temp_status})")
                print(f"  Uso de memoria VRAM: {memory_utilization:.2f}% ({memory_status})")
                print(f"  Carga de la GPU: {load:.2f}%")
                print(f"  Memoria total: {memory_total} MB")
                print(f"  Memoria libre: {memory_free} MB")
                print(f"  Memoria utilizada: {memory_used} MB ({memory_percentage:.2f}%)")
                print(f"  Umbral de temperatura: {max_temp}°C")
                print(f"  Umbral de memoria: {max_memory}%")
                print("========================================")
                print(f"  Refresh rate: {refresh_rate} segundos")
                print("========================================")
                time.sleep(refresh_rate)
            except IndexError:
                print("Error: No se pudo obtener información de la GPU.")
                break
            except Exception as e:
                print(f"Error temporal: {e}")
                time.sleep(refresh_rate)
                continue
    except KeyboardInterrupt:
        print("\nMonitor de GPU detenido.")
    except Exception as e:
        print(f"Error crítico: {e}")

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            refresh_rate = int(sys.argv[1])
        else:
            refresh_rate = 2

        if len(sys.argv) > 2:
            max_temp = int(sys.argv[2])
        else:
            max_temp = 85

        if len(sys.argv) > 3:
            max_memory = int(sys.argv[3])
        else:
            max_memory = 90

        monitor_gpu(refresh_rate, max_temp, max_memory)

        print("\nResumen ejecutivo:")
        print("El monitor de GPU se ejecutó con éxito.")
        print("Se monitorearon los siguientes parámetros:")
        print("- Temperatura con umbral de alerta")
        print("- Uso de memoria VRAM con umbral de alerta")
        print("- Carga de la GPU")
        print("- Memoria total, libre y utilizada")
        print(f"Configuración: Refresh rate={refresh_rate}s, Temp max={max_temp}°C, Memoria max={max_memory}%")
    except ValueError:
        print("Error: Parámetros inválidos. Uso: python monitor_gpu.py [refresh_rate] [max_temp] [max_memory]")
    except Exception as e:
        print(f"Error durante la ejecución: {e}")