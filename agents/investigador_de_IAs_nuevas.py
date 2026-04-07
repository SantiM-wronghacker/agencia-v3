import google.generativeai as genai
import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
from urllib.parse import urlparse

# --- Configuración ---
# Asegúrate de tener tu clave API de Google Gemini como variable de entorno.
# export GEMINI_API_KEY='TU_CLAVE_API'
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("La variable de entorno GEMINI_API_KEY no está configurada.")

genai.configure(api_key=GEMINI_API_KEY)

# Modelo a utilizar
MODEL_NAME = "gemini-1.5-flash" # Puedes cambiar a "gemini-1.5-pro" si necesitas más capacidad
model = genai.GenerativeModel(MODEL_NAME)

# Ruta al archivo de historial
HISTORY_FILE = "ai_news_history.json"

# Número de días para considerar información "reciente" (para evitar repeticiones)
RECENT_DAYS = 7

# Número máximo de resultados de búsqueda a procesar por día
MAX_SEARCH_RESULTS = 10

# Tiempo de espera entre solicitudes web para evitar ser bloqueado
REQUEST_DELAY_SECONDS = 2

# Agente de usuario para las solicitudes HTTP
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# --- Funciones Auxiliares ---

def load_history():
    """Carga el historial de resúmenes desde un archivo JSON."""
    if not os.path.exists(HISTORY_FILE):
        return {"last_run": None, "summaries": []}
    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"Advertencia: El archivo de historial '{HISTORY_FILE}' está corrupto. Creando uno nuevo.")
            return {"last_run": None, "summaries": []}

def save_history(history):
    """Guarda el historial de resúmenes en un archivo JSON."""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=4, ensure_ascii=False)

def clean_old_history(history):
    """Elimina las entradas de historial más antiguas que RECENT_DAYS."""
    cutoff_date = (datetime.now() - timedelta(days=RECENT_DAYS)).isoformat()
    history['summaries'] = [
        s for s in history['summaries']
        if s['date'] >= cutoff_date
    ]
    return history

def search_web(query):
    """
    Realiza una búsqueda web utilizando Google (simulado o a través de un proxy simple).
    Para un uso en producción, se recomienda una API de búsqueda como Google Custom Search API,
    Serper.dev, o SerpAPI. Este ejemplo usa una aproximación simple.
    """
    print(f"Buscando en la web: '{query}'")
    headers = {"User-Agent": USER_AGENT}
    search_url = f"https://www.google.com/search?q={query}&hl=es&gl=es"
    
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        # Google a menudo usa 'div' con data-hveid o 'a' con h3 dentro
        # Esta es una heurística y puede requerir ajuste si Google cambia su HTML
        for g in soup.find_all('div', class_='g'):
            link = g.find('a')
            title_tag = g.find('h3')
            snippet_tag = g.find('div', class_='VwiC3b') # Clase para el snippet
            
            if link and title_tag and snippet_tag:
                url = link['href']
                title = title_tag.text
                snippet = snippet_tag.text
                
                # Filtrar enlaces de Google relacionados, imágenes, etc.
                if url.startswith("http") and "google.com/search?" not in url:
                    results.append({'title': title, 'url': url, 'snippet': snippet})
                    if len(results) >= MAX_SEARCH_RESULTS * 2: # Obtener más de los que necesitamos, luego filtrar
                        break
        print(f"Encontrados {len(results)} resultados.")
        return results[:MAX_SEARCH_RESULTS] # Limitar a MAX_SEARCH_RESULTS
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la búsqueda web: {e}")
        return []

