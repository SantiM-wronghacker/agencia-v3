import google.generativeai as genai
import os
import argparse

def setup_generative_model():
    """
    Configura la API de Google Generative AI y devuelve el modelo.
    Requiere que la variable de entorno GOOGLE_API_KEY esté configurada.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "ERROR: La variable de entorno GOOGLE_API_KEY no está configurada.\n"
            "Por favor, configúrala con tu clave de API de Google Gemini."
        )
    genai.configure(api_key=api_key)
    # Puedes elegir entre modelos como 'gemini-pro', 'gemini-1.5-flash', etc.
    # 'gemini-pro' es un buen punto de partida general.
    model = genai.GenerativeModel('gemini-pro')
    return model

def read_process_description(file_path: str) -> str | None:
    """
    Lee el contenido de un archivo de texto que describe un proceso empresarial.

    Args:
        file_path (str): La ruta al archivo de texto.

    Returns:
        str | None: El contenido del archivo como una cadena, o None si hay un error.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no fue encontrado.")
        return None
    except Exception as e:
        print(f"Error al leer el archivo '{file_path}': {e}")
        return None

def create_automation_prompt(process_description_text: str) -> str:
    """
    Crea el prompt para el modelo de IA, instruyéndole sobre cómo generar
    la propuesta de automatización paso a paso en Python.

    Args:
        process_description_text (str): El texto que describe el proceso empresarial.

    Returns:
        str: El prompt completo para el modelo de IA.
    """
    prompt = f"""
    Eres un agente experto en automatización de procesos empresariales. Tu misión es leer la descripción de un proceso de una empresa y proponer una automatización paso a paso utilizando Python.

    El objetivo es convertir el proceso manual descrito en un flujo de trabajo automatizado, identificando las tareas clave que pueden ser programadas y ofreciendo ejemplos de código Python.

    Aquí está la descripción del proceso empresarial:
    ---
    {process_description_text}
    ---

    Por favor, propone una automatización paso a paso en Python. Para cada paso, incluye:
    1.  Una breve descripción del objetivo del paso.
    2.  Un ejemplo de código Python que ilustre cómo se podría implementar ese paso. Si un paso es complejo o requiere decisiones humanas, explica cómo se podría integrar la lógica de decisión o qué bibliotecas de Python podrían ser útiles. Asegúrate de que el código sea claro y explicativo, usando pseudocódigo o ejemplos funcionales simples cuando sea apropiado.

    Estructura tu respuesta de la siguiente manera:

    **Propuesta de Automatización del Proceso**

    **Visión General:**
    [Breve resumen de la propuesta, los beneficios esperados y el enfoque general de la automatización.]

    **Pasos de Automatización en Python:**

    **Paso 1: [Nombre Descriptivo del Paso]**
    Descripción: [Detalles del objetivo de este paso y su lógica.]
    Código Python (Ejemplo):
    
    # Importar bibliotecas necesarias para este paso (si aplica)
    # Ej: import pandas as pd, import requests
    
    # Código de ejemplo para el Paso 1
    # Asegúrate de usar docstrings y comentarios para explicar el código.
    def ejecutar_paso_1():
        print("Implementando el Paso 1: Inicialización o adquisición de datos...")
        # Lógica de ejemplo:
        # datos = obtener_datos_de_fuente_externa()
        # return datos
    
    # if __name__ == "__main__":
    #    ejecutar_paso_1()
    

    **Paso 2: [Nombre Descriptivo del Paso]**
    Descripción: [Detalles del objetivo de este paso y su lógica.]
    Código Python (Ejemplo):
    
    # Código de ejemplo para el Paso 2
    def ejecutar_paso_2(datos_previos):
        print("Implementando el Paso 2: Procesamiento o transformación...")
        # Lógica de ejemplo:
        # datos_procesados = limpiar_y_transformar(datos_previos)
        # return datos_procesados
    
    ... (Continúa con tantos pasos como sean necesarios para cubrir todo el proceso)

    **Paso N: [Nombre Descriptivo del Paso Final]**
    Descripción: [Detalles del objetivo del paso final, como generación de informes o notificaciones.]
    Código Python (Ejemplo):
    
    # Código de ejemplo para el Paso Final
    def ejecutar_paso_final(resultados):
        print("Implementando el Paso Final: Entrega o almacenamiento...")
        # Lógica de ejemplo:
        # generar_informe_pdf(resultados)
        # enviar_correo_electronico(informe_pdf)
    

    Consideraciones Adicionales:
    [Cualquier nota sobre dependencias de bibliotecas, manejo de errores, seguridad, escalabilidad, monitoreo o futuras mejoras.]
    """
    return prompt

def generate_automation_proposal(model, prompt: str) -> str | None:
    """
    Envía el prompt al modelo de IA y recupera la propuesta de automatización.

    Args:
        model: El modelo de Google Generative AI configurado.
        prompt (str): El prompt completo a enviar al modelo.

    Returns:
        str | None: El texto de la propuesta generada por la IA, o None si hay un error.
    """
    try:
        # Generamos el contenido. Para outputs potencialmente largos,
        # podríamos usar streaming (stream=True) y concatenar los chunks.
        # Por simplicidad, aquí esperamos la respuesta completa.
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error al generar la propuesta con la IA: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Agente de Automatización de Procesos Empresariales.\n"
            "Lee un archivo de texto describiendo un proceso y propone una "
            "automatización paso a paso en Python usando IA."
        )
    )
    parser.add_argument(
        "file_path",
        type=str,
        help="Ruta al archivo de texto que describe el proceso empresarial."
    )
    args = parser.parse_args()

    try:
        model = setup_generative_model()
    except ValueError as e:
        print(e)
        exit(1)

    print(f"\nLeyendo el archivo de proceso: '{args.file_path}'...")
    process_text = read_process_description(args.file_path)

    if process_text:
        print("\nGenerando propuesta de automatización con IA. Esto puede tomar un momento...")
        prompt = create_automation_prompt(process_text)
        automation_proposal = generate_automation_proposal(model, prompt)

        if automation_proposal:
            print("\n" + "=" * 80)
            print("                 PROVUESTA DE AUTOMATIZACIÓN GENERADA                 ")
            print("=" * 80)
            print(automation_proposal)
            print("=" * 80)
            print("\n¡La propuesta ha sido generada con éxito!")
        else:
            print("\nNo se pudo generar la propuesta de automatización. Revisa los logs de error.")
    else:
        print("\nNo se pudo leer el archivo de descripción del proceso. Por favor, verifica la ruta y permisos.")

if __name__ == "__main__":
    main()