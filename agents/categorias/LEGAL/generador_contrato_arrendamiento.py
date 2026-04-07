"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Generador de contratos de arrendamiento
TECNOLOGÍA: Python, sys
"""
import datetime
import os
import sys
import time

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

class ContratoArrendamiento:
    def __init__(self, nombre_arrendador, direccion_arrendador, nombre_arrendatario, direccion_arrendatario):
        self.nombre_arrendador = nombre_arrendador
        self.direccion_arrendador = direccion_arrendador
        self.nombre_arrendatario = nombre_arrendatario
        self.direccion_arrendatario = direccion_arrendatario

    def generar_contrato(self, plazo_meses, renta_mensual, dias_pago, tiempo_aviso, ciudad, pais):
        contrato = f"""
CONTRATO DE ARRENDAMIENTO

Entre {self.nombre_arrendador}, con domicilio en {self.direccion_arrendador}, en su calidad de ARRENDADOR,
y {self.nombre_arrendatario}, con domicilio en {self.direccion_arrendatario}, en su calidad de ARRENDATARIO,

se ha convenido lo siguiente:

1. OBJETO DEL CONTRATO: El ARRENDADOR arrenda al ARRENDATARIO el inmueble ubicado en {self.direccion_arrendador},
por un plazo de {plazo_meses} meses, a partir de la fecha de firma de este contrato.

2. RENTA: La renta mensual será de ${renta_mensual}, pagadera dentro de los primeros {dias_pago} días de cada mes.

3. OBLIGACIONES DEL ARRENDATARIO: El ARRENDATARIO se compromete a:
- Pagar la renta en la fecha y forma convenidas.
- Mantener el inmueble en buen estado y realizar los reparos necesarios.
- No subarrendar el inmueble sin el consentimiento previo y por escrito del ARRENDADOR.

4. OBLIGACIONES DEL ARRENDADOR: El ARRENDADOR se compromete a:
- Entregar el inmueble en buen estado y libre de defectos.
- Realizar los reparos necesarios para mantener el inmueble en buen estado.

5. TERMINACIÓN DEL CONTRATO: El contrato podrá ser terminado por cualquiera de las partes con {tiempo_aviso} días de antelación.

6. LEY APLICABLE: Este contrato se regirá e interpretará de acuerdo con las leyes del {pais}.

7. JURISDICCIÓN: Cualquier disputa o controversia que surgiera en virtud de este contrato será sometida a los tribunales de {ciudad}.

En fe de lo cual, las partes firman este contrato en dos copias, en la ciudad de {ciudad}, a {datetime.date.today().day} de {datetime.date.today().strftime("%B")} de {datetime.date.today().year}.

ARRENDADOR: {self.nombre_arrendador}
ARRENDATARIO: {self.nombre_arrendatario}
"""
        return contrato


def main():
    if len(sys.argv) < 10:
        nombre_arrendador = "Juan Pérez"
        direccion_arrendador = "Calle 123, Colonia Centro"
        nombre_arrendatario = "María García"
        direccion_arrendatario = "Calle 456, Colonia Norte"
        plazo_meses = "12"
        renta_mensual = "10000"
        dias_pago = "5"
        tiempo_aviso = "30"
        ciudad = "Ciudad de México"
        pais = "México"
    else:
        nombre_arrendador = sys.argv[1]
        direccion_arrendador = sys.argv[2]
        nombre_arrendatario = sys.argv[3]
        direccion_arrendatario = sys.argv[4]
        plazo_meses = sys.argv[5]
        renta_mensual = sys.argv[6]
        dias_pago = sys.argv[7]
        tiempo_aviso = sys.argv[8]
        ciudad = sys.argv[9]
        pais = sys.argv[10]

    contrato = ContratoArrendamiento(nombre_arrendador, direccion_arrendador, nombre_arrendatario, direccion_arrendatario)
    print(contrato.generar_contrato(plazo_meses, renta_mensual, dias_pago, tiempo_aviso, ciudad, pais))

    nombre_archivo = f"contrato_{nombre_arrendador}_{nombre_arrendatario}_{datetime.date.today().strftime('%Y-%m-%d')}.txt"
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(contrato.generar_contrato(plazo_meses, renta_mensual, dias_pago, tiempo_aviso, ciudad, pais))
    print(f"Contrato guardado en el archivo {nombre_archivo}")
    time.sleep(2)

if __name__ == "__main__":
    main()