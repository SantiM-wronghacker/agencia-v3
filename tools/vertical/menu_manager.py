import json
from pathlib import Path

from tools.base import BaseTool, ToolResult, tool

_DATA_FILE = Path("data/menu.json")

_DEFAULT_MENU = {
    "entradas": [
        {"name": "Ensalada César", "price": 120.0, "description": "Lechuga romana, crutones, aderezo"},
        {"name": "Sopa de fideo", "price": 80.0, "description": "Caldo de pollo, fideos, verduras"},
    ],
    "platos_fuertes": [
        {"name": "Filete a la plancha", "price": 280.0, "description": "Con papas y ensalada"},
        {"name": "Pechuga en salsa", "price": 220.0, "description": "Salsa de hongos, arroz"},
    ],
    "bebidas": [
        {"name": "Agua de jamaica", "price": 40.0, "description": "1 litro"},
        {"name": "Refresco", "price": 35.0, "description": "355 ml"},
    ],
    "postres": [
        {"name": "Flan napolitano", "price": 70.0, "description": "Con cajeta"},
        {"name": "Pastel del día", "price": 85.0, "description": "Consultar sabores"},
    ],
    "especiales": [],
}


def _load() -> dict:
    if not _DATA_FILE.exists():
        return dict(_DEFAULT_MENU)
    try:
        return json.loads(_DATA_FILE.read_text(encoding="utf-8"))
    except Exception:
        return dict(_DEFAULT_MENU)


def _save(data: dict) -> None:
    _DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    _DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


@tool
class MenuManagerTool(BaseTool):
    name = "menu_manager"
    description = (
        "Gestiona el menú de restaurantes. "
        "Úsala para consultar, actualizar precios "
        "y agregar especiales del día."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "get_menu":
            return self._get_menu(**kwargs)
        if action == "update_price":
            return self._update_price(**kwargs)
        if action == "add_special":
            return self._add_special(**kwargs)
        if action == "remove_special":
            return self._remove_special(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _get_menu(self, category: str = None) -> ToolResult:
        menu = _load()
        if category:
            items = menu.get(category, [])
            if not items:
                return self._success(f"Categoría '{category}' vacía o no encontrada")
            lines = [f"=== {category.upper()} ==="]
            for item in items:
                lines.append(f"  • {item['name']} — ${item['price']:.2f}: {item.get('description','')}")
            return self._success("\n".join(lines), raw_data={category: items})

        lines = []
        for cat, items in menu.items():
            if items:
                lines.append(f"\n=== {cat.upper()} ===")
                for item in items:
                    lines.append(f"  • {item['name']} — ${item['price']:.2f}: {item.get('description','')}")
        return self._success("\n".join(lines) if lines else "Menú vacío", raw_data=menu)

    def _update_price(self, item_name: str = "", new_price: float = 0.0) -> ToolResult:
        menu = _load()
        for cat_items in menu.values():
            for item in cat_items:
                if item["name"].lower() == item_name.lower():
                    item["price"] = new_price
                    _save(menu)
                    return self._success(
                        f"Precio de '{item_name}' actualizado a ${new_price:.2f}"
                    )
        return self._error(f"'{item_name}' no encontrado en el menú")

    def _add_special(
        self,
        name: str = "",
        description: str = "",
        price: float = 0.0,
        category: str = "especiales",
    ) -> ToolResult:
        menu = _load()
        if category not in menu:
            menu[category] = []
        menu[category].append({"name": name, "description": description, "price": price})
        _save(menu)
        return self._success(f"Especial '{name}' agregado al menú por ${price:.2f}")

    def _remove_special(self, name: str = "") -> ToolResult:
        menu = _load()
        found = False
        for cat_items in menu.values():
            before = len(cat_items)
            cat_items[:] = [i for i in cat_items if i["name"].lower() != name.lower()]
            if len(cat_items) < before:
                found = True
        if not found:
            return self._error(f"'{name}' no encontrado en el menú")
        _save(menu)
        return self._success(f"'{name}' eliminado del menú")
