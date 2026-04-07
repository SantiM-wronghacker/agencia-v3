"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Validador de leads para agencia inmobiliaria que clasifica clientes según presupuesto y urgencia
TECNOLOGÍA: Python
"""

import sys
import time

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

class Lead:
    def __init__(self, nombre, presupuesto, urgencia):
        self.nombre = nombre
        self.presupuesto = presupuesto
        self.urgencia = urgencia

    def calificar_leads(self):
        try:
            if self.presupuesto < 10000 and self.urgencia == "baja":
                return "Frio"
            elif (self.presupuesto >= 10000 and self.presupuesto < 50000) and (self.urgencia == "media" or self.urgencia == "baja"):
                return "Tibio"
            elif self.presupuesto >= 50000 and self.urgencia == "alta":
                return "Caliente"
            elif self.presupuesto >= 50000 and (self.urgencia == "media" or self.urgencia == "baja"):
                return "Tibio"
            elif self.presupuesto < 10000 and self.urgencia == "alta":
                return "Tibio"
            else:
                return "Frio"
        except Exception as e:
            return f"Error: {str(e)}"

class ValidadorLeads:
    def __init__(self):
        self.leads = []

    def agregar_lead(self, nombre, presupuesto, urgencia):
        lead = Lead(nombre, presupuesto, urgencia)
        self.leads.append(lead)

    def calificar_leads(self):
        total_leads = len(self.leads)
        leads_calientes = 0
        leads_tibios = 0
        leads_frios = 0
        for lead in self.leads:
            calificacion = lead.calificar_leads()
            print(f"Nombre: {lead.nombre}, Presupuesto: ${lead.presupuesto:,.2f}, Urgencia: {lead.urgencia}, Calificacion: {calificacion}")
            if calificacion == "Caliente":
                leads_calientes += 1
            elif calificacion == "Tibio":
                leads_tibios += 1
            elif calificacion == "Frio":
                leads_frios += 1
        print(f"\nResumen Ejecutivo:")
        print(f"Total de Leads: {total_leads}")
        print(f"Leads Calientes: {leads_calientes} ({leads_calientes/total_leads*100:.2f}%)")
        print(f"Leads Tibios: {leads_tibios} ({leads_tibios/total_leads*100:.2f}%)")
        print(f"Leads Frios: {leads_frios} ({leads_frios/total_leads*100:.2f}%)")

def main():
    if len(sys.argv) > 1:
        try:
            nombre = sys.argv[1]
            presupuesto = float(sys.argv[2])
            urgencia = sys.argv[3].lower()
            if urgencia not in ["alta", "media", "baja"]:
                urgencia = "media"
        except (ValueError, IndexError):
            print("Error: Parámetros incorrectos. Usando valores por defecto.")
            nombre = "Cliente"
            presupuesto = 50000
            urgencia = "media"
    else:
        print("No se proporcionaron argumentos. Usando valores por defecto.")
        nombre = "Cliente"
        presupuesto = 50000
        urgencia = "media"
    validador = ValidadorLeads()
    validador.agregar_lead(nombre, presupuesto, urgencia)
    validador.agregar_lead("Cliente2", 20000, "alta")
    validador.agregar_lead("Cliente3", 80000, "media")
    validador.agregar_lead("Cliente4", 30000, "baja")
    validador.calificar_leads()

if __name__ == "__main__":
    main()