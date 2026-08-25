import pygame

from managers.map_manager import MapManager
from managers.npc_manager import NPCManager
from managers.physics_manager import PhysicsManager


class WorldManager:
    """
    Il Coordinatore (Facade).

    Racchiude MapManager, NPCManager e PhysicsManager e fa da UNICO punto
    di contatto tra "il mondo di gioco" e qualsiasi attore esterno (oggi gli
    NPC, in futuro il player). Nessuno fuori da questo file dovrebbe
    importare MapManager/PhysicsManager/NPCManager direttamente: si passa
    sempre da qui.

    Ordine di creazione (importante per evitare dipendenze circolari):
      1. MapManager     -> non dipende da nessuno.
      2. NPCManager      -> dipende solo da tile_size (di MapManager).
      3. PhysicsManager -> dipende da MapManager + NPCManager.
    """

    def __init__(self, map_path: str, tile_textures_paths: dict, npc_texture_path: str):
        self.map_manager = MapManager(map_path, tile_textures_paths)
        self.npc_manager = NPCManager(self.map_manager.tile_size, npc_texture_path)
        self.physics_manager = PhysicsManager(self.map_manager, self.npc_manager)

    # ------------------------------------------------------------------ #
    # Interfaccia esposta agli attori del mondo (NPC, futuro Player)
    # ------------------------------------------------------------------ #

    def can_move_to(self, col: int, row: int, mover=None) -> bool:
        """Unico modo, per qualsiasi entità, di chiedere il permesso di spostarsi."""
        return self.physics_manager.can_move_to(col, row, mover=mover)

    def get_map_dimensions(self) -> tuple:
        """
        Espone solo ciò che serve (dimensioni in celle), senza dare accesso
        diretto a MapManager: gli NPC non devono mai leggere la grid a mano.
        """
        return self.map_manager.cols, self.map_manager.rows

    def spawn_npc(self, col: int, row: int):
        return self.npc_manager.spawn_npc(col, row)

    def despawn_npc(self, npc):
        self.npc_manager.despawn_npc(npc)

    # ------------------------------------------------------------------ #
    # Ciclo di vita per frame (chiamato da main.py)
    # ------------------------------------------------------------------ #

    def update(self, dt: float):
        self.npc_manager.update(dt, self)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.map_manager.get_map_surface(), (0, 0))
        self.npc_manager.draw(screen)