def extract_article_text(url):
    """Extrae el texto principal de un artículo de una URL."""
    print(f"Intentando extraer texto de: {url}")
    headers = {"User-Agent": USER_AGENT}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Intenta encontrar el contenido principal en tags comunes de artículos
        # Esto es una heurística, puede que no funcione para todos los sitios
        
        # Eliminar scripts, estilos, navegaciones, pie de página, etc.
        for unwanted_tag in soup(['script', 'style', 'nav', 'footer', 'aside', 'header', 'form']):
            unwanted_tag.decompose()

        main_content = []
        # Busca párrafos dentro de contenedores de artículo/contenido
        article_containers = soup.find_all(['article', 'main', 'div'], class_=['story-content', 'article-content', 'post-content', 'entry-content', 'body-text'])
        
        if not article_containers:
            # Si no se encuentran contenedores específicos, busca todos los párrafos
            article_containers = [soup] # Usa todo el documento como un contenedor

        for container in article_containers:
            for p in container.find_all('p'):
                text = p.get_text(strip=True)
                if text and len(text) > 50: # Solo párrafos con contenido significativo
                    main_content.append(text)
            
            # También busca encabezados
            for h_tag in container.find_all(['h1', 'h2', 'h3', 'h4']):
                text = h_tag.get_text(strip=True)
                if text and len(text) > 10:
                    main_content.append(text)


        article_text = "\n\n".join(main_content)
        
        if not article_text or len(article_text) < 200:
            print(f"Advertencia: No se pudo extraer suficiente texto del artículo en {url}. Longitud: {len(article_text)}")
            return None
        return article_text
    except requests.exceptions.RequestException as e:
        print(f"Error al extraer texto de {url}: {e}")
        return None
    except Exception as e:
        print(f"Error inesperado al procesar {url}: {e}")
        return None


def generate_summary(text_content, title):
    """Genera un resumen del texto usando Google Gemini."""
    prompt = (
        f"Eres un experto en inteligencia artificial. Lee el siguiente artículo titulado '{title}' y haz un resumen conciso "
        f"de los puntos más importantes y novedosos en el área de la inteligencia artificial. "
        f"Enfócate en lo que es realmente nuevo, innovador o tiene un impacto significativo. "
        f"El resumen debe ser de aproximadamente 100-200 palabras. "
        f"\n\nCONTENIDO DEL ARTÍCULO:\n\n{text_content}"
    )
    try:
        response = model.generate_content(prompt)
        # Acceder al texto de la respuesta, manejando posibles listas de partes
        if hasattr(response, 'text'):
            return response.text
        elif hasattr(response, 'parts') and response.parts:
            # Si la respuesta es una lista de partes, unirlas
            return "".join([part.text for part in response.parts if hasattr(part, 'text')])
        else:
            return "No se pudo generar el resumen."
    except Exception as e:
        print(f"Error al generar resumen con la IA: {e}")
        return None

def is_duplicate_content(new_summary, historical_summaries):
    """
    Compara el nuevo resumen con resúmenes históricos para evitar repetición.
    Utiliza el modelo de lenguaje para una comparación semántica.
    """
    if not historical_summaries:
        return False

    # Limitar la cantidad de resúmenes históricos enviados a la IA para evitar exceder el límite de tokens
    # Seleccionamos los 5 resúmenes más recientes y relevantes (quizás por longitud o contenido)
    recent_historical_summaries = [s['summary'] for s in historical_summaries[-5:]] # Solo los últimos 5
    
    historical_text = "\n".join([f"- {s}" for s in recent_historical_summaries])

    prompt = (
        "Analiza el siguiente 'NUEVO RESUMEN' y compáralo con los 'RESÚMENES HISTÓRICOS' proporcionados. "
        "Determina si el 'NUEVO RESUMEN' contiene información que es sustancialmente la misma o muy similar "
        "a alguna de las ya presentes en los 'RESÚMENES HISTÓRICOS', indicando una repetición significativa. "
        "Responde SOLO con 'SÍ' si es una repetición clara, o 'NO' si aporta información novedosa o sustancialmente diferente. "
        "No añadas explicaciones a la respuesta 'SÍ' o 'NO'."
        f"\n\nRESÚMENES HISTÓRICOS:\n{historical_text}"
        f"\n\nNUEVO RESUMEN:\n{new_summary}"
        "\n\n¿Es el NUEVO RESUMEN una repetición? (SÍ/NO):"
    )

    try:
        response = model.generate_content(prompt)
        response_text = ""
        if hasattr(response, 'text'):
            response_text = response.text.strip().upper()
        elif hasattr(response, 'parts') and response.parts:
            response_text = "".join([part.text for part in response.parts if hasattr(part, 'text')]).strip().upper()

        print(f"Verificación de duplicado de IA: '{response_text}'")
        return "SÍ" in response_text
    except Exception as e:
        print(f"Error al verificar duplicado con IA: {e}. Asumiendo que no es duplicado para continuar.")
        return False

