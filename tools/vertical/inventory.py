import json
from pathlib import Path

from tools.base import BaseTool, ToolResult, tool
from tools.utils.dates import now_iso

_DATA_FILE = Path("data/inventory.json")


def _load() -> dict:
    if not _DATA_FILE.exists():
        return {}
    try:
        return json.loads(_DATA_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save(data: dict) -> None:
    _DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    _DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


@tool
class InventoryTool(BaseTool):
    name = "inventory"
    description = (
        "Gestiona inventario de productos. "
        "Úsala para consultar stock, actualizar cantidades "
        "y generar alertas de stock bajo."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "get_stock":
            return self._get_stock(**kwargs)
        if action == "update_stock":
            return self._update_stock(**kwargs)
        if action == "low_stock_alert":
            return self._low_stock_alert(**kwargs)
        if action == "add_product":
            return self._add_product(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _get_stock(self, product_id: str = None, category: str = None) -> ToolResult:
        data = _load()
        if product_id:
            prod = data.get(product_id)
            if not prod:
                return self._error(f"Producto '{product_id}' no encontrado")
            return self._success(
                f"{prod['name']} [{product_id}]: {prod['stock']} unidades",
                raw_data={"product_id": product_id, **prod},
            )
        items = list(data.values())
        if category:
            items = [i for i in items if i.get("category") == category]
        if not items:
            return self._success("Sin productos en inventario")
        lines = ["Inventario:"]
        for item in sorted(items, key=lambda x: x.get("name", "")):
            lines.append(f"  [{item.get('product_id','?')}] {item['name']}: {item['stock']} uds | ${item.get('price',0):,.2f}")
        return self._success("\n".join(lines), raw_data={"products": items})

    def _update_stock(
        self,
        product_id: str = "",
        quantity: int = 0,
        operation: str = "set",
    ) -> ToolResult:
        data = _load()
        prod = data.get(product_id)
        if not prod:
            return self._error(f"Producto '{product_id}' no encontrado")

        current = prod["stock"]
        if operation == "set":
            new_qty = quantity
        elif operation == "add":
            new_qty = current + quantity
        elif operation == "subtract":
            new_qty = current - quantity
            if new_qty < 0:
                return self._error(
                    f"Stock insuficiente: {current} unidades disponibles, "
                    f"se intentan restar {quantity}"
                )
        else:
            return self._error(f"Operación no válida: {operation}. Usa: set, add, subtract")

        prod["stock"] = new_qty
        prod["updated_at"] = now_iso()
        _save(data)
        return self._success(
            f"Stock de '{product_id}' actualizado a {new_qty} unidades",
            raw_data={"product_id": product_id, "stock": new_qty},
        )

    def _low_stock_alert(self, threshold: int = 10) -> ToolResult:
        data = _load()
        low_items = [p for p in data.values() if p.get("stock", 0) <= threshold]
        if not low_items:
            return self._success(f"Sin productos con stock ≤ {threshold} unidades")
        lines = [f"{len(low_items)} producto(s) con stock bajo (≤{threshold}):"]
        for item in sorted(low_items, key=lambda x: x.get("stock", 0)):
            lines.append(f"  ⚠ {item['name']}: {item['stock']} unidades")
        return self._success(
            "\n".join(lines),
            raw_data={"low_stock": low_items, "threshold": threshold},
        )

    def _add_product(
        self,
        product_id: str = "",
        name: str = "",
        initial_stock: int = 0,
        category: str = "",
        price: float = 0.0,
    ) -> ToolResult:
        data = _load()
        if product_id in data:
            return self._error(f"Producto '{product_id}' ya existe")
        data[product_id] = {
            "product_id": product_id,
            "name": name,
            "stock": initial_stock,
            "category": category,
            "price": price,
            "created_at": now_iso(),
            "updated_at": now_iso(),
        }
        _save(data)
        return self._success(
            f"Producto '{name}' agregado con {initial_stock} unidades",
            raw_data={"product_id": product_id, "name": name, "stock": initial_stock},
        )
