from tools.base import BaseTool, ToolResult, tool
from tools.utils.http import HTTPClient

_BASE = "https://api.trello.com/1"


@tool
class TrelloTool(BaseTool):
    name = "trello"
    description = (
        "Gestiona tarjetas y tableros en Trello. "
        "Úsala para crear tareas, mover cards "
        "y consultar el estado de proyectos."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "create_card":
            return self._create_card(**kwargs)
        if action == "move_card":
            return self._move_card(**kwargs)
        if action == "get_board":
            return self._get_board(**kwargs)
        if action == "get_lists":
            return self._get_lists(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _auth_params(self) -> dict:
        return {
            "key": self.credentials.get("api_key", ""),
            "token": self.credentials.get("token", ""),
        }

    def _check_credentials(self) -> ToolResult | None:
        if not self.credentials.get("api_key"):
            return self._error("Credencial api_key no configurada")
        if not self.credentials.get("token"):
            return self._error("Credencial token no configurada")
        return None

    def _create_card(
        self,
        list_id: str = "",
        name: str = "",
        description: str = "",
        due_date: str = None,
    ) -> ToolResult:
        err = self._check_credentials()
        if err:
            return err

        params: dict = {
            "idList": list_id,
            "name": name,
            "desc": description,
            **self._auth_params(),
        }
        if due_date:
            params["due"] = due_date

        client = HTTPClient(_BASE)
        resp = client.post("/cards", data=params)
        if not resp or "id" not in resp:
            return self._error(f"Error al crear card '{name}' en Trello")

        card_id = resp["id"]
        return self._success(
            f"Card '{name}' creada en Trello",
            raw_data={"card_id": card_id, "url": resp.get("url", "")},
        )

    def _move_card(self, card_id: str = "", list_id: str = "") -> ToolResult:
        err = self._check_credentials()
        if err:
            return err

        params = {"idList": list_id, **self._auth_params()}
        client = HTTPClient(_BASE)
        resp = client.post(f"/cards/{card_id}", data=params)
        if not resp or "id" not in resp:
            return self._error(f"Error al mover card {card_id} en Trello")

        return self._success(
            f"Card movida a lista {list_id}",
            raw_data={"card_id": card_id, "list_id": list_id},
        )

    def _get_board(self, board_id: str = "") -> ToolResult:
        err = self._check_credentials()
        if err:
            return err

        client = HTTPClient(_BASE)
        resp = client.get(f"/boards/{board_id}/cards", params=self._auth_params())
        if not resp:
            return self._error(f"Error al obtener tablero {board_id} de Trello")

        cards = resp if isinstance(resp, list) else resp.get("cards", [])
        lines = [f"Tablero {board_id} ({len(cards)} cards):"]
        for card in cards:
            name = card.get("name", "Sin nombre")
            list_name = card.get("idList", "?")
            lines.append(f"  - {name} (lista: {list_name})")

        return self._success("\n".join(lines), raw_data={"cards": cards})

    def _get_lists(self, board_id: str = "") -> ToolResult:
        err = self._check_credentials()
        if err:
            return err

        client = HTTPClient(_BASE)
        resp = client.get(f"/boards/{board_id}/lists", params=self._auth_params())
        if not resp:
            return self._error(f"Error al obtener listas del tablero {board_id}")

        lists = resp if isinstance(resp, list) else []
        lines = [f"Listas en tablero {board_id} ({len(lists)}):"]
        for lst in lists:
            lines.append(f"  - {lst.get('name', '?')} (ID: {lst.get('id', '?')})")

        return self._success("\n".join(lines), raw_data={"lists": lists})