# --- Lógica Principal del Agente ---

def run_daily_agent():
    """Ejecuta el agente para buscar, resumir y almacenar nuevas noticias de IA."""
    print(f"[{datetime.now().isoformat()}] Iniciando el agente de noticias de IA...")

    history = load_history()
    history = clean_old_history(history) # Limpiar entradas antiguas

    current_date = datetime.now().isoformat()
    if history['last_run'] and history['last_run'].split('T')[0] == current_date.split('T')[0]:
        print(f"El agente ya se ejecutó hoy ({current_date.split('T')[0]}). Saliendo.")
        return

    # Consulta de búsqueda para encontrar novedades
    search_query = "novedades inteligencia artificial OR IA hoy OR esta semana OR recientes"
    search_results = search_web(search_query)

    new_summaries_found = []
    processed_urls = set(s['source_url'] for s in history['summaries']) # URLs ya procesadas en el historial
    
    for i, result in enumerate(search_results):
        print(f"\nProcesando resultado {i+1}/{len(search_results)}: {result['title']}")
        
        url = result['url']
        # Normalizar URL para evitar duplicados como http vs https o www vs no-www
        parsed_url = urlparse(url)
        normalized_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
        
        if normalized_url in processed_urls:
            print(f"Saltando: URL ya procesada en el historial: {url}")
            continue

        time.sleep(REQUEST_DELAY_SECONDS) # Pausar para ser amable con los servidores

        article_text = extract_article_text(url)
        if not article_text:
            print(f"No se pudo extraer el texto principal de {url}. Saltando.")
            continue
        
        # Considerar si el artículo completo es muy corto antes de resumir
        if len(article_text) < 300: # Por ejemplo, si el texto es muy corto, puede que no valga la pena resumir
            print(f"Texto del artículo demasiado corto ({len(article_text)} caracteres) para generar un resumen significativo. Saltando.")
            continue

        summary = generate_summary(article_text, result['title'])
        if not summary:
            print(f"No se pudo generar un resumen para {result['title']}. Saltando.")
            continue
        
        # Verificar si el nuevo resumen es un duplicado semántico de los anteriores
        if is_duplicate_content(summary, history['summaries']):
            print(f"Resumen para '{result['title']}' es muy similar a uno ya existente. Saltando.")
            processed_urls.add(normalized_url) # Añadir al set para evitar reprocesar hoy
            continue

        print(f"\n--- Nuevo Resumen Importante ---")
        print(f"Título: {result['title']}")
        print(f"URL: {url}")
        print(f"Resumen:\n{summary}")
        print(f"-------------------------------")

        new_entry = {
            "date": current_date,
            "title": result['title'],
            "source_url": url,
            "summary": summary
        }
        history['summaries'].append(new_entry)
        new_summaries_found.append(new_entry)
        processed_urls.add(normalized_url) # Asegurarse de que esta URL no se procese de nuevo hoy

    history['last_run'] = current_date
    save_history(history)

    if new_summaries_found:
        print(f"\nAgente completado. Se encontraron y guardaron {len(new_summaries_found)} nuevas noticias.")
    else:
        print("\nAgente completado. No se encontraron noticias novedosas o no se pudieron procesar.")

# --- Ejecutar el Agente ---
if __name__ == "__main__":
    run_daily_agent()