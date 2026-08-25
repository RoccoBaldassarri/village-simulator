class Inventory:
    def __init__(self):
        self.items: dict[str, int] = {}

    def add_item(self, item) -> None:
        self.items[item.name] = self.items.get(item.name, 0) + 1

    def count(self, item_name: str) -> int:
        return self.items.get(item_name, 0)

    def __str__(self) -> str:
        if not self.items:
            return "empty"
        return ", ".join(f"{name} x{qty}" for name, qty in self.items.items())
