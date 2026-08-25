import pygame
from entities.items.item import Item

#firt item test

class Apple(Item):
    name = "apple"

    def draw(self, surface, tile_size: int):
        center = (
            self.col * tile_size + tile_size // 2,
            self.row * tile_size + tile_size // 2,
        )
        radius = tile_size // 3
        pygame.draw.circle(surface, (200, 40, 40), center, radius)
        pygame.draw.circle(surface, (120, 20, 20), center, radius, width=2)