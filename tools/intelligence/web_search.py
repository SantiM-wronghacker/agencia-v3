from tools.base import BaseTool, ToolResult, tool

_DDG_URL = "https://api.duckduckgo.com/"
_SERPAPI_URL = "https://serpapi.com/search"


@tool
class WebSearchTool(BaseTool):
    name = "web_search"
    description = (
        "Busca información actualizada en internet. "
        "Úsala cuando necesites datos recientes, noticias "
        "o información que puede haber cambiado."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "search":
            return self._search(**kwargs)
        if action == "search_news":
            return self._search_news(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _search(self, query: str = "", num_results: int = 5) -> ToolResult:
        serpapi_key = self.credentials.get("serpapi_key")
        import httpx

        try:
            if serpapi_key:
                r = httpx.get(
                    _SERPAPI_URL,
                    params={"q": query, "api_key": serpapi_key, "num": num_results},
                    timeout=15,
                )
                r.raise_for_status()
                data = r.json()
                results = [
                    {
                        "title": item.get("title", ""),
                        "link": item.get("link", ""),
                        "snippet": item.get("snippet", ""),
                    }
                    for item in data.get("organic_results", [])[:num_results]
                ]
            else:
                r = httpx.get(
                    _DDG_URL,
                    params={"q": query, "format": "json", "no_html": 1, "skip_disambig": 1},
                    timeout=15,
                )
                r.raise_for_status()
                data = r.json()
                results = [
                    {
                        "title": item.get("Text", "")[:80],
                        "link": item.get("FirstURL", ""),
                        "snippet": item.get("Text", ""),
                    }
                    for item in data.get("RelatedTopics", [])[:num_results]
                    if item.get("FirstURL")
                ]

            if not results:
                return self._success(
                    f"Sin resultados para: {query}",
                    raw_data={"results": [], "query": query},
                )

            lines = []
            for i, res in enumerate(results, 1):
                lines.append(f"{i}. {res['title']}")
                if res.get("snippet") and res["snippet"] != res["title"]:
                    lines.append(f"   {res['snippet'][:120]}")
                lines.append(f"   URL: {res['link']}")
            return self._success(
                "\n".join(lines),
                raw_data={"results": results, "query": query},
            )
        except Exception as e:
            return self._error(f"Error en búsqueda: {e}")

    def _search_news(self, query: str = "", num_results: int = 5) -> ToolResult:
        serpapi_key = self.credentials.get("serpapi_key")
        import httpx

        try:
            if serpapi_key:
                r = httpx.get(
                    _SERPAPI_URL,
                    params={"q": query, "tbm": "nws", "api_key": serpapi_key,
                            "num": num_results},
                    timeout=15,
                )
                r.raise_for_status()
                data = r.json()
                results = [
                    {
                        "title": item.get("title", ""),
                        "link": item.get("link", ""),
                        "snippet": item.get("snippet", ""),
                        "date": item.get("date", ""),
                    }
                    for item in data.get("news_results", [])[:num_results]
                ]
            else:
                r = httpx.get(
                    _DDG_URL,
                    params={"q": query, "format": "json", "no_html": 1,
                            "skip_disambig": 1, "df": "w"},
                    timeout=15,
                )
                r.raise_for_status()
                data = r.json()
                results = [
                    {
                        "title": item.get("Text", "")[:80],
                        "link": item.get("FirstURL", ""),
                        "snippet": item.get("Text", ""),
                        "date": "",
                    }
                    for item in data.get("RelatedTopics", [])[:num_results]
                    if item.get("FirstURL")
                ]

            if not results:
                return self._success(
                    f"Sin noticias para: {query}",
                    raw_data={"results": [], "query": query},
                )

            lines = []
            for i, res in enumerate(results, 1):
                date_str = f" [{res['date']}]" if res.get("date") else ""
                lines.append(f"{i}. {res['title']}{date_str}")
                lines.append(f"   URL: {res['link']}")
            return self._success(
                "\n".join(lines),
                raw_data={"results": results, "query": query},
            )
        except Exception as e:
            return self._error(f"Error en búsqueda de noticias: {e}")
