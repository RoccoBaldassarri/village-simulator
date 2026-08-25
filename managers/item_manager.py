import pygame


class ItemManager:
    def __init__(self):
        self.items = []

    def spawn_item(self, item):
        self.items.append(item)
        return item

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)

    def get_item_at(self, col: int, row: int):
        for item in self.items:
            if item.col == col and item.row == row:
                return item
        return None

    def get_nearest_item(self, from_col: int, from_row: int):
        if not self.items:
            return None
        return min(self.items, key=lambda it: abs(it.col - from_col) + abs(it.row - from_row))

    def draw(self, surface: pygame.Surface, tile_size: int):
        for item in self.items:
            item.draw(surface, tile_size)
