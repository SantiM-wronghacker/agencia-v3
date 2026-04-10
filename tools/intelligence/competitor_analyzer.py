from tools.base import BaseTool, ToolResult, tool


@tool
class CompetitorAnalyzerTool(BaseTool):
    name = "competitor_analyzer"
    description = (
        "Analiza sitios web de competidores. "
        "Úsala para investigar precios, contenido "
        "y estrategia de la competencia."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "analyze_website":
            return self._analyze_website(**kwargs)
        if action == "compare_social":
            return self._compare_social(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _analyze_website(self, url: str = "") -> ToolResult:
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
            r = httpx.get(url, timeout=15,
                          headers={"User-Agent": "Mozilla/5.0"})
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")

            title = soup.title.string.strip() if soup.title else "N/A"
            meta_desc = ""
            meta = soup.find("meta", attrs={"name": "description"})
            if meta:
                meta_desc = meta.get("content", "")[:200]

            h1s = [h.get_text(strip=True) for h in soup.find_all("h1")][:5]
            h2s = [h.get_text(strip=True) for h in soup.find_all("h2")][:8]

            all_links = soup.find_all("a", href=True)
            from urllib.parse import urlparse
            parsed = urlparse(url)
            base_domain = parsed.netloc
            internal = sum(1 for a in all_links if base_domain in a["href"] or a["href"].startswith("/"))
            external = len(all_links) - internal

            scripts = [s.get("src", "") for s in soup.find_all("script", src=True)]
            techs = []
            tech_map = {
                "wordpress": "WordPress", "wp-content": "WordPress",
                "jquery": "jQuery", "react": "React", "vue": "Vue.js",
                "angular": "Angular", "bootstrap": "Bootstrap",
                "shopify": "Shopify", "wix": "Wix",
            }
            for src in scripts:
                for key, name in tech_map.items():
                    if key in src.lower() and name not in techs:
                        techs.append(name)

            server = r.headers.get("server", "N/D")
            word_count = len(soup.get_text().split())

            lines = [
                f"=== ANÁLISIS: {url} ===",
                f"Título: {title}",
                f"Descripción: {meta_desc or 'N/A'}",
                f"Palabras aprox: {word_count:,}",
                f"Server: {server}",
                f"Tecnologías detectadas: {', '.join(techs) or 'N/D'}",
                f"Links internos: {internal} | externos: {external}",
                f"\nH1s: {' | '.join(h1s) or 'N/A'}",
                f"H2s: {' | '.join(h2s) or 'N/A'}",
            ]
            return self._success(
                "\n".join(lines),
                raw_data={
                    "url": url, "title": title, "technologies": techs,
                    "word_count": word_count, "internal_links": internal,
                    "external_links": external,
                },
            )
        except Exception as e:
            return self._error(f"Error analizando {url}: {e}")

    def _compare_social(self, accounts: list = None) -> ToolResult:
        if not accounts:
            return self._error("Se requiere al menos una cuenta en 'accounts'")
        try:
            import httpx
            from bs4 import BeautifulSoup
        except ImportError:
            return self._error(
                "beautifulsoup4 no instalado. Ejecuta: pip install beautifulsoup4"
            )
        results = []
        for account_url in accounts:
            if not account_url.startswith("http"):
                results.append({"url": account_url, "error": "URL inválida"})
                continue
            try:
                r = httpx.get(account_url, timeout=10,
                              headers={"User-Agent": "Mozilla/5.0"})
                soup = BeautifulSoup(r.text, "html.parser")
                title = soup.title.string.strip() if soup.title else account_url
                meta = soup.find("meta", attrs={"name": "description"})
                desc = meta.get("content", "")[:100] if meta else ""
                results.append({"url": account_url, "name": title, "description": desc})
            except Exception as e:
                results.append({"url": account_url, "error": str(e)})

        lines = ["=== COMPARATIVA REDES SOCIALES ==="]
        for r in results:
            if "error" in r:
                lines.append(f"\n• {r['url']}: Error — {r['error']}")
            else:
                lines.append(f"\n• {r['name']}")
                lines.append(f"  URL: {r['url']}")
                if r.get("description"):
                    lines.append(f"  Descripción: {r['description']}")
        return self._success("\n".join(lines), raw_data={"accounts": results})
