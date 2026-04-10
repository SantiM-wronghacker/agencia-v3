from tools.base import BaseTool, ToolResult, tool

_HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; AgenciaBot/1.0)"}


@tool
class WebScraperTool(BaseTool):
    name = "web_scraper"
    description = (
        "Extrae contenido de páginas web. "
        "Úsala para obtener texto de artículos, "
        "precios, datos o cualquier contenido público."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "scrape":
            return self._scrape(**kwargs)
        if action == "extract_text":
            return self._extract_text(**kwargs)
        if action == "monitor_price":
            return self._monitor_price(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _scrape(self, url: str = "", selectors: dict = None) -> ToolResult:
        if not url.startswith("http"):
            return self._error(f"URL inválida: '{url}'. Debe comenzar con http:// o https://")
        try:
            import httpx
            from bs4 import BeautifulSoup
        except ImportError:
            return self._error(
                "beautifulsoup4 no instalado. Ejecuta: pip install beautifulsoup4"
            )
        try:
            r = httpx.get(url, timeout=15, headers=_HEADERS)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            if selectors:
                data = {}
                for key, sel in selectors.items():
                    el = soup.select_one(sel)
                    data[key] = el.get_text(strip=True) if el else ""
                return self._success(str(data), raw_data=data)
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()
            text = soup.get_text(separator="\n", strip=True)
            text = "\n".join(line for line in text.split("\n") if line.strip())
            return self._success(
                text[:3000],
                raw_data={"url": url, "length": len(text)},
            )
        except Exception as e:
            return self._error(f"Error scraping {url}: {e}")

    def _extract_text(self, url: str = "") -> ToolResult:
        if not url.startswith("http"):
            return self._error(f"URL inválida: '{url}'")
        try:
            import httpx
            from bs4 import BeautifulSoup
        except ImportError:
            return self._error(
                "beautifulsoup4 no instalado. Ejecuta: pip install beautifulsoup4"
            )
        try:
            r = httpx.get(url, timeout=15, headers=_HEADERS)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            for tag in soup(["script", "style", "nav", "footer", "header",
                              "aside", "form", "button", "iframe"]):
                tag.decompose()
            # Prefer main content tags
            main = soup.find("main") or soup.find("article") or soup.find("body")
            text = main.get_text(separator="\n", strip=True) if main else ""
            text = "\n".join(line for line in text.split("\n") if len(line.strip()) > 20)
            return self._success(
                text[:4000],
                raw_data={"url": url, "length": len(text)},
            )
        except Exception as e:
            return self._error(f"Error extrayendo texto de {url}: {e}")

    def _monitor_price(self, url: str = "", selector: str = "") -> ToolResult:
        if not url.startswith("http"):
            return self._error(f"URL inválida: '{url}'")
        if not selector:
            return self._error("El parámetro 'selector' es obligatorio")
        try:
            import httpx
            from bs4 import BeautifulSoup
        except ImportError:
            return self._error(
                "beautifulsoup4 no instalado. Ejecuta: pip install beautifulsoup4"
            )
        try:
            r = httpx.get(url, timeout=15, headers=_HEADERS)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            el = soup.select_one(selector)
            if not el:
                return self._error(f"Selector '{selector}' no encontrado en {url}")
            value = el.get_text(strip=True)
            return self._success(
                f"Valor en '{selector}': {value}",
                raw_data={"url": url, "selector": selector, "value": value},
            )
        except Exception as e:
            return self._error(f"Error monitoreando {url}: {e}")
