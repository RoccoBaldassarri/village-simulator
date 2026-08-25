import pygame

from core.game_state import GameState
from core.config import MAP_PATH, TILE_TEXTURES, NPC_TEXTURE_PATH
from managers.world_manager import WorldManager
from entities.items.apple import Apple

class GameplayScene:
    def __init__(self, display_manager):
        self.display = display_manager
        self.next_state = None

        self.world = WorldManager(MAP_PATH, TILE_TEXTURES, NPC_TEXTURE_PATH)

        cols, rows = self.world.get_map_dimensions()
        self.world.spawn_npc(col=0, row=0)
        self.world.spawn_item(Apple(col=cols - 1, row=rows - 1))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.next_state = GameState.MENU

    def update(self, dt):
        self.world.update(dt)

    def draw(self):
        self.display.clear((0, 0, 0))
        self.world.draw(self.display.get_screen())
        self.display.draw_text(
            "ESC to return to main menu",
            (10, 10),
            font=self.display.font_small,
        )
