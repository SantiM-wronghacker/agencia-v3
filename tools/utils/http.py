import httpx


class HTTPClient:
    def __init__(self, base_url: str = "", timeout: int = 30, headers: dict = None):
        self.base_url = base_url
        self.timeout = timeout
        self.headers = headers or {}

    def get(self, path: str, params: dict = None) -> dict | None:
        try:
            url = f"{self.base_url}{path}" if self.base_url else path
            with httpx.Client(timeout=self.timeout) as client:
                r = client.get(url, params=params, headers=self.headers)
                r.raise_for_status()
                return r.json()
        except Exception:
            return None

    def post(self, path: str, data: dict = None, json: dict = None) -> dict | None:
        try:
            url = f"{self.base_url}{path}" if self.base_url else path
            with httpx.Client(timeout=self.timeout) as client:
                r = client.post(url, data=data, json=json, headers=self.headers)
                r.raise_for_status()
                return r.json()
        except Exception:
            return None
