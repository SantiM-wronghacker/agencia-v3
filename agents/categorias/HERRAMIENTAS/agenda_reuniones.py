"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente para gestionar una agenda de reuniones
TECNOLOGÍA: Python, Groq
"""

from llm_router import completar

def _groq_compat_create(**kwargs):
    """Compatibilidad con llamadas antiguas a client.chat.completions.create"""
    messages = kwargs.get('messages', [])
    temperatura = kwargs.get('temperature', 0.5)
    max_tokens = kwargs.get('max_tokens', 1000)

    class _Resp:
        class _Choice:
            class _Msg:
                content = ""
            message = _Msg()
        choices = [_Choice()]

    resultado = completar(messages, temperatura=temperatura, max_tokens=max_tokens)
    resp = _Resp()
    resp.choices[0].message.content = resultado or ""
    return resp

import sys
import time

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

class AgendaReuniones:
    def __init__(self):
        self.horarios_disponibles = []
        self.reuniones_agendadas = []
        self.api_key = 'GROQ_API_KEY_PLACEHOLDER'
        self.modelo = 'llama-3.3-70b-versatile'

    def agregar_horario_disponible(self, horario):
        self.horarios_disponibles.append(horario)

    def agregar_reunion(self, titulo, duracion):
        try:
            if not self.horarios_disponibles:
                print("No hay horarios disponibles agregados")
                return

            for horario in self.horarios_disponibles:
                if horario["disponible"]:
                    self.reuniones_agendadas.append({
                        "titulo": titulo,
                        "duracion": duracion,
                        "horario": horario["hora"]
                    })
                    horario["disponible"] = False
                    break
            else:
                print("No hay horarios disponibles para agregar la reunion")
        except Exception as e:
            print(f"Error al agregar reunion: {e}")

    def generar_agenda(self):
        try:
            with open("agenda.txt", "w", encoding='utf-8') as archivo:
                for reunion in self.reuniones_agendadas:
                    archivo.write(f"{reunion['horario']} - {reunion['titulo']} ({reunion['duracion']} minutos)\n")
            print("Agenda generada correctamente")
        except Exception as e:
            print(f"Error al generar agenda: {e}")

    def imprimir_agenda(self):
        try:
            for reunion in self.reuniones_agendadas:
                print(f"{reunion['horario']} - {reunion['titulo']} ({reunion['duracion']} minutos)")
        except Exception as e:
            print(f"Error al imprimir agenda: {e}")

    def obtener_sugerencias(self, texto):
        try:
            respuesta = groq.get_completion(
                model=self.modelo,
                prompt=texto,
                max_tokens=100,
                api_key=self.api_key
            )
            if respuesta:
                sugerencias = respuesta.text
                return sugerencias
            else:
                print(f"Error al obtener sugerencias")
                return None
        except Exception as e:
            print(f"Error al obtener sugerencias: {e}")
            return None

def main():
    agenda = AgendaReuniones()

    if len(sys.argv) > 1:
        hora = sys.argv[1]
        titulo = sys.argv[2]
        duracion = int(sys.argv[3])
        texto = sys.argv[4]
    else:
        hora = "09:00"
        titulo = "Reunion de trabajo"
        duracion = 60
        texto = "Reunion de trabajo"

    print(f"Horario: {hora}, Titulo: {titulo}, Duracion: {duracion} minutos, Texto: {texto}")

    agenda.agregar_horario_disponible({"hora": hora, "disponible": True})
    agenda.agregar_reunion(titulo, duracion)
    agenda.generar_agenda()
    agenda.imprimir_agenda()
    sugerencias = agenda.obtener_sugerencias(texto)
    if sugerencias:
        print("Sugerencias:")
        print(sugerencias)
    time.sleep(2)

if __name__ == "__main__":
    main()