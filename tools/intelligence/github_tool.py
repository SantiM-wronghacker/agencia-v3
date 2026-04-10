from tools.base import BaseTool, ToolResult, tool

_BASE = "https://api.github.com"


@tool
class GitHubTool(BaseTool):
    name = "github_tool"
    description = (
        "Interactúa con repositorios de GitHub. "
        "Úsala para crear issues, ver PRs "
        "y obtener información de repos."
    )

    def _get_headers(self) -> dict | None:
        token = self.credentials.get("github_token")
        if not token:
            return None
        return {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "create_issue":
            return self._create_issue(**kwargs)
        if action == "get_issues":
            return self._get_issues(**kwargs)
        if action == "get_repo_info":
            return self._get_repo_info(**kwargs)
        if action == "create_pr_summary":
            return self._create_pr_summary(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _create_issue(
        self, repo: str = "", title: str = "", body: str = "", labels: list = None
    ) -> ToolResult:
        headers = self._get_headers()
        if not headers:
            return self._error("Credencial GitHub no configurada: github_token")
        import httpx

        try:
            r = httpx.post(
                f"{_BASE}/repos/{repo}/issues",
                json={"title": title, "body": body, "labels": labels or []},
                headers=headers,
                timeout=15,
            )
            r.raise_for_status()
            data = r.json()
            return self._success(
                f"Issue creado: #{data['number']} — {title}\n"
                f"URL: {data['html_url']}",
                raw_data={"number": data["number"], "url": data["html_url"]},
            )
        except Exception as e:
            return self._error(f"Error GitHub: {e}")

    def _get_issues(self, repo: str = "", state: str = "open") -> ToolResult:
        headers = self._get_headers()
        if not headers:
            return self._error("Credencial GitHub no configurada: github_token")
        import httpx

        try:
            r = httpx.get(
                f"{_BASE}/repos/{repo}/issues",
                params={"state": state, "per_page": 20},
                headers=headers,
                timeout=15,
            )
            r.raise_for_status()
            issues = r.json()
            lines = [
                f"#{i['number']} {i['title']} ({i['state']})"
                for i in issues
                if "pull_request" not in i
            ]
            return self._success(
                "\n".join(lines) if lines else "Sin issues",
                raw_data={"issues": issues},
            )
        except Exception as e:
            return self._error(f"Error GitHub: {e}")

    def _get_repo_info(self, repo: str = "") -> ToolResult:
        headers = self._get_headers()
        if not headers:
            return self._error("Credencial GitHub no configurada: github_token")
        import httpx

        try:
            r = httpx.get(f"{_BASE}/repos/{repo}", headers=headers, timeout=15)
            r.raise_for_status()
            d = r.json()
            return self._success(
                f"Repo: {d['full_name']}\n"
                f"Descripción: {d.get('description', '')}\n"
                f"Stars: {d['stargazers_count']} | Forks: {d['forks_count']}\n"
                f"Lenguaje: {d.get('language', '')}\n"
                f"Issues abiertos: {d['open_issues_count']}",
                raw_data=d,
            )
        except Exception as e:
            return self._error(f"Error GitHub: {e}")

    def _create_pr_summary(self, repo: str = "", pr_number: int = 0) -> ToolResult:
        headers = self._get_headers()
        if not headers:
            return self._error("Credencial GitHub no configurada: github_token")
        import httpx

        try:
            r = httpx.get(
                f"{_BASE}/repos/{repo}/pulls/{pr_number}",
                headers=headers,
                timeout=15,
            )
            r.raise_for_status()
            pr = r.json()
            return self._success(
                f"PR #{pr_number}: {pr['title']}\n"
                f"Estado: {pr['state']} | Merged: {pr.get('merged', False)}\n"
                f"Cambios: +{pr.get('additions', 0)} -{pr.get('deletions', 0)}\n"
                f"Archivos: {pr.get('changed_files', 0)}\n"
                f"Autor: {pr['user']['login']}",
                raw_data=pr,
            )
        except Exception as e:
            return self._error(f"Error GitHub: {e}")
