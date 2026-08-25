import pygame

from entities.npc import NPC


class NPCManager:
    """
    L'Ufficio Anagrafe.

    Possiede la lista di TUTTI gli NPC vivi nel mondo ed è l'unico modulo
    autorizzato a modificarla (spawn/despawn). Espone anche la risposta alla
    domanda "questa tile è occupata da un NPC?", usata da PhysicsManager.

    Comunicazione:
      - Viene interrogato da PhysicsManager per i controlli dinamici di collisione.
      - Viene chiamato da WorldManager una volta per frame per update()/draw()
        di tutti gli NPC in blocco.
      - Ogni singolo NPC non conosce NPCManager: comunica solo con la
        facade WorldManager (vedi entities/npc.py).
    """

    def __init__(self, tile_size: int, npc_texture_path: str):
        self.tile_size = tile_size
        self.npc_texture = self._load_texture(npc_texture_path)

        self.npcs = []
        self._next_id = 0

    def _load_texture(self, path: str) -> pygame.Surface:
        try:
            image = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(image, (self.tile_size, self.tile_size))
        except pygame.error as e:
            raise RuntimeError(f"NPCManager: errore caricamento texture NPC: {e}")

    # ------------------------------------------------------------------ #
    # Spawn / Despawn
    # ------------------------------------------------------------------ #

    def spawn_npc(self, col: int, row: int) -> NPC:
        npc = NPC(
            npc_id=self._next_id,
            col=col,
            row=row,
            tile_size=self.tile_size,
            texture=self.npc_texture,
        )
        self._next_id += 1
        self.npcs.append(npc)
        return npc

    def despawn_npc(self, npc: NPC):
        if npc in self.npcs:
            self.npcs.remove(npc)

    # ------------------------------------------------------------------ #
    # Query dinamiche (usate da PhysicsManager)
    # ------------------------------------------------------------------ #

    def is_tile_occupied(self, col: int, row: int, excluding: NPC = None) -> bool:
        for npc in self.npcs:
            if npc is excluding:
                continue
            if npc.col == col and npc.row == row:
                return True
        return False

    # ------------------------------------------------------------------ #
    # Ciclo di vita per frame (chiamato da WorldManager)
    # ------------------------------------------------------------------ #

    def update(self, dt: float, world):
        for npc in self.npcs:
            npc.update(dt, world)

    def draw(self, surface: pygame.Surface):
        for npc in self.npcs:
            npc.draw(surface)
