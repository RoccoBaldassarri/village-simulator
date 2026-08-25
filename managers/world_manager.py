import pygame

from managers.map_manager import MapManager
from managers.npc_manager import NPCManager
from managers.item_manager import ItemManager
from managers.physics_manager import PhysicsManager


class WorldManager:
    def __init__(self, map_path: str, tile_textures_paths: dict, npc_texture_path: str):
        self.map_manager = MapManager(map_path, tile_textures_paths)
        self.npc_manager = NPCManager(self.map_manager.tile_size, npc_texture_path)
        self.item_manager = ItemManager()
        self.physics_manager = PhysicsManager(self.map_manager, self.npc_manager)

    def can_move_to(self, col: int, row: int, mover=None) -> bool:
        return self.physics_manager.can_move_to(col, row, mover=mover)

    def is_static_walkable(self, col: int, row: int) -> bool:
        return self.map_manager.is_walkable(col, row)

    def get_map_dimensions(self) -> tuple:
        return self.map_manager.cols, self.map_manager.rows

    def spawn_npc(self, col: int, row: int):
        return self.npc_manager.spawn_npc(col, row)

    def despawn_npc(self, npc):
        self.npc_manager.despawn_npc(npc)

    def spawn_item(self, item):
        return self.item_manager.spawn_item(item)

    def get_item_at(self, col: int, row: int):
        return self.item_manager.get_item_at(col, row)

    def get_nearest_item(self, col: int, row: int):
        return self.item_manager.get_nearest_item(col, row)

    def collect_item(self, item):
        self.item_manager.remove_item(item)

    def update(self, dt: float):
        self.npc_manager.update(dt, self)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.map_manager.get_map_surface(), (0, 0))
        self.item_manager.draw(screen, self.map_manager.tile_size)
        self.npc_manager.draw(screen)